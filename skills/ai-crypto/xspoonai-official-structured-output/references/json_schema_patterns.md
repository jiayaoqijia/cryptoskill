# JSON Schema Patterns

## Minimal Strict Schema Template

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "field": {"type": "string"}
  },
  "required": ["field"]
}
```

## Repair Prompt (Error-Only)

```
SYSTEM:
You must return ONLY valid JSON that matches the schema. Fix the errors.

USER:
Schema:
<SCHEMA>

Invalid JSON:
<OUTPUT>

Validation errors:
<ERRORS>
```

## Retry Strategy

- First pass: normal strict prompt.
- If validation fails: feed schema + output + error list into repair prompt.
- If still invalid after 2 attempts: return a structured error object from your application layer.
- Input can be empty; output must still strictly match the schema.

## Validation Checklist

- JSON parses successfully
- All required fields present
- No additional keys (unless allowed)
- Enums and formats respected
