# 프로젝트 구조 가이드

작성일: 2026-05-13

이 문서는 새 프로젝트를 시작할 때 참고하기 위한 기본 구조 가이드입니다.
목표는 코드를 처음부터 완벽하게 나누는 것이 아니라, 기능이 커져도 어디에 무엇을 둬야 하는지 헷갈리지 않게 기준을 잡는 것입니다.

## 1. 기본 원칙

프로젝트 구조를 잡을 때는 먼저 역할을 나눕니다.

```text
domain          핵심 개념과 규칙
application     실제 기능 흐름
infrastructure  DB, 외부 API, 파일, AI 모델 같은 기술 연결
presentation    HTTP API, CLI, worker 같은 외부 입구
frontend        사용자 화면
docs            사람이 읽는 설계와 설명
tests           동작을 검증하는 테스트
```

가장 중요한 기준은 의존 방향입니다.

```text
presentation
    ↓
application
    ↓
domain

infrastructure는 application/domain이 필요로 하는 인터페이스를 실제 기술로 구현합니다.
```

`domain`은 가장 안쪽 핵심입니다. 그래서 DB, FastAPI, React, OpenAI 같은 바깥 기술을 직접 몰라도 되게 만드는 것이 좋습니다.

## 2. 추천 디렉터리 구조

백엔드와 프론트엔드를 함께 두는 프로젝트라면 아래 구조를 기본값으로 생각하면 좋습니다.

```text
project/
  backend/
    src/
      domain/
      application/
      infrastructure/
      presentation/
      main.py
    tests/
    pyproject.toml
    README.md

  frontend/
    app/
    README.md

  docs/
  README.md
```

작은 프로젝트라면 처음부터 모든 폴더를 만들 필요는 없습니다.
하지만 기능이 커질 가능성이 있으면 위 구조를 미리 잡아두는 편이 나중에 덜 헷갈립니다.

## 3. 각 계층의 역할

### domain

서비스의 핵심 개념을 둡니다.

예시:

```text
Pet
PetRecord
Schedule
Reminder
User
CareSuggestion
```

이 계층에는 가능하면 외부 기술 의존성을 넣지 않습니다.

좋은 방향:

```python
class PetRecord:
    pet_id: str
    category: str
    content: str
```

피하고 싶은 방향:

```python
class PetRecord:
    def save(self):
        sqlite3.connect("app.db")
```

도메인 모델이 직접 DB를 알게 되면 나중에 저장 방식을 바꾸기 어려워집니다.

### application

사용자가 실제로 하려는 행동, 즉 유스케이스와 흐름을 둡니다.

예시:

```text
기록 저장하기
음성 기록을 텍스트로 바꾸고 구조화하기
최근 기록을 분석해서 위험 신호 찾기
돌봄 추천 만들기
리마인더 계획하기
```

AI 프로젝트에서는 `agent`, `pipeline`, `service`, `use_case` 같은 이름을 많이 씁니다.

```text
application/
  agents/
    record_structuring_agent.py
    risk_detection_agent.py

  pipelines/
    pet_log_graph.py

  services/
    pet_record_service.py
```

`application`은 여러 객체를 조립해서 "기능 하나"를 완성하는 곳입니다.

### infrastructure

실제 외부 기술과 연결되는 코드를 둡니다.

예시:

```text
DB 연결
repository 구현체
OpenAI API client
Whisper speech-to-text provider
파일 저장소
이메일/SMS 발송
외부 병원 API
```

```text
infrastructure/
  database.py
  repositories/
    record_repository.py
  speech/
    speech_to_text.py
  llm/
    openai_client.py
```

핵심은 외부 기술을 이 계층에 가둬두는 것입니다.
그래야 나중에 SQLite에서 PostgreSQL로 바꾸거나, Whisper에서 다른 STT로 바꿔도 application 전체가 흔들리지 않습니다.

### presentation

외부 요청이 들어오는 입구입니다.

웹 백엔드에서는 보통 HTTP route/controller가 여기에 들어갑니다.

```text
presentation/
  http/
    pet_log_routes.py
    profile_routes.py
```

이 계층은 request를 받고, application 계층을 호출하고, response를 반환합니다.
비즈니스 로직을 많이 넣지 않는 것이 좋습니다.

### frontend

사용자 화면과 클라이언트 로직을 둡니다.

Next.js 기준 예시:

```text
frontend/app/web/src/
  app/
  components/
  lib/
    api-client.ts
  types/
```

프론트엔드에서도 비슷한 기준을 적용할 수 있습니다.

```text
app/pages       화면 단위
components      재사용 UI
lib/api-client  백엔드 호출
lib/utils       공통 유틸
types           타입 정의
```

## 4. 새 기능을 만들 때 생각 순서

기능을 추가할 때는 아래 질문 순서로 생각하면 좋습니다.

```text
1. 이 기능의 핵심 데이터는 무엇인가?
   → domain

2. 사용자가 하려는 행동은 무엇인가?
   → application

3. DB나 외부 API 같은 기술 연결이 필요한가?
   → infrastructure

4. API로 어떻게 받을 것인가?
   → presentation

5. 화면에서는 어떻게 호출하고 보여줄 것인가?
   → frontend

6. 어떤 동작을 테스트해야 안심할 수 있는가?
   → tests
```

예를 들어 "음성으로 반려동물 기록 저장하기" 기능을 만든다면:

