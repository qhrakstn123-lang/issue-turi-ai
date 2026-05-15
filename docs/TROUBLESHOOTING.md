# Issue Turi AI Troubleshooting

## 2026-05-15. Browser should use port 3000 only

### 증상

사용자가 `http://localhost:3000`에서 ShortsFlow UI를 보고 있는데도 `AI 기획 생성` 시 `Failed to fetch`가 표시됐다. `8000`과 `3000`이 따로 노는 것처럼 보였다.

### 원인

기존 `frontend/web/lib/api.ts`가 browser에서 직접 `http://127.0.0.1:8000`으로 API를 호출했다. 이 구조는 CORS, stale backend process, duplicate backend process가 있을 때 사용자가 문제를 이해하기 어렵다.

### 해결

Next.js App Router에 `frontend/web/app/api/[...path]/route.ts` proxy route를 추가했다. 이제 frontend는 기본적으로 same-origin `/api/...`를 호출하고, Next.js server가 내부 Python backend `http://127.0.0.1:8000`으로 전달한다.

### 검증 명령어

```powershell
uv run --project . --with pytest pytest tests/test_next_frontend.py::NextFrontendTests::test_next_frontend_scaffold_exists_without_replacing_static_frontend tests/test_next_frontend.py::NextFrontendTests::test_next_frontend_uses_required_components_and_api_base_url -q
cd frontend/web
npm.cmd run typecheck
npm.cmd run lint
npm.cmd run build
```

### 결과

```text
2 passed, 9 subtests passed
tsc --noEmit succeeded
next lint: No ESLint warnings or errors
next build succeeded
```

### 재발 방지

브라우저에서 사용하는 app URL은 `http://localhost:3000`으로 통일한다. backend 주소가 바뀌면 browser env가 아니라 server-side `BACKEND_API_BASE_URL`을 우선 사용한다.

## 2026-05-15. Next.js preview Failed to fetch from backend API

### 증상

`http://127.0.0.1:3000` Next.js 화면에서 `AI 기획 생성`을 누르면 대본이나 장면 결과가 나오지 않고 `Failed to fetch`가 표시됐다.

### 원인

Next.js frontend는 `http://127.0.0.1:3000`에서 실행되고 backend API는 `http://127.0.0.1:8000`에서 실행된다. 브라우저가 JSON `POST` 요청 전에 CORS preflight `OPTIONS` 요청을 보내는데, backend HTTP server가 `OPTIONS`를 처리하지 않아 501을 반환했다.

### 해결

`backend/src/presentation/http/server.py`에 `do_OPTIONS`를 추가하고 API 응답에 공통 CORS headers를 반환하도록 정리했다.

### 검증 명령어

```powershell
uv run --project . --with pytest pytest tests/test_http_server.py::HttpServerTests::test_server_allows_next_frontend_cors_preflight -q
uv run --project . --with pytest pytest -q
cd frontend/web
npm.cmd run typecheck
npm.cmd run lint
```

### 결과

```text
1 passed
96 passed, 32 subtests passed
tsc --noEmit succeeded
next lint: No ESLint warnings or errors
```

### 재발 방지

Next.js처럼 다른 origin에서 backend API를 호출하는 화면을 추가할 때는 `OPTIONS` preflight와 `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`를 함께 테스트한다.

이 문서는 작업 중 발생한 문제, 원인, 해결, 검증 방법을 기록합니다. 같은 문제가 다시 나오면 먼저 이 문서를 확인합니다.

## 2026-05-14. Python 3.14 대신 3.12 사용 문제

### 증상

프로젝트 실행 또는 테스트 시 기대한 Python 버전과 다른 버전이 잡힐 수 있다.

### 원인

프로젝트는 Python 3.12를 기준으로 한다. 시스템에 여러 Python 버전이 설치되어 있으면 shell 기본 Python 또는 uv가 다른 버전을 선택할 수 있다.

