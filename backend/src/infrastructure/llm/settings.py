from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMProviderSettings:
    provider: str = "fake"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5"

    @classmethod
    def from_env(cls) -> LLMProviderSettings:
        return cls(
            provider=os.environ.get("ISSUE_TURI_LLM_PROVIDER", "fake"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            openai_model=os.environ.get("OPENAI_MODEL", "gpt-5"),
        )
