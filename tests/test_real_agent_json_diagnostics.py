import unittest
from pathlib import Path
from unittest.mock import patch

from main import run_smoke_real
from backend.src.application.agents.real.editing_direction import RealEditingDirectionAgent
from backend.src.application.agents.real.script_writer import RealScriptWriterAgent
from backend.src.application.agents.real.storyboard import RealStoryboardAgent
from backend.src.application.agents.real.subtitle import RealSubtitleAgent
from backend.src.application.agents.real.visual_asset import RealVisualAssetSuggestionAgent
from backend.src.application.agents.validation import JsonResponseValidator, LLMResponseValidationError
from backend.src.domain.models import ContentProject, OutputFormat, Scene, Storyboard, VideoScript
from backend.src.infrastructure.llm.fake_client import FakeLLMClient
from backend.src.infrastructure.prompts.file_prompt_loader import FilePromptLoader


def project():
    return ContentProject.create(
        topic="community cafe order issue",
        target_audience="shorts viewers",
        tone="fast",
        style_template_id="issue_turi_basic",
        video_length_seconds=45,
        output_format=OutputFormat.YOUTUBE_SHORTS,
    )


def script():
    return VideoScript(
        title="Cafe order issue",
        narration="Explain the context quickly.",
        target_duration_seconds=45,
        style_notes=["keep it clear"],
    )


def storyboard():
    return Storyboard([Scene.minimal("scene_001", 3.0), Scene.minimal("scene_002", 3.0)])


class RealAgentJsonDiagnosticsTests(unittest.TestCase):
    def test_invalid_json_errors_include_real_agent_name_and_short_preview(self):
        cases = [
            (
                "RealScriptWriterAgent",
                lambda response: RealScriptWriterAgent(
                    llm_client=FakeLLMClient([response]),
                    prompt_loader=FilePromptLoader(Path("prompts")),
                    response_validator=JsonResponseValidator(
                        required_fields={"title", "narration", "target_duration_seconds", "style_notes"}
                    ),
                ).generate(project()),
            ),
            (
                "RealStoryboardAgent",
                lambda response: RealStoryboardAgent(
                    llm_client=FakeLLMClient([response]),
                    prompt_loader=FilePromptLoader(Path("prompts")),
                    response_validator=JsonResponseValidator(required_fields={"scenes"}),
                ).generate(project(), script()),
            ),
            (
                "RealSubtitleAgent",
                lambda response: RealSubtitleAgent(
                    llm_client=FakeLLMClient([response]),
                    prompt_loader=FilePromptLoader(Path("prompts")),
                    response_validator=JsonResponseValidator(required_fields={"subtitles"}),
                ).apply(project(), script(), storyboard()),
            ),
            (
                "RealVisualAssetSuggestionAgent",
                lambda response: RealVisualAssetSuggestionAgent(
                    llm_client=FakeLLMClient([response]),
                    prompt_loader=FilePromptLoader(Path("prompts")),
                    response_validator=JsonResponseValidator(required_fields={"visuals"}),
                ).apply(project(), script(), storyboard()),
            ),
            (
                "RealEditingDirectionAgent",
                lambda response: RealEditingDirectionAgent(
                    llm_client=FakeLLMClient([response]),
                    prompt_loader=FilePromptLoader(Path("prompts")),
                    response_validator=JsonResponseValidator(required_fields={"editing_directions"}),
                ).apply(project(), script(), storyboard()),
            ),
        ]

        for agent_name, call_agent in cases:
            with self.subTest(agent_name=agent_name):
                raw_response = f"{agent_name} returned markdown, not JSON\n```json"

                with self.assertRaises(LLMResponseValidationError) as context:
                    call_agent(raw_response)

                message = str(context.exception)
                self.assertIn(agent_name, message)
                self.assertIn("invalid JSON response", message)
                self.assertIn("raw_response_preview=", message)
                self.assertIn("returned markdown", message)
                self.assertLessEqual(len(message), 650)

    def test_smoke_real_generate_error_can_surface_agent_name(self):
        class ApiWithAgentJsonError:
            def handle(self, method, path, body):
                if method == "POST" and path == "/api/projects":
                    return 201, {"project": {"project_id": "project_001"}}
                if method == "POST" and path == "/api/generate/shorts-plan":
                    return 400, {
                        "error": "RealVisualAssetSuggestionAgent: invalid JSON response; raw_response_preview=```json"
                    }
                raise AssertionError(f"unexpected API call: {method} {path}")

        with patch.dict(
            "os.environ",
            {
                "ISSUE_TURI_LLM_PROVIDER": "openai",
                "OPENAI_API_KEY": "test-key-that-must-not-leak",
            },
            clear=True,
        ), patch("main.create_api", return_value=ApiWithAgentJsonError()):
            status = run_smoke_real("topic")

        self.assertEqual(status["ok"], False)
        self.assertEqual(status["stage"], "generate")
        self.assertIn("RealVisualAssetSuggestionAgent", status["error"])
        self.assertIn("raw_response_preview=", status["error"])
        self.assertNotIn("test-key-that-must-not-leak", str(status))

    def test_real_agent_prompts_forbid_non_json_wrappers(self):
        required_lines = [
            "Return only a valid JSON object.",
            "Do not include markdown code fences.",
            "Do not include explanations before or after JSON.",
            "Do not include comments.",
            "Do not return a markdown list.",
        ]
        prompt_paths = [
            Path("prompts/shorts/script_writer.md"),
            Path("prompts/shorts/storyboard.md"),
            Path("prompts/shorts/subtitle.md"),
            Path("prompts/shorts/visual_prompt.md"),
            Path("prompts/shorts/editing_direction.md"),
        ]

        for prompt_path in prompt_paths:
            with self.subTest(prompt_path=str(prompt_path)):
                prompt = prompt_path.read_text(encoding="utf-8")
                for line in required_lines:
                    self.assertIn(line, prompt)


if __name__ == "__main__":
    unittest.main()
