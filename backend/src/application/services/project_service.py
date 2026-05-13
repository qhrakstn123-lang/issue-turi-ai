from __future__ import annotations

from typing import Any, Protocol

from backend.src.application.pipelines.shorts_generation import ShortsGenerationPipeline
from backend.src.domain.models import ContentProject, OutputFormat


class ProjectRepository(Protocol):
    def save(self, project: ContentProject) -> ContentProject:
        ...

    def get(self, project_id: str) -> ContentProject:
        ...

    def list(self) -> list[ContentProject]:
        ...


class ProjectService:
    def __init__(self, repository: ProjectRepository, shorts_pipeline: ShortsGenerationPipeline) -> None:
        self._repository = repository
        self._shorts_pipeline = shorts_pipeline

    def create_project(
        self,
        topic: str,
        target_audience: str,
        tone: str,
        style_template_id: str,
        video_length_seconds: int,
        output_format: OutputFormat,
    ) -> ContentProject:
        project = ContentProject.create(
            topic=topic,
            target_audience=target_audience,
            tone=tone,
            style_template_id=style_template_id,
            video_length_seconds=video_length_seconds,
            output_format=output_format,
        )
        return self._repository.save(project)

    def generate_shorts_plan(self, project_id: str):
        project = self._repository.get(project_id)
        result = self._shorts_pipeline.generate(project)
        self._repository.save(project.with_generation_result(result))
        return result

    def update_scene(self, project_id: str, scene_id: str, **changes: Any) -> ContentProject:
        project = self._repository.get(project_id)
        if project.generation_result is None:
            raise ValueError("project has no generation result")
        updated_result = project.generation_result.update_scene(scene_id, **changes)
        updated_project = project.with_generation_result(updated_result)
        return self._repository.save(updated_project)

    def get_project(self, project_id: str) -> ContentProject:
        return self._repository.get(project_id)

    def list_projects(self) -> list[ContentProject]:
        return self._repository.list()