### 해결

`.python-version`을 존중하고 모든 Python 명령은 `uv run --project .`로 실행한다.

### 검증 명령어

```powershell
uv run --project . python --version
```

### 결과

Python 3.12 계열이 출력되어야 한다.

### 재발 방지

- `python`, `pip` 직접 실행을 피한다.
- 테스트와 서버 실행은 항상 문서화된 uv 명령을 사용한다.

## 2026-05-14. `.venv` 삭제 중 액세스 거부 문제

### 증상

`.venv` 또는 관련 cache 삭제 중 Windows에서 access denied가 발생할 수 있다.

### 원인

Python process, server process, editor, test runner가 `.venv` 안의 파일을 잡고 있을 수 있다.

### 해결

실행 중인 서버와 Python process를 먼저 확인하고 종료한 뒤 삭제한다. 무리하게 재귀 삭제하지 않는다.

### 검증 명령어

```powershell
Get-Process | Where-Object { $_.ProcessName -like '*python*' }
```

### 결과

프로젝트 `.venv`를 사용하는 process를 확인할 수 있다.

### 재발 방지

- 삭제 전 서버와 테스트 runner를 종료한다.
- recursive delete 전 대상 경로가 workspace 내부인지 확인한다.

## 2026-05-14. `ISSUE_TURI_LLM_PROVIDER=openai` 환경변수 테스트 오염 문제

### 증상

로컬 shell에 real mode 환경변수가 남아 있으면 테스트가 fake mode가 아니라 openai mode로 동작할 수 있다.

### 원인

환경변수가 테스트 프로세스에 상속되면 composition이 real agent bundle을 만들려고 한다.

### 해결

`tests/conftest.py`에서 `ISSUE_TURI_LLM_PROVIDER`, `OPENAI_API_KEY`, `OPENAI_MODEL`을 테스트마다 제거한다.

### 검증 명령어

```powershell
uv run --project . --with pytest pytest -q
```

### 결과

local real-mode 환경변수와 무관하게 fake 기반 테스트가 통과한다.

### 재발 방지

- 자동 테스트에서 real OpenAI API를 호출하지 않는다.
- 테스트에는 `FakeLLMClient`를 사용한다.

## 2026-05-14. `smoke-real` KeyError: `result`

### 증상

`smoke-real` 실행 중 generate 응답에 `result`가 없으면 `KeyError: 'result'`가 발생할 수 있었다.

### 원인

generate 단계가 실패했는데 성공 응답처럼 바로 `result`에 접근했다.

### 해결

`main.py`의 smoke-real 진단 흐름에서 create/generate/get 단계별 status와 payload를 확인하고, `result` 또는 `project`가 없으면 구조화된 error를 반환한다.

### 검증 명령어

```powershell
uv run --project . --with pytest pytest tests/test_main_demo.py -q
```

### 결과

실패 단계, status, error, hint가 포함된 payload가 반환된다.

### 재발 방지

- 외부 agent/LLM이 개입되는 단계는 응답 shape를 먼저 확인한다.
- smoke command는 실패 원인을 숨기지 않는다.

## 2026-05-14. `model_not_found` 또는 잘못된 `OPENAI_MODEL` 이름

### 증상

real mode에서 OpenAI 호출 시 model not found 계열 오류가 발생할 수 있다.

### 원인

`OPENAI_MODEL` 값이 현재 계정 또는 API에서 사용할 수 없는 모델명일 수 있다.

### 해결

환경변수의 모델명을 사용 가능한 모델로 설정한다. 기본값은 settings에서 `gpt-5`로 둔다.

### 검증 명령어

```powershell
$env:OPENAI_MODEL="gpt-5"
uv run --project . --with openai python main.py smoke-real --topic "테스트 주제"
```

### 결과

모델명 문제가 없으면 다음 실패는 JSON 계약 또는 agent 응답 품질 문제로 좁혀진다.

