# ShortsFlow Frontend/Backend Contract

This document maps backend/API result fields and frontend-only state to their display and export locations in `frontend/web`.

It is a UI/data contract guide, not a backend API migration plan. Do not change backend domain/application/pipeline behavior just to satisfy this document unless a feature task explicitly scopes that work.

## Primary Surfaces

- Primary UI: `frontend/web`
- Legacy UI: `frontend/app`
- Backend/API: `http://127.0.0.1:8000`
- Primary browser URL: `http://localhost:3000` or the actual Next.js dev port

`frontend/app` is a legacy 안내/호환 page. New product UI work belongs in `frontend/web`.

## Field Mapping

### `generation_result.video_script`

Fields:

- `title`
- `narration`
- `target_duration_seconds`
- `style_notes`

Frontend display:

- `ResultSummary`
- Script overview area

### `source_brief`

Fields:

- `source_url`
- `source_type`
- `source_title`
- `source_context`
- `source_angle`

Frontend display:

- Source-first Project Form
- Source summary card or source-first hint
- Source capture direction near TimelinePanel or SceneCard when relevant

Export:

- Include in JSON export when source-first input exists.

### `generation_result.storyboard.scenes`

Fields:

- `narration`
- `tts_text`
- `subtitle`
- `emphasis_caption`
- `estimated_duration`

Frontend display and edit:

- `SceneCard`
- `SceneEditor`

Manual edits are frontend-only until DB persistence is implemented.

### Visual Fields

Fields:

- `visual_asset_type`
- `visual_description`
- `generated_image_prompt`
- `gif_or_clip_suggestion`
- `stock_search_keywords`

Frontend display:

- `VisualSection`

These fields describe visual planning. They do not imply real image generation.

### Sourcing Fields

Fields:

- `visual_source_strategy`
- `capture_source_type`
- `capture_usage_mode`
- `asset_usage_note`

Frontend display:

- `SourcingSection`
- Asset review area
- Timeline or SceneCard context when source capture planning is added

These fields should clarify whether material is a direct capture candidate, mockup/rewrite candidate, license-required, permission-required, user-provided, AI support, or avoid.

### `generation_result.timeline`

Fields:

- `total_duration`
- `scenes[].start_time`
- `scenes[].end_time`
- `scenes[].duration`
- `scenes[].beats`
- `scenes[].asset_review_checklist`

Frontend display:

- `TimelinePanel`

Defensive rendering rule:

- Treat `beats` as `scene.beats ?? []`.
- Treat `asset_review_checklist` as `scene.asset_review_checklist ?? []`.
- JSON export should keep both fields as arrays.

### `asset_source_candidates`

Fields:

- `scene_id`
- `source_type`
- `source_url`
- `source_title`
- `usage_mode`
- `license_status`
- `needs_blur`
- `needs_rewrite`
- `approved_for_use`
- `review_notes`

Frontend display and edit:

- `AssetCandidateRegister`

Export:

- Include in JSON export as `asset_source_candidates`.

State:

- Frontend-only until DB persistence is implemented.
- Can disappear on refresh before persistence exists.

### Safety Review

Fields:

- `safety_status`
- `required_human_review`
- `safety_notes`
- `copyright_risks`
- `rumor_or_defamation_risks`
- `privacy_or_portrait_risks`
- `source_usage_risks`
- `recommended_revisions`

Frontend display:

- `SafetyReviewPanel`

Safety review is a structured human-review aid, not legal approval.

## Planned Fields

### `source_capture_plans`

Fields:

- `scene_id`
- `primary_asset_plan`
- `capture_target`
- `fallback_asset_plan`
- `backup_asset_plan`
- `ai_image_needed`
- `source_review_note`

Planned frontend display:

- Source Capture Plan panel
- TimelinePanel near scene timing
- SceneCard near sourcing context

Current implementation:

- `source_capture_plans` is frontend-only rule-based planning state.
- It is generated from `source_brief` and `generation_result.storyboard.scenes`.
- It is displayed compactly near each TimelinePanel scene.
- It is exported in JSON.
- It does not imply automatic crawling, downloading, capture, image generation, TTS, or MP4 rendering.

## JSON Export Standard

Current export shape:

```json
{
  "generation_result": {},
  "source_brief": {},
  "source_capture_plans": [],
  "asset_source_candidates": []
}
```

Rules:

- `generation_result` is always included when a result exists.
- `source_brief` is included when source-first input exists.
- `source_capture_plans` is always included as an array.
- `asset_source_candidates` is always included as an array.
- Do not include API keys, environment variables, secrets, or local credentials.
- Keep frontend-only manual edits reflected in exported `generation_result`.
- Keep frontend-only `asset_source_candidates` reflected in export.

## Frontend-only State

The following are frontend-only before persistence:

- manual scene edits
- `asset_source_candidates`
- `source_brief`
- `source_capture_plans`

Until DB persistence exists, these may disappear on refresh. JSON export is the current preservation path.

## Change Checklist

When backend fields are added or frontend-only state changes:

1. Decide the display location in `frontend/web`.
2. Decide whether the field is editable, read-only, or review-only.
3. Decide whether JSON export must include it.
4. Add defensive rendering for optional or old-result shapes.
5. Avoid changing API structure unless the feature explicitly requires it.
6. Keep `frontend/app` unchanged.
