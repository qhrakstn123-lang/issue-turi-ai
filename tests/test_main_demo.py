import unittest

from main import build_demo_payload


class MainDemoTests(unittest.TestCase):
    def test_build_demo_payload_returns_generated_shorts_plan(self):
        payload = build_demo_payload("지하철 안내문 때문에 반응이 갈린 사건")

        self.assertEqual(payload["project"]["output_format"], "youtube_shorts")
        self.assertEqual(payload["project"]["status"], "ready_for_review")
        self.assertEqual(len(payload["result"]["storyboard"]["scenes"]), 8)
        self.assertEqual(payload["result"]["storyboard"]["scenes"][0]["scene_purpose"], "hook")


if __name__ == "__main__":
    unittest.main()
