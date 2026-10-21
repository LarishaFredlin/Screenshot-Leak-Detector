
import subprocess

def show_alert(file_path, keywords):
    title = "Screenshot Leak Detector"
    message = "Sensitive keywords: " + ", ".join(keywords)

    # Escape strings for AppleScript
    title = title.replace("\\", "\\\\").replace('"', '\\"')
    message = message.replace("\\", "\\\\").replace('"', '\\"')

    script = (
        f'display notification "{message}" '
        f'with title "{title}"'
    )

    try:
        subprocess.run(
            ["osascript", "-e", script],
            check=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        print("[INFO] Notification command completed.")
    except (subprocess.SubprocessError, OSError) as error:
        print(f"[WARNING] Notification failed: {error}")
