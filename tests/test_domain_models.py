import unittest

from backend.src.domain.models import (
    ContentProject,
    OutputFormat,
    ProjectStatus,
    Scene,
    Timeline,
)


class DomainModelTests(unittest.TestCase):
    def test_content_project_accepts_only_supported_output_formats(self):
        project = ContentProject.create(
            topic="커뮤니티에서 갑자기 화제가 된 사건",
            target_audience="20대 이슈 관심층",
            tone="빠른 썰체",
            style_template_id="issue_turi_basic",
            video_length_seconds=50,
            output_format=OutputFormat.YOUTUBE_SHORTS,
        )

        self.assertEqual(project.output_format, OutputFormat.YOUTUBE_SHORTS)
        self.assertEqual(project.status, ProjectStatus.DRAFT)
        self.assertEqual(project.video_length_seconds, 50)

    def test_scene_rejects_invalid_estimated_duration(self):
        with self.assertRaises(ValueError):
            Scene(
                scene_id="scene_001",
                scene_purpose="hook",
                narration="짧은 훅",
                tts_text="짧은 훅",
                subtitle="짧은 훅",
                emphasis_caption="훅",
                visual_asset_type="image",
                visual_description="스마트폰 댓글 화면",
                generated_image_prompt="Korean community comment screen",
                gif_or_clip_suggestion="none",
                stock_search_keywords=["community", "comments"],
                motion_direction="zoom_in",
                transition="quick_cut",
                sound_effect_hint="pop",
                estimated_duration=1.0,
                editing_notes="자막을 크게 등장",
                copyright_safety_note="직접 생성 이미지 사용",
            )

    def test_timeline_uses_scene_durations_in_order(self):
        scenes = [
            Scene.minimal(scene_id="scene_001", estimated_duration=3.0),
            Scene.minimal(scene_id="scene_002", estimated_duration=4.0),
        ]

        timeline = Timeline.from_scenes("project_001", OutputFormat.YOUTUBE_SHORTS, scenes)

        self.assertEqual(timeline.total_duration, 7.0)
        self.assertEqual(timeline.scenes[0].start_time, 0.0)
        self.assertEqual(timeline.scenes[0].end_time, 3.0)
        self.assertEqual(timeline.scenes[1].start_time, 3.0)
        self.assertEqual(timeline.scenes[1].end_time, 7.0)


if __name__ == "__main__":
    unittest.main()
