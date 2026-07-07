import pytest
from timeseek.app import cached_entries, cache_lock
from collections import namedtuple
import time

Entry = namedtuple("Entry", ["id", "app", "title", "text", "timestamp", "embedding", "filename", "notes"])

def test_layout_structure(client):
    """Verify that layout.html includes necessary M3 stylesheets and structural elements."""
    response = client.get('/dashboard')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'm3-tokens.css' in html
    assert 'custom.css' in html
    assert 'nav-rail' in html
    assert 'theme-toggle' in html

def test_theme_toggle_persistence_script(client):
    """Verify the theme toggle script exists and handles localStorage."""
    response = client.get('/dashboard')
    html = response.data.decode('utf-8')
    assert 'function toggleTheme()' in html
    assert "localStorage.setItem('theme', newTheme)" in html
    assert "localStorage.getItem('theme')" in html

def test_dashboard_components(client):
    """Verify dashboard specific components are present."""
    response = client.get('/dashboard')
    html = response.data.decode('utf-8')
    assert 'id="heatmap"' in html
    assert 'id="wordcloud"' in html
    assert 'Bulk Delete' in html
    assert 'Full Purge' in html

def test_api_heatmap_empty(client):
    """Verify heatmap API returns empty dict when no data."""
    with cache_lock:
        cached_entries.clear()
    response = client.get('/api/heatmap')
    assert response.status_code == 200
    assert response.json == {}

def test_api_wordcloud_empty(client):
    """Verify wordcloud API returns empty list when no data."""
    with cache_lock:
        cached_entries.clear()
    response = client.get('/api/wordcloud')
    assert response.status_code == 200
    assert response.json == []
