---
name: swap-approve
description: This skill should be used when the user asks to "approve token", "check allowance", "approve USDC for swapping", "token approval", "revoke approval", "set allowance", "remove approval", "check token approval", "approve router", or wants to manage ERC-20 token approvals for the KyberSwap router. Supports checking allowance, approving exact amounts, unlimited approvals, and revoking approvals.
metadata:
  tags:
    - defi
    - kyberswap
    - approval
    - allowance
    - erc20
    - evm
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Approve Skill

Manage ERC-20 token approvals for the KyberSwap router. Check current allowance, approve exact amounts, approve unlimited, or revoke approvals using Foundry's `cast`.

## Prerequisites

- **Foundry installed**: `cast` must be available in PATH
- **Wallet configured**: One of the methods below (only needed for setting/revoking approvals, not for checking allowance)
- **Native token for gas**: Approval transactions cost gas (~46k gas for standard ERC-20)

### Wallet Setup (One-Time)

> ### ⚠️ USE YOUR EXISTING WALLET MANAGEMENT FIRST ⚠️
>
> **If you or your agent already have wallet management** (key management service, vault, HSM, custodial API, MPC signer, or any secure signing infrastructure), **use that.** Skip the examples below entirely.
>
> The wallet options below are **example setups for development and testing only.** They have known security issues: plaintext password files on disk, private keys in shell environments, no access control, no audit trail, no key rotation. **Do not use them with real funds in production.**

**Option A: Encrypted Keystore (Recommended)**
```bash
cast wallet import mykey --interactive
# Enter private key, then set encryption password

# Create password file securely (prompts without echoing to terminal)
printf "Password: " && read -s pw && printf '\n' && echo "$pw" > ~/.foundry/.password && chmod 600 ~/.foundry/.password
```

**Option B: Environment Variable**
Set the key in your current shell session only (do not persist to shell profiles):
```bash
printf "Enter private key: " && read -s PRIVATE_KEY && printf '\n' && export PRIVATE_KEY
```

**Option C: Ledger Hardware Wallet**
- Connect Ledger, open Ethereum app
- No setup needed, will prompt for physical confirmation

See `${CLAUDE_PLUGIN_ROOT}/skills/swap-execute/references/wallet-setup.md` for detailed instructions.

**NEVER echo, print, log, or display any private key value, even in error messages or debug output.**

## Input Parsing

The user will provide input like:
- `check USDC allowance on ethereum for 0xAbc123...`
- `approve 100 USDC on arbitrum from 0xAbc123...`
- `approve unlimited LINK on base from 0xAbc123...`
- `revoke USDT approval on ethereum from 0xAbc123...`

Extract these fields:
- **token** — the token symbol (e.g., USDC, LINK)
- **chain** — the chain slug (default: `ethereum`)
- **sender** — the wallet address (**required**)
- **amount** — the amount to approve (optional):
  - Omitted or "check" = check current allowance only
  - A number (e.g., `100`, `0.5`) = approve that exact amount
  - `"unlimited"` or `"max"` = approve type(uint256).max
  - `"0"` or `"revoke"` = revoke approval (set allowance to 0)

**If the sender address is not provided, ask the user for it before proceeding.** Do not guess or use a placeholder address.

**Sender address validation — reject or warn before proceeding:**
- **Must not be the zero address** (`0x0000000000000000000000000000000000000000`) — invalid sender.
- **Must not be the native token sentinel** (`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`) — this is a placeholder, not a real account.
- **Must match format** `^0x[a-fA-F0-9]{40}$` — reject malformed addresses.

## Router Address

The KyberSwap router address is the same on all supported chains:

```
0x6131B5fae19EA4f9D964eAc0408E4408b66337b5
```

## Workflow

### Step 1: Validate Input

1. Verify the sender address is provided and valid.
2. **Reject native tokens** — if the user asks to approve ETH, BNB, MATIC/POL, AVAX, MNT, S, BERA, RON, XTZ, or MON, explain:

> Native tokens (ETH, BNB, MATIC, etc.) do not use the ERC-20 approval mechanism. They are sent directly as `msg.value` in the transaction. No approval is needed to swap native tokens through the KyberSwap router.

If the user intended the wrapped version (WETH, WBNB, WMATIC, etc.), suggest they specify the wrapped token symbol instead.

### Step 2: Resolve Token Address

Read the token registry at `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`.

Look up the token for the specified chain. Match case-insensitively. Note the **decimals** for the token.

**If the token is not found in the registry:**
Use the fallback sequence described at the bottom of `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`:
1. **KyberSwap Token API** (preferred) — search whitelisted tokens first: `https://token-api.kyberswap.com/api/v1/public/tokens?chainIds={chainId}&name={symbol}&isWhitelisted=true` via WebFetch. Pick the result whose `symbol` matches exactly with the highest `marketCap`. If no whitelisted match, retry without `isWhitelisted`.
2. **CoinGecko API** (secondary fallback) — search CoinGecko for verified contract addresses.
3. **Ask user manually** (final fallback) — ask the user for the contract address and decimals. Never guess or fabricate addresses.

