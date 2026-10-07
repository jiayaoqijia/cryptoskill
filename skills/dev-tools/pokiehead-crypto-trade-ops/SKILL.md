---
name: crypto-trade-ops
description: Connect exchange APIs (Bitunix/MEXC), deploy idempotent price-trigger and tiered-exit watchers, and alert before liquidation. Use when automating a manual trading plan.
---

# Crypto Trade Ops

Automate a trading plan the operator has ALREADY decided. Never invent levels.

## 0. Rules
- The human owns every level (entry, tiers, SL). You automate; you do not advise.
- Credentials live in 0600 files OUTSIDE any repo. Never log them, never echo them.
- Run from a residential IP: MEXC/Bitunix hang on datacenter/VPN IPs (verified).

## 1. Connect
1. Ask the operator for API key+secret (trade permission; withdraw OFF).
2. Store as ~/.config/bitunix.secret (see config.example format), chmod 600.
3. Prove the pipe: `python3 bitunix_client.py price` (public), then `account` (signed).

## 2. Watchers (the whole system)
- `entry_trigger.sh` - one-shot entry when price crosses a level. Flag file = no doubles.
- `ladder_watch.sh` - tiered exits via state machine on disk (1->2->3).
- Both: exit 0 always, output only when they act. Cron every 5 min.
- SL alert: separate watcher that messages the human BEFORE the liquidation zone.
- Native SL on autopilot: entry_trigger passes SL_PCT -> presetStopLossPrice on the entry.
  FIRE TEST first: minimal entry with SL, VERIFY the stop in the exchange UI, close.

## 3. Signing cheat-sheet
- Bitunix: host fapi.bitunix.com; sign = sha256(sha256(nonce+ts+key+payload)+secret);
  GET payload is empty; POST payload is the compact JSON body.
- MEXC: HMAC-SHA256 of the urlencoded query; the key goes in a custom header.

## 4. Hardening checklist
- [ ] Withdraw permissions disabled on the API key
- [ ] Flag/state dirs exist and are writable
- [ ] Watcher tested with thresholds already crossed (dry run) before going live
- [ ] Alert channel wired (chat announce) and tested with a fake trigger
