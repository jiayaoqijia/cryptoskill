---
name: skill-pr-prep
track: platform-challenge
version: 0.1.0
summary: Bundle pull.md and screenshot placeholders for PR
---

## Description

Bundle pull.md and screenshot placeholders for pull request submission. Prepares all required PR documentation and assets.

## Inputs

```json
{
  "skill_path": "Path to skill directory",
  "output_path": "Path to save PR bundle"
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "bundle_path": "Path to PR bundle",
    "files": []
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Prepare PR
```bash
echo '{"skill_path":"./my-skill","output_path":"./pr-ready"}' | python3 scripts/main.py
```

## Examples

### Example 1: Prepare PR Bundle
```bash
$ echo '{"skill_path":"dao-proposal-starter","output_path":"./pr"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "bundle_path": "./pr",
    "files": ["pull.md", "screenshot1.png", "screenshot2.png"]
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
