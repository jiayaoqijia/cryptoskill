# Policies

**⚠️ MANDATORY: Every wallet MUST have a policy attached.**

Policies define guardrails for agent behavior — what transactions are allowed or denied. They are your first line of defense against abuse.

---

## Why Policies Are Required

Without policies, an agent wallet can:
- Send unlimited amounts
- Interact with any contract
- Operate on any chain
- Drain the entire wallet

**Never create a wallet without a policy. No exceptions.**

---

## Create Policy

```bash
POST /v1/policies
```

### Request

```json
{
  "version": "1.0",
  "name": "Agent spending limits",
  "chain_type": "ethereum",
  "rules": [
    {
      "name": "Allow transfers up to 0.05 ETH",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "value",
          "operator": "lte",
          "value": "50000000000000000"
        }
      ],
      "action": "ALLOW"
    }
  ]
}
```

### Response

```json
{
  "id": "tb54eps4z44ed0jepousxi4n",
  "name": "Agent spending limits",
  "chain_type": "ethereum",
  "version": "1.0",
  "rules": [...],
  "created_at": 1741833088894
}
```

---

## Recommended Policy Templates

### 🔒 Conservative (Recommended for Start)

Maximum safety, minimum risk:

```json
{
  "version": "1.0",
  "name": "Conservative agent policy",
  "chain_type": "ethereum",
  "rules": [
    {
      "name": "Max 0.01 ETH per tx (~$25)",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "value",
          "operator": "lte",
          "value": "10000000000000000"
        }
      ],
      "action": "ALLOW"
    },
    {
      "name": "Base mainnet only",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "chain_id",
          "operator": "eq",
          "value": "8453"
        }
      ],
      "action": "ALLOW"
    }
  ]
}
```

### ⚖️ Moderate

Balanced for regular use:

```json
{
  "version": "1.0",
  "name": "Moderate agent policy",
  "chain_type": "ethereum",
  "rules": [
    {
      "name": "Max 0.05 ETH per tx (~$100)",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "value",
          "operator": "lte",
          "value": "50000000000000000"
        }
      ],
      "action": "ALLOW"
    },
    {
      "name": "L2 chains only",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "chain_id",
          "operator": "in",
          "value": ["8453", "42161", "10", "137"]
        }
      ],
      "action": "ALLOW"
    }
  ]
}
```

### 🎯 DeFi-Specific

For DeFi operations with contract allowlist:

```json
{
  "version": "1.0",
  "name": "DeFi agent policy",
  "chain_type": "ethereum",
  "rules": [
    {
      "name": "Max 0.1 ETH per tx",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "value",
          "operator": "lte",
          "value": "100000000000000000"
        }
      ],
      "action": "ALLOW"
    },
    {
      "name": "Base only",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "chain_id",
          "operator": "eq",
          "value": "8453"
        }
      ],
      "action": "ALLOW"
    },
    {
      "name": "Only approved contracts",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "to",
          "operator": "in",
          "value": [
            "0x...",
            "0x...",
            "0x..."
          ]
        }
      ],
      "action": "ALLOW"
    }
  ]
}
```

---

## Policy Rules

Each rule has:
- `name` — Human-readable name
- `method` — Transaction method this rule applies to
- `conditions` — Array of conditions that must ALL be true
- `action` — `ALLOW` or `DENY`

### Methods

| Method | Description |
|--------|-------------|
| `eth_sendTransaction` | Send EVM transaction |
| `eth_signTransaction` | Sign EVM transaction |
| `eth_signTypedData_v4` | Sign typed data (EIP-712) |
| `signTransaction` | Sign Solana transaction |
| `signAndSendTransaction` | Sign and send Solana transaction |
| `*` | All methods (use carefully!) |

### Conditions

#### Ethereum Transaction Conditions

```json
{
  "field_source": "ethereum_transaction",
  "field": "to",
  "operator": "eq",
  "value": "0x..."
}
```

Fields: `to`, `value`, `chain_id`

#### Operators

| Operator | Description |
|----------|-------------|
| `eq` | Equals |
| `gt` | Greater than |
| `gte` | Greater than or equal |
| `lt` | Less than |
| `lte` | Less than or equal |
| `in` | In list |
| `in_condition_set` | In condition set |

---

## ⚠️ Policy Anti-Patterns

**Never do these:**

```json
// ❌ No spending limit
{
  "name": "Allow everything",
  "method": "*",
  "conditions": [],
  "action": "ALLOW"
}

// ❌ Limit too high
{
  "field": "value",
  "operator": "lte",
  "value": "10000000000000000000"  // 10 ETH = ~$25,000!
}

// ❌ No chain restriction (allows expensive mainnet txs)
{
  "name": "Any chain",
  "method": "eth_sendTransaction",
  "conditions": [{
    "field": "value",
    "operator": "lte",
    "value": "100000000000000000"
  }],
  "action": "ALLOW"
}
```

---

## API Operations

### Get Policy

```bash
GET /v1/policies/{policy_id}
```

### Update Policy

```bash
PATCH /v1/policies/{policy_id}
```

### Delete Policy

```bash
DELETE /v1/policies/{policy_id}
```

**⚠️ PROTECTED: Requires explicit verbal confirmation from user.**

Before executing, the agent must:
1. Explain what policy will be deleted and security implications
2. Ask user to confirm by saying something explicit like "yes, delete the policy"
3. Only proceed after clear confirmation

### Add Rule to Policy

```bash
POST /v1/policies/{policy_id}/rules
```

### Delete Rule from Policy

```bash
DELETE /v1/policies/{policy_id}/rules/{rule_id}
```

**⚠️ PROTECTED: Requires explicit verbal confirmation from user.**

Rule deletion weakens security. Always confirm with user before executing.

---

## Policy Checklist

Before attaching a policy to a wallet:

```
□ Spending limit is set (recommend <0.1 ETH / ~$250)
□ Chain is restricted (recommend L2 only)
□ Contract allowlist is configured (if DeFi)
□ Policy name is descriptive
□ Rules are tested on testnet first
```
