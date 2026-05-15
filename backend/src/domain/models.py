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
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "needs_review"


class VisualAssetType(StrEnum):
    IMAGE = "image"
    GIF = "gif"
    SHORT_CLIP = "short_clip"
    TEXT_ONLY = "text_only"
    ICON = "icon"
    BACKGROUND = "background"


class VisualSourceStrategy(StrEnum):
    REFERENCE_CAPTURE = "reference_capture"
    MOCKUP = "mockup"
    STOCK_ASSET = "stock_asset"
    AI_GENERATED = "ai_generated"
    ORIGINAL_STICKER = "original_sticker"
    TEXT_CARD = "text_card"
    USER_PROVIDED = "user_provided"
    AVOID = "avoid"


class CaptureSourceType(StrEnum):
    COMMUNITY = "community"
    NEWS = "news"
    YOUTUBE = "youtube"
    BROADCAST = "broadcast"
    INSTAGRAM = "instagram"
    GOOGLE_IMAGE = "google_image"
    STOCK_SITE = "stock_site"
    USER_PROVIDED = "user_provided"
    AI_GENERATED = "ai_generated"
    NONE = "none"


class CaptureUsageMode(StrEnum):
    DIRECT_CAPTURE_CANDIDATE = "direct_capture_candidate"
    MOCKUP_RECOMMENDED = "mockup_recommended"
    LICENSE_REQUIRED = "license_required"
    PERMISSION_REQUIRED = "permission_required"
    AVOID = "avoid"


class BeatType(StrEnum):
    HOOK = "hook"
    EVIDENCE = "evidence"
    REACTION = "reaction"
    TURNING_POINT = "turning_point"
    PAYOFF = "payoff"
    CTA = "cta"


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
            if result.safety_status != SafetyStatus.APPROVED
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
    visual_source_strategy: VisualSourceStrategy = VisualSourceStrategy.AI_GENERATED
    capture_source_type: CaptureSourceType = CaptureSourceType.AI_GENERATED
    capture_usage_mode: CaptureUsageMode = CaptureUsageMode.DIRECT_CAPTURE_CANDIDATE
    asset_usage_note: str = "Use self-made or properly licensed assets and verify rights before publishing."
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
            "visual_source_strategy",
            _coerce_allowed_value(VisualSourceStrategy, self.visual_source_strategy, "visual_source_strategy"),
        )
        object.__setattr__(
            self,
            "capture_source_type",
            _coerce_allowed_value(CaptureSourceType, self.capture_source_type, "capture_source_type"),
        )
        object.__setattr__(
            self,
            "capture_usage_mode",
            _coerce_allowed_value(CaptureUsageMode, self.capture_usage_mode, "capture_usage_mode"),
        )
        if not self.asset_usage_note.strip():
            raise ValueError("asset_usage_note is required")
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
            visual_source_strategy="ai_generated",
            capture_source_type="ai_generated",
            capture_usage_mode="direct_capture_candidate",
            asset_usage_note="Use self-made or properly licensed assets and verify rights before publishing.",
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
    timeline: Timeline
    safety_status: SafetyStatus
    safety_notes: list[str]
    copyright_risks: list[str] = field(default_factory=list)
    rumor_or_defamation_risks: list[str] = field(default_factory=list)
    privacy_or_portrait_risks: list[str] = field(default_factory=list)
    source_usage_risks: list[str] = field(default_factory=list)
    required_human_review: bool = False
    recommended_revisions: list[str] = field(default_factory=list)

    def update_scene(self, scene_id: str, **changes: Any) -> GenerationResult:
        updated_scenes = [
            scene.update(**changes) if scene.scene_id == scene_id else scene
            for scene in self.storyboard.scenes
        ]
        if updated_scenes == self.storyboard.scenes:
            raise ValueError(f"scene not found: {scene_id}")
        updated_storyboard = Storyboard(updated_scenes)
        return replace(
            self,
            storyboard=updated_storyboard,
            timeline=Timeline.from_scenes(self.project_id, self.timeline.output_format, updated_storyboard.scenes),
        )


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
    beats: list[ProductionBeat] = field(default_factory=list)
    asset_review_checklist: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProductionBeat:
    beat_type: BeatType
    start_time: float
    end_time: float
    text: str
    motion: str
    sound_effect: str
    note: str


def _scene_text_contains(scene: Scene, *needles: str) -> bool:
    text = " ".join(
        [
            scene.scene_purpose,
            scene.narration,
            scene.subtitle,
            scene.emphasis_caption,
            scene.visual_description,
            scene.editing_notes,
        ]
    ).lower()
    return any(needle.lower() in text for needle in needles)


