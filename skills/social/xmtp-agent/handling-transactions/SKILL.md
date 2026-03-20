---
name: handling-transactions
description: Token transactions and wallet integration for XMTP agents. Use when sending USDC, creating transaction requests, or handling transaction confirmations. Triggers on USDC transfer, wallet calls, or transaction reference.
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP transactions

Send and receive token transactions using wallet_sendCalls (EIP-5792) specification.

## When to apply

Reference these guidelines when:
- Sending USDC or other tokens
- Creating transaction requests
- Handling transaction confirmations
- Checking token balances
- Working with smart contract wallets

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Send | CRITICAL | `send-` |
| 2 | Receive | CRITICAL | `receive-` |
| 3 | Balance | HIGH | `balance-` |

## Quick reference

### Send (CRITICAL)
- `send-usdc-transfer` - Create USDC transfer requests
- `send-wallet-calls` - Send wallet_sendCalls messages

### Receive (CRITICAL)
- `receive-transaction-reference` - Handle transaction confirmations

### Balance (HIGH)
- `balance-check` - Check USDC balance

## Supported networks

| Network | Chain ID | USDC Address |
|---------|----------|--------------|
| Base Sepolia | 84532 | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| Base Mainnet | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

## Quick start

```typescript
import { validHex } from "@xmtp/agent-sdk";

// Check balance using viem
const balance = await getUSDCBalance("base-sepolia", validHex(address));

// Create USDC transfer calls (EIP-5792)
const calls = createUSDCTransferCalls(
  "base-sepolia",
  validHex(fromAddress),
  validHex(toAddress),
  1000000 // 1 USDC (6 decimals)
);
await ctx.conversation.sendWalletSendCalls(calls);
```

## Implementation snippets

**USDC token config:**

```typescript
const USDC_TOKENS: Record<string, { address: string; decimals: number }> = {
  "base-sepolia": { address: "0x036CbD53842c5426634e7929541eC2318f3dCF7e", decimals: 6 },
  "base-mainnet": { address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", decimals: 6 },
};
```

**Get USDC balance:**

```typescript
import { createPublicClient, formatUnits, http } from "viem";
import { baseSepolia, base } from "viem/chains";

const getUSDCBalance = async (networkId: string, address: HexString): Promise<string> => {
  const token = USDC_TOKENS[networkId];
  const client = createPublicClient({
    chain: networkId === "base-mainnet" ? base : baseSepolia,
    transport: http(),
  });
  const balance = await client.readContract({
    address: token.address as HexString,
    abi: [{ inputs: [{ name: "account", type: "address" }], name: "balanceOf", outputs: [{ type: "uint256" }], stateMutability: "view", type: "function" }],
    functionName: "balanceOf",
    args: [address],
  });
  return formatUnits(balance, token.decimals);
};
```

**Create USDC transfer calls:**

```typescript
import { toHex } from "viem";

const createUSDCTransferCalls = (
  networkId: string, from: HexString, to: string, amount: number
): WalletSendCalls => {
  const token = USDC_TOKENS[networkId];
  const data = `0xa9059cbb${to.slice(2).padStart(64, "0")}${BigInt(amount).toString(16).padStart(64, "0")}`;
  return {
    version: "1.0",
    from,
    chainId: toHex(networkId === "base-mainnet" ? 8453 : 84532),
    calls: [{ to: token.address as HexString, data: validHex(data) }],
  };
};
```

## How to use

Read individual rule files for detailed explanations:

```
rules/send-usdc-transfer.md
rules/receive-transaction-reference.md
rules/balance-check.md
```

