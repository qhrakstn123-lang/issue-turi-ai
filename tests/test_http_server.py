import http.client
import json
import threading
import unittest

from backend.src.presentation.http.server import create_server


class HttpServerTests(unittest.TestCase):
    def test_server_serves_frontend_and_api(self):
        server = create_server("127.0.0.1", 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        port = server.server_address[1]

        try:
            connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
            connection.request("GET", "/")
            html_response = connection.getresponse()
            html = html_response.read().decode("utf-8")

            payload = json.dumps(
                {
                    "topic": "문구 하나 때문에 댓글이 갈린 사건",
                    "target_audience": "이슈 쇼츠 시청자",
                    "tone": "빠른 썰체",
                    "style_template_id": "issue_turi_basic",
                    "video_length_seconds": 50,
                    "output_format": "youtube_shorts",
                },
                ensure_ascii=False,
            ).encode("utf-8")
            connection.request("POST", "/api/projects", body=payload, headers={"Content-Type": "application/json"})
            api_response = connection.getresponse()
            api_payload = json.loads(api_response.read().decode("utf-8"))
        finally:
            server.shutdown()
            server.server_close()

        self.assertEqual(html_response.status, 200)
        self.assertIn("ShortsFlow Next.js frontend를 사용하세요", html)
        self.assertEqual(api_response.status, 201)
        self.assertEqual(api_payload["project"]["output_format"], "youtube_shorts")

    def test_server_allows_next_frontend_cors_preflight(self):
        server = create_server("127.0.0.1", 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        port = server.server_address[1]

        try:
            connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
            connection.request(
                "OPTIONS",
                "/api/projects",
                headers={
                    "Origin": "http://127.0.0.1:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type",
                },
            )
            response = connection.getresponse()
            response.read()
        finally:
            server.shutdown()
            server.server_close()

        self.assertEqual(response.status, 204)
        self.assertEqual(response.getheader("Access-Control-Allow-Origin"), "*")
        self.assertIn("POST", response.getheader("Access-Control-Allow-Methods"))
        self.assertIn("Content-Type", response.getheader("Access-Control-Allow-Headers"))


if __name__ == "__main__":
    unittest.main()
