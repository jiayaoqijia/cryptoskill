---
name: spoonos-testing-patterns
description: Test SpoonOS agents effectively. Use when writing unit tests, integration tests, mocking LLM responses, or debugging agent behavior.
---

# Testing Patterns

Comprehensive testing strategies for SpoonOS agents.

## Testing Pyramid

```
        /\
       /  \      E2E Tests (few)
      /----\
     /      \    Integration Tests (some)
    /--------\
   /          \  Unit Tests (many)
  /------------\
```

## Unit Testing Tools

### Testing a Custom Tool

```python
# tests/test_tools.py
import pytest
from unittest.mock import AsyncMock, patch
from my_agent.tools import PriceTool, WalletTool

@pytest.mark.asyncio
async def test_price_tool_success():
    """Test successful price fetch."""
    tool = PriceTool()

    # Mock the HTTP response
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "bitcoin": {"usd": 50000, "usd_24h_change": 2.5}
        })
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await tool.execute(coin_id="bitcoin", currency="usd")

        assert "50,000" in result
        assert "2.50%" in result

@pytest.mark.asyncio
async def test_price_tool_not_found():
    """Test handling of unknown coin."""
    tool = PriceTool()

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={})
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await tool.execute(coin_id="unknown_coin")

        assert "not found" in result.lower()

@pytest.mark.asyncio
async def test_wallet_tool_validation():
    """Test address validation."""
    tool = WalletTool()

    # Invalid address
    result = await tool.execute(address="invalid", chain="ethereum")
    assert "Error" in result

    # Valid address format
    result = await tool.execute(
        address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7",
        chain="ethereum"
    )
    # Should not have validation error
    assert "Invalid" not in result or "validation" not in result.lower()
```

### Testing Tool Parameters

```python
def test_tool_parameters_schema():
    """Verify tool parameter schema."""
    tool = PriceTool()

    params = tool.parameters

    assert params["type"] == "object"
    assert "coin_id" in params["properties"]
    assert "required" in params
    assert "coin_id" in params["required"]

def test_tool_to_param():
    """Test OpenAI-compatible conversion."""
    tool = PriceTool()

    param = tool.to_param()

    assert param["type"] == "function"
    assert param["function"]["name"] == "get_price"
    assert "description" in param["function"]
```

## Mocking LLM Responses

### Mock ChatBot

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from spoon_ai.chat import ChatBot

@pytest.fixture
def mock_chatbot():
    """Create a mock ChatBot that returns predefined responses."""
    chatbot = MagicMock(spec=ChatBot)

    async def mock_chat(messages, tools=None, **kwargs):
        # Return a mock response based on input
        last_message = messages[-1]["content"]

        if "price" in last_message.lower():
            return MagicMock(
                content="I'll check the price for you.",
                tool_calls=[{
                    "id": "call_123",
                    "function": {
                        "name": "get_price",
                        "arguments": '{"coin_id": "bitcoin"}'
                    }
                }]
            )
        else:
            return MagicMock(
                content="I don't understand that request.",
                tool_calls=None
            )

    chatbot.chat = AsyncMock(side_effect=mock_chat)
    return chatbot

@pytest.fixture
def mock_tool_response():
    """Fixture for mocking tool execution."""
    async def _mock_response(tool_name, expected_result):
        tool = MagicMock()
        tool.execute = AsyncMock(return_value=expected_result)
        return tool
    return _mock_response
```

### Using Mock in Tests

```python
# tests/test_agent.py
import pytest
from my_agent import TradingAgent

@pytest.mark.asyncio
async def test_agent_price_query(mock_chatbot):
    """Test agent handles price queries."""
    agent = TradingAgent()
    agent.llm = mock_chatbot

    # Mock tool execution
    agent.tools["get_price"].execute = AsyncMock(
        return_value="BTC: $50,000 USD"
    )

    result = await agent.run("What's the Bitcoin price?")

    # Verify tool was called
    agent.tools["get_price"].execute.assert_called_once()
    assert "50,000" in result

