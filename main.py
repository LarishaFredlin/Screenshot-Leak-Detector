
import config
import database
from monitor import start_monitoring


def main():
    print("=" * 50)
    print(" REAL-TIME SCREENSHOT LEAK DETECTOR")
    print("=" * 50)

    database.setup_database()

    print(f"[INFO] Database: {config.DB_PATH}")
    print(f"[INFO] Monitoring folder: {config.MONITOR_FOLDER}")

    start_monitoring()


if __name__ == "__main__":
    main()
