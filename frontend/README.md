# Frontend

현재는 백엔드 MVP를 먼저 구현했다.

다음 단계에서는 이 폴더에 Next.js 또는 정적 MVP UI를 두고 아래 흐름을 연결한다.

1. 주제, 타깃, 톤, 영상 길이 입력
2. `POST /api/projects`
3. `POST /api/generate/shorts-plan`
4. 장면별 결과 미리보기
5. `PATCH /api/projects/{project_id}`로 장면 수정
