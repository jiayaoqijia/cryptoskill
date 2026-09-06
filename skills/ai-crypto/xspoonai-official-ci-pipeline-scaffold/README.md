# ci-pipeline-scaffold (Track: enterprise-skills)

Generate production-ready CI/CD pipeline configurations for GitHub Actions and other platforms

## Overview

This skill generates complete CI/CD pipeline configurations based on project type and required stages. It creates workflow files with build, test, and deployment steps optimized for different technology stacks.

## Features

- **Multi-Language Support**: Python, Node.js, Java, Go configurations
- **Stage Templates**: Configurable build, test, lint, and deploy stages
- **Best Practices**: Includes caching, parallel jobs, and security scanning
- **GitHub Actions Ready**: Generate `.github/workflows/*.yml` files
- **Extensible**: Add custom stages and steps

## Use Cases

- Bootstrap new projects with CI/CD pipelines
- Standardize pipeline configuration across teams
- Generate pipeline templates for different project types
- Ensure consistent deployment practices
- Automate code quality checks

## Quickstart
```bash
python3 scripts/main.py --help
```

## Example
```bash
python3 scripts/main.py --demo
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_type | string | Yes | Project type (python, node, java, go) |
| stages | array | Yes | Pipeline stages to include (build, test, deploy) |
| platform | string | No | Platform (github, gitlab, azure) - default: github |

## Example Output

```json
{
  "ok": true,
  "data": {
    "config": "name: CI Pipeline\n\non:\n  push:\n    branches: [ main, develop ]\n\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - run: pytest tests/",
    "filename": ".github/workflows/ci.yml",
    "project_type": "python",
    "stages": ["build", "test", "deploy"]
  }
}
```
