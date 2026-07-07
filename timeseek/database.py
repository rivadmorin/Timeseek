import sqlite3
from collections import namedtuple
import numpy as np
from typing import Any, List, Optional, Tuple

from timeseek.config import db_path

# Define the structure of a database entry using namedtuple
Entry = namedtuple("Entry", ["id", "app", "title", "text", "timestamp", "embedding", "filename", "notes"])


def create_db() -> None:
    """
    Creates the SQLite database and the 'entries' table if they don't exist.
    Also handles schema migrations (adding 'filename' and 'notes' columns).
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
            # Migration: Add columns if they don't exist
            cursor.execute("PRAGMA table_info(entries)")
            columns = [column[1] for column in cursor.fetchall()]

            if "filename" not in columns:
                print("Migrating database: Adding 'filename' column.")
                cursor.execute("ALTER TABLE entries ADD COLUMN filename TEXT")

            if "notes" not in columns:
                print("Migrating database: Adding 'notes' column.")
                cursor.execute("ALTER TABLE entries ADD COLUMN notes TEXT DEFAULT ''")

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
            cursor.execute("SELECT id, app, title, text, timestamp, embedding, filename, notes FROM entries ORDER BY timestamp DESC")
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
                        notes=row["notes"] or ""
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
    text: str, timestamp: int, embedding: np.ndarray, app: str, title: str, filename: str, notes: str = ""
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
                """INSERT INTO entries (text, timestamp, embedding, app, title, filename, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(timestamp) DO NOTHING""",
                (text, timestamp, embedding_bytes, app, title, filename, notes),
            )
            conn.commit()
            if cursor.rowcount > 0:
                last_row_id = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error during insertion: {e}")
    return last_row_id

def update_entry_notes(entry_id: int, notes: str) -> bool:
    """
    Updates the notes for a specific entry.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE entries SET notes = ? WHERE id = ?", (notes, entry_id))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error during notes update: {e}")
        return False

def delete_entry(entry_id: int) -> bool:
    """
    Deletes an entry from the database by its ID.
    Returns True if an entry was deleted, False otherwise.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error during deletion: {e}")
        return False

def prune_old_data(retention_days: int) -> int:
    """
    Deletes entries older than retention_days.
    Returns the number of deleted records.
    """
    import time
    import os
    from timeseek.config import screenshots_path

    cutoff_timestamp = int(time.time()) - (retention_days * 86400)
    deleted_count = 0

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Find filenames to delete from disk
            cursor.execute("SELECT filename FROM entries WHERE timestamp < ?", (cutoff_timestamp,))
            files_to_delete = cursor.fetchall()

            for row in files_to_delete:
                if row["filename"]:
                    filepath = os.path.join(screenshots_path, row["filename"])
                    if os.path.exists(filepath):
                        try:
                            os.remove(filepath)
                        except Exception as e:
                            print(f"Failed to delete file {filepath}: {e}")

            # Delete from database
            cursor.execute("DELETE FROM entries WHERE timestamp < ?", (cutoff_timestamp,))
            deleted_count = cursor.rowcount
            conn.commit()

            if deleted_count > 0:
                print(f"Auto-pruning: Deleted {deleted_count} entries older than {retention_days} days.")

    except sqlite3.Error as e:
        print(f"Database error during pruning: {e}")

    return deleted_count

def delete_entries_by_range(start_timestamp: int, end_timestamp: int) -> int:
    """
    Deletes entries within a specific timestamp range.
    Returns the number of deleted records.
    """
    import os
    from timeseek.config import screenshots_path

    deleted_count = 0
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Find filenames to delete from disk
            cursor.execute("SELECT filename FROM entries WHERE timestamp >= ? AND timestamp <= ?", (start_timestamp, end_timestamp))
            files_to_delete = cursor.fetchall()

            for row in files_to_delete:
                if row["filename"]:
                    filepath = os.path.join(screenshots_path, row["filename"])
                    if os.path.exists(filepath):
                        try:
                            os.remove(filepath)
                        except Exception as e:
                            print(f"Failed to delete file {filepath}: {e}")

            # Delete from database
            cursor.execute("DELETE FROM entries WHERE timestamp >= ? AND timestamp <= ?", (start_timestamp, end_timestamp))
            deleted_count = cursor.rowcount
            conn.commit()

    except sqlite3.Error as e:
        print(f"Database error during range deletion: {e}")

    return deleted_count
