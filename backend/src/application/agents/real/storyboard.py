from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.src.application.agents.llm import LLMClient
from backend.src.application.agents.prompts import PromptLoader
from backend.src.application.agents.validation import JsonResponseValidator, LLMResponseValidationError
from backend.src.domain.models import ContentProject, Scene, Storyboard, VideoScript


SCENE_FIELDS = {
    "scene_id",
    "scene_purpose",
    "narration",
    "tts_text",
    "subtitle",
    "emphasis_caption",
    "visual_asset_type",
    "visual_description",
    "generated_image_prompt",
    "gif_or_clip_suggestion",
    "stock_search_keywords",
    "motion_direction",
    "transition",
    "sound_effect_hint",
    "estimated_duration",
    "editing_notes",
    "copyright_safety_note",
}


@dataclass(frozen=True)
class RealStoryboardAgent:
    llm_client: LLMClient
    prompt_loader: PromptLoader
    response_validator: JsonResponseValidator

    def generate(self, project: ContentProject, script: VideoScript) -> Storyboard:
        response = self.llm_client.complete(self._build_prompt(project, script))
        payload = self.response_validator.validate(response)
        scenes_payload = payload["scenes"]
        if not isinstance(scenes_payload, list):
            raise ValueError("scenes must be a list")
        return Storyboard([self._scene_from_payload(scene) for scene in scenes_payload])

    def _build_prompt(self, project: ContentProject, script: VideoScript) -> str:
        template = self.prompt_loader.load("shorts/storyboard")
        return "\n\n".join(
            [
                template,
                "Project input:",
                f"- topic: {project.topic}",
                f"- target_audience: {project.target_audience}",
                f"- tone: {project.tone}",
                f"- style_template_id: {project.style_template_id}",
                f"- video_length_seconds: {project.video_length_seconds}",
                "VideoScript:",
                f"- title: {script.title}",
                f"- narration: {script.narration}",
                f"- target_duration_seconds: {script.target_duration_seconds}",
                f"- style_notes: {script.style_notes}",
                'Return JSON only in the shape {"scenes": [...]} with every required scene field.',
            ]
        )

    def _scene_from_payload(self, payload: Any) -> Scene:
        if not isinstance(payload, dict):
            raise ValueError("scene must be an object")
        missing_fields = sorted(field for field in SCENE_FIELDS if field not in payload)
        if missing_fields:
            raise ValueError(f"missing scene field: {missing_fields[0]}")
        normalized = {field: payload[field] for field in SCENE_FIELDS}
        normalized["estimated_duration"] = self._duration(payload["estimated_duration"])
        normalized["stock_search_keywords"] = self._stock_search_keywords(
            payload["stock_search_keywords"]
        )
        return Scene(**normalized)

    def _duration(self, value: Any) -> float:
        if isinstance(value, int | float):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError as exc:
                raise LLMResponseValidationError(
                    f"estimated_duration must be numeric: {value}"
                ) from exc
        raise LLMResponseValidationError("estimated_duration must be numeric")

    def _stock_search_keywords(self, value: Any) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise LLMResponseValidationError("stock_search_keywords must be a list")
        return [str(keyword) for keyword in value]
