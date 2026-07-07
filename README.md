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

Timeseek is a fully open-source, privacy-first alternative to proprietary solutions like Microsoft's Windows Recall or Limitless' Rewind.ai.

## ✨ New in this version: Material Design 3
We've completely overhauled the UI using **Google Material Design 3 (M3)** principles:
- **Dark/Light Mode Support**: Seamlessly switch between themes.
- **Offline-First UI**: All Material Web components and fonts are localized for 100% offline usage.
- **Improved UX**: New Navigation Rail, semantic search cards, and an immersive timeline viewer.

## What does it do?

Timeseek captures your digital history through regularly taken snapshots. The text and images are analyzed and made searchable locally on your machine.

## Features

- **Time Travel**: Revisit past digital activities via our new M3 Timeline scrubber.
- **Local-First AI**: Privacy and security via local processing. No data ever leaves your device.
- **Semantic Search**: Advanced local OCR and vector search results in a modern M3 grid.
- **Offline Assets**: 100% offline capable. No CDN dependencies or external API calls for core functionality.

## Technical Architecture

Timeseek operates on a sophisticated pipeline designed for efficiency and privacy:

1.  **Deduplication (MSSIM)**: Uses *Mean Structural Similarity Index* to compare screenshots. If the screen hasn't changed significantly, processing is skipped to save CPU/Battery.
2.  **OCR (doctr)**: Extracts text using a specialized `doctr` model optimized for local execution.
3.  **Embeddings (NLP)**: Text is converted into 384-dimensional vectors using the `all-MiniLM-L6-v2` model.
4.  **Storage (SQLite)**: Metadata and embeddings are stored in a local SQLite database for fast retrieval and semantic search.

## Project Structure

- **`timeseek/app.py`**: Flask server, UI routing, and background recording thread management.
- **`timeseek/screenshot.py`**: Core logic for multi-monitor capture and MSSIM-based deduplication.
- **`timeseek/ocr.py`**: OCR implementation using the `python-doctr` library.
- **`timeseek/nlp.py`**: Semantic search logic, vector embeddings, and cosine similarity calculations.
- **`timeseek/database.py`**: SQLite schema, migrations (defensive column addition), and persistence.
- **`timeseek/config.py`**: Centralized configuration and CLI argument parsing.
- **`timeseek/templates/`**: M3-compliant Jinja2 templates for the web interface.

## Get Started

### Prerequisites
- Python 3.12 (Recommended)
- MacOSX / Windows / Linux
- Git

### Standard Installation
```bash
python3 -m pip install --upgrade --no-cache-dir git+https://github.com/timeseek/timeseek.git
```

### Advanced / Development Installation
If you are contributing or need specific OCR dependencies:
```bash
git clone https://github.com/timeseek/timeseek.git
cd timeseek
pip install -e .
```
*Note: This project depends on a specific fork of `python-doctr` for optimized performance.*

### To Run
```bash
python3 -m timeseek.app
```
Open your browser to [http://localhost:8082](http://localhost:8082).

## Arguments
- `--storage-path`: Specify where screenshots and database are stored. Default is OS-specific user data folder.
- `--port`: Custom port for the web server (default: 8082).
- `--primary-monitor-only`: Only record the primary monitor to save space/processing.

## 🤖 Agentic Development (Jules & The Orchestrator)

This repository is optimized for **Agentic Workflow**. We use a specialized system of "Specialized Agents" (Scribe, Inspector, Builder, etc.) coordinated by an **Orchestrator**.

- **Documentation**: All agent-specific memories and technical deep-dives are located in the `docs/` directory.
- **Index**: See `docs/index.md` for a map of the project's knowledge base.
- **Contributing**: If you are an AI agent or a human developer, please refer to `AGENTS.md` for development protocols.

## Uninstall instructions

1. Uninstall the package: `pip uninstall timeseek`
2. Remove stored data:
   - **Windows**: `rmdir /s %APPDATA%\\timeseek`
   - **macOS**: `rm -rf ~/Library/Application\\ Support/timeseek`
   - **Linux**: `rm -rf ~/.local/share/timeseek`

## License
Timeseek is released under the [AGPLv3](https://opensource.org/licenses/AGPL-3.0).
