import os

import pytest


@pytest.fixture(autouse=True)
def isolate_llm_provider_env():
    original_values = {
        key: os.environ.get(key)
        for key in ("ISSUE_TURI_LLM_PROVIDER", "OPENAI_API_KEY", "OPENAI_MODEL")
    }
    for key in original_values:
        os.environ.pop(key, None)

    yield

    for key, value in original_values.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
