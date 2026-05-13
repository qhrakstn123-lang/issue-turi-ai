from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from backend.src.presentation.http.api import IssueTuriApi, create_api


FRONTEND_ROOT = Path(__file__).resolve().parents[4] / "frontend" / "app"


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    api = create_api()

    class RequestHandler(IssueTuriRequestHandler):
        shared_api = api

    return ThreadingHTTPServer((host, port), RequestHandler)


class IssueTuriRequestHandler(BaseHTTPRequestHandler):
    shared_api: IssueTuriApi

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            self._write_api_response(*self.shared_api.handle("GET", path, None))
            return
        self._serve_static(path)

    def do_POST(self) -> None:
        self._handle_json_request("POST")

    def do_PATCH(self) -> None:
        self._handle_json_request("PATCH")

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _handle_json_request(self, method: str) -> None:
        path = urlparse(self.path).path
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
            payload = json.loads(body)
        except json.JSONDecodeError:
            self._write_api_response(400, {"error": "invalid JSON body"})
            return

        self._write_api_response(*self.shared_api.handle(method, path, payload))

    def _write_api_response(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, path: str) -> None:
        relative = "index.html" if path in {"/", ""} else path.lstrip("/")
        target = (FRONTEND_ROOT / relative).resolve()
        if not str(target).startswith(str(FRONTEND_ROOT.resolve())) or not target.exists():
            self._write_static_response(404, b"Not found", "text/plain; charset=utf-8")
            return

        content_type = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "text/javascript; charset=utf-8",
        }.get(target.suffix, "application/octet-stream")
        self._write_static_response(200, target.read_bytes(), content_type)

    def _write_static_response(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = create_server()
    host, port = server.server_address

    print(f"IssueTuri server running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()