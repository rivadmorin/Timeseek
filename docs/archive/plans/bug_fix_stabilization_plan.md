---
plan_id: bug_fix_stabilization
title: "Orchestration Plan: Bug Fix & Environment Stabilization"
goal: "Resolve environment inconsistencies, fix failing tests, and identify logic bugs."
status: executing
created: 2024-05-25
updated: 2024-05-25
---

# Orchestration Plan: Bug Fix & Environment Stabilization

## 1. Context & Risk Analysis (Pre-Mortem)
- **Context:** Initial scan showed pytest collection failures and a critical type mismatch bug in `app.py` search route.
- **Technical Risk:** Search results will be garbage or crash if embeddings are misinterpreted.
- **Mitigation:** Align all embedding operations to `float32` as defined in `nlp.py`.

## 2. Global Constraints & Active Rules
- **Active Rules:** Always use PYTHONPATH=. for tests.
- **Avoid Errors:** ERR-PY-OVERSHADOW (Duplicate functions in screenshot.py).

## 3. Sequenced Task Checklist

- [x] Task 1: Scholar 🧠 - Environment Stabilization (Fix dependencies and Python version mismatch)
  - **Read Boundary:**
    - [setup.py](file:///app/setup.py)
    - [.python-version](file:///app/.python-version)
  - **Write/Modify Boundary:**
    - [Environment]
  - **Verification & Testing:**
    - Command: `PYTHONPATH=. python3 -m pytest`
    - Success Criteria: Tests collected and running.
  - **Target Staging Memory:** `docs/staged/bug_fix_stabilization-scholar-25-05-2024-env.md`

- [x] Task 2: Bug Hunter 🐛 - Fix Embedding Type Mismatch in app.py
  - **Read Boundary:**
    - [openrecall/app.py](file:///app/openrecall/app.py)
    - [openrecall/database.py](file:///app/openrecall/database.py)
  - **Write/Modify Boundary:**
    - [openrecall/app.py](file:///app/openrecall/app.py)
  - **Verification & Testing:**
    - Command: Manual inspection and ensuring no type mismatch.
    - Success Criteria: `embeddings` in `app.py` are correctly derived from `Entry` objects.
  - **Target Staging Memory:** `docs/staged/bug_fix_stabilization-bughunter-25-05-2024-logic.md`

- [ ] Task 3: Test Pilot 🧪 - Add Search Regression Test
  - **Read Boundary:**
    - [tests/test_nlp.py](file:///app/tests/test_nlp.py)
  - **Write/Modify Boundary:**
    - [tests/test_search.py](file:///app/tests/test_search.py)
  - **Verification & Testing:**
    - Command: `PYTHONPATH=. python3 -m pytest tests/test_search.py`
    - Success Criteria: Test passes.
  - **Target Staging Memory:** `docs/staged/bug_fix_stabilization-testpilot-25-05-2024-test.md`
