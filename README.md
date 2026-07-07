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

## ✨ New in this version: Four Features Expansion 🚀
We've added powerful new capabilities to enhance your privacy and organization:
- **🚫 App Blacklist**: Prevent sensitive applications (like password managers) from being recorded.
- **🏷️ Snapshot Annotations**: Add personal notes and context to any moment in your timeline.
- **🧹 Auto-Pruning Engine**: Configurable data retention to automatically manage disk space.
- **🔍 Advanced Search Filters**: Easily filter search results by application to find exactly what you need.

## Features

- **Time Travel**: Revisit past digital activities via our new M3 Timeline scrubber.
- **Local-First AI**: Privacy and security via local processing. No data ever leaves your device.
- **Semantic Search**: Advanced local OCR and vector search results in a modern M3 grid.
- **Offline Assets**: 100% offline capable. No CDN dependencies or external API calls for core functionality.
- **Privacy First**: Built-in blacklist and local-only storage ensures your data stays yours.

## Technical Architecture

Timeseek operates on a sophisticated pipeline designed for efficiency and privacy:

1.  **Deduplication (MSSIM)**: Uses *Mean Structural Similarity Index* to compare screenshots. If the screen hasn't changed significantly, processing is skipped.
2.  **Privacy Filter**: Checks active application against user-defined blacklist before capture.
3.  **OCR (doctr)**: Extracts text using a specialized \`doctr\` model optimized for local execution.
4.  **Embeddings (NLP)**: Text is converted into 384-dimensional vectors using the \`all-MiniLM-L6-v2\` model.
5.  **Storage (SQLite)**: Metadata, annotations, and embeddings are stored in a local SQLite database.
6.  **Auto-Maintenance**: Pruning engine runs on startup to enforce data retention policies.

## Arguments
- `--storage-path`: Specify where screenshots and database are stored.
- `--port`: Custom port for the web server (default: 8082).
- `--primary-monitor-only`: Only record the primary monitor.
- `--blacklist`: Comma-separated list of app names to ignore.
- `--retention-days`: Number of days to keep data (default: 30).

## Get Started

### To Run
```bash
python3 -m timeseek.app --blacklist "Bitwarden,1Password" --retention-days 14
```
Open your browser to [http://localhost:8082](http://localhost:8082).

## 🤖 Agentic Development (Jules & The Orchestrator)

This repository is optimized for **Agentic Workflow**. We use a specialized system of "Specialized Agents" (Scribe, Inspector, Builder, etc.) coordinated by an **Orchestrator**.

- **Documentation**: All agent-specific memories and technical deep-dives are located in the \`docs/\` directory.
- **Index**: See \`docs/index.md\` for a map of the project's knowledge base.

## License
Timeseek is released under the [AGPLv3](https://opensource.org/licenses/AGPL-3.0).
