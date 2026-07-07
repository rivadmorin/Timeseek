# Material Memory Journal

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
## 06-07-2026 - M3 Design System Tokens Configured
- **Tags:** #material #tokens #m3 #css
- **Level:** 🟢 INFO
- **Scope:** [timeseek/static/css/m3-tokens.css](file:///app/timeseek/static/css/m3-tokens.css)
- **Notify Agents:** @Material @Builder @Taste
- **Symptom:** UI lacked standardized M3 color tokens.
- **Root Cause:** N/A (UI Overhaul)
- **Learning:** Defining Surface Containers (Lowest to Highest) is key for M3's "Tonal Elevation" logic in Dark Mode.
- **Action/Rule:** Always use --md-sys-color-* variables instead of hex codes in templates.
- **Verify Command:** `grep "md-sys-color" timeseek/static/css/m3-tokens.css`
