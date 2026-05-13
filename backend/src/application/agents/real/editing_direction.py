from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.src.application.agents.llm import LLMClient
from backend.src.application.agents.prompts import PromptLoader
from backend.src.application.agents.validation import JsonResponseValidator, LLMResponseValidationError
from backend.src.domain.models import (
    ContentProject,
    MotionDirection,
    SoundEffectHint,
    Storyboard,
    Transition,
    VideoScript,
)


EDITING_FIELDS = {
    "scene_id",
    "motion_direction",
    "transition",
    "sound_effect_hint",
    "editing_notes",
}


@dataclass(frozen=True)
class RealEditingDirectionAgent:
    llm_client: LLMClient
    prompt_loader: PromptLoader
    response_validator: JsonResponseValidator

    def apply(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> Storyboard:
        response = self.llm_client.complete(self._build_prompt(project, script, storyboard))
        payload = self.response_validator.validate(response)
        directions_payload = payload["editing_directions"]
        if not isinstance(directions_payload, list):
            raise LLMResponseValidationError("editing_directions must be a list")

        direction_updates = self._direction_updates(directions_payload, storyboard)
        return Storyboard(
            [
                scene.update(**direction_updates[scene.scene_id])
                if scene.scene_id in direction_updates
                else scene
                for scene in storyboard.scenes
            ]
        )

    def _build_prompt(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> str:
        template = self.prompt_loader.load("shorts/editing_direction")
        scene_lines = [
            (
                f"- {scene.scene_id}: purpose={scene.scene_purpose}; "
                f"narration={scene.narration}; subtitle={scene.subtitle}; "
                f"emphasis_caption={scene.emphasis_caption}; "
                f"visual_asset_type={scene.visual_asset_type}; "
                f"visual_description={scene.visual_description}; "
                f"estimated_duration={scene.estimated_duration}; "
                f"current_motion={scene.motion_direction}; "
                f"current_transition={scene.transition}; "
                f"current_sound_effect={scene.sound_effect_hint}"
            )
            for scene in storyboard.scenes
        ]
        return "\n\n".join(
            [
                template,
                "Project input:",
                f"- topic: {project.topic}",
                f"- target_audience: {project.target_audience}",
                f"- tone: {project.tone}",
                f"- style_template_id: {project.style_template_id}",
                "VideoScript:",
                f"- title: {script.title}",
                f"- narration: {script.narration}",
                f"- target_duration_seconds: {script.target_duration_seconds}",
                f"- style_notes: {script.style_notes}",
                "Storyboard scenes:",
                "\n".join(scene_lines),
                'Return JSON only in the shape {"editing_directions": [...]} with every required editing field.',
            ]
        )

    def _direction_updates(
        self,
        directions_payload: list[Any],
        storyboard: Storyboard,
    ) -> dict[str, dict[str, Any]]:
        scene_ids = {scene.scene_id for scene in storyboard.scenes}
        updates: dict[str, dict[str, Any]] = {}
        for item in directions_payload:
            if not isinstance(item, dict):
                raise LLMResponseValidationError("editing direction item must be an object")
            missing_fields = sorted(field for field in EDITING_FIELDS if field not in item)
            if missing_fields:
                raise LLMResponseValidationError(f"missing editing direction field: {missing_fields[0]}")

            scene_id = str(item["scene_id"])
            if scene_id not in scene_ids:
                raise LLMResponseValidationError(f"unknown scene_id: {scene_id}")

            updates[scene_id] = {
                "motion_direction": self._motion_direction(item["motion_direction"]),
                "transition": self._transition(item["transition"]),
                "sound_effect_hint": self._sound_effect_hint(item["sound_effect_hint"]),
                "editing_notes": str(item["editing_notes"]),
            }
        return updates

    def _motion_direction(self, value: Any) -> MotionDirection:
        try:
            return MotionDirection(str(value))
        except ValueError as exc:
            raise LLMResponseValidationError(f"unsupported motion_direction: {value}") from exc

    def _transition(self, value: Any) -> Transition:
        try:
            return Transition(str(value))
        except ValueError as exc:
            raise LLMResponseValidationError(f"unsupported transition: {value}") from exc

    def _sound_effect_hint(self, value: Any) -> SoundEffectHint:
        try:
            return SoundEffectHint(str(value))
        except ValueError as exc:
            raise LLMResponseValidationError(f"unsupported sound_effect_hint: {value}") from exc
