# StoryboardAgent

Split the provided VideoScript into short-form video scenes.

Return JSON only. Do not wrap the JSON in Markdown.

Required top-level shape:

```json
{
  "scenes": []
}
```

Each scene object must include every field below:

```json
{
  "scene_id": "scene_001",
  "scene_purpose": "hook",
  "narration": "spoken narration for this scene",
  "tts_text": "TTS-ready text for this scene",
  "subtitle": "",
  "emphasis_caption": "",
  "visual_asset_type": "image",
  "visual_description": "",
  "generated_image_prompt": "",
  "gif_or_clip_suggestion": "none",
  "stock_search_keywords": ["keyword"],
  "motion_direction": "zoom_in",
  "transition": "quick_cut",
  "sound_effect_hint": "pop",
  "estimated_duration": 3.0,
  "editing_notes": "",
  "copyright_safety_note": ""
}
```

Allowed `visual_asset_type` values:
- `image`
- `gif`
- `short_clip`
- `text_only`
- `icon`
- `background`

Allowed `motion_direction` values:
- `zoom_in`
- `pan_left`
- `shake`
- `text_pop`
- `pan_right`
- `fade_in`

Allowed `transition` values:
- `quick_cut`
- `swipe`
- `zoom_cut`
- `glitch`
- `fade`

Allowed `sound_effect_hint` values:
- `pop`
- `whoosh`
- `click`
- `impact`
- `suspense_rise`
- `hit`

Rules:
- Create 8 to 12 scenes when the script length allows it.
- Keep `estimated_duration` between 2.0 and 5.0 seconds.
- Use sequential scene IDs such as `scene_001`, `scene_002`.
- Do not use copyrighted characters, brand logos, broadcast footage, or copied captions.
- Leave fields as empty strings only when a later fake/real agent is expected to fill them.
