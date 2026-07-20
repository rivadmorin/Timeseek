import pytest
from timeseek.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_dashboard_route(client):
    """Test that the dashboard route returns 200."""
    rv = client.get('/dashboard')
    assert rv.status_code == 200
    assert b'Daily Dashboard' in rv.data

def test_purge_route(client):
    """Test that the purge route redirects back to dashboard."""
    rv = client.post('/purge')
    assert rv.status_code == 302
    assert '/dashboard' in rv.headers['Location']

def test_index_route(client):
    rv = client.get('/')
    assert rv.status_code == 302
    assert '/dashboard' in rv.headers['Location']

def test_timeline_route(client):
    rv = client.get('/timeline')
    assert rv.status_code == 200

def test_search_route(client):
    rv = client.get('/search')
    assert rv.status_code == 200

def test_api_heatmap(client):
    rv = client.get('/api/heatmap')
    assert rv.status_code == 200

def test_api_wordcloud(client):
    rv = client.get('/api/wordcloud')
    assert rv.status_code == 200
