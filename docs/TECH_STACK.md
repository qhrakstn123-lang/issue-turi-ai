# Issue Turi AI Tech Stack

## 프로젝트 개요

Issue Turi AI는 유튜브 채널 "이슈털이"를 위한 쇼츠 기획 MVP입니다.

현재 목표는 완성 영상 파일을 만드는 것이 아니라, 사람이 검토할 수 있는 쇼츠 제작 기획 데이터를 생성하는 것입니다.

현재 흐름:

```text
topic input
-> script
-> storyboard scenes
-> subtitles
-> visual sourcing suggestions
-> editing directions
-> safety review
-> browser preview
-> JSON download
```

아직 실제 이미지, 음성, 영상 파일은 생성하지 않습니다.

## MVP 목표

MVP 1의 핵심 목표는 다음입니다.

- 주제, 타깃, 톤, 스타일, 길이를 입력한다.
- 쇼츠용 script와 scene plan을 만든다.
- 장면별 subtitle, emphasis caption, visual prompt, sourcing strategy, editing direction을 만든다.
- safety review 결과를 구조화해서 보여준다.
- 브라우저에서 결과를 preview한다.
- 생성 결과를 JSON으로 다운로드한다.
- fake mode를 기본으로 유지한다.
- real OpenAI 연동은 명시적으로 `ISSUE_TURI_LLM_PROVIDER=openai` 또는 `real`일 때만 사용한다.

## 전체 아키텍처

레이어 방향은 다음을 유지합니다.

```text
presentation -> application -> domain
```

외부 세부 구현은 infrastructure에 둡니다.

```text
frontend
  -> presentation/http
  -> application/service
  -> application/pipeline
  -> application/agents
  -> domain/models
  -> infrastructure/openai, prompt loader, repository
```

현재 LangChain, LangGraph, RAG는 사용하지 않습니다.

현재 구조는 직접 만든 pipeline orchestrator, agent interface, prompt loader, LLM client wrapper, JSON validator 기반입니다.

## 프론트엔드 구조

프론트엔드는 `frontend/app` 아래의 정적 HTML/CSS/JS입니다.

- `frontend/app/index.html`: 입력 폼, 결과 summary, safety review, scene 카드 template, JSON 다운로드 버튼
- `frontend/app/app.js`: API 호출, 결과 렌더링, safety/visual/sourcing 표시, JSON 다운로드
- `frontend/app/styles.css`: MVP 화면 스타일

사용 중인 프론트엔드 프레임워크는 없습니다.

- Next.js 없음
- React 없음
- Vue 없음
- 빌드 단계 없음

브라우저 동작 흐름:

1. 사용자가 form을 제출한다.
2. `POST /api/projects`로 프로젝트를 만든다.
3. `POST /api/generate/shorts-plan`로 생성 pipeline을 실행한다.
4. 응답의 `result`를 화면에 표시한다.
5. `Download JSON` 버튼으로 현재 `result`를 pretty JSON 파일로 저장한다.

## 백엔드 구조

백엔드는 Python 3.12와 표준 라이브러리 HTTP server 중심의 단순 MVP 구조입니다.

주요 진입점:

- `backend/src/presentation/http/server.py`: 정적 프론트엔드와 JSON API를 함께 서빙
- `backend/src/presentation/http/api.py`: API route 처리
- `backend/src/presentation/composition.py`: provider mode에 따라 fake/real agent bundle 구성
- `main.py`: demo 실행, server 실행, `smoke-real` 실행

현재 서버 실행:

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

브라우저 URL:

```text
http://127.0.0.1:8000
```

## 레이어별 책임

### domain

위치:

```text
backend/src/domain
```

역할:

- 핵심 모델과 enum 정의
- 외부 API, HTTP, DB, OpenAI를 모름

주요 모델:

- `ContentProject`
- `VideoScript`
- `Scene`
- `Storyboard`
- `GenerationResult`
- `Timeline`

주요 enum:

- `OutputFormat`
- `ProjectStatus`
- `SafetyStatus`
- `VisualAssetType`
- `VisualSourceStrategy`
- `CaptureSourceType`
- `CaptureUsageMode`
- `MotionDirection`
- `Transition`
- `SoundEffectHint`

### application

위치:

```text
backend/src/application
```

