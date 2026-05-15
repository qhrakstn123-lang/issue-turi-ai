# ShortsFlow 업데이트 제품 플랜 & UI 리디자인 로드맵

> 이 문서는 기존 “이슈털이 AI 콘텐츠 제작 서비스” 초기 플랜을 현재 `issue-turi-ai` 구현 상태에 맞게 수정한 최신 제품/개발 플랜입니다.  
> 서비스 브랜드는 특정 채널명에 종속되지 않도록 **ShortsFlow**로 정리합니다.

---

## 1. 결론

기존 플랜의 방향은 맞지만, 지금 상태에서는 그대로 쓰면 안 됩니다.

기존 플랜은 “처음 시작하기 전 전체 설계” 기준이었고, 현재 프로젝트는 이미 다음 단계까지 진행됐습니다.

- fake MVP pipeline 구현
- full real LLM pipeline 구현
- RealSafetyReviewAgent까지 연결
- visual sourcing strategy 구현
- preview UI 확장
- JSON 다운로드 기능 추가
- Next.js + React + TypeScript `frontend/web` 추가
- 문서화 기반 구축

따라서 이제 플랜은 아래 방향으로 수정해야 합니다.

```text
초기 기획서 생성기
→ ShortsFlow AI Shorts Planning Studio
→ 다크모드 SaaS 대시보드
→ 프로젝트 상세/장면 편집 스튜디오
→ Timeline builder
→ DB 저장/프로젝트 관리
→ 이미지/TTS/렌더링 provider
→ MP4 자동 생성
→ 카드뉴스/롱폼 확장
```

---

## 2. 브랜드 방향

### 기존 이름

- Issue Turi AI
- 이슈털이 AI
- 이슈털이 Studio

### 수정 방향

채널명이 들어가면 나중에 다른 사용자에게 판매하거나 배포하기 어렵습니다.  
따라서 UI와 서비스명은 범용 브랜드로 갑니다.

### 최종 추천 브랜드

```text
ShortsFlow
AI Shorts Planning Studio
```

### 브랜드 의미

- Shorts: 유튜브 쇼츠, 릴스, 짧은 영상 콘텐츠
- Flow: 주제 입력부터 기획, 장면, 검토, 내보내기까지 이어지는 제작 흐름
- Studio: 단순 생성기가 아니라 콘텐츠 제작 도구라는 느낌

### 화면 문구 예시

```text
ShortsFlow
AI Shorts Planning Studio

Plan better. Create faster. Grow bigger.
```

한국어 메인 카피는 다음 중 하나를 사용합니다.

```text
오늘도 이슈를 짧고 강렬한 쇼츠로 만들어보세요.
주제 하나로 쇼츠 기획서를 완성하세요.
아이디어를 장면, 자막, 안전 검토까지 한 번에 정리하세요.
```

---

## 3. 서비스 한 문장 정의

**ShortsFlow는 콘텐츠 제작자가 주제만 입력하면 AI가 쇼츠용 대본, 장면 구성, 자막, 시각자료 소싱 전략, 편집 지시, 안전성 검토를 생성하고, 이후 이미지/TTS/MP4 렌더링까지 확장할 수 있는 AI Shorts Planning Studio입니다.**

---

## 4. 현재 구현 상태

### 4.1 완료된 기능

| 영역 | 상태 | 설명 |
| --- | --- | --- |
| 주제 입력 | 완료 | topic, target, tone, style, length 입력 |
| fake MVP pipeline | 완료 | 외부 API 없이 deterministic 결과 생성 |
| OpenAI real mode | 완료 | `ISSUE_TURI_LLM_PROVIDER=openai` 또는 `real` |
| ScriptWriter | 완료 | title, narration, style_notes 생성 |
| Storyboard | 완료 | scene_id 기반 장면 생성 |
| Subtitle | 완료 | subtitle, emphasis_caption 업데이트 |
| VisualAssetSuggestion | 완료 | visual field + sourcing field 생성 |
| EditingDirection | 완료 | motion, transition, sound, editing_notes 생성 |
| SafetyReview | 완료 | risk list와 human review flag 생성 |
| Preview UI | 완료 | static UI와 Next.js UI 기반 결과 표시 |
| JSON 다운로드 | 완료 | 현재 generation result를 pretty JSON으로 다운로드 |
| smoke-real | 완료 | real pipeline 수동 실행 및 진단 |
| 문서화 | 완료 | TECH_STACK, TROUBLESHOOTING, DEVELOPMENT_LOG 등 |

