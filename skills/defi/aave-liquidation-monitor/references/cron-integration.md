# Cron Integration Guide

This skill integrates with OpenClaw's cron scheduler to run monitoring checks automatically on a schedule you define.

## How It Works

When you run `/aave-monitor enable`, the skill:

1. **Reads your config** (wallet address, thresholds, interval, etc.)
2. **Creates a cron job** that runs every N hours
3. **Registers with OpenClaw's scheduler** for persistent, background execution
4. **Runs checks silently** in the background
5. **Sends alerts only when needed** (when HF drops below threshold)

## Commands

### Enable Monitoring

```bash
/aave-monitor enable [--interval N] [--chain ethereum]
```

Starts automatic monitoring. Options:
- `--interval N` — Check every N hours (default: from config, usually 6)
- `--chain ethereum` — Monitor specific chain (default: ethereum)

Example:
```bash
/aave-monitor enable --interval 4
```

### Check Status

```bash
/aave-monitor status
```

Shows:
- Current config
- Last check time and result
- Next scheduled check
- Last alert (if any)

Example output:
```
Wallet: 0x1234...5678
Chain: ethereum
Thresholds: Critical 1.05 | Warning 1.2
Interval: 6 hours
Next check: 2026-02-11 14:00 UTC
Last check: 2026-02-11 08:15 UTC (STABLE, HF: 2.31)
```

### Manual Check

```bash
/aave-monitor check
```

