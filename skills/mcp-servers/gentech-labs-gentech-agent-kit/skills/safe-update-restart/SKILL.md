---
name: safe-update-restart
description: "Safe update/restart procedure for a production Hermes VPS that runs many live APIs, services, and multiple agent gateways sharing one venv. Full backup → controlled window → restart → verify every service and endpoint after. Never blind-restart."
version: 1.0.0
author: Gentech
tags: [update, restart, deployment, operations, hermes, gateway, verification, backup, safety]
license: MIT
---

# Safe Update & Restart for Production VPS

## When to Use
- Updating Hermes Agent (`hermes update`) on a box that runs live services.
- Restarting the gateway, x402 gateway, or any service someone may be connected to.
- Any restart where "someone could be connecting any minute."
- Recovering after a service or gateway change.

## The Core Principle
**Never blind-restart.** A production VPS hosts many live APIs, x402 services, and
multiple agent gateways that share one Hermes venv. A careless update/restart can drop
a live connection or take down a service with no warning. Always: **backup → controlled
window → restart each service → verify everything after.**

## The Procedure

### Step 1 — Record the baseline (BEFORE touching anything)
Capture current state so you can prove nothing regressed:
```bash
# hermes gateways (note PIDs)
for p in <profile1> <profile2> <profile3>; do
  pid=$(pgrep -f "profile $p gateway run" | head -1)
  echo "$p: pid=${pid:-DOWN}"
done
# systemd services
for svc in <x402-api> <x402-backend@...> <other services>; do
  echo "$svc: $(systemctl is-active "$svc" 2>/dev/null)"
done
# public endpoints
for u in "https://api.example.net/" "https://api.example.net/status"; do
  echo "$u -> $(curl -s -m 12 -o /dev/null -w '%{http_code}' "$u")"
done
```

### Step 2 — Take a rollback-safe backup
Use the **quick snapshot** (covers config, .env, auth, state.db, cron — the
rollback-critical files). A full zip of `~/.hermes` can be 30-40GB+ and take 30+ min —
too heavy for rollback needs.
```bash
hermes backup -q -l pre-update-$(date +%Y%m%d) -o /root/hermes-quick-backup.zip
```
Also record the git rollback point:
```bash
cd /usr/local/lib/hermes-agent && git log -1 --oneline && git describe --tags
```
> **PITFALL:** A full `hermes backup` (no `-q`) zips the entire 30-40GB `~/.hermes`
> including cargo/node caches — it's slow and produces giant zips that fill disk. Use
> `-q` unless you have a specific reason for the full archive. Delete any stale
> `.partial` files it leaves behind.

### Step 3 — Controlled update
```bash
cd /usr/local/lib/hermes-agent && hermes update --yes
```
Run it in the **background** with completion notification — a large commit jump (hundreds
of commits) takes several minutes for git pull + dependency reinstall, and will exceed a
foreground timeout.
> The update does a **graceful gateway drain** before restarting managed gateways on the
> new code — this is the safe handoff, not a bug. Wait it out; don't kill it.

### Step 4 — Verify every service and endpoint AFTER (the checklist)
Compare against the Step 1 baseline. All gateways should have **new PIDs** (restarted on
new code); all services `active`; all endpoints matching the baseline code.
```bash
# 1. gateways restarted on new code?
for p in <profiles>; do echo "$p: pid=$(pgrep -f "profile $p gateway run" | head -1)"; done
# 2. version bumped?
hermes --version
# 3. services still active?
for svc in <services>; do echo "$svc: $(systemctl is-active "$svc")"; done
# 4. public endpoints still up (must match baseline)?
for u in <endpoints>; do echo "$u -> $(curl -s -m 12 -o /dev/null -w '%{http_code}' "$u")"; done
# 5. paid API rail still intact (x402 returns 402 PaymentRequired, not 500)?
curl -s -m 15 -L "<paid-endpoint>" -o /tmp/resp.json -w "HTTP %{http_code}\n"
```

## Pitfalls
- ❌ **Blind `hermes update`** on a box with other live agents — can drop their sessions. Backup + controlled window first.
- ❌ **Full backup when you only need rollback state** — `-q` snapshot is enough; full zip is 30-40GB and slow.
- ❌ **Killing the update during gateway drain** — the drain is the graceful handoff; killing it mid-drain can orphan gateways.
- ❌ **Truncating a 402 body with `head -c`** then failing JSON parse — a 402 PaymentRequired response is correct; parse the *full* body to verify the rail.
- ❌ **Assuming a service is broken when it was `inactive` in the baseline too** — compare against the Step 1 baseline, not an assumed "should be active" list.
- ❌ **`git rev-list --count <old>..origin/main`** counts all upstream commits; the actual update jump may differ (see `hermes version`).

## Verification
- All gateways show new PIDs (restarted on new code).
- `hermes --version` shows the new version.
- Every service `active` (matching baseline).
- Every public endpoint returns the baseline HTTP code.
- Paid API rail returns HTTP 402 with valid x402Version + accepts (not 5xx).
