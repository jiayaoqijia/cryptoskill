# Infra — VPN box, repo layout, farm scheduling, monitoring, backups

## The VPN box

The farm, captures, monitoring, and submit queue run on an **always-on box
inside the event VPN** — not a dev laptop (sleep = lost ticks; the analysis
laptop needs its CPU for RE anyway). Any machine with systemd: old laptop,
home server, cloud VM in the allowed region.

- Wired if possible; joins the organizer VPN (WireGuard/OpenVPN config from
  the event); ssh access for the whole team; NTP on (tick alignment matters).
- Runs: `scripts/farm.py` (timer-driven), `checker-wrap.sh` per service,
  tcpdump captures, `fail2ban`-style log watching on the gameboxes.
- Legal: all scanning/exploit traffic stays inside the event network per the
  rules — team subnets, gameboxes, documented APIs. Nothing else. See
  `../ctf/SKILL.md` remote gate: A/D gets one pre-authorization per event
  ("A/D remote OK for `<event>`"), scoped to the event network.

## Event repo layout (git, one repo per event)

```
work/<event>/
  services/<svc>/{orig,patched,patches,checker,compose,captures,notes.md}
  exploits/                     # farm modules: <svc>-<bug>.py
  farm/
    teams.txt                   # one host per line
    ids.json                    # host -> flag id
    submit.sh                   # --submit-cmd target (token lives here)
    farm-state.json             # farm ledger (gitignored)
  monitor/
    verdicts.log                # checker-wrap.sh appends here
    failures/                   # output of failed checker runs
  notes.md                      # rules, scoring, tick length, creds, timeline
```

`.gitignore`:

```
*.pcap
farm/farm-state.json*
farm/farm-state.json.tmp
farm/token
monitor/failures/
```

Commit discipline: one commit per patch (`patches/NNN-x.patch` + patched/
refresh), one per new exploit module. Keep `submit.sh` + `token` mode 600 and
gitignored; the repo may be shared widely after the event.

## Farm scheduling

One farm **cycle per tick**, driven by a systemd user timer — no
long-running process to babysit, state on disk between cycles, journal logs
for free:

```ini
# ~/.config/systemd/user/ad-farm.service
[Unit]
Description=A/D exploit farm cycle
[Service]
Type=oneshot
WorkingDirectory=/home/team/work/<event>/farm
ExecStart=/usr/bin/python3 /home/team/work/<event>/scripts/farm.py --submit-cmd ./submit.sh
```

```ini
# ~/.config/systemd/user/ad-farm.timer
[Unit]
Description=A/D farm every tick
[Timer]
OnCalendar=*:0/5
RandomizedDelaySec=20
AccuracySec=1
Persistent=false
[Install]
WantedBy=timers.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now ad-farm.timer
systemctl --user list-timers ad-farm.timer     # verify next fire time
journalctl --user -u ad-farm.service -f        # live cycle output
```

- `*:0/5` = every 5 minutes — set to the event's tick length
  (`OnCalendar=*:0/2` for 2-minute ticks, `*:0/10` for 10).
- `RandomizedDelaySec` jitter: don't fire in lockstep with every other team's
  farm at T+0 — it bursts the scoreboard API and makes your traffic pattern
  clockwork-obvious in other teams' captures.
- Cron alternative (no systemd):

```cron
*/5 * * * * sleep $((RANDOM % 20)); cd /home/team/work/<event>/farm && \
  /usr/bin/python3 ../scripts/farm.py --submit-cmd ./submit.sh >> farm.log 2>&1
```

- Very fast ticks: run one persistent process instead —
  `farm.py --interval 60 --submit-cmd ./submit.sh` inside tmux; it persists
  state after every cycle, so a crash costs one cycle.

## Submission queue

`farm.py` submits via `--submit-cmd`: a shell command run with `$FLAG` in the
environment; exit 0 = accepted, non-zero = retry with backoff, cooldown
enforced between calls. CTFd/rCTF endpoints: `../ctf/references/submission.md`.
Most A/D organizers roll a custom HTTP API — template `farm/submit.sh`:

```bash
#!/usr/bin/env bash
# submit.sh — one flag from $FLAG; exit 0 = accepted by the scoreboard.
set -euo pipefail
TOKEN=$(cat "$(dirname "$0")/token")
curl -sf -X POST \
     -H "Authorization: Bearer $TOKEN" \
     --data-urlencode "flag=$FLAG" \
     https://ad.example.com/api/submit >/dev/null
```

- `curl -f` turns HTTP errors into non-zero exit → the farm retries with
  backoff instead of silently dropping.
- Adapt endpoint/fields/auth from the organizer's docs; keep the exit-code
  contract so the farm never needs changing.
- chmod +x submit.sh; chmod 600 token.

## Monitoring

**SLA**: run `scripts/checker-wrap.sh` per service each tick — same timer
pattern as the farm (a second oneshot service, or one `monitor.sh` looping
services):

```bash
#!/usr/bin/env bash
# monitor.sh — one SLA verdict per service, alert on 2 consecutive FAILs.
set -u
cd "$(dirname "$0")/.."            # repo root
WEBHOOK="${WEBHOOK:-}"             # team chat webhook, optional
for svc in "$@"; do
  scripts/checker-wrap.sh -n "$svc" -t 60 -- \
      python3 "services/$svc/checker/check.py" "$svc.gamebox" 5000 || true
  fails=$(grep " $svc " monitor/verdicts.log | tail -n 2 | awk '$3=="FAIL"' | wc -l)
  if [ "$fails" -eq 2 ]; then
    msg="$svc SLA FAIL x2 — rollback now (defense.md)"
    curl -sf -X POST -d "payload=$msg" "$WEBHOOK" 2>/dev/null || notify-send "A/D" "$msg"
  fi
done
```

**Farm health** each tick: `farm-state.json` `cycles` increments, `queue`
drains (not growing monotonically), `failed` not filling. Cycle summaries:
`journalctl --user -u ad-farm.service --since -10min`.

**Disk**: pcaps rotate bounded (`-W 96`), still check `du -sh captures/`
daily; delete mined-and-committed-notes captures first.

Truth source is `monitor/verdicts.log` — greppable, append-only, one line per
checker run. If the team wants graphs, ship counts from that file to whatever
dashboard they already run; do not build one during the event.

## Backups

- `farm-state.json` is the flag ledger + pending queue: copy off-box daily:

```bash
rsync -a box:work/<event>/farm/ backups/<event>-$(date +%F)/
```

- Repo mirror (private remote — exploits in a public repo after the event
  only if the rules allow):

```cron
30 3 * * * cd /home/team/work/<event> && git add -A && git commit -m "auto $(date -Is)" >/dev/null; git push origin main >/dev/null
```

- Gameboxes: `good/` last-known-good trees live on the gameboxes themselves
  (`defense.md` rollback); also rsync one copy of each patched tree to the
  VPN box per deploy.

## Rules and legal notes

- **All attack traffic stays inside the event network** per the rulebook:
  organizer VPN/subnets, gameboxes, documented APIs. Scanning anything else
  is disqualification — and it is someone else's machine.
- No DoS, no service crashes: they cost other teams their SLA, violate every
  A/D rulebook, and make you the incident.
- The router's remote gate applies with the A/D pre-authorization exception
  (SKILL.md operating rules); re-confirm scope if the organizer adds
  infrastructure mid-event.
