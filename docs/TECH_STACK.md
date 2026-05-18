# Issue Turi AI Tech Stack

## Current Snapshot

Issue Turi AI is currently a ShortsFlow planning MVP. It generates structured shorts planning data, review information, timeline data, and browser previews. It does not generate images, audio, or MP4 files yet.

Primary UI:

```text
frontend/web
Next.js + React + TypeScript
http://localhost:3000
```

Legacy UI:

```text
frontend/app
Static HTML/CSS/JS
Served by the Python backend at http://127.0.0.1:8000
```

`frontend/app` is kept as a legacy 안내/호환 page. Do not add new UI features there. Future UI work should target `frontend/web`.

Product direction: ShortsFlow is source-capture-first, not AI-image-first. AI images are support/background/replacement cuts, not the default visual plan.

## Runtime Topology

Recommended local development flow:

```text
Browser
-> http://localhost:3000
-> Next.js /api proxy
-> internal Python backend at http://127.0.0.1:8000
```

The Python backend still runs on `127.0.0.1:8000`, but that port is now primarily the API server and legacy page host. The ShortsFlow working UI is the Next.js dev server on `localhost:3000`, or the actual dev port printed by Next.js if port 3000 is unavailable.

## Architecture

Layer direction:

```text
presentation -> application -> domain
```

External implementation details live in infrastructure.

```text
frontend/web
  -> presentation/http
  -> application/service
  -> application/pipeline
  -> application/agents
  -> domain/models
  -> infrastructure/openai, prompt loader, repository
```

Current implementation does not use LangChain, LangGraph, RAG, vector DB, or external retrieval. The project uses a direct Python pipeline orchestrator, agent protocols, prompt markdown files, an LLM client wrapper, and JSON validators.

## Backend Stack

- Python 3.12
- uv
- Standard-library HTTP server for the MVP
- In-memory repository
- Optional OpenAI SDK only for manual real-mode checks

Main entry points:

- `backend/src/presentation/http/server.py`: API server and legacy static frontend host
- `backend/src/presentation/http/api.py`: JSON API routes
- `backend/src/presentation/composition.py`: provider-mode composition
- `main.py`: demo, server, and `smoke-real`

## Frontend Stack

### `frontend/web`

This is the current primary UI.

- Next.js App Router
- React
- TypeScript
- Same-origin `/api/...` calls by default
- Route-handler proxy to the Python backend
- ShortsFlow dark-mode SaaS shell

Important files:

- `frontend/web/app/page.tsx`
- `frontend/web/app/layout.tsx`
- `frontend/web/app/globals.css`
- `frontend/web/app/api/[...path]/route.ts`
- `frontend/web/lib/api.ts`
- `frontend/web/lib/types.ts`
- `frontend/web/components/*`

Current components:

- `ProjectForm`
- `ResultSummary`
- `SafetyReviewPanel`
- `SceneCard`
- `VisualSection`
- `SourcingSection`
- `EditingSection`
- `TimelinePanel`
- `AssetCandidateRegister`
- `JsonDownloadButton`

Current source-first frontend state:

- `ProjectForm` supports optional `source_url`, `source_type`, `source_title`, `source_context`, and `source_angle`.
- Topic-only generation still works.
- Source URLs are not fetched, crawled, downloaded, searched, or screenshotted.
- Source-first metadata is exported as `source_brief` when present.
- Source URL/type can seed one unapproved frontend-only `asset_source_candidate` using safety defaults.
- Source-first context can be reflected in the generated planning request by user-provided text, not by reading the external URL.

### `frontend/app`

This is the legacy static UI.

- Keep it available.
- Do not delete it.
- Do not add new product UI features here.
- Use it only as a simple fallback/legacy 안내 page hosted by the Python backend.

## Provider Modes

### fake mode

Default mode.

```text
ISSUE_TURI_LLM_PROVIDER=fake
```

or unset.

Characteristics:

- No API key
- No external API calls
- Deterministic fake agents
- Used for tests and normal MVP development

### openai/real mode

