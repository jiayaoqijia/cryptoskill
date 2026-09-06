# Pydantic Patterns

## Model First

Define a single source of truth model and validate all outputs against it.

```python
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    priority: str
    due_date: str | None
```

## Repair Loop

- Try parsing into the model.
- If validation fails, re-prompt with errors and require JSON-only output.

## JSON-Only Prompt

```
SYSTEM:
You are a JSON generator. Output ONLY valid JSON.

USER:
Return JSON matching this Pydantic model schema:
<MODEL_SCHEMA>

Input:
<INPUT>
```
