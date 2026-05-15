# ShortsFlow Updated Product Plan & UI Reference Roadmap

> This document reflects the current `issue-turi-ai` implementation state. It replaces older planning notes that described Timeline Builder or Next.js migration as future work.

## 1. Product Positioning

ShortsFlow is an AI Shorts Planning Studio.

It helps a creator turn one topic into:

- script direction
- storyboard scenes
- subtitles and emphasis captions
- visual sourcing strategy
- editing directions
- sound cue hints
- safety and rights review
- timeline planning data
- production beats
- asset review checklist
- JSON export

It is not yet a media renderer. It does not generate final image files, TTS audio, or MP4 videos.

## 2. Brand Direction

Use the service brand:

```text
ShortsFlow
AI Shorts Planning Studio
```

Keep channel-specific language such as "이슈털이" as a style/template or operating-channel context, not as the product brand.

Suggested UI copy:

```text
ShortsFlow
AI Shorts Planning Studio

Plan better. Create faster. Grow bigger.
```

Korean copy examples:

```text
주제 하나로 쇼츠 기획서를 완성하세요.
아이디어를 장면, 자막, 안전 검토까지 한 번에 정리하세요.
오늘의 이슈를 짧고 강렬한 쇼츠로 정리하세요.
```

## 3. Current Implementation Status

Completed:

| Area | Status |
| --- | --- |
| topic/target/tone/style/length input | done |
| fake MVP pipeline | done |
| OpenAI/real provider mode | done |
| `RealScriptWriterAgent` | done |
| `RealStoryboardAgent` | done |
| `RealSubtitleAgent` | done |
| `RealVisualAssetSuggestionAgent` | done |
| `RealEditingDirectionAgent` | done |
| `RealSafetyReviewAgent` | done |
| visual sourcing strategy | done |
| safety review fields | done |
| `GenerationResult.timeline` | done |
| scene production beats | done |
| scene asset review checklist | done |
| Next.js + React + TypeScript UI in `frontend/web` | done |
| legacy static UI retained in `frontend/app` | done |
| same-origin Next.js `/api/...` proxy | done |
| frontend-only Manual Asset Register | done |
| JSON export with `generation_result` and `asset_source_candidates` | done |

Not implemented:

| Area | Status |
| --- | --- |
| DB persistence | not implemented |
| project list/reopen from DB | not implemented |
| real image generation | not implemented |
| TTS generation | not implemented |
| asset storage | not implemented |
| MP4 rendering | not implemented |
| login/payment/deployment | not implemented |
| upload automation | not implemented |

## 4. Frontend State

Primary UI:

```text
frontend/web
Next.js + React + TypeScript
http://localhost:3000
```

If Next.js selects another dev port, use the actual port printed by `npm run dev`.

Backend and legacy page:

```text
http://127.0.0.1:8000
```

`frontend/app` is a legacy 안내/호환 page. It should remain available but should not receive new product UI features.

## 5. API and Provider State

Default mode:

```text
fake
```

Real LLM mode is enabled only by:

```text
ISSUE_TURI_LLM_PROVIDER=openai
```

or:

```text
ISSUE_TURI_LLM_PROVIDER=real
```

Real pipeline:

```text
RealScriptWriterAgent
-> RealStoryboardAgent
-> RealSubtitleAgent
-> RealVisualAssetSuggestionAgent
-> RealEditingDirectionAgent
-> RealSafetyReviewAgent
```

The real pipeline still returns planning JSON only.

## 6. UI Reference Usage

Reference image path:

```text
docs/assets/ui-reference/shortsflow-dark-dashboard-and-editor-reference.png
```

Use this image as a design direction reference only.

Allowed reference use:

- layout rhythm
- dark-mode tone
- dashboard/editor composition
- sidebar/topbar/workspace structure
- dense production-studio feel

Do not copy:

- temporary text
- fake names or numbers
- example thumbnails
- any reference-specific brand details

## 7. Updated Roadmap

### Phase 1: Manual Edit / Scene 수정 UI

Recommended next step.

Reason:

- The app already generates rich planning data.
- Users need to correct generated text, subtitles, sourcing notes, and editing notes before persistence.
- Editing workflow should stabilize before DB migrations or renderer contracts.

Scope:

- `frontend/web`
- safe editable scene fields
- local state and JSON export first
- no `frontend/app` feature work
- no image/TTS/MP4 generation

### Phase 2: Publishing Readiness

Add pre-upload review data:

- originality risk
- reused-content risk
- monetization risk
- source-rights risk
- human-review checklist
- upload-blocking notes

### Phase 3: DB Persistence / Project Management

Add persistence after editable planning data is stable:

- SQLite or another repository
- project list
- project detail reopen
- edited scene save
- saved JSON export

### Phase 4: Media Production Providers

Add after planning/edit/review contracts are stable:

- image provider
- TTS provider
- asset storage
- render job manager
- MP4 renderer

## 8. Guardrails

- Keep fake mode as default.
- Automated tests must not call real OpenAI or any external API.
- Do not add media generation in documentation-only or UI-editing slices.
- Do not add new product UI features to `frontend/app`.
- Keep `frontend/web` as the UI target for future ShortsFlow work.
