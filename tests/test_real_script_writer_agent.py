import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.src.application.agents.real.script_writer import RealScriptWriterAgent
from backend.src.application.agents.validation import JsonResponseValidator, LLMResponseValidationError
from backend.src.domain.models import ContentProject, OutputFormat
from backend.src.infrastructure.llm.fake_client import FakeLLMClient
from backend.src.infrastructure.llm.openai_client import (
    MissingOpenAIAPIKeyError,
    OpenAILLMClient,
)
from backend.src.infrastructure.llm.settings import LLMProviderSettings
from backend.src.infrastructure.prompts.file_prompt_loader import FilePromptLoader


def project():
    return ContentProject.create(
        topic="카페 주문 사건",
        target_audience="20대 이슈 쇼츠 시청자",
        tone="빠른 말투",
        style_template_id="issue_turi_basic",
        video_length_seconds=45,
        output_format=OutputFormat.YOUTUBE_SHORTS,
    )


def script_agent_for(response: str) -> RealScriptWriterAgent:
    return RealScriptWriterAgent(
        llm_client=FakeLLMClient([response]),
        prompt_loader=FilePromptLoader(Path("prompts")),
        response_validator=JsonResponseValidator(
            required_fields={"title", "narration", "target_duration_seconds", "style_notes"}
        ),
    )


class RealScriptWriterAgentTests(unittest.TestCase):
    def test_agent_builds_prompt_and_converts_valid_llm_json_to_video_script(self):
        project = ContentProject.create(
            topic="카페 주문 논란",
            target_audience="20대 이슈 시청자",
            tone="빠른 말투",
            style_template_id="issue_turi_basic",
            video_length_seconds=45,
            output_format=OutputFormat.YOUTUBE_SHORTS,
        )
        client = FakeLLMClient(
            [
                (
                    '{"title":"카페 주문 논란 1분 정리",'
                    '"narration":"핵심만 빠르게 정리합니다.",'
                    '"target_duration_seconds":45,'
                    '"style_notes":["첫 3초에 훅을 둔다"]}'
                )
            ]
        )
        with tempfile.TemporaryDirectory() as directory:
            prompt_file = Path(directory) / "shorts" / "script_writer.md"
            prompt_file.parent.mkdir()
            prompt_file.write_text("# ScriptWriterAgent\nJSON only.", encoding="utf-8")
            agent = RealScriptWriterAgent(
                llm_client=client,
                prompt_loader=FilePromptLoader(Path(directory)),
                response_validator=JsonResponseValidator(
                    required_fields={"title", "narration", "target_duration_seconds", "style_notes"}
                ),
            )

            script = agent.generate(project)

        self.assertEqual(script.title, "카페 주문 논란 1분 정리")
        self.assertEqual(script.narration, "핵심만 빠르게 정리합니다.")
        self.assertEqual(script.target_duration_seconds, 45)
        self.assertEqual(script.style_notes, ["첫 3초에 훅을 둔다"])
        self.assertEqual(len(client.prompts), 1)
        self.assertIn("# ScriptWriterAgent", client.prompts[0])
        self.assertIn("카페 주문 논란", client.prompts[0])

    def test_agent_accepts_valid_style_notes_list(self):
        agent = script_agent_for(
            (
                '{"title":"카페 주문 사건",'
                '"narration":"핵심만 빠르게 정리합니다.",'
                '"target_duration_seconds":45,'
                '"style_notes":["첫 문장은 강하게","확정되지 않은 정보는 단정하지 않기"]}'
            )
        )

        script = agent.generate(project())

        self.assertEqual(script.style_notes, ["첫 문장은 강하게", "확정되지 않은 정보는 단정하지 않기"])

    def test_agent_rejects_style_notes_string_with_field_name(self):
        agent = script_agent_for(
            (
                '{"title":"카페 주문 사건",'
                '"narration":"핵심만 빠르게 정리합니다.",'
                '"target_duration_seconds":45,'
                '"style_notes":"첫 문장은 강하게"}'
            )
        )

        with self.assertRaisesRegex(LLMResponseValidationError, "style_notes"):
            agent.generate(project())

    def test_agent_rejects_non_string_style_note_item_with_field_name(self):
        agent = script_agent_for(
            (
                '{"title":"카페 주문 사건",'
                '"narration":"핵심만 빠르게 정리합니다.",'
                '"target_duration_seconds":45,'
                '"style_notes":["첫 문장은 강하게", 3]}'
            )
        )

        with self.assertRaisesRegex(LLMResponseValidationError, "style_notes"):
            agent.generate(project())

    def test_agent_rejects_invalid_script_field_types_with_field_names(self):
        invalid_cases = [
            ("title", '{"title":3,"narration":"본문","target_duration_seconds":45,"style_notes":[]}'),
            ("narration", '{"title":"제목","narration":3,"target_duration_seconds":45,"style_notes":[]}'),
            (
                "target_duration_seconds",
                '{"title":"제목","narration":"본문","target_duration_seconds":"forty five","style_notes":[]}',
            ),
        ]

        for field_name, response in invalid_cases:
            with self.subTest(field_name=field_name):
                agent = script_agent_for(response)

                with self.assertRaisesRegex(LLMResponseValidationError, field_name):
                    agent.generate(project())

    def test_script_writer_prompt_requires_style_notes_json_array(self):
        prompt = Path("prompts/shorts/script_writer.md").read_text(encoding="utf-8")

        self.assertIn("style_notes must be a JSON array of strings", prompt)
        self.assertIn("Do not return style_notes as a string", prompt)
        self.assertIn("Do not return style_notes as a markdown list", prompt)
        self.assertIn('"style_notes": [', prompt)
        self.assertIn("Return one JSON object only", prompt)

    def test_llm_provider_settings_defaults_to_fake(self):
        with patch.dict(os.environ, {}, clear=True):
            settings = LLMProviderSettings.from_env()

        self.assertEqual(settings.provider, "fake")
        self.assertIsNone(settings.openai_api_key)

    def test_llm_provider_settings_reads_openai_api_key(self):
        with patch.dict(
            os.environ,
            {"ISSUE_TURI_LLM_PROVIDER": "openai", "OPENAI_API_KEY": "test-key"},
            clear=True,
        ):
            settings = LLMProviderSettings.from_env()

        self.assertEqual(settings.provider, "openai")
        self.assertEqual(settings.openai_api_key, "test-key")

    def test_openai_client_requires_api_key(self):
        with self.assertRaisesRegex(MissingOpenAIAPIKeyError, "OPENAI_API_KEY"):
            OpenAILLMClient(api_key="")


if __name__ == "__main__":
    unittest.main()
