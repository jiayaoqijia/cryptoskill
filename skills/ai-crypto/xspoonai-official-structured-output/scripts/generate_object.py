#!/usr/bin/env python3
"""Generate and validate strict JSON objects (schema or Pydantic).

This is a reference implementation stub. Replace `call_llm` with your
agent/LLM invocation. The repair loop uses validation errors to re-prompt.
"""

from __future__ import annotations

import json
from typing import Any, Callable, Type

from pydantic import BaseModel, ValidationError


def _call_llm(prompt: str) -> str:
    """Placeholder for your LLM call."""
    raise NotImplementedError("Wire this to your LLM/agent client.")


def _validate_json_schema(data: dict, schema: dict) -> None:
    """Minimal JSON Schema validation hook.

    Replace with `jsonschema.validate` if available in your environment.
    """
    # Keep this stub to avoid extra dependencies in the repository.
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


def _extract_json_object(text: str) -> str:
    """Best-effort extraction of a JSON object from mixed output."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return text
    return text[start : end + 1]


def _schema_error_summary(data: dict, schema: dict) -> str:
    """Generate a deterministic error summary for repair prompts."""
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


def generate_object(schema: dict, input_text: str | None, call_llm: Callable[[str], str] | None = None) -> dict:
    """Generate a JSON object that matches a JSON Schema."""
    call_llm = call_llm or _call_llm
    safe_input = input_text if input_text is not None else ""
    base_prompt = (
        "You are a JSON generator. Output ONLY valid JSON that matches the given schema.\n"
        "Do not include Markdown, comments, or trailing text.\n\n"
        f"Schema:\n{json.dumps(schema)}\n\nInput:\n{safe_input}\n"
    )

    output = call_llm(base_prompt)
    for _ in range(2):
        try:
            data = json.loads(_extract_json_object(output))
            _validate_json_schema(data, schema)
            return data
        except Exception as exc:  # noqa: BLE001 - used for repair pass
            try:
                candidate = json.loads(_extract_json_object(output))
                error_summary = _schema_error_summary(candidate, schema)
            except Exception:
                error_summary = str(exc)
            repair_prompt = (
                "You must return ONLY valid JSON that matches the schema. Fix the errors.\n\n"
                f"Schema:\n{json.dumps(schema)}\n\n"
                f"Invalid JSON:\n{output}\n\n"
                f"Validation errors:\n{error_summary}\n"
            )
            output = call_llm(repair_prompt)

    raise ValueError("Failed to produce valid JSON after repair attempts.")


def generate_object_pydantic(model: Type[BaseModel], input_text: str | None, call_llm: Callable[[str], str] | None = None) -> BaseModel:
    """Generate a JSON object and parse it into a Pydantic model."""
    call_llm = call_llm or _call_llm
    model_schema = model.model_json_schema()
    safe_input = input_text if input_text is not None else ""
    base_prompt = (
        "You are a JSON generator. Output ONLY valid JSON that matches the given schema.\n"
        "Do not include Markdown, comments, or trailing text.\n\n"
        f"Schema:\n{json.dumps(model_schema)}\n\nInput:\n{safe_input}\n"
    )

    output = call_llm(base_prompt)
    for _ in range(2):
        try:
            data = json.loads(_extract_json_object(output))
            return model.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as exc:
            repair_prompt = (
                "You must return ONLY valid JSON that matches the schema. Fix the errors.\n\n"
                f"Schema:\n{json.dumps(model_schema)}\n\n"
                f"Invalid JSON:\n{output}\n\n"
                f"Validation errors:\n{exc}\n"
            )
            output = call_llm(repair_prompt)

    raise ValueError("Failed to produce valid JSON after repair attempts.")
