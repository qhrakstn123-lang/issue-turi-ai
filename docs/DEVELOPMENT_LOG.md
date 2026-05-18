# Issue Turi AI Development Log

## 2026-05-18

### Source-first Project Form

`frontend/web`의 ProjectForm에 source-first 입력을 추가했습니다. 기존 topic-only 생성은 유지하고, 사용자가 원하면 source URL/type/title/context/angle을 함께 넣어 source-capture-first 기획 흐름으로 시작할 수 있습니다.

추가된 동작:

- `source_url`, `source_type`, `source_title`, `source_context`, `source_angle` 입력
- URL 입력 시 외부 fetch/crawl/download/screenshot 없이 metadata로만 보관
- source-first 입력이 있을 때 `source_brief`를 JSON export에 포함
- source URL/type이 있으면 초기 `asset_source_candidate`를 frontend state에 생성
- 기존 `assetCandidateSafety` helper를 재사용해 community/instagram blur/rewrite, google_image license_required 등 안전 기본값 적용
- UI에 `소스 기반 기획` badge와 timeline source capture direction 표시

변경 파일:

- `frontend/web/components/ProjectForm.tsx`
- `frontend/web/app/page.tsx`
- `frontend/web/components/JsonDownloadButton.tsx`
- `frontend/web/components/TimelinePanel.tsx`
- `frontend/web/lib/types.ts`
- `frontend/web/app/globals.css`
- `tests/test_next_frontend.py`
- `docs/SOURCE_FIRST_WORKFLOW.md`
- `docs/product-plan.md`
- `docs/HANDOFF.md`
- `docs/current-project-state.md`
- `docs/TECH_STACK.md`
- `.agents/skills/shortsflow-production-grammar/SKILL.md`
- `.agents/skills/issue-turi-shorts-generation/SKILL.md`
- `docs/DEVELOPMENT_LOG.md`

제외한 것:

- 외부 사이트 자동 fetch/crawl/download/screenshot
- Google 이미지 자동 검색/캡처
- 이미지 생성
- TTS
- MP4 렌더링
- DB 저장
- `frontend/app` 변경

검증 결과:

```text
uv run --project . --with pytest pytest -q: 106 passed, 39 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

다음 추천 작업:

Source Capture Plan을 추가해 scene별 primary asset plan, capture target, fallback/mockup/rewrite plan, source review note를 구조화합니다.

## 2026-05-18

### Source-first Workflow 문서 기준선

ShortsFlow 제품 방향을 AI-image-first가 아니라 source-capture-first workflow로 재정의했습니다.

핵심 기준:

- topic-only 입력은 유지하지만 source-first input을 우선 제품 방향으로 둡니다.
- `source_context`는 사용자가 직접 요약하거나 붙여넣은 텍스트입니다.
- 외부 URL을 자동 fetch, crawl, scrape, download, capture하지 않습니다.
- AI 이미지는 기본값이 아니라 보조 컷, 배경 컷, 대체 컷입니다.
- source capture, mockup/rewrite, licensed/user-provided asset, google image reference, ai_generated 순서로 visual source priority를 둡니다.

변경 파일:

- `docs/SOURCE_FIRST_WORKFLOW.md`
- `docs/product-plan.md`
- `docs/HANDOFF.md`
- `docs/current-project-state.md`
- `.agents/skills/issue-turi-shorts-generation/SKILL.md`
- `.agents/skills/shortsflow-production-grammar/SKILL.md`

## 2026-05-18

### Manual Asset Register 안전 기본값

Manual Asset Register에서 `source_type`과 `license_status`에 따라 안전 기본값과 review notes를 자동 보정했습니다.

주요 보정:

- `community`, `instagram`: blur/rewrite 기본 활성화, 승인 해제, 닉네임/프로필/댓글 원문/개인정보 review note
- `news`, `youtube`, `broadcast`: blur 기본 활성화, permission/license 확인 note
- `google_image`: `license_required` 기본값과 원본 출처/라이선스 확인 note
- `ai_generated`: 실존 인물 오인, 브랜드/캐릭터 유사성, 허위 사실 암시 확인 note
- `user_provided`: 소유/허가 확인 note
- `avoid`: 승인 해제와 “사용 금지 또는 대체 필요” note 보장

변경 파일:

- `frontend/web/components/AssetCandidateRegister.tsx`
- `frontend/web/lib/assetCandidateSafety.ts`
- `frontend/web/app/globals.css`
- `tests/test_next_frontend.py`
- `docs/DEVELOPMENT_LOG.md`

검증 결과:

```text
uv run --project . --with pytest pytest -q: 105 passed, 39 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

## 2026-05-15

### Manual Edit runtime 안정화

Manual Edit 입력 중 `source.beats.map(...)`에서 발생하던 runtime error를 수정했습니다. legacy/fake/old result 또는 frontend-recalculated timeline에서 `beats`와 `asset_review_checklist`가 빠져도 화면과 JSON export가 깨지지 않도록 normalize했습니다.

변경 파일:

