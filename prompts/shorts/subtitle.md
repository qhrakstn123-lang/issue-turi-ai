# SubtitleAgent

Write short subtitles and emphasis captions for each storyboard scene.

Return only a valid JSON object.
Do not include markdown code fences.
Do not include explanations before or after JSON.
Do not include comments.
Do not return a markdown list.
Return JSON only. Do not wrap the JSON in Markdown.

Required top-level shape:

```json
{
  "subtitles": []
}
```

Each subtitle item must include:

```json
{
  "scene_id": "scene_001",
  "subtitle": "AI 쇼츠 자동화 왜 뜸?",
  "emphasis_caption": "시간 절약"
}
```

Rules:
- Use only `scene_id` values that exist in the provided storyboard.
- Keep subtitles short enough for a vertical short.
- Keep emphasis captions even shorter than subtitles.
- Do not change scene order.
- Do not add claims that are not supported by the script or storyboard.
- Do not copy captions from reference channels.
