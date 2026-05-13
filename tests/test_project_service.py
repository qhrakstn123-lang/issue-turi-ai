import unittest

from backend.src.application.agents.fake_agents import create_fake_agent_bundle
from backend.src.application.pipelines.shorts_generation import ShortsGenerationPipeline
from backend.src.application.services.project_service import ProjectService
from backend.src.domain.models import OutputFormat, ProjectStatus
from backend.src.infrastructure.database.memory_repository import InMemoryProjectRepository


class ProjectServiceTests(unittest.TestCase):
    def test_create_generate_and_update_project(self):
        service = ProjectService(
            repository=InMemoryProjectRepository(),
            shorts_pipeline=ShortsGenerationPipeline(create_fake_agent_bundle()),
        )

        project = service.create_project(
            topic="한 브랜드 공지문 때문에 댓글이 갈린 사건",
            target_audience="이슈 쇼츠 시청자",
            tone="빠른 썰체",
            style_template_id="issue_turi_basic",
            video_length_seconds=50,
            output_format=OutputFormat.YOUTUBE_SHORTS,
        )
        result = service.generate_shorts_plan(project.project_id)
        updated = service.update_scene(
            project.project_id,
            "scene_001",
            subtitle="댓글 갈린 공지",
            motion_direction="shake",
        )

        self.assertEqual(result.project_id, project.project_id)
        self.assertEqual(updated.status, ProjectStatus.READY_FOR_REVIEW)
        self.assertEqual(updated.generation_result.storyboard.scenes[0].subtitle, "댓글 갈린 공지")
        self.assertEqual(updated.generation_result.storyboard.scenes[0].motion_direction, "shake")


if __name__ == "__main__":
    unittest.main()
