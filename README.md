```
   ____                   ____                  ____   
  / __ \____  ___  ____  / __ \___  _________ _/ / /   
 / / / / __ \/ _ \/ __ \/ /_/ / _ \/ ___/ __ `/ / /    
/ /_/ / /_/ /  __/ / / / _, _/  __/ /__/ /_/ / / /     
\____/ .___/\___/_/ /_/_/ |_|\___/\___/\__,_/_/_/      
    /_/                                                                                                                         
```
**Enjoy this project?** Show your support by starring it! ⭐️ Thank you!

Join our [Discord](https://discord.gg/RzvCYRgUkx) and/or [Telegram](https://t.me/+5DULWTesqUYwYjY0) community to stay informed of updates!

# Take Control of Your Digital Memory (M3 Overhauled! 🕴️)

Timeseek is a fully open-source, privacy-first alternative to proprietary solutions like Microsoft's Windows Recall or Limitless' Rewind.ai. It records your screen, extracts text locally via OCR, computes semantic embeddings, and lets you search or scrub through your digital history—100% offline.

---

## ✨ Features

- **🕒 Time Travel (M3 Timeline)**: Scrub through past digital activities with an interactive Material Design 3 timeline player.
- **🔍 Semantic & Vector Search**: Perform fast, local similarity search across past screen content powered by `sentence-transformers` embeddings.
- **🚫 App & Keyword Blacklist**: Protect sensitive information by automatically excluding specified applications (e.g., password managers) or snapshots containing specific sensitive keywords.
- **🏷️ Snapshot Annotations**: Add custom notes and personal context directly to any captured snapshot.
- **🧹 Auto-Pruning Engine**: Configurable data retention policies to automatically delete snapshots and database entries older than a set threshold.
- **📊 Activity Analytics**: Track usage patterns with interactive hourly activity graphs, heatmaps, and OCR word clouds on the Dashboard.
- **📄 Single-Snapshot PDF Export**: Easily export and format individual recorded moments for archiving or sharing.
- **🔒 Privacy First & Offline Capable**: Zero cloud dependencies. No CDN calls or external API dependencies for core functionality.

---

## 🛠️ Technical Architecture

Timeseek operates on a high-performance local pipeline:

1. **Screen Capture & Deduplication (MSSIM)**: Screenshots are captured periodically. Structural similarity (MSSIM) is evaluated against the previous frame—if no meaningful visual change is detected, processing is skipped.
2. **Privacy Filter**: Evaluates active window metadata against user-defined application and keyword blacklists before capturing or saving images.
3. **Local OCR (doctr)**: Extracts textual content from captured images using a light, local `doctr` OCR model.
4. **NLP Embeddings**: Text content is transformed into 384-dimensional dense vectors using `all-MiniLM-L6-v2`.
5. **Storage & Caching (SQLite)**: Snapshot metadata, notes, and vector embeddings are indexed in a local SQLite database and cached in memory for instant query responses.
6. **Auto-Maintenance**: An automated pruning process runs on startup to clean up physical images and database rows past the configured retention limit.

---

## 💻 CLI Options & Configuration

You can customize Timeseek at launch using command-line arguments:

| Flag | Type | Default | Description |
|---|---|---|---|
| `--port` | `int` | `8082` | Web server port. |
| `--blacklist` | `str` | `Bitwarden,1Password,...` | Comma-separated list of application names to ignore. |
| `--keyword-blacklist` | `str` | `""` | Comma-separated list of text keywords to ignore snapshots containing them. |
| `--retention-days` | `int` | `30` | Data retention period in days before auto-pruning. |
| `--image-quality` | `int` | `80` | Saved JPEG screenshot quality (1-100). |
| `--ocr-lang` | `str` | `"en"` | Language code for local OCR model. |
| `--primary-monitor-only` | `flag` | `False` | Limit screen recording to primary monitor only. |

---

## 📁 Project Structure

```
timeseek/
├── app.py           # Flask web application & API routing
├── config.py        # Centralized configuration & argument parsing
├── database.py      # SQLite schema, migrations, CRUD, and auto-pruning
├── nlp.py           # Vector embeddings & cosine similarity search engine
├── ocr.py           # Local OCR text extraction engine
├── screenshot.py    # Background screen recording loop & MSSIM deduplication
├── state.py         # Thread-safe global application state
├── utils.py         # Formatting and app categorization helpers
├── static/          # CSS, JS, and M3 design assets
└── templates/       # Jinja2 HTML templates (Dashboard, Timeline, Search, etc.)
```

---

## 🚀 Quick Start

### Installation

Clone the repository and install in editable mode:
```bash
git clone https://github.com/rivadmorin/Timeseek.git
cd Timeseek
pip install -e .
```

To uninstall:
```bash
pip uninstall -y Timeseek
```

### Running Timeseek

Launch Timeseek with custom configuration flags:
```bash
python3 -m timeseek.app --blacklist "Bitwarden,1Password" --keyword-blacklist "secret,confidential" --retention-days 14
```

Access the web interface in your browser at:
**[http://localhost:8082](http://localhost:8082)**

---

## 🤖 Agentic Development System

This repository utilizes an **Agentic Development Workflow** powered by specialized agents (Scribe, Inspector, Builder, Bug Hunter, Taste, etc.) coordinated by an Orchestrator.

- **Knowledge Base**: Detailed logs and architecture learnings are located in `docs/`.
- **Index**: Map of agent memories available at [`docs/index.md`](docs/index.md).

---

## 📜 License

Timeseek is released under the [AGPLv3 License](https://opensource.org/licenses/AGPL-3.0).
