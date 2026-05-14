from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


class LLMResponseValidationError(ValueError):
    pass


def response_preview(response: str, max_chars: int = 400) -> str:
    compact = " ".join(response.split())
    if len(compact) <= max_chars:
        return compact
    return f"{compact[:max_chars]}..."


def validate_agent_json_response(
    agent_name: str,
    response_validator: JsonResponseValidator,
    response: str,
) -> dict[str, Any]:
    try:
        return response_validator.validate(response)
    except LLMResponseValidationError as exc:
        preview = response_preview(response)
        raise LLMResponseValidationError(
            f"{agent_name}: {exc}; raw_response_preview={preview}"
        ) from exc


@dataclass(frozen=True)
class JsonResponseValidator:
    required_fields: set[str]
    enum_fields: dict[str, set[str]] = field(default_factory=dict)

    def validate(self, response: str) -> dict[str, Any]:
        if not response.strip():
            raise LLMResponseValidationError("empty LLM response")

        try:
            payload = json.loads(response)
        except json.JSONDecodeError as exc:
            raise LLMResponseValidationError("invalid JSON response") from exc

        if not isinstance(payload, dict):
            raise LLMResponseValidationError("JSON response must be an object")

        missing_fields = sorted(field for field in self.required_fields if field not in payload)
        if missing_fields:
            raise LLMResponseValidationError(f"missing required field: {missing_fields[0]}")

        for field_name, allowed_values in self.enum_fields.items():
            if field_name not in payload:
                continue
            if payload[field_name] not in allowed_values:
                raise LLMResponseValidationError(f"unsupported {field_name}: {payload[field_name]}")

        return payload
