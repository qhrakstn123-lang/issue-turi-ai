---
name: shortsflow-ui-designer
description: Use when planning or changing frontend/web ShortsFlow UI, mapping backend fields to React components, adding source-first UI, updating JSON export, or distinguishing real planning features from placeholders.
---

# ShortsFlow UI Designer

Use this skill for `frontend/web` Next.js + React + TypeScript UI work.

## Required Reading

Before UI work, read:

- `docs/UI_DESIGN_GUIDE.md`
- `docs/FRONTEND_BACKEND_CONTRACT.md`
- `docs/SOURCE_FIRST_WORKFLOW.md`
- `docs/HANDOFF.md`

## Boundaries

- Work in `frontend/web` unless explicitly told otherwise.
- Do not add new product UI features to `frontend/app`; it is legacy 안내/호환 UI.
- Do not change backend domain/application/pipeline logic for UI-only work.
- Do not add external URL fetch, crawl, download, screenshot, or Google image search.
- Do not mix image generation, TTS, MP4 rendering, DB persistence, login, or payment into UI tasks unless explicitly scoped.

## UI Principles

- Keep ShortsFlow as a dark-mode SaaS production studio.
- Preserve source-capture-first workflow.
- Treat AI images as support/background/replacement cuts, not the default visual plan.
- Clearly separate real features from placeholder/future features.
- Risky source material should surface rights, privacy, portrait-right, and defamation review needs.

## Data Contract Checklist

When backend fields or frontend-only state are added:

1. Map the field to a display surface using `docs/FRONTEND_BACKEND_CONTRACT.md`.
2. Decide whether it belongs in `SceneCard`, `TimelinePanel`, `SafetyReviewPanel`, `AssetCandidateRegister`, Source-first Project Form, or JSON export.
3. Add defensive rendering for optional fields and old result shapes.
4. Confirm JSON export still includes `generation_result`, optional `source_brief`, and `asset_source_candidates`.
5. Keep frontend-only state explicit: manual scene edits, source brief, and asset source candidates can disappear on refresh before DB persistence.

## Verification

Before calling UI work complete, run:

```powershell
uv run --project . --with pytest pytest -q
cd frontend/web
npm run typecheck
npm run lint
npm run build
```
