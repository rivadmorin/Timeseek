# Scribe Memory Journal

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
## 25-05-2024 - README Project Structure Update
- **Tags:** #documentation #readme #scribe
- **Level:** 🟢 INFO
- **Scope:** [README.md](file:///app/README.md)
- **Notify Agents:** @All
- **Symptom:** README was missing a clear overview of the refactored project structure.
- **Root Cause:** Previous refactoring tasks (by Bug Hunter and Inspector) changed the file organization but did not update the documentation.
- **Learning:** Documentation tasks should always follow refactoring tasks to ensure the "Source of Truth" (README) reflects the current codebase state.
- **Action/Rule:** Always check for directory structure changes in previous plan tasks and reflect them in the "Project Structure" section of the README.
## 06-07-2026 - Documentation Updated for M3 Overhaul
- **Tags:** #scribe #readme #docs
- **Level:** 🟢 INFO
- **Scope:** [README.md](file:///app/README.md)
- **Notify Agents:** @Scribe @Orchestrator
- **Symptom:** README didn't mention the new M3 UI features.
- **Root Cause:** N/A (Feature Update)
- **Learning:** Highlighting the "Offline-First UI" and "M3 Overhaul" in the README increases trust and modern appeal.
- **Action/Rule:** Always update the Prerequisites section if Python version requirements change during testing.
- **Verify Command:** `cat README.md`
## 06-07-2026 - Enhanced Technical Documentation & Agentic Intro
- **Tags:** #documentation #readme #agents
- **Level:** 🟢 INFO
- **Scope:** [README.md](file:///app/README.md)
- **Notify Agents:** @Scribe @Orchestrator
- **Symptom:** README was informative but lacked deep technical flow and explanation of the internal agent system.
- **Root Cause:** Documentation lagged behind the rapid development of the agentic orchestration system.
- **Learning:** Explaining the "Why" (MSSIM, vector dims) alongside the "How" (Installation) helps both human and AI contributors navigate the project more effectively.
- **Action/Rule:** Always include a section on the Agentic System when updating documentation in an Orchestrator-led workspace.
- **Verify Command:** `cat README.md | grep "Technical Architecture"`
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
