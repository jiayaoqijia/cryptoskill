# Transaction Analysis Skill

## Metadata
- **Name**: transaction-analysis
- **Category**: Web3 Data Intelligence
- **Version**: 1.0.0
- **Author**: Your Name
- **Supported Chains**: Ethereum, Polygon

## Description
A comprehensive on-chain transaction analysis skill for tracking wallet activities, analyzing transaction patterns, and monitoring fund flows across Ethereum and Polygon networks.

## Triggers
- "analyze transaction"
- "track wallet"
- "transaction history"
- "fund flow"
- "wallet activity"

## Capabilities
1. **Transaction History Analysis**: Retrieve and analyze complete transaction history for any address
2. **Fund Flow Tracking**: Track token transfers and ETH movements between addresses
3. **Transaction Pattern Detection**: Identify recurring patterns, frequent counterparties, and unusual activities
4. **Multi-chain Support**: Analyze transactions across Ethereum and Polygon networks
5. **Gas Analysis**: Calculate total gas spent and identify gas optimization opportunities

## Required Environment Variables
```bash
ETHEREUM_RPC=https://eth.llamarpc.com
POLYGON_RPC=https://polygon.llamarpc.com
ETHERSCAN_API_KEY=your_etherscan_api_key
POLYGONSCAN_API_KEY=your_polygonscan_api_key
```

## Available Scripts
1. `get_transaction_history.py` - Retrieve transaction history for an address
2. `analyze_fund_flow.py` - Track token and ETH transfers
3. `detect_patterns.py` - Identify transaction patterns and anomalies
4. `calculate_gas_usage.py` - Analyze gas consumption
5. `get_token_transfers.py` - Get ERC20 token transfer history
6. `analyze_counterparties.py` - Identify frequent transaction counterparties

## Usage Examples

### Example 1: Analyze Wallet Transaction History
```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(skill_paths=["./transaction-analysis"])
await agent.activate_skill("transaction-analysis")

result = await agent.run(
    "Analyze the transaction history for address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
)
```

### Example 2: Track Fund Flow
```python
result = await agent.run(
    "Track all USDC transfers from 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb in the last 30 days"
)
```

### Example 3: Detect Unusual Patterns
```python
result = await agent.run(
    "Detect any unusual transaction patterns for wallet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
)
```

## Prompt Template
When this skill is activated, the agent receives the following context:

```
You are a Web3 transaction analysis expert. You have access to tools that can:
- Retrieve complete transaction histories from Ethereum and Polygon
- Track token transfers and fund flows
- Detect patterns and anomalies in transaction behavior
- Calculate gas usage and optimization opportunities
- Identify frequent counterparties and transaction relationships

When analyzing transactions:
1. Always verify the address format is valid
2. Specify the blockchain network (Ethereum or Polygon)
3. Consider the time range for analysis
4. Look for patterns like recurring transfers, unusual amounts, or suspicious activities
5. Provide actionable insights and recommendations

Available tools: {tool_names}
```

## Output Format
The skill returns structured data including:
- Transaction count and volume
- Top counterparties
- Token transfer summary
- Gas usage statistics
- Detected patterns or anomalies
- Visualization-ready data (JSON format)

## Dependencies
- web3.py >= 6.0.0
- requests >= 2.31.0
- python-dotenv >= 1.0.0
- pandas >= 2.0.0 (optional, for data analysis)

## Notes
- Rate limits apply based on your RPC provider and API keys
- Free tier Etherscan API allows 5 calls/second
- Consider caching results for frequently queried addresses
- Large wallets may require pagination for complete history
