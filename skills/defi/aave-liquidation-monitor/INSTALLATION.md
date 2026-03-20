# Aave Liquidation Monitor – Installation & Quick Start

## What You're Getting

A fully-featured, production-ready skill for monitoring your Aave V3 positions with automated alerts when liquidation risk approaches.

### Skill Structure

```
aave-liquidation-monitor/
├── SKILL.md                          ← Main skill definition & commands
├── scripts/
│   └── monitor.js                    ← Core monitoring logic (GraphQL queries, alerts)
├── references/
│   ├── config-guide.md               ← Detailed config options & recommendations
│   ├── aave-api.md                   ← Aave V3 GraphQL API reference
│   └── cron-integration.md           ← How automated scheduling works
└── assets/
    └── config-template.json          ← Sample config file
```

## Installation Steps

### Step 0: Verify Prerequisites

Before using this skill, you must have:

1. ✅ **OpenClaw installed and running** (v1.0+)
2. ✅ **A messaging channel configured** (Telegram, Discord, or Slack)
   - The skill sends alerts through OpenClaw's existing channel integrations
   - No API tokens are stored in the skill itself
3. ✅ **Your Ethereum wallet address** (the one with Aave positions)

**No private keys or credentials go in this skill.** All credentials are managed by OpenClaw.

### Step 1: Install the Skill

Option A: Via ClawhHub CLI (recommended):
```bash
clawhub install aave-liquidation-monitor
```

Option B: Copy to workspace:
```bash
cp -r /home/goliso/clawd/skills/aave-liquidation-monitor \
  ~/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/
```

### Step 2: Verify Installation

```bash
# Check that OpenClaw can discover the skill
openclaw skills list | grep aave

# Should output:
# aave-liquidation-monitor - Proactive monitoring of Aave V3...
```

### Step 3: Initialize Configuration

Run this command in OpenClaw (via Telegram, Discord, or CLI):

```bash
/aave-config init
```

You'll be prompted for:
1. **Ethereum wallet address** (the one with Aave positions)
2. **Health factor thresholds** (defaults: critical 1.05, warning 1.2)
3. **Check interval** (default: 6 hours)
4. **Notification verbosity** (default: quiet = alerts only)
5. **Notification channel** (default: telegram)

Example input:
```
→ Wallet: 0x1234567890abcdef1234567890abcdef12345678
→ Thresholds: critical=1.05 warning=1.2
→ Interval: 6
→ Verbosity: quiet
→ Channel: telegram
✅ Config saved!
```

### Step 4: Test the Monitor

Run a manual check to ensure everything works:

```bash
/aave-monitor check
```

Expected output:
```
Health Factor: 2.31 (Stable ✓)
Total Collateral: $50,342.12
Total Debt: $21,804.00
Debt Ratio: 43.3%

Borrowed Assets:
  USDC: 15,000
  WETH: 0.5
  USDT: 6,804

Supplied Assets:
  WETH: 10
  USDC: 20,000
  DAI: 30,000
```

If you get an error:
- **"Invalid wallet address"** → Check format: must be `0x` + 40 hex chars
- **"No user account found"** → Wallet has no Aave position, or wrong chain selected
- **"API error"** → Aave API might be temporarily down; try again in a minute

### Step 5: Enable Automatic Monitoring

```bash
/aave-monitor enable
```

The skill now runs checks every 6 hours (or your configured interval). Alerts are sent automatically to your channel when health factor drops below threshold.

Status: ✅ Monitoring active!

---

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `/aave-monitor check` | Run a manual check right now |
| `/aave-monitor enable` | Start automatic monitoring |
| `/aave-monitor disable` | Pause automatic monitoring |
| `/aave-monitor status` | See current config & last check result |
| `/aave-monitor history` | View last 5 checks |
| `/aave-monitor logs` | View check execution logs |
| `/aave-config init` | Initial setup wizard |
| `/aave-config view` | View current config |
| `/aave-config set <param> <value>` | Update a setting |
| `/aave-config reset` | Wipe config and start fresh |

---

## Configuration Examples

### Example 1: High-Leverage Trading (Frequent Monitoring)

You're actively borrowing on Aave and want early warnings.

```bash
/aave-config set checkInterval 3        # Check every 3 hours
/aave-config set thresholds critical=1.1 warning=1.15
/aave-config set verbosity verbose      # Daily summaries too
/aave-monitor disable
/aave-monitor enable
```

Result: Alerts every 3 hours if HF < 1.15; daily position summary if HF > 1.5.

### Example 2: Long-Term Lender (Minimal Alerts)

