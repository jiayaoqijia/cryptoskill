---
name: skill-ci-checklist
track: platform-challenge
version: 0.1.0
summary: Emit PR checklist for skill quality gates
---

## Description

Generate a comprehensive PR checklist for skill quality gates. Validates that skills meet submission requirements before pull request.

## Inputs

```json
{
  "skill_path": "Path to skill directory",
  "skill_name": "Skill name"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "checklist": [],
    "passed": true
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Generate Checklist
```bash
echo '{"skill_path":"./my-skill","skill_name":"my-skill"}' | python3 scripts/main.py
```

## Examples

### Example 1: Check Skill Quality
```bash
$ echo '{"skill_path":"web3-core-operations/dao-proposal-starter","skill_name":"dao-proposal-starter"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "checklist": ["✓ README.md exists", "✓ SKILL.md exists", "✓ Scripts working"],
    "passed": true
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
