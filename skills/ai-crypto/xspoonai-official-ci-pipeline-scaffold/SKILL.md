---
name: ci-pipeline-scaffold
track: enterprise-skills
version: 0.1.0
summary: Generate minimal CI YAML for lint, test, and build
---

## Description

Emit minimal CI YAML configuration for common CI/CD platforms. Supports GitHub Actions, GitLab CI, and other CI systems with lint, test, and build stages.

## Inputs

```json
{
  "platform": "github|gitlab|jenkins",
  "language": "python|javascript|go",
  "stages": ["lint", "test", "build"]
}
```

## Outputs

```json
{
  "ok": true,
  "data": {
    "yaml": "CI YAML content",
    "filename": ".github/workflows/ci.yml"
  }
}
```

## Usage

### Demo Mode
```bash
python scripts/main.py --demo
```

### Generate CI Config
```bash
echo '{"platform": "github", "language": "python", "stages": ["lint", "test", "build"]}' | python3 scripts/main.py
```

## Examples

### Example 1: GitHub Actions CI
```bash
$ echo '{"platform": "github", "language": "python"}' | python3 scripts/main.py
{
  "ok": true,
  "data": {
    "yaml": "name: CI\non: push\njobs:\n  lint:\n    runs-on: ubuntu-latest",
    "filename": ".github/workflows/ci.yml"
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
    "platform": "Unsupported platform"
  }
}
```
