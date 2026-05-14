from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.src.application.agents.llm import LLMClient
from backend.src.application.agents.prompts import PromptLoader
from backend.src.application.agents.validation import (
    JsonResponseValidator,
    LLMResponseValidationError,
    validate_agent_json_response,
)
from backend.src.domain.models import ContentProject, VideoScript


@dataclass(frozen=True)
class RealScriptWriterAgent:
    llm_client: LLMClient
    prompt_loader: PromptLoader
    response_validator: JsonResponseValidator

    def generate(self, project: ContentProject) -> VideoScript:
        response = self.llm_client.complete(self._build_prompt(project))
        payload = validate_agent_json_response("RealScriptWriterAgent", self.response_validator, response)
        return VideoScript(
            title=self._string_field(payload, "title"),
            narration=self._string_field(payload, "narration"),
            target_duration_seconds=self._duration(payload),
            style_notes=self._style_notes(payload),
        )

    def _build_prompt(self, project: ContentProject) -> str:
        template = self.prompt_loader.load("shorts/script_writer")
        return "\n\n".join(
            [
                template,
                "Project input:",
                f"- topic: {project.topic}",
                f"- target_audience: {project.target_audience}",
                f"- tone: {project.tone}",
                f"- style_template_id: {project.style_template_id}",
                f"- video_length_seconds: {project.video_length_seconds}",
                (
                    "Return JSON only with title, narration, target_duration_seconds, and style_notes. "
                    "style_notes must be a JSON array of strings."
                ),
            ]
        )

    def _string_field(self, payload: dict[str, Any], field_name: str) -> str:
        value = payload[field_name]
        if not isinstance(value, str):
            raise LLMResponseValidationError(f"{field_name} must be a string")
        if not value.strip():
            raise LLMResponseValidationError(f"{field_name} must be a non-empty string")
        return value

    def _duration(self, payload: dict[str, Any]) -> int:
        value = payload["target_duration_seconds"]
        if isinstance(value, bool) or not isinstance(value, int):
            raise LLMResponseValidationError("target_duration_seconds must be an integer")
        return value

    def _style_notes(self, payload: dict[str, Any]) -> list[str]:
        style_notes = payload["style_notes"]
        if not isinstance(style_notes, list):
            raise LLMResponseValidationError("style_notes must be a JSON array of strings")
        notes: list[str] = []
        for index, note in enumerate(style_notes):
            if not isinstance(note, str):
                raise LLMResponseValidationError(f"style_notes[{index}] must be a string")
            notes.append(note)
        return notes