You supplied collateral but rarely borrow. Just want danger alerts.

```bash
/aave-config set checkInterval 12       # Check every 12 hours
/aave-config set thresholds critical=1.05 warning=1.3
/aave-config set verbosity quiet        # Alerts only
/aave-monitor disable
/aave-monitor enable
```

Result: Silent monitoring 2x daily; alerts only if HF drops below 1.3.

### Example 3: Monitor Multiple Chains

Monitor the same wallet address on both Ethereum and Polygon:

```bash
# Check which chains you're using
/aave-monitor check --chain ethereum
/aave-monitor check --chain polygon

# Create separate monitoring jobs (future feature)
# For now, manually check each chain:
/aave-monitor check --chain polygon
```

---

## Alert Examples

You'll receive messages like these when your health factor is at risk:

### 🚨 Critical Alert (HF < 1.05)

```
🚨 AAVE LIQUIDATION RISK – CRITICAL
Chain: Ethereum
Health Factor: 1.02 (Liquidation at ≤1.0!)
⏰ ACTION REQUIRED IMMEDIATELY

Position Summary:
Total Collateral: $50,000
Total Debt: $48,000
Debt Ratio: 96%

Borrowed Assets:
  USDC: 40,000
  WETH: 8 ETH

Actions:
1. Repay debt (especially WETH)
2. Supply more collateral
3. Enable eMode (higher LTV for correlated assets)

Checked: 2026-02-11 08:15 UTC
```

### ⚠️ Warning Alert (HF 1.05–1.2)

```
⚠️ AAVE WARNING
Health Factor: 1.15
Position approaching liquidation zone.

Suggested Actions:
- Repay $2,000 USDC, OR
- Supply $5,000+ collateral (WETH, stETH, etc.)

Check back: 2026-02-11 14:00 UTC
```

### ✅ Healthy Position (HF > 1.5, verbose mode only)

```
✅ AAVE POSITION HEALTHY
Health Factor: 2.31
Total Collateral: $50,342
Total Debt: $21,804
Debt Ratio: 43%

Position is stable. ✨ All clear.
Next check: tomorrow at same time.
```

---

## Troubleshooting

### Problem: "Config not found - run `/aave-config init` first"

**Solution:**
```bash
/aave-config init
```

Then answer the setup prompts.

### Problem: "API Error – retrying"

**Cause:** Aave API temporarily unreachable.

**Solution:** Automated retries happen. If it persists:
1. Check https://status.aave.com
2. Run `/aave-monitor check` to test manually
3. Monitoring will resume on next interval

### Problem: Alerts go to wrong channel

**Cause:** Channel config doesn't match active channels.

**Solution:**
```bash
/aave-config view channels    # List available channels
/aave-config set channel discord
/aave-monitor disable
/aave-monitor enable          # Recreate job
```

### Problem: I want to monitor a different wallet

**Solution:**
```bash
/aave-config set walletAddress 0xnewaddress...
/aave-monitor disable
/aave-monitor enable          # Restart with new address
```

### Problem: Alerts are too frequent (or not frequent enough)

**Solution:** Adjust interval:
```bash
/aave-config set checkInterval 4  # Change to 4 hours
/aave-monitor disable
/aave-monitor enable
```

---

## Documentation Roadmap

- **SKILL.md** ← Start here for commands and quick start
- **config-guide.md** ← Details on each config option
- **aave-api.md** ← Deep dive into Aave GraphQL API (for advanced users)
- **cron-integration.md** ← How background scheduling works

---

## Security & Privacy

✅ **No private keys stored or requested**
- Read-only monitoring via public Aave GraphQL API
- No signing or transactions

✅ **Wallet address stored locally**
- Encrypted in OpenClaw local config
- Never sent to external services (except Aave public API)

✅ **Zero external dependencies**
- Only calls Aave's public GraphQL endpoint
- No third-party APIs or data brokers

---

## Support & Feedback

### Found a bug?
Check the logs: `/aave-monitor logs 20`

### Want a feature?
Ideas: multiple wallets, eMode detection, lending rate tracking, etc.

### Need help?
1. Check `SKILL.md` for command reference
2. Check `config-guide.md` for config questions
3. Check `aave-api.md` for API questions

---

## Next Steps

1. ✅ Run `/aave-config init` to set up
2. ✅ Run `/aave-monitor check` to test
3. ✅ Run `/aave-monitor enable` to start monitoring
4. ✅ Customize interval/thresholds as needed

**That's it!** Your Aave position is now monitored 24/7. You'll only be notified when health factor drops below your warning threshold.

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-11  
**Status:** ✅ Production Ready
