---
name: radar-live-money-gate
description: >-
  Preflight before DUP Market Radar live spot capital. Fail-closed checklist;
  never enable futures auto; never invent KuCoin keys. Use when the user asks
  to go live, dry_run false, or enable auto with real money.
license: MIT
compatibility: Requires dup-market-radar checkout, .env with KuCoin Spot keys, radar_native.
metadata:
  author: dup-labs
  version: "0.1.10"
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
4. Never print or commit secrets. Never invent missing KuCoin keys.

## Steps

1. Prefer recent `verify Full` / `go_ready` evidence (not 48h soak).
2. Confirm `radar_native` available
3. `.env`: KuCoin Spot KEY/SECRET/PASSPHRASE + IP whitelist (operator fills — do not invent)
4. `.env`: `RADAR_API_KEY` + `RADAR_REQUIRE_API_KEY=1`
5. Status check: `.\scripts\go_live_money.ps1 -Status` (lists blockers; exit 0 ≠ PASS)
6. `.\scripts\go_live_money.ps1` → **PASS** required before activate
7. `$env:RADAR_PROFILE='live-money'; .\scripts\run_radar.ps1`
8. Dashboard: `ok=true`, `mtf_ensure_ok=true`, then Auto ON only if operator asks
9. Keep size caps small (overlay ~5 USDT)

Optional helper: [scripts/check_env_presence.ps1](scripts/check_env_presence.ps1) (presence only).

## Rollback

Unset `RADAR_PROFILE` or Auto OFF immediately.

## Refuse

- Flipping `dry_run: false` in default.yaml as primary path.
- Enabling auto without go_live PASS.
- Claiming live-ready when `-Status` only listed blockers.
- Starting 48h soak as part of live-money.

## References

- [Checklist](references/live-money-checklist.md)
