# Issue Turi AI - Codex Project Instructions

## Project Goal

This project is an AI content creation tool for the YouTube channel "이슈털이".

Final goal:
topic input -> script -> scenes -> subtitles -> visual prompts -> image/TTS generation -> motion directions -> sound cues -> timeline -> MP4 rendering.

Current phase:
MVP 1 / structure hardening.

Current MVP goal:
- Generate a shorts planning document.
- Use fake agents only.
- Do not call real OpenAI, ElevenLabs, image generation, TTS, or rendering APIs yet.
- Keep the app simple and testable.

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
- frontend: static UI for MVP
- tests: automated tests
- docs: project documentation
- prompts: prompt templates

Dependency direction:
presentation -> application -> domain

Domain must not know about:
- OpenAI
- ElevenLabs
- Remotion
- FFmpeg
- HTTP
- frontend
- database implementation

Infrastructure should implement external details.

## Agent Rules

Agents should be separated by responsibility.

Current fake agents must remain available for tests.

Before real AI integration:
- define agent interfaces/protocols
- keep fake agents for testing
- make pipelines depend on interfaces, not fake classes
- validate AI output before using it

Recommended agent concepts:
- ScriptWriterAgent
- StoryboardAgent
- VisualAssetSuggestionAgent
- SubtitleAgent
- EditingDirectionAgent
- SoundCueAgent
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
- static frontend tests

Every refactor must keep tests passing.

Preferred test command:
- `uv run --project . --with pytest pytest -q`

## MVP 1 Scope

MVP 1 should support:
- topic input
- target audience input
- style selection
- fake shorts script generation
- scene generation
- subtitle generation
- emphasis caption generation
- visual prompt suggestion
- motion direction suggestion
- sound cue suggestion
- safety review note
- preview in browser

MVP 1 does not need:
- real AI API
- real image generation
- real TTS
- real video rendering
- database persistence
- login
- deployment
- payment

## Future Phases

MVP 2:
- real LLM provider
- prompt modules
- JSON validation
- error handling

MVP 3:
- persistence with SQLite or another repository

MVP 4:
- image generation provider
- TTS provider
- asset storage
- timeline builder

MVP 5:
- Remotion or FFmpeg MP4 rendering
- render job manager
- MP4 download

Later:
- Instagram card news
- trend/topic sourcing
- longform video
- YouTube/Instagram upload

## Safety and Copyright Rules

Do not copy reference channels.

Reference channels are only for general production grammar:
- hook style
- subtitle rhythm
- pacing
- scene structure
- motion style
- sound cue timing

Do not copy:
- exact scripts
- exact captions
- thumbnails
- branding
- unique expressions
- downloaded YouTube clips
- broadcast footage without rights

Prefer:
- AI-generated visuals
- licensed stock assets
- self-made motion graphics
- safe sound effects
- user-provided materials with permission

Risky topics should be marked as requiring review.
Do not present rumors as confirmed facts.
Avoid excessive personal attacks or defamatory claims.

## Frontend Rules

Current frontend is a simple static MVP.
Keep it simple until backend structure is stable.
Do not introduce heavy frameworks unless requested.

Development server:
- `uv run --project . python -m backend.src.presentation.http.server`

Browser URL:
- `http://127.0.0.1:8000`

## Refactoring Rules

When refactoring:
- keep behavior unchanged
- update tests
- avoid large unrelated changes
- explain changed files
- run tests
- provide the next recommended step

Do not combine structural refactor with real AI integration in the same change.
