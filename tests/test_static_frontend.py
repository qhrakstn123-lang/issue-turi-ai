import unittest
from pathlib import Path


class StaticFrontendTests(unittest.TestCase):
    def test_static_frontend_contains_mvp_controls(self):
        html = Path("frontend/app/index.html").read_text(encoding="utf-8")
        script = Path("frontend/app/app.js").read_text(encoding="utf-8")

        self.assertIn('id="topic"', html)
        self.assertIn('id="target_audience"', html)
        self.assertIn('id="scene-list"', html)
        self.assertIn("/api/projects", script)
        self.assertIn("/api/generate/shorts-plan", script)


if __name__ == "__main__":
    unittest.main()
