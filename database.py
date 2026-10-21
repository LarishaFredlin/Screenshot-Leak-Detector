
import sqlite3
import hashlib
from datetime import datetime

import config


def setup_database():
    with sqlite3.connect(config.DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leak_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                file_path TEXT NOT NULL,
                detected_keywords TEXT NOT NULL,
                risk_score INTEGER NOT NULL
            )
        """)

        # Add a fingerprint column to existing databases.
        columns = {
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(leak_logs)"
            ).fetchall()
        }

        if "file_hash" not in columns:
            conn.execute(
                "ALTER TABLE leak_logs ADD COLUMN file_hash TEXT"
            )


def calculate_file_hash(file_path):
    """Return a SHA-256 fingerprint of the image file."""
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as image_file:
            for chunk in iter(
                lambda: image_file.read(1024 * 1024), b""
            ):
                sha256.update(chunk)

        return sha256.hexdigest()

    except OSError as error:
        print(f"[ERROR] Could not hash image: {error}")
        return None


def is_duplicate(file_hash):
    """Check whether this image has already been logged."""
    if not file_hash:
        return False

    with sqlite3.connect(config.DB_PATH) as conn:
        result = conn.execute(
            "SELECT 1 FROM leak_logs WHERE file_hash = ? LIMIT 1",
            (file_hash,)
        ).fetchone()

    return result is not None


def log_event(file_path, keywords):
    """Log a detection unless the same image is already recorded."""
    file_hash = calculate_file_hash(file_path)

    if not file_hash:
        print("[WARNING] Event not logged because hashing failed.")
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keywords_text = ", ".join(keywords)
    risk_score = len(keywords)

    with sqlite3.connect(config.DB_PATH) as conn:
        # Check and insert in the same database transaction.
        existing = conn.execute(
            "SELECT 1 FROM leak_logs WHERE file_hash = ? LIMIT 1",
            (file_hash,)
        ).fetchone()

        if existing:
            print("[INFO] Duplicate screenshot. Event not logged.")
            return False

        conn.execute("""
            INSERT INTO leak_logs
            (timestamp, file_path, detected_keywords, risk_score, file_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (
            timestamp,
            file_path,
            keywords_text,
            risk_score,
            file_hash
        ))

    print(f"[LOG] Event saved. Risk score: {risk_score}")
    return True
