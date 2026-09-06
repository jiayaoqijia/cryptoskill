# api-contract-diff (Track: enterprise-skills)

Detect breaking and non-breaking changes between OpenAPI/Swagger specifications

## Overview

This skill compares two API contract versions and identifies all changes, categorizing them by impact level. It detects removed endpoints, new methods, parameter changes, and response schema modifications to help prevent breaking changes in production.

## Features

- **Breaking Change Detection**: Identify endpoints and methods that were removed
- **Non-Breaking Changes**: Track additions and optional parameter updates
- **Comprehensive Diff**: Compare full OpenAPI schemas including paths, methods, and parameters
- **Impact Assessment**: Categorize changes by severity for API consumers
- **JSON Output**: Structured format for integration with CI/CD pipelines

## Use Cases

- Validate API changes before deployment
- Prevent unintended breaking changes to public APIs
- Document API evolution and compatibility
- Enforce API versioning policies
- Generate API changelog from contract changes

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
| schema1 | object | Yes | First OpenAPI specification |
| schema2 | object | Yes | Second OpenAPI specification (reference) |
| format | string | No | Output format (json, summary) - default: json |

## Example Output

```json
{
  "ok": true,
  "data": {
    "breaking_changes": [
      {
        "type": "removed_endpoint",
        "path": "/posts"
      },
      {
        "type": "removed_method",
        "path": "/users",
        "method": "put"
      }
    ],
    "non_breaking_changes": [],
    "additions": [
      {
        "type": "new_endpoint",
        "path": "/comments"
      },
      {
        "type": "new_method",
        "path": "/users",
        "method": "delete"
      }
    ]
  }
}
```