역할:

- use case, service, pipeline, agent interface, fake/real agent 구현
- pipeline이 fake class에 직접 의존하지 않고 interface와 bundle에 의존

주요 파일:

- `services/project_service.py`
- `pipelines/shorts_generation.py`
- `agents/interfaces.py`
- `agents/fake_agents.py`
- `agents/real/*.py`
- `agents/validation.py`

### infrastructure

위치:

```text
backend/src/infrastructure
```

역할:

- 외부 세부 구현 담당
- OpenAI client
- fake LLM client
- prompt file loader
- in-memory repository

주요 파일:

- `llm/openai_client.py`
- `llm/fake_client.py`
- `llm/settings.py`
- `prompts/file_prompt_loader.py`
- `database/memory_repository.py`

### presentation

위치:

```text
backend/src/presentation
```

역할:

- HTTP API
- HTTP server
- dependency composition

주요 파일:

- `composition.py`
- `http/api.py`
- `http/server.py`

### frontend

위치:

```text
frontend/app
```

역할:

- 정적 MVP UI
- 입력 폼
- 생성 결과 preview
- safety review 표시
- visual sourcing 표시
- JSON 다운로드

## fake mode와 openai/real mode

### fake mode

기본값입니다.

```text
ISSUE_TURI_LLM_PROVIDER=fake
```

또는 환경변수가 없으면 fake mode입니다.

특징:

- API key 필요 없음
- 외부 네트워크 호출 없음
- 테스트와 MVP preview에 사용
- `FakeScriptWriterAgent`, `FakeStoryboardAgent`, `FakeVisualAssetSuggestionAgent`, `FakeSubtitleAgent`, `FakeEditingDirectionAgent`, `FakeSafetyReviewAgent` 사용

### openai/real mode

명시적으로 켭니다.

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
```

특징:

- OpenAI API key 필요
- 실제 비용 발생 가능
- 자동 테스트에서는 사용 금지
- real agent 응답은 JSON으로 검증
- 이미지/TTS/MP4는 여전히 생성하지 않음

## 현재 full real pipeline

`ISSUE_TURI_LLM_PROVIDER=openai` 또는 `real`일 때 현재 real pipeline은 다음 순서입니다.

```text
RealScriptWriterAgent
-> RealStoryboardAgent
-> RealSubtitleAgent
-> RealVisualAssetSuggestionAgent
-> RealEditingDirectionAgent
-> RealSafetyReviewAgent
```

pipeline 구현 위치:

```text
backend/src/application/pipelines/shorts_generation.py
```

agent 조립 위치:

```text
backend/src/presentation/composition.py
```

## LLMClient 구조

LLM 호출은 application agent가 직접 OpenAI SDK에 묶이지 않도록 interface로 감쌉니다.

주요 구성:

- `LLMClient`: prompt를 받아 string response를 반환하는 protocol
- `OpenAILLMClient`: OpenAI API 호출 구현체
- `FakeLLMClient`: 테스트용 fake 응답 queue

테스트에서는 `FakeLLMClient`만 사용합니다.

## PromptLoader 구조

real agent는 prompt markdown을 직접 파일에서 읽습니다.

구성:

- `PromptLoader`: prompt name을 받아 string template을 반환하는 protocol
- `FilePromptLoader`: `prompts/` 디렉터리에서 markdown 파일 로드

주요 prompt:

- `prompts/shorts/script_writer.md`
- `prompts/shorts/storyboard.md`
- `prompts/shorts/subtitle.md`
- `prompts/shorts/visual_prompt.md`
- `prompts/shorts/editing_direction.md`
- `prompts/safety/review.md`

## JsonResponseValidator 구조

real agent 응답은 JSON 계약을 통과해야 pipeline에 들어갑니다.

구성:

- `JsonResponseValidator`
- `LLMResponseValidationError`
- `validate_agent_json_response`

검증하는 것:

- 빈 응답 여부
- JSON parse 가능 여부
- JSON object 여부
- required field 존재 여부
- enum field 허용값 여부

agent별 추가 검증:

- list type
- scene_id 존재 여부
- unknown scene_id 여부
- numeric duration
- allowed enum
- non-empty asset usage note
- safety review extra key 금지

## visual sourcing 구조

`RealVisualAssetSuggestionAgent`는 단순 이미지 프롬프트 생성기가 아닙니다.

장면별로 어떤 시각 자료를 어떤 방식으로 써야 하는지 추천합니다.

주요 필드:

- `visual_asset_type`
- `visual_description`
- `generated_image_prompt`
- `gif_or_clip_suggestion`
- `stock_search_keywords`
- `visual_source_strategy`
- `capture_source_type`
- `capture_usage_mode`
- `asset_usage_note`

허용 전략:

- `reference_capture`
- `mockup`
- `stock_asset`
- `ai_generated`
- `original_sticker`
- `text_card`
- `user_provided`
- `avoid`

핵심 원칙:

- capture는 무조건 금지하지 않는다.
- 다만 news, YouTube, broadcast, Instagram, community, Google image는 각각 권리/개인정보/출처 위험을 분류한다.
- 실제 이미지 파일을 다운로드하거나 생성하지 않는다.
- 최종 권리 판단은 safety review와 사람이 한다.

## safety review 구조

`RealSafetyReviewAgent`는 법적 판단자가 아닙니다.

역할은 다음 위험을 구조화해서 flag로 보여주는 것입니다.

- 저작권 위험
- 루머/명예훼손 위험
- 개인정보/초상권 위험
- 출처 사용 위험
- 사람 검토 필요 여부
- 수정 권장 사항

주요 결과 필드:

- `safety_status`
- `safety_notes`
- `copyright_risks`
- `rumor_or_defamation_risks`
- `privacy_or_portrait_risks`
- `source_usage_risks`
- `required_human_review`
- `recommended_revisions`

허용 safety status:

- `approved`
- `needs_review`
- `rejected`

## 테스트 명령어

전체 테스트:

```powershell
uv run --project . --with pytest pytest -q
```

Python 버전 확인:

```powershell
uv run --project . python --version
```

프론트 정적 테스트:

```powershell
uv run --project . --with pytest pytest tests/test_static_frontend.py -q
```

real mixed pipeline 계약 테스트:

```powershell
uv run --project . --with pytest pytest tests/test_real_mixed_pipeline_contract.py -q
```

## smoke-real 실행법

real mode를 수동으로 확인할 때만 사용합니다.

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
uv run --project . --with openai python main.py smoke-real --topic "AI 쇼츠 자동화에 사람들이 관심 갖는 이유"
```

