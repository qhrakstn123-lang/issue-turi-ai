from __future__ import annotations

from collections import deque


class FakeLLMClient:
    def __init__(self, responses: list[str] | None = None) -> None:
        self._responses = deque(responses or [])
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if not self._responses:
            return ""
        return self._responses.popleft()