### Step 3: Check Current Allowance

Determine the RPC URL for the chain:

| Chain | RPC URL |
|-------|---------|
| ethereum | `https://ethereum-rpc.publicnode.com` |
| arbitrum | `https://arb1.arbitrum.io/rpc` |
| polygon | `https://polygon-rpc.com` |
| optimism | `https://mainnet.optimism.io` |
| base | `https://mainnet.base.org` |
| bsc | `https://bsc-dataseed.binance.org` |
| avalanche | `https://api.avax.network/ext/bc/C/rpc` |
| linea | `https://rpc.linea.build` |
| mantle | `https://rpc.mantle.xyz` |
| sonic | `https://rpc.soniclabs.com` |
| berachain | `https://rpc.berachain.com` |
| ronin | `https://api.roninchain.com/rpc` |
| unichain | `https://rpc.unichain.org` |
| hyperevm | `https://rpc.hyperliquid.xyz/evm` |
| plasma | `https://plasma.drpc.org` |
| etherlink | `https://node.mainnet.etherlink.com` |
| monad | `https://rpc.monad.xyz` |
| megaeth | `https://rpc.megaeth.com` |

Or the user can specify a custom RPC with `--rpc-url`.

Run the allowance check:

```bash
cast call \
  --rpc-url {RPC_URL} \
  {tokenAddress} \
  "allowance(address,address)(uint256)" \
  {sender} \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5
```

Convert the result from wei to human-readable using the token's decimals:
```
humanAllowance = allowanceWei / 10^(token decimals)
```

Display the current allowance:

```
## Current Allowance

| Detail | Value |
|--------|-------|
| Token | {symbol} (`{tokenAddress}`) |
| Chain | {chain} |
| Owner | `{sender}` |
| Spender (Router) | `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` |
| Current allowance | {humanAllowance} {symbol} |
```

If the allowance equals `115792089237316195423570985008687907853269984665640564039457584007913129639935` (type(uint256).max), display it as **"Unlimited"** instead of the raw number.

### Step 4: Determine Action

- **Check only** (no amount specified): Display allowance from Step 3 and stop.
- **Approval needed** (amount specified): Compare current allowance to requested amount.
  - If current allowance >= requested amount: Inform the user the approval is already sufficient. Ask if they still want to set a new approval.
  - If current allowance < requested amount: Proceed to Step 5.
- **Revoke** (amount = 0): Proceed to Step 5 regardless of current allowance (unless already 0).
- **Unlimited**: Proceed to Step 5 (unless already unlimited).

### Step 5: Confirm Approval

**CRITICAL: Always confirm before executing. Approval transactions are on-chain and cost gas.**

Present the approval details:

```
## Token Approval -- Confirmation Required

| Detail | Value |
|--------|-------|
| Token | {symbol} ({tokenAddress}) |
| Chain | {chain} |
| Spender (Router) | 0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 |
| Current allowance | {currentAllowance} {symbol} |
| New allowance | {requestedAmount} {symbol} |
| Sender | {sender} |

{WARNING}

Do you want to proceed? (yes/no)
```

**Warnings by type:**

- **Exact amount**: "This approves the router to spend exactly {amount} {symbol} from your wallet."
- **Unlimited**: "SECURITY WARNING: Unlimited approvals allow the router to spend ALL your {symbol} tokens. If the router contract is ever compromised, an attacker could drain your entire {symbol} balance. Only use with wallets holding limited funds. For large holdings, prefer exact-amount approvals."
- **Revoke (amount=0)**: "This removes the router's permission to spend your {symbol}. Existing pending swaps using this token will fail."

Wait for explicit "yes" confirmation before proceeding.

### Step 6: Execute Approval

After user confirms, ask for wallet method (if not already specified):

```
How do you want to sign this transaction?

1. Keystore (encrypted key at ~/.foundry/keystores/)
2. Environment variable ($PRIVATE_KEY)
3. Ledger hardware wallet
4. Trezor hardware wallet
```

**Wallet flags summary:**

| Method | Flags |
|--------|-------|
| Keystore | `--account NAME --password-file ~/.foundry/.password` |
| Env var | `--private-key $PRIVATE_KEY` |
| Ledger | `--ledger` |
| Trezor | `--trezor` |

Determine the approval amount in wei:

| User request | amountInWei |
|--------------|-------------|
| Exact amount (e.g., `100`) | `amount * 10^(token decimals)` — plain integer, no decimals, no scientific notation |
| Unlimited / max | `115792089237316195423570985008687907853269984665640564039457584007913129639935` |
| Revoke / 0 | `0` |

Build and execute the `cast send` command:

**Option 1: Keystore + Password File (Recommended)**
```bash
cast send \
  --rpc-url {RPC_URL} \
  --account {keystore_name} \
  --password-file ~/.foundry/.password \
  {tokenAddress} \
  "approve(address,uint256)" \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  {amountInWei}
```

