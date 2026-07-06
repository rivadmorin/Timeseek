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
## 06-07-2026 - Documentation Updated for M3 Overhaul
- **Tags:** #scribe #readme #docs
- **Level:** 🟢 INFO
- **Scope:** [README.md](file:///app/README.md)
- **Notify Agents:** @Scribe @Orchestrator
- **Symptom:** README didn't mention the new M3 UI features.
- **Root Cause:** N/A (Feature Update)
- **Learning:** Highlighting the "Offline-First UI" and "M3 Overhaul" in the README increases trust and modern appeal.
- **Action/Rule:** Always update the Prerequisites section if Python version requirements change during testing.
## 25-05-2024 - README Project Structure Update
- **Tags:** #documentation #readme #scribe
- **Level:** 🟢 INFO
- **Scope:** [README.md](file:///app/README.md)
- **Notify Agents:** @All
- **Symptom:** README was missing a clear overview of the refactored project structure.
- **Root Cause:** Previous refactoring tasks (by Bug Hunter and Inspector) changed the file organization but did not update the documentation.
- **Learning:** Documentation tasks should always follow refactoring tasks to ensure the "Source of Truth" (README) reflects the current codebase state.
- **Action/Rule:** Always check for directory structure changes in previous plan tasks and reflect them in the "Project Structure" section of the README.
- **Verify Command:** `cat README.md`
