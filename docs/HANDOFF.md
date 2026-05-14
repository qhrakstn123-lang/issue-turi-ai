# Issue Turi AI Handoff

## Current Status

Default mode is the fake MVP pipeline.

`ISSUE_TURI_LLM_PROVIDER=openai` or `real` uses the current real mixed pipeline:

1. `RealScriptWriterAgent`
2. `RealStoryboardAgent`
3. `RealSubtitleAgent`
4. `RealVisualAssetSuggestionAgent`
5. `RealEditingDirectionAgent`
6. `FakeSafetyReviewAgent`

Not implemented yet:
- `RealSafetyReviewAgent`
- image generation
- TTS
- MP4 rendering
- database persistence
- upload/deployment/payment flows

## Must Read First

Read these before making changes:

- `AGENTS.md`
- `.agents/skills/issue-turi-shorts-generation/SKILL.md`
- `README.md`
- `docs/HANDOFF.md`

## Test Command

```powershell
uv run --project . --with pytest pytest -q
```

Automated tests must not call real OpenAI or any external API.

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
- `FakeSafetyReviewAgent`: currently provides safety status and notes.

## Existing Safety Nets

Important tests:

- `tests/test_real_mixed_pipeline_contract.py`
- `tests/test_real_script_writer_agent.py`
- `tests/test_real_storyboard_agent.py`
- `tests/test_real_subtitle_agent.py`
- `tests/test_real_visual_asset_agent.py`
- `tests/test_real_editing_direction_agent.py`
- `tests/test_llm_composition.py`
- `tests/conftest.py`

`tests/conftest.py` removes `ISSUE_TURI_LLM_PROVIDER`, `OPENAI_API_KEY`, and `OPENAI_MODEL` for each test so local real-mode environment variables do not leak into fake-mode tests.

## Visual Sourcing Strategy

Before adding `RealSafetyReviewAgent`, `RealVisualAssetSuggestionAgent` has been expanded from a simple AI image prompt agent into a per-scene visual sourcing strategy recommender.

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
