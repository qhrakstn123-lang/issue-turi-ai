from __future__ import annotations


class MissingOpenAIAPIKeyError(ValueError):
    pass


class OpenAILLMClient:
    def __init__(self, api_key: str | None, model: str = "gpt-5") -> None:
        if not api_key:
            raise MissingOpenAIAPIKeyError("OPENAI_API_KEY is required for OpenAILLMClient")
        self._api_key = api_key
        self._model = model

    def complete(self, prompt: str) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package is not installed") from exc

        client = OpenAI(api_key=self._api_key)
        response = client.responses.create(model=self._model, input=prompt)
        return response.output_text
