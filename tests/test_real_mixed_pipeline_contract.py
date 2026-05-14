import json
import tempfile
import unittest
from pathlib import Path

from backend.src.application.agents.interfaces import ShortsAgentBundle
from backend.src.application.agents.real.editing_direction import RealEditingDirectionAgent
from backend.src.application.agents.real.script_writer import RealScriptWriterAgent
from backend.src.application.agents.real.safety_review import RealSafetyReviewAgent
from backend.src.application.agents.real.storyboard import RealStoryboardAgent
from backend.src.application.agents.real.subtitle import RealSubtitleAgent
from backend.src.application.agents.real.visual_asset import RealVisualAssetSuggestionAgent
from backend.src.application.agents.validation import JsonResponseValidator
from backend.src.application.pipelines.shorts_generation import ShortsGenerationPipeline
from backend.src.domain.models import ContentProject, OutputFormat, SafetyStatus
from backend.src.infrastructure.llm.fake_client import FakeLLMClient
from backend.src.infrastructure.prompts.file_prompt_loader import FilePromptLoader


def project():
    return ContentProject.create(
        topic="AI shorts automation",
        target_audience="creators",
        tone="fast and clear",
        style_template_id="issue_turi_basic",
        video_length_seconds=50,
        output_format=OutputFormat.YOUTUBE_SHORTS,
    )


def scene_payload(index: int):
    return {
        "scene_id": f"scene_{index:03d}",
        "scene_purpose": "hook" if index == 1 else "context",
        "narration": f"narration {index}",
        "tts_text": f"narration {index}",
        "subtitle": "",
        "emphasis_caption": "",
        "visual_asset_type": "image",
        "visual_description": f"base visual {index}",
        "generated_image_prompt": f"base prompt {index}",
        "gif_or_clip_suggestion": "none",
        "stock_search_keywords": [f"base keyword {index}"],
        "motion_direction": "zoom_in",
        "transition": "quick_cut",
        "sound_effect_hint": "pop",
        "estimated_duration": "3.0" if index == 1 else 3.0,
        "editing_notes": f"base editing {index}",
        "copyright_safety_note": "use safe assets",
    }


