import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parent / "submissions.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT NOT NULL,
                file_id TEXT NOT NULL,
                file_unique_id TEXT NOT NULL UNIQUE,
                file_type TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        connection.commit()
    logger.info("Database initialized at %s", DB_PATH)


def insert_submission(
    user_id: int,
    username: str | None,
    full_name: str,
    file_id: str,
    file_unique_id: str,
    file_type: str,
) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO submissions (
                user_id,
                username,
                full_name,
                file_id,
                file_unique_id,
                file_type,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                full_name,
                file_id,
                file_unique_id,
                file_type,
                timestamp,
            ),
        )
        connection.commit()


def is_duplicate(file_unique_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT 1
            FROM submissions
            WHERE file_unique_id = ?
            LIMIT 1
            """,
            (file_unique_id,),
        )
        row = cursor.fetchone()
    return row is not None


def get_submission_count(user_id: int, since_timestamp: str) -> int:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT COUNT(*)
            FROM submissions
            WHERE user_id = ?
              AND timestamp >= ?
            """,
            (user_id, since_timestamp),
        )
        row = cursor.fetchone()

    return int(row[0]) if row else 0
