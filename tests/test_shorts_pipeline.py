import unittest

from backend.src.application.agents.fake_agents import create_fake_agent_bundle
from backend.src.application.agents.interfaces import ShortsAgentBundle
from backend.src.application.pipelines.shorts_generation import ShortsGenerationPipeline
from backend.src.domain.models import ContentProject, OutputFormat, SafetyStatus, Storyboard, VideoScript


class ShortsGenerationPipelineTests(unittest.TestCase):
    def test_pipeline_depends_on_general_agent_bundle(self):
        class ScriptWriter:
            def generate(self, project):
                return VideoScript("title", "narration", project.video_length_seconds, [])

        class StoryboardAgent:
            def generate(self, project, script):
                return Storyboard([])

        class PassthroughAgent:
            def apply(self, storyboard):
                return storyboard

        class SubtitleAgent:
            def apply(self, project, script, storyboard):
                return storyboard

        class SafetyReview:
            def review(self, project, storyboard):
                return type("Review", (), {"status": SafetyStatus.APPROVED, "notes": []})()

        project = ContentProject.create(
            topic="topic",
            target_audience="audience",
            tone="tone",
            style_template_id="issue_turi_basic",
            video_length_seconds=45,
            output_format=OutputFormat.YOUTUBE_SHORTS,
        )
        bundle = ShortsAgentBundle(
            script_writer=ScriptWriter(),
            storyboard=StoryboardAgent(),
            visual_asset=PassthroughAgent(),
            subtitle=SubtitleAgent(),
            editing_direction=PassthroughAgent(),
            safety_review=SafetyReview(),
        )

        result = ShortsGenerationPipeline(bundle).generate(project)

        self.assertEqual(result.project_id, project.project_id)
        self.assertEqual(result.safety_status, SafetyStatus.APPROVED)
        self.assertEqual(result.storyboard.scenes, [])

    def test_pipeline_generates_deterministic_scene_editing_plan(self):
        project = ContentProject.create(
            topic="요즘 커뮤니티에서 논란이 된 카페 주문 사건",
            target_audience="20대 이슈 관심층",
            tone="빠르고 친근한 썰체",
            style_template_id="issue_turi_basic",
            video_length_seconds=48,
            output_format=OutputFormat.YOUTUBE_SHORTS,
        )

        result = ShortsGenerationPipeline(create_fake_agent_bundle()).generate(project)

        self.assertEqual(result.project_id, project.project_id)
        self.assertEqual(result.safety_status, SafetyStatus.APPROVED)
        self.assertEqual(len(result.storyboard.scenes), 8)
        first_scene = result.storyboard.scenes[0]
        self.assertEqual(first_scene.scene_purpose, "hook")
        self.assertEqual(first_scene.motion_direction, "zoom_in")
        self.assertEqual(first_scene.transition, "quick_cut")
        self.assertEqual(first_scene.sound_effect_hint, "pop")
        self.assertIn("카페 주문 사건", result.video_script.title)

    def test_pipeline_marks_rumor_like_topics_for_review(self):
        project = ContentProject.create(
            topic="확인 안 된 루머로 유명인을 비난하는 사건",
            target_audience="20대 이슈 관심층",
            tone="강한 어그로",
            style_template_id="issue_turi_basic",
            video_length_seconds=45,
            output_format=OutputFormat.YOUTUBE_SHORTS,
        )

        result = ShortsGenerationPipeline(create_fake_agent_bundle()).generate(project)

        self.assertEqual(result.safety_status, SafetyStatus.REVIEW_REQUIRED)
        self.assertIn("검토 필요", result.safety_notes[0])


if __name__ == "__main__":
    unittest.main()
