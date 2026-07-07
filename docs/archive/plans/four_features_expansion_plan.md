---
plan_id: four_features_expansion
title: "Orchestration Plan: Four Features Expansion"
goal: "Implement App Blacklist, Snapshot Annotations, Auto-Pruning, and Advanced Search Filters."
status: executing
created: 2024-05-25
updated: 2024-05-25
---

# Orchestration Plan: Four Features Expansion

## 1. Context & Risk Analysis (Pre-Mortem)
- **Context:** Enhancing Timeseek with user-requested privacy (blacklist), organization (annotations), maintenance (pruning), and discovery (filters) features.
- **Technical Risk:**
    - Database schema migrations might fail if not handled defensively.
    - Blacklist logic in the main recording loop could introduce latency or crashes if app name retrieval fails.
    - Auto-pruning might delete data unexpectedly if the retention logic is flawed.
- **Mitigation:**
    - Use `PRAGMA table_info` for safe schema updates.
    - Wrap active app retrieval in try-except blocks.
    - Implement dry-run or logging for pruning before full activation.

## 2. Global Constraints & Active Rules
- **Active Rules:** Follow Material Design 3 (M3) principles for all UI additions. Ensure all assets remain local-first.
- **Avoid Errors:** ERR-PY-OVERSHADOW, ERR-DB-SCHEMA-MISMATCH.

## 3. Sequenced Task Checklist

- [ ] Task 1: **Builder 🏗️** - Implement App Blacklist
  - **Read Boundary:** `timeseek/config.py`, `timeseek/screenshot.py`
  - **Write/Modify Boundary:** `timeseek/config.py`, `timeseek/screenshot.py`
  - **Verification:** Run `python3 -m timeseek.screenshot` (if testable) or verify logic flow.
  - **Target Staging Memory:** `docs/staged/four_features_expansion-builder-25-05-2024-blacklist.md`

- [ ] Task 2: **Builder 🏗️** & **Taste 💅** - Implement Snapshot Annotations
  - **Read Boundary:** `timeseek/database.py`, `timeseek/app.py`, `timeseek/templates/timeline.html`
  - **Write/Modify Boundary:** `timeseek/database.py`, `timeseek/app.py`, `timeseek/templates/timeline.html`
  - **Verification:** Check DB column existence; test POST /update_note endpoint.
  - **Target Staging Memory:** `docs/staged/four_features_expansion-builder-25-05-2024-annotations.md`

- [ ] Task 3: **Builder 🏗️** & **Bug Hunter 🐛** - Implement Auto-Pruning Engine
  - **Read Boundary:** `timeseek/config.py`, `timeseek/database.py`, `timeseek/app.py`
  - **Write/Modify Boundary:** `timeseek/config.py`, `timeseek/database.py`, `timeseek/app.py`
  - **Verification:** Mock old data and ensure it's deleted on startup.
  - **Target Staging Memory:** `docs/staged/four_features_expansion-builder-25-05-2024-pruning.md`

- [ ] Task 4: **Builder 🏗️** & **Taste 💅** - Advanced Search Filters
  - **Read Boundary:** `timeseek/app.py`, `timeseek/templates/search.html`
  - **Write/Modify Boundary:** `timeseek/app.py`, `timeseek/templates/search.html`
  - **Verification:** Perform search with app filter and verify results.
  - **Target Staging Memory:** `docs/staged/four_features_expansion-builder-25-05-2024-search.md`

- [ ] Task 5: **Inspector 🧐** & **Scribe 📜** - Quality Assurance & Docs
  - **Read Boundary:** All modified files, `README.md`
  - **Write/Modify Boundary:** `README.md`, `docs/index.md`
  - **Verification:** Ensure all tests pass and documentation is up to date.
