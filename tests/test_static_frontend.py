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

    def test_static_frontend_displays_visual_sourcing_and_safety_review_fields(self):
        html = Path("frontend/app/index.html").read_text(encoding="utf-8")
        script = Path("frontend/app/app.js").read_text(encoding="utf-8")

        self.assertIn('id="result-summary"', html)
        self.assertIn('id="safety-review"', html)
        self.assertIn('class="scene-section scene-visual"', html)
        self.assertIn('class="scene-section scene-sourcing"', html)
        self.assertIn("required_human_review", script)
        self.assertIn("copyright_risks", script)
        self.assertIn("rumor_or_defamation_risks", script)
        self.assertIn("privacy_or_portrait_risks", script)
        self.assertIn("source_usage_risks", script)
        self.assertIn("recommended_revisions", script)
        self.assertIn("visual_source_strategy", script)
        self.assertIn("asset_usage_note", script)
        self.assertIn("stock_search_keywords", script)


if __name__ == "__main__":
    unittest.main()