- `frontend/web/app/page.tsx`
- `frontend/web/components/JsonDownloadButton.tsx`
- `frontend/web/lib/normalize.ts`
- `tests/test_http_api.py`
- `tests/test_next_frontend.py`
- `docs/TROUBLESHOOTING.md`
- `docs/DEVELOPMENT_LOG.md`

검증 결과:

```text
uv run --project . --with pytest pytest -q: 104 passed, 39 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

## 2026-05-15

### Manual Edit / Scene 수정 UI

`frontend/web`의 scene card에 compact Manual Edit UI를 추가했습니다. backend domain/application/pipeline, backend API, `frontend/app`, 외부 API, 이미지/TTS/MP4/DB 기능은 변경하지 않았습니다.

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

수정된 scene은 `Edited` badge를 표시하고 scene 단위로 원본으로 되돌릴 수 있습니다. 수정값은 browser state, scene card, summary duration, timeline timing, JSON export의 `generation_result`에 반영됩니다.

변경 파일:

- `frontend/web/app/page.tsx`
- `frontend/web/app/globals.css`
- `frontend/web/components/SceneCard.tsx`
- `frontend/web/components/SceneEditor.tsx`
- `tests/test_next_frontend.py`
- `docs/HANDOFF.md`
- `docs/TECH_STACK.md`
- `docs/DEVELOPMENT_LOG.md`

검증 결과:

```text
uv run --project . --with pytest pytest -q: 103 passed, 39 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

## 2026-05-15

### 구현 상태 문서 정리

현재 구현 상태 기준으로 문서와 테스트 문자열을 정리했습니다.

정리 기준:

- 주 UI는 `frontend/web`의 Next.js + React + TypeScript ShortsFlow UI
- `frontend/app`은 legacy 안내/호환 페이지
- 신규 UI 작업은 `frontend/web` 기준
- `localhost:3000` 또는 실제 Next.js dev port가 ShortsFlow 작업 화면
- `127.0.0.1:8000`은 backend API server와 legacy static page host
- 기본 mode는 fake pipeline
- `openai` 또는 `real` provider mode에서만 real LLM pipeline 사용
- JSON export는 `generation_result`와 `asset_source_candidates` 기준

검증 결과:

```text
uv run --project . --with pytest pytest -q: 102 passed, 38 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

## 2026-05-15

### Timeline production beats와 asset review checklist

Timeline에 rule-based Shorts production beats와 scene별 asset review checklist를 추가했습니다. 새 LLM agent, prompt, 외부 API, 이미지/TTS/MP4 기능은 추가하지 않았습니다.

변경 파일:

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

검증 결과:

```text
uv run --project . --with pytest pytest -q: 101 passed, 37 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

## 2026-05-15

### Next.js same-origin API proxy

Next.js frontend를 `localhost:3000` 중심으로 통합했습니다. 브라우저는 Python backend `8000`을 직접 호출하지 않고, Next.js same-origin `/api/...` route handler를 통해 backend로 proxy합니다.

변경 파일:

- `frontend/web/app/api/[...path]/route.ts`
- `frontend/web/lib/api.ts`
- `tests/test_next_frontend.py`
- `README.md`
- `docs/RUNNING.md`
- `docs/HANDOFF.md`
- `docs/TECH_STACK.md`

검증 결과:

```text
uv run --project . --with pytest pytest tests/test_next_frontend.py::NextFrontendTests::test_next_frontend_scaffold_exists_without_replacing_static_frontend tests/test_next_frontend.py::NextFrontendTests::test_next_frontend_uses_required_components_and_api_base_url -q: 2 passed, 9 subtests passed
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
```

## 2026-05-15

### Timeline builder 첫 slice

생성 결과가 scene 목록만이 아니라 실제 편집 순서를 표현하는 `timeline` 데이터를 포함하도록 backend/frontend slice를 추가했습니다.

변경 파일:

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

검증 결과:

```text
npm.cmd run typecheck: succeeded
npm.cmd run lint: no warnings or errors
npm.cmd run build: succeeded
uv run --project . --with pytest pytest -q: 95 passed, 32 subtests passed
```

## 2026-05-14

### MVP scaffold와 real agent 기반

fake MVP scaffold, agent interface, LLM client, prompt loader, JSON validator, provider settings, real agent chain, safety review, preview UI, JSON download, Next.js frontend를 순차적으로 추가했습니다.

주요 결과:

- fake mode project 생성과 shorts plan 생성
- `ShortsAgentBundle`과 agent protocol
- OpenAI SDK에 직접 묶이지 않는 LLM client/prompt/validator 구조
- `RealScriptWriterAgent`
- `RealStoryboardAgent`
- `RealSubtitleAgent`
- `RealVisualAssetSuggestionAgent`
- `RealEditingDirectionAgent`
- `RealSafetyReviewAgent`
- real mixed pipeline contract tests
- safety review risk fields
- legacy static preview 확장
- JSON download
- `frontend/web` Next.js + React + TypeScript UI

자동 테스트는 fake provider를 사용하며 real OpenAI API를 호출하지 않습니다.
