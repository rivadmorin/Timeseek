# Scholar Memory Journal

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

---

## ERROR FINGERPRINT DICTIONARY

To ensure all agents can resolve common build, environment, and code compilation errors instantly without manual troubleshooting.

| Error Signature (Regex/Text) | Inferred Root Cause | Verified Resolution / Fix Command |
| --- | --- | --- |
| `Cannot find module '@components/...'` | Missing TypeScript path mapping in tsconfig.json or vite.config.ts | Add alias to `vite.config.ts` and tsconfig paths |
| `exit code 127: ... command not found` | Tool is not installed globally or missing from local PATH | Install via npm/pnpm/pip, or use explicit executable path |

## 25-05-2024 - Python Function Overshadowing Bug
- **Tags:** #python #bug #architecture
- **Level:** 🔴 CRITICAL
- **Scope:** [openrecall/screenshot.py](file:///app/openrecall/screenshot.py)
- **Notify Agents:** @BugHunter @Inspector
- **Fingerprint ID:** ERR-PY-OVERSHADOW
- **Symptom:** Application fails to start or crashes with NameError inside a loop that should be working.
- **Root Cause:** Multiple definitions of the same function name in the same module. The last definition wins and may contain incomplete or broken code.
- **Learning:** Always use linters (flake8/pylint) to detect redifinition of functions. Duplicate code often indicates a failed merge or copy-paste error.
- **Action/Rule:** Never commit files with duplicate top-level function definitions.
- **Verify Command:** `grep "def function_name" file.py | wc -l`
