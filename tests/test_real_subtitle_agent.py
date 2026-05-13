import json
import tempfile
import unittest
from pathlib import Path

from backend.src.application.agents.real.subtitle import RealSubtitleAgent
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
    return Storyboard([Scene.minimal("scene_001", 3.0), Scene.minimal("scene_002", 3.0)])


def subtitle_agent_for(payload):
    return RealSubtitleAgent(
        llm_client=FakeLLMClient([json.dumps(payload, ensure_ascii=False)]),
        prompt_loader=FilePromptLoader(Path("prompts")),
        response_validator=JsonResponseValidator(required_fields={"subtitles"}),
    )


class RealSubtitleAgentTests(unittest.TestCase):
    def test_agent_updates_existing_storyboard_by_scene_id(self):
        client = FakeLLMClient(
            [
                json.dumps(
                    {
                        "subtitles": [
                            {
                                "scene_id": "scene_001",
                                "subtitle": "AI 쇼츠 자동화 왜 뜸?",
                                "emphasis_caption": "시간 절약",
                            }
                        ]
                    },
                    ensure_ascii=False,
                )
            ]
        )
        with tempfile.TemporaryDirectory() as directory:
            prompt_file = Path(directory) / "shorts" / "subtitle.md"
            prompt_file.parent.mkdir()
            prompt_file.write_text("# SubtitleAgent\nJSON only.", encoding="utf-8")
            agent = RealSubtitleAgent(
                llm_client=client,
                prompt_loader=FilePromptLoader(Path(directory)),
                response_validator=JsonResponseValidator(required_fields={"subtitles"}),
            )

            updated = agent.apply(project(), script(), storyboard())

        self.assertEqual(updated.scenes[0].subtitle, "AI 쇼츠 자동화 왜 뜸?")
        self.assertEqual(updated.scenes[0].emphasis_caption, "시간 절약")
        self.assertEqual(updated.scenes[1].subtitle, storyboard().scenes[1].subtitle)
        self.assertIn("AI shorts automation", client.prompts[0])
        self.assertIn("scene_001", client.prompts[0])

    def test_agent_rejects_missing_subtitles(self):
        agent = subtitle_agent_for({"items": []})

        with self.assertRaisesRegex(ValueError, "missing required field"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_missing_scene_id(self):
        agent = subtitle_agent_for(
            {"subtitles": [{"subtitle": "text", "emphasis_caption": "emphasis"}]}
        )

        with self.assertRaisesRegex(LLMResponseValidationError, "scene_id"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_missing_subtitle(self):
        agent = subtitle_agent_for(
            {"subtitles": [{"scene_id": "scene_001", "emphasis_caption": "emphasis"}]}
        )

        with self.assertRaisesRegex(LLMResponseValidationError, "subtitle"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_missing_emphasis_caption(self):
        agent = subtitle_agent_for(
            {"subtitles": [{"scene_id": "scene_001", "subtitle": "text"}]}
        )

        with self.assertRaisesRegex(LLMResponseValidationError, "emphasis_caption"):
            agent.apply(project(), script(), storyboard())

    def test_agent_rejects_unknown_scene_id(self):
        agent = subtitle_agent_for(
            {
                "subtitles": [
                    {
                        "scene_id": "scene_999",
                        "subtitle": "text",
                        "emphasis_caption": "emphasis",
                    }
                ]
            }
        )

        with self.assertRaisesRegex(LLMResponseValidationError, "unknown scene_id"):
            agent.apply(project(), script(), storyboard())


if __name__ == "__main__":
    unittest.main()
