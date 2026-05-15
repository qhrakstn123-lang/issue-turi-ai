# Issue Turi AI Development Log

## 2026-05-15

### 작업 내용

현재 구현 상태 기준으로 문서와 테스트 문자열 상태를 정리했다. 기능 코드, backend API, frontend 동작은 변경하지 않았다.

정리한 기준:

- 현재 주 UI는 `frontend/web`의 Next.js + React + TypeScript ShortsFlow UI다.
- `frontend/app`은 삭제하지 않고 legacy 안내/호환 페이지로 유지한다.
- 신규 UI 작업은 `frontend/web` 기준으로 진행한다.
- `http://localhost:3000` 또는 실제 Next.js dev port가 ShortsFlow 작업 화면이다.
- `http://127.0.0.1:8000`은 backend API server와 legacy static page host다.
- 기본 mode는 fake pipeline이다.
- `openai` 또는 `real` provider mode에서만 real LLM pipeline을 사용한다.
- `GenerationResult.timeline`, production beats, asset review checklist, frontend-only Manual Asset Register 상태를 문서에 반영했다.
- JSON export 구조는 `generation_result`와 `asset_source_candidates` 기준으로 정리했다.

### 변경 파일

- `AGENTS.md`
- `.agents/skills/issue-turi-shorts-generation/SKILL.md`
- `README.md`
- `docs/RUNNING.md`
- `docs/HANDOFF.md`
- `docs/current-project-state.md`
- `docs/TECH_STACK.md`
- `docs/product-plan.md`
- `doc/SHORTSFLOW_UPDATED_PRODUCT_PLAN_WITH_UI_REFERENCE.md`
- `docs/DEVELOPMENT_LOG.md`

### 검증 결과

```text
uv run --project . --with pytest pytest -q: 102 passed, 38 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

### 다음 단계

Manual Edit / Scene 수정 UI를 먼저 진행한 뒤 Publishing Readiness를 추가하는 순서를 추천한다.

## 2026-05-15

### 작업 내용

Timeline에 rule-based Shorts production beat와 scene별 asset review checklist를 추가했다. 새 LLM agent, prompt, 외부 API, 이미지/TTS/MP4 기능은 추가하지 않았다.

### 변경 파일

- `backend/src/domain/models.py`
- `frontend/web/lib/types.ts`
- `frontend/web/components/TimelinePanel.tsx`
- `frontend/web/app/globals.css`
- `tests/test_domain_models.py`
- `tests/test_project_service.py`
- `tests/test_next_frontend.py`
- `docs/HANDOFF.md`
- `docs/TECH_STACK.md`
- `docs/DEVELOPMENT_LOG.md`

### 검증 결과

```text
uv run --project . --with pytest pytest -q: 101 passed, 37 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

### 다음 단계

Publishing readiness check를 추가해 원본성, reused-content 위험, 수익화 위험, 사람 검토 항목을 업로드 전 단계에서 구조화한다.

## 2026-05-15

### 작업 내용

Next.js frontend를 `localhost:3000` 중심으로 통합했다. 브라우저는 더 이상 Python backend `8000`을 직접 호출하지 않고, Next.js의 same-origin `/api/...` route handler를 통해 backend로 proxy한다.

### 변경 파일

- `frontend/web/app/api/[...path]/route.ts`
- `frontend/web/lib/api.ts`
- `tests/test_next_frontend.py`
- `README.md`
- `docs/RUNNING.md`
- `docs/HANDOFF.md`
- `docs/TECH_STACK.md`

### 검증 결과

```text
uv run --project . --with pytest pytest tests/test_next_frontend.py::NextFrontendTests::test_next_frontend_scaffold_exists_without_replacing_static_frontend tests/test_next_frontend.py::NextFrontendTests::test_next_frontend_uses_required_components_and_api_base_url -q: 2 passed, 9 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

### 다음 단계

사용자는 `http://localhost:3000`만 확인하도록 안내한다. Python backend는 내부 API engine으로 유지하고, 실행 편의를 위해 추후 `scripts/run-dev.bat`를 추가할 수 있다.

