import pytest
from unittest.mock import patch, MagicMock
from timeseek.app import app, cached_entries
from timeseek.database import Entry
import numpy as np

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_timeline_with_entries(client):
    # This is a bit tricky to mock a global list that is accessed within the lock
    # We can just append to the real cached_entries for testing, and clear it afterwards
    global cached_entries
    entry = Entry(id=1, app="TestApp", title="TestTitle", text="Some text",
                 timestamp=1000, embedding=np.zeros(384), filename="test.webp", notes="note", is_favorite=False)

    # We need to import the real cached_entries from the module to modify it directly
    import timeseek.app as flask_app
    flask_app.cached_entries.clear()
    flask_app.cached_entries.append(entry)

    rv = client.get('/timeline?app=TestApp')
    assert rv.status_code == 200
    assert b"TestApp" in rv.data

    rv = client.get('/search?q=test')
    assert rv.status_code == 200

    flask_app.cached_entries.clear()

@patch('timeseek.app.update_entry_notes')
def test_update_note(mock_update, client):
    mock_update.return_value = True
    rv = client.post('/update_note/1', json={'notes': 'new note'})
    assert rv.status_code == 200
    assert rv.json['success'] == True

    mock_update.return_value = False
    rv = client.post('/update_note/999', json={'notes': 'new note'})
    assert rv.status_code == 404

def test_delete_entry_not_found(client):
    rv = client.post('/delete/999')
    assert rv.status_code == 404
