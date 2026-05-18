# Issue Turi AI - Codex Project Instructions

## Project Goal

This project is an AI content creation tool for the YouTube channel "이슈털이".

Final goal:

```text
topic/source input
-> script
-> scenes
-> subtitles
-> visual sourcing
-> source capture plan
-> motion directions
-> sound cues
-> timeline
-> image/TTS generation
-> MP4 rendering
```

Current phase: MVP 1 / planning and preview hardening.

Current MVP goal:

- Generate a shorts planning document and browser preview.
- Use fake agents by default.
- Use real LLM agents only when `ISSUE_TURI_LLM_PROVIDER` is `openai` or `real`.
- Do not call ElevenLabs, image generation, TTS, rendering, crawling, or screenshot APIs yet.
- Keep the app simple and testable.

## Product Direction

ShortsFlow is source-capture-first, not AI-image-first.

Topic-only input remains supported, but the preferred workflow uses `source_url`, `source_type`, `source_title`, `source_context`, and `source_angle`.

`source_context` is user-provided text. Do not automatically fetch, crawl, scrape, download, search, or screenshot external URLs.

AI images are support/background/replacement cuts, not the default visual plan.

Before Source Capture Plan or frontend UI work, read:

- `docs/SOURCE_FIRST_WORKFLOW.md`
- `docs/UI_DESIGN_GUIDE.md`
- `docs/FRONTEND_BACKEND_CONTRACT.md`
- `.agents/skills/shortsflow-production-grammar/SKILL.md`
- `.agents/skills/shortsflow-ui-designer/SKILL.md`

For source-first UI changes, always check the backend/frontend contract and JSON export shape together.

## Python and uv Rules

Use uv for all Python commands.
Use Python 3.12.
Respect `.python-version`.

Preferred commands:

- `uv run --project . --with pytest pytest -q`
- `uv run --project . python -m backend.src.presentation.http.server`
- `uv run --project . python --version`

Do not suggest pip commands unless explicitly requested.

## Git Rules

Do not commit:

- `.venv/`
- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`
- `.env`
- generated media outputs
- rendered videos
- storage files
- logs

Before committing, run:

- `git add -n .`
- `uv run --project . --with pytest pytest -q`

Avoid broad Git commands unless specifically requested:

- `git add ..`
- `git add -A`

## Architecture Rules

Keep the layered structure:

- domain: core models and rules
- application: use cases, agents, pipelines, services
- infrastructure: external clients, repositories, providers, renderers
- presentation: HTTP/API layer
- frontend/web: primary Next.js + React + TypeScript UI
- frontend/app: legacy static 안내/호환 UI
- tests: automated tests
- docs: project documentation
- prompts: prompt templates

Dependency direction:

```text
presentation -> application -> domain
```

Domain must not know about OpenAI, ElevenLabs, Remotion, FFmpeg, HTTP, frontend, or database implementation.

Infrastructure should implement external details.

## Agent Rules

Agents should be separated by responsibility.

Current fake agents must remain available for tests.

Before real AI integration:

- define agent interfaces/protocols
- keep fake agents for testing
- make pipelines depend on interfaces, not fake classes
- validate AI output before using it

Current real agent concepts:

- ScriptWriterAgent
- StoryboardAgent
- SubtitleAgent
- VisualAssetSuggestionAgent
- EditingDirectionAgent
- SafetyReviewAgent

## Testing Rules

Tests must not call real external APIs.
Use fake agents and fake providers.

Required test areas:

- domain model tests
- pipeline tests
- service tests
- HTTP API tests
- HTTP server tests
- frontend tests

Every refactor must keep tests passing.

Preferred test command:

```powershell
uv run --project . --with pytest pytest -q
```

## MVP Scope

MVP supports:

- topic input
- source-first metadata input
- target audience input
- style selection
- fake shorts script generation
- scene generation
- subtitle generation
- emphasis caption generation
- visual prompt suggestion
- visual sourcing strategy
- motion direction suggestion
- sound cue suggestion
- safety review note
- timeline planning
- production beats
- asset review checklist
- frontend-only Manual Scene Edit
- frontend-only Manual Asset Register
- JSON export
- browser preview

MVP does not need automatic URL crawling/capture/download, Google image automatic search/download, real image generation, real TTS, real video rendering, database persistence, login, deployment, or payment.

## Safety and Copyright Rules

Do not copy reference channels.

Reference channels:

- 강석주
- 뇌전구
- 얘봐라

Upload channel:

- 이슈털이

Reference channels are only for general production grammar: first-second hook, subtitle rhythm, pacing, scene structure, source-screen composition, motion style, and sound cue timing.

Do not copy exact scripts, exact captions, thumbnails, TTS voice or speech style, edit tempo or cut structure, branding, unique expressions, downloaded YouTube clips, broadcast footage without rights, logos, captures, images, or original comments without permission/review.

Risky topics should be marked as requiring review. Do not present rumors as confirmed facts. Avoid excessive personal attacks or defamatory claims.

## Frontend Rules

Current primary frontend is `frontend/web`, a Next.js + React + TypeScript ShortsFlow UI.

`frontend/app` is a legacy static 안내/호환 page. Keep it available, but do not add new product UI features there.

Future UI work should target `frontend/web` unless explicitly requested.

Before frontend UI work:

- read `docs/UI_DESIGN_GUIDE.md`
- read `docs/FRONTEND_BACKEND_CONTRACT.md`
- follow `.agents/skills/shortsflow-ui-designer/SKILL.md`

Backend/API server:

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

Primary browser URL:

```text
http://localhost:3000
```

Backend and legacy URL:

```text
http://127.0.0.1:8000
```

## Refactoring Rules

When refactoring:

- keep behavior unchanged
- update tests
- avoid large unrelated changes
- explain changed files
- run tests
- provide the next recommended step

Do not combine structural refactor with real AI integration in the same change.

## Documentation Rules

Keep project documentation current:

- When an important troubleshooting issue happens, record it in `docs/TROUBLESHOOTING.md`.
- When a major feature or milestone is completed, update `docs/DEVELOPMENT_LOG.md`.
- When architecture, provider modes, pipeline structure, frontend/backend contract, or technical stack changes, update `docs/TECH_STACK.md` and related docs.
- Documentation-only tasks must not change feature code, API behavior, frontend behavior, prompts, or tests unless explicitly requested.
- Do not record API keys, secrets, or `.env` values in documentation.
