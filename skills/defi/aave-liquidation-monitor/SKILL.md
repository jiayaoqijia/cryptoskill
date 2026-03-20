---
name: aave-liquidation-monitor
description: "Proactive monitoring of Aave V3 borrow positions with liquidation alerts. Queries user collateral, debt, and health factor across chains (Ethereum, Polygon, Arbitrum, etc.). Sends urgent alerts to Telegram/Discord/Slack when health factor drops below configurable thresholds (critical at 1.05, warning at 1.2). Use when you need continuous monitoring of Aave positions, want alerts before liquidation risk occurs, or need periodic summaries of your borrowing health."
---

# Aave Liquidation Monitor

## Quick Start

Configure your wallet and thresholds once, then the skill runs automatically every 6 hours (configurable).

### Step 1: Initialize Your Config

Run `/aave-config init` to set up:
- Your Ethereum wallet address (read-only; no private keys required)
- Health factor thresholds (default: critical 1.05, warning 1.2, stable >1.5)
- Check interval in hours (default: 6)
- Notification verbosity (verbose = daily summaries even if stable; quiet = only alerts)
- Preferred notification channel (Telegram default, or specify Discord/Slack)

Example:
```
/aave-config init
→ Wallet: 0x1234...5678
→ Thresholds: 1.05 (critical), 1.2 (warning)
→ Interval: 6 hours
→ Verbosity: quiet (alerts only)
→ Channel: telegram
```

### Step 2: Test the Monitor

Run `/aave-monitor check` to fetch your position immediately and see the alert format:

```
/aave-monitor check
→ Fetching position for 0x1234...5678 on Ethereum...
→ Health Factor: 2.31 (Stable ✓)
→ Total Collateral: $50,342.12
→ Total Debt: $21,804.00
→ Borrowed Assets: USDC (15,000), WETH (0.5), USDT (6,804)
→ Supplied Assets: WETH (10), USDC (20,000), DAI (30,000)
```

### Step 3: Enable Proactive Monitoring

Run `/aave-monitor enable` to start automatic checks every 6 hours. The skill registers a cron job that silently runs in the background and alerts you only when health factor drops below threshold.

For manual override:
```
/aave-monitor enable --interval 4   # Check every 4 hours
/aave-monitor disable               # Stop monitoring
/aave-monitor status                # See current config + last check result
```

## Configuration Reference

See `references/config-guide.md` for detailed config options, chain support, and threshold guidance.

See `references/aave-api.md` for Aave V3 GraphQL schema and query patterns.

**Security & Credentials:** See `SECURITY.md` for how credentials are handled and threat model.

**For auditors:** See `SECURITY.md` for code review checklist and architecture details.

## How It Works

1. **Query Phase**: Calls Aave V3 GraphQL API with your wallet address
2. **Analysis Phase**: Extracts health factor, collateral, debt, borrowed/supplied assets
3. **Alert Logic**:
   - If HF < 1.05 → **CRITICAL** (red alert, send immediately)
   - If HF < 1.2 → **WARNING** (yellow alert, send immediately)
   - If HF > 1.5 → **STABLE** (no alert, unless verbose mode enables daily summary)
4. **Notification Phase**: Posts alert to your configured channel with clear summary
5. **Retry Logic**: If API fails, retries up to 3 times with exponential backoff

## Error Handling

- **Invalid wallet address** → Logs error, skips check, retries next interval
- **API timeout** → Retries up to 3x with exponential backoff (2s, 4s, 8s)
- **Malformed response** → Alerts you to API changes, logs full response for debugging
- **Network errors** → Silently retries; alerts only if all retries fail

## Security & Credentials

**NO private keys are requested or stored** — this is read-only monitoring only.

### How messaging credentials work

The skill uses **OpenClaw's built-in message routing** — it does NOT store Telegram, Discord, or Slack tokens.

1. You configure your messaging channel in OpenClaw (outside this skill)
2. The skill calls OpenClaw's messaging API with just the alert text
3. OpenClaw routes the message using your configured channels

Example:
```
/aave-config set channel telegram
→ OpenClaw sends alerts via your pre-configured Telegram channel
```

