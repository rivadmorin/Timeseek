# Test Pilot Memory Journal

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
## 06-07-2026 - UI Functional Testing Completed
- **Tags:** #testpilot #unittest #ui
- **Level:** 🟢 INFO
- **Scope:** [tests/ui_functional_test.py](file:///app/tests/ui_functional_test.py)
- **Notify Agents:** @TestPilot @Builder
- **Symptom:** N/A (Verification)
- **Root Cause:** N/A
- **Learning:** Mocking heavy dependencies (numpy, doctr, mss) is essential for running UI unit tests in a limited sandbox environment.
- **Action/Rule:** Always test both "Empty State" and "Populated State" for the Timeline slider.
- **Verify Command:** `python3 tests/ui_functional_test.py`
