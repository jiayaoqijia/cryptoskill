---
title: Create USDC transfer requests
impact: CRITICAL
tags: transactions, usdc, transfer, wallet
---

## Create USDC transfer requests

Use `createUSDCTransferCalls` to create EIP-5792 compliant transfer requests.

**Basic transfer:**

```typescript
import { createUSDCTransferCalls } from "../../utils/transactions";
import { validHex } from "@xmtp/agent-sdk";

const networkId = "base-sepolia"; // or "base-mainnet"

// Create transfer request (amount in smallest units, 6 decimals)
const walletSendCalls = createUSDCTransferCalls(
  networkId,
  validHex(senderAddress),  // from
  validHex(recipientAddress), // to
  1000000 // 1 USDC = 1,000,000 (6 decimals)
);

// Send to conversation
await ctx.conversation.sendWalletSendCalls(walletSendCalls);
```

**Parse user input:**

```typescript
// Convert USDC string to base units
const parseUsdcToBaseUnits = (raw: string): number | null => {
  const s = raw.trim();
  if (!s) return null;

  // Accept: "2", "2.5", ".5"
  if (!/^(?:\d+(?:\.\d+)?|\.\d+)$/.test(s)) return null;

  const [wholePart, fracPartRaw = ""] = s.split(".");
  const whole = BigInt(wholePart === "" ? "0" : wholePart);
  const fracPart = fracPartRaw.padEnd(6, "0").slice(0, 6);
  const frac = BigInt(fracPart === "" ? "0" : fracPart);
  const units = whole * 1_000_000n + frac;

  if (units <= 0n) return null;
  return Number(units);
};

// Usage: "/tx 2.5" -> 2500000
const amount = parseUsdcToBaseUnits("2.5"); // 2500000
```

**WalletSendCalls structure:**

```typescript
const walletSendCalls: WalletSendCallsParams = {
  version: "1.0",
  from: "0x123...abc",
  chainId: "0x14a34", // Base Sepolia in hex
  calls: [
    {
      to: "0x456...xyz",
      data: "0x...", // ERC20 transfer call data
      metadata: {
        description: "Transfer 10 USDC on Base Sepolia",
        transactionType: "transfer",
        currency: "USDC",
        amount: 10,
        decimals: 6,
        networkId: "base-sepolia",
      },
    },
  ],
};
```
