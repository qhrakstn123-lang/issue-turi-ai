import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.src.application.agents.real.script_writer import RealScriptWriterAgent
from backend.src.application.agents.validation import JsonResponseValidator
from backend.src.domain.models import ContentProject, OutputFormat
from backend.src.infrastructure.llm.fake_client import FakeLLMClient
from backend.src.infrastructure.llm.openai_client import (
    MissingOpenAIAPIKeyError,
    OpenAILLMClient,
)
from backend.src.infrastructure.llm.settings import LLMProviderSettings
from backend.src.infrastructure.prompts.file_prompt_loader import FilePromptLoader


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
