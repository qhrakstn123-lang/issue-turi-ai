# Issue Turi AI 현재 구현 상태

이 문서는 현재 저장소를 처음 보는 사람이 지금 무엇이 동작하고, 무엇이 아직 범위 밖인지 빠르게 파악하기 위한 요약입니다.

## 핵심 요약

현재 프로젝트는 완성형 영상 생성기가 아니라 **ShortsFlow 쇼츠 제작 보조 MVP**입니다.

제품 방향은 AI 이미지 중심 자동 생성이 아니라 **source-capture-first workflow**입니다. 커뮤니티, 뉴스, 유튜브, 방송, 인스타그램, 구글 이미지 reference, stock, user-provided 자료를 먼저 고려하고, AI 이미지는 원본 자료가 부족하거나 대체 컷/배경 컷이 필요할 때 쓰는 보조 수단입니다.

다음 기능 작업 전에는 [docs/SOURCE_FIRST_WORKFLOW.md](SOURCE_FIRST_WORKFLOW.md)를 먼저 확인합니다.

## 현재 주 UI

현재 주 UI는 `frontend/web`의 **Next.js + React + TypeScript** ShortsFlow UI입니다.

```text
http://localhost:3000
```

Next.js dev server가 다른 포트를 배정하면 터미널에 표시된 실제 dev port를 사용합니다.

`http://127.0.0.1:8000`은 Python backend API 서버이자 legacy 안내 페이지 host입니다. 일반적인 ShortsFlow 작업 화면은 `localhost:3000` 또는 실제 Next.js dev port입니다.

## Legacy Frontend

`frontend/app`은 삭제하지 않고 legacy 안내/호환 페이지로 유지합니다.

역할:

- Python backend가 직접 서빙할 수 있는 legacy 안내 화면
- 간단한 정적 fallback
- 기존 테스트 호환성 유지

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

각 agent는 자기 책임 필드만 수정합니다. Safety review는 scene을 직접 수정하지 않고 `GenerationResult`의 safety 필드만 업데이트합니다.

## GenerationResult 내용

현재 생성 결과는 다음 계획 데이터를 포함합니다.

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

`source_context`는 사용자가 직접 요약하거나 붙여넣은 텍스트입니다. URL을 입력해도 ShortsFlow는 외부 사이트를 자동으로 fetch, crawl, download, screenshot하지 않습니다.

source-first 입력이 있으면 브라우저 상태와 JSON 다운로드에 `source_brief`가 포함되고, 초기 `asset_source_candidate`가 하나 생성됩니다. 이 후보는 사용 승인 상태가 아니며 source type에 따라 blur, rewrite, license, permission review 기본값이 적용됩니다.

## Manual Asset Register

`frontend/web`에는 scene별 frontend-only Manual Asset Register가 있습니다.

사용자는 `AssetSourceCandidate`를 추가, 수정, 승인, 삭제할 수 있습니다.

주요 필드:

- `asset_candidate_id`
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

수정된 scene은 `Edited` badge를 표시하고 scene 단위로 원본으로 되돌릴 수 있습니다. 수정값은 화면, timeline, summary duration, JSON 다운로드의 `generation_result`에 반영됩니다.

## JSON Export

현재 JSON 다운로드 구조는 다음과 같습니다.

```json
{
  "generation_result": {},
  "source_brief": {},
  "asset_source_candidates": []
}
```

`source_brief`는 source-first 입력이 있을 때만 포함됩니다. `asset_source_candidates`는 후보가 없으면 빈 배열일 수 있습니다.

`generation_result.timeline.scenes[]`에는 `beats`와 `asset_review_checklist`가 항상 배열로 포함되도록 frontend에서 normalize합니다.

## 참고 채널 기준

참고 채널:

- 강석주
- 뇌전구
- 얘봐라

업로드 채널:

- 이슈털이

참고 가능한 것은 빠른 이슈 해설형 쇼츠의 일반 제작 문법입니다.

- 첫 1초 hook
- 빠른 TTS 기반 진행
- 커뮤니티/뉴스/자료화면 중심 구성
- 짧은 scene 단위 컷 전환
- 큰 자막/강조 자막 리듬
- 반응, 쟁점, 맥락 전환, 결론, 댓글 유도 구조
- 자료화면과 설명 자막의 조합
- 썸네일의 명확한 이슈 전달 방식

복제 금지:

- 특정 채널의 대본 문장
- 썸네일 디자인
- TTS 목소리/말투
- 편집 템포와 컷 구성
- 로고, 캡처, 이미지, 댓글 원문 무단 사용

참고 채널을 그대로 따라 하지 않고 이슈털이용 원본 포맷으로 재구성합니다.

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