**You must have a messaging channel already set up in OpenClaw.** See OpenClaw docs for setting up Telegram/Discord/Slack integrations.

### Data handling

- **Wallet address:** Stored in OpenClaw's encrypted config (never sent to external services except Aave's public API)
- **API responses:** Parsed for health factor only; sensitive position data is NOT logged
- **Credentials:** Managed by OpenClaw, never stored in skill files

### What the skill accesses

✅ **Aave GraphQL API (public)** — reads your position data  
✅ **OpenClaw message routing** — sends formatted alerts to your configured channel  
✅ **Cron scheduler** — runs background checks on your interval

❌ **Does NOT:**
- Request private keys
- Store API tokens
- Execute transactions
- Modify your positions

## Examples

### Alert Examples

**Critical Alert (HF < 1.05):**
```
🚨 AAVE LIQUIDATION RISK – CRITICAL
Health Factor: 1.02 (Liquidation threshold: 1.0)
⏰ Action required immediately!

📊 Position Summary:
Total Collateral: $50,000
Total Debt: $48,000
Debt Ratio: 96%

Borrowed (at risk):
- USDC: 40,000
- WETH: 8 ETH (~$31k)

Suggested Actions:
1. Repay debt (especially WETH)
2. Supply more collateral
3. Enable eMode if available (higher LTV on correlated assets)

Last checked: 2026-02-11 08:15 UTC
```

**Warning Alert (HF < 1.2):**
```
⚠️ AAVE WARNING
Health Factor: 1.15 (Approaching 1.2 threshold)

Position approaching liquidation. Consider:
- Repaying $2,000 USDC or
- Adding $5,000 collateral (WETH or stETH)
```

**Stable Position (HF > 1.5, verbose mode only):**
```
✅ AAVE POSITION HEALTHY
Health Factor: 2.31
Total Collateral: $50,342.12
Total Debt: $21,804.00

All clear. Check again tomorrow.
```

### Command Examples

```bash
# One-time position check
/aave-monitor check

# Start automatic monitoring
/aave-monitor enable

# Change thresholds (e.g., earlier warning at HF 1.3)
/aave-config set thresholds 1.05 1.3

# Check monitoring status
/aave-monitor status

# View last 5 check results with alerts
/aave-monitor history 5

# Disable monitoring temporarily
/aave-monitor disable
```

## Chains Supported

Primary: Ethereum mainnet

Also works (with same config address where applicable):
- Polygon
- Arbitrum
- Optimism
- Base
- Avalanche
- Gnosis

Edit `scripts/monitor.js` to add chains or customize per-chain endpoints.

## Customization

**Change check interval:**
```
/aave-config set interval 4  # Check every 4 hours
```

**Change alert thresholds:**
```
/aave-config set thresholds 1.1 1.25  # Critical at 1.1, warning at 1.25
```

**Enable verbose mode (daily summaries even if stable):**
```
/aave-config set verbosity verbose
```

**Switch notification channel:**
```
/aave-config set channel discord
```

## Implementation Details

See `scripts/monitor.js` for the core monitoring logic (GraphQL queries, health factor calculation, alert formatting).

See `scripts/cron-runner.js` for cron job integration with OpenClaw's cron scheduler.

## Troubleshooting

**"Invalid wallet address"**
→ Check format: must be 0x... format. Try `/aave-config view` to see current config.

**"Health factor not returned by API"**
→ Wallet may not have Aave position. Try `/aave-monitor check` for immediate response.

**"API endpoint unreachable"**
→ Aave API may be down. Skill retries automatically. Check https://status.aave.com.

**"No notifications sent"**
→ Check that your notification channel is active. Run `/aave-monitor check` to test delivery.

## Notes

- Health factor = Total Collateral / Total Debt (net of liquidation threshold ratios)
- Liquidation occurs when HF ≤ 1.0
- Variable debt accrues interest; stable debt is fixed-rate
- eMode allows higher LTV for correlated assets (e.g., stablecoins, ETH-LSTs)
- Supplied assets are collateral; they earn interest but can be seized if you're liquidated

---

**Last Updated:** 2026-02-11 | **Status:** Ready for configuration
