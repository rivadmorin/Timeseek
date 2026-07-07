import pytest
import os
import sqlite3
import numpy as np
from timeseek.database import insert_entry, delete_entry, create_db
from timeseek.config import db_path, screenshots_path

@pytest.fixture
def setup_db():
    create_db()
    yield
    if os.path.exists(db_path):
        os.remove(db_path)

def test_delete_entry(setup_db):
    embedding = np.zeros(384, dtype=np.float32)
    filename = "test_delete.webp"

    # Insert
    entry_id = insert_entry("test text", 123456789, embedding, "TestApp", "TestTitle", filename)
    assert entry_id is not None

    # Verify it exists
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM entries WHERE id = ?", (entry_id,))
        assert cursor.fetchone() is not None

    # Delete
    result = delete_entry(entry_id)
    assert result is True

    # Verify it's gone
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM entries WHERE id = ?", (entry_id,))
        assert cursor.fetchone() is None

def test_delete_nonexistent_entry(setup_db):
    result = delete_entry(99999)
    assert result is False