Runs a check immediately (doesn't affect the schedule):
```bash
/aave-monitor check --chain polygon
```

Returns:
```
Health Factor: 2.31 (Stable ✓)
Total Collateral: $50,342.12
Total Debt: $21,804.00
...
```

### Disable Monitoring

```bash
/aave-monitor disable
```

Stops the cron job. Can be re-enabled anytime.

### View History

```bash
/aave-monitor history [limit]
```

Shows last N checks (default: 5):

```
2026-02-11 08:15 UTC | STABLE | HF 2.31
2026-02-11 02:15 UTC | STABLE | HF 2.28
2026-02-10 20:15 UTC | STABLE | HF 2.35
```

## Cron Job Lifecycle

### Creation

When you enable monitoring:

```bash
/aave-monitor enable --interval 6
```

This creates a cron job internally with:
```json
{
  "name": "aave-monitor-check",
  "schedule": {
    "kind": "every",
    "everyMs": 21600000  // 6 hours in milliseconds
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Check Aave position: 0x1234...5678 (eth) - if HF<1.2 alert, else silent"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### Execution

The scheduler runs the job at the specified interval. Each execution:

1. Calls the monitor script with your wallet address
2. Fetches latest health factor from Aave API
3. Compares to your thresholds
4. Sends alert (if needed) or remains silent
5. Updates last-check timestamp in config

### Logs

Check job execution logs:

```bash
/aave-monitor logs [limit]
```

Output:
```
2026-02-11 08:15:24 UTC | Health Factor: 2.31 (no alert needed)
2026-02-11 02:15:18 UTC | Health Factor: 2.28 (no alert needed)
2026-02-11 00:15:12 UTC | Health Factor: 1.18 ⚠️ WARNING ALERT SENT
```

### Deletion

When you disable monitoring:

```bash
/aave-monitor disable
```

The cron job is paused but not deleted. Re-enable it anytime with:

```bash
/aave-monitor enable
```

To permanently delete the job:

```bash
/aave-monitor disable --remove
```

## Scheduler Reliability

OpenClaw's cron scheduler:
- ✅ Persists across restarts
- ✅ Automatically retries failed checks
- ✅ Prevents duplicate runs (no overlap)
- ✅ Logs all executions with timestamps
- ✅ Supports concurrent jobs for multiple wallets/chains (future)

## Timezone Notes

All cron times are in **UTC** by default. Your alert timestamps are also in UTC.

Example: If you set `interval: 6`, checks happen at:
- 00:00 UTC
- 06:00 UTC
- 12:00 UTC
- 18:00 UTC

If you need a custom schedule, see "Advanced: Custom Schedules" below.

## Troubleshooting

### Cron Job Not Running

**Symptom:** `/aave-monitor status` shows "No checks scheduled" or old last-check time

**Solution:**
```bash
/aave-monitor disable
/aave-monitor enable
```

This recreates the cron job.

### Alerts Not Being Sent

**Symptom:** Health factor is low, but no alert received

**Causes & Solutions:**
1. Check if monitoring is enabled: `/aave-monitor status`
2. Check your channel config: Does Telegram/Discord/Slack have an active connection?
3. Run manual check: `/aave-monitor check` to verify API works
4. View logs: `/aave-monitor logs 10` to see if check ran

### Duplicate Alerts

**Symptom:** Getting the same alert multiple times

**Solution:** This shouldn't happen, but if it does:
```bash
/aave-monitor disable
/aave-monitor enable  # Recreates job with deduplication
```

### Interval Too Frequent or Too Long

**Change interval:**
```bash
/aave-config set checkInterval 4  # Every 4 hours
/aave-monitor disable
/aave-monitor enable  # Recreate with new interval
```

---

## Advanced: Custom Schedules

For non-standard schedules, you can create a custom cron job directly:

### Example: Check at Specific Times (5am, 1pm, 9pm UTC)

```bash
/cron add \
  --name "aave-monitor-custom" \
  --schedule "cron:0 5,13,21 * * *" \
  --payload agentTurn \
  --message "Run Aave monitor check for 0x1234...5678"
```

### Example: Check Every 4 Hours Starting at 2am UTC

```bash
/cron add \
  --name "aave-monitor-every4" \
  --schedule "every:14400000" \
  --payload agentTurn \
  --message "Run Aave monitor check" \
  --anchorMs 1707555600000  # 2026-02-10 02:00 UTC
```

See `/cron help` for full cron syntax options.

---

## Performance Impact

Each check uses minimal resources:
- **Network:** 1 HTTP request to Aave API (~50 KB)
- **CPU:** <100ms processing per check
- **Memory:** <10 MB temporary
- **Storage:** ~1 KB per check result logged

Running checks every 6 hours:
- **Monthly API calls:** 120
- **Monthly data:** ~6 MB
- **Cost:** Free (Aave API is public, no API key needed)

---

## Integration with Other OpenClaw Features

### Combine with `/cron` for Advanced Scheduling

Create multiple monitoring jobs with different thresholds:

```bash
# Conservative monitoring (daily summary)
/aave-monitor enable --interval 24 --label "Daily Summary"

# Aggressive monitoring (every 2 hours)
/aave-monitor enable --interval 2 --label "Active Trading"
```

### Combine with Message Routing

Alerts are automatically routed to your configured channel (Telegram, Discord, etc.) based on skill config.

### Combine with Session History

All checks are logged to OpenClaw session history:

```bash
/sessions history [limit]
```

Includes alert messages and check results for audit trail.

---

## Best Practices

1. **Start with 6-hour interval**, adjust based on your leverage level
2. **Test with `/aave-monitor check`** before enabling automated monitoring
3. **Monitor logs** the first few days to ensure correct behavior
4. **Adjust thresholds** based on your risk tolerance, not market conditions
5. **Keep wallet address updated** if you use different addresses for different pools

---

## Monitoring Multiple Wallets (Future)

Currently, you can only monitor one wallet per OpenClaw instance. For multiple wallets:

**Option 1:** Spawn a separate sub-agent session for each wallet
```bash
/sessions spawn --agentId main --label "Monitor Wallet 2" \
  --task "Enable Aave monitoring for 0xanotheraddress"
```

**Option 2:** Use multiple OpenClaw instances with separate configs

This will be simplified in a future release with built-in multi-wallet support.

