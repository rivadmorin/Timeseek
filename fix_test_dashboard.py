import re

with open('tests/test_dashboard.py', 'r') as f:
    content = f.read()

# Add mock patch for 'timeseek.app.cached_entries' and 'timeseek.app.update_entry_notes'
# or remove the references depending on what the error is in dashboard test. Wait, the dashboard test didn't fail earlier.
# But just in case, I should check the PR comments to see what they say!
