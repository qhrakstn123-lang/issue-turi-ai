# 아키텍처

## 계층

- `domain`: 핵심 모델과 규칙. 외부 기술을 모른다.
- `application`: agent, pipeline, service를 조립한다.
- `infrastructure`: repository, LLM, TTS, 이미지, 렌더링, 저장소 구현체를 둔다.
- `presentation`: API 어댑터를 둔다.
- `frontend`: 사용자가 입력하고 결과를 보는 화면을 둔다.

## 현재 구현

- 도메인 모델: `backend/src/domain/models.py`
- fake agent: `backend/src/application/agents/fake_agents.py`
- 쇼츠 파이프라인: `backend/src/application/pipelines/shorts_generation.py`
- 프로젝트 서비스: `backend/src/application/services/project_service.py`
- 인메모리 저장소: `backend/src/infrastructure/database/memory_repository.py`
- 프레임워크 독립 API 어댑터: `backend/src/presentation/http/api.py`

## 의존 방향

`presentation -> application -> domain`을 유지한다. infrastructure는 application이 요구하는 저장소/provider 역할을 구현한다.
