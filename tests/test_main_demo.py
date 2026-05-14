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
        self.assertIn("visual_source_strategy", payload["result"]["storyboard"]["scenes"][0])
        self.assertIn("capture_source_type", payload["result"]["storyboard"]["scenes"][0])
        self.assertIn("capture_usage_mode", payload["result"]["storyboard"]["scenes"][0])
        self.assertIn("asset_usage_note", payload["result"]["storyboard"]["scenes"][0])

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

    def test_smoke_real_returns_generate_error_payload_without_keyerror(self):
        class ApiWithGenerateError:
            def handle(self, method, path, body):
                if method == "POST" and path == "/api/projects":
                    return 201, {"project": {"project_id": "project_001"}}
                if method == "POST" and path == "/api/generate/shorts-plan":
                    return 400, {"error": "missing visual field: visual_source_strategy"}
                raise AssertionError(f"unexpected API call: {method} {path}")

        with patch.dict(
            "os.environ",
            {
                "ISSUE_TURI_LLM_PROVIDER": "openai",
                "OPENAI_API_KEY": "test-key-that-must-not-leak",
            },
            clear=True,
        ), patch("main.create_api", return_value=ApiWithGenerateError()):
            status = run_smoke_real("topic")

        self.assertEqual(status["ok"], False)
        self.assertEqual(status["stage"], "generate")
        self.assertEqual(status["status"], 400)
        self.assertEqual(status["error"], "missing visual field: visual_source_strategy")
        self.assertEqual(status["detail"], {"error": "missing visual field: visual_source_strategy"})
        self.assertIn("visual_source_strategy", status["hint"])
        self.assertNotIn("test-key-that-must-not-leak", str(status))

    def test_smoke_real_returns_create_payload_error_without_keyerror(self):
        class ApiWithMalformedCreate:
            def handle(self, method, path, body):
                if method == "POST" and path == "/api/projects":
                    return 201, {"project": {}}
                raise AssertionError(f"unexpected API call: {method} {path}")

        with patch.dict(
            "os.environ",
            {
                "ISSUE_TURI_LLM_PROVIDER": "openai",
                "OPENAI_API_KEY": "test-key-that-must-not-leak",
            },
            clear=True,
        ), patch("main.create_api", return_value=ApiWithMalformedCreate()):
            status = run_smoke_real("topic")

        self.assertEqual(status["ok"], False)
        self.assertEqual(status["stage"], "create")
        self.assertEqual(status["status"], 201)
        self.assertEqual(status["error"], "missing project_id in create response")
        self.assertEqual(status["detail"], {"project": {}})
        self.assertNotIn("test-key-that-must-not-leak", str(status))


if __name__ == "__main__":
    unittest.main()
