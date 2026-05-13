from __future__ import annotations

from dataclasses import dataclass

from backend.src.domain.models import (
    ContentProject,
    SafetyStatus,
    Scene,
    Storyboard,
    VideoScript,
)


@dataclass(frozen=True)
class SafetyReview:
    status: SafetyStatus
    notes: list[str]


class FakeScriptWriterAgent:
    def generate(self, project: ContentProject) -> VideoScript:
        return VideoScript(
            title=f"{project.topic} 1분 정리",
            narration=(
                f"요즘 {project.topic} 때문에 반응이 갈리고 있음. "
                "처음엔 단순한 해프닝처럼 보였는데, 사람들이 집중한 지점은 따로 있었음. "
                "핵심 쟁점을 짚고 마지막에 의견을 물어본다."
            ),
            target_duration_seconds=project.video_length_seconds,
            style_notes=[
                "첫 3초 안에 궁금증을 만든다.",
                "한 장면당 한 메시지만 전달한다.",
                "확인되지 않은 내용은 단정하지 않는다.",
            ],
        )


class FakeStoryboardAgent:
    PURPOSES = [
        "hook",
        "context",
        "reaction",
        "key_issue",
        "detail",
        "turning_point",
        "conclusion",
        "comment_cta",
    ]

    def generate(self, project: ContentProject, script: VideoScript) -> Storyboard:
        duration = min(5.0, max(2.0, round(project.video_length_seconds / 10, 1)))
        scenes: list[Scene] = []
        for index, purpose in enumerate(self.PURPOSES, start=1):
            scenes.append(
                Scene(
                    scene_id=f"scene_{index:03d}",
                    scene_purpose=purpose,
                    narration=self._narration_for(project.topic, purpose),
                    tts_text=self._narration_for(project.topic, purpose),
                    subtitle="",
                    emphasis_caption="",
                    visual_asset_type="image",
                    visual_description="",
                    generated_image_prompt="",
                    gif_or_clip_suggestion="none",
                    stock_search_keywords=[],
                    motion_direction="zoom_in",
                    transition="quick_cut",
                    sound_effect_hint="pop",
                    estimated_duration=duration,
                    editing_notes="",
                    copyright_safety_note="",
                )
            )
        return Storyboard(scenes)

    def _narration_for(self, topic: str, purpose: str) -> str:
        lines = {
            "hook": f"요즘 {topic}, 이거 때문에 댓글이 확 갈렸음.",
            "context": "처음엔 그냥 작은 해프닝처럼 보였는데 상황이 커졌음.",
            "reaction": "사람들은 왜 이 장면에서 반응했는지 서로 다른 말을 하고 있음.",
            "key_issue": "핵심은 누가 맞냐보다, 이 기준을 어디까지 봐야 하냐는 점임.",
            "detail": "한쪽은 과하다고 보고, 다른 쪽은 당연한 반응이라고 봄.",
            "turning_point": "그런데 뒤늦게 나온 맥락 때문에 분위기가 조금 달라졌음.",
            "conclusion": "그래서 이 사건은 단순 논란보다 기준 싸움에 가까움.",
            "comment_cta": "너는 이 상황, 어느 쪽 말이 더 이해됨?",
        }
        return lines[purpose]


class FakeVisualAssetSuggestionAgent:
    TYPES = ["image", "text_only", "image", "icon", "background", "image", "text_only", "background"]

    def apply(self, storyboard: Storyboard) -> Storyboard:
        scenes = []
        for index, scene in enumerate(storyboard.scenes):
            visual_type = self.TYPES[index]
            scenes.append(
                scene.update(
                    visual_asset_type=visual_type,
                    visual_description=self._description(visual_type, scene.scene_purpose),
                    gif_or_clip_suggestion="라이선스 확인된 짧은 반응 GIF 후보",
                    stock_search_keywords=["korean issue", scene.scene_purpose, "vertical shorts"],
                )
            )
        return Storyboard(scenes)

    def _description(self, visual_type: str, purpose: str) -> str:
        if visual_type == "text_only":
            return "강한 배경색 위에 큰 한 줄 자막"
        if visual_type == "icon":
            return "의견이 갈리는 느낌의 아이콘과 도형 화면"
        if visual_type == "background":
            return "어두운 그라데이션 배경과 큰 강조 자막"
        return f"{purpose} 장면용 스마트폰/커뮤니티 분위기 이미지"


