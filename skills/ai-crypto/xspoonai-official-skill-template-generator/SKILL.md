---
name: skill-template-generator
track: platform-challenge
version: 0.1.0
summary: Generate a new skill skeleton with placeholders
---

## Description

Generate a new skill skeleton with placeholders. Creates complete skill structure with README.md, SKILL.md, and scripts directory.

## Inputs

```json
{
  "skill_name": "Name of new skill",
  "track": "web3-core-operations|enterprise-skills",
  "output_path": "Path to create skill"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "skill_path": "Path to created skill",
    "files_created": []
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Generate Skill
```bash
echo '{"skill_name":"my-skill","track":"web3-core-operations"}' | python3 scripts/main.py
```

## Examples

### Example 1: Create New Skill
```bash
$ echo '{"skill_name":"token-analyzer","track":"web3-data-intelligence","output_path":"./"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "skill_path": "./token-analyzer",
    "files_created": ["README.md", "SKILL.md", "scripts/main.py"]
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
    "skill_name": "Skill name already exists"
  }
}
```
