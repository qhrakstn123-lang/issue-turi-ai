# ShortsFlow Product Plan

## Service Definition

ShortsFlow is a source-capture-first AI Shorts Planning Studio. A creator can still enter a topic, target audience, tone, style, and desired length, but the preferred product direction is to plan shorts from original sources such as community links, news, YouTube, broadcast material, Instagram, Google image references, stock sites, and user-provided material.

Read [docs/SOURCE_FIRST_WORKFLOW.md](SOURCE_FIRST_WORKFLOW.md) before planning the next feature slice.

AI images are not the default visual strategy. They are support assets for background shots, replacement cuts, or scenes where original source material is insufficient, risky, or unavailable.

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

Preferred source-first inputs:

- `source_url`
- `source_type`
- `source_title`
- `source_context`
- `source_angle`

ShortsFlow must not automatically fetch, crawl, download, or capture external URLs.

Reference channels are 강석주, 뇌전구, and 얘봐라. The upload channel is 이슈털이. These channels are references only for general fast issue-explainer production grammar such as first-second hooks, large subtitle rhythm, source-screen pacing, and reaction-to-context structure.

ShortsFlow must not copy reference-channel script sentences, thumbnails, TTS voice or speech style, edit tempo/cut structure, logos, captures, images, or original comments. The output should be rebuilt as an original 이슈털이 format.

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
- Source-first Project Form in `frontend/web`
- optional `source_brief` JSON export
- source-first initial `asset_source_candidate` creation with safety defaults

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
- automatic crawling/capture/download
- thumbnail generation

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

### Phase 1: Source-first Project Form

Goal: make source-first input the primary planning flow while preserving topic-only input for quick ideation and fake-mode tests.

Status: first frontend-only slice implemented.

Scope:

- `frontend/web` only unless explicitly scoped otherwise
- source URL/type/title/context/angle fields
- no URL fetch, crawl, scrape, capture, or download
- no real media generation
- no changes to `frontend/app`
- source-first metadata is exported as `source_brief`
- source URL/type can seed one unapproved source-review asset candidate

### Phase 2: Source Capture Plan

Goal: structure how each scene should use source captures, mockups, licensed/user-provided assets, Google image references, and AI-generated support visuals.

Candidate fields:

- `primary_asset_plan`
- `capture_target`
- `fallback_asset_plan`
- `backup_asset_plan`
- `ai_image_needed`
- `source_review_note`

### Phase 3: Manual Screenshot / Capture Asset Upload

Goal: let users manually register their own captured/uploaded assets and review metadata without automatic crawling or downloading.

### Phase 4: Thumbnail Planner

Goal: plan thumbnail concepts from safe source material, mockups, and generated support visuals without copying reference-channel thumbnails.

### Phase 5: TTS Script / Voice Direction

Goal: refine narration text and voice direction before any TTS provider is added.

### Phase 6: Publishing Readiness

Goal: add upload-readiness planning data before DB and renderer work.

Candidate fields:

- originality risk
- reused-content risk
- monetization risk
- source-rights risk
- required human checks
- upload-blocking notes

### Phase 7: DB Persistence

Goal: preserve projects and edited planning results.

Candidate implementation:

- SQLite repository
- project list
- project detail reopen
- scene edit save
- exported JSON from saved state

### Phase 8: Asset and Media Providers

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
- automatic URL crawling/capture/download
- AI-image-first visual planning
- payment
- team collaboration
- upload automation
