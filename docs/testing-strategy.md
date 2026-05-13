# 테스트 전략

## 현재 테스트

표준 라이브러리 `unittest`를 사용한다. 외부 API와 실제 렌더링은 호출하지 않는다.

검증 범위:

- domain model validation
- fake agent 기반 shorts pipeline
- safety review
- in-memory project service
- presentation API adapter
- `main.py` demo payload

실행:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 다음 테스트

- SQLite repository 교체 가능성
- JSON parsing/validation 실패
- TimelineBuilder 세부 출력
- renderer job 상태 전이
- frontend interaction