```text
domain
  PetRecord, StructuredRecordCandidate

application
  SpeechRecordPipeline
  RecordStructuringAgent

infrastructure
  SpeechToTextProvider
  RecordRepository

presentation
  POST /records/voice

frontend
  녹음 버튼
  업로드 API 호출
  저장 후보 확인 UI

tests
  음성 입력이 텍스트로 변환되는지
  구조화 후보가 만들어지는지
  확인이 필요한 경우 바로 저장하지 않는지
```

## 5. AI 프로젝트에서의 추천 구조

AI 기능이 들어가는 프로젝트는 역할을 더 명확히 나누면 좋습니다.

```text
agent
  AI에게 특정 판단이나 생성을 시키는 단위

pipeline
  여러 agent, repository, service를 연결하는 전체 흐름

provider/client
  실제 외부 AI API나 모델을 호출하는 기술 연결

prompt
  모델에게 전달하는 지시문과 출력 형식
```

예시:

```text
backend/src/application/
  agents/
    record_structuring_agent.py
    context_analysis_agent.py
    risk_detection_agent.py

  pipelines/
    pet_log_graph.py

backend/src/infrastructure/
  llm/
    openai_client.py
    prompts.py

  speech/
    speech_to_text.py
```

AI 기능은 실패 가능성이 있으므로 아래를 같이 고민합니다.

```text
모델 응답이 비어 있으면 어떻게 할지
잘못된 JSON이 오면 어떻게 할지
위험한 내용은 바로 저장하지 않고 확인받을지
사용자 입력 원문과 AI 요약본을 둘 다 저장할지
AI 결과를 테스트에서 어떻게 고정할지
```

## 6. 파일을 나누는 기준

처음부터 너무 잘게 쪼갤 필요는 없습니다.
다만 아래 신호가 보이면 분리를 고민합니다.

```text
한 파일이 300~500줄을 넘는다
하나의 클래스가 여러 책임을 가진다
테스트하기 어렵다
같은 로직이 여러 곳에 반복된다
외부 기술을 바꾸기 어렵다
이름이 너무 추상적이라 역할이 잘 안 보인다
```

예를 들어 pipeline 파일이 너무 커지면 이렇게 나눌 수 있습니다.

```text
application/pipelines/
  pet_log_graph.py
  pet_log_nodes.py
  pet_log_routing.py
```

또는 기능 단위로 나눌 수도 있습니다.

```text
application/services/
  record_service.py
  context_service.py
  recommendation_service.py
```

중요한 것은 "파일 수를 늘리는 것"이 아니라 "각 파일의 역할을 설명할 수 있게 만드는 것"입니다.

## 7. 주석을 다는 기준

공부할 때는 주석을 많이 달아도 괜찮습니다.
직접 설명을 쓰면서 구조를 이해하는 과정 자체가 도움이 됩니다.

다만 협업용 코드에서는 보통 아래 기준을 씁니다.

좋은 주석:

```python
# ai_preview는 저장 없이 후보와 분석 결과만 보여주는 모드다.
if input.source == "ai_preview":
    return "confirm"
```

줄여도 되는 주석:

```python
# 로그를 남기기 위한 기본 모듈
import logging
```

현업 코드에서는 "무엇을 하는지"보다 "왜 이렇게 하는지"를 주석으로 남기는 경우가 많습니다.
학습용 주석은 따로 남겨도 좋고, 최종 정리 단계에서 README나 docs로 옮겨도 좋습니다.

## 8. 테스트 전략

테스트는 계층별로 목적이 다릅니다.

```text
domain test
  핵심 규칙이 맞는지 확인

application test
  유스케이스 흐름이 맞는지 확인

infrastructure test
  DB 저장, 외부 연동 wrapper가 맞는지 확인

presentation test
  API 요청/응답이 맞는지 확인

frontend test
  사용자 행동과 화면 상태가 맞는지 확인
```

AI 기능은 실제 모델을 매번 호출하지 말고, 테스트에서는 fake agent나 mock provider를 쓰는 편이 좋습니다.

```python
class FakeRecordStructuringAgent:
    def structure(self, input):
        return fixed_record_batch
```

그래야 테스트가 빠르고 안정적입니다.

## 9. 프로젝트 시작 체크리스트

새 프로젝트를 시작할 때 아래 순서로 정리합니다.

```text
1. 이 서비스가 해결하려는 문제를 한 문장으로 쓴다.
2. 핵심 사용자 행동을 3~5개 적는다.
3. 핵심 도메인 모델을 적는다.
4. 백엔드 계층 구조를 잡는다.
5. 프론트엔드 화면 구조를 잡는다.
6. 외부 기술 의존성을 적는다.
7. 가장 먼저 만들 MVP 흐름 하나를 정한다.
8. 테스트할 핵심 시나리오를 적는다.
9. README와 docs에 구조 설명을 남긴다.
```

## 10. 한 줄 요약

앞으로 프로젝트 구조를 잡을 때는 아래 문장을 기준으로 삼으면 됩니다.

```text
domain에는 핵심 개념,
application에는 기능 흐름,
infrastructure에는 외부 기술,
presentation에는 외부 입구,
frontend에는 사용자 화면,
docs에는 사람이 이해할 설명,
tests에는 안심할 수 있는 검증을 둔다.
```

