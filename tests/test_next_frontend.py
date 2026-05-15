import unittest
from pathlib import Path


class NextFrontendTests(unittest.TestCase):
    def test_next_frontend_scaffold_exists_without_replacing_static_frontend(self):
        self.assertTrue(Path("frontend/app/index.html").exists())
        self.assertTrue(Path("frontend/web/package.json").exists())
        self.assertTrue(Path("frontend/web/app/page.tsx").exists())
        self.assertTrue(Path("frontend/web/app/layout.tsx").exists())
        self.assertTrue(Path("frontend/web/app/api/[...path]/route.ts").exists())
        self.assertTrue(Path("frontend/web/lib/api.ts").exists())
        self.assertTrue(Path("frontend/web/lib/types.ts").exists())

    def test_next_frontend_uses_required_components_and_api_base_url(self):
        component_names = [
            "ProjectForm",
            "ResultSummary",
            "SafetyReviewPanel",
            "SceneCard",
            "VisualSection",
            "SourcingSection",
            "EditingSection",
            "TimelinePanel",
            "AssetCandidateRegister",
            "JsonDownloadButton",
        ]
        for component_name in component_names:
            with self.subTest(component_name=component_name):
                self.assertTrue(Path(f"frontend/web/components/{component_name}.tsx").exists())

        api = Path("frontend/web/lib/api.ts").read_text(encoding="utf-8")
        proxy = Path("frontend/web/app/api/[...path]/route.ts").read_text(encoding="utf-8")
        package_json = Path("frontend/web/package.json").read_text(encoding="utf-8")

        self.assertIn("NEXT_PUBLIC_API_BASE_URL", api)
        self.assertIn('|| ""', api)
        self.assertNotIn('|| "http://127.0.0.1:8000"', api)
        self.assertIn("BACKEND_API_BASE_URL", proxy)
        self.assertIn("http://127.0.0.1:8000", proxy)
        self.assertIn('"expect"', proxy)
        self.assertIn('"connection"', proxy)
        self.assertIn("export async function POST", proxy)
        self.assertIn("export async function GET", proxy)
        self.assertIn("export async function PATCH", proxy)
        self.assertIn('"dev"', package_json)
        self.assertIn('"build"', package_json)
        self.assertIn('"lint"', package_json)

    def test_next_frontend_preserves_preview_features(self):
        page = Path("frontend/web/app/page.tsx").read_text(encoding="utf-8")
        scene_card = Path("frontend/web/components/SceneCard.tsx").read_text(encoding="utf-8")
        visual = Path("frontend/web/components/VisualSection.tsx").read_text(encoding="utf-8")
        sourcing = Path("frontend/web/components/SourcingSection.tsx").read_text(encoding="utf-8")
        safety = Path("frontend/web/components/SafetyReviewPanel.tsx").read_text(encoding="utf-8")
        timeline = Path("frontend/web/components/TimelinePanel.tsx").read_text(encoding="utf-8")
        asset_register = Path("frontend/web/components/AssetCandidateRegister.tsx").read_text(encoding="utf-8")
        download = Path("frontend/web/components/JsonDownloadButton.tsx").read_text(encoding="utf-8")
        types = Path("frontend/web/lib/types.ts").read_text(encoding="utf-8")

        self.assertIn("createProject", page)
        self.assertIn("generateShortsPlan", page)
        self.assertIn("대본", scene_card)
        self.assertIn("자막", scene_card)
        self.assertIn("generated_image_prompt", visual)
        self.assertIn("stock_search_keywords", visual)
        self.assertIn("asset_usage_note", sourcing)
        self.assertIn("required_human_review", safety)
        self.assertIn("recommended_revisions", safety)
        self.assertIn("result.timeline", timeline)
        self.assertIn("start_time", timeline)
        self.assertIn("end_time", timeline)
        self.assertIn("scene.beats", timeline)
        self.assertIn("beat.beat_type", timeline)
        self.assertIn("asset_review_checklist", timeline)
        self.assertIn("scene.beats ?? []", timeline)
        self.assertIn("scene.asset_review_checklist ?? []", timeline)
        self.assertIn("AssetCandidateRegister", timeline)
        self.assertIn("AssetSourceCandidate", types)
        self.assertIn("asset_candidate_id", types)
        self.assertIn('"community"', types)
        self.assertIn('"license_required"', types)
        self.assertIn("자료 후보 등록", asset_register)
        self.assertIn("onAddCandidate", asset_register)
        self.assertIn("onDeleteCandidate", asset_register)
        self.assertIn("approved_for_use", asset_register)
        self.assertIn("검토 필요", asset_register)
        self.assertIn("asset_source_candidates", download)
        self.assertIn("generation_result", download)
        self.assertIn("JSON.stringify(exportPayload, null, 2)", download)
        self.assertIn("issue-turi-plan-", download)

    def test_next_frontend_keeps_asset_candidates_frontend_only(self):
        page = Path("frontend/web/app/page.tsx").read_text(encoding="utf-8")
        api = Path("frontend/web/lib/api.ts").read_text(encoding="utf-8")
        asset_register = Path("frontend/web/components/AssetCandidateRegister.tsx").read_text(encoding="utf-8")

        self.assertIn("assetSourceCandidates", page)
        self.assertIn("setAssetSourceCandidates", page)
        self.assertIn("onAddAssetCandidate", page)
        self.assertIn("onUpdateAssetCandidate", page)
        self.assertIn("onDeleteAssetCandidate", page)
        self.assertNotIn("asset_source_candidates", api)
        self.assertNotIn("fetch(", asset_register)

    def test_next_frontend_uses_shortsflow_dark_studio_shell(self):
        layout = Path("frontend/web/app/layout.tsx").read_text(encoding="utf-8")
        page = Path("frontend/web/app/page.tsx").read_text(encoding="utf-8")
        form = Path("frontend/web/components/ProjectForm.tsx").read_text(encoding="utf-8")
        css = Path("frontend/web/app/globals.css").read_text(encoding="utf-8")

        self.assertIn("ShortsFlow", layout)
        self.assertIn("AI 쇼츠 기획 스튜디오", layout)
        self.assertIn("ShortsFlow", page)
        self.assertIn("더 잘 기획하고, 더 빠르게 만들고, 더 크게 성장하세요.", page)
        self.assertIn("홈", page)
        self.assertIn("프로젝트", page)
        self.assertIn("템플릿", page)
        self.assertIn("AI 아이디어", page)
        self.assertIn("대본 & 훅", page)
        self.assertIn("장면", page)
        self.assertIn("에셋", page)
        self.assertIn("분석", page)
        self.assertIn("설정", page)
        self.assertIn("준비 중", page)
        self.assertIn("프로젝트, 템플릿, 아이디어 검색", page)
        self.assertIn("새 프로젝트", page)
        self.assertIn("이슈털이 쇼츠 플래너", form)
        self.assertIn("AI 기획 생성", form)
        self.assertIn("color-scheme: dark", css)
        self.assertIn("--gradient-primary", css)
        self.assertIn("app-shell", css)
        self.assertIn("sidebar", css)
        self.assertIn("topbar", css)


if __name__ == "__main__":
    unittest.main()
