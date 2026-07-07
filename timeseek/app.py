import json
import os
import shutil
from collections import Counter
from datetime import datetime
from threading import Thread, Lock

import numpy as np
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify

from timeseek.config import appdata_folder, screenshots_path, db_path, args, ACTIVE_SLEEP
from timeseek.database import create_db, get_all_entries, delete_entry
from timeseek.nlp import batch_cosine_similarity, get_embedding
from timeseek.screenshot import record_screenshots_thread
from timeseek.utils import human_readable_time, timestamp_to_human_readable

app = Flask(__name__)

app.jinja_env.filters["human_readable_time"] = human_readable_time
app.jinja_env.filters["timestamp_to_human_readable"] = timestamp_to_human_readable

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
    with cache_lock:
        entries = list(cached_entries)

    entries_json = json.dumps([
        {
            "timestamp": e.timestamp,
            "filename": e.filename,
            "app": e.app,
            "title": e.title
        } for e in entries
    ])
    return render_template("timeline.html", entries=entries, entries_json=entries_json)


@app.route("/search")
def search():
    """Handles search queries using vectorized similarity search."""
    q = request.args.get("q", "")
    with cache_lock:
        entries = list(cached_entries)

    apps = sorted(list(set(e.app for e in entries if e.app)))

    if not q:
        return render_template("search.html", entries=entries, apps=apps)

    if not entries:
         return render_template("search.html", entries=[], apps=[])

    # Optimization: Use vectorized matrix multiplication for similarity search
    query_embedding = get_embedding(q)
    embeddings_matrix = np.array([entry.embedding for entry in entries], dtype=np.float32)

    similarities = batch_cosine_similarity(query_embedding, embeddings_matrix)
    indices = np.argsort(similarities)[::-1]
    sorted_entries = [entries[i] for i in indices]

    return render_template("search.html", entries=sorted_entries, apps=apps)


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


if __name__ == "__main__":
    create_db()
    refresh_cache()

    print(f"Appdata folder: {appdata_folder}")
    print(f"Starting server on port: {args.port}")

    # Start the recording thread with the cache refresh callback
    t = Thread(target=record_screenshots_thread, args=(refresh_cache,), daemon=True)
    t.start()

    app.run(port=args.port)