### 재발 방지

- 모델명은 코드에 하드코딩하지 않고 환경변수로 관리한다.
- 문서에는 예시 key 또는 실제 key를 기록하지 않는다.

## 2026-05-14. `style_notes must be a list`

### 증상

real script writer 응답에서 `style_notes`가 문자열로 오면 validation error가 발생한다.

### 원인

`VideoScript.style_notes`는 `list[str]` 계약인데 LLM이 단일 문자열을 반환할 수 있다.

### 해결

prompt와 agent validation에서 `style_notes`가 list여야 함을 명확히 한다.

### 검증 명령어

```powershell
uv run --project . --with pytest pytest tests/test_real_script_writer_agent.py -q
```

### 결과

잘못된 type은 validation error로 잡힌다.

### 재발 방지

- real agent prompt에는 JSON shape와 type을 명시한다.
- LLM 응답은 domain model로 넣기 전에 검증한다.

## 2026-05-14. invalid JSON response

### 증상

real agent가 markdown fence, 설명문, 깨진 JSON 등을 반환하면 `invalid JSON response`가 발생한다.

### 원인

LLM 응답이 strict JSON object가 아니거나 parse할 수 없는 문자열이다.

### 해결

`JsonResponseValidator`와 `validate_agent_json_response`가 agent 이름과 raw response preview를 포함한 진단 오류를 반환하도록 한다.

### 검증 명령어

```powershell
uv run --project . --with pytest pytest tests/test_real_agent_json_diagnostics.py -q
```

### 결과

오류 메시지에 agent 이름과 response preview가 포함된다.

### 재발 방지

- prompt에 `Return JSON only`를 넣는다.
- smoke-real 실패 시 raw preview를 보고 prompt 또는 validator를 조정한다.

## 2026-05-14. `smoke-real` 대기 또는 KeyboardInterrupt 문제

### 증상

real mode smoke 실행이 오래 걸리거나 사용자가 KeyboardInterrupt로 중단할 수 있다.

### 원인

실제 LLM 호출은 네트워크, 모델 응답 시간, retry, 응답 생성 길이에 영향을 받는다.

### 해결

smoke-real은 명시적인 수동 점검에만 사용하고, 자동 테스트에는 넣지 않는다. 오래 걸리면 중단 후 어느 agent 단계에서 멈췄는지 진단을 추가한다.

### 검증 명령어

```powershell
uv run --project . --with pytest pytest -q
```

### 결과

자동 테스트는 real API 없이 빠르게 완료된다.

### 재발 방지

- real smoke와 automated test를 분리한다.
- 긴 real 호출은 비용과 시간을 예상하고 실행한다.

## 2026-05-14. `file://`로 `index.html` 직접 열어서 Failed to fetch 발생

### 증상

브라우저에서 `frontend/app/index.html`을 직접 열면 API 호출이 `Failed to fetch`로 실패할 수 있다.

### 원인

정적 파일을 `file://`로 열면 `/api/projects`, `/api/generate/shorts-plan` 요청을 처리할 HTTP server가 없다.

### 해결

프로젝트 HTTP server를 실행한 뒤 `http://127.0.0.1:8000`으로 접속한다.

### 검증 명령어

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

브라우저:

```text
http://127.0.0.1:8000
```

### 결과

정적 프론트엔드와 JSON API가 같은 서버에서 동작한다.

### 재발 방지

- README와 handoff 문서의 server 실행법을 따른다.
- `file://` 직접 실행은 지원 흐름으로 보지 않는다.

## 2026-05-14. Codex usage limit과 context token 혼동

### 증상

Codex 사용량 제한과 대화 context token 한계를 같은 문제로 오해할 수 있다.

### 원인

usage limit은 계정/세션 사용량 정책이고, context token은 모델이 한 번에 유지할 수 있는 대화/코드 문맥 한계다.

### 해결

