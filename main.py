import json
import sys
from typing import Any

from backend.src.infrastructure.llm.settings import LLMProviderSettings
from backend.src.presentation.composition import create_api
from backend.src.presentation.http.server import create_server


def build_demo_payload(topic: str) -> dict[str, Any]:
    api = create_api()
    _, create_payload = api.handle(
        "POST",
        "/api/projects",
        {
            "topic": topic,
            "target_audience": "이슈 쇼츠 시청자",
            "tone": "빠르고 친근한 썰체",
            "style_template_id": "issue_turi_basic",
            "video_length_seconds": 50,
            "output_format": "youtube_shorts",
        },
    )
    project_id = create_payload["project"]["project_id"]
    _, result_payload = api.handle("POST", "/api/generate/shorts-plan", {"project_id": project_id})
    _, project_payload = api.handle("GET", f"/api/projects/{project_id}", None)
    return {"project": project_payload["project"], "result": result_payload["result"]}


def run_smoke_real(topic: str) -> dict[str, Any]:
    settings = LLMProviderSettings.from_env()
    provider = settings.provider.lower()
    if provider not in {"openai", "real"}:
        return {
            "ok": False,
            "error": "smoke-real requires ISSUE_TURI_LLM_PROVIDER=openai or real",
        }
    if not settings.openai_api_key:
        return {"ok": False, "error": "OPENAI_API_KEY is required for smoke-real"}

    try:
        return {"ok": True, **build_demo_payload(topic)}
    except Exception as exc:
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "hint": (
                "Check the failing real agent JSON contract: invalid JSON, missing field, "
                "unsupported enum value, or unknown scene_id."
            ),
        }


def _topic_from_args(args: list[str]) -> str:
    if "--topic" in args:
        index = args.index("--topic")
        if index + 1 >= len(args):
            raise ValueError("--topic requires a value")
        return args[index + 1]
    return "요즘 사람들이 AI 쇼츠 자동화에 관심 가지는 이유"


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "smoke-real":
        payload = run_smoke_real(_topic_from_args(sys.argv[2:]))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        raise SystemExit(0 if payload["ok"] else 1)

    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        server = create_server("127.0.0.1", port)
        print(f"Serving 이슈털이 쇼츠 플래너 at http://127.0.0.1:{port}")
        server.serve_forever()
        return

    payload = build_demo_payload("커뮤니티에서 반응이 갈린 카페 주문 사건")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
