
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder for screenshots captured using macOS Screenshot
MONITOR_FOLDER = os.path.expanduser(
    "~/Desktop/MonitoredScreenshots"
)

DB_PATH = os.path.join(BASE_DIR, "leak_logs.db")

SENSITIVE_KEYWORDS = [
    "password",
    "confidential",
    "salary",
    "credit card",
    "bank account",
    "customer",
    "secret"
]

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")

OCR_CONFIG = "--oem 3 --psm 6"

os.makedirs(MONITOR_FOLDER, exist_ok=True)
