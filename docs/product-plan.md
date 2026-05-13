# 이슈털이 AI 콘텐츠 제작 서비스 제품 계획

## 서비스 정의

사용자가 주제를 입력하면 AI가 이슈/썰 쇼츠용 대본, 장면 구성, 자막, 이미지 프롬프트, TTS 문장, 모션, 효과음, 전환 지시를 생성하는 콘텐츠 제작 웹서비스다.

## MVP 1

- `youtube_shorts` 형식만 지원한다.
- 실제 OpenAI, 이미지 생성, TTS, 영상 렌더링은 호출하지 않는다.
- fake agent 기반으로 항상 같은 입력에 대해 예측 가능한 쇼츠 편집 지시서를 만든다.
- 결과는 8개 장면의 storyboard로 구성된다.

## MVP 2 확장

- 이미지 생성 provider, TTS provider, TimelineBuilder, VideoRenderer, AssetStorage를 붙인다.
- 첫 렌더링은 9:16 고정 템플릿 기반 MP4 생성으로 제한한다.

## 제외

참고 채널 영상 다운로드, 저작권 위험 자료 자동 수집, 결제, 팀 협업, 업로드 자동화는 MVP에서 제외한다.
