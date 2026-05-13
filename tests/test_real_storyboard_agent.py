import json
import tempfile
import unittest
from pathlib import Path

from backend.src.application.agents.fake_agents import (
    FakeEditingDirectionAgent,
    FakeSubtitleAgent,
    FakeVisualAssetSuggestionAgent,
)
from backend.src.application.agents.interfaces import ShortsAgentBundle
from backend.src.application.agents.real.script_writer import RealScriptWriterAgent
from backend.src.application.agents.real.storyboard import RealStoryboardAgent
from backend.src.application.agents.validation import (
    JsonResponseValidator,
    LLMResponseValidationError,
)
from backend.src.application.pipelines.shorts_generation import ShortsGenerationPipeline
from backend.src.domain.models import ContentProject, OutputFormat, SafetyStatus, VideoScript
from backend.src.infrastructure.llm.fake_client import FakeLLMClient
from backend.src.infrastructure.prompts.file_prompt_loader import FilePromptLoader


def scene_json(**overrides):
    scene = {
        "scene_id": "scene_001",
        "scene_purpose": "hook",
        "narration": "This issue is drawing attention.",
        "tts_text": "This issue is drawing attention.",
        "subtitle": "",
        "emphasis_caption": "",
        "visual_asset_type": "image",
        "visual_description": "",
        "generated_image_prompt": "",
        "gif_or_clip_suggestion": "none",
        "stock_search_keywords": ["issue", "shorts"],
        "motion_direction": "zoom_in",
        "transition": "quick_cut",
        "sound_effect_hint": "pop",
        "estimated_duration": 3.0,
        "editing_notes": "",
        "copyright_safety_note": "",
    }
    scene.update(overrides)
    return scene


def project():
    return ContentProject.create(
        topic="cafe order issue",
        target_audience="shorts viewers",
        tone="fast",
        style_template_id="issue_turi_basic",
        video_length_seconds=45,
        output_format=OutputFormat.YOUTUBE_SHORTS,
    )


def storyboard_agent_for(payload):
    return RealStoryboardAgent(
        llm_client=FakeLLMClient([json.dumps(payload, ensure_ascii=False)]),
        prompt_loader=FilePromptLoader(Path("prompts")),
        response_validator=JsonResponseValidator(required_fields={"scenes"}),
    )


