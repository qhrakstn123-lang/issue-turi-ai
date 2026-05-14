# Issue Turi AI 현재 구현 상태

이 문서는 이 저장소를 처음 보는 사람이 현재 코드 구조, 실행 방식, 웹 페이지에서 실제로 되는 일, 그리고 LangChain/LangGraph/RAG 같은 외부 AI 프레임워크 사용 여부를 빠르게 이해하기 위한 안내서입니다.

## 한 줄 요약

현재 프로젝트는 완성된 영상 생성기가 아니라, 유튜브 쇼츠 제작을 위한 기획 데이터를 만드는 MVP입니다.

사용자가 웹 페이지에서 주제와 톤을 입력하면 백엔드는 다음 결과를 만듭니다.

- 쇼츠 제목과 전체 내레이션 방향
- 장면별 storyboard
- 장면별 자막과 강조 자막
- 장면별 비주얼 제안과 이미지 프롬프트
- 장면별 비주얼 출처 전략
- 장면별 모션, 전환, 효과음 힌트
- 안전/권리/루머/명예훼손/개인정보/초상권/출처 사용 위험 플래그

아직 하지 않는 것:

- 실제 이미지 생성
- TTS 음성 생성
- 영상 렌더링
- MP4 다운로드
- 데이터베이스 영구 저장
- 로그인/배포/결제

## 실행 방법

기본 실행은 fake pipeline입니다. API key가 필요 없고 외부 AI API를 호출하지 않습니다.

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

브라우저에서 엽니다.

```text
http://127.0.0.1:8000
```

