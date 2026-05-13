from __future__ import annotations

from typing import Protocol


class PromptLoader(Protocol):
    def load(self, name: str) -> str:
        ...
