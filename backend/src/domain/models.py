from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import Any
from uuid import uuid4


class OutputFormat(StrEnum):
    YOUTUBE_SHORTS = "youtube_shorts"
    INSTAGRAM_CARD_NEWS = "instagram_card_news"
    INSTAGRAM_REELS = "instagram_reels"
    LONGFORM_VIDEO = "longform_video"


class ProjectStatus(StrEnum):
    DRAFT = "draft"
    GENERATING = "generating"
    READY_FOR_REVIEW = "ready_for_review"
    REVIEW_REQUIRED = "review_required"
    GENERATION_FAILED = "generation_failed"


class SafetyStatus(StrEnum):
    APPROVED = "approved"
    REVIEW_REQUIRED = "review_required"


class VisualAssetType(StrEnum):
    IMAGE = "image"
    GIF = "gif"
    SHORT_CLIP = "short_clip"
    TEXT_ONLY = "text_only"
    ICON = "icon"
    BACKGROUND = "background"


class MotionDirection(StrEnum):
    ZOOM_IN = "zoom_in"
    PAN_LEFT = "pan_left"
    SHAKE = "shake"
    TEXT_POP = "text_pop"
    PAN_RIGHT = "pan_right"
    FADE_IN = "fade_in"


class Transition(StrEnum):
    QUICK_CUT = "quick_cut"
    SWIPE = "swipe"
    ZOOM_CUT = "zoom_cut"
    GLITCH = "glitch"
    FADE = "fade"


class SoundEffectHint(StrEnum):
    POP = "pop"
    WHOOSH = "whoosh"
    CLICK = "click"
    IMPACT = "impact"
    SUSPENSE_RISE = "suspense_rise"
    HIT = "hit"


def _coerce_allowed_value(enum_type: type[StrEnum], value: StrEnum | str, field_name: str) -> StrEnum:
    try:
        return enum_type(value)
    except ValueError as exc:
        raise ValueError(f"unsupported {field_name}") from exc


@dataclass(frozen=True)
class ContentProject:
    project_id: str
    topic: str
    target_audience: str
    tone: str
    style_template_id: str
    video_length_seconds: int
    output_format: OutputFormat
    status: ProjectStatus = ProjectStatus.DRAFT
    generation_result: GenerationResult | None = None

    @classmethod
    def create(
        cls,
        topic: str,
        target_audience: str,
        tone: str,
        style_template_id: str,
        video_length_seconds: int,
        output_format: OutputFormat,
    ) -> ContentProject:
        if not topic.strip():
            raise ValueError("topic is required")
        if output_format != OutputFormat.YOUTUBE_SHORTS:
            raise ValueError("MVP only supports youtube_shorts")
        if not 30 <= video_length_seconds <= 90:
            raise ValueError("video_length_seconds must be between 30 and 90")
        return cls(
            project_id=f"project_{uuid4().hex[:12]}",
            topic=topic.strip(),
            target_audience=target_audience.strip(),
            tone=tone.strip(),
            style_template_id=style_template_id.strip(),
            video_length_seconds=video_length_seconds,
            output_format=output_format,
        )

    def with_generation_result(self, result: GenerationResult) -> ContentProject:
        next_status = (
            ProjectStatus.REVIEW_REQUIRED
            if result.safety_status == SafetyStatus.REVIEW_REQUIRED
            else ProjectStatus.READY_FOR_REVIEW
        )
        return replace(self, status=next_status, generation_result=result)


@dataclass(frozen=True)
class VideoScript:
    title: str
    narration: str
    target_duration_seconds: int
    style_notes: list[str]


