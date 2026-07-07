import pytest
import os
import time
from collections import namedtuple

# Set testing environment variable BEFORE importing app
os.environ["FLASK_ENV"] = "testing"

from timeseek.app import app as flask_app, cached_entries, cache_lock

Entry = namedtuple("Entry", ["id", "app", "title", "text", "timestamp", "embedding", "filename", "notes"])

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True

    # Seed mock data
    with cache_lock:
        cached_entries.clear()
        cached_entries.append(Entry(1, "TestApp", "TestTitle", "TestText", int(time.time()), None, "test.webp", "test notes"))

    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()