def _scene_needs_evidence_beat(scene: Scene) -> bool:
    if scene.visual_source_strategy in {
        VisualSourceStrategy.REFERENCE_CAPTURE,
        VisualSourceStrategy.MOCKUP,
        VisualSourceStrategy.STOCK_ASSET,
        VisualSourceStrategy.USER_PROVIDED,
    }:
        return True
    if scene.capture_source_type not in {CaptureSourceType.AI_GENERATED, CaptureSourceType.NONE}:
        return True
    return scene.capture_usage_mode in {
        CaptureUsageMode.MOCKUP_RECOMMENDED,
        CaptureUsageMode.LICENSE_REQUIRED,
        CaptureUsageMode.PERMISSION_REQUIRED,
        CaptureUsageMode.AVOID,
    }


def _beat_note(beat_type: BeatType, scene: Scene) -> str:
    if beat_type == BeatType.HOOK:
        return "Open with the clearest conflict or curiosity gap in this scene."
    if beat_type == BeatType.EVIDENCE:
        return (
            "Show or describe supporting material; "
            f"strategy={scene.visual_source_strategy}, "
            f"source={scene.capture_source_type}, "
            f"usage={scene.capture_usage_mode}."
        )
    if beat_type == BeatType.REACTION:
        return "Emphasize the audience split or comment reaction without overstating facts."
    if beat_type == BeatType.TURNING_POINT:
        return "Introduce the context shift or reversal that changes how viewers read the issue."
    if beat_type == BeatType.PAYOFF:
        return "Resolve the issue into one clear takeaway or framing point."
    return "End with a clear viewer response prompt."


def _build_production_beats(
    scene: Scene,
    start_time: float,
    end_time: float,
    scene_index: int,
    scene_count: int,
) -> list[ProductionBeat]:
    beat_types: list[BeatType] = []
    if scene_index == 0:
        beat_types.append(BeatType.HOOK)
    if _scene_needs_evidence_beat(scene):
        beat_types.append(BeatType.EVIDENCE)
    if _scene_text_contains(scene, "reaction", "comment", "댓글", "반응"):
        beat_types.append(BeatType.REACTION)
    if _scene_text_contains(scene, "turning_point", "turning point", "반전", "맥락", "전환"):
        beat_types.append(BeatType.TURNING_POINT)
    if _scene_text_contains(scene, "conclusion", "close", "payoff", "결론", "마무리", "정리"):
        beat_types.append(BeatType.PAYOFF)
    if scene_index == scene_count - 1:
        beat_types.append(BeatType.CTA)

    deduped: list[BeatType] = []
    for beat_type in beat_types:
        if beat_type not in deduped:
            deduped.append(beat_type)

    if not deduped:
        return []

    duration = end_time - start_time
    text = scene.emphasis_caption.strip() or scene.subtitle.strip() or scene.narration.strip()
    beats: list[ProductionBeat] = []
    for index, beat_type in enumerate(deduped):
        beat_start = round(start_time + (duration * index / len(deduped)), 2)
        beat_end = end_time if index == len(deduped) - 1 else round(start_time + (duration * (index + 1) / len(deduped)), 2)
        beats.append(
            ProductionBeat(
                beat_type=beat_type,
                start_time=max(start_time, beat_start),
                end_time=min(end_time, beat_end),
                text=text,
                motion=scene.motion_direction,
                sound_effect=scene.sound_effect_hint,
                note=_beat_note(beat_type, scene),
            )
        )
    return beats


def _build_asset_review_checklist(scene: Scene) -> list[str]:
    checklist: list[str] = []
    if scene.capture_source_type in {CaptureSourceType.COMMUNITY, CaptureSourceType.INSTAGRAM}:
        checklist.append("Check nicknames, profile images, original comments, personal data, and defamation risk.")
    elif scene.capture_source_type in {CaptureSourceType.NEWS, CaptureSourceType.YOUTUBE, CaptureSourceType.BROADCAST}:
        checklist.append("Check logos, screenshot rights, and whether permission_required applies.")
    elif scene.capture_source_type == CaptureSourceType.GOOGLE_IMAGE:
        checklist.append("Confirm license_required before using any Google image material.")
    elif scene.capture_source_type == CaptureSourceType.STOCK_SITE:
        checklist.append("Confirm stock license, model release, and location/property release.")
    elif scene.capture_source_type == CaptureSourceType.AI_GENERATED:
        checklist.append("Check real person confusion, brand or character similarity, and false factual implication.")
    elif scene.capture_source_type == CaptureSourceType.USER_PROVIDED:
        checklist.append("Confirm usage rights, source, and permission for user-provided material.")

    if scene.capture_usage_mode == CaptureUsageMode.AVOID:
        checklist.append("Do not use this source as-is; replace it or create a safer alternative.")
    if scene.capture_usage_mode == CaptureUsageMode.LICENSE_REQUIRED:
        checklist.append("Verify license_required status before publishing.")
    if scene.capture_usage_mode == CaptureUsageMode.PERMISSION_REQUIRED:
        checklist.append("Verify permission_required status before publishing.")
    if scene.asset_usage_note.strip():
        checklist.append(f"Asset note: {scene.asset_usage_note.strip()}")

    return checklist


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
                    beats=_build_production_beats(scene, start_time, end_time, len(timeline_scenes), len(scenes)),
                    asset_review_checklist=_build_asset_review_checklist(scene),
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