### 4.2 아직 안 된 기능

| 영역 | 상태 | 이유 |
| --- | --- | --- |
| 프로젝트 DB 저장 | 미완성 | 현재는 in-memory/JSON 다운로드 중심 |
| 프로젝트 목록/재열기 | 미완성 | persistence 필요 |
| 장면 편집 후 저장 | 부분/미완성 | scene patch는 있으나 본격 editor 아님 |
| TimelineBuilder | 미완성 | 다음 단계 후보 |
| 실제 이미지 생성 | 미완성 | provider/interface 필요 |
| 실제 TTS 생성 | 미완성 | ElevenLabs/OpenAI TTS provider 필요 |
| AssetStorage | 미완성 | 로컬/S3 저장소 설계 필요 |
| RenderJobManager | 미완성 | MP4 렌더링 상태 관리 필요 |
| MP4 렌더링 | 미완성 | Remotion 또는 FFmpeg 필요 |
| 로그인/결제/크레딧 | 미완성 | 서비스화 후반부 |
| 카드뉴스 | 미완성 | 확장 기능 |
| 롱폼 | 미완성 | 확장 기능 |
| 업로드 자동화 | 미완성 | YouTube/Instagram API 후순위 |

---

## 5. 기존 플랜에서 수정해야 하는 부분

### 5.1 채널 종속 표현 제거

기존 플랜에는 “이슈털이 채널용”, “이슈털이 기본형” 같은 표현이 많습니다.  
서비스화 관점에서는 브랜드와 기능을 범용화해야 합니다.

수정 전:

```text
이슈털이 쇼츠 제작 지시서 생성기
이슈털이 기본 스타일
이슈털이 채널용 콘텐츠 방향
```

수정 후:

```text
ShortsFlow AI Shorts Planning Studio
ShortsFlow 기본 쇼츠 스타일
이슈/썰/정보형 쇼츠 제작자용 콘텐츠 방향
```

### 5.2 MVP 1을 현재 완료 상태 기준으로 재분류

기존 플랜의 MVP 1은 “편집 지시서 MVP”였습니다.  
현재는 MVP 1의 핵심 backend와 preview/export가 대부분 완료되었습니다.

수정된 분류:

```text
MVP 1A. AI 쇼츠 기획 생성 pipeline — 완료
MVP 1B. visual sourcing + safety review — 완료
MVP 1C. preview UI + JSON export — 완료
MVP 1D. Next.js frontend/web 이식 — 완료
MVP 1E. ShortsFlow dark UI redesign — 다음 작업
MVP 1F. Timeline builder — 다음 후보
MVP 1G. DB persistence/project management — 이후 작업
```

### 5.3 MVP 2 전에 MVP 1.5 추가

기존 플랜은 MVP 1 다음에 바로 자동 영상 생성 MVP로 넘어갑니다.  
하지만 지금 구조에서는 그 사이에 **Timeline & Persistence 단계**가 필요합니다.

```text
MVP 1.5. Timeline & Project Persistence
- TimelineBuilder
- scene start/end time 계산
- total duration / target duration 비교
- 프로젝트 저장
- 프로젝트 목록
- 프로젝트 상세 재조회
- scene 수정 저장
- JSON 재다운로드
```

이걸 하지 않고 바로 이미지/TTS/MP4로 가면 생성 결과 관리가 어렵습니다.

---

## 6. 새 로드맵

### Phase 0. 완료된 기반

- fake MVP pipeline
- full real pipeline
- RealScriptWriterAgent
- RealStoryboardAgent
- RealSubtitleAgent
- RealVisualAssetSuggestionAgent
- RealEditingDirectionAgent
- RealSafetyReviewAgent
- visual sourcing strategy
- safety risk fields
- smoke-real diagnostic
- static preview UI
- JSON download
- Next.js frontend/web
- docs 기반 문서화

