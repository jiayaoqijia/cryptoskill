# Aave Liquidation Monitor – Configuration Guide

## Initial Setup: `/aave-config init`

Running `/aave-config init` will prompt you through these fields:

### 1. Ethereum Wallet Address

**Field:** `walletAddress`

Your Ethereum wallet address (read-only, no private key needed).

Format: `0x` followed by 40 hex characters

Example: `0x1234567890abcdef1234567890abcdef12345678`

**Where to find it:**
- Metamask: Click account → copy address
- Etherscan: Search your ENS name or address at etherscan.io
- Hardware wallet: Check your wallet's address display

**Security note:** This address is public blockchain data. It's written locally in OpenClaw config but never sent to external services except Aave's public GraphQL API.

### 2. Health Factor Thresholds

**Field:** `thresholds`

Three threshold levels (in order of severity):

- **Critical Threshold** (default: `1.05`)
  - Triggers urgent alert when HF drops below this
  - Liquidation happens at HF ≤ 1.0, so 1.05 gives you ~5% buffer
  - Suggested range: 1.02–1.10

- **Warning Threshold** (default: `1.2`)
  - Triggers warning alert (less urgent) when HF drops below this
  - Should be higher than critical; gives you time to react
  - Suggested range: 1.15–1.5

- **Stable Threshold** (default: `1.5`)
  - Above this, position is considered safe
  - Used only in verbose mode to decide if daily summary is needed
  - Suggested range: 1.3–2.0

Example config:
```json
{
  "thresholds": {
    "critical": 1.05,
    "warning": 1.2,
    "stable": 1.5
  }
}
```

**Why these matter:**
- Aave liquidation happens when HF ≤ 1.0
- Your collateral can be seized instantly at liquidation
- Liquidators earn 5–10% penalty for executing liquidation
- Setting thresholds lower = fewer alerts but less reaction time
- Setting thresholds higher = more alerts but more time to act

### 3. Check Interval (Hours)

**Field:** `checkInterval`

How often the monitor runs automatically (in hours).

Default: `6` (checks every 6 hours)

Options: 1, 2, 3, 4, 6, 8, 12, 24

Example: Setting to `4` means checks run at 00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC daily.

**Guidance:**
- **High leverage (HF 1.1–1.5):** Use 2–4 hours (closer monitoring)
- **Medium leverage (HF 1.5–2.0):** Use 6 hours (standard)
- **Low leverage (HF >2.0):** Use 12–24 hours (rare changes)

### 4. Notification Verbosity

**Field:** `verbosity`

Controls how often you get alerts.

- **`quiet` (default)**
  - Only sends alerts when HF drops below warning threshold
  - No messages if position is stable
  - Recommended for normal positions

- **`verbose`**
  - Sends daily summary even if position is stable (HF > 1.5)
  - Useful if you want to track your position trending
  - Recommended for very high leverage or active borrowing

- **`silent`**
  - No notifications at all (monitoring still runs)
  - Only useful if you check status manually with `/aave-monitor status`

### 5. Notification Channel

**Field:** `channel`

Where alerts are sent.

Options: `telegram` (default), `discord`, `slack`

**Important:** Make sure you have the channel already configured in OpenClaw before setting it here. If channel is not active, alerts will fail.

To check available channels:
```
/aave-config view channels
```

Example:
```json
{
  "channel": "telegram"
}
```

---

## Update Configuration: `/aave-config set`

Change individual settings without re-running init:

```bash
# Change wallet address
/aave-config set walletAddress 0xnewaddress...

# Change thresholds
/aave-config set thresholds critical=1.1 warning=1.25 stable=1.6

# Change check interval
/aave-config set checkInterval 4

# Change verbosity
/aave-config set verbosity verbose

# Change notification channel
/aave-config set channel discord
```

---

## View Configuration: `/aave-config view`

Display all current settings:

```
/aave-config view
→
Wallet Address: 0x1234...5678
Thresholds: Critical 1.05 | Warning 1.2 | Stable 1.5
Check Interval: 6 hours
Verbosity: quiet
Channel: telegram
Last Check: 2026-02-11 08:15 UTC
Last Status: STABLE (HF 2.31)
```

---

## Chain-Specific Configuration (Advanced)

By default, the monitor checks Ethereum mainnet. To monitor other chains or multiple chains:

### Single Chain Other Than Ethereum

Edit the skill config:

```json
{
  "chain": "polygon"
}
```

Supported chains:
- `ethereum` (default)
- `polygon`
- `arbitrum`
- `optimism`
- `base`
- `avalanche`

### Multiple Chains (Future Enhancement)

Currently, the skill monitors one chain at a time. To monitor multiple chains, you'll need separate cron jobs:

```bash
# Create separate jobs for each chain
/aave-monitor enable --chain polygon --interval 6 --label "Aave Monitor (Polygon)"
/aave-monitor enable --chain ethereum --interval 6 --label "Aave Monitor (Ethereum)"
```

---

## Threshold Recommendations by Leverage Level

| Leverage | HF Range | Recommended Thresholds | Check Interval |
|----------|----------|------------------------|-----------------|
| High | 1.05–1.3 | Critical: 1.05, Warning: 1.15 | 2–3 hours |
| Medium | 1.3–2.0 | Critical: 1.05, Warning: 1.2 | 6 hours |
| Low | 2.0+ | Critical: 1.05, Warning: 1.3 | 12 hours |

---

## Common Scenarios

### Scenario: Actively Trading with Borrowed Assets
- Thresholds: Critical 1.05, Warning 1.15
- Interval: 3 hours
- Verbosity: verbose (want daily position updates)
- Reason: Positions change rapidly; early warnings are critical

### Scenario: Long-Term Lender (Set & Forget)
- Thresholds: Critical 1.05, Warning 1.3
- Interval: 12 hours
- Verbosity: quiet (only alert on danger)
- Reason: Minimal changes; don't need frequent updates

### Scenario: Yield Farming on Borrowed Capital
- Thresholds: Critical 1.1, Warning 1.25
- Interval: 4 hours
- Verbosity: verbose (track APY + risk)
- Reason: Higher leverage; need tighter monitoring and position updates

---

## Troubleshooting Config

**Q: I set the wallet address but still see "Invalid wallet address"**

A: Check the format is exactly `0x` + 40 hex chars. No spaces, no mixed case issues.

Example of valid format:
```
0x1234567890abcdef1234567890abcdef12345678
```

**Q: I changed thresholds but alerts still trigger at old values**

A: The cron job uses the old config. Run:
```
/aave-monitor disable
/aave-monitor enable
```

This restarts the monitoring job with new thresholds.

**Q: Alerts go to Telegram but I want Discord**

A: Run:
```
/aave-config set channel discord
/aave-monitor disable
/aave-monitor enable
```

Then verify Discord channel is configured in OpenClaw.

**Q: I want to monitor multiple wallets or chains**

A: Create separate jobs with different labels:
```
/aave-monitor enable --wallet 0xfirstaddress --label "Main Account"
/aave-monitor enable --wallet 0xsecondaddress --label "Trading Account"
```

(Feature coming soon)

---

## Reset Configuration

To start fresh:

```bash
/aave-config reset
/aave-config init
```

This wipes all settings and asks you to re-enter them.

