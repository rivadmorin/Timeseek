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
- **Scope:** [openrecall/static/css/custom.css](file:///app/openrecall/static/css/custom.css)
- **Notify Agents:** @Taste @Design
- **Symptom:** UI felt static; corners weren't concentric.
- **Root Cause:** N/A (Polish)
- **Learning:** Adjusting inner border-radius (e.g., card-image) to be slightly smaller than the outer container (card) creates a more harmonious "concentric" look.
- **Action/Rule:** Use `cubic-bezier(0.4, 0, 0.2, 1)` for standard M3 transitions.
- **Verify Command:** Visual inspection of card corners.
