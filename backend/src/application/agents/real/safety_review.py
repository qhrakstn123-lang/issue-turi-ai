from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.src.application.agents.interfaces import SafetyReview
from backend.src.application.agents.llm import LLMClient
from backend.src.application.agents.prompts import PromptLoader
from backend.src.application.agents.validation import (
    JsonResponseValidator,
    LLMResponseValidationError,
    validate_agent_json_response,
)
from backend.src.domain.models import ContentProject, SafetyStatus, Storyboard, VideoScript


SAFETY_FIELDS = {
    "safety_status",
    "safety_notes",
    "copyright_risks",
    "rumor_or_defamation_risks",
    "privacy_or_portrait_risks",
    "source_usage_risks",
    "required_human_review",
    "recommended_revisions",
}


@dataclass(frozen=True)
class RealSafetyReviewAgent:
    llm_client: LLMClient
    prompt_loader: PromptLoader
    response_validator: JsonResponseValidator

    def review(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> SafetyReview:
        response = self.llm_client.complete(self._build_prompt(project, script, storyboard))
        payload = validate_agent_json_response("RealSafetyReviewAgent", self.response_validator, response)
        self._reject_extra_keys(payload)
        return SafetyReview(
            status=self._safety_status(payload["safety_status"]),
            notes=self._string_list(payload["safety_notes"], "safety_notes"),
            copyright_risks=self._string_list(payload["copyright_risks"], "copyright_risks"),
            rumor_or_defamation_risks=self._string_list(
                payload["rumor_or_defamation_risks"],
                "rumor_or_defamation_risks",
            ),
            privacy_or_portrait_risks=self._string_list(
                payload["privacy_or_portrait_risks"],
                "privacy_or_portrait_risks",
            ),
            source_usage_risks=self._string_list(payload["source_usage_risks"], "source_usage_risks"),
            required_human_review=self._required_human_review(payload["required_human_review"]),
            recommended_revisions=self._string_list(payload["recommended_revisions"], "recommended_revisions"),
        )

    def _build_prompt(self, project: ContentProject, script: VideoScript, storyboard: Storyboard) -> str:
        template = self.prompt_loader.load("safety/review")
        scene_lines = [
            (
                f"- {scene.scene_id}: purpose={scene.scene_purpose}; "
                f"narration={scene.narration}; subtitle={scene.subtitle}; "
                f"emphasis_caption={scene.emphasis_caption}; "
                f"visual_source_strategy={scene.visual_source_strategy}; "
                f"capture_source_type={scene.capture_source_type}; "
                f"capture_usage_mode={scene.capture_usage_mode}; "
                f"asset_usage_note={scene.asset_usage_note}; "
                f"visual_description={scene.visual_description}; "
                f"generated_image_prompt={scene.generated_image_prompt}; "
                f"editing_notes={scene.editing_notes}; "
                f"copyright_safety_note={scene.copyright_safety_note}"
            )
            for scene in storyboard.scenes
        ]
        return "\n\n".join(
            [
                template,
                "You are not a legal judge. Flag safety, rights, rumor, defamation, privacy, portrait, and source usage risks for human review.",
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
                "Return JSON only with exactly these top-level keys: "
                + ", ".join(sorted(SAFETY_FIELDS))
                + ".",
            ]
        )

    def _reject_extra_keys(self, payload: dict[str, Any]) -> None:
        extra_keys = sorted(set(payload) - SAFETY_FIELDS)
        if extra_keys:
            raise LLMResponseValidationError(f"unexpected field: {extra_keys[0]}")

    def _safety_status(self, value: Any) -> SafetyStatus:
        try:
            return SafetyStatus(str(value))
        except ValueError as exc:
            raise LLMResponseValidationError(f"unsupported safety_status: {value}") from exc

    def _required_human_review(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise LLMResponseValidationError("required_human_review must be a boolean")
        return value

    def _string_list(self, value: Any, field_name: str) -> list[str]:
        if not isinstance(value, list):
            raise LLMResponseValidationError(f"{field_name} must be a list")
        if not all(isinstance(item, str) for item in value):
            raise LLMResponseValidationError(f"{field_name} must contain only strings")
        return value
