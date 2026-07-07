import os
import sqlite3
import time
import unittest
from collections import namedtuple

import numpy as np

# Ensure we're testing the local version
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from timeseek.database import create_db, insert_entry, get_all_entries, get_timestamps, Entry
from timeseek.config import appdata_folder, db_path

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Clean up database before each test."""
        if os.path.exists(db_path):
            os.remove(db_path)
        create_db()

    def tearDown(self):
        """Clean up database after each test."""
        if os.path.exists(db_path):
             os.remove(db_path)

    def test_01_create_db(self):
        """Test database and table creation."""
        self.assertTrue(os.path.exists(db_path))
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entries'")
            self.assertIsNotNone(cursor.fetchone())

            # Check for filename column
            cursor.execute("PRAGMA table_info(entries)")
            columns = [column[1] for column in cursor.fetchall()]
            self.assertIn("filename", columns)

    def test_02_insert_entry(self):
        """Test inserting a single entry."""
        ts = int(time.time())
        embedding = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        filename = f"{ts}_0.webp"
        inserted_id = insert_entry("Test text", ts, embedding, "TestApp", "TestTitle", filename)
        self.assertIsNotNone(inserted_id)

        entries = get_all_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].text, "Test text")
        self.assertEqual(entries[0].timestamp, ts)
        self.assertTrue(np.array_equal(entries[0].embedding, embedding))
        self.assertEqual(entries[0].app, "TestApp")
        self.assertEqual(entries[0].title, "TestTitle")
        self.assertEqual(entries[0].filename, filename)

    def test_insert_duplicate_timestamp(self):
        """Test inserting an entry with a duplicate timestamp (should be ignored)."""
        ts = int(time.time())
        embedding1 = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        embedding2 = np.array([0.4, 0.5, 0.6], dtype=np.float32)
        filename1 = "file1.webp"
        filename2 = "file2.webp"

        id1 = insert_entry("First text", ts, embedding1, "App1", "Title1", filename1)
        self.assertIsNotNone(id1)

        id2 = insert_entry("Second text", ts, embedding2, "App2", "Title2", filename2)
        self.assertIsNone(id2) # Should be None because of ON CONFLICT DO NOTHING

        entries = get_all_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].text, "First text")

    def test_get_all_entries_empty(self):
        """Test get_all_entries with an empty database."""
        entries = get_all_entries()
        self.assertEqual(len(entries), 0)

    def test_get_all_entries_multiple(self):
        """Test retrieving multiple entries."""
        ts1 = int(time.time())
        ts2 = ts1 + 10
        ts3 = ts1 - 10
        emb1 = np.array([0.1] * 5, dtype=np.float32)
        emb2 = np.array([0.2] * 5, dtype=np.float32)
        emb3 = np.array([0.3] * 5, dtype=np.float32)

        insert_entry("Text 1", ts1, emb1, "App1", "Title1", "f1.webp")
        insert_entry("Text 2", ts2, emb2, "App2", "Title2", "f2.webp")
        insert_entry("Text 3", ts3, emb3, "App3", "Title3", "f3.webp")

        entries = get_all_entries()
        self.assertEqual(len(entries), 3)
        # Should be ordered by timestamp DESC
        self.assertEqual(entries[0].timestamp, ts2)
        self.assertEqual(entries[1].timestamp, ts1)
        self.assertEqual(entries[2].timestamp, ts3)

    def test_get_timestamps_multiple(self):
        """Test retrieving multiple timestamps."""
        ts1 = int(time.time())
        ts2 = ts1 + 10
        ts3 = ts1 - 10
        emb = np.array([0.1] * 5, dtype=np.float32)

        insert_entry("T1", ts1, emb, "A1", "T1", "f1.webp")
        insert_entry("T2", ts2, emb, "A2", "T2", "f2.webp")
        insert_entry("T3", ts3, emb, "A3", "T3", "f3.webp")

        timestamps_data = get_timestamps()
        self.assertEqual(len(timestamps_data), 3)
        self.assertEqual(timestamps_data[0]['timestamp'], ts2)
        self.assertEqual(timestamps_data[1]['timestamp'], ts1)
        self.assertEqual(timestamps_data[2]['timestamp'], ts3)
        self.assertEqual(timestamps_data[0]['filename'], "f2.webp")

if __name__ == '__main__':
    unittest.main()
