---
plan_id: stability_aesthetics
title: "Orchestration Plan: Stability & Aesthetics Refinement"
goal: "Fix database schema mismatch, broken UI image paths, and improve theme toggle logic."
status: draft
created: 2026-07-06
updated: 2026-07-06
---

# Orchestration Plan: Stability & Aesthetics Refinement

## 1. Context & Risk Analysis (Pre-Mortem)
- **Context:** The application has a critical runtime error where `insert_entry` is called with more arguments than defined. Furthermore, the database schema lacks a `filename` column, causing images to be unreachable in the UI which expects a different naming convention.
- **Technical Risk:** Adding a column to an existing SQLite database requires careful execution to avoid data loss, although the project is in early development.
- **Mitigation:** Update `create_db` to include the `filename` column and update `insert_entry` to store it. UI templates will be updated to use this `filename`.

## 2. Global Constraints & Active Rules
- **Active Rules:**
  - Respect Material 3 (M3) design tokens.
  - Offline-first execution.
- **Avoid Errors:**
  - ERR-PY-OVERSHADOW: Do not shadow existing functions.
  - ERR-DB-SCHEMA: Ensure schema migrations are handled (add column if missing).

## 3. Sequenced Task Checklist

- [ ] Task 1: Bug Hunter 🐛 - Fix Database Schema and insert_entry mismatch
  - **Read Boundary:**
    - [openrecall/database.py](file:///app/openrecall/database.py)
    - [openrecall/screenshot.py](file:///app/openrecall/screenshot.py)
  - **Write/Modify Boundary:**
    - [openrecall/database.py](file:///app/openrecall/database.py)
  - **Depends On:** None
  - **Verification & Testing:**
    - Command: `python3 -c "from openrecall.database import create_db; create_db()"`
    - Success Criteria: Database schema contains `filename` column.
  - **Target Staging Memory:** `docs/staged/stability_aesthetics-bughunter-06-07-2026-t1.md`

- [ ] Task 2: Bug Hunter 🐛 - Fix broken UI image paths in templates
  - **Read Boundary:**
    - [openrecall/database.py](file:///app/openrecall/database.py)
    - [openrecall/templates/timeline.html](file:///app/openrecall/templates/timeline.html)
    - [openrecall/templates/search.html](file:///app/openrecall/templates/search.html)
  - **Write/Modify Boundary:**
    - [openrecall/database.py](file:///app/openrecall/database.py)
    - [openrecall/templates/timeline.html](file:///app/openrecall/templates/timeline.html)
    - [openrecall/templates/search.html](file:///app/openrecall/templates/search.html)
  - **Depends On:** Task 1
  - **Verification & Testing:**
    - Manual: Verify images display correctly in both Timeline and Search views.
    - Success Criteria: HTML img tags use the correct `filename` from the database.
  - **Target Staging Memory:** `docs/staged/stability_aesthetics-bughunter-06-07-2026-t2.md`

- [ ] Task 3: Inspector 🧐 - Centralize configuration (Port) and Cleanup
  - **Read Boundary:**
    - [openrecall/app.py](file:///app/openrecall/app.py)
    - [openrecall/config.py](file:///app/openrecall/config.py)
  - **Write/Modify Boundary:**
    - [openrecall/app.py](file:///app/openrecall/app.py)
    - [openrecall/config.py](file:///app/openrecall/config.py)
  - **Depends On:** Task 2
  - **Verification & Testing:**
    - Command: `python3 -m py_compile openrecall/app.py`
    - Success Criteria: Port is read from `config.py`.
  - **Target Staging Memory:** `docs/staged/stability_aesthetics-inspector-06-07-2026-t3.md`

- [ ] Task 4: Taste 💅 - Refine UI Aesthetics and Theme Toggle
  - **Read Boundary:**
    - [openrecall/templates/layout.html](file:///app/openrecall/templates/layout.html)
  - **Write/Modify Boundary:**
    - [openrecall/templates/layout.html](file:///app/openrecall/templates/layout.html)
  - **Depends On:** Task 3
  - **Verification & Testing:**
    - Manual: Verify theme toggle icon correctly represents the *next* or *current* state intuitively.
    - Success Criteria: UI feels polished and adheres to M3 logic.
  - **Target Staging Memory:** `docs/staged/stability_aesthetics-taste-06-07-2026-t4.md`
