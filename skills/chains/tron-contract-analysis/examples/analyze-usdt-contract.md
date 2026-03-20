# Example: Analyze USDT Contract

## User Prompt

```
Analyze the USDT contract on TRON: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t
```

## Expected Workflow

1. **Contract Info** → `getContractInfo("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")` → Settings, deployer
2. **Contract ABI** → `getContract("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")` → Full ABI + bytecode
3. **Token Info** → `getTrc20Info("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")` → Name, symbol, decimals
4. **Transactions** → `getContractTransactions("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", limit=200)` → Recent calls
5. **Events** → `getEventsByContractAddress("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", limit=200)` → Transfer events
6. **Top Holders** → `getTrc20TokenHolders("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", limit=20)` → Holder distribution
7. **Energy Estimate** → `estimateEnergy(owner, contract, "transfer(address,uint256)", params)` → Cost per transfer

## Expected Output (Sample)

```
## Contract Analysis: TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t

### Deployment Info
- Contract Name: TetherToken
- Deployer: THPvaUhoh2Qn2y9THCZML3H4Af3Q3A9m6r
- Deployed: 2019-04-16
- Open Source: Yes (ABI available)
- Standard: TRC-20

### Method Summary
- Total Methods: 23
- Read-only: 8 (name, symbol, decimals, totalSupply, balanceOf, allowance, ...)
- State-changing: 9 (transfer, approve, transferFrom, issue, redeem, ...)
- Admin/Privileged: 6 (addBlackList, removeBlackList, pause, unpause, ...)

### Popular Methods (by call frequency)
| Rank | Method          | Call Count | Avg Energy |
|------|-----------------|-----------|------------|
| 1    | transfer()      | ~800,000/day | 14,631 |
| 2    | approve()       | ~50,000/day  | 12,500 |
| 3    | transferFrom()  | ~30,000/day  | 16,000 |

### Top 5 Holders
| Rank | Address     | Balance        | % of Supply |
|------|------------|---------------|-------------|
| 1    | TKHuV...   | 12,500,000,000 | 21.3%      |
| 2    | TVGDb...   | 8,200,000,000  | 14.0%      |
| 3    | TMuA2...   | 3,100,000,000  | 5.3%       |

### Energy Economics
- User Energy Share: 0% (contract pays all energy)
- Avg Energy per Transfer: ~14,631
- Origin Energy Limit: 10,000,000

### Safety Score: Safe

**Positive Factors:**
- Open-source verified contract
- Standard TRC-20 implementation
- Operated by Tether (established issuer)
- Extremely high holder count and activity
- Long operational history (since 2019)

**Caution Factors:**
- Admin can blacklist addresses (addBlackList)
- Admin can pause all transfers (pause)
- Admin can issue new tokens (issue) — centralized supply control
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getContractInfo` | 1 | Contract settings |
| `getContract` | 1 | ABI + bytecode |
| `getTrc20Info` | 1 | Token metadata |
| `getContractTransactions` | 1 | Transaction history |
| `getEventsByContractAddress` | 1 | Event logs |
| `getTrc20TokenHolders` | 1 | Holder distribution |
| `estimateEnergy` | 1 | Energy cost |
