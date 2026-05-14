import json
import tempfile
import unittest
from pathlib import Path

from backend.src.application.agents.real.safety_review import RealSafetyReviewAgent
from backend.src.application.agents.validation import (
    JsonResponseValidator,
    LLMResponseValidationError,
)
from backend.src.domain.models import ContentProject, OutputFormat, SafetyStatus, Scene, Storyboard, VideoScript
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
        narration="Explain why automation matters without presenting rumors as facts.",
        target_duration_seconds=45,
        style_notes=["short captions"],
    )


def storyboard():
    return Storyboard(
        [
            Scene.minimal("scene_001", 3.0).update(
                subtitle="AI automation is spreading",
                emphasis_caption="automation wave",
                visual_source_strategy="reference_capture",
                capture_source_type="community",
                capture_usage_mode="mockup_recommended",
                asset_usage_note="Use a self-made community mockup; avoid real usernames and profile images.",
                visual_description="community comment style mockup",
                generated_image_prompt="vertical community comment mockup, no real names",
                editing_notes="show comments quickly",
                copyright_safety_note="avoid direct screenshots",
            )
        ]
    )


def safety_payload(**overrides):
    payload = {
        "safety_status": "needs_review",
        "safety_notes": ["Community-style visuals need human review before publishing."],
        "copyright_risks": ["Avoid copying exact community screenshots."],
        "rumor_or_defamation_risks": [],
        "privacy_or_portrait_risks": ["Do not expose usernames or profile images."],
        "source_usage_risks": ["Mock up the comments instead of using direct capture."],
        "required_human_review": True,
        "recommended_revisions": ["Use fictional comments and anonymized UI."],
    }
    payload.update(overrides)
    return payload


def safety_agent_for(payload):
    return RealSafetyReviewAgent(
        llm_client=FakeLLMClient([json.dumps(payload, ensure_ascii=False)]),
        prompt_loader=FilePromptLoader(Path("prompts")),
        response_validator=JsonResponseValidator(
            required_fields={
                "safety_status",
                "safety_notes",
                "copyright_risks",
                "rumor_or_defamation_risks",
                "privacy_or_portrait_risks",
                "source_usage_risks",
                "required_human_review",
                "recommended_revisions",
            },
            enum_fields={"safety_status": {"approved", "needs_review", "rejected"}},
        ),
    )


class RealSafetyReviewAgentTests(unittest.TestCase):
    def test_valid_json_becomes_safety_review(self):
        agent = safety_agent_for(safety_payload())

        review = agent.review(project(), script(), storyboard())

        self.assertEqual(review.status, SafetyStatus.NEEDS_REVIEW)
        self.assertEqual(review.notes, ["Community-style visuals need human review before publishing."])
        self.assertEqual(review.copyright_risks, ["Avoid copying exact community screenshots."])
        self.assertEqual(review.rumor_or_defamation_risks, [])
        self.assertEqual(review.privacy_or_portrait_risks, ["Do not expose usernames or profile images."])
        self.assertEqual(review.source_usage_risks, ["Mock up the comments instead of using direct capture."])
        self.assertTrue(review.required_human_review)
        self.assertEqual(review.recommended_revisions, ["Use fictional comments and anonymized UI."])

    def test_agent_does_not_modify_scenes(self):
        original = storyboard()
        agent = safety_agent_for(safety_payload())

        agent.review(project(), script(), original)

        self.assertEqual(original, storyboard())

    def test_prompt_includes_safety_contract_and_visual_context(self):
        client = FakeLLMClient([json.dumps(safety_payload(), ensure_ascii=False)])
        with tempfile.TemporaryDirectory() as directory:
            prompt_file = Path(directory) / "safety" / "review.md"
            prompt_file.parent.mkdir()
            prompt_file.write_text("# SafetyReviewAgent\nJSON only.", encoding="utf-8")
            agent = RealSafetyReviewAgent(
                llm_client=client,
                prompt_loader=FilePromptLoader(Path(directory)),
                response_validator=JsonResponseValidator(
                    required_fields={
                        "safety_status",
                        "safety_notes",
                        "copyright_risks",
                        "rumor_or_defamation_risks",
                        "privacy_or_portrait_risks",
                        "source_usage_risks",
                        "required_human_review",
                        "recommended_revisions",
                    },
                    enum_fields={"safety_status": {"approved", "needs_review", "rejected"}},
                ),
            )

            agent.review(project(), script(), storyboard())

        prompt = client.prompts[0]
        self.assertIn("AI shorts automation", prompt)
        self.assertIn("scene_001", prompt)
        self.assertIn("asset_usage_note", prompt)
        self.assertIn("copyright_safety_note", prompt)
        self.assertIn("legal judge", prompt)

    def test_rejects_missing_safety_status(self):
        payload = safety_payload()
        del payload["safety_status"]
        agent = safety_agent_for(payload)

        with self.assertRaisesRegex(LLMResponseValidationError, "safety_status"):
            agent.review(project(), script(), storyboard())

    def test_rejects_invalid_safety_status(self):
        agent = safety_agent_for(safety_payload(safety_status="unclear"))

        with self.assertRaisesRegex(LLMResponseValidationError, "safety_status"):
            agent.review(project(), script(), storyboard())

    def test_rejects_non_boolean_required_human_review(self):
        agent = safety_agent_for(safety_payload(required_human_review="true"))

        with self.assertRaisesRegex(LLMResponseValidationError, "required_human_review"):
            agent.review(project(), script(), storyboard())

    def test_rejects_non_list_safety_fields(self):
        for field_name in [
            "safety_notes",
            "copyright_risks",
            "rumor_or_defamation_risks",
            "privacy_or_portrait_risks",
            "source_usage_risks",
            "recommended_revisions",
        ]:
            with self.subTest(field_name=field_name):
                agent = safety_agent_for(safety_payload(**{field_name: "not a list"}))

                with self.assertRaisesRegex(LLMResponseValidationError, field_name):
                    agent.review(project(), script(), storyboard())

    def test_rejects_non_string_list_items(self):
        agent = safety_agent_for(safety_payload(copyright_risks=["ok", 123]))

        with self.assertRaisesRegex(LLMResponseValidationError, "copyright_risks"):
            agent.review(project(), script(), storyboard())

    def test_rejects_extra_keys(self):
        agent = safety_agent_for(safety_payload(legal_verdict="safe"))

        with self.assertRaisesRegex(LLMResponseValidationError, "unexpected field"):
            agent.review(project(), script(), storyboard())


if __name__ == "__main__":
    unittest.main()
