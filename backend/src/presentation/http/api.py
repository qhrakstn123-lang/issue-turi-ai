from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any

from backend.src.application.services.project_service import ProjectService
from backend.src.domain.models import OutputFormat


class IssueTuriApi:
    def __init__(self, service: ProjectService) -> None:
        self._service = service

    def handle(self, method: str, path: str, body: dict[str, Any] | None) -> tuple[int, dict[str, Any]]:
        try:
            return self._handle(method.upper(), path, body or {})
        except (KeyError, ValueError) as exc:
            return 400, {"error": str(exc)}

    def _handle(self, method: str, path: str, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        if method == "POST" and path == "/api/projects":
            project = self._service.create_project(
                topic=str(body.get("topic", "")),
                target_audience=str(body.get("target_audience", "")),
                tone=str(body.get("tone", "")),
                style_template_id=str(body.get("style_template_id", "issue_turi_basic")),
                video_length_seconds=int(body.get("video_length_seconds", 50)),
                output_format=OutputFormat(str(body.get("output_format", "youtube_shorts"))),
            )
            return 201, {"project": to_json(project)}

        if method == "GET" and path == "/api/projects":
            return 200, {"projects": [to_json(project) for project in self._service.list_projects()]}

        if method == "POST" and path == "/api/generate/shorts-plan":
            result = self._service.generate_shorts_plan(str(body["project_id"]))
            return 200, {"result": to_json(result)}

        if path.startswith("/api/projects/"):
            project_id = path.removeprefix("/api/projects/")
            if method == "GET":
                return 200, {"project": to_json(self._service.get_project(project_id))}
            if method == "PATCH":
                scene_id = str(body.pop("scene_id"))
                project = self._service.update_scene(project_id, scene_id, **body)
                return 200, {"project": to_json(project)}

        return 404, {"error": f"route not found: {method} {path}"}


def to_json(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {field.name: to_json(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, list):
        return [to_json(item) for item in value]
    if isinstance(value, dict):
        return {key: to_json(item) for key, item in value.items()}
    return value