class RealMixedPipelineContractTests(unittest.TestCase):
    def test_real_mixed_chain_preserves_fields_and_updates_by_scene_id(self):
        scenes = [scene_payload(index) for index in range(1, 11)]
        subtitles = [
            {
                "scene_id": scene["scene_id"],
                "subtitle": f"subtitle {index}",
                "emphasis_caption": f"emphasis {index}",
            }
            for index, scene in enumerate(scenes, start=1)
        ]
        visuals = [
            {
                "scene_id": scene["scene_id"],
                "visual_asset_type": "text_only" if index == 2 else "image",
                "visual_description": f"real visual {index}",
                "generated_image_prompt": f"real image prompt {index}",
                "gif_or_clip_suggestion": f"clip suggestion {index}",
                "stock_search_keywords": [f"real keyword {index}", "shorts"],
                "visual_source_strategy": "text_card" if index == 2 else "mockup",
                "capture_source_type": "none" if index == 2 else "youtube",
                "capture_usage_mode": "mockup_recommended",
                "asset_usage_note": f"Use a safe mockup for scene {index}; do not copy real captions or thumbnails.",
            }
            for index, scene in enumerate(scenes, start=1)
        ]
        editing_directions = [
            {
                "scene_id": scene["scene_id"],
                "motion_direction": "pan_left" if index == 2 else "zoom_in",
                "transition": "fade" if index == 3 else "quick_cut",
                "sound_effect_hint": "whoosh" if index == 4 else "pop",
                "editing_notes": f"real editing {index}",
            }
            for index, scene in enumerate(scenes, start=1)
        ]
        safety_payload = {
            "safety_status": "needs_review",
            "safety_notes": ["Human review is needed for mockup sourcing before publishing."],
            "copyright_risks": ["Do not copy real thumbnails or captions."],
            "rumor_or_defamation_risks": [],
            "privacy_or_portrait_risks": ["Avoid real usernames and profile images."],
            "source_usage_risks": ["Use mockups instead of direct YouTube captures."],
            "required_human_review": True,
            "recommended_revisions": ["Replace all reference captures with self-made mockups."],
        }

        with tempfile.TemporaryDirectory() as directory:
            bundle = self._bundle(
                Path(directory),
                script_payload={
                    "title": "AI shorts automation",
                    "narration": "Explain the whole flow.",
                    "target_duration_seconds": 50,
                    "style_notes": ["keep it fast"],
                },
                storyboard_payload={"scenes": scenes},
                subtitle_payload={"subtitles": subtitles},
                visual_payload={"visuals": visuals},
                editing_payload={"editing_directions": editing_directions},
                safety_payload=safety_payload,
            )

            result = ShortsGenerationPipeline(bundle).generate(project())

        self.assertEqual(result.safety_status, SafetyStatus.NEEDS_REVIEW)
        self.assertTrue(result.required_human_review)
        self.assertEqual(result.copyright_risks, ["Do not copy real thumbnails or captions."])
        self.assertEqual(result.privacy_or_portrait_risks, ["Avoid real usernames and profile images."])
        self.assertEqual(result.source_usage_risks, ["Use mockups instead of direct YouTube captures."])
        self.assertEqual(result.recommended_revisions, ["Replace all reference captures with self-made mockups."])
        self.assertEqual(result.video_script.title, "AI shorts automation")
        self.assertEqual(len(result.storyboard.scenes), 10)

        first = result.storyboard.scenes[0]
        self.assertEqual(first.scene_id, "scene_001")
        self.assertEqual(first.scene_purpose, "hook")
        self.assertEqual(first.narration, "narration 1")
        self.assertEqual(first.estimated_duration, 3.0)
        self.assertEqual(first.subtitle, "subtitle 1")
        self.assertEqual(first.emphasis_caption, "emphasis 1")
        self.assertEqual(first.visual_asset_type, "image")
        self.assertEqual(first.visual_description, "real visual 1")
        self.assertEqual(first.generated_image_prompt, "real image prompt 1")
        self.assertEqual(first.gif_or_clip_suggestion, "clip suggestion 1")
        self.assertEqual(first.stock_search_keywords, ["real keyword 1", "shorts"])
        self.assertEqual(first.visual_source_strategy, "mockup")
        self.assertEqual(first.capture_source_type, "youtube")
        self.assertEqual(first.capture_usage_mode, "mockup_recommended")
        self.assertEqual(first.asset_usage_note, "Use a safe mockup for scene 1; do not copy real captions or thumbnails.")
        self.assertEqual(first.motion_direction, "zoom_in")
        self.assertEqual(first.transition, "quick_cut")
        self.assertEqual(first.sound_effect_hint, "pop")
        self.assertEqual(first.editing_notes, "real editing 1")
        self.assertEqual(first.copyright_safety_note, "use safe assets")

        second = result.storyboard.scenes[1]
        self.assertEqual(second.scene_id, "scene_002")
        self.assertEqual(second.scene_purpose, "context")
        self.assertEqual(second.narration, "narration 2")
        self.assertEqual(second.estimated_duration, 3.0)
        self.assertEqual(second.subtitle, "subtitle 2")
        self.assertEqual(second.emphasis_caption, "emphasis 2")
        self.assertEqual(second.visual_asset_type, "text_only")
        self.assertEqual(second.visual_description, "real visual 2")
        self.assertEqual(second.visual_source_strategy, "text_card")
        self.assertEqual(second.capture_source_type, "none")
        self.assertEqual(second.motion_direction, "pan_left")
        self.assertEqual(second.transition, "quick_cut")
        self.assertEqual(second.sound_effect_hint, "pop")

        third = result.storyboard.scenes[2]
        self.assertEqual(third.transition, "fade")
        self.assertEqual(third.visual_description, "real visual 3")
        self.assertEqual(third.subtitle, "subtitle 3")

        fourth = result.storyboard.scenes[3]
        self.assertEqual(fourth.sound_effect_hint, "whoosh")
        self.assertEqual(fourth.estimated_duration, 3.0)

        scene_ids = [scene.scene_id for scene in result.storyboard.scenes]
        self.assertEqual(scene_ids, [f"scene_{index:03d}" for index in range(1, 11)])

    def _bundle(
        self,
        prompt_root: Path,
        script_payload: dict,
        storyboard_payload: dict,
        subtitle_payload: dict,
        visual_payload: dict,
        editing_payload: dict,
        safety_payload: dict,
    ) -> ShortsAgentBundle:
        shorts = prompt_root / "shorts"
        shorts.mkdir()
        safety = prompt_root / "safety"
        safety.mkdir()
        for prompt_name in [
            "script_writer",
            "storyboard",
            "subtitle",
            "visual_prompt",
            "editing_direction",
        ]:
            (shorts / f"{prompt_name}.md").write_text(f"# {prompt_name}\nJSON only.", encoding="utf-8")
        (safety / "review.md").write_text("# safety review\nJSON only.", encoding="utf-8")

        prompt_loader = FilePromptLoader(prompt_root)
        return ShortsAgentBundle(
            script_writer=RealScriptWriterAgent(
                llm_client=FakeLLMClient([json.dumps(script_payload, ensure_ascii=False)]),
                prompt_loader=prompt_loader,
                response_validator=JsonResponseValidator(
                    required_fields={"title", "narration", "target_duration_seconds", "style_notes"}
                ),
            ),
            storyboard=RealStoryboardAgent(
                llm_client=FakeLLMClient([json.dumps(storyboard_payload, ensure_ascii=False)]),
                prompt_loader=prompt_loader,
                response_validator=JsonResponseValidator(required_fields={"scenes"}),
            ),
            subtitle=RealSubtitleAgent(
                llm_client=FakeLLMClient([json.dumps(subtitle_payload, ensure_ascii=False)]),
                prompt_loader=prompt_loader,
                response_validator=JsonResponseValidator(required_fields={"subtitles"}),
            ),
            visual_asset=RealVisualAssetSuggestionAgent(
                llm_client=FakeLLMClient([json.dumps(visual_payload, ensure_ascii=False)]),
                prompt_loader=prompt_loader,
                response_validator=JsonResponseValidator(required_fields={"visuals"}),
            ),
            editing_direction=RealEditingDirectionAgent(
                llm_client=FakeLLMClient([json.dumps(editing_payload, ensure_ascii=False)]),
                prompt_loader=prompt_loader,
                response_validator=JsonResponseValidator(required_fields={"editing_directions"}),
            ),
            safety_review=RealSafetyReviewAgent(
                llm_client=FakeLLMClient([json.dumps(safety_payload, ensure_ascii=False)]),
                prompt_loader=prompt_loader,
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
            ),
        )


if __name__ == "__main__":
    unittest.main()