## 2026-05-15

### 작업 내용

Timeline builder의 첫 번째 backend/frontend slice를 추가했다. 생성 결과가 이제 scene 목록뿐 아니라 실제 편집 순서를 나타내는 `timeline` 데이터를 포함한다.

### 변경 파일

- `backend/src/domain/models.py`
- `backend/src/application/pipelines/shorts_generation.py`
- `frontend/web/lib/types.ts`
- `frontend/web/app/page.tsx`
- `frontend/web/app/globals.css`
- `frontend/web/components/ResultSummary.tsx`
- `frontend/web/components/TimelinePanel.tsx`
- `tests/test_shorts_pipeline.py`
- `tests/test_http_api.py`
- `tests/test_next_frontend.py`
- `docs/TECH_STACK.md`
- `docs/HANDOFF.md`

### 검증 결과

```text
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
uv run --project . --with pytest pytest -q: 95 passed, 32 subtests passed
```

### 다음 단계

Timeline을 더 세밀한 production grammar와 asset-review checklist로 확장한다. DB persistence는 그 다음에 붙이는 것이 좋다.

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

`frontend/web`를 ShortsFlow 다크모드 SaaS UI로 리디자인했다.

### 변경 파일

- `frontend/web/app/layout.tsx`
- `frontend/web/app/page.tsx`
- `frontend/web/app/globals.css`
- `tests/test_next_frontend.py`
- `docs/HANDOFF.md`
- `docs/TECH_STACK.md`
- `docs/DEVELOPMENT_LOG.md`

### 검증 결과

기존 static frontend와 backend API는 유지하고, Next.js 앱만 ShortsFlow 브랜드 작업 화면으로 변경했다. 좌측 sidebar, 상단 search/action bar, hero panel, summary cards, safety review, scene cards, placeholder UI를 다크모드 SaaS 스타일로 정리했다.

검증 명령:

```powershell
cd frontend/web
npm.cmd run build
npm.cmd run lint
npm.cmd run typecheck
cd ../..
uv run --project . --with pytest pytest -q
```

검증 결과:

```text
Next.js build succeeded
No ESLint warnings or errors
tsc --noEmit succeeded
94 passed, 31 subtests passed
```

### 다음 단계

Timeline builder 또는 DB persistence 중 하나를 선택한다. 현재 추천은 Timeline builder다.

## 2026-05-14

### 작업 내용

Next.js + React + TypeScript 프론트엔드 앱을 `frontend/web`에 추가했다.

### 변경 파일

- `frontend/web/package.json`
- `frontend/web/app/layout.tsx`
- `frontend/web/app/page.tsx`
- `frontend/web/app/globals.css`
- `frontend/web/components/ProjectForm.tsx`
- `frontend/web/components/ResultSummary.tsx`
- `frontend/web/components/SafetyReviewPanel.tsx`
- `frontend/web/components/SceneCard.tsx`
- `frontend/web/components/VisualSection.tsx`
- `frontend/web/components/SourcingSection.tsx`
- `frontend/web/components/EditingSection.tsx`
- `frontend/web/components/JsonDownloadButton.tsx`
- `frontend/web/lib/api.ts`
- `frontend/web/lib/types.ts`
- `tests/test_next_frontend.py`
- `README.md`
- `docs/HANDOFF.md`
- `docs/TECH_STACK.md`

### 검증 결과

기존 static frontend를 유지하면서 Next.js App Router 기반 preview UI를 병렬로 추가했다. API 호출은 `lib/api.ts`, 타입은 `lib/types.ts`, 화면은 React components로 분리했다.

검증 명령:

```powershell
uv run --project . --with pytest pytest -q
cd frontend/web
npm.cmd install
npm.cmd run build
npm.cmd run lint
npm.cmd run typecheck
```

검증 결과:

```text
93 passed, 31 subtests passed
Next.js build succeeded
No ESLint warnings or errors
tsc --noEmit succeeded
```

### 다음 단계

이후 Timeline builder 또는 DB persistence 작업으로 넘어간다.

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
