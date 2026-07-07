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