real mode를 직접 확인하려면 환경변수를 설정해야 합니다.

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
uv run --project . --with openai python -m backend.src.presentation.http.server
```

real mode에서도 현재는 기획 JSON만 생성합니다. 이미지, TTS, MP4 렌더링은 실행하지 않습니다.

## 웹 페이지에서 실제로 되는 흐름

현재 프론트엔드는 `frontend/app` 아래의 정적 HTML/CSS/JS입니다. React, Vue 같은 프론트엔드 프레임워크는 쓰지 않습니다.

사용자 흐름:

1. 웹 페이지에서 topic, target audience, tone, style, video length를 입력합니다.
2. 프론트엔드가 `POST /api/projects`를 호출해서 프로젝트를 만듭니다.
3. 이어서 `POST /api/generate/shorts-plan`을 호출해서 쇼츠 기획 생성을 요청합니다.
4. 백엔드가 pipeline을 실행합니다.
5. 프론트엔드가 결과를 화면에 표시합니다.

현재 웹 페이지가 보여주는 주요 항목:

- 생성된 script title
- safety status
- scene 목록
- scene purpose
- estimated duration
- narration
- subtitle
- motion direction
- sound effect hint
- editing notes

현재 웹 페이지가 아직 충분히 보여주지 않는 항목:

- visual source strategy
- asset usage note
- generated image prompt
- copyright risks
- rumor/defamation risks
- privacy/portrait risks
- source usage risks
- required human review
- recommended revisions

즉, 백엔드 결과 모델에는 safety와 visual sourcing 정보가 들어가지만, 현재 브라우저 UI는 그중 일부만 간단히 보여주는 상태입니다.

## 전체 코드 구조

프로젝트는 레이어 구조를 따릅니다.

```text
presentation -> application -> domain
```

각 레이어 역할:

- `domain`: 핵심 데이터 모델과 enum
- `application`: agent interface, fake/real agent, pipeline, service
- `infrastructure`: OpenAI client, fake LLM client, prompt loader, in-memory repository
- `presentation`: HTTP API, HTTP server, composition
- `frontend`: 정적 MVP 웹 페이지
- `prompts`: real agent용 prompt template
- `tests`: 자동 테스트

중요한 파일:

- `backend/src/domain/models.py`
  - `ContentProject`, `VideoScript`, `Scene`, `Storyboard`, `GenerationResult`
  - `SafetyStatus`, `VisualSourceStrategy`, `CaptureSourceType`, `CaptureUsageMode` 등 enum

- `backend/src/application/pipelines/shorts_generation.py`
  - 쇼츠 생성 pipeline 순서를 정의합니다.

- `backend/src/application/agents/interfaces.py`
  - agent protocol과 `ShortsAgentBundle`을 정의합니다.

- `backend/src/application/agents/fake_agents.py`
  - 기본 MVP에서 쓰는 fake agent 구현체입니다.

- `backend/src/application/agents/real/`
  - OpenAI/real mode에서 쓰는 real agent 구현체입니다.

- `backend/src/presentation/composition.py`
  - `ISSUE_TURI_LLM_PROVIDER` 값에 따라 fake bundle 또는 real bundle을 조립합니다.

- `backend/src/presentation/http/api.py`
  - `/api/projects`, `/api/generate/shorts-plan` 같은 API route를 처리합니다.

- `backend/src/presentation/http/server.py`
  - 정적 프론트엔드 파일과 JSON API를 함께 서빙합니다.

## Agent는 어디에 쓰였나

이 프로젝트의 agent는 LangChain agent가 아닙니다. 직접 만든 Python class와 protocol입니다.

공통 interface는 `backend/src/application/agents/interfaces.py`에 있습니다.

현재 pipeline 순서:

```text
ScriptWriterAgent
-> StoryboardAgent
-> VisualAssetSuggestionAgent
-> SubtitleAgent
-> EditingDirectionAgent
-> SafetyReviewAgent
-> GenerationResult
```

fake mode에서는 다음 구현체가 쓰입니다.

- `FakeScriptWriterAgent`
- `FakeStoryboardAgent`
- `FakeVisualAssetSuggestionAgent`
- `FakeSubtitleAgent`
- `FakeEditingDirectionAgent`
- `FakeSafetyReviewAgent`

openai/real mode에서는 다음 구현체가 쓰입니다.

- `RealScriptWriterAgent`
- `RealStoryboardAgent`
- `RealVisualAssetSuggestionAgent`
- `RealSubtitleAgent`
- `RealEditingDirectionAgent`
- `RealSafetyReviewAgent`

real agent는 다음 부품을 사용합니다.

- `PromptLoader`: `prompts/` 아래 markdown prompt를 읽습니다.
- `LLMClient`: OpenAI 또는 fake LLM client 인터페이스입니다.
- `JsonResponseValidator`: LLM 응답 JSON의 필수 필드와 enum 값을 검증합니다.

테스트에서는 real OpenAI API를 호출하지 않고 `FakeLLMClient`만 사용합니다.

## LangChain, LangGraph, RAG 사용 여부

현재 이 프로젝트에는 LangChain이 들어가지 않았습니다.

현재 이 프로젝트에는 LangGraph가 들어가지 않았습니다.

현재 이 프로젝트에는 RAG도 들어가지 않았습니다.

지금 구조는 다음에 가깝습니다.

```text
직접 만든 pipeline orchestrator
+ 직접 만든 agent interface
+ prompt markdown
+ LLM client wrapper
+ JSON validator
```

RAG가 없다는 뜻:

- 외부 문서 검색/임베딩/vector DB 검색을 하지 않습니다.
- 지식 베이스에서 관련 문서를 찾아 prompt에 붙이는 단계가 없습니다.
- 현재 prompt 입력은 사용자 project 정보, script, storyboard scene 데이터입니다.

LangGraph가 없다는 뜻:

- graph node/state/edge 기반 실행 엔진을 쓰지 않습니다.
- 현재 pipeline은 Python method 호출 순서로 고정되어 있습니다.

LangChain이 없다는 뜻:

- LangChain chain, tool, retriever, agent executor를 쓰지 않습니다.
- 현재 real agent는 직접 prompt를 만들고 `LLMClient.complete()`를 호출합니다.

## fake mode와 real mode 차이

기본값은 fake mode입니다.

```text
ISSUE_TURI_LLM_PROVIDER=fake
```

또는 환경변수를 설정하지 않으면 fake mode입니다.

fake mode 특징:

- API key 필요 없음
- 외부 네트워크 호출 없음
- deterministic한 테스트용 결과 생성
- MVP 웹 흐름 확인에 사용
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
- real agent들이 prompt를 만들고 OpenAI LLM 응답을 받음
- 응답은 JSON으로 검증됨
- 그래도 이미지/TTS/MP4는 생성하지 않음

## GenerationResult에 들어가는 것

현재 최종 결과 모델은 `GenerationResult`입니다.

주요 필드:

- `project_id`
- `video_script`
- `storyboard`
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
- `estimated_duration`
- `editing_notes`
- `copyright_safety_note`

## 안전 검토의 의미

`RealSafetyReviewAgent`와 `FakeSafetyReviewAgent`는 법적 판단자가 아닙니다.

역할은 다음 위험을 구조화해서 표시하는 것입니다.

- 저작권 위험
- 루머 또는 명예훼손 위험
- 개인정보 또는 초상권 위험
- 출처 사용 위험
- 사람이 최종 검토해야 하는지 여부
- 수정 권장 사항

최종 판단은 사람이 한다는 전제가 유지됩니다.

## 현재 개발 단계

현재 단계는 MVP 1 / structure hardening입니다.

진행된 것:

- layered architecture
- fake pipeline
- optional OpenAI real pipeline
- scene별 visual sourcing strategy
- real safety review agent
- HTTP JSON API
- static MVP frontend
- in-memory repository
- automated tests

아직 다음 단계로 남은 것:

- 브라우저 UI에서 safety risk 세부 필드 표시
- JSON schema 수준의 더 강한 validation
- real mode manual smoke test 품질 개선
- persistence 저장소
- image generation provider
- TTS provider
- timeline builder 고도화
- MP4 rendering

## 테스트

전체 테스트:

```powershell
uv run --project . --with pytest pytest -q
```

중요 테스트:

- `tests/test_shorts_pipeline.py`
- `tests/test_real_mixed_pipeline_contract.py`
- `tests/test_real_safety_review_agent.py`
- `tests/test_llm_composition.py`
- `tests/test_http_api.py`
- `tests/test_http_server.py`
- `tests/test_static_frontend.py`

테스트 원칙:

- 실제 OpenAI API 호출 금지
- 실제 외부 네트워크 호출 금지
- `FakeLLMClient` 사용
- fake mode가 기본으로 계속 동작해야 함
