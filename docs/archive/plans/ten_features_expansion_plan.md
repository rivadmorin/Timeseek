---
plan_id: ten_features_expansion
title: "Orchestration Plan: Ten Features Expansion"
goal: "Implement 10 new features to enhance utility, privacy, and insights in Timeseek."
status: executing
created: 2026-07-07
updated: 2026-07-07
---

# Orchestration Plan: Ten Features Expansion

## 1. Context & Risk Analysis (Pre-Mortem)
- **Context:** Timeseek has a solid M3 foundation. These 10 features expand its capabilities into data management (deletion, optimization), better UX (dark mode, copy-to-click), and analytics (heatmap, word cloud).
- **Technical Risk:**
    - Database schema migrations for new settings/metadata.
    - PDF library size/dependency issues for "Offline/Portable" goal.
    - Performance overhead of keyword blacklisting during recording.
- **Mitigation:**
    - Use defensive schema migrations.
    - Prioritize lightweight or built-in libraries for exports.
    - Optimize keyword matching with sets or Aho-Corasick if needed.

## 2. Global Constraints & Active Rules
- **Active Rules:**
    - Maintain "Offline-First" (No CDNs).
    - M3 Design compliance.
    - Defensive database migrations.
- **Avoid Errors:**
    - [ERR-SQLITE-LOCKED] - Ensure connections are closed or use WAL.

## 3. Sequenced Task Checklist

### Phase 1: UX & Privacy Quick Wins
- [ ] Task 1: **Builder 🏗️** & **Taste 💅** - Implement **Click-to-Copy OCR Text** (Feature 3).
  - **Read Boundary:** `timeseek/templates/timeline.html`, `timeseek/templates/search.html`
  - **Write/Modify Boundary:** `timeseek/templates/timeline.html`, `timeseek/templates/search.html`, `timeseek/static/js/app.js`
  - **Verification:** Click copy button, verify clipboard content.
- [ ] Task 2: **Builder 🏗️** & **Taste 💅** - Implement **Dark/Light Mode Toggle** (Feature 5).
  - **Read Boundary:** `timeseek/templates/layout.html`, `timeseek/static/css/m3-tokens.css`
  - **Write/Modify Boundary:** `timeseek/templates/layout.html`, `timeseek/static/css/custom.css`, `timeseek/static/js/app.js`
  - **Verification:** Toggle theme, verify CSS variables update and persist in localStorage.
- [ ] Task 3: **Builder 🏗️** & **Sentinel 🛡️** - Implement **Keyword Blacklist** (Feature 7).
  - **Read Boundary:** `timeseek/config.py`, `timeseek/screenshot.py`, `timeseek/ocr.py`
  - **Write/Modify Boundary:** `timeseek/config.py`, `timeseek/screenshot.py`
  - **Verification:** Add "Sensitive" to blacklist, record a screen with that word, verify it is NOT saved.
- [ ] Task 4: **Builder 🏗️** & **Bug Hunter 🐛** - Implement **Bulk Time-Range Deletion** (Feature 6).
  - **Read Boundary:** `timeseek/database.py`, `timeseek/app.py`, `timeseek/templates/dashboard.html`
  - **Write/Modify Boundary:** `timeseek/database.py`, `timeseek/app.py`, `timeseek/templates/dashboard.html`
  - **Verification:** Delete "Last 1 Hour", verify DB entries and files are gone.

### Phase 2: Dashboard & Insights
- [ ] Task 5: **Builder 🏗️** & **Taste 💅** - Implement **Activity Heatmap Dashboard** (Feature 2).
  - **Read Boundary:** `timeseek/app.py`, `timeseek/templates/dashboard.html`
  - **Write/Modify Boundary:** `timeseek/app.py`, `timeseek/templates/dashboard.html`, `timeseek/static/js/heatmap.js`
  - **Verification:** View dashboard, see heatmap populated with historical data.
- [ ] Task 6: **Builder 🏗️** & **Scholar 🧠** - Implement **Top Keywords Word Cloud** (Feature 9).
  - **Read Boundary:** `timeseek/app.py`, `timeseek/database.py`, `timeseek/templates/dashboard.html`
  - **Write/Modify Boundary:** `timeseek/app.py`, `timeseek/templates/dashboard.html`
  - **Verification:** Verify word cloud displays most frequent OCR words.
- [ ] Task 7: **Builder 🏗️** & **Scholar 🧠** - Implement **Smart Categorization (App Groups)** (Feature 4).
  - **Read Boundary:** `timeseek/utils.py`, `timeseek/app.py`, `timeseek/templates/timeline.html`
  - **Write/Modify Boundary:** `timeseek/utils.py`, `timeseek/app.py`, `timeseek/templates/timeline.html`
  - **Verification:** Apps like "VS Code" categorized as "Development".

### Phase 3: Utilities & Optimization
- [ ] Task 8: **Builder 🏗️** & **Nomad 💾** - Implement **Storage Optimizer** (Feature 10).
  - **Read Boundary:** `timeseek/config.py`, `timeseek/screenshot.py`
  - **Write/Modify Boundary:** `timeseek/config.py`, `timeseek/screenshot.py`
  - **Verification:** Lower quality setting, verify file sizes decrease.
- [ ] Task 9: **Builder 🏗️** & **Nomad 💾** - Implement **Multi-Language OCR Support** (Feature 8).
  - **Read Boundary:** `timeseek/ocr.py`, `timeseek/config.py`
  - **Write/Modify Boundary:** `timeseek/ocr.py`, `timeseek/config.py`
  - **Verification:** Change language to 'fr', verify OCR still works for French text.
- [ ] Task 10: **Builder 🏗️** & **Scribe 📜** - Implement **Export to PDF/Image** (Feature 1).
  - **Read Boundary:** `timeseek/app.py`, `timeseek/templates/timeline.html`
  - **Write/Modify Boundary:** `timeseek/app.py`, `timeseek/templates/timeline.html`
  - **Verification:** Click Export, receive PDF with image and OCR text.

## 4. Final Review & Submit
- [ ] Final Task: **Orchestrator 🕴️** - Consolidate memories and submit PR.