---

### Phase 1. ShortsFlow 다크모드 UI 리디자인

**목표:** 현재 Next.js UI를 전문적인 다크모드 SaaS 화면으로 재구성합니다.

#### 디자인 기준

- 브랜드명: `ShortsFlow`
- subtitle: `AI Shorts Planning Studio`
- 전체 다크모드
- 보라/블루/시안 계열 그라데이션 포인트
- glass/card 기반 SaaS dashboard
- 현재 가능한 기능만 실제 연결
- 아직 안 되는 기능은 `준비 중`, `Coming soon`, `Mock`으로 표시

#### UI 레퍼런스 기준

- 대시보드: 이전에 만든 2번째 SaaS dashboard 이미지를 다크모드로 변환한 스타일
- 프로젝트 상세/장면 편집: 이전에 만든 3번째 production studio/editor 이미지를 다크모드로 변환한 스타일
- 실제 구현 시 아래 레퍼런스 이미지를 우선 참고한다.

#### UI 레퍼런스 이미지 보관 위치

레퍼런스 이미지는 repository 안에 아래 경로로 저장한다.

```text
docs/assets/ui-reference/shortsflow-dark-dashboard-and-editor-reference.png
```

권장 폴더 구조:

```text
docs/
  assets/
    ui-reference/
      shortsflow-dark-dashboard-and-editor-reference.png
```

이 이미지는 최종 디자인 파일이 아니라 **디자인 방향 기준(reference of intent)** 으로만 사용한다.
구현 시에는 이미지의 레이아웃, 정보 구조, 다크모드 톤, 카드 스타일, 사이드바/탑바/대시보드/프로젝트 편집 구조를 참고하되, 이미지 안의 임시 텍스트·숫자·가짜 썸네일·사용자 정보는 그대로 복사하지 않는다.

#### 구현 범위

- `frontend/web`만 수정
- 기존 `frontend/app` static UI 유지
- backend API 구조 변경 금지
- 기능 추가 금지
- 생성/preview/json download 유지

#### 예상 화면 구조

```text
ShortsFlow App Shell
├── Sidebar
│   ├── Home
│   ├── Projects
│   ├── Templates
│   ├── AI Idea
│   ├── Script & Hook
│   ├── Scenes
│   ├── Assets
│   ├── Analytics
│   └── Settings
├── Topbar
│   ├── Search
│   ├── Help
│   ├── Notification
│   └── User menu
└── Main
    ├── Dashboard / Home
    └── Project Detail / Scene Editor
```

---

### Phase 2. Timeline builder

**목표:** 현재 scene의 `estimated_duration`을 기반으로 실제 영상 제작용 timeline preview를 만듭니다.

#### 기능

- scene별 start/end time 계산
- total estimated duration 계산
- target duration과 gap 표시
- scene purpose별 timeline card 표시
- subtitle/narration 요약 표시
- JSON 다운로드 결과에 timeline preview 포함 여부 검토

#### 우선 프론트 계산으로 시작

처음에는 backend domain을 건드리지 않고 `frontend/web`에서 계산합니다.

```text
scene_001: 0:00 - 0:05
scene_002: 0:05 - 0:10
scene_003: 0:10 - 0:15
```

---

### Phase 3. DB persistence / 프로젝트 관리

**목표:** JSON 다운로드에 의존하지 않고 프로젝트를 저장하고 다시 열 수 있게 합니다.

#### 기능

- 프로젝트 저장
- 프로젝트 목록
- 프로젝트 상세 조회
- generation result 저장
- scene 수정 저장
- safety status 저장
- updated_at / created_at 관리

#### MVP DB

처음에는 SQLite 또는 파일 기반 repository로 시작해도 됩니다.

---

### Phase 4. Scene editing save flow

**목표:** 화면에서 scene별 필드를 수정하고 저장할 수 있게 합니다.

#### 1차 수정 대상

