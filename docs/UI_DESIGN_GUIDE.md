# ShortsFlow UI Design Guide

## Identity

- Brand: ShortsFlow
- Subtitle: AI Shorts Planning Studio
- Upload channel: 이슈털이
- Reference channels: 강석주, 뇌전구, 얘봐라

Reference channels are only references for general fast issue-explainer Shorts production grammar. Do not copy their script sentences, thumbnail design, TTS voice or speech style, editing structure, logos, captures, images, or original comments.

## Product Direction

ShortsFlow is a source-capture-first production studio. The UI should help creators plan shorts from source material, review asset candidates, and prepare an edit timeline.

AI images are not the default visual strategy. They are support/background/replacement cuts when original source material is insufficient, risky, or unavailable.

## Visual Style

Keep the current dark-mode SaaS production studio style:

- calm, work-focused, and information-dense
- compact panels over marketing-style sections
- clear hierarchy for planning, review, timeline, and export
- no decorative UI that competes with production data
- visible distinction between generated data, frontend-only edits, and future placeholders

Use `frontend/web` as the primary UI surface. `frontend/app` is a legacy 안내/호환 page and is not a target for new product UI work.

## Core UI Areas

### Source-first Project Form

The form should support both topic-only and source-first creation.

Design principles:

- Keep source fields optional.
- Make it clear that URLs are not fetched, crawled, downloaded, searched, or screenshotted.
- Treat `source_context` as user-provided text.
- When source-first fields exist, show a compact "소스 기반 기획" signal.
- Do not over-explain frontend-only behavior in the main flow; preserve a natural JSON export workflow.

### SceneCard

Scene cards should show the current scene plan at a glance:

- narration and TTS text
- subtitle and emphasis caption
- estimated duration
- visual summary
- sourcing and editing cues
- edited state when frontend-only manual edits exist

Scene-level additions should stay compact. Prefer progressive disclosure for long prompts, capture plans, checklists, and manual editing.

### TimelinePanel

TimelinePanel should show sequence, duration, source/capture direction, production beats, and asset review checklist.

Design principles:

- Preserve scannable timing information.
- Keep `beats` and `asset_review_checklist` visually grouped with the relevant scene.
- For source-first work, show source capture direction near scene timing or scene review context.
- Do not make timeline controls imply real rendering until MP4 rendering exists.

### SafetyReviewPanel

SafetyReviewPanel should make human review requirements easy to spot:

- `safety_status`
- `required_human_review`
- safety notes
- copyright, rumor/defamation, privacy/portrait, and source-usage risks
- recommended revisions

Use caution states for risk, but do not present safety output as legal approval.

### AssetCandidateRegister

AssetCandidateRegister is for frontend-only manual source review.

Design principles:

- Show source type, source URL/title, usage mode, license status, blur/rewrite needs, approval state, and review notes.
- Risky sources such as community, instagram, news, youtube, broadcast, and google_image should be visually noticeable.
- `approved_for_use` should remain conservative by default.
- `avoid` should clearly indicate that use is blocked or replacement is needed.

## Real Features vs Placeholder Features

Actual current features:

- fake and optional real LLM planning pipeline
- storyboard, subtitles, visual sourcing, editing cues, safety review
- timeline, production beats, asset review checklist
- Source-first Project Form
- Manual Scene Edit
- Manual Asset Register
- JSON export

Placeholder or future features:

- automatic crawling
- automatic screenshot/capture
- Google image automatic search/download
- image generation
- TTS generation
- thumbnail generation
- MP4 rendering
- DB persistence
- login
- payment
- deployment

Never design a control that appears to perform an unimplemented media operation unless it is clearly presented as planning-only.

## Rights And Safety Principles

External captures, Google images, community material, news screenshots, YouTube frames, broadcast footage, and Instagram material require rights, privacy, portrait-right, and defamation review.

Community and Instagram sources should prioritize blur, mockup, and rewrite. Google image material is a license-review reference until original source and license are confirmed. News, YouTube, and broadcast captures usually need permission or mockup replacement.

## UI Work Checklist

Before frontend UI work:

1. Read `docs/UI_DESIGN_GUIDE.md`.
2. Read `docs/FRONTEND_BACKEND_CONTRACT.md`.
3. Use `.agents/skills/shortsflow-ui-designer/SKILL.md`.
4. Confirm whether the change is real behavior, frontend-only state, or placeholder planning UI.
5. Confirm JSON export impact when source-first or frontend-only fields are involved.
