from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from backend.src.domain.models import ContentProject, SafetyStatus, Storyboard, VideoScript


@dataclass(frozen=True)
class SafetyReview:
    status: SafetyStatus
    notes: list[str]
    copyright_risks: list[str] = field(default_factory=list)
    rumor_or_defamation_risks: list[str] = field(default_factory=list)
    privacy_or_portrait_risks: list[str] = field(default_factory=list)
    source_usage_risks: list[str] = field(default_factory=list)
    required_human_review: bool = False
    recommended_revisions: list[str] = field(default_factory=list)


class ScriptWriterAgent(Protocol):
    def generate(self, project: ContentProject) -> VideoScript:
        ...


class StoryboardAgent(Protocol):
    def generate(self, project: ContentProject, script: VideoScript) -> Storyboard:
        ...


class VisualAssetSuggestionAgent(Protocol):
    def apply(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> Storyboard:
        ...


class SubtitleAgent(Protocol):
    def apply(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> Storyboard:
        ...


class EditingDirectionAgent(Protocol):
    def apply(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> Storyboard:
        ...


class SafetyReviewAgent(Protocol):
    def review(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> SafetyReview:
        ...


@dataclass(frozen=True)
class ShortsAgentBundle:
    script_writer: ScriptWriterAgent
    storyboard: StoryboardAgent
    visual_asset: VisualAssetSuggestionAgent
    subtitle: SubtitleAgent
    editing_direction: EditingDirectionAgent
    safety_review: SafetyReviewAgent
