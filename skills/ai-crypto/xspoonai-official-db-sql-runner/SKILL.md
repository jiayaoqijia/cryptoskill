---
name: db-sql-runner
track: ai-productivity
version: 0.1.0
summary: Run parameterized SQL queries against configured database
---

## Description

Run parameterized SQL queries against a configured database. Supports safe parameterized queries with dev-mode restrictions for testing and development.

## Inputs

```json
{
  "query": "SELECT * FROM users WHERE id = ?",
  "params": ["value"],
  "database": "dev|test"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "rows": [],
    "count": 0
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Run Query
```bash
echo '{"query":"SELECT * FROM users","params":[],"database":"dev"}' | python3 scripts/main.py
```

## Examples

### Example 1: Query Results
```bash
$ echo '{"query":"SELECT * FROM users WHERE id = ?","params":[1],"database":"dev"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "rows": [{"id": 1, "name": "John"}],
    "count": 1
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
    "query": "Invalid SQL syntax"
  }
}
```
