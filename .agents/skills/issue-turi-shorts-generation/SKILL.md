---
name: issue-turi-shorts-generation
description: Use when working on Issue Turi YouTube Shorts scripts, storyboards, subtitles, visual asset suggestions, editing directions, safety checks, real agent prompts, or shorts generation pipeline verification.
---

# Issue Turi Shorts Generation

Use this skill to keep the Issue Turi Shorts workflow consistent when generating or modifying scripts, scenes, subtitles, visual asset suggestions, editing directions, safety review notes, real agent prompts, or pipeline tests.

## Current Pipeline

The current real mixed pipeline order is fixed:

1. `RealScriptWriterAgent`
2. `RealStoryboardAgent`
3. `RealSubtitleAgent`
4. `RealVisualAssetSuggestionAgent`
5. `RealEditingDirectionAgent`
6. `RealSafetyReviewAgent`

Default mode remains fake. Real agents are used only when `ISSUE_TURI_LLM_PROVIDER` is `openai` or `real`.

## Agent Responsibilities

- `ScriptWriter`: create the title, hook, and overall script direction.
- `Storyboard`: create scene structure keyed by stable `scene_id`.
- `Subtitle`: update only `subtitle` and `emphasis_caption`.
- `VisualAssetSuggestion`: update only `visual_asset_type`, `visual_description`, `generated_image_prompt`, `gif_or_clip_suggestion`, `stock_search_keywords`, `visual_source_strategy`, `capture_source_type`, `capture_usage_mode`, and `asset_usage_note`.
- `EditingDirection`: update only `motion_direction`, `transition`, `sound_effect_hint`, and `editing_notes`.
- `Safety`: review risky wording, copyright risk, rumor risk, defamation risk, privacy/portrait risk, and source usage risk. It is not a legal judge; it flags risks and required human review.

## Invariants

- Do not recreate an existing `Scene` wholesale after storyboard creation.
- Update scenes by `scene_id`.
- Each agent may modify only its responsibility fields.
- Do not overwrite results from earlier agents.
- Validate enum values through the domain enums.
- Preserve core fields such as `estimated_duration`, `narration`, and `scene_purpose`.
- Safety review must not modify `Scene` objects; it may only update safety fields on `GenerationResult`.
- Use `FakeLLMClient` in tests.
- Never create tests that call the real OpenAI API.
- Keep fake mode working as the default MVP behavior.

## Reference Channel Rules

Reference channels:
- 뇌전구: https://www.youtube.com/@%EB%87%8C%EC%A0%84%EA%B5%AC
- 걍석주: https://www.youtube.com/@%EA%B1%8D%EC%84%9D%EC%A3%BC

Operating channel:
- 이슈털이: https://www.youtube.com/@issueyo

Use reference channels only for general production grammar:
- hook style
- subtitle rhythm
- cut pacing
- motion style
- sound cue timing

Do not copy exact scripts, captions, thumbnails, branding, unique expressions, downloaded clips, broadcast footage, or channel-specific presentation.

## Visual Asset Rules

Do not assume every scene needs an AI-generated image. Suggest the best safe visual form per scene:
- reference capture candidates
- community-capture-style mockups
- licensed stock images or clips
- reaction stickers
- text cards
- AI image prompts

Capture is not categorically banned, but the agent must classify the sourcing plan for each scene:
- `visual_source_strategy`: `reference_capture`, `mockup`, `stock_asset`, `ai_generated`, `original_sticker`, `text_card`, `user_provided`, or `avoid`
- `capture_source_type`: `community`, `news`, `youtube`, `broadcast`, `instagram`, `google_image`, `stock_site`, `user_provided`, `ai_generated`, or `none`
- `capture_usage_mode`: `direct_capture_candidate`, `mockup_recommended`, `license_required`, `permission_required`, or `avoid`
- `asset_usage_note`: non-empty note covering copyright, source attribution, portrait rights, privacy, defamation, license, permission, mockup replacement, or avoid reasons

Google image material should usually be `license_required`. YouTube, broadcast, and news captures should usually be `permission_required` or `mockup_recommended`. Community and Instagram captures must call out privacy, usernames, profile images, original comment text, and defamation risk. User-owned or user-provided assets may be classified as `user_provided`.

Do not generate, search, download, or capture real image files in this workflow. The visual agent recommends a sourcing strategy only; final safety and rights review still belongs to safety/review steps.

## Testing

Use:

```powershell
uv run --project . --with pytest pytest -q
```

For real mixed pipeline contract coverage, maintain tests around scene ID consistency, field preservation, fake provider isolation, and no-network LLM behavior.

## Prohibited

- Do not put OpenAI API keys in code.
- Do not commit `.env`.
- Do not write tests that call the real OpenAI API.
- Do not mix UI redesign, image generation, TTS, or MP4 rendering into this workflow.
- Do not change `AGENTS.md` as part of skill-only updates unless explicitly requested.
