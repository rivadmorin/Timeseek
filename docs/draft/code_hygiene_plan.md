---
plan_id: code_hygiene
title: "Orchestration Plan: Codebase Hygiene & Standardization"
goal: "Improve codebase maintainability by extracting constants, auditing imports, and standardizing documentation."
status: draft
created: 2026-07-06
updated: 2026-07-06
---

# Orchestration Plan: Codebase Hygiene & Standardization

## 1. Context & Risk Analysis (Pre-Mortem)
- **Context:** The current codebase has hardcoded magic numbers (e.g., ports) and inconsistent docstring styles which can hinder future scalability and readability.
- **Technical Risk:** Extracting constants might lead to circular imports if not carefully placed in `config.py`.
- **Mitigation:** Verify import chains before moving constants and run the application to ensure it still binds to the correct ports/paths.

## 2. Global Constraints & Active Rules
- **Active Rules:**
  - Preserve exact runtime semantics (Inspector boundary).
  - Keep changes under 50 lines per task.
- **Avoid Errors:**
  - ERR-PY-OVERSHADOW: Ensure no function redefinitions during refactoring.

## 3. Sequenced Task Checklist

- [ ] Task 1: Inspector 🧐 - Extract magic numbers to config.py
  - **Read Boundary:**
    - [openrecall/app.py](file:///app/openrecall/app.py)
    - [openrecall/config.py](file:///app/openrecall/config.py)
  - **Write/Modify Boundary:**
    - [openrecall/app.py](file:///app/openrecall/app.py)
    - [openrecall/config.py](file:///app/openrecall/config.py)
  - **Depends On:** None
  - **Verification & Testing:**
    - Command: `python3 -m py_compile openrecall/app.py openrecall/config.py`
    - Success Criteria: Files compile without syntax errors.
  - **Rollback Action:** `git checkout openrecall/app.py openrecall/config.py`
  - **Target Staging Memory:** `docs/staged/code_hygiene-inspector-06-07-2026-t1.md`

- [ ] Task 2: Inspector 🧐 - Audit and cleanup unused imports/variables
  - **Read Boundary:**
    - [openrecall/](file:///app/openrecall/)
  - **Write/Modify Boundary:**
    - [openrecall/app.py](file:///app/openrecall/app.py)
    - [openrecall/nlp.py](file:///app/openrecall/nlp.py)
    - [openrecall/database.py](file:///app/openrecall/database.py)
    - [openrecall/screenshot.py](file:///app/openrecall/screenshot.py)
  - **Depends On:** Task 1
  - **Verification & Testing:**
    - Command: `pytest`
    - Success Criteria: All tests pass.
  - **Rollback Action:** `git checkout openrecall/`
  - **Target Staging Memory:** `docs/staged/code_hygiene-inspector-06-07-2026-t2.md`

- [ ] Task 3: Inspector 🧐 - Standardize JSDoc/Docstring headers
  - **Read Boundary:**
    - [openrecall/](file:///app/openrecall/)
  - **Write/Modify Boundary:**
    - [openrecall/utils.py](file:///app/openrecall/utils.py)
    - [openrecall/ocr.py](file:///app/openrecall/ocr.py)
  - **Depends On:** Task 2
  - **Verification & Testing:**
    - Command: `python3 -m py_compile openrecall/utils.py openrecall/ocr.py`
    - Success Criteria: Files compile without syntax errors.
  - **Rollback Action:** `git checkout openrecall/`
  - **Target Staging Memory:** `docs/staged/code_hygiene-inspector-06-07-2026-t3.md`
