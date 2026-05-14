import json
import sys
from typing import Any

from backend.src.infrastructure.llm.settings import LLMProviderSettings
from backend.src.presentation.composition import create_api
from backend.src.presentation.http.server import create_server


SMOKE_REAL_HINT = (
    "Check the failing real agent JSON contract: invalid JSON, missing field, "
    "unsupported enum value, unknown scene_id, or missing visual sourcing fields "
    "(visual_source_strategy, capture_source_type, capture_usage_mode, asset_usage_note)."
)


def build_demo_payload(topic: str) -> dict[str, Any]:
    payload, error = _build_demo_payload_with_diagnostics(topic)
    if error is not None:
        raise RuntimeError(error["error"])
    return payload


def _build_demo_payload_with_diagnostics(topic: str) -> tuple[dict[str, Any], None] | tuple[None, dict[str, Any]]:
    api = create_api()
    create_status, create_payload = api.handle(
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
    if create_status != 201:
        return None, _smoke_real_error("create", create_status, create_payload)

    project = create_payload.get("project")
    project_id = project.get("project_id") if isinstance(project, dict) else None
    if not project_id:
        return None, _smoke_real_error(
            "create",
            create_status,
            create_payload,
            error="missing project_id in create response",
        )
    generate_status, result_payload = api.handle("POST", "/api/generate/shorts-plan", {"project_id": project_id})
    if generate_status != 200:
        return None, _smoke_real_error("generate", generate_status, result_payload)
    if "result" not in result_payload:
        return None, _smoke_real_error(
            "generate",
            generate_status,
            result_payload,
            error="missing result in generate response",
        )

    get_status, project_payload = api.handle("GET", f"/api/projects/{project_id}", None)
    if get_status != 200:
        return None, _smoke_real_error("get", get_status, project_payload)
    if "project" not in project_payload:
        return None, _smoke_real_error(
            "get",
            get_status,
            project_payload,
            error="missing project in get response",
        )

    return {"project": project_payload["project"], "result": result_payload["result"]}, None


def _smoke_real_error(
    stage: str,
    status: int,
    payload: dict[str, Any],
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "stage": stage,
        "status": status,
        "error": error or str(payload.get("error", f"{stage} stage failed")),
        "detail": payload,
        "hint": SMOKE_REAL_HINT,
    }


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
        payload, error = _build_demo_payload_with_diagnostics(topic)
        if error is not None:
            return error
        return {"ok": True, **payload}
    except Exception as exc:
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "hint": SMOKE_REAL_HINT,
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
