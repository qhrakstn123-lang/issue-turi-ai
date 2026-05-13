import unittest
from unittest.mock import patch

from main import build_demo_payload, run_smoke_real


class MainDemoTests(unittest.TestCase):
    def test_build_demo_payload_returns_generated_shorts_plan(self):
        payload = build_demo_payload("지하철 안내문 때문에 반응이 갈린 사건")

        self.assertEqual(payload["project"]["output_format"], "youtube_shorts")
        self.assertEqual(payload["project"]["status"], "ready_for_review")
        self.assertEqual(len(payload["result"]["storyboard"]["scenes"]), 8)
        self.assertEqual(payload["result"]["storyboard"]["scenes"][0]["scene_purpose"], "hook")

    def test_smoke_real_rejects_fake_provider_without_calling_openai(self):
        with patch.dict("os.environ", {"ISSUE_TURI_LLM_PROVIDER": "fake"}, clear=True):
            status = run_smoke_real("topic")

        self.assertEqual(status["ok"], False)
        self.assertIn("requires ISSUE_TURI_LLM_PROVIDER=openai or real", status["error"])

    def test_smoke_real_reports_missing_api_key_without_printing_secret(self):
        with patch.dict("os.environ", {"ISSUE_TURI_LLM_PROVIDER": "openai"}, clear=True):
            status = run_smoke_real("topic")

        self.assertEqual(status["ok"], False)
        self.assertIn("OPENAI_API_KEY", status["error"])
        self.assertNotIn("topic", status["error"])


if __name__ == "__main__":
    unittest.main()
