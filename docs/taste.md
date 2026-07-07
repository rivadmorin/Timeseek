# Taste Memory Journal

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
## 06-07-2026 - Visual Polishing Phase Completed
- **Tags:** #taste #aesthetic #polish #css
- **Level:** 🟢 INFO
- **Scope:** [timeseek/static/css/custom.css](file:///app/timeseek/static/css/custom.css)
- **Notify Agents:** @Taste @Design
- **Symptom:** UI felt static; corners weren't concentric.
- **Root Cause:** N/A (Polish)
- **Learning:** Adjusting inner border-radius (e.g., card-image) to be slightly smaller than the outer container (card) creates a more harmonious "concentric" look.
- **Action/Rule:** Use `cubic-bezier(0.4, 0, 0.2, 1)` for standard M3 transitions.
- **Verify Command:** Visual inspection of card corners.
## 06-07-2026 - Refined UI Aesthetics and Theme Toggle Persistence
- **Tags:** #ui #ux #m3 #theme
- **Level:** 🟢 INFO
- **Scope:** [timeseek/templates/layout.html](file:///app/timeseek/templates/layout.html)
- **Notify Agents:** @Taste @Orchestrator
- **Symptom:** Theme toggle state was lost on page refresh, and the toggle icon logic was slightly confusing.
- **Root Cause:** Lack of client-side persistence (localStorage) and inconsistent icon mapping.
- **Learning:** For better UX, visual preferences like themes should be persisted across sessions. The toggle icon should ideally represent the *action* or the *next state* to maintain intuitive flow.
- **Action/Rule:** Added `localStorage` persistence to the theme toggle and aligned the icon to suggest the alternative mode. Improved CSS transitions and focus states for M3 components.
- **Verify Command:** Manual verification of theme persistence after page reload.

## [2026-07-06] M3 Dashboard & Filter UI
- **Design**: Created a systematic "Daily Dashboard" following Material Design 3 dark theme principles.
- **UX**: Improved search results with semantic labels and "App Badges" for quick recognition.
- **Aesthetics**: Used tonal layers and blur effects for the timeline overlay to maintain a "clean and reliable" feel.
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
# Taste 💅 Learning: M3 Refinement & Visual Rhythm
- **Plan ID:** ui_refinement_and_verification
- **Agent:** Taste 💅
- **Learning:** Hardcoded M3 tokens in templates should be moved to `m3-tokens.css` for consistency across themes. Using `opacity` on primary containers for heatmap levels creates a more cohesive visual rhythm than hardcoded hex values. Smooth transitions on the theme toggle icon (`transform`) improve perceived quality.
- **Action/Rule:** Always link `m3-tokens.css` in the layout and use CSS variables for semantic coloring.
- **Verify Command:** Manual inspection of `layout.html` and `custom.css`.
