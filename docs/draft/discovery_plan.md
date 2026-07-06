---
plan_id: discovery
title: "Orchestration Plan: Deep Discovery & Stabilization"
goal: "Fix critical bugs and refactor UI for better maintainability"
status: executing
created: 2024-05-25
updated: 2024-05-25
---

# Orchestration Plan: Deep Discovery & Stabilization

## 1. Context & Risk Analysis
- **Context:** The codebase has critical "shadow bugs" (duplicate functions) and mixed concerns (UI in app.py).
- **Technical Risk:** Deleting the wrong function definition could break multi-monitor support.
- **Mitigation:** Carefully compared definitions before deletion.

## 3. Sequenced Task Checklist

- [x] Task 1: Bug Hunter 🐛 - Fix duplicate record_screenshots_thread
- [x] Task 2: Inspector 🧐 - Refactor Flask templates to separate files
- [x] Task 3: Test Pilot 🧪 - Align NLP cosine similarity tests
- [ ] Task 4: Scribe 📜 - Update README with new project structure
