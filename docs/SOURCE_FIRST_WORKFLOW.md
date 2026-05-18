# ShortsFlow Source-First Workflow

## 1. Product Direction

ShortsFlow is not an AI Shorts auto-generator.

ShortsFlow is a production assistant for planning shorts from original sources such as community posts, news, YouTube, broadcast material, Instagram, Google image references, stock sites, user-provided material, and AI-generated support visuals.

The product direction is **source-capture-first shorts production**:

```text
source input
-> source context and angle
-> script/storyboard
-> source capture plan
-> asset candidates
-> edit timeline
-> review checklist
-> export package
```

AI images are not the default visual strategy. They are a support option for background shots, replacement cuts, explanatory visuals, or scenes where the original source is insufficient, risky, or unavailable.

## Reference And Operating Channels

Reference channels:

- 강석주
- 뇌전구
- 얘봐라

Operating/upload channel:

- 이슈털이

These reference channels are only general production-grammar references for fast issue-explainer Shorts. They may inform hook rhythm, source-screen pacing, large subtitle cadence, short scene transitions, issue framing, and comment-call structure.

Do not copy reference-channel script sentences, thumbnail design, TTS voice or speech style, edit tempo/cut structure, logos, captures, images, or original comments. ShortsFlow should reconstruct an original 이슈털이 format from source material and safe review rules.

## 2. Source-First Input

Topic-only input remains supported because it is useful for quick ideation and fake-mode tests.

The preferred product direction is source-first input:

- `topic`
- `source_url`
- `source_type`
- `source_title`
- `source_context`
- `source_angle`

`source_context` is text provided by the user. It can be a summary, copied excerpt, or manually written context. ShortsFlow should not automatically fetch, crawl, scrape, download, or capture external URLs.

`source_angle` describes why the source matters for the video, such as "reaction split", "policy controversy", "unexpected context", "creator response", or "public safety concern".

## 3. Visual Source Priority

Visual planning should use this priority order:

1. `source_capture`
2. `mockup_rewrite`
3. `licensed_stock` or `user_provided`
4. `google_image_reference` as a license-review candidate
5. `ai_generated` as a support/background/replacement cut

The system should never treat a URL, screenshot, or Google image as automatically usable. It should produce planning and review data so a human can decide what is safe to use.

## 4. Source Type Rules

### community / instagram

Check nicknames, profile images, original comments, personal information, privacy risk, and defamation risk.

Prefer blur, mockup, and rewrite over direct original capture. Direct capture should remain a candidate only until rights, privacy, and defamation risks are reviewed.

### news / youtube / broadcast

Check logos, screenshot rights, source attribution, `permission_required`, and whether a direct capture is necessary.

Prefer self-made summary cards, recreated diagrams, or mockups when possible.

### google_image

Google image material is only a reference or license-review candidate until the original source and license are confirmed.

Do not automatically capture or download Google image results.

### stock_site

Check stock license, model release, location/property release, and permitted platform and usage scope.

### user_provided

Confirm that the user owns the material or has permission to use it.

### ai_generated

Check real-person confusion, brand or character similarity, false factual implication, and whether the image could be mistaken for documentary evidence.

AI-generated images should support the story, not replace source verification.

## 5. Scene Planning Concepts

Future scene planning can include:

- `primary_asset_plan`
- `capture_target`
- `fallback_asset_plan`
- `backup_asset_plan`
- `ai_image_needed`
- `source_review_note`

These concepts should guide planning before media generation or rendering. They do not imply automatic capture, crawling, download, image generation, TTS, or MP4 rendering.

## 6. Current Implementation Connection

Already implemented:

- shorts script generation
- storyboard scenes
- visual sourcing
- safety review
- timeline
- production beats
- asset review checklist
- Manual Asset Register
- Manual Scene Edit
- Source-first Project Form in `frontend/web`
- frontend-only `source_brief` export
- source-first initial asset candidate creation
- JSON export

Not implemented:

- automatic crawling
- automatic capture
- automatic Google image search/download
- image generation
- TTS
- thumbnail generation
- MP4 rendering
- DB persistence

## 7. Next Feature Order

Recommended next feature order:

1. Source Capture Plan
2. Manual Screenshot / Capture Asset Upload
3. Thumbnail Planner
4. TTS Script / Voice Direction
5. Publishing Readiness
6. DB persistence
7. Image/TTS/MP4 renderer

## 8. What Not To Do

- Do not copy reference-channel scripts, thumbnails, branding, or unique editing structure.
- Do not automatically crawl, scrape, capture, or download external sites.
- Do not treat Google images as usable assets without license review.
- Do not approve captured source use without rights, privacy, and defamation review.
- Do not return to an AI-image-first workflow.
- Do not make image generation the default visual strategy.
