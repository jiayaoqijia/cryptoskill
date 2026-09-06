---
name: test-generator
description: auto-generate pytest scaffolds from python source code.
version: 1.0.0
author: SpoonOS Contributor
tags: [testing, pytest, automation, code-quality]
---

# Unit Test Generator

A high-impact skill that automatically scaffolds `pytest` test files based on your Python source code. It parses your code structure (classes and functions) and generates corresponding test functions.

## Quick Start

```python
# Generate tests for a file
result = await agent.run_tool("generate_tests", file_path="src/calculator.py")
print(result)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [generate_tests.py](scripts/generate_tests.py) | Analyzes code and generates test files |

## Environment Variables

None required. Uses standard library `ast`.

## Best Practices

1. Use this tool to quickly bootstrap a test suite for legacy code.
2. The generated tests are scaffolds; you must fill in the assertions!
