---
name: trongrid-contract-analysis
description: "Analyze TRON smart contracts including deployment info, ABI methods, transaction patterns, top callers, energy costs, and safety assessment. Use when a user asks about a smart contract, wants to verify contract safety, check what a contract does, identify top callers, or detect potential scams. Covers TRC-20/TRC-721 identification, open-source verification, and risk scoring."
metadata:
  version: "1.0.0"
  mcp-server: trongrid
---

# Contract Analysis

Perform deep analysis of TRON smart contracts — deployment details, method signatures, call patterns, top callers, energy economics, and safety risk assessment.

# MCP Server
- **Prerequisite**: [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Instructions

### Step 1: Fetch Contract Basics

Run in parallel:

1. `getContractInfo` — Contract name, deployer (origin_address), `consume_user_resource_percent`, `origin_energy_limit`, creation time, energy usage stats
2. `getContract` — Full ABI definition, bytecode, whether ABI is available (indicates open-source status)

### Step 2: Parse Contract Methods

From the ABI, categorize all methods:

- **Read-only** (view/pure): Safe calls, no state changes
- **State-changing**: transfers, approvals, settings
- **Admin/Owner**: privileged ops (mint, pause, blacklist, upgrade)
- **Events**: what the contract logs

Identify standard interfaces: TRC-20, TRC-721, TRC-1155, proxy/upgradeable patterns.

### Step 3: Analyze Transaction Activity

1. `getContractTransactions` — Total count, recent patterns, success/failure rate
2. `getEventsByContractAddress` — Most frequent events, parameter patterns
3. `getContractInternalTransactions` — Inter-contract calls, TRX transfers within execution

### Step 4: Identify Top Callers

From transaction data, aggregate:
- Top 5 by transaction count
- Top 5 by value (TRX or token amount)
- Classify callers: exchange, bot, regular user, other contract

### Step 5: Estimate Energy Costs

Call `estimateEnergy` with common method calls to assess:
- Typical energy cost per transaction type
- Whether the contract is energy-efficient
- Cost split between user and contract owner (based on `consume_user_resource_percent`)

### Step 6: Safety Assessment

**High Risk indicators:**
- No ABI (unverified/closed source)
- Unlimited mint capability
- Pause/freeze can lock user funds
- Blacklist function, self-destruct, hidden transfer fees
- Proxy pattern (upgradeable logic)
- `consume_user_resource_percent = 100` (users pay all energy)

**Medium Risk indicators:**
- Very few unique callers vs. high tx count
- Recently created with sudden high activity
- Admin functions without timelock/multisig

**Positive indicators:**
- Open-source verified, standard implementation
- Timelock on admin functions, multisig requirements
- Long history with consistent activity, diverse callers

### Step 7: Compile Contract Report

```
## Contract Analysis: [address]

### Deployment
- Name: [name] | Deployer: [address]
- Deployed: [date] | Open Source: [Yes/No]
- Standard: [TRC-20/TRC-721/Custom]

### Methods
- Total: [count] (Read: [X], Write: [Y], Admin: [Z])

### Top Methods (by call frequency)
| Method | Calls | Avg Energy |
|--------|-------|------------|
| transfer() | XX,XXX | X,XXX |

### Top Callers
| Address | Tx Count | Label |
|---------|----------|-------|
| TXxx... | X,XXX | [Exchange/Bot/Unknown] |

### Activity
- Total Txs: [count] | Daily Avg: [count]
- Success Rate: [X.X%] | Unique Callers: [count]

### Energy Economics
- User Pays: [X%] | Avg Energy/Tx: [amount]

### Safety Score: [Safe / Caution / High Risk]
- Risk Factors: [list]
- Positive Factors: [list]
- Recommendation: [actionable advice]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No ABI found | Contract not verified or ABI cleared | Note as unverified; analyze bytecode patterns and transaction data instead |
| Address is not a contract | Regular account address provided | Inform user this is a regular account, suggest using trongrid-account-profiling skill |
| No transactions | Newly deployed or unused contract | Report as inactive; check deployer's other contracts for context |
| Contract self-destructed | Contract no longer exists on-chain | Inform user; historical tx data may still be available |

## Examples

- [Analyze USDT contract](examples/analyze-usdt-contract.md)
- [Check contract safety](examples/check-contract-safety.md)
