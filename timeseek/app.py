import re
import json
import os
import shutil
from collections import Counter
from datetime import datetime
from threading import Thread, Lock

import numpy as np
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify

from timeseek.config import appdata_folder, screenshots_path, db_path, args, ACTIVE_SLEEP, RETENTION_DAYS
from timeseek.database import create_db, get_all_entries, delete_entry, update_entry_notes, prune_old_data, delete_entries_by_range
from timeseek.nlp import batch_cosine_similarity, get_embedding
from timeseek.screenshot import record_screenshots_thread
from timeseek.utils import human_readable_time, timestamp_to_human_readable, get_app_category

app = Flask(__name__)

app.jinja_env.filters["human_readable_time"] = human_readable_time
app.jinja_env.filters["timestamp_to_human_readable"] = timestamp_to_human_readable
app.jinja_env.globals.update(get_app_category=get_app_category)

# Global cache for entries to speed up search and dashboard
cached_entries = []
cache_lock = Lock()

def refresh_cache():
    """Reloads entries from the database into the global cache."""
    global cached_entries
    new_entries = get_all_entries()
    with cache_lock:
        cached_entries = new_entries

@app.route("/")
def index():
    """Redirects to the dashboard view."""
    return redirect(url_for('dashboard'))


@app.route("/dashboard")
def dashboard():
    """Renders the dashboard with usage statistics."""
    with cache_lock:
        entries = list(cached_entries)

    total_snapshots = len(entries)
    total_time_seconds = total_snapshots * ACTIVE_SLEEP
    total_time_human = human_readable_time(total_time_seconds)

    app_counts = Counter(e.app for e in entries if e.app)
    top_apps = app_counts.most_common(5)

    hourly_counts = Counter()
    for e in entries:
        dt = datetime.fromtimestamp(e.timestamp)
        hourly_counts[dt.hour] += 1

    hourly_activity = []
    for h in range(24):
        hourly_activity.append((h, hourly_counts[h]))

    max_hourly = max(hourly_counts.values()) if hourly_counts else 0

    return render_template("dashboard.html",
                           total_snapshots=total_snapshots,
                           total_time_human=total_time_human,
                           top_apps=top_apps,
                           hourly_activity=hourly_activity,
                           max_hourly=max_hourly)


@app.route("/timeline")
def timeline():
    """Renders the timeline view showing all recorded moments."""
    app_filter = request.args.get("app", "")
    with cache_lock:
        entries = list(cached_entries)

    if app_filter:
        entries = [e for e in entries if e.app == app_filter]

    entries_json = json.dumps([
        {
            "timestamp": e.timestamp,
            "filename": e.filename,
            "app": e.app,
            "title": e.title,
            "notes": e.notes,
            "category": get_app_category(e.app or "")
        } for e in entries
    ])
    return render_template("timeline.html", entries=entries, entries_json=entries_json)


@app.route("/search")
def search():
    """Handles search queries using vectorized similarity search with optional filtering."""
    q = request.args.get("q", "")
    app_filter = request.args.get("app", "")

    with cache_lock:
        entries = list(cached_entries)

    apps = sorted(list(set(e.app for e in entries if e.app)))

    # Apply app filter first if present
    if app_filter:
        entries = [e for e in entries if e.app == app_filter]

    if not q:
        return render_template("search.html", entries=entries, apps=apps, current_app=app_filter)

    if not entries:
         return render_template("search.html", entries=[], apps=[], current_app=app_filter)

    # Optimization: Use vectorized matrix multiplication for similarity search
    query_embedding = get_embedding(q)
    embeddings_matrix = np.array([entry.embedding for entry in entries], dtype=np.float32)

    similarities = batch_cosine_similarity(query_embedding, embeddings_matrix)
    indices = np.argsort(similarities)[::-1]
    sorted_entries = [entries[i] for i in indices]

    return render_template("search.html", entries=sorted_entries, apps=apps, current_app=app_filter)


@app.route("/update_note/<int:entry_id>", methods=["POST"])
def update_note(entry_id):
    """Updates the notes for a specific entry and refreshes the cache."""
    notes = request.json.get("notes", "")
    if update_entry_notes(entry_id, notes):
        refresh_cache()
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Entry not found"}), 404


@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete(entry_id):
    """Deletes a specific entry, its image, and refreshes the cache."""
    with cache_lock:
        entry = next((e for e in cached_entries if e.id == entry_id), None)

    if entry:
        # Delete image file
        image_path = os.path.join(screenshots_path, entry.filename)
        if os.path.exists(image_path):
            os.remove(image_path)

        # Delete DB record
        if delete_entry(entry_id):
            refresh_cache()
            return jsonify({"success": True})

    return jsonify({"success": False, "error": "Entry not found"}), 404


@app.route("/bulk_delete", methods=["POST"])
def bulk_delete():
    import time
    hours = int(request.form.get("range", 0))
    if hours > 0:
        end = int(time.time())
        start = end - (hours * 3600)
        delete_entries_by_range(start, end)
        refresh_cache()
    return redirect(url_for("dashboard"))


@app.route("/purge", methods=["POST"])
def purge():
    """Deletes all screenshots and the database."""
    if os.path.exists(screenshots_path):
        shutil.rmtree(screenshots_path)
    os.makedirs(screenshots_path, exist_ok=True)

    if os.path.exists(db_path):
        os.remove(db_path)

    create_db()
    refresh_cache()
    return redirect(url_for('dashboard'))


@app.route("/static/<filename>")
def serve_image(filename):
    """Serves recorded screenshots from the appdata directory."""
    return send_from_directory(screenshots_path, filename)

@app.route("/api/heatmap")
def heatmap_api():
    """Returns activity intensity data for the heatmap."""
    with cache_lock:
        entries = list(cached_entries)

    counts = Counter()
    for e in entries:
        day = datetime.fromtimestamp(e.timestamp).strftime("%Y-%m-%d")
        counts[day] += 1

    return jsonify(counts)

@app.route("/api/wordcloud")
def wordcloud_api():
    """Returns top keywords from OCR text."""
    with cache_lock:
        entries = list(cached_entries)

    words = []
    # Stop words (very basic list)
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "is", "are", "was", "were", "of", "it", "that", "this"}

    for e in entries:
        if e.text:
            # Simple word extraction
            extracted = re.findall(r'\w{4,}', e.text.lower())
            words.extend([w for w in extracted if w not in stop_words])

    top_words = Counter(words).most_common(50)
    return jsonify([{"text": w, "size": c} for w, c in top_words])

@app.route("/export/pdf/<int:entry_id>")
def export_pdf(entry_id):
    """Exports a single entry to a basic PDF-like HTML page for printing."""
    with cache_lock:
        entry = next((e for e in cached_entries if e.id == entry_id), None)

    if not entry:
        return "Entry not found", 404

    return render_template("export_pdf.html", entry=entry)

if __name__ == "__main__":
    create_db()

    # Run auto-pruning on startup
    prune_old_data(RETENTION_DAYS)

    refresh_cache()

    print(f"Appdata folder: {appdata_folder}")
    print(f"Starting server on port: {args.port}")

    # Start the recording thread with the cache refresh callback
    t = Thread(target=record_screenshots_thread, args=(refresh_cache,), daemon=True)
    t.start()

    app.run(port=args.port)
