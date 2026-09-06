# Structured Output Skill

A skill for producing stable, schema-validated JSON outputs (non-streaming and streaming), similar to `generateObject` and `streamObject` patterns.

## What This Skill Covers

- Strict JSON-only prompting patterns
- JSON Schema validation + retry/repair loop
- Pydantic model validation + parsing
- Streaming JSON assembly with incremental validation

## Quick Start

1. Choose schema format (JSON Schema or Pydantic). Input text can be empty; output must still match the schema.
2. Use the strict prompt templates in `references/`.
3. Validate output and run a repair pass if invalid.

## Example: JSON Schema

```python
from scripts.generate_object import generate_object

schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string"},
        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
        "due_date": {"type": ["string", "null"], "format": "date"}
    },
    "required": ["title", "priority", "due_date"]
}

result = generate_object(schema=schema, input_text="Fix login bug by Friday")
print(result)
```

## Example: Pydantic

```python
from pydantic import BaseModel
from scripts.generate_object import generate_object_pydantic

class Task(BaseModel):
    title: str
    priority: str
    due_date: str | None

result = generate_object_pydantic(model=Task, input_text="Fix login bug by Friday")
print(result.model_dump())
```

## Streaming

See `scripts/stream_object.py` for a buffered stream parser that assembles a JSON object, then validates it against JSON Schema or a Pydantic model (optional repair via `repair_call`).
