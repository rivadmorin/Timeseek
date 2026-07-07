import pytest
import numpy as np
from timeseek.app import app
from timeseek.database import Entry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_no_query(client):
    response = client.get('/search')
    assert response.status_code == 200
    assert b"Search" in response.data

def test_search_with_query(client, mocker):
    # Mock database and NLP to avoid side effects
    # Using namedtuple or similar that can be accessed via entry['timestamp']
    class MockEntry(dict):
        def __init__(self, id, app, title, text, timestamp, embedding):
            super().__init__(id=id, app=app, title=title, text=text, timestamp=timestamp, embedding=embedding)
            self.id = id
            self.app = app
            self.title = title
            self.text = text
            self.timestamp = timestamp
            self.embedding = embedding

    mock_entries = [
        MockEntry(1, "App1", "Title1", "Text1", 100, np.array([1, 0, 0], dtype=np.float32)),
        MockEntry(2, "App2", "Title2", "Text2", 200, np.array([0, 1, 0], dtype=np.float32))
    ]
    mocker.patch('timeseek.app.get_all_entries', return_value=mock_entries)
    mocker.patch('timeseek.app.get_embedding', return_value=np.array([1, 0, 0], dtype=np.float32))

    response = client.get('/search?q=test')
    assert response.status_code == 200
    assert b"100.webp" in response.data
    assert b"200.webp" in response.data