- subtitle
- emphasis_caption
- narration
- tts_text
- visual_description
- generated_image_prompt
- visual_source_strategy
- capture_usage_mode
- asset_usage_note
- motion_direction
- transition
- sound_effect_hint
- editing_notes
- estimated_duration

#### 주의

- scene_id는 변경 금지
- real agent 결과를 통째로 덮어쓰지 않기
- field ownership 유지

---

### Phase 5. Fake provider 기반 자동 영상 생성 준비

**목표:** 실제 외부 API 없이 자동 영상 생성 구조를 먼저 설계합니다.

#### 추가할 interface

- ImageGenerationProvider
- TTSProvider
- AssetStorage
- TimelineBuilder
- FakeVideoRenderer
- RenderJobManager

#### 테스트 원칙

- 실제 OpenAI, ElevenLabs, 이미지 API, 렌더링 호출 금지
- fake provider로 deterministic 결과 생성
- 렌더링 job status 테스트

---

### Phase 6. 실제 이미지/TTS provider 연결

**목표:** 장면별 image/TTS asset을 실제 파일로 생성합니다.

#### 후보

- 이미지: OpenAI Image API, Stable Diffusion, ComfyUI
- TTS: ElevenLabs, OpenAI TTS, edge-tts

#### 주의

- API key 코드에 저장 금지
- 테스트에서 실제 외부 API 호출 금지
- 생성 실패/부분 실패 처리

---

### Phase 7. Timeline JSON + RenderJob + MP4

**목표:** 실제 쇼츠 MP4 생성 MVP를 만듭니다.

#### 구성

- backend TimelineBuilder
- RenderJobManager
- Remotion 또는 FFmpeg renderer
- MP4 download endpoint
- render status UI

#### 렌더링 상태

```text
pending
processing
completed
failed
```

---

### Phase 8. 카드뉴스 확장

**목표:** `output_format=instagram_card_news`를 추가합니다.

#### 구조

- CardNewsPlannerAgent
- SlideCopyAgent
- CardDesignDirectionAgent
- CarouselCaptionAgent

---

### Phase 9. 롱폼/릴스/업로드 자동화

후순위 확장입니다.

- longform script generation
- instagram reels
- YouTube upload
- Instagram upload
- team collaboration
- credit/payment

---

## 7. UI 리디자인 상세 플랜

### 7.0 UI 레퍼런스 파일

다크모드 UI 구현 전, 다음 이미지를 먼저 확인한다.

```text
docs/assets/ui-reference/shortsflow-dark-dashboard-and-editor-reference.png
```

사용 기준:

- 왼쪽 영역의 Dashboard는 SaaS형 홈/대시보드 레이아웃 참고
- 오른쪽 영역의 Project Detail / Scene Editor는 production studio형 편집 화면 참고
- 전체 톤은 dark navy/black 기반
- 포인트 컬러는 violet, blue, cyan 계열
- 카드 UI는 얇은 border, 약한 glow, 충분한 padding 사용
- 실제 구현에서는 현재 연결 가능한 기능만 활성화하고, 미구현 기능은 disabled/mock/coming soon으로 표시

### 7.1 Home / Dashboard

**스타일:** 2번째 SaaS dashboard reference의 다크모드 버전

#### 목적

사용자가 현재 프로젝트 현황과 빠른 생성 진입점을 보는 화면입니다.

#### 표시 항목

- 환영 문구
- search bar
- 프로젝트 summary cards
  - 전체 프로젝트
  - draft
  - 검토 필요
  - 총 scene 수
  - 최근 생성 결과
- 최근 프로젝트
- 빠른 만들기
  - AI 아이디어 생성
  - 새 프로젝트 만들기
  - 템플릿으로 시작
  - 주제 분석하기
- 검토 및 할 일
- 콘텐츠 기획 개요
- 트렌드 키워드

#### 지금 연결 가능한 기능

- 새 프로젝트 생성 폼으로 이동
- AI 기획 생성
- JSON 다운로드
- 현재 결과 preview

#### 아직 mock 처리할 기능

- 프로젝트 목록
- 크레딧 사용량
- 최근 활동
- 통계 그래프
- 템플릿
- 팀/프로필

---

### 7.2 Project Detail / Scene Editor

