---
name: spoonos-application-templates
description: Ready-to-use agent application templates for common Web3 use cases. Use when building trading bots, NFT minters, DAO assistants, portfolio managers, or research agents with SpoonOS framework.
---

# Application Templates

Production-ready templates for building SpoonOS agents.

## Quick Start

```bash
# Copy template
cp -r templates/trading-bot my-trading-bot
cd my-trading-bot

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
python main.py
```

## Available Templates

| Template | Use Case | Key Features |
|----------|----------|--------------|
| `trading-bot` | DeFi trading automation | Price monitoring, swap execution, PnL tracking |
| `nft-minter` | NFT creation & deployment | Metadata generation, IPFS upload, contract deployment |
| `dao-assistant` | Governance participation | Proposal monitoring, voting automation, delegation |
| `portfolio-manager` | Multi-chain asset tracking | Balance aggregation, performance analytics |
| `research-agent` | Market analysis | News aggregation, sentiment analysis, report generation |

## Template Structure

```
template-name/
├── main.py              # Entry point
├── agent.py             # Agent configuration
├── tools/               # Custom tools
│   └── __init__.py
├── config/
│   └── settings.py      # Configuration
├── requirements.txt
├── .env.example
└── README.md
```

## Trading Bot Template

### Configuration

```python
# agent.py
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from tools import PriceMonitorTool, SwapExecutorTool, PositionTrackerTool

class TradingAgent(SpoonReactMCP):
    name = "trading_bot"
    description = "Automated DeFi trading agent"

    system_prompt = """You are a DeFi trading assistant.

    CAPABILITIES:
    - Monitor token prices across DEXs
    - Execute swaps with slippage protection
    - Track portfolio positions and PnL

    RULES:
    - Always check price impact before swaps
    - Never exceed configured max slippage
    - Log all transactions for audit
    """

    max_steps = 10

    def __init__(self):
        super().__init__(
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([
                PriceMonitorTool(),
                SwapExecutorTool(),
                PositionTrackerTool()
            ])
        )
```

### Tools

See `references/trading-bot.md` for complete tool implementations.

## NFT Minter Template

### Configuration

```python
# agent.py
from spoon_ai.agents import SpoonReactMCP
from tools import MetadataGeneratorTool, IPFSUploadTool, ContractDeployTool

class NFTMinterAgent(SpoonReactMCP):
    name = "nft_minter"
    description = "NFT creation and deployment agent"

    system_prompt = """You are an NFT creation assistant.

    WORKFLOW:
    1. Generate or process artwork metadata
    2. Upload assets to IPFS via Pinata
    3. Deploy or interact with NFT contracts
    4. Mint tokens with proper metadata URI

    STANDARDS:
    - Follow ERC-721/ERC-1155 metadata standards
    - Validate image dimensions and formats
    - Ensure IPFS pinning before minting
    """
```

See `references/nft-minter.md` for complete implementation.

## DAO Assistant Template

### Configuration

```python
# agent.py
from spoon_ai.agents import SpoonReactMCP
from tools import ProposalMonitorTool, VotingTool, DelegationTool

class DAOAssistantAgent(SpoonReactMCP):
    name = "dao_assistant"
    description = "DAO governance participation agent"

    system_prompt = """You are a DAO governance assistant.

    CAPABILITIES:
    - Monitor active proposals on Snapshot/Tally
    - Analyze proposal impact and voting patterns
    - Execute votes based on configured preferences
    - Manage delegation settings

    GOVERNANCE PROTOCOLS:
    - Snapshot (off-chain): gasless voting
    - Tally (on-chain): Governor contracts
    - Compound Governor: timelock execution
    """
```

See `references/dao-assistant.md` for complete implementation.

## Portfolio Manager Template

### Configuration

```python
# agent.py
from spoon_ai.agents import SpoonReactMCP
from tools import BalanceAggregatorTool, PerformanceTrackerTool, AlertTool

class PortfolioManagerAgent(SpoonReactMCP):
    name = "portfolio_manager"
    description = "Multi-chain portfolio tracking agent"

    system_prompt = """You are a portfolio management assistant.

    CAPABILITIES:
    - Aggregate balances across EVM chains
    - Track token prices and portfolio value
    - Calculate performance metrics (ROI, PnL)
    - Send alerts on significant changes

    SUPPORTED CHAINS:
    Ethereum, Polygon, Arbitrum, Optimism, Base
    """
```

See `references/portfolio-manager.md` for complete implementation.

## Research Agent Template

### Configuration

```python
# agent.py
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.tools.mcp_tool import MCPTool

class ResearchAgent(SpoonReactMCP):
    name = "research_agent"
    description = "Crypto market research agent"

    system_prompt = """You are a crypto research analyst.

    CAPABILITIES:
    - Search and aggregate crypto news
    - Analyze on-chain metrics
    - Generate research reports
    - Track social sentiment

    OUTPUT FORMAT:
    - Executive summary
    - Key metrics
    - Risk assessment
    - Actionable insights
    """

    def __init__(self):
        tavily = MCPTool(
            name="tavily-search",
            mcp_config={
                "command": "npx",
                "args": ["-y", "tavily-mcp"],
                "env": {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")}
            }
        )
        super().__init__(
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([tavily, OnChainMetricsTool()])
        )
```

See `references/research-agent.md` for complete implementation.

## Customization Guide

### Adding Custom Tools

```python
from spoon_ai.tools.base import BaseTool
from pydantic import Field

class MyCustomTool(BaseTool):
    name: str = "my_tool"
    description: str = "What this tool does"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param1"]
    })

    async def execute(self, param1: str) -> str:
        # Implementation
        return result
```

### Modifying System Prompts

Effective prompts include:
- Clear role definition
- Specific capabilities list
- Behavioral rules/constraints
- Output format expectations

### Adding MCP Tools

```python
from spoon_ai.tools.mcp_tool import MCPTool

# NPX-based tool
my_mcp_tool = MCPTool(
    name="tool-name",
    mcp_config={
        "command": "npx",
        "args": ["-y", "package-name"],
        "env": {"API_KEY": os.getenv("API_KEY")}
    }
)

# Add to agent
agent.tools.add_tool(my_mcp_tool)
```

## Environment Variables

All templates use these common variables:

```bash
# LLM Provider
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Web3
PRIVATE_KEY=0x...
RPC_URL=https://eth.llamarpc.com

# Tools
TAVILY_API_KEY=tvly-...
ETHERSCAN_API_KEY=...
```

## Running Templates

### Development Mode

```bash
# Interactive CLI
python main.py

# Single query
python main.py --query "Check ETH price"
```

### Production Mode

```bash
# With logging
python main.py --log-level INFO

# As daemon
nohup python main.py --daemon &
```

## References

- `references/trading-bot.md` - Complete trading bot implementation
- `references/nft-minter.md` - NFT minting tools and workflows
- `references/dao-assistant.md` - DAO governance integration
- `references/portfolio-manager.md` - Portfolio tracking implementation
- `references/research-agent.md` - Research agent tools
