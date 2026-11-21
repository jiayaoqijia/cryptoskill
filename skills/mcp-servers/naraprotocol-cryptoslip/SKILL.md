---
name: cryptoslip-pocket-slip
description: Non-custodial Base Mainnet (8453) PocketSlip wallet and settlement MCP skill for AI agents. Provision an agent with a $5 USDC, ETH, cbBTC, or NARA CryptoSLIP URL instead of a master wallet private key; auto-rotates on boot (<1s Keep at 0% fee), enforces an out-of-context BoundedAgentPolicy spend firewall, pays HTTP 402 APIs and merchants, sends 1-tap Telegram/X/SMS human bounties, executes 1-tx Multicall3 batch payouts, verifies cryptographic payment receipts, reclaims unclaimed slips, and collects 0.25% lifetime referral rewards.
license: MIT
compatibility: Node.js >= 22. Run pinned version `npx @cryptoslip/mcp@1.0.2` with `CRYPTOSLIP_URL="<YOUR_SLIP_URL>"`.
metadata:
  author: nara-protocol
  version: "1.0.2"
  chain: base-mainnet-8453
  mcp-package: "@cryptoslip/mcp@1.0.2"
  sdk-package: "@cryptoslip/sdk@1.0.0"
  openclaw:
    requires:
      bins:
        - node
      env:
        - CRYPTOSLIP_URL
      optionalEnv:
        - CRYPTOSLIP_MAX_PER_CALL_USD
        - CRYPTOSLIP_MAX_DAILY_USD
        - CRYPTOSLIP_MAX_SPENDS_PER_MIN
        - CRYPTOSLIP_ALLOWED_RECIPIENTS
        - CRYPTOSLIP_ALLOWED_DOMAINS
        - CRYPTOSLIP_RPC_URL
        - CRYPTOSLIP_STATE_PATH
  registry-targets:
    - openclaw-skills
    - clawhub
    - rentahuman-mcp
    - claude-code
allowed-tools:
  - mcp__cryptoslip__cryptoslip_status
  - mcp__cryptoslip__cryptoslip_pay_human
  - mcp__cryptoslip__cryptoslip_batch_payout
  - mcp__cryptoslip__cryptoslip_pay_x402_or_merchant
  - mcp__cryptoslip__cryptoslip_verify_or_export_receipt
  - mcp__cryptoslip__cryptoslip_reclaim_unclaimed
  - mcp__cryptoslip__cryptoslip_withdraw_referrals
---

# CryptoSLIP PocketSlip Skill (`@cryptoslip/mcp`)

Give any autonomous agent bounded pocket funds on **Base Mainnet (`8453`)** using a single CryptoSLIP `#` URL â€” **zero master wallet private key required**.

## Why PocketSlip Exists

1. **Zero Master Key Exposure (`V-01` Boot Auto-Keep):** Provision the MCP server with `CRYPTOSLIP_URL="<YOUR_SLIP_URL>"` (for example, a `$5.00 USDC` slip). On startup (`bootAndRotate()`), if the slip is unrotated (`nonces == 0`), `PocketSlipVault` immediately executes an on-chain `Keep` (`0%` protocol fee), rotating `claimSigner` to a fresh local key stored with `0600` file permissions. The original `.env` link becomes invalid on-chain in under a second, capping worst-case prompt-injection exposure strictly to that single slip.
2. **Deterministic Out-of-Context Firewall (`V-02` `BoundedAgentPolicy`):** Every signature passes through `BoundedAgentPolicy` inside the Node.js signer boundary before signing:
   - Per-call spend cap (`maxPerCallUsdMicro`, default `$0.50` in micro-API mode)
   - Sliding-window rate limits (`maxSpendsPerMinute`, `maxDailyUsdMicro`)
   - Protocol & token contract destination denylist (`assertSafeDestination` â€” blocks zero/burn addresses, token contracts, vaults, routers, and public test keys)
   - Optional recipient & domain allowlists (`allowedRecipients`, `allowedDomains`)
   - Recursive output secret scrubber (`redactSecretsFromToolOutput`) so raw claim secrets never enter LLM telemetry logs
   - Canonical Uniswap V4 `NARALiquidityHookV5` (`0x07d8F2Dfd121B10dE3176DeAb6A8C0eaa2646aCC`) enforcement for all `NARA` swaps
3. **Serialized Spend Queue & Sub-Minimum Guard (`V-03`):** Concurrent spends serialize through per-slip `SlipMutex` with pre-flight `$0.10 USDC` (`100 sats` cbBTC / `0.000001` ETH or NARA) remainder checks on `CryptoSlipVaultV32` (`v33`: `0x3f80aa68Fb4834d6E119EE1cf932C14419Cf63EB`).
4. **Self-Funded USDC Network Fees (`V-04`):** Headless agent calls default to Circle `TokenPaymasterV08` (`0x0578cFB241215b77442a541325d6A4E6dFE700Ec`) + `Simple7702Account` (`0xe6Cae83BdE06E4c305530e199D7217f42808555B`) so bots never consume human mobile relay quotas.

