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

## 06-07-2026 - Plan Created: M3 UI Overhaul
- **Tags:** #orchestration #plan #ui #m3
- **Level:** 🟢 INFO
- **Scope:** [docs/draft/m3_ui_overhaul_plan.md](file:///app/docs/draft/m3_ui_overhaul_plan.md)
- **Notify Agents:** @Design @Material @Builder @Nomad @Taste @TestPilot @Scribe
- **Symptom:** User requested total UI overhaul with M3, dark/light mode, and offline support for desktop.
- **Learning:** Complexity requires sequential dispatch of 7 specialists to ensure M3 compliance and offline stability.
- **Action/Rule:** Always verify offline asset availability in Nomad phase before Builder starts template refactoring.

## 06-07-2026 - M3 UI Overhaul Consolidated
- **Tags:** #consolidation #m3 #overhaul
- **Level:** 🟢 INFO
- **Scope:** [docs/archive/plans/m3_ui_overhaul_plan.md](file:///app/docs/archive/plans/m3_ui_overhaul_plan.md)
- **Notify Agents:** @All
- **Symptom:** N/A
- **Learning:** Completing a 7-specialist pipeline for UI overhaul requires strict memory staging to ensure cross-specialist rules are followed.
- **Action/Rule:** Final cleanup must include moving draft plans to archive.
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

## 06-07-2026 - Merge Conflict Resolved
- **Tags:** #git #conflict #readme
- **Level:** 🟢 INFO
- **Scope:** [README.md](file:///app/README.md)
- **Notify Agents:** @Scribe @Orchestrator
- **Symptom:** PR conflict when merging to main.
- **Root Cause:** Upstream changes added "Project Structure" and "Arguments" sections to README.
- **Learning:** Always pull from origin/main before final submission to detect conflicts early.
- **Action/Rule:** Preserve new informative sections (Structure/Arguments) while keeping M3 overhaul highlights.
- **Verify Command:** `git status` (Verify no pending conflicts)
