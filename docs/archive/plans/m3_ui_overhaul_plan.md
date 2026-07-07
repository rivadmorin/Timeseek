---
plan_id: m3_ui_overhaul
title: "Orchestration Plan: Material Design 3 UI Overhaul"
goal: "Complete redesign of Timeseek UI using M3, supporting light/dark modes and offline functionality."
status: completed
created: 2026-07-06
updated: 2026-07-06
---

# Orchestration Plan: Material Design 3 UI Overhaul

## 1. Context & Risk Analysis (Pre-Mortem)
- **Context:** Timeseek is a local-first application for desktop. The current UI is functional but lacks modern design standards.
- **Technical Risk:** Potential breaking of Flask routing or Jinja2 template logic. Dependency on online CDNs for Material components which conflicts with the offline-first requirement.
- **Mitigation:** Use Nomad 💾 to localize all assets. Perform atomic commits for each template. Verify functionality after every major UI change.

## 2. Global Constraints & Active Rules
- **Active Rules:** Must support both Light and Dark modes. Must work 100% offline. Use Material Design 3 (M3) components and tokens.
- **Avoid Errors:** ERR-0001 (Duplicate functions - identified in previous plan).

## 3. Sequenced Task Checklist

- [ ] Task 1: Design 🎨 - Generate M3 Mockups via Stitch
  - **Read Boundary:**
    - [timeseek/templates/](file:///app/timeseek/templates/)
  - **Write/Modify Boundary:**
    - [docs/staged/m3_ui_overhaul-design-06-07-2026-v1.md](file:///app/docs/staged/)
  - **Depends On:** None
  - **Verification & Testing:** User approval of visual mockups.
  - **Target Staging Memory:** `docs/staged/m3_ui_overhaul-design-06-07-2026-v1.md`

- [ ] Task 2: Nomad 💾 - Offline Asset Localization
  - **Read Boundary:**
    - None
  - **Write/Modify Boundary:**
    - [timeseek/static/](file:///app/timeseek/static/)
  - **Depends On:** Task 1
  - **Verification & Testing:** Check if CSS/JS files are accessible via local paths in browser.
  - **Target Staging Memory:** `docs/staged/m3_ui_overhaul-nomad-06-07-2026-v1.md`

- [ ] Task 3: Material 📐 - Design System Configuration
  - **Read Boundary:**
    - [docs/init/Material 📐 - Google Jules.md](file:///app/docs/init/)
  - **Write/Modify Boundary:**
    - [timeseek/static/css/m3-tokens.css](file:///app/timeseek/static/css/m3-tokens.css)
  - **Depends On:** Task 2
  - **Verification & Testing:** Inspect element styles to ensure M3 tokens are applied.
  - **Target Staging Memory:** `docs/staged/m3_ui_overhaul-material-06-07-2026-v1.md`

- [ ] Task 4: Builder 🏗️ - Template Refactoring & UX Logic
  - **Read Boundary:**
    - [timeseek/templates/](file:///app/timeseek/templates/)
    - [timeseek/app.py](file:///app/timeseek/app.py)
  - **Write/Modify Boundary:**
    - [timeseek/templates/](file:///app/timeseek/templates/)
    - [timeseek/app.py](file:///app/timeseek/app.py)
  - **Depends On:** Task 3
  - **Verification & Testing:** Run `python -m timeseek.app` and verify Search/Timeline functionality.
  - **Target Staging Memory:** `docs/staged/m3_ui_overhaul-builder-06-07-2026-v1.md`

- [ ] Task 5: Taste 💅 - Visual Rhythm & Polish
  - **Read Boundary:**
    - [timeseek/templates/](file:///app/timeseek/templates/)
  - **Write/Modify Boundary:**
    - [timeseek/static/css/custom.css](file:///app/timeseek/static/css/custom.css)
  - **Depends On:** Task 4
  - **Verification & Testing:** Visual inspection for spacing and concentric corners.
  - **Target Staging Memory:** `docs/staged/m3_ui_overhaul-taste-06-07-2026-v1.md`

- [ ] Task 6: Test Pilot 🧪 - Comprehensive Verification
  - **Read Boundary:**
    - [tests/](file:///app/tests/)
  - **Write/Modify Boundary:**
    - [tests/ui_functional_test.py](file:///app/tests/ui_functional_test.py)
  - **Depends On:** Task 5
  - **Verification & Testing:** All tests pass.
  - **Target Staging Memory:** `docs/staged/m3_ui_overhaul-testpilot-06-07-2026-v1.md`

- [ ] Task 7: Scribe 📜 - Documentation Finalization
  - **Read Boundary:**
    - [README.md](file:///app/README.md)
  - **Write/Modify Boundary:**
    - [README.md](file:///app/README.md)
  - **Depends On:** Task 6
  - **Verification & Testing:** Readme reflects new UI features.
  - **Target Staging Memory:** `docs/staged/m3_ui_overhaul-scribe-06-07-2026-v1.md`