**스타일:** 3번째 production studio/editor reference의 다크모드 버전

#### 목적

한 프로젝트의 장면을 검토하고, 나중에는 수정/저장/렌더링으로 이어지는 작업 화면입니다.

#### 레이아웃

```text
Project Detail
├── Left: Scene Timeline List
│   ├── scene thumbnail
│   ├── scene_id
│   ├── scene_purpose
│   ├── duration
│   └── status badge
├── Center: Scene Editor
│   ├── Script
│   ├── Subtitle
│   ├── Visual
│   ├── Sourcing
│   ├── Editing
│   └── Safety
└── Right: Review & Export Panel
    ├── Project summary
    ├── Preview image/video placeholder
    ├── Safety checklist
    ├── Risk summary
    ├── Recommended revisions
    └── Export buttons
```

#### 지금 연결 가능한 기능

- scene list 표시
- scene별 상세 표시
- generated_image_prompt 표시
- visual sourcing 표시
- safety review 표시
- JSON 다운로드

#### 아직 mock 처리할 기능

- preview video
- image upload
- TTS 미리듣기
- save draft
- render MP4
- human reviewer
- team comment

---

## 8. 구현 시 금지할 것

다음은 ShortsFlow dark UI redesign 단계에서 하면 안 됩니다.

- backend domain/application 변경
- API response 구조 변경
- DB 추가
- 로그인 추가
- 결제/크레딧 실제 구현
- 이미지 생성 API 추가
- TTS API 추가
- MP4 renderer 추가
- YouTube/Instagram upload 추가
- 기존 static `frontend/app` 삭제
- real OpenAI API 테스트 호출
- API key 코드/문서에 기록

---

## 9. 다음 Codex 실행 프롬프트

아래 프롬프트를 Codex에 넣으면 됩니다.

```txt
frontend/web을 ShortsFlow 다크모드 SaaS UI로 리디자인해줘.

목표:
- 기존 static frontend/app은 삭제하거나 망가뜨리지 않는다.
- backend API 구조는 바꾸지 않는다.
- 이미지 생성, TTS, MP4 렌더링, DB, 로그인, 결제 기능은 추가하지 않는다.
- 현재 frontend/web의 생성 기능, 결과 preview, safety review 표시, scene card 표시, JSON 다운로드 기능은 유지한다.
- 브랜드명을 ShortsFlow로 변경한다.
- subtitle은 AI Shorts Planning Studio로 표시한다.
- 전체 UI를 다크모드 기반의 전문 SaaS 스타일로 변경한다.

디자인 방향:
- 먼저 docs/assets/ui-reference/shortsflow-dark-dashboard-and-editor-reference.png 이미지를 확인하고 이 이미지를 UI 레퍼런스로 삼는다.
- 대시보드는 레퍼런스 이미지의 SaaS dashboard 스타일을 따른다.
- 프로젝트 상세/장면 편집은 레퍼런스 이미지의 production studio/editor 스타일을 따른다.
- 전체 UI는 다크모드 기반으로 구현한다.
- 레퍼런스 이미지는 방향성 참고용이다. 이미지 안의 임시 텍스트, 숫자, 썸네일, 사용자 정보는 그대로 복사하지 않는다.
- 현재 단계에서는 route를 과하게 늘리지 말고, 기존 page 구조 안에서 dashboard-like shell과 project detail/editor 영역을 구성한다.
- 좌측 sidebar를 추가한다.
- 상단 topbar를 추가한다.
- 메인 영역은 카드 기반으로 구성한다.
- 보라/블루/시안 계열 그라데이션을 포인트 컬러로 사용한다.
- safety_status, required_human_review, scene count, estimated duration은 summary card로 보여준다.
- scene card는 어두운 production studio 카드형 디자인으로 정리한다.
- generated_image_prompt, asset_usage_note, risk lists는 가독성 좋게 표시한다.
- JSON 다운로드 버튼은 상단 action button으로 배치한다.

브랜드/문구:
- 서비스명: ShortsFlow
- subtitle: AI Shorts Planning Studio
- 메인 카피: Plan better. Create faster. Grow bigger.
- CTA:
  - 새 프로젝트
  - AI 기획 생성
  - JSON 다운로드
  - 내보내기

현재 실제 연결할 기능:
- 주제 입력
- AI 기획 생성
- 결과 summary 표시
- safety review 표시
- scene detail 표시
- visual/sourcing/editing 표시
- JSON 다운로드

mock 또는 disabled로 둘 기능:
- 프로젝트 목록
- 크레딧
- 최근 활동
- 팀 협업
- 이미지 생성
- TTS
- MP4 렌더링
- 업로드 자동화
- 결제

수정 범위:
- frontend/web/app/page.tsx
- frontend/web/app/layout.tsx
- frontend/web/app/globals.css
- frontend/web/components/*
- 필요하면 frontend/web/lib/types.ts는 타입 보완만 가능
- README.md 또는 docs/HANDOFF.md에는 실행 방법 또는 UI 상태만 최소 반영

주의:
- backend 코드 변경 금지
- API response 구조 변경 금지
- 기존 pytest 깨지면 안 됨
- 기존 Next.js build/lint/typecheck 깨지면 안 됨
- npm run build 통과
- npm run lint 통과
- npm run typecheck 통과
- uv run --project . --with pytest pytest -q 통과
- 변경 파일과 이유를 설명해줘
```

