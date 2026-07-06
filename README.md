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

OpenRecall is a fully open-source, privacy-first alternative to proprietary solutions like Microsoft's Windows Recall or Limitless' Rewind.ai.

## ✨ New in this version: Material Design 3
We've completely overhauled the UI using **Google Material Design 3 (M3)** principles:
- **Dark/Light Mode Support**: Seamlessly switch between themes.
- **Offline-First UI**: All Material Web components and fonts are localized for 100% offline usage.
- **Improved UX**: New Navigation Rail, semantic search cards, and an immersive timeline viewer.

## What does it do?

OpenRecall captures your digital history through regularly taken snapshots. The text and images are analyzed and made searchable.

## Features

- **Time Travel**: Revisit past digital activities via our new M3 Timeline scrubber.
- **Local-First AI**: Privacy and security via local processing.
- **Semantic Search**: Advanced local OCR search results in a modern M3 grid.
- **Offline Assets**: No CDN dependencies.

## Project Structure

OpenRecall is organized into modular components for better maintainability:

- **`openrecall/app.py`**: Main entry point, Flask web server, and UI routing.
- **`openrecall/templates/`**: Jinja2 HTML templates for the web interface (`timeline.html`, `search.html`).
- **`openrecall/config.py`**: Configuration management, argument parsing, and storage path setup.
- **`openrecall/database.py`**: SQLite database schema and data persistence logic.
- **`openrecall/nlp.py`**: Natural Language Processing for semantic search embeddings using cosine similarity.
- **`openrecall/ocr.py`**: Optical Character Recognition (`doctr`) to extract text from captured images.
- **`openrecall/screenshot.py`**: Background thread logic for capturing and storing periodic screenshots.
- **`openrecall/utils.py`**: Helper functions for time conversion and formatting.

## Get Started

### Prerequisites
- Python 3.12 (Recommended)
- MacOSX/Windows/Linux
- Git

To install:
```
python3 -m pip install --upgrade --no-cache-dir git+https://github.com/openrecall/openrecall.git
```

To run:
```
python3 -m openrecall.app
```
Open your browser to [http://localhost:8082](http://localhost:8082).

## Project Structure

OpenRecall is organized into modular components for better maintainability:

- **`openrecall/app.py`**: Main entry point, Flask web server, and UI routing.
- **`openrecall/templates/`**: Jinja2 HTML templates for the web interface (`timeline.html`, `search.html`).
- **`openrecall/config.py`**: Configuration management, argument parsing, and storage path setup.
- **`openrecall/database.py`**: SQLite database schema and data persistence logic.
- **`openrecall/nlp.py`**: Natural Language Processing for semantic search embeddings using cosine similarity.
- **`openrecall/ocr.py`**: Optical Character Recognition (`doctr`) to extract text from captured images.
- **`openrecall/screenshot.py`**: Background thread logic for capturing and storing periodic screenshots.
- **`openrecall/utils.py`**: Helper functions for time conversion and formatting.

## Arguments
`--storage-path` (default: user data path for your OS): allows you to specify the path where the screenshots and database should be stored. We recommend [creating an encrypted volume](docs/encryption.md) to store your data.

`--primary-monitor-only` (default: False): only record the primary monitor (rather than individual screenshots for other monitors)

## Uninstall instructions

To uninstall OpenRecall and remove all stored data:

1. Uninstall the package:
   ```
   python3 -m pip uninstall openrecall
   ```

2. Remove stored data:
   - On Windows:
     ```
     rmdir /s %APPDATA%\openrecall
     ```
   - On macOS:
     ```
     rm -rf ~/Library/Application\ Support/openrecall
     ```
   - On Linux:
     ```
     rm -rf ~/.local/share/openrecall
     ```

Note: If you specified a custom storage path at any time using the `--storage-path` argument, make sure to remove that directory too.

## Contribute

As an open-source project, we welcome contributions from the community. If you'd like to help improve OpenRecall, please submit a pull request or open an issue on our GitHub repository.

## Contact the maintainers
mail@datatalk.be

## License
OpenRecall is released under the [AGPLv3](https://opensource.org/licenses/AGPL-3.0).
