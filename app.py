
from flask import Flask, render_template
import sqlite3
import config

app = Flask(__name__)


@app.route("/")
def dashboard():
    with sqlite3.connect(config.DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        total_events = conn.execute(
            "SELECT COUNT(*) FROM leak_logs"
        ).fetchone()[0]

        total_risk = conn.execute(
            "SELECT COALESCE(SUM(risk_score), 0) FROM leak_logs"
        ).fetchone()[0]

        recent_logs = conn.execute("""
            SELECT id, timestamp, file_path,
                   detected_keywords, risk_score
            FROM leak_logs
            ORDER BY id DESC
            LIMIT 100
        """).fetchall()

    return render_template(
        "index.html",
        total_events=total_events,
        total_risk=total_risk,
        recent_logs=recent_logs
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
