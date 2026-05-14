# Issue Turi AI Development Log

이 문서는 주요 개발 흐름을 시간순으로 기록합니다. 새 세션에서 현재 상태를 빠르게 파악하거나 발표/PPT 자료를 만들 때 참고합니다.

## 2026-05-14

### 작업 내용

fake MVP scaffold를 구성했다.

### 변경 파일

- `backend/src/domain/models.py`
- `backend/src/application/agents/fake_agents.py`
- `backend/src/application/pipelines/shorts_generation.py`
- `backend/src/application/services/project_service.py`
- `backend/src/presentation/http/api.py`
- `backend/src/presentation/http/server.py`
- `frontend/app/index.html`
- `frontend/app/app.js`
- `frontend/app/styles.css`
- `tests/*`

### 검증 결과

fake mode에서 project 생성, shorts plan 생성, browser preview가 동작하도록 테스트 기반을 만들었다.

### 다음 단계

agent 책임을 분리하고 real LLM 연동을 준비한다.

## 2026-05-14

### 작업 내용

agent interface를 분리했다.

### 변경 파일

- `backend/src/application/agents/interfaces.py`
- `backend/src/application/agents/fake_agents.py`
- `backend/src/application/pipelines/shorts_generation.py`

### 검증 결과

pipeline이 fake class가 아니라 `ShortsAgentBundle`과 protocol에 의존하도록 정리했다.

### 다음 단계

LLM client, prompt loader, JSON validator를 추가한다.

## 2026-05-14

### 작업 내용

`LLMClient`, `PromptLoader`, `JsonResponseValidator`를 추가했다.

### 변경 파일

- `backend/src/application/agents/llm.py`
- `backend/src/application/agents/prompts.py`
- `backend/src/application/agents/validation.py`
- `backend/src/infrastructure/llm/fake_client.py`
- `backend/src/infrastructure/prompts/file_prompt_loader.py`

### 검증 결과

real agent가 OpenAI SDK에 직접 묶이지 않고 client/prompt/validator를 주입받을 수 있는 구조가 되었다.

### 다음 단계

OpenAI client와 real script writer를 추가한다.

## 2026-05-14

### 작업 내용

`OpenAILLMClient`와 provider settings를 추가했다.

### 변경 파일

- `backend/src/infrastructure/llm/openai_client.py`
- `backend/src/infrastructure/llm/settings.py`
- `backend/src/presentation/composition.py`

### 검증 결과

`ISSUE_TURI_LLM_PROVIDER=fake`는 fake bundle을 만들고, `openai` 또는 `real`은 real bundle을 만들 수 있는 기반이 생겼다.

### 다음 단계

real agent를 단계별로 추가한다.

## 2026-05-14

### 작업 내용

`RealScriptWriterAgent`를 추가했다.

### 변경 파일

- `backend/src/application/agents/real/script_writer.py`
- `prompts/shorts/script_writer.md`
- `tests/test_real_script_writer_agent.py`

### 검증 결과

title, narration, target duration, style notes를 JSON 계약으로 검증한다.

### 다음 단계

storyboard real agent를 추가한다.

## 2026-05-14

### 작업 내용

`RealStoryboardAgent`를 추가했다.

### 변경 파일

- `backend/src/application/agents/real/storyboard.py`
- `prompts/shorts/storyboard.md`
- `tests/test_real_storyboard_agent.py`

### 검증 결과

stable `scene_id`를 가진 `Scene` 목록을 만들고, duration과 enum 값을 검증한다.

### 다음 단계

subtitle agent를 추가하고 scene 업데이트 방식을 고정한다.

## 2026-05-14

### 작업 내용

`RealSubtitleAgent`를 추가했다.

### 변경 파일

- `backend/src/application/agents/real/subtitle.py`
- `prompts/shorts/subtitle.md`
- `tests/test_real_subtitle_agent.py`

### 검증 결과

subtitle agent는 `subtitle`, `emphasis_caption`만 scene_id 기준으로 업데이트한다.

### 다음 단계

visual asset suggestion agent를 추가한다.

## 2026-05-14

### 작업 내용

`RealVisualAssetSuggestionAgent`를 추가했다.

### 변경 파일

- `backend/src/application/agents/real/visual_asset.py`
- `prompts/shorts/visual_prompt.md`
- `tests/test_real_visual_asset_agent.py`

