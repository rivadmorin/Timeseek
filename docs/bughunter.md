# Bug Hunter Memory Journal

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
## 25-05-2024 - Fixed Embedding Type Mismatch in app.py
- **Tags:** #bug #logic #python #flask
- **Level:** 🔴 CRITICAL
- **Scope:** [timeseek/app.py](file:///app/timeseek/app.py)
- **Notify Agents:** @BugHunter @Scholar
- **Symptom:** Search results were incorrectly ordered or failed due to `np.frombuffer` with wrong dtype (`float64` instead of `float32`) and attempting to buffer an object that was already a numpy array.
- **Root Cause:** `get_all_entries()` already returns deserialized numpy arrays, but `app.py` tried to deserialize them again with the wrong type.
- **Learning:** Always check the return types of data access layer functions before applying secondary transformations. Centralize deserialization logic in the database layer.
- **Action/Rule:** Ensure `app.py` delegates data parsing to `database.py`.
- **Verify Command:** `PYTHONPATH=. python3 -m pytest`
## 25-05-2024 - Environment Stabilization & Dependency Resolution
- **Tags:** #environment #python #pytest
- **Level:** 🟢 INFO
- **Scope:** [setup.py](file:///app/setup.py)
- **Notify Agents:** @Scholar @Orchestrator
- **Symptom:** pytest failed to collect tests due to ModuleNotFoundError (numpy) despite it being in setup.py.
- **Root Cause:** Python version mismatch (.python-version requested 3.11 but sandbox uses 3.12) and dependencies were not installed in the active environment.
- **Learning:** Always verify the active python path and version before assuming dependencies are present. Use `python3 -m pip install` and `python3 -m pytest` to ensure the correct environment is used.
- **Action/Rule:** Remove .python-version if it conflicts with the sandbox environment to allow fallback to available system python.
- **Verify Command:** `PYTHONPATH=. python3 -m pytest`

## 25-05-2024 - NumPy & SciPy Compatibility Learning
- **Tags:** #numpy #scipy #compatibility
- **Level:** 🟡 WARNING
- **Scope:** [Environment]
- **Notify Agents:** @Scholar
- **Symptom:** `AttributeError: module 'numpy' has no attribute 'long'` when importing `scipy.sparse`.
- **Root Cause:** NumPy 2.0+ removed several deprecated attributes like `long`. Older versions of SciPy (pre-1.14) are incompatible with NumPy 2.0.
- **Learning:** When upgrading to NumPy 2.0, ensure SciPy is also upgraded to at least 1.14.0.
- **Action/Rule:** Pin NumPy < 2.0 if working with legacy SciPy, or upgrade both in tandem.
## 25-05-2024 - Added Search Regression Tests
- **Tags:** #testing #regression #flask
- **Level:** 🟢 INFO
- **Scope:** [tests/test_search.py](file:///app/tests/test_search.py)
- **Notify Agents:** @TestPilot @Orchestrator
- **Symptom:** No automated verification for the search route logic.
- **Learning:** Mocking database and NLP components allows for fast, side-effect-free testing of web routes.
- **Action/Rule:** Always include route-level tests when modifying application logic in `app.py`.
- **Verify Command:** `PYTHONPATH=. python3 -m pytest tests/test_search.py`
# Orchestrator Learning: Discovery Phase
- **Plan ID:** discovery
- **Agent:** Orchestrator 🕴️
- **Learning:** Stabilization is required. Detected and fixed critical function shadowing in `screenshot.py`. Refactored UI templates for better SOC.
- **Status:** Phase 1 Complete.
## 06-07-2026 - Fixed Database Schema and insert_entry Mismatch
- **Tags:** #bug #database #sqlite #schema
- **Level:** 🔴 CRITICAL
- **Scope:** [timeseek/database.py](file:///app/timeseek/database.py)
- **Notify Agents:** @BugHunter @Orchestrator
- **Symptom:** Application crashed during screenshot recording because `insert_entry` was called with 6 arguments but only accepted 5. Additionally, the UI could not reliably find images because the filename was not stored.
- **Root Cause:** Database schema was missing the `filename` column and the `insert_entry` function signature was outdated compared to its usage in `screenshot.py`.
- **Learning:** Schema migrations should be handled defensively in `create_db` using `PRAGMA table_info` to ensure new columns are added without wiping existing data.
- **Action/Rule:** Always sync `database.py` signatures with caller logic in `screenshot.py` or `app.py`.
- **Verify Command:** `python3 -c "from timeseek.database import create_db; create_db()"`
## 06-07-2026 - Fixed Broken UI Image Paths in Templates
- **Tags:** #bug #frontend #jinja2 #ui
- **Level:** 🟢 INFO
- **Scope:** [timeseek/templates/timeline.html](file:///app/timeseek/templates/timeline.html), [timeseek/templates/search.html](file:///app/timeseek/templates/search.html), [timeseek/database.py](file:///app/timeseek/database.py)
- **Notify Agents:** @BugHunter @Orchestrator
- **Symptom:** Images failed to load in Timeline and Search views, appearing as broken links.
- **Root Cause:** The UI was hardcoded to expect `timestamp.webp`, but the backend saves files as `timestamp_monitorindex.webp` to support multi-monitor setups.
- **Learning:** Never assume file naming conventions in the UI; always retrieve the actual filename from the data source (database).
- **Action/Rule:** Updated `get_timestamps` to return both timestamp and filename, and updated templates to use the `filename` field.
- **Verify Command:** Manual visual inspection of UI.
## 25-05-2024 - Implemented Snapshot Annotations
- **Tags:** #database #ui #builder #taste
- **Level:** 🟢 INFO
- **Scope:** [timeseek/database.py](file:///app/timeseek/database.py), [timeseek/app.py](file:///app/timeseek/app.py), [timeseek/templates/timeline.html](file:///app/timeseek/templates/timeline.html)
- **Notify Agents:** @Orchestrator @Builder @Taste
- **Symptom:** Snapshots lacked context or personal notes.
- **Root Cause:** Missing schema support and UI elements for user annotations.
- **Learning:** Defensive schema migrations using `PRAGMA table_info` are essential for maintaining data integrity during feature rollouts. M3 text fields should be subtle but responsive.
- **Action/Rule:** Always provide a way for users to add context to their digital history to improve retrieval relevance.
- **Verify Command:** `python3 -m py_compile timeseek/database.py timeseek/app.py`
## 25-05-2024 - Implemented App Blacklist
- **Tags:** #privacy #config #builder
- **Level:** 🟢 INFO
- **Scope:** [timeseek/config.py](file:///app/timeseek/config.py), [timeseek/screenshot.py](file:///app/timeseek/screenshot.py)
- **Notify Agents:** @Orchestrator @Builder
- **Symptom:** Users could not exclude sensitive apps from recording.
- **Root Cause:** Lack of application filtering in the recording loop.
- **Learning:** Privacy-centric features should be integrated as early as possible in the data capture pipeline to avoid unnecessary processing and storage of sensitive info.
- **Action/Rule:** Always check the active application against the blacklist before initiating screenshot capture or OCR.
- **Verify Command:** `python3 -m py_compile timeseek/config.py timeseek/screenshot.py`
## 25-05-2024 - Implemented Auto-Pruning Engine
- **Tags:** #maintenance #database #builder #bughunter
- **Level:** 🟢 INFO
- **Scope:** [timeseek/config.py](file:///app/timeseek/config.py), [timeseek/database.py](file:///app/timeseek/database.py), [timeseek/app.py](file:///app/timeseek/app.py)
- **Notify Agents:** @Orchestrator @Builder @BugHunter
- **Symptom:** Local disk space could be exhausted over time due to unlimited snapshot storage.
- **Root Cause:** Lack of automated data cleanup logic.
- **Learning:** Storage management is a critical part of local-first applications. Running pruning on startup ensures a clean state without needing complex background cron jobs.
- **Action/Rule:** Always implement a configurable data retention policy for high-volume data capture systems.
- **Verify Command:** `python3 -m py_compile timeseek/config.py timeseek/database.py timeseek/app.py`
## 25-05-2024 - Implemented Advanced Search Filters
- **Tags:** #ui #search #builder #taste
- **Level:** 🟢 INFO
- **Scope:** [timeseek/app.py](file:///app/timeseek/app.py), [timeseek/templates/search.html](file:///app/timeseek/templates/search.html)
- **Notify Agents:** @Orchestrator @Builder @Taste
- **Symptom:** Search results were often cluttered with results from irrelevant applications.
- **Root Cause:** Lack of category/application-based filtering in the search interface.
- **Learning:** Contextual filtering significantly improves the user experience in large datasets. M3 filter chips should be persistent across searches where appropriate.
- **Action/Rule:** Always allow users to narrow down search results using metadata like application name.
- **Verify Command:** `python3 -m py_compile timeseek/app.py`
## 25-05-2024 - Quality Assurance for Expansion
- **Tags:** #qa #testing #inspector
- **Level:** 🟢 INFO
- **Scope:** [tests/test_search.py](file:///app/tests/test_search.py)
- **Notify Agents:** @Orchestrator @TestPilot @Inspector
- **Symptom:** Original tests failed due to outdated assumptions about database entry structure (filename and notes were missing).
- **Root Cause:** Schema expansion during the "Four Features" phase.
- **Learning:** Mock objects in tests must be kept in sync with the actual data models in `database.py`. Vectorized search results should be verified by matching expected filenames or IDs.
- **Action/Rule:** Always update regression tests immediately after schema or data model changes.
- **Verify Command:** `PYTHONPATH=. python3 -m pytest tests/test_search.py`
## 07-07-2026 - Added UI documentation screenshots
- **Tags:** #documentation #ui #m3
- **Level:** 🟢 INFO
- **Scope:** [README.md](file:///app/README.md)
- **Notify Agents:** @Palette @Scribe
- **Symptom:** README lacked visual representation of the new Material Design 3 UI.
- **Root Cause:** Documentation was purely text-based and didn't showcase the UX improvements.
- **Learning:** Playwright can be used in the agent environment to capture live application state for documentation.
- **Action/Rule:** Always include screenshots when making significant UI/UX changes to ensure clarity for users.
- **Verify Command:** `grep "UI Gallery" README.md`
