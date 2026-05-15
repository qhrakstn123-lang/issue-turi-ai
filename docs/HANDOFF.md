# Issue Turi AI Handoff

## Current Status

Default mode is the fake MVP pipeline.

`ISSUE_TURI_LLM_PROVIDER=openai` or `real` uses the current real mixed pipeline:

1. `RealScriptWriterAgent`
2. `RealStoryboardAgent`
3. `RealSubtitleAgent`
4. `RealVisualAssetSuggestionAgent`
5. `RealEditingDirectionAgent`
6. `RealSafetyReviewAgent`

Not implemented yet:
- image generation
- TTS
- MP4 rendering
- database persistence
- upload/deployment/payment flows

Recently added:
- Browser preview shows visual sourcing and safety review details.
- Browser-only JSON download exports the current `GenerationResult`.
- Optional Next.js + React + TypeScript frontend exists under `frontend/web`.
- `frontend/web` has been redesigned as a ShortsFlow dark-mode SaaS planning studio.
- `GenerationResult.timeline` is now returned by the backend and shown in the Next.js `TimelinePanel`.
- The Next.js app now uses same-origin `/api/...` routes on `localhost:3000`; those route handlers proxy to the internal Python backend at `127.0.0.1:8000`.
- Timeline scenes now include rule-based production beats and an asset review checklist.

## Must Read First

Read these before making changes:

- `AGENTS.md`
- `.agents/skills/issue-turi-shorts-generation/SKILL.md`
- `README.md`
- `docs/HANDOFF.md`
- `docs/current-project-state.md`
- `docs/TECH_STACK.md`
- `docs/TROUBLESHOOTING.md`
- `docs/DEVELOPMENT_LOG.md`

## Test Command

```powershell
uv run --project . --with pytest pytest -q
```

Automated tests must not call real OpenAI or any external API.

## Frontend Options

Static MVP frontend:

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

Open:

```text
http://127.0.0.1:8000
```

Optional Next.js frontend:

```powershell
cd frontend/web
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

The Next.js app uses same-origin `/api/...` calls by default. The browser should stay on `http://localhost:3000`; Next route handlers proxy API traffic to the internal Python backend. Set `BACKEND_API_BASE_URL` only if the backend runs somewhere other than `http://127.0.0.1:8000`.

## Project Documentation

- `docs/current-project-state.md`: beginner-friendly summary of what currently runs and what the web page does.
- `docs/RUNNING.md`: local backend, static frontend, and Next.js frontend running guide.
- `docs/TECH_STACK.md`: technical stack, architecture, pipeline, provider modes, test/smoke commands, and excluded features.
- `docs/TROUBLESHOOTING.md`: dated issue records with symptoms, causes, fixes, verification, and prevention notes.
- `docs/DEVELOPMENT_LOG.md`: chronological development log with changed files, verification, and next steps.

## Manual Real Smoke

