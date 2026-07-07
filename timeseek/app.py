from threading import Thread

import numpy as np
from flask import Flask, render_template, request, send_from_directory

from timeseek.config import appdata_folder, screenshots_path, args
from timeseek.database import create_db, get_all_entries, get_timestamps
from timeseek.nlp import cosine_similarity, get_embedding
from timeseek.screenshot import record_screenshots_thread
from timeseek.utils import human_readable_time, timestamp_to_human_readable

app = Flask(__name__)

app.jinja_env.filters["human_readable_time"] = human_readable_time
app.jinja_env.filters["timestamp_to_human_readable"] = timestamp_to_human_readable


@app.route("/")
def timeline():
    """Renders the timeline view showing all recorded moments."""
    timestamps = get_timestamps()
    return render_template("timeline.html", timestamps=timestamps)


@app.route("/search")
def search():
    """Handles search queries and returns relevant entries based on embedding similarity."""
    q = request.args.get("q", "")
    if not q:
        return render_template("search.html", entries=[])

    entries = get_all_entries()
    embeddings = [entry.embedding for entry in entries]
    query_embedding = get_embedding(q)
    similarities = [cosine_similarity(query_embedding, emb) for emb in embeddings]
    indices = np.argsort(similarities)[::-1]
    sorted_entries = [entries[i] for i in indices]

    return render_template("search.html", entries=sorted_entries)


@app.route("/timeline")
def timeline_redirect():
    """Alias for the root timeline route."""
    return timeline()


@app.route("/static/<filename>")
def serve_image(filename):
    """Serves recorded screenshots from the appdata directory."""
    return send_from_directory(screenshots_path, filename)


if __name__ == "__main__":
    create_db()

    print(f"Appdata folder: {appdata_folder}")
    print(f"Starting server on port: {args.port}")

    # Start the background thread for continuous screenshot recording
    t = Thread(target=record_screenshots_thread, daemon=True)
    t.start()

    app.run(port=args.port)
