# Frontend and Backend Running Guide

이 문서는 `issue-turi-ai`를 처음 보는 사람이 로컬에서 백엔드와 프런트엔드를 실행하는 방법을 정리합니다.

현재 실행 방식은 두 가지입니다.

1. 백엔드가 정적 프런트엔드(`frontend/app`)까지 같이 서빙하는 방식
2. 백엔드는 API 서버로 켜고, Next.js 프런트엔드(`frontend/web`)를 별도 서버로 켜는 방식

기본값은 fake pipeline입니다. fake mode는 OpenAI API key가 필요 없고 외부 API를 호출하지 않습니다.

## Requirements

- Python 3.12
- uv
- Node.js와 npm: Next.js 프런트엔드를 실행할 때만 필요

Python 버전 확인:

```powershell
uv run --project . python --version
```

## Recommended Local Run

현재 작업 화면을 보기 위한 추천 방식입니다.

터미널 1에서 백엔드 API 서버를 실행합니다.

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

백엔드 주소:

```text
http://127.0.0.1:8000
```

터미널 2에서 Next.js 프런트엔드를 실행합니다.

```powershell
cd frontend/web
npm install
npm run dev
```

Next.js 프런트엔드 주소:

```text
http://127.0.0.1:3000
```

`frontend/web`는 기본적으로 `http://127.0.0.1:8000` 백엔드 API를 호출합니다.

백엔드 주소를 바꾸고 싶으면 Next.js 실행 전에 설정합니다.

```powershell
cd frontend/web
$env:NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:8000"
npm run dev
```

## Static MVP Frontend

가장 단순한 실행 방식입니다. 백엔드 서버 하나가 API와 정적 HTML/CSS/JS 프런트엔드를 같이 제공합니다.

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

브라우저에서 엽니다.

```text
http://127.0.0.1:8000
```

주의: `frontend/app/index.html`을 `file://`로 직접 열면 API 요청이 실패할 수 있습니다. 반드시 위 서버를 켠 뒤 `http://127.0.0.1:8000`으로 접속하세요.

## Backend Only

백엔드 API만 켜고 싶을 때도 같은 명령을 사용합니다.

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

주요 API:

- `POST /api/projects`
- `POST /api/generate/shorts-plan`
- `GET /api/projects`
- `GET /api/projects/{project_id}`
- `PATCH /api/projects/{project_id}`

현재 repository는 in-memory 방식입니다. 서버를 끄면 생성한 프로젝트 데이터는 사라집니다.

## Fake Mode

아무 환경변수를 설정하지 않으면 fake mode로 동작합니다.

fake mode 특징:

- API key가 필요 없습니다.
- 실제 OpenAI API를 호출하지 않습니다.
- 이미지 생성, TTS, MP4 렌더링을 하지 않습니다.
- 테스트와 일반 로컬 확인에 가장 안전합니다.

명시적으로 fake mode를 지정하려면:

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="fake"
uv run --project . python -m backend.src.presentation.http.server
```

## OpenAI / Real Mode

real mode는 수동 확인용입니다. 실제 OpenAI API를 호출할 수 있고 비용이 발생할 수 있습니다.

PowerShell 환경변수 예시:

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
uv run --project . --with openai python -m backend.src.presentation.http.server
```

주의:

- API key를 코드, 문서, commit에 남기지 마세요.
- `.env`를 commit하지 마세요.
- 자동 테스트에서는 real mode를 사용하지 않습니다.

## Manual Smoke Real

서버를 켜지 않고 real pipeline 한 번만 확인할 때 사용합니다.

```powershell
$env:ISSUE_TURI_LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
uv run --project . --with openai python main.py smoke-real --topic "AI 쇼츠 자동화에 사람들이 관심 갖는 이유"
```

이 명령은 JSON을 stdout에 출력합니다. 파일 저장, 이미지 생성, TTS, MP4 렌더링은 하지 않습니다.

## Verification

백엔드와 Python 테스트:

```powershell
uv run --project . --with pytest pytest -q
```

Next.js 프런트엔드 검증:

```powershell
cd frontend/web
npm run typecheck
npm run lint
npm run build
```

## Common Problems

### Failed to fetch

원인:

- 정적 HTML을 `file://`로 직접 열었거나
- 백엔드 서버가 꺼져 있거나
- Next.js가 바라보는 API 주소가 잘못되었습니다.

해결:

```powershell
uv run --project . python -m backend.src.presentation.http.server
```

그리고 브라우저에서 `http://127.0.0.1:8000` 또는 `http://127.0.0.1:3000`으로 접속합니다.

### npm.ps1 실행 정책 오류

PowerShell에서 `npm`이 막히면 `npm.cmd`를 사용합니다.

```powershell
cd frontend/web
npm.cmd run dev
```

### 포트가 이미 사용 중인 경우

백엔드는 기본 `8000`, Next.js는 기본 `3000`을 사용합니다. 이미 사용 중이면 기존 서버를 종료하거나 다른 포트로 실행하세요.

Next.js 다른 포트 예시:

```powershell
cd frontend/web
npm run dev -- -p 3001
```

### real mode에서 API key 오류

`OPENAI_API_KEY`가 설정되어 있는지 확인합니다. key 값을 터미널이나 문서에 출력하지 마세요.

## What Is Not Running Yet

현재 로컬 실행으로 확인할 수 없는 기능:

- 이미지 생성
- TTS 생성
- MP4 렌더링
- DB 저장
- 로그인
- 결제
- 배포
