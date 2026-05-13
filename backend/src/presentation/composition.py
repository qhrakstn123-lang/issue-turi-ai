from __future__ import annotations

from backend.src.application.agents.fake_agents import create_fake_agent_bundle
from backend.src.application.pipelines.shorts_generation import ShortsGenerationPipeline
from backend.src.application.services.project_service import ProjectService
from backend.src.infrastructure.database.memory_repository import InMemoryProjectRepository
from backend.src.presentation.http.api import IssueTuriApi


def create_api() -> IssueTuriApi:
    service = ProjectService(
        repository=InMemoryProjectRepository(),
        shorts_pipeline=ShortsGenerationPipeline(create_fake_agent_bundle()),
    )
    return IssueTuriApi(service)
