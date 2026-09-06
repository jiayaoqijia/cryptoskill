# Transaction Analysis Skill

> **Track 1: Web3 Data Intelligence** - On-chain transaction analysis for Ethereum and Polygon

A comprehensive skill for analyzing blockchain transactions, tracking fund flows, and detecting patterns across Ethereum and Polygon networks.

## Features

- 📊 **Transaction History**: Complete transaction history retrieval and analysis
- 💸 **Fund Flow Tracking**: Track ETH and ERC20 token movements
- 🔍 **Pattern Detection**: Identify recurring patterns and anomalies
- ⛽ **Gas Analysis**: Calculate gas usage and optimization opportunities
- 🔗 **Multi-chain**: Support for Ethereum and Polygon networks
- 👥 **Counterparty Analysis**: Identify frequent transaction partners

## Installation

### 1. Copy to Your Project

```bash
# For SpoonReactSkill agents
mkdir -p .agent/skills
cp -r transaction-analysis/ .agent/skills/

# For Claude Code / Cursor
mkdir -p .claude/skills
cp -r transaction-analysis/ .claude/skills/
```

### 2. Install Dependencies

```bash
pip install web3 requests python-dotenv pandas
```

### 3. Configure Environment Variables

Create a `.env` file:

```bash
# Blockchain RPCs
ETHEREUM_RPC=https://eth.llamarpc.com
POLYGON_RPC=https://polygon.llamarpc.com

# API Keys (get free keys from etherscan.io and polygonscan.com)
ETHERSCAN_API_KEY=your_etherscan_api_key
POLYGONSCAN_API_KEY=your_polygonscan_api_key
```

## Usage

### With SpoonReactSkill Agent

```python
from spoon_ai.agents import SpoonReactSkill
from spoon_ai.chat import ChatBot

class TransactionAnalyzer(SpoonReactSkill):
    def __init__(self, **kwargs):
        kwargs.setdefault('skill_paths', ['.agent/skills'])
        kwargs.setdefault('scripts_enabled', True)
        super().__init__(**kwargs)

async def main():
    agent = TransactionAnalyzer(
        llm=ChatBot(llm_provider="openai", model_name="gpt-4o")
    )
    await agent.initialize()
    await agent.activate_skill("transaction-analysis")

    # Analyze a wallet
    result = await agent.run(
        "Analyze transaction history for 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb on Ethereum"
    )
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### With Claude Code

```bash
# Copy skill to Claude Code skills directory
cp -r transaction-analysis/ ~/.claude/skills/

# Use in conversation
"Analyze the transaction history for wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
```

## Available Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `get_transaction_history.py` | Retrieve complete transaction history | `python scripts/get_transaction_history.py <address> <chain>` |
| `analyze_fund_flow.py` | Track token and ETH transfers | `python scripts/analyze_fund_flow.py <address> <chain>` |
| `detect_patterns.py` | Identify transaction patterns | `python scripts/detect_patterns.py <address> <chain>` |
| `calculate_gas_usage.py` | Analyze gas consumption | `python scripts/calculate_gas_usage.py <address> <chain>` |
| `get_token_transfers.py` | Get ERC20 token transfers | `python scripts/get_token_transfers.py <address> <chain>` |
| `analyze_counterparties.py` | Find frequent counterparties | `python scripts/analyze_counterparties.py <address> <chain>` |

## Examples

### Example 1: Basic Transaction Analysis

```bash
python scripts/get_transaction_history.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum
```

**Output:**
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "chain": "ethereum",
  "total_transactions": 1234,
  "first_transaction": "2021-03-15T10:30:00Z",
  "last_transaction": "2024-02-08T15:45:00Z",
  "total_eth_received": "125.5",
  "total_eth_sent": "98.3",
  "net_eth_balance_change": "27.2"
}
```

### Example 2: Token Transfer Analysis

```bash
python scripts/get_token_transfers.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum
```

**Output:**
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "token_transfers": [
    {
      "token": "USDC",
      "contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "total_received": "50000.00",
      "total_sent": "45000.00",
      "net_balance": "5000.00"
    }
  ]
}
```

### Example 3: Pattern Detection

```bash
python scripts/detect_patterns.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum
```

**Output:**
```json
{
  "patterns_detected": [
    {
      "type": "recurring_transfer",
      "description": "Regular USDC transfers to 0xabc... every Monday",
      "frequency": "weekly",
      "average_amount": "1000 USDC"
    },
    {
      "type": "unusual_activity",
      "description": "Large ETH transfer (50 ETH) detected",
      "timestamp": "2024-02-01T12:00:00Z",
      "severity": "medium"
    }
  ]
}
```

## API Rate Limits

| Provider | Free Tier | Rate Limit |
|----------|-----------|------------|
| Etherscan | Yes | 5 calls/second |
| Polygonscan | Yes | 5 calls/second |
| Public RPC | Yes | Varies by provider |

**Tip**: For production use, consider:
- Using paid API plans for higher rate limits
- Implementing caching for frequently queried addresses
- Using private RPC endpoints (Alchemy, Infura)

## Contributing

This skill is part of the **SpoonOS Awesome Skill Challenge - Track 1: Web3 Data Intelligence**.

To improve this skill:
1. Fork the repository
2. Make your changes
3. Test with real wallet addresses
4. Submit a PR with screenshots

## License

MIT License - See LICENSE file for details

## Support

- GitHub Issues: [spoon-awesome-skill/issues](https://github.com/XSpoonAi/spoon-awesome-skill/issues)
- Documentation: [SpoonOS Docs](https://docs.spoon.ai)

## Changelog

### v1.0.0 (2024-02-08)
- Initial release
- Support for Ethereum and Polygon
- 6 analysis scripts
- Pattern detection
- Gas analysis
