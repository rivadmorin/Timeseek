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
- **Scope:** [openrecall/app.py](file:///app/openrecall/app.py), [openrecall/config.py](file:///app/openrecall/config.py)
- **Notify Agents:** @Inspector @Orchestrator
- **Symptom:** Port was hardcoded in `app.py`, making it difficult for users to change via CLI.
- **Root Cause:** Lack of centralized configuration management for runtime parameters.
- **Learning:** CLI arguments should be parsed in a central `config.py` and made available globally to ensure consistency across the application.
- **Action/Rule:** Added `--port` argument to `config.py` and updated `app.py` to respect it. Also added docstrings to main routes.
- **Verify Command:** `python3 -m py_compile openrecall/app.py`
