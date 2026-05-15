import unittest
from pathlib import Path


class StaticFrontendTests(unittest.TestCase):
    def test_static_frontend_is_deprecated_notice_page(self):
        html = Path("frontend/app/index.html").read_text(encoding="utf-8")

        self.assertIn("ShortsFlow Next.js frontend를 사용하세요", html)
        self.assertIn("Legacy / Deprecated", html)
        self.assertIn("http://127.0.0.1:8000", html)
        self.assertIn("http://localhost:3000", html)
        self.assertIn("uv run --project . python -m backend.src.presentation.http.server", html)
        self.assertIn("cd frontend/web &amp;&amp; npm run dev", html)
        self.assertIn("frontend/app", html)
        self.assertIn("frontend/web", html)

    def test_static_frontend_no_longer_mounts_legacy_mvp_app(self):
        html = Path("frontend/app/index.html").read_text(encoding="utf-8")

        self.assertNotIn('id="topic"', html)
        self.assertNotIn('id="project-form"', html)
        self.assertNotIn('id="scene-list"', html)
        self.assertNotIn('<script src="./app.js"></script>', html)

    def test_legacy_static_assets_are_still_kept(self):
        self.assertTrue(Path("frontend/app/app.js").exists())
        self.assertTrue(Path("frontend/app/styles.css").exists())


if __name__ == "__main__":
    unittest.main()