### 검증 결과

visual field만 scene_id 기준으로 업데이트하고, 이전 agent 결과를 덮어쓰지 않도록 테스트했다.

### 다음 단계

visual sourcing strategy를 더 명시적으로 확장한다.

## 2026-05-14

### 작업 내용

visual sourcing strategy를 추가했다.

### 변경 파일

- `backend/src/domain/models.py`
- `backend/src/application/agents/real/visual_asset.py`
- `prompts/shorts/visual_prompt.md`
- `tests/test_real_visual_asset_agent.py`
- `tests/test_real_mixed_pipeline_contract.py`

### 검증 결과

`visual_source_strategy`, `capture_source_type`, `capture_usage_mode`, `asset_usage_note`를 scene별로 생성하고 검증한다.

### 다음 단계

editing direction agent를 추가한다.

## 2026-05-14

### 작업 내용

`RealEditingDirectionAgent`를 추가했다.

### 변경 파일

- `backend/src/application/agents/real/editing_direction.py`
- `prompts/shorts/editing_direction.md`
- `tests/test_real_editing_direction_agent.py`

### 검증 결과

motion, transition, sound effect, editing notes만 업데이트한다.

### 다음 단계

real mixed pipeline contract test를 강화한다.

## 2026-05-14

### 작업 내용

full mixed pipeline contract test를 구성했다.

### 변경 파일

- `tests/test_real_mixed_pipeline_contract.py`
- `tests/test_llm_composition.py`

### 검증 결과

real agent chain이 scene_id를 유지하고, agent별 field ownership을 지키는지 확인한다.

### 다음 단계

smoke-real 진단을 개선한다.

## 2026-05-14

### 작업 내용

`smoke-real` 진단을 개선했다.

### 변경 파일

- `main.py`
- `tests/test_main_demo.py`
- `tests/test_real_agent_json_diagnostics.py`

### 검증 결과

create/generate/get 단계별 실패 원인, status, payload, hint를 구조화해서 확인할 수 있다.

### 다음 단계

safety review도 real agent로 확장한다.

## 2026-05-14

### 작업 내용

`RealSafetyReviewAgent`를 추가했다.

### 변경 파일

- `backend/src/application/agents/real/safety_review.py`
- `backend/src/application/agents/interfaces.py`
- `backend/src/application/pipelines/shorts_generation.py`
- `backend/src/domain/models.py`
- `backend/src/presentation/composition.py`
- `prompts/safety/review.md`
- `tests/test_real_safety_review_agent.py`
- `tests/test_real_mixed_pipeline_contract.py`
- `tests/test_llm_composition.py`

### 검증 결과

safety status, notes, risk lists, human review flag, recommended revisions를 `GenerationResult`에 반영한다. `RealSafetyReviewAgent`는 scene을 수정하지 않는다.

### 다음 단계

preview UI에서 visual sourcing과 safety review 결과를 표시한다.

## 2026-05-14

### 작업 내용

Preview UI를 확장했다.

### 변경 파일

- `frontend/app/index.html`
- `frontend/app/app.js`
- `frontend/app/styles.css`
- `tests/test_static_frontend.py`

### 검증 결과

브라우저에서 visual 정보, sourcing 정보, safety review summary, risk details, recommended revisions를 확인할 수 있다.

### 다음 단계

생성 결과를 파일로 보관할 수 있게 JSON 다운로드를 추가한다.

## 2026-05-14

### 작업 내용

JSON 다운로드 기능을 추가했다.

### 변경 파일

- `frontend/app/index.html`
- `frontend/app/app.js`
- `frontend/app/styles.css`
- `tests/test_static_frontend.py`

### 검증 결과

생성 성공 후 `Download JSON` 버튼이 표시되고, 현재 `GenerationResult`를 pretty JSON으로 브라우저 다운로드할 수 있다.

검증 명령:

```powershell
uv run --project . --with pytest pytest -q
```

최근 결과:

```text
90 passed, 23 subtests passed
```

### 다음 단계

Timeline builder 또는 DB persistence 중 하나를 선택한다. 추천은 Timeline builder를 먼저 만들어 이후 TTS, asset, MP4 renderer의 기준 데이터를 고정하는 것이다.