Manual mode only.

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
```

Characteristics:

- Calls the real OpenAI API
- May incur cost
- Never used by automated tests
- Still produces planning JSON only
- Does not generate images, TTS, or MP4

## Current Real Pipeline

When `ISSUE_TURI_LLM_PROVIDER` is `openai` or `real`, the pipeline order is:

```text
RealScriptWriterAgent
-> RealStoryboardAgent
-> RealSubtitleAgent
-> RealVisualAssetSuggestionAgent
-> RealEditingDirectionAgent
-> RealSafetyReviewAgent
```

Field ownership:

- `RealScriptWriterAgent`: script title, narration, target duration, style notes
- `RealStoryboardAgent`: initial `Scene` objects and stable `scene_id` values
- `RealSubtitleAgent`: `subtitle`, `emphasis_caption`
- `RealVisualAssetSuggestionAgent`: visual and sourcing fields
- `RealEditingDirectionAgent`: motion, transition, sound, editing notes
- `RealSafetyReviewAgent`: safety fields on `GenerationResult` only

## Timeline State

`GenerationResult.timeline` is implemented.

The timeline currently includes:

- scene start/end/duration data
- subtitle and emphasis-caption timing
- visual metadata
- motion and transition metadata
- narration audio placeholders
- sound effect timing
- rule-based production beats
- scene-level asset review checklist

This remains a planning layer. It does not render media.

## Manual Asset Register

`frontend/web` includes a scene-level Manual Asset Register.

Scope:

- Frontend only
- No backend API changes
- No persistence after refresh

Users can add, update, approve, and delete `AssetSourceCandidate` items per scene.

Candidate fields include:

- `source_type`
- `source_url`
- `source_title`
- `usage_mode`
- `license_status`
- `needs_blur`
- `needs_rewrite`
- `approved_for_use`
- `review_notes`

Risky license states such as `license_required`, `permission_required`, and `avoid` are visually highlighted.

JSON download exports:

```json
{
  "generation_result": {},
  "asset_source_candidates": []
}
```

## Manual Edit / Scene 수정 UI

`frontend/web` includes a compact frontend-only scene editor inside each `SceneCard`.

Editable fields:

- `narration`
- `tts_text`
- `subtitle`
- `emphasis_caption`
- `estimated_duration`
- `visual_description`
- `generated_image_prompt`
- `asset_usage_note`
- `editing_notes`

Scope:

- Frontend state only
- No backend PATCH call
- No DB persistence
- No changes to backend domain/application/pipeline
- No changes to `frontend/app`

Behavior:

- Edited scenes show an `Edited` badge.
- Each scene can be reverted to the generated original with `원본으로 되돌리기`.
- Edited values update the visible scene card.
- Edited `estimated_duration` rebuilds frontend timeline timing and summary duration.
- JSON download keeps the existing payload shape and includes the edited `generation_result` plus `asset_source_candidates`.
- Edits are lost on refresh because persistence is not implemented yet.

## Visual Sourcing

`RealVisualAssetSuggestionAgent` is a visual sourcing strategy recommender, not just an image prompt generator.

Key fields:

- `visual_asset_type`
- `visual_description`
- `generated_image_prompt`
- `gif_or_clip_suggestion`
- `stock_search_keywords`
- `visual_source_strategy`
- `capture_source_type`
- `capture_usage_mode`
- `asset_usage_note`

Capture is not categorically banned. The system classifies whether material should be direct-capture candidate, mockup, license-required, permission-required, user-provided, or avoided. Final rights review remains human.

Reference channels are 강석주, 뇌전구, and 얘봐라. The upload channel is 이슈털이. They are references only for general fast issue-explainer production grammar. Do not copy scripts, thumbnails, TTS voice/speech style, edit tempo/cut structure, logos, captures, images, or original comments.

## Safety Review

`RealSafetyReviewAgent` is not a legal judge. It structures risk flags for human review.

Safety result fields:

- `safety_status`
- `safety_notes`
- `copyright_risks`
- `rumor_or_defamation_risks`
- `privacy_or_portrait_risks`
- `source_usage_risks`
- `required_human_review`
- `recommended_revisions`

Allowed statuses:

- `approved`
- `needs_review`
- `rejected`

## Excluded Features

Not implemented yet:

- database persistence
- project list/reopen from DB
- real image generation
- real TTS
- asset storage
- MP4 rendering
- render job manager
- login
- payment
- deployment
- upload automation

## Commands

Python tests:

```powershell
uv run --project . --with pytest pytest -q
```

Python version:

```powershell
uv run --project . python --version
```

Backend:

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

Next.js frontend:

```powershell
cd frontend/web
npm run dev
```

Frontend verification:

```powershell
cd frontend/web
npm run typecheck
npm run lint
npm run build
```

## Recommended Next Technical Direction

Recommended sequence:

1. Source Capture Plan
   - Add scene-level primary capture, mockup/rewrite, fallback/backup asset, and source review fields.
   - Keep it as planning/review data.

2. Publishing Readiness
   - Add originality, reused-content, monetization, source-rights, and human-check planning fields.
   - Keep it as planning/review data.

3. DB persistence
   - Add SQLite or another repository once the edited planning contract is stable.

4. Media providers
   - Image/TTS/asset storage/rendering after planning and review data are stable.
