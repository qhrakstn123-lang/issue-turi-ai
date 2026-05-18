# Issue Turi AI 현재 구현 상태

이 문서는 현재 저장소를 처음 보는 사람이 지금 무엇이 동작하고, 무엇이 아직 범위 밖인지 빠르게 파악하기 위한 요약입니다.

## 핵심 요약

현재 프로젝트는 완성형 영상 생성기가 아니라 **ShortsFlow 쇼츠 제작 보조 MVP**입니다.

제품 방향은 AI 이미지 중심 자동 생성이 아니라 **source-capture-first workflow**입니다. 커뮤니티, 뉴스, 유튜브, 방송, 인스타그램, 구글 이미지 reference, stock, user-provided 자료를 먼저 고려하고, AI 이미지는 원본 자료가 부족하거나 대체 컷/배경 컷이 필요할 때 쓰는 보조 수단입니다.

다음 기능 작업 전에는 다음 문서를 먼저 확인합니다.

- [docs/SOURCE_FIRST_WORKFLOW.md](SOURCE_FIRST_WORKFLOW.md)
- [docs/UI_DESIGN_GUIDE.md](UI_DESIGN_GUIDE.md)
- [docs/FRONTEND_BACKEND_CONTRACT.md](FRONTEND_BACKEND_CONTRACT.md)

`frontend/web` UI 작업은 `.agents/skills/shortsflow-ui-designer/SKILL.md`를 따릅니다.

## 현재 주 UI

현재 주 UI는 `frontend/web`의 **Next.js + React + TypeScript** ShortsFlow UI입니다.

```text
http://localhost:3000
```

Next.js dev server가 다른 포트를 배정하면 터미널에 표시된 실제 dev port를 사용합니다.

`http://127.0.0.1:8000`은 Python backend API 서버이자 legacy 안내 페이지 host입니다. 일반적인 ShortsFlow 작업 화면은 `localhost:3000` 또는 실제 Next.js dev port입니다.

## Legacy Frontend

`frontend/app`은 삭제하지 않고 legacy 안내/호환 페이지로 유지합니다.

신규 제품 UI 기능은 `frontend/app`에 추가하지 않습니다. 앞으로 UI 작업은 `frontend/web` 기준으로 진행합니다.

## 실행 방법

터미널 1에서 backend를 실행합니다.

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

터미널 2에서 Next.js frontend를 실행합니다.

```powershell
cd frontend/web
npm run dev
```

브라우저:

```text
http://localhost:3000
```

기본 mode는 fake pipeline입니다. API key 없이 동작하며 외부 AI API를 호출하지 않습니다.

## Fake Mode와 Real Mode

기본값은 fake mode입니다.

```text
ISSUE_TURI_LLM_PROVIDER=fake
```

또는 환경변수를 설정하지 않으면 fake mode입니다.

real mode는 다음 값에서만 사용합니다.

```text
ISSUE_TURI_LLM_PROVIDER=openai
```

또는:

```text
ISSUE_TURI_LLM_PROVIDER=real
```

real mode는 OpenAI API key가 필요합니다. 그래도 현재는 planning JSON만 생성하며 이미지, TTS, MP4는 생성하지 않습니다. 자동 테스트는 real API를 호출하면 안 됩니다.

## 현재 Real Pipeline

`ISSUE_TURI_LLM_PROVIDER=openai` 또는 `real`일 때 real pipeline 순서는 고정입니다.

```text
RealScriptWriterAgent
-> RealStoryboardAgent
-> RealSubtitleAgent
-> RealVisualAssetSuggestionAgent
-> RealEditingDirectionAgent
-> RealSafetyReviewAgent
```

## 현재 구현된 계획 데이터

현재 생성 결과는 다음 데이터를 포함합니다.

- 쇼츠 제목과 전체 내레이션 방향
- scene별 storyboard
- scene별 자막과 강조 자막
- scene별 visual suggestion과 generated-image prompt
- scene별 visual sourcing strategy
- scene별 motion, transition, sound cue
- 안전/권리/루머/명예훼손/개인정보/초상권/source usage risk
- `GenerationResult.timeline`
- scene별 rule-based production beats
- scene별 asset review checklist

Timeline은 planning contract입니다. 실제 음성, 이미지, MP4 파일은 만들지 않습니다.

## Source-First Project Form

`frontend/web`의 ProjectForm은 기존 topic-only 생성 흐름을 유지하면서 source-first 입력도 지원합니다.

추가 입력:

- `source_url`
- `source_type`
- `source_title`
- `source_context`
- `source_angle`

