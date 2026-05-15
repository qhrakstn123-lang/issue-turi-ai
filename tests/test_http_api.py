import unittest

from backend.src.application.agents.validation import LLMResponseValidationError
from backend.src.presentation.composition import create_api
from backend.src.presentation.http.api import IssueTuriApi


class NullService:
    pass


class RuntimeErrorService:
    def create_project(self, **kwargs):
        raise RuntimeError("openai package is not installed")


class ValidationErrorService:
    def create_project(self, **kwargs):
        raise LLMResponseValidationError("estimated_duration must be numeric: abc")


class HttpApiTests(unittest.TestCase):
    def test_http_api_accepts_prebuilt_service(self):
        service = NullService()
        api = IssueTuriApi(service)

        self.assertIs(api._service, service)

    def test_runtime_errors_return_clear_json_error(self):
        api = IssueTuriApi(RuntimeErrorService())

        status, payload = api.handle(
            "POST",
            "/api/projects",
            {
                "topic": "topic",
                "target_audience": "audience",
                "tone": "tone",
                "style_template_id": "issue_turi_basic",
                "video_length_seconds": 50,
                "output_format": "youtube_shorts",
            },
        )

        self.assertEqual(status, 500)
        self.assertEqual(payload["error"], "openai package is not installed")

    def test_llm_validation_errors_return_clear_json_error(self):
        api = IssueTuriApi(ValidationErrorService())

        status, payload = api.handle(
            "POST",
            "/api/projects",
            {
                "topic": "topic",
                "target_audience": "audience",
                "tone": "tone",
                "style_template_id": "issue_turi_basic",
                "video_length_seconds": 50,
                "output_format": "youtube_shorts",
            },
        )

        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "estimated_duration must be numeric: abc")

    def test_create_generate_get_and_patch_project(self):
        api = create_api()

        create_status, create_payload = api.handle(
            "POST",
            "/api/projects",
            {
                "topic": "편의점 안내문 때문에 반응이 갈린 사건",
                "target_audience": "이슈 쇼츠 시청자",
                "tone": "빠른 썰체",
                "style_template_id": "issue_turi_basic",
                "video_length_seconds": 50,
                "output_format": "youtube_shorts",
            },
        )
        project_id = create_payload["project"]["project_id"]

        generate_status, generate_payload = api.handle(
            "POST",
            "/api/generate/shorts-plan",
            {"project_id": project_id},
        )
        patch_status, patch_payload = api.handle(
            "PATCH",
            f"/api/projects/{project_id}",
            {"scene_id": "scene_001", "subtitle": "반응 갈린 안내문"},
        )
        get_status, get_payload = api.handle("GET", f"/api/projects/{project_id}", None)

        self.assertEqual(create_status, 201)
        self.assertEqual(generate_status, 200)
        self.assertEqual(patch_status, 200)
        self.assertEqual(get_status, 200)
        self.assertEqual(len(generate_payload["result"]["storyboard"]["scenes"]), 8)
        self.assertEqual(generate_payload["result"]["timeline"]["aspect_ratio"], "9:16")
        self.assertEqual(generate_payload["result"]["timeline"]["scenes"][0]["start_time"], 0.0)
        self.assertEqual(
            patch_payload["project"]["generation_result"]["storyboard"]["scenes"][0]["subtitle"],
            "반응 갈린 안내문",
        )
        self.assertEqual(get_payload["project"]["project_id"], project_id)

    def test_invalid_output_format_returns_400(self):
        api = create_api()

        status, payload = api.handle(
            "POST",
            "/api/projects",
            {
                "topic": "테스트 주제",
                "target_audience": "시청자",
                "tone": "빠른 썰체",
                "style_template_id": "issue_turi_basic",
                "video_length_seconds": 50,
                "output_format": "longform_video",
            },
        )

        self.assertEqual(status, 400)
        self.assertIn("MVP only supports", payload["error"])


if __name__ == "__main__":
    unittest.main()
