---
name: shortsflow-production-grammar
description: Use when defining ShortsFlow production grammar, source-first planning, visual source priority, capture/rewrite rules, thumbnail planning, publishing readiness, or source review workflows.
---

# ShortsFlow Production Grammar

Before planning or changing production workflow features, read:

- `docs/SOURCE_FIRST_WORKFLOW.md`
- `docs/UI_DESIGN_GUIDE.md`
- `docs/FRONTEND_BACKEND_CONTRACT.md`
- `docs/HANDOFF.md`
- `docs/TECH_STACK.md`

For frontend UI work, also use `.agents/skills/shortsflow-ui-designer/SKILL.md`.

## Product Direction

ShortsFlow is source-capture-first, not AI-image-first.

Topic-only input remains supported, but the preferred workflow is:

```text
source_url
source_type
source_title
source_context
source_angle
-> source capture plan
-> storyboard/timeline
-> asset candidates
-> review checklist
-> export
```

`source_context` is user-provided text. Do not automatically fetch, crawl, scrape, download, search, screenshot, or capture external URLs.

## Visual Source Priority

1. `source_capture`
2. `mockup_rewrite`
3. `licensed_stock` or `user_provided`
4. `google_image_reference` as a license-review candidate
5. `ai_generated` as a support/background/replacement cut

AI images are not the default visual strategy.

## Reference Channel Rules

Reference channels:

- 강석주
- 뇌전구
- 얘봐라

Operating/upload channel:

- 이슈털이

Use these channels only for general fast issue-explainer production grammar:

- first-second hook pressure
- fast TTS-based issue progression
- source-screen and explanation-caption pairing
- short scene-level cuts
- large subtitle/emphasis rhythm
- reaction -> issue -> context shift -> conclusion -> comment prompt structure
- clear issue-forward thumbnail communication

Do not copy reference-channel script sentences, thumbnail designs, TTS voice or speech style, edit tempo/cut structure, logos, captures, images, original comments, or channel-specific presentation. Rebuild the format as original 이슈털이 production grammar.

## Guardrails

- Do not copy reference-channel dialogue, thumbnails, branding, TTS voice/speech style, edit tempo/cut structure, or unique presentation.
- Do not treat Google images as usable without license review.
- Do not approve captures without rights, privacy, portrait-right, and defamation review.
- Do not add external API calls, crawling, downloading, DB persistence, image generation, TTS, or MP4 rendering unless the user explicitly scopes that work.
- Source-first UI changes must check backend/frontend contract and JSON export shape together.
