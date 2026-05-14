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
        storyboard = self._agents.editing_direction.apply(project, script, storyboard)
        safety = self._agents.safety_review.review(project, script, storyboard)

        return GenerationResult(
            project_id=project.project_id,
            video_script=script,
            storyboard=storyboard,
            safety_status=safety.status,
            safety_notes=safety.notes,
            copyright_risks=safety.copyright_risks,
            rumor_or_defamation_risks=safety.rumor_or_defamation_risks,
            privacy_or_portrait_risks=safety.privacy_or_portrait_risks,
            source_usage_risks=safety.source_usage_risks,
            required_human_review=safety.required_human_review,
            recommended_revisions=safety.recommended_revisions,
        )
