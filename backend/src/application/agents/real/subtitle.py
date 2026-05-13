from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.src.application.agents.llm import LLMClient
from backend.src.application.agents.prompts import PromptLoader
from backend.src.application.agents.validation import JsonResponseValidator, LLMResponseValidationError
from backend.src.domain.models import ContentProject, Storyboard, VideoScript


SUBTITLE_FIELDS = {"scene_id", "subtitle", "emphasis_caption"}


@dataclass(frozen=True)
class RealSubtitleAgent:
    llm_client: LLMClient
    prompt_loader: PromptLoader
    response_validator: JsonResponseValidator

    def apply(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> Storyboard:
        response = self.llm_client.complete(self._build_prompt(project, script, storyboard))
        payload = self.response_validator.validate(response)
        subtitles_payload = payload["subtitles"]
        if not isinstance(subtitles_payload, list):
            raise LLMResponseValidationError("subtitles must be a list")

        subtitle_updates = self._subtitle_updates(subtitles_payload, storyboard)
        return Storyboard(
            [
                scene.update(**subtitle_updates[scene.scene_id])
                if scene.scene_id in subtitle_updates
                else scene
                for scene in storyboard.scenes
            ]
        )

    def _build_prompt(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> str:
        template = self.prompt_loader.load("shorts/subtitle")
        scene_lines = [
            (
                f"- {scene.scene_id}: purpose={scene.scene_purpose}; "
                f"narration={scene.narration}; current_subtitle={scene.subtitle}; "
                f"current_emphasis_caption={scene.emphasis_caption}"
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
                'Return JSON only in the shape {"subtitles": [...]} with scene_id, subtitle, and emphasis_caption.',
            ]
        )

    def _subtitle_updates(self, subtitles_payload: list[Any], storyboard: Storyboard) -> dict[str, dict[str, str]]:
        scene_ids = {scene.scene_id for scene in storyboard.scenes}
        updates: dict[str, dict[str, str]] = {}
        for item in subtitles_payload:
            if not isinstance(item, dict):
                raise LLMResponseValidationError("subtitle item must be an object")
            missing_fields = sorted(field for field in SUBTITLE_FIELDS if field not in item)
            if missing_fields:
                raise LLMResponseValidationError(f"missing subtitle field: {missing_fields[0]}")

            scene_id = str(item["scene_id"])
            if scene_id not in scene_ids:
                raise LLMResponseValidationError(f"unknown scene_id: {scene_id}")

            updates[scene_id] = {
                "subtitle": str(item["subtitle"]),
                "emphasis_caption": str(item["emphasis_caption"]),
            }
        return updates
