# ShortsFlow Product Plan

## Service Definition

ShortsFlow is an AI Shorts Planning Studio. A creator enters a topic, target audience, tone, style, and desired length; the system generates structured shorts planning data for human review.

Current output includes:

- script direction
- storyboard scenes
- subtitles and emphasis captions
- visual suggestions and generated-image prompts
- visual sourcing strategy
- editing directions
- sound cue hints
- safety and rights review flags
- timeline data
- production beats
- scene-level asset review checklist
- frontend-only manual asset source candidates

## Current Status

Completed:

- fake MVP pipeline
- optional OpenAI/real LLM pipeline
- real agent chain through safety review
- visual sourcing strategy
- safety review fields
- `GenerationResult.timeline`
- scene production beats
- scene asset review checklist
- Next.js + React + TypeScript primary UI in `frontend/web`
- legacy static UI retained in `frontend/app`
- same-origin Next.js `/api/...` proxy to Python backend
- JSON export with `generation_result` and `asset_source_candidates`
- manual real smoke command
- automated fake-mode tests

Not implemented:

- database persistence
- project reopen/list from DB
- real image generation
- TTS generation
- asset storage
- MP4 rendering
- login
- payment
- deployment
- upload automation

## Frontend Direction

Primary UI:

```text
frontend/web
http://localhost:3000
```

If Next.js chooses another dev port, use the actual port printed by `npm run dev`.

Backend and legacy page:

```text
http://127.0.0.1:8000
```

`frontend/app` is a legacy 안내/호환 page. It should remain available, but new UI features should be built in `frontend/web`.

## Provider Direction

Default mode is fake.

Real LLM mode is available only when:

```text
ISSUE_TURI_LLM_PROVIDER=openai
```

or:

```text
ISSUE_TURI_LLM_PROVIDER=real
```

The current real pipeline is:

```text
RealScriptWriterAgent
-> RealStoryboardAgent
-> RealSubtitleAgent
-> RealVisualAssetSuggestionAgent
-> RealEditingDirectionAgent
-> RealSafetyReviewAgent
```

Automated tests must not call real external APIs.

## Roadmap

### Phase 1: Manual Edit / Scene 수정 UI

Goal: let users correct generated planning data before persistence or media generation.

Scope:

- `frontend/web` only unless explicitly scoped otherwise
- scene text/caption/sourcing/editing fields
- local state and JSON export first
- no real media generation
- no changes to `frontend/app`

### Phase 2: Publishing Readiness

Goal: add upload-readiness planning data before DB and renderer work.

Candidate fields:

- originality risk
- reused-content risk
- monetization risk
- source-rights risk
- required human checks
- upload-blocking notes

### Phase 3: DB Persistence

Goal: preserve projects and edited planning results.

Candidate implementation:

- SQLite repository
- project list
- project detail reopen
- scene edit save
- exported JSON from saved state

### Phase 4: Asset and Media Providers

Goal: generate and store real production assets.

Deferred until planning/edit/review contracts are stable:

- image provider
- TTS provider
- asset storage
- render job manager
- MP4 renderer

## MVP Exclusions

Do not include in the current MVP slice:

- downloaded reference-channel footage
- copyrighted broadcast clips without rights
- automatic scraping of risky media
- payment
- team collaboration
- upload automation
