from __future__ import annotations

from backend.src.application.agents.interfaces import ShortsAgentBundle
from backend.src.domain.models import ContentProject, GenerationResult


class ShortsGenerationPipeline:
    def __init__(self, agents: ShortsAgentBundle) -> None:
        self._agents = agents

    def generate(self, project: ContentProject) -> GenerationResult:
        script = self._agents.script_writer.generate(project)
        storyboard = self._agents.storyboard.generate(project, script)
        storyboard = self._agents.visual_asset.apply(project, script, storyboard)
        storyboard = self._agents.subtitle.apply(project, script, storyboard)
        storyboard = self._agents.editing_direction.apply(storyboard)
        safety = self._agents.safety_review.review(project, storyboard)

        return GenerationResult(
            project_id=project.project_id,
            video_script=script,
            storyboard=storyboard,
            safety_status=safety.status,
            safety_notes=safety.notes,
        )