긴 작업은 `docs/HANDOFF.md`, `docs/current-project-state.md`, `docs/TECH_STACK.md`, `docs/DEVELOPMENT_LOG.md`에 상태를 남겨 context가 줄어도 이어갈 수 있게 한다.

### 검증 명령어

```powershell
git status --short
```

### 결과

작업 상태와 문서 변경 파일을 확인할 수 있다.

### 재발 방지

- 큰 기능이 끝날 때 development log를 업데이트한다.
- 새 세션 시작 시 handoff 문서를 먼저 읽는다.

## 2026-05-14. API key 사용 시 실제 비용 발생 주의

### 증상

`ISSUE_TURI_LLM_PROVIDER=openai` 또는 `real`로 실행하면 실제 OpenAI API 호출이 발생할 수 있다.

### 원인

real mode composition이 `OpenAILLMClient`를 사용한다.

### 해결

자동 테스트와 일반 MVP 확인은 fake mode로 실행한다. real smoke는 명시적으로 필요할 때만 실행한다.

### 검증 명령어

```powershell
uv run --project . --with pytest pytest -q
```

### 결과

테스트는 실제 API key 없이 통과해야 한다.

### 재발 방지

- `.env`와 API key를 커밋하지 않는다.
- 테스트에 real OpenAI 호출을 넣지 않는다.
- real mode 실행 전 비용 발생 가능성을 확인한다.

## 2026-05-14. PowerShell에서 `npm install` 실행 정책 오류

### 증상

`frontend/web`에서 `npm install` 실행 시 다음 오류가 발생했다.

```text
npm.ps1 cannot be loaded because running scripts is disabled on this system
```

### 원인

Windows PowerShell execution policy가 `npm.ps1` 실행을 막았다.

### 해결

PowerShell script shim 대신 `npm.cmd`를 사용했다.

```powershell
npm.cmd install
```

### 검증 명령어

```powershell
npm.cmd --version
npm.cmd install
```

### 결과

`npm.cmd`는 PowerShell script execution policy에 막히지 않고 실행된다.

### 재발 방지

- Windows PowerShell에서는 npm 명령이 막히면 `npm.cmd`를 사용한다.
- 문서와 자동화 예시는 Windows에서 `npm.cmd` fallback을 고려한다.

## 2026-05-14. npm cache only mode로 dependency 설치 실패

### 증상

`npm.cmd install` 첫 실행이 다음 오류로 실패했다.

```text
ENOTCACHED
cache mode is 'only-if-cached' but no cached response is available
```

### 원인

sandbox 환경에서 네트워크 접근이 제한되어 npm registry에서 dependency를 받을 수 없었다.

### 해결

사용자 승인 후 네트워크가 가능한 권한으로 `npm.cmd install`을 다시 실행했다.

### 검증 명령어

```powershell
npm.cmd install
```

### 결과

Next.js, React, TypeScript, ESLint dependencies가 설치되고 `package-lock.json`이 생성되었다.

### 재발 방지

- 새 npm dependency 설치가 필요하면 네트워크 승인이 필요할 수 있음을 예상한다.
- 설치 후 `node_modules`는 커밋하지 않는다.

## 2026-05-14. Next.js build 중 `spawn EPERM`

### 증상

`npm.cmd run build` 실행 시 다음 오류가 발생했다.

```text
Error: spawn EPERM
```

### 원인

Next.js production build가 worker child process를 spawn하는 과정에서 sandbox 권한 제한에 걸렸다.

### 해결

사용자 승인 후 권한 상승으로 같은 build 명령을 다시 실행했다.

### 검증 명령어

```powershell
npm.cmd run build
```

### 결과

Next.js production build가 성공했다.

### 재발 방지

- Next.js build가 `spawn EPERM`으로 실패하면 코드 오류와 권한 오류를 구분한다.
- 권한 문제로 확인되면 같은 명령을 승인받아 재실행한다.