class FakeVisualPromptAgent:
    def apply(self, storyboard: Storyboard) -> Storyboard:
        return Storyboard(
            [
                scene.update(
                    generated_image_prompt=(
                        f"Vertical 9:16 Korean issue explainer background, {scene.visual_description}, "
                        "clean composition, no real logos, no copyrighted characters"
                    ),
                    copyright_safety_note="직접 생성 이미지 또는 라이선스 확인 스톡만 사용한다.",
                )
                for scene in storyboard.scenes
            ]
        )


class FakeTTSScriptAgent:
    def apply(self, storyboard: Storyboard) -> Storyboard:
        return Storyboard([scene.update(tts_text=scene.narration.replace("있음", "있습니다")) for scene in storyboard.scenes])


class FakeSubtitleAgent:
    SUBTITLES = [
        ("댓글 갈린 사건", "확 갈렸음"),
        ("작은 일이 커짐", "상황 커짐"),
        ("반응이 갈린 이유", "서로 다른 말"),
        ("핵심 쟁점", "기준 싸움"),
        ("과하다 vs 당연하다", "의견 충돌"),
        ("뒤늦게 나온 맥락", "분위기 반전"),
        ("결론은 기준 문제", "단순 논란 아님"),
        ("너는 어떻게 봄?", "댓글로 의견"),
    ]

    def apply(self, storyboard: Storyboard) -> Storyboard:
        return Storyboard(
            [
                scene.update(subtitle=self.SUBTITLES[index][0], emphasis_caption=self.SUBTITLES[index][1])
                for index, scene in enumerate(storyboard.scenes)
            ]
        )


class FakeEditingDirectionAgent:
    MOTIONS = ["zoom_in", "pan_left", "shake", "text_pop", "pan_right", "zoom_in", "fade_in", "text_pop"]
    TRANSITIONS = ["quick_cut", "quick_cut", "swipe", "zoom_cut", "quick_cut", "glitch", "fade", "quick_cut"]

    def apply(self, storyboard: Storyboard) -> Storyboard:
        return Storyboard(
            [
                scene.update(
                    motion_direction=self.MOTIONS[index],
                    transition=self.TRANSITIONS[index],
                    editing_notes=(
                        f"{scene.emphasis_caption} 부분에서 자막 크기를 키우고 "
                        f"{self.MOTIONS[index]} 모션을 적용한다."
                    ),
                )
                for index, scene in enumerate(storyboard.scenes)
            ]
        )


class FakeSoundCueAgent:
    CUES = ["pop", "whoosh", "click", "impact", "click", "suspense_rise", "hit", "pop"]

    def apply(self, storyboard: Storyboard) -> Storyboard:
        return Storyboard(
            [
                scene.update(sound_effect_hint=self.CUES[index], sound_effect_asset=f"sfx/{self.CUES[index]}.wav")
                for index, scene in enumerate(storyboard.scenes)
            ]
        )


class FakeSafetyReviewAgent:
    RISK_WORDS = ("루머", "비난", "확인 안 된", "저격", "허위")

    def review(self, project: ContentProject, storyboard: Storyboard) -> SafetyReview:
        if any(word in project.topic or word in project.tone for word in self.RISK_WORDS):
            return SafetyReview(
                SafetyStatus.REVIEW_REQUIRED,
                ["검토 필요: 루머, 비난, 사실 확인 위험이 있는 표현이 포함되어 있습니다."],
            )
        return SafetyReview(SafetyStatus.APPROVED, ["저작권과 루머 위험이 낮은 편집 지시서입니다."])


@dataclass(frozen=True)
class FakeAgentBundle:
    script_writer: FakeScriptWriterAgent
    storyboard: FakeStoryboardAgent
    visual_asset: FakeVisualAssetSuggestionAgent
    visual_prompt: FakeVisualPromptAgent
    tts_script: FakeTTSScriptAgent
    subtitle: FakeSubtitleAgent
    editing_direction: FakeEditingDirectionAgent
    sound_cue: FakeSoundCueAgent
    safety_review: FakeSafetyReviewAgent


def create_fake_agent_bundle() -> FakeAgentBundle:
    return FakeAgentBundle(
        script_writer=FakeScriptWriterAgent(),
        storyboard=FakeStoryboardAgent(),
        visual_asset=FakeVisualAssetSuggestionAgent(),
        visual_prompt=FakeVisualPromptAgent(),
        tts_script=FakeTTSScriptAgent(),
        subtitle=FakeSubtitleAgent(),
        editing_direction=FakeEditingDirectionAgent(),
        sound_cue=FakeSoundCueAgent(),
        safety_review=FakeSafetyReviewAgent(),
    )
