# Nomad Memory Journal

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
## 06-07-2026 - Asset Localization Phase Completed
- **Tags:** #nomad #offline #assets
- **Level:** 🟢 INFO
- **Scope:** [timeseek/static/](file:///app/timeseek/static/)
- **Notify Agents:** @Nomad @Builder
- **Symptom:** Initial templates relied on CDNs.
- **Root Cause:** N/A (Offline requirement)
- **Learning:** Localizing fonts and Material Web components ensures the application works without internet access.
- **Action/Rule:** Always use relative paths (e.g., ../fonts/) in localized CSS files.
- **Verify Command:** `ls -R timeseek/static/`
