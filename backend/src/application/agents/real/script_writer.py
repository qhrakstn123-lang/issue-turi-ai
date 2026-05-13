from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.src.application.agents.llm import LLMClient
from backend.src.application.agents.prompts import PromptLoader
from backend.src.application.agents.validation import JsonResponseValidator
from backend.src.domain.models import ContentProject, VideoScript


@dataclass(frozen=True)
class RealScriptWriterAgent:
    llm_client: LLMClient
    prompt_loader: PromptLoader
    response_validator: JsonResponseValidator

    def generate(self, project: ContentProject) -> VideoScript:
        response = self.llm_client.complete(self._build_prompt(project))
        payload = self.response_validator.validate(response)
        return VideoScript(
            title=str(payload["title"]),
            narration=str(payload["narration"]),
            target_duration_seconds=int(payload["target_duration_seconds"]),
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
                "Return JSON only with title, narration, target_duration_seconds, and style_notes.",
            ]
        )

    def _style_notes(self, payload: dict[str, Any]) -> list[str]:
        style_notes = payload["style_notes"]
        if not isinstance(style_notes, list):
            raise ValueError("style_notes must be a list")
        return [str(note) for note in style_notes]