@pytest.mark.asyncio
async def test_agent_max_steps():
    """Test agent respects max_steps limit."""
    agent = TradingAgent()
    agent.max_steps = 2

    # Mock LLM to always request tool calls
    agent.llm.chat = AsyncMock(return_value=MagicMock(
        content="",
        tool_calls=[{"id": "1", "function": {"name": "get_price", "arguments": "{}"}}]
    ))

    result = await agent.run("Complex query requiring many steps")

    assert agent.current_step <= agent.max_steps
```

## Integration Testing

### Testing Agent with Real Tools

```python
# tests/integration/test_agent_integration.py
import pytest
import os

# Skip if no API keys
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="Requires OPENAI_API_KEY"
)

@pytest.mark.asyncio
async def test_agent_full_flow():
    """Integration test with real LLM."""
    from my_agent import ResearchAgent

    agent = ResearchAgent()
    await agent.initialize()

    result = await agent.run("What is 2 + 2?")

    assert "4" in result

@pytest.mark.asyncio
async def test_agent_tool_execution():
    """Test agent executes tools correctly."""
    from my_agent import TradingAgent
    from my_agent.tools import CalculatorTool

    agent = TradingAgent()
    agent.tools.add_tool(CalculatorTool())

    result = await agent.run("Calculate 100 * 5")

    assert "500" in result
```

### Testing with Fixtures

```python
# tests/integration/conftest.py
import pytest
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

@pytest.fixture(scope="session")
def real_agent():
    """Create a real agent for integration tests."""
    return SpoonReactMCP(
        name="test_agent",
        llm=ChatBot(model_name="gpt-4o-mini"),  # Use cheaper model
        tools=ToolManager([]),
        max_steps=5
    )

@pytest.fixture
def isolated_agent(real_agent):
    """Get agent with fresh state."""
    real_agent.reset()
    return real_agent
```

## Testing MCP Tools

### Mock MCP Server

```python
# tests/test_mcp_tools.py
import pytest
from unittest.mock import AsyncMock, patch
from spoon_ai.tools.mcp_tool import MCPTool

@pytest.fixture
def mock_mcp_client():
    """Mock MCP client for testing."""
    with patch('spoon_ai.tools.mcp_tool.MCPClient') as mock:
        client_instance = AsyncMock()
        client_instance.list_tools = AsyncMock(return_value=[
            {"name": "search", "description": "Search the web"}
        ])
        client_instance.call_tool = AsyncMock(return_value={
            "content": [{"type": "text", "text": "Search results..."}]
        })
        mock.return_value = client_instance
        yield client_instance

@pytest.mark.asyncio
async def test_mcp_tool_execution(mock_mcp_client):
    """Test MCP tool execution."""
    tool = MCPTool(
        name="test-mcp",
        mcp_config={"command": "npx", "args": ["-y", "test-mcp"]}
    )

    result = await tool.execute(query="test query")

    mock_mcp_client.call_tool.assert_called_once()
    assert "Search results" in result
```

## Testing StateGraph Workflows

### Graph Unit Tests

```python
# tests/test_graph.py
import pytest
from spoon_ai.graph import StateGraph, END
from typing import TypedDict

class TestState(TypedDict):
    value: int
    processed: bool

def increment(state: TestState) -> dict:
    return {"value": state["value"] + 1}

def double(state: TestState) -> dict:
    return {"value": state["value"] * 2}

def mark_processed(state: TestState) -> dict:
    return {"processed": True}

@pytest.fixture
def simple_graph():
    """Create a simple test graph."""
    graph = StateGraph(TestState)
    graph.add_node("increment", increment)
    graph.add_node("double", double)
    graph.add_node("mark", mark_processed)
    graph.set_entry_point("increment")
    graph.add_edge("increment", "double")
    graph.add_edge("double", "mark")
    graph.add_edge("mark", END)
    return graph.compile()

@pytest.mark.asyncio
async def test_graph_execution(simple_graph):
    """Test graph executes all nodes."""
    result = await simple_graph.invoke({
        "value": 5,
        "processed": False
    })

    # 5 + 1 = 6, 6 * 2 = 12
    assert result["value"] == 12
    assert result["processed"] == True

