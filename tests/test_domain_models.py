import unittest

from backend.src.domain.models import (
    BeatType,
    ContentProject,
    MotionDirection,
    OutputFormat,
    ProjectStatus,
    Scene,
    SoundEffectHint,
    Timeline,
    Transition,
    VisualAssetType,
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

    def test_scene_normalizes_allowed_string_values_to_enums(self):
        scene = Scene.minimal(scene_id="scene_001", estimated_duration=3.0)

        self.assertEqual(scene.visual_asset_type, VisualAssetType.IMAGE)
        self.assertEqual(scene.motion_direction, MotionDirection.ZOOM_IN)
        self.assertEqual(scene.transition, Transition.QUICK_CUT)
        self.assertEqual(scene.sound_effect_hint, SoundEffectHint.POP)

    def test_scene_rejects_unsupported_allowed_values(self):
        with self.assertRaises(ValueError):
            Scene.minimal(scene_id="scene_001", estimated_duration=3.0).update(
                visual_asset_type="unsupported"
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

    def test_timeline_adds_production_beats_for_shorts_structure(self):
        scenes = [
            Scene.minimal(scene_id="scene_001", estimated_duration=3.0).update(
                scene_purpose="hook",
                emphasis_caption="watch this first",
            ),
            Scene.minimal(scene_id="scene_002", estimated_duration=3.0).update(
                scene_purpose="reaction",
                emphasis_caption="comments split",
            ),
            Scene.minimal(scene_id="scene_003", estimated_duration=3.0).update(
                scene_purpose="turning_point",
                emphasis_caption="context changed",
            ),
            Scene.minimal(scene_id="scene_004", estimated_duration=3.0).update(
                scene_purpose="conclusion",
                emphasis_caption="final point",
            ),
        ]

        timeline = Timeline.from_scenes("project_001", OutputFormat.YOUTUBE_SHORTS, scenes)

        self.assertEqual(timeline.scenes[0].beats[0].beat_type, BeatType.HOOK)
        self.assertIn(BeatType.REACTION, [beat.beat_type for beat in timeline.scenes[1].beats])
        self.assertIn(BeatType.TURNING_POINT, [beat.beat_type for beat in timeline.scenes[2].beats])
        self.assertIn(BeatType.PAYOFF, [beat.beat_type for beat in timeline.scenes[3].beats])
        self.assertEqual(timeline.scenes[-1].beats[-1].beat_type, BeatType.CTA)

    def test_timeline_adds_evidence_beat_for_sourced_visuals(self):
        scene = Scene.minimal(scene_id="scene_001", estimated_duration=4.0).update(
            visual_source_strategy="reference_capture",
            capture_source_type="community",
            capture_usage_mode="mockup_recommended",
            asset_usage_note="Use a self-made mockup instead of copying a real post.",
        )

        timeline_scene = Timeline.from_scenes("project_001", OutputFormat.YOUTUBE_SHORTS, [scene]).scenes[0]

        evidence = [beat for beat in timeline_scene.beats if beat.beat_type == BeatType.EVIDENCE]
        self.assertEqual(len(evidence), 1)
        self.assertIn("reference_capture", evidence[0].note)
        self.assertIn("community", evidence[0].note)

    def test_timeline_beat_times_stay_inside_scene_range(self):
        scene = Scene.minimal(scene_id="scene_001", estimated_duration=5.0).update(
            scene_purpose="reaction",
            visual_source_strategy="mockup",
            capture_source_type="instagram",
            capture_usage_mode="mockup_recommended",
        )

        timeline_scene = Timeline.from_scenes("project_001", OutputFormat.YOUTUBE_SHORTS, [scene]).scenes[0]

        for beat in timeline_scene.beats:
            with self.subTest(beat=beat.beat_type):
                self.assertGreaterEqual(beat.start_time, timeline_scene.start_time)
                self.assertLessEqual(beat.end_time, timeline_scene.end_time)
                self.assertLessEqual(beat.start_time, beat.end_time)

    def test_timeline_asset_review_checklist_reflects_capture_source_type(self):
        scenes = [
            Scene.minimal(scene_id="scene_001", estimated_duration=3.0).update(
                capture_source_type="community",
                asset_usage_note="Blur post author.",
            ),
            Scene.minimal(scene_id="scene_002", estimated_duration=3.0).update(
                capture_source_type="youtube",
                capture_usage_mode="permission_required",
                asset_usage_note="Confirm clip permission.",
            ),
            Scene.minimal(scene_id="scene_003", estimated_duration=3.0).update(
                capture_source_type="google_image",
                capture_usage_mode="license_required",
                asset_usage_note="Check image license.",
            ),
            Scene.minimal(scene_id="scene_004", estimated_duration=3.0).update(
                capture_source_type="stock_site",
                asset_usage_note="Check stock license.",
            ),
            Scene.minimal(scene_id="scene_005", estimated_duration=3.0).update(
                capture_source_type="ai_generated",
                asset_usage_note="Avoid real person resemblance.",
            ),
            Scene.minimal(scene_id="scene_006", estimated_duration=3.0).update(
                capture_source_type="user_provided",
                asset_usage_note="Confirm user permission.",
            ),
        ]

        timeline = Timeline.from_scenes("project_001", OutputFormat.YOUTUBE_SHORTS, scenes)

        self.assertIn("nicknames", " ".join(timeline.scenes[0].asset_review_checklist))
        self.assertIn("permission_required", " ".join(timeline.scenes[1].asset_review_checklist))
        self.assertIn("license_required", " ".join(timeline.scenes[2].asset_review_checklist))
        self.assertIn("model release", " ".join(timeline.scenes[3].asset_review_checklist))
        self.assertIn("real person", " ".join(timeline.scenes[4].asset_review_checklist))
        self.assertIn("usage rights", " ".join(timeline.scenes[5].asset_review_checklist))

    def test_timeline_asset_review_checklist_marks_avoid_usage(self):
        scene = Scene.minimal(scene_id="scene_001", estimated_duration=3.0).update(
            capture_usage_mode="avoid",
            asset_usage_note="Do not use this source.",
        )

        timeline_scene = Timeline.from_scenes("project_001", OutputFormat.YOUTUBE_SHORTS, [scene]).scenes[0]

        self.assertIn("Do not use", " ".join(timeline_scene.asset_review_checklist))


if __name__ == "__main__":
    unittest.main()
