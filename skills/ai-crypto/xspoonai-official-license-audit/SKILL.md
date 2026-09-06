---
name: license-audit
track: enterprise-skills
version: 0.1.0
summary: Collect and audit dependency license metadata
---

## Description

Collect license metadata for project dependencies. Performs license compliance audits and generates license reports for open source projects.

## Inputs

```json
{
  "project_path": "Path to project directory",
  "format": "json|csv"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "dependencies": [],
    "licenses": []
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Audit Project Licenses
```bash
echo '{"project_path": ".", "format": "json"}' | python3 scripts/main.py
```

## Examples

### Example 1: License Report
```bash
$ echo '{"project_path": ".", "format": "json"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "dependencies": ["numpy", "requests"],
    "licenses": ["MIT", "Apache-2.0"]
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
    "project_path": "Directory not found"
  }
}
```
