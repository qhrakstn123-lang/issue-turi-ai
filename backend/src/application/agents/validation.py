from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


class LLMResponseValidationError(ValueError):
    pass


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
