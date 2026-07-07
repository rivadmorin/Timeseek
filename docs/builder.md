# Builder Memory Journal

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
## 06-07-2026 - Template Implementation Phase Completed
- **Tags:** #builder #jinja2 #templates #m3
- **Level:** 🟢 INFO
- **Scope:** [timeseek/templates/](file:///app/timeseek/templates/)
- **Notify Agents:** @Builder @TestPilot @Taste
- **Symptom:** UI was using Bootstrap modals and standard inputs.
- **Root Cause:** N/A (UI Overhaul)
- **Learning:** Using the HTML5 `<dialog>` element simplifies M3 modal implementation without heavy JS libraries.
- **Action/Rule:** Ensure `data-theme` is handled at the `<html>` level for global token swapping.
- **Verify Command:** `python3 -m timeseek.app` (Check if port 8082 serves the new layout)
