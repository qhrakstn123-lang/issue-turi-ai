from __future__ import annotations

from backend.src.domain.models import ContentProject


class InMemoryProjectRepository:
    def __init__(self) -> None:
        self._projects: dict[str, ContentProject] = {}

    def save(self, project: ContentProject) -> ContentProject:
        self._projects[project.project_id] = project
        return project

    def get(self, project_id: str) -> ContentProject:
        try:
            return self._projects[project_id]
        except KeyError as exc:
            raise KeyError(f"project not found: {project_id}") from exc

    def list(self) -> list[ContentProject]:
        return list(self._projects.values())
