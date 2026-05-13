from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.src.application.agents.llm import LLMClient
from backend.src.application.agents.prompts import PromptLoader
from backend.src.application.agents.validation import JsonResponseValidator, LLMResponseValidationError
from backend.src.domain.models import ContentProject, Storyboard, VideoScript, VisualAssetType


VISUAL_FIELDS = {
    "scene_id",
    "visual_asset_type",
    "visual_description",
    "generated_image_prompt",
    "gif_or_clip_suggestion",
    "stock_search_keywords",
}


@dataclass(frozen=True)
class RealVisualAssetSuggestionAgent:
    llm_client: LLMClient
    prompt_loader: PromptLoader
    response_validator: JsonResponseValidator

    def apply(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> Storyboard:
        response = self.llm_client.complete(self._build_prompt(project, script, storyboard))
        payload = self.response_validator.validate(response)
        visuals_payload = payload["visuals"]
        if not isinstance(visuals_payload, list):
            raise LLMResponseValidationError("visuals must be a list")

        visual_updates = self._visual_updates(visuals_payload, storyboard)
        return Storyboard(
            [
                scene.update(**visual_updates[scene.scene_id])
                if scene.scene_id in visual_updates
                else scene
                for scene in storyboard.scenes
            ]
        )

    def _build_prompt(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> str:
        template = self.prompt_loader.load("shorts/visual_prompt")
        scene_lines = [
            (
                f"- {scene.scene_id}: purpose={scene.scene_purpose}; "
                f"narration={scene.narration}; subtitle={scene.subtitle}; "
                f"emphasis_caption={scene.emphasis_caption}; "
                f"current_visual_asset_type={scene.visual_asset_type}; "
                f"current_visual_description={scene.visual_description}"
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
                'Return JSON only in the shape {"visuals": [...]} with every required visual field.',
            ]
        )

    def _visual_updates(self, visuals_payload: list[Any], storyboard: Storyboard) -> dict[str, dict[str, Any]]:
        scene_ids = {scene.scene_id for scene in storyboard.scenes}
        updates: dict[str, dict[str, Any]] = {}
        for item in visuals_payload:
            if not isinstance(item, dict):
                raise LLMResponseValidationError("visual item must be an object")
            missing_fields = sorted(field for field in VISUAL_FIELDS if field not in item)
            if missing_fields:
                raise LLMResponseValidationError(f"missing visual field: {missing_fields[0]}")

            scene_id = str(item["scene_id"])
            if scene_id not in scene_ids:
                raise LLMResponseValidationError(f"unknown scene_id: {scene_id}")

            updates[scene_id] = {
                "visual_asset_type": self._visual_asset_type(item["visual_asset_type"]),
                "visual_description": str(item["visual_description"]),
                "generated_image_prompt": str(item["generated_image_prompt"]),
                "gif_or_clip_suggestion": str(item["gif_or_clip_suggestion"]),
                "stock_search_keywords": self._stock_search_keywords(item["stock_search_keywords"]),
            }
        return updates

    def _visual_asset_type(self, value: Any) -> VisualAssetType:
        try:
            return VisualAssetType(str(value))
        except ValueError as exc:
            raise LLMResponseValidationError(f"unsupported visual_asset_type: {value}") from exc

    def _stock_search_keywords(self, value: Any) -> list[str]:
        if not isinstance(value, list):
            raise LLMResponseValidationError("stock_search_keywords must be a list")
        return [str(keyword) for keyword in value]
