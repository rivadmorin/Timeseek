# Launchpad Memory Journal

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

## 07-07-2026 - Standardizing Lifecycle Scripts for Timeseek
- **Tags:** #orchestration/shell #lifecycle
- **Level:** 🟢 INFO
- **Scope:** [launchpad/timeseek.sh](file:///app/launchpad/timeseek.sh), [launchpad/timeseek.bat](file:///app/launchpad/timeseek.bat)
- **Notify Agents:** @Orchestrator
- **Symptom:** Inconsistent lifecycle command signatures across platforms.
- **Root Cause:** Initial scripts only had a subset of required commands and lacked prerequisite checks.
- **Learning:** Standardizing on check-prereqs, install, start, stop, uninstall, and help ensures a predictable developer and user experience.
- **Action/Rule:** Always implement the full suite of lifecycle commands in Launchpad scripts.
- **Verify Command:** ./launchpad/timeseek.sh help
