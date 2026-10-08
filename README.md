
# Take Control of Your Digital Memory (M3 Overhauled! 🕴️ - Full Rust 🚀)

Timeseek is a fully open-source, privacy-first alternative to proprietary solutions like Microsoft's Windows Recall or Limitless' Rewind.ai. Written 100% in Rust, it records your screen, extracts text locally, computes semantic embeddings, and lets you search or scrub through your digital history—100% offline with zero Python runtime overhead.

---

## ✨ Features

- **🚀 100% Full Rust Engine**: High performance, memory efficiency, native async web server (`Axum`), and multi-threaded screen recording.
- **🕒 Time Travel (M3 Timeline)**: Scrub through past digital activities with an interactive Material Design 3 timeline player.
- **🔍 Semantic & Vector Search**: Perform fast, local similarity search across past screen content powered by vector embeddings and cosine similarity.
- **🚫 App & Keyword Blacklist**: Protect sensitive information by automatically excluding specified applications (e.g., password managers) or snapshots containing specific sensitive keywords.
- **🏷️ Snapshot Annotations**: Add custom notes and personal context directly to any captured snapshot.
- **🧹 Auto-Pruning Engine**: Configurable data retention policies to automatically delete snapshots and database entries older than a set threshold.
- **📊 Activity Analytics**: Track usage patterns with interactive hourly activity graphs and statistics on the Dashboard.
- **🔒 Privacy First & Offline Capable**: Zero cloud dependencies. No external API calls.

---

## 🛠️ Technical Architecture

Timeseek Rust operates on a native high-performance local pipeline:

1. **Screen Capture & Deduplication (SSIM)**: Screenshots are captured periodically via native screen capture tools. Structural similarity (SSIM) is evaluated against the previous frame in Rust—if no visual change is detected, processing is skipped.
2. **Privacy Filter**: Evaluates application metadata against user-defined app and keyword blacklists before capturing or saving images.
3. **Storage & Caching (SQLite)**: Snapshot metadata, notes, and vector embeddings are indexed in a local SQLite database (`rusqlite`) and cached in memory for instant query responses.
4. **Auto-Maintenance**: Automated pruning on startup cleans up physical images and database rows past the configured retention limit.

---

## 💻 CLI Options & Configuration

Launch Timeseek Rust with command-line arguments:

| Flag | Type | Default | Description |
|---|---|---|---|
| `--port` / `-p` | `u16` | `8082` | Web server port. |
| `--db-path` / `-d` | `str` | `"timeseek.db"` | Path to SQLite database file. |
| `--screenshots-path` / `-s` | `str` | `"images"` | Folder path to store captured screenshots. |
| `--blacklist` / `-b` | `str` | `""` | Comma-separated list of application names to ignore. |
| `--keyword-blacklist` / `-k` | `str` | `""` | Comma-separated list of text keywords to ignore snapshots containing them. |
| `--retention-days` / `-r` | `u64` | `30` | Data retention period in days before auto-pruning. |
| `--primary-monitor-only` | `flag` | `false` | Limit screen recording to primary monitor only. |

---

## 📁 Project Structure

```
.
├── Cargo.toml         # Cargo binary package definition & Rust dependencies
├── src/
│   ├── main.rs        # Main CLI entry point & server initialization
│   ├── lib.rs         # Module exports
│   ├── db.rs          # SQLite database schema, CRUD, & auto-pruning
│   ├── state.rs       # Thread-safe global application state
│   ├── cache.rs       # Thread-safe in-memory snapshot cache
│   ├── recording.rs   # Background Tokio screen recording loop & deduplication
│   ├── image_proc.rs  # SSIM structural image comparison algorithm
│   ├── ml.rs          # Vector embedding calculation & SIMD cosine similarity
│   └── web.rs         # Axum web server, REST API, & template handlers
├── tests/
│   └── rust_tests.rs  # Integration and unit tests
└── timeseek/
    ├── static/        # Material Design 3 CSS, JS, and UI assets
    └── templates/     # HTML templates parsed via minijinja
```

---

## 🚀 Quick Start

### Build & Run with Cargo

Compile and run Timeseek in release mode:
```bash
cargo run --release -- --port 8082 --retention-days 14
```

Or run tests:
```bash
cargo test
```

Access the web interface in your browser at:
**[http://localhost:8082](http://localhost:8082)**

---

## 📜 License

Timeseek is released under the [AGPLv3 License](https://opensource.org/licenses/AGPL-3.0).