@dataclass(frozen=True)
class Scene:
    scene_id: str
    scene_purpose: str
    narration: str
    tts_text: str
    subtitle: str
    emphasis_caption: str
    visual_asset_type: VisualAssetType
    visual_description: str
    generated_image_prompt: str
    gif_or_clip_suggestion: str
    stock_search_keywords: list[str]
    motion_direction: MotionDirection
    transition: Transition
    sound_effect_hint: SoundEffectHint
    estimated_duration: float
    editing_notes: str
    copyright_safety_note: str
    generated_image_url: str | None = None
    sound_effect_asset: str | None = None
    actual_duration: float | None = None

    def __post_init__(self) -> None:
        if not 2.0 <= self.estimated_duration <= 5.0:
            raise ValueError("estimated_duration must be between 2 and 5 seconds")
        object.__setattr__(
            self,
            "visual_asset_type",
            _coerce_allowed_value(VisualAssetType, self.visual_asset_type, "visual_asset_type"),
        )
        object.__setattr__(
            self,
            "motion_direction",
            _coerce_allowed_value(MotionDirection, self.motion_direction, "motion_direction"),
        )
        object.__setattr__(
            self,
            "transition",
            _coerce_allowed_value(Transition, self.transition, "transition"),
        )
        object.__setattr__(
            self,
            "sound_effect_hint",
            _coerce_allowed_value(SoundEffectHint, self.sound_effect_hint, "sound_effect_hint"),
        )

    @classmethod
    def minimal(cls, scene_id: str, estimated_duration: float) -> Scene:
        return cls(
            scene_id=scene_id,
            scene_purpose="context",
            narration="상황을 빠르게 정리한다.",
            tts_text="상황을 빠르게 정리한다.",
            subtitle="상황 정리",
            emphasis_caption="핵심",
            visual_asset_type="image",
            visual_description="쇼츠 배경용 이미지",
            generated_image_prompt="vertical Korean issue explainer background",
            gif_or_clip_suggestion="none",
            stock_search_keywords=["issue", "korea"],
            motion_direction="zoom_in",
            transition="quick_cut",
            sound_effect_hint="pop",
            estimated_duration=estimated_duration,
            editing_notes="핵심 단어를 크게 강조한다.",
            copyright_safety_note="직접 생성 또는 라이선스 확인 자료만 사용한다.",
        )

    def update(self, **changes: Any) -> Scene:
        return replace(self, **changes)


@dataclass(frozen=True)
class Storyboard:
    scenes: list[Scene]


@dataclass(frozen=True)
class GenerationResult:
    project_id: str
    video_script: VideoScript
    storyboard: Storyboard
    safety_status: SafetyStatus
    safety_notes: list[str]

    def update_scene(self, scene_id: str, **changes: Any) -> GenerationResult:
        updated_scenes = [
            scene.update(**changes) if scene.scene_id == scene_id else scene
            for scene in self.storyboard.scenes
        ]
        if updated_scenes == self.storyboard.scenes:
            raise ValueError(f"scene not found: {scene_id}")
        return replace(self, storyboard=Storyboard(updated_scenes))


@dataclass(frozen=True)
class TimelineScene:
    scene_id: str
    start_time: float
    end_time: float
    duration: float
    visual_asset: dict[str, str | None]
    narration_audio: dict[str, str | None]
    subtitle: dict[str, float | str]
    emphasis_caption: dict[str, float | str]
    motion: str
    transition: str
    sound_effect: dict[str, float | str | None]


@dataclass(frozen=True)
class Timeline:
    project_id: str
    output_format: OutputFormat
    aspect_ratio: str
    resolution: str
    fps: int
    total_duration: float
    audio_mix: dict[str, float | None]
    scenes: list[TimelineScene] = field(default_factory=list)

    @classmethod
    def from_scenes(cls, project_id: str, output_format: OutputFormat, scenes: list[Scene]) -> Timeline:
        cursor = 0.0
        timeline_scenes: list[TimelineScene] = []
        for scene in scenes:
            duration = scene.actual_duration or scene.estimated_duration
            start_time = round(cursor, 2)
            end_time = round(cursor + duration, 2)
            timeline_scenes.append(
                TimelineScene(
                    scene_id=scene.scene_id,
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    visual_asset={"type": scene.visual_asset_type, "url": scene.generated_image_url},
                    narration_audio={"url": None},
                    subtitle={"text": scene.subtitle, "start_time": start_time + 0.2, "end_time": end_time - 0.2},
                    emphasis_caption={"text": scene.emphasis_caption, "start_time": max(start_time, end_time - 1.2), "end_time": end_time},
                    motion=scene.motion_direction,
                    transition=scene.transition,
                    sound_effect={"type": scene.sound_effect_hint, "start_time": start_time},
                )
            )
            cursor = end_time

        return cls(
            project_id=project_id,
            output_format=output_format,
            aspect_ratio="9:16",
            resolution="1080x1920",
            fps=30,
            total_duration=round(cursor, 2),
            audio_mix={
                "background_music": None,
                "background_music_volume": 0.15,
                "narration_volume": 1.0,
                "sfx_volume": 0.7,
            },
            scenes=timeline_scenes,
        )
