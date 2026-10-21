
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config
import ocr_engine
import detector
import database
import alert


class ScreenshotHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path

        if filepath.lower().endswith(config.IMAGE_EXTENSIONS):
            print(f"\n[INFO] New image detected: {filepath}")
            self.process_image(filepath)

    def on_moved(self, event):
        # Handle images moved into the monitored folder.
        if event.is_directory:
            return

        filepath = event.dest_path

        if filepath.lower().endswith(config.IMAGE_EXTENSIONS):
            print(f"\n[INFO] Image moved into folder: {filepath}")
            self.process_image(filepath)

    def process_image(self, filepath):
        # Wait until the image has finished being written.
        for _ in range(10):
            if os.path.isfile(filepath):
                try:
                    size1 = os.path.getsize(filepath)
                    time.sleep(0.5)
                    size2 = os.path.getsize(filepath)

                    if size1 > 0 and size1 == size2:
                        break

                except OSError:
                    pass

            time.sleep(0.5)

        else:
            print("[WARNING] Image is not ready or is unavailable.")
            return

        # Calculate the image fingerprint.
        file_hash = database.calculate_file_hash(filepath)

        if not file_hash:
            print("[WARNING] Could not identify screenshot. Skipping.")
            return

        # Skip images that have already generated a detection log.
        if database.is_duplicate(file_hash):
            print(
                "[INFO] Duplicate screenshot detected. "
                "Skipping OCR and alert."
            )
            return

        # Extract text using OCR.
        print("[INFO] Extracting text with OCR...")
        text = ocr_engine.extract_text(filepath)

        if not text:
            print("[INFO] No readable text found.")
            return

        # Check the extracted text for sensitive keywords.
        keywords = detector.check_keywords(text)

        if keywords:
            print(f"[ALERT] Sensitive keywords found: {keywords}")

            # Save the event only if it is not a duplicate.
            saved = database.log_event(filepath, keywords)

            # Send an alert only when the event was saved.
            if saved:
                alert.show_alert(filepath, keywords)

        else:
            print("[INFO] No configured sensitive keywords found.")


def start_monitoring():
    os.makedirs(config.MONITOR_FOLDER, exist_ok=True)

    handler = ScreenshotHandler()
    observer = Observer()

    observer.schedule(
        handler,
        config.MONITOR_FOLDER,
        recursive=False
    )

    observer.start()

    print("=" * 50)
    print(" REAL-TIME SCREENSHOT LEAK DETECTOR")
    print("=" * 50)
    print(f"[INFO] Monitoring: {config.MONITOR_FOLDER}")
    print("[INFO] Duplicate prevention enabled.")
    print("[INFO] Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Stopping monitor...")

    finally:
        observer.stop()
        observer.join()
       