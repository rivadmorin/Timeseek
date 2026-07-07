# Bolt Memory Journal

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

## [2026-07-06] Vectorized Search & Recording Optimization
- **Performance**: Vectorized similarity search using `batch_cosine_similarity` with matrix multiplication. This reduces search time from O(N) Python calls to O(N) optimized C/BLAS operations.
- **Efficiency**: Implemented adaptive sleep intervals in `screenshot.py` (3s active, 5s idle) and increased SSIM threshold to 0.95 to reduce redundant processing.
- **Storage**: Optimized WebP compression quality (80) for screenshots.
- **Caching**: Added `functools.lru_cache` to `get_embedding` to speed up repeated search queries.
