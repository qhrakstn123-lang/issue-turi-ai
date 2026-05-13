from __future__ import annotations

from pathlib import Path

from backend.src.application.agents.fake_agents import (
    FakeEditingDirectionAgent,
    FakeSafetyReviewAgent,
    FakeStoryboardAgent,
    FakeSubtitleAgent,
    FakeVisualAssetSuggestionAgent,
    create_fake_agent_bundle,
)
from backend.src.application.agents.interfaces import ShortsAgentBundle
from backend.src.application.agents.real.script_writer import RealScriptWriterAgent
from backend.src.application.agents.real.storyboard import RealStoryboardAgent
from backend.src.application.agents.real.subtitle import RealSubtitleAgent
from backend.src.application.agents.validation import JsonResponseValidator
from backend.src.application.pipelines.shorts_generation import ShortsGenerationPipeline
from backend.src.application.services.project_service import ProjectService
from backend.src.infrastructure.database.memory_repository import InMemoryProjectRepository
from backend.src.infrastructure.llm.openai_client import OpenAILLMClient
from backend.src.infrastructure.llm.settings import LLMProviderSettings
from backend.src.infrastructure.prompts.file_prompt_loader import FilePromptLoader
from backend.src.presentation.http.api import IssueTuriApi


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def create_api() -> IssueTuriApi:
    settings = LLMProviderSettings.from_env()
    service = ProjectService(
        repository=InMemoryProjectRepository(),
        shorts_pipeline=ShortsGenerationPipeline(create_agent_bundle(settings)),
    )
    return IssueTuriApi(service)


def create_agent_bundle(settings: LLMProviderSettings) -> ShortsAgentBundle:
    provider = settings.provider.lower()
    if provider == "fake":
        return create_fake_agent_bundle()
    if provider not in {"openai", "real"}:
        raise ValueError(f"unsupported LLM provider: {settings.provider}")

    return ShortsAgentBundle(
        script_writer=RealScriptWriterAgent(
            llm_client=OpenAILLMClient(
                api_key=settings.openai_api_key,
                model=settings.openai_model,
            ),
            prompt_loader=FilePromptLoader(PROJECT_ROOT / "prompts"),
            response_validator=JsonResponseValidator(
                required_fields={
                    "title",
                    "narration",
                    "target_duration_seconds",
                    "style_notes",
                }
            ),
        ),
        storyboard=RealStoryboardAgent(
            llm_client=OpenAILLMClient(
                api_key=settings.openai_api_key,
                model=settings.openai_model,
            ),
            prompt_loader=FilePromptLoader(PROJECT_ROOT / "prompts"),
            response_validator=JsonResponseValidator(required_fields={"scenes"}),
        ),
        visual_asset=FakeVisualAssetSuggestionAgent(),
        subtitle=RealSubtitleAgent(
            llm_client=OpenAILLMClient(
                api_key=settings.openai_api_key,
                model=settings.openai_model,
            ),
            prompt_loader=FilePromptLoader(PROJECT_ROOT / "prompts"),
            response_validator=JsonResponseValidator(required_fields={"subtitles"}),
        ),
        editing_direction=FakeEditingDirectionAgent(),
        safety_review=FakeSafetyReviewAgent(),
    )
