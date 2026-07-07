import sqlite3
from collections import namedtuple
import numpy as np
from typing import Any, List, Optional, Tuple

from timeseek.config import db_path

# Define the structure of a database entry using namedtuple
Entry = namedtuple("Entry", ["id", "app", "title", "text", "timestamp", "embedding", "filename"])


def create_db() -> None:
    """
    Creates the SQLite database and the 'entries' table if they don't exist.
    Also handles schema migrations (adding 'filename' column).
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS entries (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       app TEXT,
                       title TEXT,
                       text TEXT,
                       timestamp INTEGER UNIQUE,
                       embedding BLOB
                   )"""
            )
            # Migration: Add filename column if it doesn't exist
            cursor.execute("PRAGMA table_info(entries)")
            columns = [column[1] for column in cursor.fetchall()]
            if "filename" not in columns:
                print("Migrating database: Adding 'filename' column.")
                cursor.execute("ALTER TABLE entries ADD COLUMN filename TEXT")

            # Add index on timestamp for faster lookups
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_timestamp ON entries (timestamp)"
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during table creation: {e}")


def get_all_entries() -> List[Entry]:
    """
    Retrieves all entries from the database.
    """
    entries: List[Entry] = []
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, app, title, text, timestamp, embedding, filename FROM entries ORDER BY timestamp DESC")
            results = cursor.fetchall()
            for row in results:
                embedding = np.frombuffer(row["embedding"], dtype=np.float32)
                entries.append(
                    Entry(
                        id=row["id"],
                        app=row["app"],
                        title=row["title"],
                        text=row["text"],
                        timestamp=row["timestamp"],
                        embedding=embedding,
                        filename=row["filename"],
                    )
                )
    except sqlite3.Error as e:
        print(f"Database error while fetching all entries: {e}")
    return entries


def get_timestamps() -> List[dict]:
    """
    Retrieves all timestamps and filenames from the database, ordered descending.
    Returns a list of dictionaries with 'timestamp' and 'filename'.
    """
    data = []
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, filename FROM entries ORDER BY timestamp DESC")
            results = cursor.fetchall()
            data = [{"timestamp": r["timestamp"], "filename": r["filename"]} for r in results]
    except sqlite3.Error as e:
        print(f"Database error while fetching timestamps: {e}")
    return data


def insert_entry(
    text: str, timestamp: int, embedding: np.ndarray, app: str, title: str, filename: str
) -> Optional[int]:
    """
    Inserts a new entry into the database.
    """
    embedding_bytes: bytes = embedding.astype(np.float32).tobytes()
    last_row_id: Optional[int] = None
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO entries (text, timestamp, embedding, app, title, filename)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(timestamp) DO NOTHING""",
                (text, timestamp, embedding_bytes, app, title, filename),
            )
            conn.commit()
            if cursor.rowcount > 0:
                last_row_id = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error during insertion: {e}")
    return last_row_id