`source_context`는 사용자가 직접 요약하거나 붙여넣은 텍스트입니다. URL을 입력해도 ShortsFlow는 외부 사이트를 자동으로 fetch, crawl, download, search, screenshot하지 않습니다.

source-first 입력이 있으면 브라우저 상태와 JSON 다운로드에 `source_brief`가 포함되고, 초기 `asset_source_candidate`가 하나 생성됩니다. 이 후보는 사용 승인 상태가 아니며 source type에 따라 blur, rewrite, license, permission review 기본값이 적용됩니다.

## Manual Asset Register

`frontend/web`에는 scene별 frontend-only Manual Asset Register가 있습니다.

사용자는 `AssetSourceCandidate`를 추가, 수정, 승인, 삭제할 수 있습니다.

이 데이터는 브라우저 state입니다. DB 저장은 아직 없으므로 새로고침하면 사라집니다. JSON 다운로드에는 포함됩니다.

## Manual Scene Edit

`frontend/web`에는 scene card 안에 compact Manual Edit UI가 있습니다.

수정 가능한 필드:

- `narration`
- `tts_text`
- `subtitle`
- `emphasis_caption`
- `estimated_duration`
- `visual_description`
- `generated_image_prompt`
- `asset_usage_note`
- `editing_notes`

수정은 frontend state에만 반영됩니다. backend PATCH API, DB 저장, pipeline 변경은 없습니다.

## Frontend/Backend 표시 기준

새 backend 필드나 frontend-only state를 추가하기 전에는 [docs/FRONTEND_BACKEND_CONTRACT.md](FRONTEND_BACKEND_CONTRACT.md)에서 표시 위치와 JSON export 반영 여부를 먼저 확인합니다.

현재 주요 매핑:

- `video_script`: `ResultSummary` / script overview
- `source_brief`: Source-first Project Form / source summary / JSON export
- `storyboard.scenes`: `SceneCard` / `SceneEditor`
- visual fields: `VisualSection`
- sourcing fields: `SourcingSection` / asset review area
- `timeline`: `TimelinePanel`
- `source_capture_plans`: `TimelinePanel`의 scene 근처 planning card / JSON export
- `asset_source_candidates`: `AssetCandidateRegister` / JSON export
- safety review fields: `SafetyReviewPanel`

## Source Capture Plan

`frontend/web`은 `source_brief`와 현재 scene 정보를 바탕으로 scene별 Source Capture Plan을 rule-based로 생성합니다.

필드:

- `scene_id`
- `primary_asset_plan`
- `capture_target`
- `fallback_asset_plan`
- `backup_asset_plan`
- `ai_image_needed`
- `source_review_note`

이 기능은 실제 캡처가 아니라 캡처/대체/검토 계획입니다. 외부 URL을 자동으로 읽거나, 캡처하거나, 이미지를 생성하지 않습니다.

## JSON Export

현재 JSON 다운로드 구조는 다음과 같습니다.

```json
{
  "generation_result": {},
  "source_brief": {},
  "source_capture_plans": [],
  "asset_source_candidates": []
}
```

`source_brief`는 source-first 입력이 있을 때만 포함됩니다. `asset_source_candidates`는 후보가 없으면 빈 배열일 수 있습니다.

## 참고 채널 기준

참고 채널:

- 강석주
- 뇌전구
- 얘봐라

업로드 채널:

- 이슈털이

참고 가능한 것은 빠른 이슈 해설형 쇼츠의 일반 제작 문법입니다. 특정 채널의 대본 문장, 썸네일 디자인, TTS 목소리/말투, 편집 템포/컷 구성, 로고, 캡처, 이미지, 댓글 원문은 복제하지 않습니다.

## 아직 미구현

- 자동 크롤링
- 자동 캡처
- Google 이미지 자동 검색/다운로드
- 이미지 생성
- TTS
- 썸네일 생성
- MP4 렌더링
- DB 저장
- 로그인
- 결제
- 배포
- 업로드 자동화

## 다음 작업 후보

1. Source Capture Plan
   - scene별 primary capture, mockup/rewrite, fallback/backup asset plan을 구조화합니다.

2. Manual Screenshot / Capture Asset Upload
   - 사용자가 직접 준비한 캡처/자료를 수동 등록합니다.

3. Publishing Readiness
   - originality, reused-content, monetization, source-rights, required human checks를 planning data로 추가합니다.

DB persistence, 이미지 생성, TTS, MP4 렌더링은 그 이후 단계입니다.