Use this only for explicit manual real-mode checks:

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="..."
$env:OPENAI_MODEL="gpt-5"
uv run --project . --with openai python main.py smoke-real --topic "요즘 사람들이 AI 쇼츠 자동화에 관심 가지는 이유"
```

Do not print, commit, or hard-code API keys.

## Important Rules

- Do not commit `.env`.
- Do not put API keys in code.
- Use `uv` for Python commands.
- Use Python 3.12 and respect `.python-version`.
- Keep fake mode as the default MVP behavior.
- Use `FakeLLMClient` in automated tests.
- Never write tests that call the real OpenAI API.
- Keep scene updates keyed by `scene_id`.
- Each real agent must update only its responsibility fields.
- Preserve core fields such as `scene_id`, `scene_purpose`, `narration`, and `estimated_duration` unless the agent explicitly owns them.

## Real Agent Field Ownership

- `RealScriptWriterAgent`: `title`, `narration`, `target_duration_seconds`, `style_notes`.
- `RealStoryboardAgent`: creates initial `Scene` objects and stable `scene_id` values.
- `RealSubtitleAgent`: updates only `subtitle` and `emphasis_caption`.
- `RealVisualAssetSuggestionAgent`: updates only `visual_asset_type`, `visual_description`, `generated_image_prompt`, `gif_or_clip_suggestion`, `stock_search_keywords`, `visual_source_strategy`, `capture_source_type`, `capture_usage_mode`, and `asset_usage_note`.
- `RealEditingDirectionAgent`: updates only `motion_direction`, `transition`, `sound_effect_hint`, and `editing_notes`.
- `RealSafetyReviewAgent`: does not modify scenes. It writes only safety fields on `GenerationResult`: `safety_status`, `safety_notes`, `copyright_risks`, `rumor_or_defamation_risks`, `privacy_or_portrait_risks`, `source_usage_risks`, `required_human_review`, and `recommended_revisions`.
- Safety review is not a legal judgment. It structures safety, rights, rumor, defamation, privacy, portrait-rights, and source-usage risk flags so a human can make the final review decision.

## Existing Safety Nets

Important tests:

- `tests/test_real_mixed_pipeline_contract.py`
- `tests/test_real_script_writer_agent.py`
- `tests/test_real_storyboard_agent.py`
- `tests/test_real_subtitle_agent.py`
- `tests/test_real_visual_asset_agent.py`
- `tests/test_real_editing_direction_agent.py`
- `tests/test_real_safety_review_agent.py`
- `tests/test_llm_composition.py`
- `tests/conftest.py`

`tests/conftest.py` removes `ISSUE_TURI_LLM_PROVIDER`, `OPENAI_API_KEY`, and `OPENAI_MODEL` for each test so local real-mode environment variables do not leak into fake-mode tests.

## Recommended Next Step

Recommended next step: refine upload/publishing readiness before DB persistence.

Reason:
- The project already produces rich scene-level planning data.
- Timeline now includes scene timing, production beats, and asset review checklist data.
- Publishing readiness can turn the plan into a practical pre-upload safety/originality checklist.
- DB persistence is useful, but storing data before the timeline contract is stable may create migration churn.

Concrete next slice:
- Add publishing readiness fields such as originality risk, reused-content risk, monetization risk, and required human checks.
- Keep it as planning data only; do not add image generation, TTS, or MP4 rendering yet.
- Keep it as planning data only; do not add image generation, TTS, or MP4 rendering yet.

Alternative next step: DB persistence with SQLite if the immediate need is to preserve generated projects and edited scenes between browser sessions.

## Visual Sourcing Strategy

`RealVisualAssetSuggestionAgent` has been expanded from a simple AI image prompt agent into a per-scene visual sourcing strategy recommender. `RealSafetyReviewAgent` reviews those sourcing fields and flags risks for human review.

Required fields:

```json
{
  "visual_source_strategy": "mockup",
  "capture_source_type": "community",
  "capture_usage_mode": "mockup_recommended",
  "asset_usage_note": "Use a self-made community-style mockup instead of copying real screenshots."
}
```

Allowed `visual_source_strategy` values:
- `reference_capture`
- `mockup`
- `stock_asset`
- `ai_generated`
- `original_sticker`
- `text_card`
- `user_provided`
- `avoid`

Allowed `capture_source_type` values:
- `community`
- `news`
- `youtube`
- `broadcast`
- `instagram`
- `google_image`
- `stock_site`
- `user_provided`
- `ai_generated`
- `none`

Allowed `capture_usage_mode` values:
- `direct_capture_candidate`
- `mockup_recommended`
- `license_required`
- `permission_required`
- `avoid`

Guidelines:
- Do not treat captures as categorically forbidden.
- Classify whether each scene is a direct capture candidate, should become a mockup, needs license/permission review, or should be avoided.
- Google image material should usually be `license_required`.
- YouTube, broadcast, and news captures should usually be `permission_required` or `mockup_recommended`.
- Community and Instagram captures must mention privacy, usernames, profile images, original comment text, and defamation risk in `asset_usage_note`.
- User-owned or user-provided material may be classified as `user_provided`.
- `asset_usage_note` must be non-empty.
- Keep fake mode as default.
- Use `FakeLLMClient` in tests.
- Do not call the real OpenAI API in tests.
- Return clear validation errors for missing fields, invalid enum values, and unsafe response shapes.

## Suggested First Prompt In A New Account

```text
This repo is issue-turi-ai.
First read AGENTS.md, README.md, docs/HANDOFF.md, and .agents/skills/issue-turi-shorts-generation/SKILL.md.
Do not add features yet.
Summarize the current architecture, real/fake pipeline state, test command, and the next safe step.
```
