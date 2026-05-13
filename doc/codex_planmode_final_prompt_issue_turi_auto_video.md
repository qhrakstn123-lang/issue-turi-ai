# Codex 플랜모드 최종 프롬프트
## 이슈털이 AI 콘텐츠 제작 서비스: 쇼츠 자동 MP4 생성 + 카드뉴스 확장 + 롱폼 확장

아래 내용을 VS코드 Codex 플랜모드에 그대로 붙여넣어 사용하세요.

---

```txt
너는 AI 영상 제작 SaaS를 설계하는 시니어 풀스택 개발자이자 AI 에이전트 아키텍트야.

나는 유튜브 쇼츠, 롱폼 영상, 인스타 카드뉴스 콘텐츠 제작을 도와주는 AI 웹서비스를 만들고 싶다.

최종 목표:
사용자가 주제만 입력하면,
AI가 이슈/썰 쇼츠용 대본, 장면 구성, 자막, 이미지/GIF/짧은 클립/텍스트 화면, TTS 음성, 효과음, 모션, 전환을 구성하고,
최종적으로 유튜브 쇼츠용 MP4 영상 파일까지 자동 생성해주는 서비스.

중요:
- 지금은 절대 코드를 작성하지 마.
- 실제 파일도 생성하지 마.
- 먼저 전체 서비스 플랜, 아키텍처, MVP 범위, 개발 순서만 작성해줘.
- 내가 승인하면 그때 1단계부터 구현을 시작한다.
- MVP와 나중에 확장할 기능을 명확히 구분해줘.
- 처음부터 모든 기능을 한 번에 만들지 말고, 실제 구현 가능한 단계로 쪼개줘.
- 쇼츠 자동 MP4 생성이 최종 목표이지만, 처음에는 안정적인 단계별 구조를 먼저 잡아줘.

==================================================
1. 서비스 한 문장 정의
==================================================

내가 만들고 싶은 서비스는 다음과 같다.

“이슈/썰 콘텐츠 제작자가 주제만 입력하면, AI가 유튜브 쇼츠용 대본, 장면 구성, 자막, 이미지/영상 프롬프트, TTS, 모션, 효과음, 전환, 타임라인을 만들고, 최종적으로 MP4 쇼츠 영상 파일까지 자동 생성해주는 AI 콘텐츠 제작 웹서비스”

처음 목표:
- 이슈털이 쇼츠 제작 지시서 생성기
- 그리고 바로 다음 단계에서 자동 영상 생성 MVP로 확장

최종 목표:
- 쇼츠 자동 MP4 생성
- 인스타 카드뉴스 자동 기획/이미지 생성
- 인스타 릴스 확장
- 롱폼 영상 확장
- 나중에는 유튜브/인스타 업로드 자동화까지 고려

==================================================
2. 내가 운영 중인 채널과 참고 채널
==================================================

내가 실제로 운영 중인 유튜브 채널:
- 채널명: 이슈털이
- 채널 주소: https://www.youtube.com/@issueyo

이 채널은 내가 직접 하나하나 작업한 쇼츠가 올라가 있는 채널이다.
현재 문제는 대본이나 주제보다 편집 완성도가 부족하다는 점이다.
따라서 이 서비스는 내 채널 “이슈털이”의 쇼츠 제작 완성도를 높이고, 최종적으로 자동 MP4 영상 생성까지 가능하게 만드는 방향으로 설계해줘.

참고하고 싶은 유튜브 쇼츠 채널:
- 뇌전구
- 걍석주

참고하고 싶은 인스타 카드뉴스 계정:
- https://www.instagram.com/izitmag_/
- https://www.instagram.com/issuemagazines/
- https://www.instagram.com/yeodam_everything/

중요:
참고 채널과 계정의 콘텐츠를 그대로 복제하지 마.
참고할 것은 콘텐츠 자체가 아니라 아래의 일반화 가능한 제작 문법이다.

참고할 요소:
1. 첫 1~3초 후킹 방식
2. 짧고 강한 자막 리듬
3. 컷 전환 속도
4. 장면당 평균 길이
5. 이미지/GIF/짧은 클립/텍스트 화면 사용 방식
6. 자막 강조 방식
7. 줌인, 줌아웃, 좌우 이동, 흔들림, 텍스트 팝업 같은 모션 사용 방식
8. 효과음 타이밍
9. 시청자가 끝까지 보게 만드는 정보 배치 방식
10. 댓글을 유도하는 마무리 방식
11. 카드뉴스의 표지, 본문 카드, 요약 카드, CTA 카드 구성 방식

피해야 할 것:
- 참고 채널의 대사, 자막, 구성, 썸네일, 고유 표현을 그대로 복사하는 것
- 남의 유튜브 영상이나 방송 자료를 무단으로 가져오는 구조
- 확인되지 않은 루머를 사실처럼 말하는 것
- 특정 인물을 과하게 비난하는 표현
- 저작권 문제가 생길 수 있는 이미지/영상/음원 사용
- 과한 어그로만 있는 콘텐츠

==================================================
3. 이슈털이 쇼츠 스타일 목표
==================================================

이슈털이 채널용 기본 쇼츠 스타일은 아래와 같다.

영상 길이:
- 40~60초

비율:
- 9:16 세로형 쇼츠
- 1080x1920 해상도 기준

장면 수:
- 8~12개

장면당 길이:
- 2~5초
- 실제 자동 렌더링 단계에서는 TTS 오디오 길이에 맞춰 장면 길이를 조정한다.

전체 구성:
1. 강한 첫 문장
2. 빠른 상황 설명
3. 사람들 반응
4. 핵심 쟁점
5. 반전 또는 결론
6. 댓글 유도

자막 스타일:
- 짧고 강하게
- 한 문장 8~15자 중심
- 핵심 단어는 크게 강조
- 말 자막과 강조 자막을 구분
- 장면마다 시선이 가는 문구를 배치
- 자동 렌더링 단계에서는 자막이 영상에 표시되어야 한다.

화면 스타일:
- 꼭 짧은 영상 클립이 들어가지 않아도 된다.
- 이미지 1장만 있어도 zoom_in, pan_left, pan_right, shake, text_pop, 효과음으로 관심을 끌 수 있어야 한다.
- 이미지, GIF, 짧은 클립, 텍스트 화면, 아이콘/도형 화면, 단순 배경 + 자막 화면을 유연하게 추천한다.
- 자동 영상 생성 MVP에서는 우선 이미지 1장 + TTS + 자막 + 간단한 모션 중심으로 시작한다.
- 이후 GIF, 스톡 영상, 짧은 클립을 확장한다.

효과음 예시:
- whoosh: 화면 전환
- pop: 자막 등장
- impact: 충격적인 내용
- click: 정보 전환
- alarm: 논란/위험 느낌
- suspense_rise: 반전 전 긴장감
- hit: 결론 강조

==================================================
4. 최종 자동 영상 생성 목표
==================================================

최종적으로는 사용자가 주제만 입력하면 유튜브 쇼츠용 MP4 영상 파일까지 자동 생성되기를 원한다.

자동 영상 생성 MVP 목표:
- 9:16 세로형 쇼츠 영상 생성
- 1080x1920 해상도 기준
- 40~60초 길이
- 8~10개 장면
- 각 장면은 이미지 1장 + TTS 음성 + 자막 + 간단한 모션으로 구성
- 모션은 zoom_in, zoom_out, pan_left, pan_right, shake 정도부터 시작
- 전환은 quick_cut, fade 정도부터 시작
- 효과음은 whoosh, pop, impact 정도부터 시작
- 최종 결과물은 MP4 파일로 다운로드할 수 있어야 한다.

처음 자동 영상 생성 버전은 고정 템플릿 기반으로 만든다.
자유 편집기처럼 만들지 않는다.

자동 영상 생성 파이프라인:
1. TopicInput
2. ScriptGeneration
3. SceneGeneration
4. VisualPromptGeneration
5. ImageGeneration
6. TTSGeneration
7. SubtitleGeneration
8. TimelineBuilder
9. VideoRenderer
10. MP4Download

렌더링 구조:
- Remotion 또는 FFmpeg 기반으로 설계한다.
- 웹서비스와 연결하기 쉬운 구조라면 Remotion을 우선 고려한다.
- FFmpeg는 나중에 오디오 합성, 자막 굽기, 포맷 변환, 압축 등에 활용할 수 있게 설계한다.
- 렌더링 작업은 시간이 걸릴 수 있으므로 RenderJobManager를 둔다.
- 렌더링 상태는 pending, processing, completed, failed 등으로 관리한다.

자동 영상 생성에서 고려할 실패 상황:
- 이미지 생성 실패
- TTS 생성 실패
- 자막 생성 실패
- 효과음 파일 누락
- 렌더링 실패
- 저장소 업로드 실패
- MP4 다운로드 링크 생성 실패
- 렌더링 시간이 너무 길어지는 경우
- 일부 장면만 생성되고 중간에 실패하는 경우

==================================================
5. 주제 소싱 전략
==================================================

이 서비스는 나중에 주제 추천 기능까지 확장할 수 있어야 한다.
하지만 처음 MVP에서는 사용자가 직접 주제를 입력하는 방식으로 시작한다.

주제 소싱 단계:

1단계 MVP:
- 사용자가 직접 주제를 입력한다.
- AI는 입력된 주제를 바탕으로 쇼츠 대본과 편집 지시서 또는 자동 영상 생성용 데이터를 만든다.

1.5단계:
- 사용자가 뉴스 링크, 커뮤니티 글 요약, 유튜브 영상 링크, 인스타 게시물 링크, 메모를 입력할 수 있게 한다.
- AI는 사용자가 넣은 자료를 분석해서 쇼츠화 가능한 관점을 추천한다.

2단계:
- 오늘의 주제 후보 추천 기능을 추가한다.
- 사용자가 여러 후보 중 하나를 선택하면 대본 생성으로 넘어간다.

3단계:
- TrendCollectorAgent를 추가한다.
- 구글 트렌드, 네이버 검색 트렌드, 유튜브 차트, 뉴스 RSS, SNS 반응, 커뮤니티 반응 등을 기반으로 주제 후보를 수집한다.
- TopicScoringAgent가 쇼츠 적합도를 점수화한다.
- SafetyReviewAgent가 루머, 저작권, 명예훼손, 민감 표현 위험을 검토한다.
- 최종적으로 사용자가 승인한 주제만 대본 생성으로 넘어간다.

주제 점수화 기준:
- 후킹 가능성
- 40~60초 안에 설명 가능한가
- 이미지/GIF/텍스트 화면으로 시각화 가능한가
- 댓글 유도 가능성이 있는가
- 최근 검색량이나 반응이 증가하고 있는가
- 루머, 비난, 저작권 위험이 낮은가
- 이슈털이 채널 톤에 맞는가

좋은 주제:
- 사람들이 이미 궁금해하는 이슈
- 반응이 갈리는 사건
- “알고 보니 이유가 있었음” 구조가 가능한 주제
- 전후 관계를 1분 안에 설명할 수 있는 주제
- 이미지 몇 장과 자막만으로도 설명 가능한 주제
- 마지막에 “너는 어떻게 생각함?”으로 댓글 유도 가능한 주제

피해야 할 주제:
- 사실 확인이 어려운 루머
- 특정 개인을 공격하는 내용
- 너무 정치적이거나 법적 리스크가 큰 내용
- 맥락 없이 자극적인 사건
- 영상/사진 저작권 의존도가 너무 높은 주제

==================================================
6. 인스타 카드뉴스 확장 방향
==================================================

인스타 카드뉴스는 처음 MVP의 핵심 기능으로 넣지 않는다.
처음 MVP는 쇼츠 제작 지시서와 자동 쇼츠 MP4 생성 구조에 집중한다.

다만 카드뉴스는 별도 서비스로 완전히 분리하지 말고,
같은 ContentProject에서 선택 가능한 output_format 중 하나로 설계한다.

output_format 예:
- youtube_shorts
- instagram_card_news
- instagram_reels
- longform_video

쇼츠와 카드뉴스의 공통 흐름:
- 주제 분석
- 핵심 메시지 정리
- 후킹 문장 생성
- 내용 순서 구성
- 시각 자료 추천
- 안전성 검토
- 최종 결과물 생성

차이점:
- 쇼츠는 scene/timeline 기반이다.
- 카드뉴스는 slide 기반이다.
- 쇼츠는 속도감, 자막, 효과음, 모션, 음성, 렌더링이 중요하다.
- 카드뉴스는 표지, 저장 가치, 짧은 문장, 디자인 방향, 공유/댓글 유도가 중요하다.

카드뉴스 생성 결과물에는 아래 항목이 포함되어야 한다.
- carousel_title
- cover_slide
- content_slides
- summary_slide
- cta_slide
- slide_title
- slide_body
- visual_asset_type
- image_prompt
- design_direction
- emphasis_text
- instagram_caption
- hashtags
- safety_note

카드뉴스용 에이전트:
1. CardNewsPlannerAgent
   - 주제를 카드뉴스 구조로 바꾼다.
   - 표지, 본문, 요약, CTA 슬라이드를 구성한다.

2. SlideCopyAgent
   - 카드별 제목과 짧은 본문을 작성한다.
   - 한 카드에 너무 많은 글자가 들어가지 않게 조절한다.

3. CardDesignDirectionAgent
   - 카드별 레이아웃, 이미지 위치, 강조 문구, 색감, 여백을 제안한다.

4. CarouselCaptionAgent
   - 인스타 게시글 본문, 해시태그, 댓글 유도 문구를 만든다.

개발 순서상 카드뉴스는 자동 쇼츠 MVP 이후 1.5단계 또는 2단계 확장 기능으로 고려한다.

==================================================
7. 프로젝트 구조 가이드 반영
==================================================

내가 업로드한 PROJECT_STRUCTURE_GUIDE.md의 구조를 참고해서 설계해줘.

기본 계층 구조:
- domain: 서비스의 핵심 개념과 규칙
- application: 실제 기능 흐름, use case, service, agent, pipeline
- infrastructure: DB, OpenAI, ElevenLabs, 이미지 생성 API, GIF/스톡 영상 검색, 영상 렌더링, 파일 저장소 같은 외부 기술 연결
- presentation: API route/controller
- frontend: 사용자 화면
- docs: 사람이 읽는 설계 문서
- tests: 동작을 검증하는 테스트

중요한 의존 방향:
- presentation → application → domain
- infrastructure는 application/domain이 필요로 하는 인터페이스를 실제 기술로 구현한다.
- domain은 DB, React, OpenAI, ElevenLabs, Remotion, FFmpeg 같은 외부 기술을 직접 몰라야 한다.

AI 프로젝트 구조:
- agent: AI에게 특정 판단이나 생성을 시키는 단위
- pipeline: 여러 agent, repository, service를 연결하는 전체 흐름
- provider/client: 실제 외부 AI API나 모델을 호출하는 기술 연결
- prompt: 모델에게 전달하는 지시문과 출력 형식

==================================================
8. 설계해야 할 AI 에이전트와 모듈
==================================================

다음 에이전트와 모듈을 고려해줘.

1. TopicAnalysisAgent
   - 사용자가 입력한 주제, 타깃, 분위기를 분석한다.
   - 쇼츠로 만들기 적합한 방향을 정리한다.

2. TrendCollectorAgent
   - 나중에 구글 트렌드, 네이버 검색 트렌드, 유튜브 차트, 뉴스, SNS, 커뮤니티 등에서 주제 후보를 수집한다.
   - MVP에서는 실제 구현하지 않고 확장 가능 구조만 설계한다.

3. TopicScoringAgent
   - 주제 후보의 쇼츠 적합도를 점수화한다.
   - 후킹 가능성, 설명 가능성, 시각화 가능성, 댓글 유도성, 위험도를 평가한다.

4. ReferenceStyleAnalysisAgent
   - 참고 채널의 스타일을 분석한다.
   - 단, 원본 콘텐츠를 복제하지 않고 편집 패턴만 일반화한다.
   - 후킹 방식, 자막 리듬, 컷 전환, 시각 자료 사용 방식, 효과음 타이밍, 정보 배치 방식을 템플릿화한다.

5. StyleTemplateAgent
   - 참고 채널/영상의 스타일을 그대로 복사하지 않고 일반화된 템플릿으로 변환한다.
   - 예: 이슈털이 기본형, 이슈 요약형, 썰 만화형, 정보 전달형, 논란 정리형, 댓글 반응형, 카드뉴스형 등

6. ScriptWriterAgent
   - 쇼츠용 대본을 생성한다.
   - 40초~1분 분량을 우선 기준으로 한다.
   - 말투는 딱딱하지 않고 썰을 푸는 느낌을 우선한다.
   - 나중에 롱폼 대본도 생성할 수 있게 확장 가능해야 한다.

7. StoryboardAgent
   - 대본을 장면 단위로 나눈다.
   - 각 장면의 목적, 화면 구성, 필요한 자막, 예상 길이를 정리한다.

8. VisualAssetSuggestionAgent
   - 각 장면에 적합한 시각 자료 유형을 추천한다.
   - 유형 예시: image, gif, short_clip, text_only, icon, background
   - 꼭 짧은 영상만 추천하지 않는다.
   - 이미지 한 장, GIF, 텍스트 화면, 아이콘 화면, 짧은 클립 중 장면에 맞는 것을 선택한다.

9. VisualPromptAgent
   - 각 장면에 맞는 이미지/영상 생성 프롬프트를 만든다.
   - Stable Diffusion, ComfyUI, OpenAI Image API, Runway 같은 도구로 확장 가능하게 설계한다.

10. ImageGenerationProvider
   - 이미지 프롬프트를 실제 이미지 파일로 변환한다.
   - MVP 자동 영상 생성 단계에서는 먼저 이미지만 생성하고, GIF/짧은 영상은 나중에 확장한다.

11. TTSScriptAgent
   - TTS로 읽기 좋은 문장으로 정리한다.
   - 장면별 TTS 또는 전체 내레이션 TTS 구조를 고려한다.

12. TTSProvider
   - ElevenLabs 같은 TTS API로 텍스트를 실제 오디오 파일로 변환한다.

13. SubtitleAgent
   - 화면 자막용 짧은 문장을 생성한다.
   - 말 자막과 강조 자막을 구분할 수 있게 설계한다.

14. EditingDirectionAgent
   - 장면별 편집 지시서를 만든다.
   - 줌인, 줌아웃, 좌우 이동, 상하 이동, 흔들림, 텍스트 팝업, 전환 효과를 추천한다.
   - 편집을 잘 못하는 사람도 그대로 따라 할 수 있게 작성한다.

15. SoundCueAgent
   - 장면 분위기에 맞는 효과음 힌트를 추천한다.
   - 예: whoosh, pop, impact, click, alarm, suspense_rise, hit

16. TimelineBuilder
   - 장면별 이미지, 음성, 자막, 모션, 전환, 효과음을 실제 렌더링 가능한 timeline JSON으로 변환한다.

17. VideoRenderer
   - Timeline 데이터를 기반으로 MP4를 생성한다.
   - Remotion 또는 FFmpeg 기반으로 설계한다.

18. RenderJobManager
   - 렌더링 작업 상태를 관리한다.
   - pending, processing, completed, failed 상태를 고려한다.

19. AssetStorage
   - 생성된 이미지, 음성, 효과음, 영상 파일을 저장한다.
   - 로컬 저장소, S3 호환 저장소, 클라우드 스토리지로 확장 가능하게 설계한다.

20. SafetyReviewAgent
   - 루머, 과장, 저작권 위험, 특정 인물 비난, 부정확한 정보 가능성을 점검한다.
   - 위험한 내용은 사용자 확인이 필요하도록 설계한다.

21. CardNewsPlannerAgent
   - 나중에 인스타 카드뉴스 구조를 생성한다.
   - 표지, 본문, 요약, CTA 슬라이드를 구성한다.

22. SlideCopyAgent
   - 카드뉴스의 카드별 제목과 본문을 작성한다.

23. CardDesignDirectionAgent
   - 카드뉴스의 디자인 방향을 제안한다.

24. CarouselCaptionAgent
   - 인스타 게시글 본문, 해시태그, 댓글 유도 문구를 만든다.

처음 MVP에서는 모든 에이전트를 완성하지 말고,
ScriptWriterAgent, StoryboardAgent, VisualAssetSuggestionAgent, SubtitleAgent, EditingDirectionAgent, SoundCueAgent 중심으로 시작하는 구조를 제안해줘.

자동 영상 생성 MVP에서는 추가로:
- ImageGenerationProvider
- TTSProvider
- TimelineBuilder
- VideoRenderer
- RenderJobManager
- AssetStorage

를 설계해줘.

==================================================
9. MVP 기능 범위
==================================================

MVP 1: 편집 지시서 MVP
- 주제 직접 입력
- 타깃 시청자 입력
- 영상 분위기 선택
- 참고 스타일 선택
- 이슈털이 기본 스타일 선택
- 쇼츠 대본 생성
- 장면별 컷 구성 생성
- 장면별 시각 자료 유형 추천
- 이미지/영상 프롬프트 생성
- TTS용 문장 생성
- 자막 초안 생성
- 강조 자막 생성
- 화면 모션 지시 생성
- 전환 효과 추천
- 효과음 힌트 추천
- 장면별 예상 길이 생성
- 장면별 편집 메모 생성
- 결과 미리보기
- 사용자가 대본/장면/자막/편집 지시를 수정할 수 있는 UI
- 생성 결과 저장

MVP 2: 자동 영상 생성 MVP
- MVP 1 결과를 기반으로 실제 이미지 생성
- TTS 음성 생성
- 자막 생성
- timeline JSON 생성
- Remotion 또는 FFmpeg 기반 MP4 렌더링
- 렌더링 상태 확인
- MP4 다운로드
- 렌더링 실패 시 에러 표시

처음 MVP에서 제외할 기능:
- 완전 자동 주제 수집
- 복잡한 GIF/스톡 영상 자동 삽입
- 고급 영상 편집기
- 유튜브 자동 업로드
- 인스타 자동 업로드
- 결제 기능
- 팀 협업 기능
- 복잡한 롱폼 자동 생성
- 참고 채널 영상 자동 다운로드
- 저작권 위험이 있는 방송/유튜브 자료 자동 수집

단, 나중에 위 기능들을 붙일 수 있게 확장 가능한 구조로 설계해줘.

==================================================
10. 핵심 사용자 흐름
==================================================

MVP 1 사용자 흐름:
1. 사용자가 새 콘텐츠 프로젝트를 만든다.
2. 사용자가 output_format으로 youtube_shorts를 선택한다.
3. 사용자가 주제, 타깃 시청자, 영상 길이, 분위기, 참고 스타일을 입력한다.
4. 사용자가 “이슈털이 기본형” 또는 다른 스타일 템플릿을 선택한다.
5. AI가 쇼츠 대본을 생성한다.
6. AI가 대본을 장면 단위로 나눈다.
7. AI가 각 장면별 시각 자료 유형을 추천한다.
8. AI가 각 장면별 이미지/영상 생성 프롬프트를 생성한다.
9. AI가 TTS용 문장과 자막용 문장을 생성한다.
10. AI가 강조 자막, 모션 지시, 전환 효과, 효과음 힌트를 생성한다.
11. SafetyReviewAgent가 루머/저작권/비난 위험을 검토한다.
12. 사용자가 결과를 미리보고 수정한다.
13. 사용자가 프로젝트를 저장한다.

MVP 2 사용자 흐름:
1. 사용자가 MVP 1에서 생성된 쇼츠 프로젝트를 선택한다.
2. 사용자가 “영상 생성하기”를 누른다.
3. 시스템이 장면별 이미지 파일을 생성한다.
4. 시스템이 TTS 오디오 파일을 생성한다.
5. 시스템이 자막과 강조 자막을 렌더링용 데이터로 변환한다.
6. TimelineBuilder가 timeline JSON을 생성한다.
7. VideoRenderer가 MP4 렌더링 작업을 시작한다.
8. RenderJobManager가 상태를 pending → processing → completed 또는 failed로 관리한다.
9. 렌더링이 완료되면 사용자가 MP4 파일을 다운로드한다.
10. 사용자는 필요하면 CapCut/Premiere/Vrew 등에서 후편집할 수 있다.

카드뉴스 확장 흐름:
1. 사용자가 기존 쇼츠 프로젝트 또는 새 주제를 선택한다.
2. output_format으로 instagram_card_news를 선택한다.
3. AI가 핵심 메시지를 카드뉴스 구조로 재배열한다.
4. 표지 카드, 본문 카드, 요약 카드, CTA 카드를 생성한다.
5. 카드별 문구, 이미지 프롬프트, 디자인 방향, 인스타 캡션, 해시태그를 생성한다.
6. 사용자가 수정 후 저장한다.

==================================================
11. 장면별 결과물 형식
==================================================

각 쇼츠 장면 결과물에는 아래 항목이 포함되어야 한다.

- scene_id
- scene_purpose
- narration
- tts_text
- subtitle
- emphasis_caption
- visual_asset_type
  예: image, gif, short_clip, text_only, icon, background
- visual_description
- generated_image_prompt
- generated_image_url
- gif_or_clip_suggestion
- stock_search_keywords
- motion_direction
  예: zoom_in, zoom_out, pan_left, pan_right, pan_up, pan_down, shake, text_pop, fade_in, fade_out
- transition
  예: quick_cut, swipe, zoom_cut, fade, glitch
- sound_effect_hint
  예: whoosh, pop, impact, click, alarm, suspense_rise, hit
- sound_effect_asset
- estimated_duration
- actual_duration
- editing_notes
- copyright_safety_note

예시:
장면 1
- 대사: “요즘 이 사건 때문에 커뮤니티가 완전 난리났음.”
- 자막: “커뮤니티 난리난 사건”
- 강조 자막: “완전 난리남”
- 시각 자료: 스마트폰 댓글 화면 느낌의 이미지
- 이미지 프롬프트: 어두운 배경의 스마트폰 화면, 빠르게 올라가는 댓글 UI, 한국 인터넷 커뮤니티 분위기, 쇼츠 배경용
- 모션: 천천히 zoom_in
- 효과음: whoosh + pop
- 전환: quick_cut
- 길이: 3초
- 편집 메모: “난리났음” 부분에서 자막을 크게 튀어나오게 강조

==================================================
12. 렌더링용 Timeline 형식
==================================================

자동 영상 생성을 위해 timeline JSON 구조를 설계해줘.

예시 구조:

{
  "project_id": "project_001",
  "output_format": "youtube_shorts",
  "aspect_ratio": "9:16",
  "resolution": "1080x1920",
  "fps": 30,
  "total_duration": 52.4,
  "audio_mix": {
    "background_music": null,
    "background_music_volume": 0.15,
    "narration_volume": 1.0,
    "sfx_volume": 0.7
  },
  "scenes": [
    {
      "scene_id": "scene_001",
      "start_time": 0,
      "end_time": 3.2,
      "duration": 3.2,
      "visual_asset": {
        "type": "image",
        "url": "/assets/images/scene_001.png"
      },
      "narration_audio": {
        "url": "/assets/audio/scene_001.mp3"
      },
      "subtitle": {
        "text": "커뮤니티 난리난 사건",
        "start_time": 0.2,
        "end_time": 2.8
      },
      "emphasis_caption": {
        "text": "완전 난리남",
        "start_time": 2.0,
        "end_time": 3.0
      },
      "motion": "zoom_in",
      "transition": "quick_cut",
      "sound_effect": {
        "type": "pop",
        "start_time": 2.0
      }
    }
  ]
}

TimelineBuilder는 장면 데이터를 이 구조로 변환해야 한다.
VideoRenderer는 이 timeline JSON을 기반으로 MP4를 생성해야 한다.

==================================================
13. 카드뉴스 결과물 형식
==================================================

카드뉴스 결과물에는 아래 항목이 포함되어야 한다.

- carousel_title
- output_format: instagram_card_news
- target_audience
- tone
- cover_slide
- content_slides
- summary_slide
- cta_slide
- instagram_caption
- hashtags
- safety_note

각 슬라이드에는 아래 항목이 포함되어야 한다.

- slide_id
- slide_type
  예: cover, context, detail, comparison, summary, cta
- slide_title
- slide_body
- emphasis_text
- visual_asset_type
- image_prompt
- design_direction
- layout_hint
- safety_note

카드뉴스 기본 구조:
1. 표지 카드: 강한 제목과 궁금증
2. 상황 설명 카드: 사건 배경 요약
3. 핵심 카드: 사람들이 반응한 이유
4. 비교/쟁점 카드: 의견이 갈리는 포인트
5. 요약 카드: 핵심 정리
6. CTA 카드: “너는 어떻게 생각함?” 댓글 유도

==================================================
14. 설계 결과물 형식
==================================================

다음 항목들을 반드시 포함해서 플랜을 작성해줘.

1. 서비스 한 문장 정의
2. 해결하려는 문제
3. 핵심 사용자
4. 이슈털이 채널용 콘텐츠 방향
5. 참고 유튜브 채널을 일반화하는 방식
6. 참고 인스타 계정을 카드뉴스 확장으로 일반화하는 방식
7. 주제 소싱 전략
8. MVP 1 편집 지시서 기능 범위
9. MVP 2 자동 영상 생성 기능 범위
10. MVP에서 제외할 기능
11. 나중에 추가할 기능
12. 핵심 사용자 흐름
13. 주요 도메인 모델
   - ContentProject
   - ContentSource
   - TopicCandidate
   - TopicScore
   - OutputFormat
   - VideoScript
   - Scene
   - Storyboard
   - StyleTemplate
   - VisualAsset
   - VisualPrompt
   - Subtitle
   - EmphasisCaption
   - TTSScript
   - EditingInstruction
   - SoundCue
   - Timeline
   - TimelineScene
   - RenderJob
   - RenderResult
   - Asset
   - CardNewsProject
   - CardSlide
   - GenerationResult
14. AI 에이전트와 모듈 목록 및 각 역할
15. 쇼츠 생성 파이프라인 구조
16. 자동 영상 렌더링 파이프라인 구조
17. 카드뉴스 생성 파이프라인 구조
18. 롱폼 확장 시 고려할 구조
19. 백엔드 폴더 구조
20. 프론트엔드 폴더 구조
21. API 설계 초안
22. DB 테이블 초안
23. 프롬프트 파일 구조
24. 렌더링 템플릿 구조
25. 외부 API 연동 계획
   - OpenAI 또는 LLM
   - ElevenLabs 또는 TTS API
   - 이미지 생성 API
   - GIF/스톡 영상 검색 API
   - Remotion 또는 FFmpeg 렌더링
   - 파일 저장소
   - 트렌드/뉴스 수집용 API 또는 RSS
26. 에러 처리 전략
   - AI 응답이 비어 있는 경우
   - JSON이 깨진 경우
   - 필수 필드가 빠진 경우
   - 외부 API 호출 실패
   - 생성 결과가 너무 길거나 짧은 경우
   - 저작권/루머/위험 표현 가능성이 있는 경우
   - 참고 채널과 너무 유사한 결과가 생성되는 경우
   - 장면별 편집 지시가 누락되는 경우
   - 이미지 생성 실패
   - TTS 생성 실패
   - 렌더링 실패
   - MP4 저장 실패
   - 카드뉴스 슬라이드에 글자가 너무 많은 경우
27. 테스트 전략
28. 개발 순서
29. 첫 번째로 구현해야 할 기능
30. 구현 전에 내가 결정해야 할 질문 목록

==================================================
15. 추천 폴더 구조 기준
==================================================

아래 구조를 참고하되, 프로젝트에 맞게 개선해줘.

project/
  backend/
    src/
      domain/
      application/
        agents/
        pipelines/
        services/
      infrastructure/
        llm/
        tts/
        image_generation/
        visual_assets/
        trend_sources/
        rendering/
        database/
        storage/
      presentation/
        http/
      main.py
    tests/
    README.md

  frontend/
    app/
    components/
    lib/
    types/
    README.md

  renderer/
    remotion/
      compositions/
      templates/
      components/
    README.md

  docs/
    product-plan.md
    architecture.md
    prompts.md
    style-templates.md
    editing-guide.md
    topic-sourcing.md
    auto-video-rendering.md
    card-news-extension.md
    testing-strategy.md

  README.md

각 폴더와 파일이 어떤 역할을 하는지 설명해줘.
처음부터 너무 많은 파일을 만들지 말고, MVP에 필요한 최소 구조와 나중에 확장할 구조를 구분해서 제안해줘.

==================================================
16. API 설계에서 고려할 엔드포인트
==================================================

아래 API를 고려해서 설계해줘.

MVP 1:
- POST /api/projects
- GET /api/projects
- GET /api/projects/{project_id}
- PATCH /api/projects/{project_id}
- POST /api/generate/shorts-plan
- POST /api/generate/scenes
- POST /api/generate/editing-instructions

MVP 2:
- POST /api/assets/images/generate
- POST /api/assets/tts/generate
- POST /api/timeline/build
- POST /api/render-jobs
- GET /api/render-jobs/{job_id}
- GET /api/render-jobs/{job_id}/download

카드뉴스 확장:
- POST /api/generate/card-news
- PATCH /api/card-news/{project_id}

주제 소싱 확장:
- POST /api/topic/analyze
- POST /api/topic/score
- GET /api/topic/trending

==================================================
17. 테스트 전략
==================================================

테스트 전략은 반드시 포함해줘.

테스트는 계층별로 나눠서 설계해줘.

1. domain test
   - ContentProject, TopicCandidate, TopicScore, VideoScript, Scene, Storyboard, StyleTemplate, VisualAsset, Subtitle, EditingInstruction, SoundCue, Timeline, RenderJob, CardSlide 같은 핵심 데이터 규칙이 맞는지 확인

2. application test
   - 쇼츠 생성 파이프라인 흐름이 맞는지 확인
   - 주제 입력 → 대본 생성 → 장면 분할 → 시각 자료 추천 → 이미지 프롬프트 생성 → TTS 문장 생성 → 자막 생성 → 모션 지시 → 효과음 힌트 생성 순서가 정상 동작하는지 확인
   - 자동 영상 생성에서는 장면 데이터 → 이미지 생성 결과 → TTS 결과 → timeline JSON → render job 생성 흐름이 정상 동작하는지 확인
   - 카드뉴스 확장에서는 주제 → 카드 구조 → 슬라이드 문구 → 디자인 지시 → 인스타 캡션 순서가 정상 동작하는지 확인

3. infrastructure test
   - OpenAI client, ElevenLabs client, 이미지 생성 client, visual asset provider, trend source provider, storage provider, renderer wrapper, DB repository가 정상적으로 대체 가능한지 확인
   - 실제 외부 API를 직접 호출하지 말고 mock provider를 사용

4. presentation test
   - API route 요청/응답 구조가 맞는지 확인
   - 잘못된 입력, 빈 입력, AI 응답 실패, 렌더링 실패 상황의 에러 응답을 확인

5. frontend test
   - 사용자가 주제를 입력하고 스타일을 선택했을 때 결과 화면이 정상적으로 바뀌는지 확인
   - 대본, 장면, 자막, 모션 지시, 효과음 힌트 수정 UI가 정상 동작하는지 확인
   - 영상 렌더링 버튼, 렌더링 상태 표시, 다운로드 버튼이 정상 동작하는지 확인
   - 나중에 카드뉴스 슬라이드 미리보기와 수정 UI가 정상 동작하는지 확인

AI/렌더링 기능 테스트 조건:
- 테스트에서 실제 OpenAI, ElevenLabs, 이미지 생성 API, 트렌드 API, 실제 렌더링을 호출하지 마.
- FakeScriptWriterAgent, FakeStoryboardAgent, FakeVisualAssetSuggestionAgent, FakeEditingDirectionAgent, FakeSoundCueAgent, FakeSubtitleAgent, FakeTopicScoringAgent, FakeImageGenerationProvider, FakeTTSProvider, FakeVideoRenderer, FakeCardNewsPlannerAgent 같은 fake agent/provider를 사용해줘.
- 테스트에서는 항상 같은 입력에 대해 같은 결과가 나오게 설계해줘.
- 모델 응답이 비어 있는 경우, JSON이 깨진 경우, 필수 필드가 빠진 경우를 테스트에 포함해줘.
- 참고 채널과 너무 유사한 결과가 생성되는 경우를 감지할 수 있는 안전 검토 흐름을 고려해줘.
- 렌더링 실패, 파일 저장 실패, 다운로드 링크 만료 같은 상황도 테스트에 포함해줘.
- 테스트가 빠르고 안정적으로 돌아가도록 설계해줘.

==================================================
18. 저작권과 안전 기준
==================================================

반드시 아래 기준을 설계에 포함해줘.

- 참고 채널의 영상, 대사, 자막, 썸네일, 고유 표현을 그대로 복사하지 않는다.
- 참고 채널은 스타일 분석용으로만 사용한다.
- 남의 유튜브 영상이나 방송 자료를 무단으로 가져오는 구조를 만들지 않는다.
- 직접 생성한 이미지/영상, 라이선스 확인된 스톡 영상, 직접 만든 모션 그래픽을 우선 사용한다.
- 효과음과 배경음악도 라이선스 확인된 소스만 사용한다.
- 루머를 사실처럼 말하지 않는다.
- 특정 인물을 과하게 비난하지 않는다.
- 사실 확인이 필요한 이슈는 SafetyReviewAgent가 사용자 확인 대상으로 표시한다.
- 위험하거나 애매한 내용은 “검토 필요” 상태로 저장한다.
- 카드뉴스도 출처 불명 내용이나 과한 단정 표현을 피한다.

==================================================
19. 개발 순서
==================================================

개발 순서는 아래 방향을 참고해서 더 구체적으로 제안해줘.

1단계:
- 서비스 목적과 MVP 범위 확정
- 이슈털이 기본 스타일 정의
- output_format 구조 정의
- 도메인 모델 정의
- TypeScript/Python 타입 또는 스키마 정의
- mock 데이터 기반으로 쇼츠 제작 지시서 화면 흐름 구현

2단계:
- 쇼츠 생성 pipeline 구조 구현
- 실제 AI API 없이 fake agent로 동작 확인
- 주제 입력 → 대본 → 장면 → 시각 자료 추천 → 프롬프트 → 자막 → 모션 → 효과음 결과 생성

3단계:
- 실제 LLM provider/client 연결
- prompt 파일 분리
- JSON 파싱 및 응답 검증 추가
- 장면별 편집 지시서 출력 형식 고정

4단계:
- 프로젝트 저장 기능 추가
- DB repository 연결
- 생성 결과 조회/수정 기능 추가
- 스타일 템플릿 저장 기능 준비

5단계:
- 자동 영상 생성 MVP 준비
- 이미지 생성 provider 연결
- TTS provider 연결
- AssetStorage 구조 구현
- TimelineBuilder 구현
- FakeVideoRenderer 기반 렌더링 흐름 테스트

6단계:
- Remotion 또는 FFmpeg 기반 실제 VideoRenderer 구현
- RenderJobManager 구현
- 렌더링 상태 표시 UI 구현
- MP4 다운로드 기능 구현

7단계:
- 사용자가 뉴스 링크/메모를 넣으면 쇼츠 관점으로 정리하는 기능 추가
- TopicScoringAgent 설계
- 주제 후보 추천 기능 준비

8단계:
- 인스타 카드뉴스 output_format 추가
- CardNewsPlannerAgent, SlideCopyAgent, CardDesignDirectionAgent 추가
- 카드뉴스 슬라이드 미리보기 UI 준비

9단계:
- GIF/스톡 영상 검색 키워드 추천 기능 고도화
- 효과음/전환 템플릿 고도화
- 영상 렌더링 품질 개선

10단계:
- 롱폼 생성 구조 확장
- 유튜브/인스타 업로드 기능 검토
- 로그인/사용량 제한/배포/운영 기능 검토

==================================================
20. 출력 방식
==================================================

답변은 설계 문서처럼 작성해줘.

중요:
- 지금은 코드를 작성하지 마.
- 실제 파일 생성도 하지 마.
- 먼저 플랜만 작성해.
- MVP와 나중에 할 기능을 명확히 구분해.
- 쇼츠 자동 MP4 생성이 최종 목표라는 점을 반영해.
- 다만 처음부터 모든 기능을 만들지 말고, 편집 지시서 MVP → 실제 AI 연결 → 자동 영상 생성 MVP 순서로 설계해.
- 카드뉴스와 롱폼은 확장 기능으로 설계해.
- 각 단계에서 어떤 파일을 만들지 설명해줘.
- 내가 승인하면 그 다음에 1단계 구현으로 넘어갈 수 있게 해줘.
```
