# Issue Turi AI 현재 구현 상태

이 문서는 현재 저장소를 처음 보는 사람이 무엇이 동작하고, 무엇이 아직 범위 밖인지 빠르게 파악하기 위한 상태 요약입니다.

## 한 줄 요약

현재 프로젝트는 완성된 영상 생성기가 아니라, 쇼츠 제작을 위한 **기획 데이터와 검토 자료를 만드는 MVP**입니다.

사용자가 ShortsFlow Next.js UI에서 주제와 톤을 입력하면 백엔드는 다음 결과를 생성합니다.

- 쇼츠 제목과 전체 내레이션 방향
- 장면별 storyboard
- 장면별 자막과 강조 자막
- 장면별 비주얼 제안과 이미지 프롬프트
- 장면별 비주얼 출처 전략
- 장면별 모션, 전환, 효과음 힌트
- 안전/권리/루머/명예훼손/개인정보/초상권/출처 사용 위험 플래그
- `GenerationResult.timeline`
- scene별 rule-based production beats
- scene별 asset review checklist

아직 하지 않는 것:

- 실제 이미지 생성
- TTS 음성 생성
- 영상 렌더링
- MP4 다운로드
- 데이터베이스 영구 저장
- 로그인/배포/결제

## 현재 주 UI

현재 주 UI는 `frontend/web`의 **Next.js + React + TypeScript** 앱입니다.

개발 중 사용자가 확인할 주소는 다음입니다.

```text
http://localhost:3000
```

또는 Next.js dev server가 다른 포트를 배정하면 터미널에 표시된 실제 dev port를 사용합니다.

브라우저 흐름:

```text
Browser
-> http://localhost:3000
-> Next.js same-origin /api/... route
-> internal Python backend at http://127.0.0.1:8000
```

`http://127.0.0.1:8000`은 Python backend API와 legacy 안내 페이지용입니다. 일반적인 ShortsFlow 작업 화면은 `localhost:3000`의 Next.js UI입니다.

## legacy frontend

`frontend/app`은 삭제하지 않고 유지합니다.

역할:

- backend server가 직접 서빙할 수 있는 legacy 안내/호환 화면
- 간단한 정적 MVP 확인용
- 기존 테스트와 최소 fallback 유지

신규 UI 기능은 `frontend/app`에 추가하지 않습니다. 앞으로 UI 작업은 `frontend/web` 기준으로 진행합니다.

## 실행 방법

터미널 1에서 Python backend를 실행합니다.

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

기본 mode는 fake pipeline입니다. API key가 필요 없고 외부 AI API를 호출하지 않습니다.

## fake mode와 real mode

기본값은 fake mode입니다.

```text
ISSUE_TURI_LLM_PROVIDER=fake
```

또는 환경변수를 설정하지 않으면 fake mode입니다.

fake mode 특징:

- API key 필요 없음
- 외부 네트워크 호출 없음
- deterministic한 테스트용 결과 생성
- 자동 테스트의 기본 전제

real mode:

```text
ISSUE_TURI_LLM_PROVIDER=openai
```

또는:

```text
ISSUE_TURI_LLM_PROVIDER=real
```

real mode 특징:

- OpenAI API key 필요
- 실제 OpenAI API 호출 가능
- 응답은 JSON 계약으로 검증
- 그래도 이미지/TTS/MP4는 생성하지 않음

## 현재 real pipeline

`ISSUE_TURI_LLM_PROVIDER=openai` 또는 `real`일 때 real pipeline 순서는 고정입니다.

```text
RealScriptWriterAgent
-> RealStoryboardAgent
-> RealSubtitleAgent
-> RealVisualAssetSuggestionAgent
-> RealEditingDirectionAgent
-> RealSafetyReviewAgent
```

각 agent는 자기 책임 필드만 수정합니다. Safety review는 scene을 수정하지 않고 `GenerationResult`의 safety 필드만 업데이트합니다.

## GenerationResult에 들어가는 것

최종 결과 모델은 `GenerationResult`입니다.

주요 필드:

- `project_id`
- `video_script`
- `storyboard`
- `timeline`
- `safety_status`
- `safety_notes`
- `copyright_risks`
- `rumor_or_defamation_risks`
- `privacy_or_portrait_risks`
- `source_usage_risks`
- `required_human_review`
- `recommended_revisions`

`storyboard.scenes` 안에는 장면별 제작 정보가 들어갑니다.

주요 scene 필드:

- `scene_id`
- `scene_purpose`
- `narration`
- `tts_text`
- `subtitle`
- `emphasis_caption`
- `visual_asset_type`
- `visual_description`
- `generated_image_prompt`
- `gif_or_clip_suggestion`
- `stock_search_keywords`
- `visual_source_strategy`
- `capture_source_type`
- `capture_usage_mode`
- `asset_usage_note`
- `motion_direction`
- `transition`
- `sound_effect_hint`
- `editing_notes`

## Timeline 상태

`GenerationResult.timeline`은 구현되어 있습니다.

현재 timeline은 다음을 포함합니다.

- scene별 `start_time`, `end_time`, `duration`
- subtitle/emphasis caption timing
- motion, transition, visual metadata
- narration audio placeholder
- sound effect timing
- rule-based production beats
- scene별 asset review checklist

이 timeline은 아직 렌더링 지시서가 아니라 planning contract입니다. 실제 음성, 이미지, MP4 파일을 만들지는 않습니다.

## Manual Asset Register

`frontend/web`에는 scene별 frontend-only Manual Asset Register가 있습니다.

사용자는 scene별 `AssetSourceCandidate`를 추가, 수정, 승인, 삭제할 수 있습니다.

후보 필드:

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

이 데이터는 브라우저 state입니다. DB 저장은 아직 없으므로 새로고침하면 사라집니다.

JSON 다운로드는 다음 구조를 사용합니다.

```json
{
  "generation_result": {},
  "asset_source_candidates": []
}
```

## 코드 구조

프로젝트는 레이어 구조를 따릅니다.

```text
presentation -> application -> domain
```

각 레이어 역할:

- `domain`: 핵심 데이터 모델과 enum
- `application`: agent interface, fake/real agent, pipeline, service
- `infrastructure`: OpenAI client, fake LLM client, prompt loader, in-memory repository
- `presentation`: HTTP API, HTTP server, composition
- `frontend/web`: 현재 주 Next.js UI
- `frontend/app`: legacy 정적 안내/호환 UI
- `prompts`: real agent용 prompt template
- `tests`: 자동 테스트

현재 LangChain, LangGraph, RAG는 사용하지 않습니다.

## 다음 안전한 작업 후보

우선순위 후보:

1. Manual Edit / Scene 수정 UI
   - 현재 생성 결과를 사람이 다듬는 흐름을 강화합니다.
   - DB 저장 전에는 frontend state 또는 JSON export 중심으로 제한하는 것이 안전합니다.

2. Publishing Readiness
   - originality risk, reused-content risk, monetization risk, required human checks를 planning data로 추가합니다.
   - 이미지/TTS/MP4 전에 업로드 전 검토 기준을 구조화할 수 있습니다.

DB persistence, 이미지 생성, TTS, MP4 렌더링은 그 이후 단계입니다.