---

## 10. 레퍼런스 이미지 추가 방법

레퍼런스 이미지를 repo에 추가할 때는 아래 경로를 사용한다.

```powershell
mkdir docs\assets\ui-reference
copy "<다운로드한 이미지 파일 경로>" docs\assets\ui-reference\shortsflow-dark-dashboard-and-editor-reference.png
```

Git에 포함할 파일:

```powershell
git add docs/assets/ui-reference/shortsflow-dark-dashboard-and-editor-reference.png
```

커밋 메시지 예시:

```bash
git commit -m "Add ShortsFlow UI reference image"
```

주의:

- 이 이미지는 디자인 레퍼런스이므로 기능 구현 코드에 import하지 않는다.
- README나 PRODUCT_PLAN에서만 참조한다.
- 이미지 파일이 너무 커지면 추후 `docs/assets/ui-reference/README.md`에 외부 링크 방식으로 전환할 수 있다.

---

## 11. 검증 명령어

### Backend / Python

```powershell
uv run --project . --with pytest pytest -q
```

### Frontend / Next.js

```powershell
cd frontend/web
npm.cmd run build
npm.cmd run lint
npm.cmd run typecheck
npm.cmd audit
```

### Manual run

```powershell
cd C:\projects\issue-turi-ai
uv run --project . python -m backend.src.presentation.http.server
```

```powershell
cd C:\projects\issue-turi-ai\frontend\web
npm.cmd run dev
```

브라우저:

```text
http://localhost:3000
```

---

## 12. 추천 커밋 메시지

```bash
git commit -m "Update product roadmap for ShortsFlow UI redesign"
```

UI 리디자인 구현 후:

```bash
git commit -m "Redesign Next.js frontend with ShortsFlow dark UI"
```

---

## 13. 최종 우선순위

현재 기준 다음 작업 순서는 다음이 가장 안전합니다.

```text
1. 이 문서 저장 및 PRODUCT_PLAN/ROADMAP 업데이트
2. ShortsFlow dark UI redesign
3. Timeline builder
4. DB persistence/project management
5. Scene editing save flow
6. fake image/TTS/render provider interfaces
7. real image/TTS provider
8. MP4 renderer/download
9. card news
10. longform
```

---

## 14. 요약

기존 플랜은 전체 방향은 맞지만, 현재 구현 상태를 반영하지 못합니다.  
이제 프로젝트는 “쇼츠 기획서 생성기”를 넘어서 **ShortsFlow: AI Shorts Planning Studio**로 재정의하는 것이 좋습니다.

지금 해야 할 가장 안전한 다음 작업은 다음입니다.

```text
ShortsFlow dark mode UI redesign
```

단, 이번 단계에서는 실제 기능 추가가 아니라 **현재 가능한 기능을 더 전문적인 SaaS UI로 보여주는 것**에 집중합니다.