**Option 2: Environment Variable**
```bash
cast send \
  --rpc-url {RPC_URL} \
  --private-key $PRIVATE_KEY \
  {tokenAddress} \
  "approve(address,uint256)" \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  {amountInWei}
```

**Option 3: Ledger**
```bash
cast send \
  --rpc-url {RPC_URL} \
  --ledger \
  {tokenAddress} \
  "approve(address,uint256)" \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  {amountInWei}
```

**Option 4: Trezor**
```bash
cast send \
  --rpc-url {RPC_URL} \
  --trezor \
  {tokenAddress} \
  "approve(address,uint256)" \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  {amountInWei}
```

### Step 7: Verify Approval

After the approval transaction confirms, re-check the allowance to verify it was set correctly:

```bash
cast call \
  --rpc-url {RPC_URL} \
  {tokenAddress} \
  "allowance(address,address)(uint256)" \
  {sender} \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5
```

Present the result:

**On success:**

```
## Approval Confirmed

| Field | Value |
|-------|-------|
| Transaction Hash | `{txHash}` |
| Block Number | {blockNumber} |
| Gas Used | {gasUsed} |
| New allowance | {verifiedAllowance} {symbol} |

**Explorer Link:** {explorerUrl}/tx/{txHash}

The KyberSwap router can now spend up to {verifiedAllowance} {symbol} from your wallet.
```

**On failure:**

```
## Approval Failed

**Error:** {error message}

See Common Errors below for troubleshooting.
```

**Explorer URLs by chain:**

| Chain | Explorer |
|-------|----------|
| ethereum | https://etherscan.io |
| arbitrum | https://arbiscan.io |
| polygon | https://polygonscan.com |
| optimism | https://optimistic.etherscan.io |
| base | https://basescan.org |
| bsc | https://bscscan.com |
| avalanche | https://snowtrace.io |
| linea | https://lineascan.build |
| mantle | https://mantlescan.xyz |
| sonic | https://sonicscan.io |
| berachain | https://berascan.com |
| ronin | https://app.roninchain.com |
| unichain | https://uniscan.xyz |
| hyperevm | https://explorer.hyperliquid.xyz |
| plasma | https://plasmascan.io |
| etherlink | https://explorer.etherlink.com |
| monad | https://explorer.monad.xyz |
| megaeth | https://explorer.megaeth.com |

## ethers.js Alternative

For agents or environments without Foundry, use ethers.js:

```javascript
const { ethers } = require("ethers");

const RPC_URL = "https://ethereum-rpc.publicnode.com";
const ROUTER = "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5";

const provider = new ethers.JsonRpcProvider(RPC_URL);
const signer = new ethers.Wallet(privateKey, provider);
const token = new ethers.Contract(tokenAddress, [
  "function allowance(address,address) view returns (uint256)",
  "function approve(address,uint256) returns (bool)",
  "function decimals() view returns (uint8)"
], signer);

// Check allowance
const allowance = await token.allowance(sender, ROUTER);
console.log("Current allowance:", ethers.formatUnits(allowance, decimals));

// Approve exact amount
const amountWei = ethers.parseUnits(amount, decimals);
const tx = await token.approve(ROUTER, amountWei);
await tx.wait();

// Approve unlimited
const unlimited = ethers.MaxUint256;
const tx2 = await token.approve(ROUTER, unlimited);
await tx2.wait();

// Revoke
const tx3 = await token.approve(ROUTER, 0n);
await tx3.wait();
```

## Important Notes

- **Native tokens do not need approval** — ETH, BNB, MATIC, AVAX, etc. are sent directly as transaction value.
- **Approvals are per-token-per-spender** — approving USDC for the router does not approve USDT. Each token requires its own approval.
- **Approval transactions cost gas** — approximately 46k gas for a standard ERC-20 approve call.
- **USDT on Ethereum mainnet** requires setting allowance to 0 before changing to a new non-zero value. If an approval fails, suggest: "Try revoking first (set allowance to 0), then approve the desired amount."
- **Never expose private keys** in command output or logs.
- **Verify router address** matches expected: `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5`

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Transaction reverted | USDT-style token requires zero-first approval | Revoke (approve 0) first, then re-approve the desired amount |
| Insufficient gas | Not enough native token for gas fees | Top up ETH/BNB/MATIC/etc. in the sender wallet |
| Invalid token | Token address is wrong for the specified chain | Verify the address on the chain's block explorer |
| Cast not found | Foundry is not installed | Install: `curl -L https://foundry.paradigm.xyz | bash && foundryup` |
| RPC timeout | Public RPC is congested or down | Try a different RPC endpoint or set `--rpc-url` manually |

## Additional Resources

### Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/references/api-reference.md`** — Full API specification, error codes, rate limiting
- **`${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`** — Token addresses and decimals by chain

## Troubleshooting

For errors not covered above (API errors, PMM/RFQ failures, full error code catalog), refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