---

## Quick Setup (Claude Code / OpenClaw / Cursor)

Create a `$5.00 USDC` slip at `https://slip.naraprotocol.io` (or `https://cryptoslip.eth.limo`) and pass it to the MCP server environment:

```json
{
  "mcpServers": {
    "cryptoslip": {
      "command": "npx",
      "args": ["@cryptoslip/mcp@1.0.2"],
      "env": {
        "CRYPTOSLIP_URL": "<YOUR_SLIP_URL>",
        "CRYPTOSLIP_MAX_PER_CALL_USD": "0.50",
        "CRYPTOSLIP_MAX_DAILY_USD": "5.00",
        "CRYPTOSLIP_MAX_SPENDS_PER_MIN": "3"
      }
    }
  }
}
```

Or via Claude Code CLI (pinned to the Sigstore-verified `1.0.2` release):

```bash
claude mcp add cryptoslip -e CRYPTOSLIP_URL="<YOUR_SLIP_URL>" -- npx @cryptoslip/mcp@1.0.2
```

---

## Available MCP Tools (7 Tools)

### 1. `cryptoslip_status`
Returns the active `PocketSlipVault` summary: slip ID, vault (`v33` `0x3f80aa68Fb4834d6E119EE1cf932C14419Cf63EB`), asset, available balance, boot-rotation state, and active `BoundedAgentPolicy` limits. Zero secret keys or `#k` fragments are ever returned.

### 2. `cryptoslip_pay_human`
Creates or splits a 1-tap `#startapp=slip_...` payout link (or 12-char `XXXX-XXXX-XXXX` off-grid `scrypt` code) to pay a human contributor over Telegram (`@cryptoslip_bot/SLIP`), X DM, Discord, or SMS:
- Supports `noTakeBack: true` (`9_999_999_999` timestamp) for instant irrevocable delivery, or revocable mode (`noTakeBack: false`) so the agent can reclaim funds via `cryptoslip_reclaim_unclaimed` if the recipient never claims.
- Only emits an outbound `#` link when `allowOutboundSlipLink` policy permits human payouts, and instructs the agent to deliver it strictly via private DM.

### 3. `cryptoslip_batch_payout`
Packs `1..500` partner or bounty payouts (`USDC` / `cbBTC` via offline EIP-3009 `ReceiveWithAuthorization` + `MintPermit`) into **1 `Multicall3` transaction** on Base (`8453`) with Base Builder Code `bc_ea68lz8s`, returning structured JSON or CSV `#` links while preserving `creator = partnerWallet` for `0.25%` lifetime referral attribution.

### 4. `cryptoslip_pay_x402_or_merchant`
Pays an HTTP `402` API endpoint, `withCryptoSlip()` tollbooth, or merchant wallet (`0x...` or `#startapp=pos_<address>`) from the active PocketSlip via `splitAndPay`:
- Enforces `BoundedAgentPolicy` spend cap, sliding-window rate limit, and `assertSafeDestination`.
- Retains remaining change inside a rotated `1:1` shielded child slip so the agent's balance stays private.

### 5. `cryptoslip_verify_or_export_receipt`
Verifies an inbound `PaymentReceiptBundleV1` on Base Mainnet in a single RPC check (`verifyPaymentReceiptOnChain`), or exports a signed receipt bundle (`JSON`, `CSV`, or self-contained printable HTML) proving exact settlement.

### 6. `cryptoslip_reclaim_unclaimed`
Executes a `0%`-fee `refundSlipDirect` on Base to recover funds from an unclaimed revocable DM slip (`cancelLockedUntil == 0` and `nonces == 0`).

### 7. `cryptoslip_withdraw_referrals`
Reads and withdraws accumulated `0.25%` (`50/50` protocol fee share) lifetime `referralCredits` earned in `USDC`, `cbBTC`, `ETH`, or `NARA` on `CryptoSlipVaultV32`.

---

## Agent Operating Rules

1. **Never paste raw `#k` URLs into public timelines.** When `cryptoslip_pay_human` generates an open `#` link, send it only inside a direct message to the intended recipient, or use `mode: "code"` (`12-char scrypt` code) for two-step verification.
2. **Respect `BoundedAgentPolicy` refusals.** If a tool call throws a policy cap, rate-limit, or blocked-destination error, halt and ask the human operator rather than retrying in a loop.
3. **Verify inbound payments on-chain.** Before fulfilling a paid request for another agent or user, call `cryptoslip_verify_or_export_receipt` to confirm Base Mainnet settlement finality.
