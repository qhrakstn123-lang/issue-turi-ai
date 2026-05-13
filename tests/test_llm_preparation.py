import unittest
from pathlib import Path

from backend.src.application.agents.llm import LLMClient
from backend.src.application.agents.validation import (
    JsonResponseValidator,
    LLMResponseValidationError,
)
from backend.src.infrastructure.llm.fake_client import FakeLLMClient
from backend.src.infrastructure.prompts.file_prompt_loader import FilePromptLoader


class LLMPreparationTests(unittest.TestCase):
    def test_fake_llm_client_returns_configured_responses_and_records_prompts(self):
        client: LLMClient = FakeLLMClient(['{"title": "ok"}'])

        response = client.complete("prompt text")

        self.assertEqual(response, '{"title": "ok"}')
        self.assertEqual(client.prompts, ["prompt text"])

    def test_file_prompt_loader_reads_prompt_by_name(self):
        loader = FilePromptLoader(Path("prompts"))

        prompt = loader.load("shorts/script_writer")

        self.assertIn("ScriptWriterAgent", prompt)

    def test_json_response_validator_parses_valid_payload(self):
        validator = JsonResponseValidator(
            required_fields={"visual_asset_type"},
            enum_fields={"visual_asset_type": {"image", "text_only"}},
        )

        payload = validator.validate('{"visual_asset_type": "image"}')

        self.assertEqual(payload["visual_asset_type"], "image")

    def test_json_response_validator_rejects_empty_response(self):
        validator = JsonResponseValidator(required_fields={"title"})

        with self.assertRaisesRegex(LLMResponseValidationError, "empty"):
            validator.validate("")

    def test_json_response_validator_rejects_invalid_json(self):
        validator = JsonResponseValidator(required_fields={"title"})

        with self.assertRaisesRegex(LLMResponseValidationError, "invalid JSON"):
            validator.validate("{not-json")

    def test_json_response_validator_rejects_missing_required_fields(self):
        validator = JsonResponseValidator(required_fields={"title", "narration"})

        with self.assertRaisesRegex(LLMResponseValidationError, "missing required field"):
            validator.validate('{"title": "ok"}')

    def test_json_response_validator_rejects_unknown_enum_value(self):
        validator = JsonResponseValidator(
            required_fields={"transition"},
            enum_fields={"transition": {"quick_cut", "fade"}},
        )

        with self.assertRaisesRegex(LLMResponseValidationError, "unsupported transition"):
            validator.validate('{"transition": "spin"}')


if __name__ == "__main__":
    unittest.main()
