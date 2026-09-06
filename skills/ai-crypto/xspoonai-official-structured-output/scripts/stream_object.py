#!/usr/bin/env python3
"""Stream and assemble a single JSON object from token chunks.

Replace `stream_llm` with your streaming client. This parser buffers
text until it forms a valid JSON object, then optionally validates it.
"""

from __future__ import annotations

import json
from typing import Callable, Iterable, Type

from pydantic import BaseModel, ValidationError


def stream_llm(prompt: str) -> Iterable[str]:
    """Placeholder for streaming LLM tokens."""
    raise NotImplementedError("Wire this to your streaming client.")


def _extract_json_object(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return text
    return text[start : end + 1]


def _validate_json_schema(data: dict, schema: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("Output must be a JSON object.")
    for key in schema.get("required", []):
        if key not in data:
            raise ValueError(f"Missing required field: {key}")
    if schema.get("additionalProperties") is False:
        allowed = set(schema.get("properties", {}).keys())
        extra = set(data.keys()) - allowed
        if extra:
            raise ValueError(f"Unexpected fields: {sorted(extra)}")


def _schema_error_summary(data: dict, schema: dict) -> str:
    errors = []
    required = schema.get("required", [])
    for key in required:
        if key not in data:
            errors.append(f"Missing required field: {key}")
    if schema.get("additionalProperties") is False:
        allowed = set(schema.get("properties", {}).keys())
        extra = set(data.keys()) - allowed
        if extra:
            errors.append(f"Unexpected fields: {sorted(extra)}")
    return "\n".join(errors) if errors else "Unknown schema mismatch."


def stream_object(
    prompt: str,
    schema: dict | None = None,
    model: Type[BaseModel] | None = None,
    repair_call: Callable[[str], str] | None = None,
) -> dict:
    buffer = ""
    for chunk in stream_llm(prompt):
        buffer += chunk
        try:
            data = json.loads(_extract_json_object(buffer))
            if isinstance(data, dict):
                break
        except json.JSONDecodeError:
            continue
    else:
        raise ValueError("Stream ended without a complete JSON object.")

    if model is not None:
        try:
            return model.model_validate(data).model_dump()
        except ValidationError as exc:
            if repair_call is None:
                raise
            repair_prompt = (
                "You must return ONLY valid JSON that matches the schema. Fix the errors.\n\n"
                f"Schema:\n{json.dumps(model.model_json_schema())}\n\n"
                f"Invalid JSON:\n{data}\n\n"
                f"Validation errors:\n{exc}\n"
            )
            repaired = repair_call(repair_prompt)
            return model.model_validate(json.loads(_extract_json_object(repaired))).model_dump()

    if schema is not None:
        try:
            _validate_json_schema(data, schema)
            return data
        except Exception as exc:  # noqa: BLE001 - used for repair pass
            if repair_call is None:
                raise
            error_summary = _schema_error_summary(data, schema)
            repair_prompt = (
                "You must return ONLY valid JSON that matches the schema. Fix the errors.\n\n"
                f"Schema:\n{json.dumps(schema)}\n\n"
                f"Invalid JSON:\n{data}\n\n"
                f"Validation errors:\n{error_summary}\n"
            )
            repaired = repair_call(repair_prompt)
            repaired_data = json.loads(_extract_json_object(repaired))
            _validate_json_schema(repaired_data, schema)
            return repaired_data

    return data
