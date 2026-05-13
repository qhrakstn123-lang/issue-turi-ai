import unittest

from backend.src.application.agents.fake_agents import (
    FakeEditingDirectionAgent,
    FakeScriptWriterAgent,
    FakeStoryboardAgent,
    FakeSubtitleAgent,
    FakeVisualAssetSuggestionAgent,
)
from backend.src.application.agents.real.script_writer import RealScriptWriterAgent
from backend.src.application.agents.real.editing_direction import RealEditingDirectionAgent
from backend.src.application.agents.real.storyboard import RealStoryboardAgent
from backend.src.application.agents.real.subtitle import RealSubtitleAgent
from backend.src.application.agents.real.visual_asset import RealVisualAssetSuggestionAgent
from backend.src.infrastructure.llm.openai_client import MissingOpenAIAPIKeyError
from backend.src.infrastructure.llm.settings import LLMProviderSettings
from backend.src.presentation.composition import create_agent_bundle


class LLMCompositionTests(unittest.TestCase):
    def test_fake_provider_keeps_existing_fake_bundle(self):
        bundle = create_agent_bundle(LLMProviderSettings(provider="fake"))

        self.assertIsInstance(bundle.script_writer, FakeScriptWriterAgent)
        self.assertIsInstance(bundle.storyboard, FakeStoryboardAgent)
        self.assertIsInstance(bundle.visual_asset, FakeVisualAssetSuggestionAgent)
        self.assertIsInstance(bundle.subtitle, FakeSubtitleAgent)
        self.assertIsInstance(bundle.editing_direction, FakeEditingDirectionAgent)

    def test_openai_provider_uses_real_content_agents_but_fake_safety(self):
        bundle = create_agent_bundle(
            LLMProviderSettings(provider="openai", openai_api_key="test-key")
        )

        self.assertIsInstance(bundle.script_writer, RealScriptWriterAgent)
        self.assertIsInstance(bundle.storyboard, RealStoryboardAgent)
        self.assertIsInstance(bundle.subtitle, RealSubtitleAgent)
        self.assertIsInstance(bundle.visual_asset, RealVisualAssetSuggestionAgent)
        self.assertIsInstance(bundle.editing_direction, RealEditingDirectionAgent)

    def test_real_provider_without_api_key_fails_clearly(self):
        with self.assertRaisesRegex(MissingOpenAIAPIKeyError, "OPENAI_API_KEY"):
            create_agent_bundle(LLMProviderSettings(provider="real"))


if __name__ == "__main__":
    unittest.main()
