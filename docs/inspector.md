# Inspector Memory Journal

Critical learnings only. Do not add routine logs.

Format:
## DD-MM-YYYY - [Judul Pembelajaran]
- **Tags:** `#kategori/alat` `#jenis-masalah`
- **Level:** `🔴 CRITICAL` | `🟡 WARNING` | `🟢 INFO`
- **Scope:** `[Nama Berkas](file:///absolute/path/to/file)`
- **Notify Agents:** `@AgentName`
- **Fingerprint ID:** `ERR-XXXX` (jika ada di docs/scholar.md)
- **Symptom:** [Gejala/pesan error yang muncul]
- **Root Cause:** [Penyebab utama arsitektur/konfigurasi]
- **Learning:** [Prinsip baru yang ditemukan]
- **Action/Rule:** [Langkah konkret tindakan pencegahan]
- **Verify Command:** `perintah verifikasi` (jika ada)
## 06-07-2026 - Centralized Port Configuration and Documentation Cleanup
- **Tags:** #hygiene #config #python #refactor
- **Level:** 🟢 INFO
- **Scope:** [timeseek/app.py](file:///app/timeseek/app.py), [timeseek/config.py](file:///app/timeseek/config.py)
- **Notify Agents:** @Inspector @Orchestrator
- **Symptom:** Port was hardcoded in `app.py`, making it difficult for users to change via CLI.
- **Root Cause:** Lack of centralized configuration management for runtime parameters.
- **Learning:** CLI arguments should be parsed in a central `config.py` and made available globally to ensure consistency across the application.
- **Action/Rule:** Added `--port` argument to `config.py` and updated `app.py` to respect it. Also added docstrings to main routes.
- **Verify Command:** `python3 -m py_compile timeseek/app.py`
## 06-07-2026 - Deep Codebase Discovery & Data Flow Audit
- **Tags:** #architecture #dataflow #ocr #nlp #sqlite
- **Level:** 🟢 INFO
- **Scope:** [timeseek/](file:///app/timeseek/)
- **Notify Agents:** @Inspector @Scribe @Orchestrator
- **Symptom:** N/A (Documentation & Audit)
- **Root Cause:** Need for a centralized technical understanding of the "Screenshot -> OCR -> NLP -> DB" pipeline.
- **Learning:**
    1. **Efficiency Layer:** The system uses MSSIM (Mean Structural Similarity Index) in `screenshot.py` to deduplicate frames before expensive OCR/NLP processing.
    2. **OCR Engine:** Relies on a specific git fork of `python-doctr` using MobileNetV3 architectures for a balance of speed and accuracy on local hardware.
    3. **Semantic Search:** Uses `all-MiniLM-L6-v2` (384d) for embeddings. Embeddings are stored as BLOBs in SQLite and similarity is calculated at runtime using `numpy.argsort`.
    4. **Platform Portability:** `setup.py` handles OS-specific logic (`pywin32`, `pyobjc`) to fetch active window metadata, which is critical for context-aware recall.
- **Action/Rule:** Ensure README.md highlights the offline-first nature and the custom OCR dependency requirements.
- **Verify Command:** `pytest tests/test_nlp.py tests/test_database.py`
