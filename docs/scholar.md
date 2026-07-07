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
- **Scope:** [timeseek/screenshot.py](file:///app/timeseek/screenshot.py)
- **Notify Agents:** @BugHunter @Inspector
- **Fingerprint ID:** ERR-PY-OVERSHADOW
- **Symptom:** Application fails to start or crashes with NameError inside a loop that should be working.
- **Root Cause:** Multiple definitions of the same function name in the same module. The last definition wins and may contain incomplete or broken code.
- **Learning:** Always use linters (flake8/pylint) to detect redifinition of functions. Duplicate code often indicates a failed merge or copy-paste error.
- **Action/Rule:** Never commit files with duplicate top-level function definitions.
- **Verify Command:** `grep "def function_name" file.py | wc -l`
## 25-05-2024 - Fixed Embedding Type Mismatch in app.py
- **Tags:** #bug #logic #python #flask
- **Level:** 🔴 CRITICAL
- **Scope:** [timeseek/app.py](file:///app/timeseek/app.py)
- **Notify Agents:** @BugHunter @Scholar
- **Symptom:** Search results were incorrectly ordered or failed due to `np.frombuffer` with wrong dtype (`float64` instead of `float32`) and attempting to buffer an object that was already a numpy array.
- **Root Cause:** `get_all_entries()` already returns deserialized numpy arrays, but `app.py` tried to deserialize them again with the wrong type.
- **Learning:** Always check the return types of data access layer functions before applying secondary transformations. Centralize deserialization logic in the database layer.
- **Action/Rule:** Ensure `app.py` delegates data parsing to `database.py`.
- **Verify Command:** `PYTHONPATH=. python3 -m pytest`
## 25-05-2024 - Environment Stabilization & Dependency Resolution
- **Tags:** #environment #python #pytest
- **Level:** 🟢 INFO
- **Scope:** [setup.py](file:///app/setup.py)
- **Notify Agents:** @Scholar @Orchestrator
- **Symptom:** pytest failed to collect tests due to ModuleNotFoundError (numpy) despite it being in setup.py.
- **Root Cause:** Python version mismatch (.python-version requested 3.11 but sandbox uses 3.12) and dependencies were not installed in the active environment.
- **Learning:** Always verify the active python path and version before assuming dependencies are present. Use `python3 -m pip install` and `python3 -m pytest` to ensure the correct environment is used.
- **Action/Rule:** Remove .python-version if it conflicts with the sandbox environment to allow fallback to available system python.
- **Verify Command:** `PYTHONPATH=. python3 -m pytest`

## 25-05-2024 - NumPy & SciPy Compatibility Learning
- **Tags:** #numpy #scipy #compatibility
- **Level:** 🟡 WARNING
- **Scope:** [Environment]
- **Notify Agents:** @Scholar
- **Symptom:** `AttributeError: module 'numpy' has no attribute 'long'` when importing `scipy.sparse`.
- **Root Cause:** NumPy 2.0+ removed several deprecated attributes like `long`. Older versions of SciPy (pre-1.14) are incompatible with NumPy 2.0.
- **Learning:** When upgrading to NumPy 2.0, ensure SciPy is also upgraded to at least 1.14.0.
- **Action/Rule:** Pin NumPy < 2.0 if working with legacy SciPy, or upgrade both in tandem.
## 25-05-2024 - Added Search Regression Tests
- **Tags:** #testing #regression #flask
- **Level:** 🟢 INFO
- **Scope:** [tests/test_search.py](file:///app/tests/test_search.py)
- **Notify Agents:** @TestPilot @Orchestrator
- **Symptom:** No automated verification for the search route logic.
- **Learning:** Mocking database and NLP components allows for fast, side-effect-free testing of web routes.
- **Action/Rule:** Always include route-level tests when modifying application logic in `app.py`.
- **Verify Command:** `PYTHONPATH=. python3 -m pytest tests/test_search.py`
# Orchestrator Learning: Discovery Phase
- **Plan ID:** discovery
- **Agent:** Orchestrator 🕴️
- **Learning:** Stabilization is required. Detected and fixed critical function shadowing in `screenshot.py`. Refactored UI templates for better SOC.
- **Status:** Phase 1 Complete.
