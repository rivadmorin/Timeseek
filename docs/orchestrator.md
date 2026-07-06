# Orchestrator Memory Journal

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

## 25-05-2024 - Discovery & Initial Triage
- **Tags:** #orchestration #triage
- **Level:** 🟢 INFO
- **Scope:** [docs/draft/deep_discovery_plan.md](file:///app/docs/draft/deep_discovery_plan.md)
- **Notify Agents:** @All
- **Symptom:** Initial workspace had critical bugs (duplicate functions) and poor SOC (UI in app.py).
- **Learning:** Discovery phase must include manual code inspection for "shadow bugs" that automated tools might miss if dependencies are missing.
- **Action/Rule:** Prioritize "Stabilization" plans before "Feature" plans for legacy or unmaintained codebases.
# Orchestrator Learning: Discovery Phase
- **Plan ID:** discovery
- **Agent:** Orchestrator 🕴️
- **Learning:** Stabilization is required. Detected and fixed critical function shadowing in `screenshot.py`. Refactored UI templates for better SOC.
- **Status:** Phase 1 Complete.
## 25-05-2024 - Core Philosophy Alignment
- **Tags:** #orchestration #philosophy #portability
- **Level:** 🟢 INFO
- **Scope:** [docs/init/](file:///app/docs/init/)
- **Notify Agents:** @All
- **Symptom:** Instructions were generic and did not emphasize the user's core philosophy.
- **Root Cause:** Initial instructions lacked the specific context of "Offline, Portable, Efficient, and 1-Click".
- **Learning:** Agent instructions must be dynamically updated when the user specifies a core mission or philosophy to ensure all subsequent tasks are aligned.
- **Action/Rule:** Always cross-reference user requests with the "Philosophical Routing Table" and update instruction files if a new overarching constraint is introduced.
