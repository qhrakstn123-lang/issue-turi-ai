import json
import tempfile
import unittest
from pathlib import Path

from backend.src.application.agents.real.visual_asset import RealVisualAssetSuggestionAgent
from backend.src.application.agents.validation import (
    JsonResponseValidator,
    LLMResponseValidationError,
)
from backend.src.domain.models import ContentProject, OutputFormat, Scene, Storyboard, VideoScript
from backend.src.infrastructure.llm.fake_client import FakeLLMClient
from backend.src.infrastructure.prompts.file_prompt_loader import FilePromptLoader


def project():
    return ContentProject.create(
        topic="AI shorts automation",
        target_audience="creators",
        tone="fast",
        style_template_id="issue_turi_basic",
        video_length_seconds=45,
        output_format=OutputFormat.YOUTUBE_SHORTS,
    )


def script():
    return VideoScript(
        title="AI shorts automation",
        narration="Explain why automation matters.",
        target_duration_seconds=45,
        style_notes=["short captions"],
    )


def storyboard():
    return Storyboard(
        [
            Scene.minimal("scene_001", 3.0).update(
                subtitle="original subtitle",
                emphasis_caption="original emphasis",
                motion_direction="shake",
                transition="fade",
                sound_effect_hint="click",
            ),
            Scene.minimal("scene_002", 3.0),
        ]
    )


def visual_payload(**overrides):
    item = {
        "scene_id": "scene_001",
        "visual_asset_type": "image",
        "visual_description": "smartphone screen with fast Korean comments about AI shorts automation",
        "generated_image_prompt": "vertical 9:16 smartphone screen, Korean comments, AI content automation",
        "gif_or_clip_suggestion": "typing comments animation",
        "stock_search_keywords": ["AI automation", "shorts editing", "social media comments"],
        "visual_source_strategy": "reference_capture",
        "capture_source_type": "community",
        "capture_usage_mode": "mockup_recommended",
        "asset_usage_note": "Use a self-made community-style mockup and avoid exposing real usernames or comments.",
    }
    item.update(overrides)
    return {"visuals": [item]}


def visual_agent_for(payload):
    return RealVisualAssetSuggestionAgent(
        llm_client=FakeLLMClient([json.dumps(payload, ensure_ascii=False)]),
        prompt_loader=FilePromptLoader(Path("prompts")),
        response_validator=JsonResponseValidator(required_fields={"visuals"}),
    )