@pytest.mark.asyncio
async def test_graph_streaming(simple_graph):
    """Test graph streaming output."""
    outputs = []

    async for event in simple_graph.astream({
        "value": 1,
        "processed": False
    }):
        outputs.append(event)

    assert len(outputs) == 3  # One per node
```

### Testing Conditional Edges

```python
def should_continue(state: TestState) -> str:
    if state["value"] > 100:
        return "end"
    return "continue"

@pytest.fixture
def conditional_graph():
    """Graph with conditional routing."""
    graph = StateGraph(TestState)
    graph.add_node("double", double)
    graph.add_node("finish", mark_processed)
    graph.set_entry_point("double")
    graph.add_conditional_edges(
        "double",
        should_continue,
        {"continue": "double", "end": "finish"}
    )
    graph.add_edge("finish", END)
    return graph.compile()

@pytest.mark.asyncio
async def test_conditional_loop(conditional_graph):
    """Test conditional edge routing."""
    result = await conditional_graph.invoke({
        "value": 10,
        "processed": False
    })

    # 10 -> 20 -> 40 -> 80 -> 160 (> 100, stop)
    assert result["value"] == 160
    assert result["processed"] == True
```

## Debugging Patterns

### Debug Logging

```python
# debug_utils.py
import logging
import json
from functools import wraps

logger = logging.getLogger(__name__)

def log_tool_call(func):
    """Decorator to log tool calls."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.debug(f"Tool call: {func.__name__}")
        logger.debug(f"Args: {args}, Kwargs: {kwargs}")

        try:
            result = await func(*args, **kwargs)
            logger.debug(f"Result: {result[:200]}...")
            return result
        except Exception as e:
            logger.error(f"Tool error: {e}")
            raise

    return wrapper

def log_agent_step(agent, step_num, action, result):
    """Log agent execution step."""
    logger.info(json.dumps({
        "agent": agent.name,
        "step": step_num,
        "action": action,
        "result_preview": str(result)[:100]
    }))
```

### Test Debugging

```python
@pytest.mark.asyncio
async def test_with_debug_output(caplog):
    """Test with captured logs."""
    import logging
    caplog.set_level(logging.DEBUG)

    agent = TradingAgent()
    result = await agent.run("Test query")

    # Check logs for debugging
    assert "Tool call" in caplog.text

    # Print all logs if test fails
    for record in caplog.records:
        print(f"{record.levelname}: {record.message}")
```

### Snapshot Testing

```python
# tests/test_snapshots.py
import pytest
import json

@pytest.fixture
def snapshot_dir(tmp_path):
    return tmp_path / "snapshots"

def test_tool_output_snapshot(snapshot_dir):
    """Compare tool output against snapshot."""
    tool = PriceTool()

    # Mock consistent response
    result = {
        "symbol": "BTC",
        "price": 50000,
        "change_24h": 2.5
    }

    snapshot_file = snapshot_dir / "price_output.json"

    if snapshot_file.exists():
        expected = json.loads(snapshot_file.read_text())
        assert result == expected
    else:
        snapshot_dir.mkdir(exist_ok=True)
        snapshot_file.write_text(json.dumps(result, indent=2))
        pytest.skip("Snapshot created")
```

## Test Configuration

### pytest.ini

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks integration tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=my_agent --cov-report=html

# Run only unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/ -m integration

# Run specific test
pytest tests/test_tools.py::test_price_tool_success -v

# Debug mode
pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov

      - name: Run unit tests
        run: pytest tests/unit/ --cov=my_agent

      - name: Run integration tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: pytest tests/integration/ -m integration
```

## Best Practices

1. **Isolate Tests** - Each test should be independent
2. **Mock External Services** - Don't rely on APIs in unit tests
3. **Use Fixtures** - Share setup code efficiently
4. **Test Edge Cases** - Errors, timeouts, empty responses
5. **Keep Tests Fast** - Unit tests should run in milliseconds
6. **Clear Assertions** - One logical assertion per test
