---
name: doc-generator
description: Auto-generate API reference documentation from Python code.
version: 1.0.0
author: SpoonOS Contributor
tags: [documentation, markdown, python, automation]
---

# Documentation Generator

A high-impact skill that parses Python source code and generates a standardized Markdown API reference. It utilizes AST parsing to extract docstrings, function signatures, and class structures.

## Quick Start

```python
# Generate docs for a file
result = await agent.run_tool("generate_docs", file_path="src/client.py")
print(result)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [doc_gen.py](scripts/doc_gen.py) | Generates Markdown documentation from Python files |

## Environment Variables

None required. Uses standard library `ast`.

## Best Practices

1. Ensure your code has partial docstrings for better output.
2. Use this to keep `README.md` or `API.md` up to date automatically.
