---
name: radar-live-money-gate
description: >-
  Preflight before DUP Market Radar live spot capital. Fail-closed checklist;
  never enable futures auto. Use when the user asks to go live, dry_run false,
  or enable auto with real money.
license: MIT
compatibility: Requires dup-market-radar checkout, .env with KuCoin Spot keys, radar_native.
metadata:
  author: dup-labs
  version: "0.1.6"
  product: dup-market-radar
---

# Live money gate (spot only)

## When to Use

- «включи live / dry_run false / торгуй на деньги»
- Before changing money-path config

## Hard rules

1. Lab default stays `dry_run: true` in `config/default.yaml`.
2. Use `RADAR_PROFILE=live-money` overlay — not silent default edit.
3. Futures auto forbidden (`FUTURES_BLOCK`).
4. Never print or commit secrets.

## Steps

1. `.\scripts\go_ready.ps1` → `ops_ready=true`
2. Confirm `radar_native` available
3. `.env`: KuCoin Spot KEY/SECRET/PASSPHRASE + IP whitelist
4. `.env`: `RADAR_API_KEY` + `RADAR_REQUIRE_API_KEY=1`
5. `.\scripts\go_live_money.ps1` → PASS
6. `$env:RADAR_PROFILE='live-money'; .\scripts\run_radar.ps1`
7. Dashboard: `ok=true`, `mtf_ensure_ok=true`, then Auto ON only if operator asks
8. Keep size caps small (overlay ~5 USDT)

Optional helper: [scripts/check_env_presence.ps1](scripts/check_env_presence.ps1) (presence only).

## Rollback

Unset `RADAR_PROFILE` or Auto OFF immediately.

## Refuse

- Flipping `dry_run: false` in default.yaml as primary path.
- Enabling auto without go_live PASS.

## References

- [Checklist](references/live-money-checklist.md)
