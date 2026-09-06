---
name: api-contract-diff
track: enterprise-skills
version: 0.1.0
summary: Compare OpenAPI and GraphQL schemas for breaking changes
---

## Description

Compare OpenAPI and GraphQL schemas to identify breaking changes and incompatibilities. Provides detailed diff output for schema migrations.

## Inputs

```json
{
  "schema_type": "openapi|graphql",
  "schema1": "First schema object",
  "schema2": "Second schema object"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "changes": [],
    "breaking_changes": []
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Compare Schemas
```bash
echo '{"schema_type": "openapi", "schema1": {}, "schema2": {}}' | python3 scripts/main.py
```

## Examples

### Example 1: Compare OpenAPI Schemas
```bash
$ echo '{"schema_type": "openapi", "schema1": {}, "schema2": {}}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "changes": ["Removed endpoint /v1/users"],
    "breaking_changes": ["Parameter type changed from string to integer"]
  }
}
```

## Error Handling

When an error occurs, the skill returns:

```json
{
  "ok": false,
  "error": "Error description",
  "details": {
    "schema_type": "Invalid schema type"
  }
}
```
