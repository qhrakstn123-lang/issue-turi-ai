import json
import tempfile
import unittest
from pathlib import Path

from backend.src.application.agents.real.editing_direction import RealEditingDirectionAgent
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
                subtitle="AI 쇼츠 자동화 왜 뜸?",
                emphasis_caption="시간 절약",
                visual_asset_type="image",
                visual_description="smartphone comments",
                generated_image_prompt="vertical 9:16 smartphone comments",
                stock_search_keywords=["AI automation"],
                sound_effect_asset="sfx/original.wav",
            ),
            Scene.minimal("scene_002", 3.0),
        ]
    )


def editing_payload(**overrides):
    item = {
        "scene_id": "scene_001",
        "motion_direction": "zoom_in",
        "transition": "quick_cut",
        "sound_effect_hint": "pop",
        "editing_notes": "Make the first caption pop and emphasize the keyword.",
    }
    item.update(overrides)
    return {"editing_directions": [item]}


def editing_agent_for(payload):
    return RealEditingDirectionAgent(
        llm_client=FakeLLMClient([json.dumps(payload, ensure_ascii=False)]),
        prompt_loader=FilePromptLoader(Path("prompts")),
        response_validator=JsonResponseValidator(required_fields={"editing_directions"}),
    )


class RealEditingDirectionAgentTests(unittest.TestCase):
    def test_agent_updates_editing_fields_by_scene_id(self):
        client = FakeLLMClient([json.dumps(editing_payload(), ensure_ascii=False)])
        with tempfile.TemporaryDirectory() as directory:
            prompt_file = Path(directory) / "shorts" / "editing_direction.md"
            prompt_file.parent.mkdir()
            prompt_file.write_text("# EditingDirectionAgent\nJSON only.", encoding="utf-8")
            agent = RealEditingDirectionAgent(
                llm_client=client,
                prompt_loader=FilePromptLoader(Path(directory)),
                response_validator=JsonResponseValidator(required_fields={"editing_directions"}),
            )

            updated = agent.apply(project(), script(), storyboard())

        first = updated.scenes[0]
        self.assertEqual(first.motion_direction, "zoom_in")
        self.assertEqual(first.transition, "quick_cut")
        self.assertEqual(first.sound_effect_hint, "pop")
        self.assertEqual(first.editing_notes, "Make the first caption pop and emphasize the keyword.")
        self.assertEqual(first.subtitle, "AI 쇼츠 자동화 왜 뜸?")
        self.assertEqual(first.emphasis_caption, "시간 절약")
        self.assertEqual(first.visual_asset_type, "image")
        self.assertEqual(first.visual_description, "smartphone comments")
        self.assertEqual(first.generated_image_prompt, "vertical 9:16 smartphone comments")
        self.assertEqual(first.stock_search_keywords, ["AI automation"])
        self.assertEqual(first.estimated_duration, 3.0)
        self.assertEqual(first.sound_effect_asset, "sfx/original.wav")
        self.assertIn("AI shorts automation", client.prompts[0])
        self.assertIn("scene_001", client.prompts[0])
        self.assertIn("smartphone comments", client.prompts[0])

    def test_agent_rejects_missing_editing_directions(self):
        agent = editing_agent_for({"items": []})

        with self.assertRaisesRegex(ValueError, "missing required field"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_missing_scene_id(self):
        payload = editing_payload()
        del payload["editing_directions"][0]["scene_id"]
        agent = editing_agent_for(payload)

        with self.assertRaisesRegex(LLMResponseValidationError, "scene_id"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_unknown_scene_id(self):
        agent = editing_agent_for(editing_payload(scene_id="scene_999"))

        with self.assertRaisesRegex(LLMResponseValidationError, "unknown scene_id"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_invalid_motion_direction(self):
        agent = editing_agent_for(editing_payload(motion_direction="spin"))

        with self.assertRaisesRegex(LLMResponseValidationError, "motion_direction"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_invalid_transition(self):
        agent = editing_agent_for(editing_payload(transition="iris_wipe"))

        with self.assertRaisesRegex(LLMResponseValidationError, "transition"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_invalid_sound_effect_hint(self):
        agent = editing_agent_for(editing_payload(sound_effect_hint="explosion"))

        with self.assertRaisesRegex(LLMResponseValidationError, "sound_effect_hint"):
            agent.apply(project(), script(), storyboard())


if __name__ == "__main__":
    unittest.main()