주의:

- 실제 OpenAI API를 호출합니다.
- 비용이 발생할 수 있습니다.
- API key를 출력, 기록, 커밋하지 않습니다.
- 자동 테스트에서 사용하지 않습니다.

## 환경변수

| 이름 | 기본값 | 설명 |
| --- | --- | --- |
| `ISSUE_TURI_LLM_PROVIDER` | `fake` | `fake`, `openai`, `real` 중 하나 |
| `OPENAI_API_KEY` | 없음 | real mode에서 필요 |
| `OPENAI_MODEL` | `gpt-5` | real mode 모델명 |

## 현재 제외된 기능

현재 구현하지 않은 기능:

- 이미지 생성
- TTS 생성
- MP4 렌더링
- DB persistence
- 로그인
- 결제
- 배포
- YouTube/Instagram 업로드
- vector DB/RAG
- LangChain/LangGraph 기반 orchestration

## 다음 확장 계획

추천 순서:

1. Timeline builder
   - scene duration을 기반으로 실제 편집 timeline data를 명확히 만든다.
   - 이후 TTS, 이미지 asset, MP4 renderer의 기준 데이터가 된다.

2. DB persistence
   - 현재 in-memory repository를 SQLite 등으로 교체한다.
   - 생성 결과와 사용자가 수정한 scene을 보존한다.

3. Asset management
   - 이미지, 음성, 효과음, stock reference metadata를 관리한다.

4. TTS provider
   - `tts_text` 기반 음성 생성 provider를 추가한다.

5. Image provider
   - `generated_image_prompt` 기반 이미지 생성 또는 asset sourcing provider를 추가한다.

6. MP4 renderer
   - Remotion 또는 FFmpeg 기반 render job manager를 추가한다.

7. JSON export 고도화
   - 현재 브라우저 JSON 다운로드를 유지하면서, 추후 DB 저장본 export, timeline export, render package export로 확장한다.
