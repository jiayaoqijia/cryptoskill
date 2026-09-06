---
name: skill-readme-linter
track: platform-challenge
version: 0.1.0
summary: Lint SKILL.md and README.md for required sections
---

## Description

Lint SKILL.md and README.md files for required sections. Validates documentation completeness and compliance with standards.

## Inputs

```json
{
  "skill_path": "Path to skill directory"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "valid": true,
    "issues": [],
    "warnings": []
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Lint Skill Docs
```bash
echo '{"skill_path":"./my-skill"}' | python3 scripts/main.py
```

## Examples

### Example 1: Check Documentation
```bash
$ echo '{"skill_path":"dao-proposal-starter"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "valid": true,
    "issues": [],
    "warnings": ["Missing example in SKILL.md"]
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
    "skill_path": "Directory not found"
  }
}
```
