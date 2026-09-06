---
name: test-guided-tool-run
description: Use when user asks to "run tool as function", "test directly", or "call standalone" (outside MCP server). Essential for correct mock Context setup (MagicMock + AsyncMock). Finds integration tests with real test data. 
user-invocable: false
---

# Test-Guided Tool Run Skill

Before running any MCP tool directly (outside the MCP server), examine the corresponding integration test to understand the correct usage pattern.

## Workflow

### 1. Find the Integration Test

```bash
python .claude/skills/test-guided-tool-run/scripts/find_test.py <tool_name>
```

Example:

```bash
python .claude/skills/test-guided-tool-run/scripts/find_test.py get_transaction_info
```

### 2. Read the Integration Test

The script outputs the test file path. Read it to understand:

- Import statements and mock context setup
- Real test data (addresses, transaction hashes, etc.)
- Expected response structure

### 3. Create Your Test Script

Use this template in `/tmp/claude/.../scratchpad/`:

```python
#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from blockscout_mcp_server.tools.<category>.<tool_module> import <tool_function>


def create_mock_ctx():
    """Create a mock MCP Context object (pattern from tests/conftest.py)."""
    ctx = MagicMock()
    ctx.report_progress = AsyncMock()
    ctx.info = AsyncMock()
    return ctx


async def main():
    ctx = create_mock_ctx()
    try:
        result = await <tool_function>(
            # Your parameters here
            ctx=ctx
        )
        print("Success! Result:")
        print(result)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Run Your Test Script

```bash
python /tmp/claude/.../scratchpad/your_test_script.py
```
