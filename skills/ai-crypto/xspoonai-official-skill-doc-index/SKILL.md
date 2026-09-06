---
name: skill-doc-index
track: platform-challenge
version: 0.1.0
summary: Build an index of skills and summaries
---

## Description

Build an index of all skills with summaries and metadata. Creates searchable documentation index for skill discovery.

## Inputs

```json
{
  "skills_path": "Path to skills directory",
  "format": "json|markdown"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "index": [],
    "total_skills": 50
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Build Index
```bash
echo '{"skills_path":"./","format":"json"}' | python3 scripts/main.py
```

## Examples

### Example 1: Generate Skill Index
```bash
$ echo '{"skills_path":".","format":"markdown"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "index": [{"name": "dao-proposal-starter", "summary": "Create DAO proposals"}],
    "total_skills": 50
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
    "skills_path": "Directory not found"
  }
}
```
