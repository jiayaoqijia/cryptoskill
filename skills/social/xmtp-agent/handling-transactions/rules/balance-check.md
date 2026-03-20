---
title: Check USDC balance
impact: HIGH
tags: transactions, balance, usdc
---

## Check USDC balance

Use `getUSDCBalance` to check token balances.

**Basic balance check:**

```typescript
import { getUSDCBalance } from "../../utils/transactions";
import { validHex } from "@xmtp/agent-sdk";

const networkId = "base-sepolia"; // or "base-mainnet"

// Get balance (returns formatted string like "10.5")
const balance = await getUSDCBalance(networkId, validHex(address));

await ctx.conversation.sendText(`Your balance: ${balance} USDC`);
```

**In a command handler:**

```typescript
import { CommandRouter } from "@xmtp/agent-sdk/middleware";

const router = new CommandRouter();

router.command("/balance", async (ctx) => {
  const agentAddress = agent.address;
  const senderAddress = await ctx.getSenderAddress();

  const agentBalance = await getUSDCBalance(networkId, validHex(agentAddress));
  const senderBalance = await getUSDCBalance(networkId, validHex(senderAddress));

  await ctx.conversation.sendText(
    `Agent balance: ${agentBalance} USDC\n` +
    `Your balance: ${senderBalance} USDC`
  );
});
```

**Generic token balance:**

```typescript
import { getTokenBalance, TokenConfig } from "../../utils/transactions";

const customToken: TokenConfig = {
  tokenAddress: "0x...",
  decimals: 18,
  symbol: "TOKEN",
};

const balance = await getTokenBalance(networkId, customToken, validHex(address));
```

**Requirements:**

- Smart contract wallet (SCW) required for transaction signing
- EOA wallets may see "Signature validation failed" error
- Get testnet USDC from [Circle Faucet](https://faucet.circle.com) or [Base Faucet](https://portal.cdp.coinbase.com/products/faucet)
