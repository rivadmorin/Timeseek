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