class RealVisualAssetSuggestionAgentTests(unittest.TestCase):
    def test_visual_prompt_prioritizes_reference_capture_when_source_context_matters(self):
        prompt = Path("prompts/shorts/visual_prompt.md").read_text(encoding="utf-8")

        self.assertIn("reference_capture first", prompt)
        self.assertIn("direct_capture_candidate means candidate only", prompt)
        self.assertIn("community -> reference_capture + community", prompt)
        self.assertIn("news -> reference_capture + news", prompt)
        self.assertIn("youtube -> reference_capture + youtube", prompt)
        self.assertIn("broadcast -> reference_capture + broadcast", prompt)
        self.assertIn("instagram -> reference_capture + instagram", prompt)
        self.assertIn("google_image -> reference_capture + google_image", prompt)
        self.assertIn("google_image: license_required", prompt)
        self.assertIn("Blur or reconstruct usernames", prompt)

    def test_agent_updates_visual_fields_by_scene_id(self):
        client = FakeLLMClient([json.dumps(visual_payload(), ensure_ascii=False)])
        with tempfile.TemporaryDirectory() as directory:
            prompt_file = Path(directory) / "shorts" / "visual_prompt.md"
            prompt_file.parent.mkdir()
            prompt_file.write_text("# VisualPromptAgent\nJSON only.", encoding="utf-8")
            agent = RealVisualAssetSuggestionAgent(
                llm_client=client,
                prompt_loader=FilePromptLoader(Path(directory)),
                response_validator=JsonResponseValidator(required_fields={"visuals"}),
            )

            updated = agent.apply(project(), script(), storyboard())

        first = updated.scenes[0]
        self.assertEqual(first.visual_asset_type, "image")
        self.assertIn("smartphone screen", first.visual_description)
        self.assertIn("vertical 9:16", first.generated_image_prompt)
        self.assertEqual(first.gif_or_clip_suggestion, "typing comments animation")
        self.assertEqual(first.stock_search_keywords, ["AI automation", "shorts editing", "social media comments"])
        self.assertEqual(first.visual_source_strategy, "reference_capture")
        self.assertEqual(first.capture_source_type, "community")
        self.assertEqual(first.capture_usage_mode, "mockup_recommended")
        self.assertIn("avoid exposing real usernames", first.asset_usage_note)
        self.assertEqual(first.subtitle, "original subtitle")
        self.assertEqual(first.emphasis_caption, "original emphasis")
        self.assertEqual(first.motion_direction, "shake")
        self.assertEqual(first.transition, "fade")
        self.assertEqual(first.sound_effect_hint, "click")
        self.assertEqual(first.estimated_duration, 3.0)
        self.assertIn("AI shorts automation", client.prompts[0])
        self.assertIn("scene_001", client.prompts[0])

    def test_agent_rejects_missing_visuals(self):
        agent = visual_agent_for({"items": []})

        with self.assertRaisesRegex(ValueError, "missing required field"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_missing_scene_id(self):
        payload = visual_payload()
        del payload["visuals"][0]["scene_id"]
        agent = visual_agent_for(payload)

        with self.assertRaisesRegex(LLMResponseValidationError, "scene_id"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_unknown_scene_id(self):
        agent = visual_agent_for(visual_payload(scene_id="scene_999"))

        with self.assertRaisesRegex(LLMResponseValidationError, "unknown scene_id"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_invalid_visual_asset_type(self):
        agent = visual_agent_for(visual_payload(visual_asset_type="poster"))

        with self.assertRaisesRegex(LLMResponseValidationError, "visual_asset_type"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_invalid_visual_source_strategy(self):
        agent = visual_agent_for(visual_payload(visual_source_strategy="copied_screenshot"))

        with self.assertRaisesRegex(LLMResponseValidationError, "visual_source_strategy"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_invalid_capture_source_type(self):
        agent = visual_agent_for(visual_payload(capture_source_type="forum"))

        with self.assertRaisesRegex(LLMResponseValidationError, "capture_source_type"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_invalid_capture_usage_mode(self):
        agent = visual_agent_for(visual_payload(capture_usage_mode="free_to_use"))

        with self.assertRaisesRegex(LLMResponseValidationError, "capture_usage_mode"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_missing_asset_usage_note(self):
        payload = visual_payload()
        del payload["visuals"][0]["asset_usage_note"]
        agent = visual_agent_for(payload)

        with self.assertRaisesRegex(LLMResponseValidationError, "asset_usage_note"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_missing_visual_sourcing_fields_with_field_names(self):
        for field_name in [
            "visual_source_strategy",
            "capture_source_type",
            "capture_usage_mode",
            "asset_usage_note",
        ]:
            with self.subTest(field_name=field_name):
                payload = visual_payload()
                del payload["visuals"][0][field_name]
                agent = visual_agent_for(payload)

                with self.assertRaisesRegex(LLMResponseValidationError, field_name):
                    agent.apply(project(), script(), storyboard())

    def test_agent_rejects_empty_asset_usage_note(self):
        agent = visual_agent_for(visual_payload(asset_usage_note=" "))

        with self.assertRaisesRegex(LLMResponseValidationError, "asset_usage_note"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_invalid_stock_search_keywords_type(self):
        agent = visual_agent_for(visual_payload(stock_search_keywords="AI automation"))

        with self.assertRaisesRegex(LLMResponseValidationError, "stock_search_keywords"):
            agent.apply(project(), script(), storyboard())


if __name__ == "__main__":
    unittest.main()