class RealStoryboardAgentTests(unittest.TestCase):
    def test_agent_builds_prompt_and_converts_valid_llm_json_to_storyboard(self):
        script = VideoScript(
            title="Cafe order issue in one minute",
            narration="Quickly explain the core issue.",
            target_duration_seconds=45,
            style_notes=["Hook in the first three seconds"],
        )
        client = FakeLLMClient([json.dumps({"scenes": [scene_json()]}, ensure_ascii=False)])
        with tempfile.TemporaryDirectory() as directory:
            prompt_file = Path(directory) / "shorts" / "storyboard.md"
            prompt_file.parent.mkdir()
            prompt_file.write_text("# StoryboardAgent\nJSON only.", encoding="utf-8")
            agent = RealStoryboardAgent(
                llm_client=client,
                prompt_loader=FilePromptLoader(Path(directory)),
                response_validator=JsonResponseValidator(required_fields={"scenes"}),
            )

            storyboard = agent.generate(project(), script)

        self.assertEqual(len(storyboard.scenes), 1)
        self.assertEqual(storyboard.scenes[0].scene_id, "scene_001")
        self.assertEqual(storyboard.scenes[0].visual_asset_type, "image")
        self.assertEqual(len(client.prompts), 1)
        self.assertIn("# StoryboardAgent", client.prompts[0])
        self.assertIn("cafe order issue", client.prompts[0])
        self.assertIn("Cafe order issue in one minute", client.prompts[0])

    def test_agent_converts_numeric_duration_string_to_float(self):
        storyboard = storyboard_agent_for({"scenes": [scene_json(estimated_duration="3.0")]}).generate(
            project(),
            VideoScript("title", "narration", 45, []),
        )

        self.assertEqual(storyboard.scenes[0].estimated_duration, 3.0)

    def test_agent_rejects_non_numeric_duration_string(self):
        agent = storyboard_agent_for({"scenes": [scene_json(estimated_duration="abc")]})

        with self.assertRaisesRegex(LLMResponseValidationError, "estimated_duration"):
            agent.generate(project(), VideoScript("title", "narration", 45, []))

    def test_agent_rejects_invalid_stock_search_keywords_type(self):
        agent = storyboard_agent_for({"scenes": [scene_json(stock_search_keywords="issue")]})

        with self.assertRaisesRegex(LLMResponseValidationError, "stock_search_keywords"):
            agent.generate(project(), VideoScript("title", "narration", 45, []))

    def test_agent_rejects_missing_scenes(self):
        agent = storyboard_agent_for({"items": []})

        with self.assertRaisesRegex(ValueError, "missing required field"):
            agent.generate(project(), VideoScript("title", "narration", 45, []))

    def test_agent_rejects_missing_scene_field(self):
        bad_scene = scene_json()
        del bad_scene["transition"]
        agent = storyboard_agent_for({"scenes": [bad_scene]})

        with self.assertRaisesRegex(ValueError, "missing scene field: transition"):
            agent.generate(project(), VideoScript("title", "narration", 45, []))

    def test_agent_rejects_invalid_scene_enum_value(self):
        agent = storyboard_agent_for({"scenes": [scene_json(transition="spin")]})

        with self.assertRaisesRegex(ValueError, "unsupported transition"):
            agent.generate(project(), VideoScript("title", "narration", 45, []))

    def test_fake_visual_asset_agent_handles_more_scenes_than_type_cycle(self):
        scenes = [scene_json(scene_id=f"scene_{index:03d}") for index in range(1, 11)]
        storyboard = storyboard_agent_for({"scenes": scenes}).generate(
            project(),
            VideoScript("title", "narration", 45, []),
        )

        updated = FakeVisualAssetSuggestionAgent().apply(storyboard)

        self.assertEqual(len(updated.scenes), 10)
        self.assertEqual(updated.scenes[8].visual_asset_type, updated.scenes[0].visual_asset_type)

    def test_mixed_real_storyboard_pipeline_survives_long_storyboard_with_fake_followups(self):
        class SafetyReviewAgent:
            def review(self, project, storyboard):
                return type("Review", (), {"status": SafetyStatus.APPROVED, "notes": []})()

        scenes = [scene_json(scene_id=f"scene_{index:03d}") for index in range(1, 11)]
        with tempfile.TemporaryDirectory() as directory:
            prompt_root = Path(directory)
            shorts = prompt_root / "shorts"
            shorts.mkdir()
            (shorts / "script_writer.md").write_text("# ScriptWriterAgent", encoding="utf-8")
            (shorts / "storyboard.md").write_text("# StoryboardAgent", encoding="utf-8")
            bundle = ShortsAgentBundle(
                script_writer=RealScriptWriterAgent(
                    llm_client=FakeLLMClient(
                        [
                            json.dumps(
                                {
                                    "title": "title",
                                    "narration": "narration",
                                    "target_duration_seconds": 45,
                                    "style_notes": [],
                                },
                                ensure_ascii=False,
                            )
                        ]
                    ),
                    prompt_loader=FilePromptLoader(prompt_root),
                    response_validator=JsonResponseValidator(
                        required_fields={"title", "narration", "target_duration_seconds", "style_notes"}
                    ),
                ),
                storyboard=RealStoryboardAgent(
                    llm_client=FakeLLMClient([json.dumps({"scenes": scenes}, ensure_ascii=False)]),
                    prompt_loader=FilePromptLoader(prompt_root),
                    response_validator=JsonResponseValidator(required_fields={"scenes"}),
                ),
                visual_asset=FakeVisualAssetSuggestionAgent(),
                subtitle=FakeSubtitleAgent(),
                editing_direction=FakeEditingDirectionAgent(),
                safety_review=SafetyReviewAgent(),
            )

            result = ShortsGenerationPipeline(bundle).generate(project())

        self.assertEqual(len(result.storyboard.scenes), 10)
        self.assertEqual(result.storyboard.scenes[9].sound_effect_hint, "whoosh")


if __name__ == "__main__":
    unittest.main()
