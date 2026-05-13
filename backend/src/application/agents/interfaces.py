from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from backend.src.domain.models import ContentProject, SafetyStatus, Storyboard, VideoScript


@dataclass(frozen=True)
class SafetyReview:
    status: SafetyStatus
    notes: list[str]


class ScriptWriterAgent(Protocol):
    def generate(self, project: ContentProject) -> VideoScript:
        ...


class StoryboardAgent(Protocol):
    def generate(self, project: ContentProject, script: VideoScript) -> Storyboard:
        ...


class VisualAssetSuggestionAgent(Protocol):
    def apply(self, storyboard: Storyboard) -> Storyboard:
        ...


class SubtitleAgent(Protocol):
    def apply(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> Storyboard:
        ...


class EditingDirectionAgent(Protocol):
    def apply(self, storyboard: Storyboard) -> Storyboard:
        ...


class SafetyReviewAgent(Protocol):
    def review(self, project: ContentProject, storyboard: Storyboard) -> SafetyReview:
        ...


@dataclass(frozen=True)
class ShortsAgentBundle:
    script_writer: ScriptWriterAgent
    storyboard: StoryboardAgent
    visual_asset: VisualAssetSuggestionAgent
    subtitle: SubtitleAgent
    editing_direction: EditingDirectionAgent
    safety_review: SafetyReviewAgent
