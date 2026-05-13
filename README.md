# 이슈털이 AI 콘텐츠 제작 서비스 MVP

이 저장소는 이슈/썰 쇼츠 제작을 위한 AI 편집 지시서 생성기 MVP입니다.

현재 구현된 범위:

- 도메인 모델
- fake agent 기반 쇼츠 생성 파이프라인
- 프로젝트 생성/저장/수정 서비스
- 프레임워크 독립 JSON API 어댑터
- 데모 실행 진입점
- 계층별 unittest

## 실행

```powershell
.\.venv\Scripts\python.exe main.py
```

브라우저 UI와 API 서버:

```powershell
.\.venv\Scripts\python.exe main.py serve 8000
```

열기: http://127.0.0.1:8000

## 테스트

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 다음 단계

1. HTTP 서버 또는 FastAPI 어댑터 연결
2. 간단한 프론트엔드 화면 구현
3. SQLite 저장소 구현
4. 실제 LLM provider와 prompt loader 연결
5. TimelineBuilder, TTS, 이미지 생성, 렌더링 MVP 확장
