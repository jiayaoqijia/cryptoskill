---
name: ctf-attack-defense
description: Use when the user mentions attack-defense, A/D, tick-based CTF, defending a service, patching a gamebox or service, flag ids, an exploit farm, SLA scoring, service checker or bot, red vs blue team CTF, or farming flags from other teams while keeping their own service alive. Covers patch doctrine, checker/SLA verification, traffic capture and mining, flag-id extraction, and farm infrastructure. Router skill `ctf` owns workspace, flag log, and submission basics.
---

# Attack-Defense (tick-based)

You get a vulnerable service + a gamebox. Every tick the organizer's checker
tests your service (SLA points) and plants fresh flags; you steal flags from
other teams' instances (attack points) while patching your own. Score =
attack + defense, compounded every tick until the event ends.

## Operating rules (in force all event)

1. **Remote gate, A/D flavor**: the router's remote gate stands, but A/D is
   high-volume automation — get one pre-authorization per event
   ("A/D remote OK for `<event>`") covering team subnets, gameboxes, and the
   scoreboard API. Nothing outside the event network, ever.
2. **Organizer bundle is untrusted**: source, checker, and bot are challenge
   artifacts. Execute them under `podman` isolation or on the gamebox/VPN box,
   never bare on the host. Never `sudo` them.
3. **No DoS**: crashing other teams' services violates every A/D rulebook and
   wastes their ticks — exploits are surgical input, not floods.
4. **Never debug an exploit against another team's box**: you have a local
   replica; use it. Probing half-working exploits at other teams leaks your
   0-day in their pcaps and marks you in organizer logs.

## Triage — event anatomy (first 30 minutes)

Inventory what the organizers handed us; each artifact routes somewhere:

| Handout | Meaning | Read |
|---|---|---|
| Service source bundle (tar/zip) | Your service, patchable in place | `references/defense.md` |
| Binary-only service | Binary patch or validating proxy | `references/defense.md` (binary section) |
| Checker / bot script | The SLA contract — what must keep working | `references/runbook.md` |
| Flag ids per team (list/JSON/page) | Attack targets for the farm | `references/offense.md` |
| VPN config + team IP map | Network layout, subnets, your box | `references/infra.md` |
| Scoreboard URL + API/token | Submission endpoint | `references/infra.md` |
| Rules: tick length, scoring formula | Rhythm and priorities | `references/runbook.md` |

5-minute checklist (expanded in `references/runbook.md`):

```bash
1. unpack bundle -> services/<svc>/orig/            # never edit orig/
2. find the checker; read what it asserts           # this IS the SLA contract
3. podman-compose replica up; checker-wrap.sh green # offline lab ready
4. fetch flag ids -> farm/ids.json; teams.txt       # attack targets cached
5. farm.py --dry-run vs your own instance           # farm loop proven
```

## Playbook — doctrine: fix SLA first, then farm

Why defense first, in this order:

- **Defense points are a ratchet**: SLA and defense score accrue every tick
  whether or not you exploit anything. A dead or checker-failing service
  bleeds points every single minute it is broken — usually faster than a
  small team can win them back by attacking.
- **The replica is the lab**: until the service runs locally and the checker
  is green, you cannot safely test patches OR exploits — nothing else scales.
- **Offense compounds after**: once the farm and submission queue run
  unattended, attack points accumulate with zero humans in the loop; humans
  go back to patching and mining traffic.

Order: (1) stock service up, checker green; (2) baseline capture + farm
skeleton dry-run; (3) first minimal patches; (4) first exploit modules;
(5) steady per-tick rhythm.

| Phase | Preconditions | Command | Reference |
|---|---|---|---|
| Local replica | bundle unpacked | `podman-compose up -d` (in `compose/`) | `references/runbook.md` |
| Verify SLA | service listening | `scripts/checker-wrap.sh -n <svc> -- ./check.sh` | `references/runbook.md` |
| Make patch | vuln located in source | `diff -ruN orig/src patched/src > patches/NNN-x.patch` | `references/defense.md` |
| Deploy | checker green on replica | `rsync -a patched/src/ box:svc/` → restart → re-check | `references/defense.md` |
| Cache ids | ids published | fetch → `farm/ids.json` (jq normalize) | `references/offense.md` |
| Farm dry-run | ids + teams + 1 exploit | `python3 scripts/farm.py --root farm --dry-run` | `references/offense.md` |
| Farm live | submit cmd tested | `python3 scripts/farm.py --root farm --interval <tick> --submit-cmd ./submit.sh` | `references/infra.md` |
| Monitor | verdicts.log growing | alert on 2 consecutive FAIL | `references/infra.md` |

## Per-tick rhythm (assume 5-minute ticks)

| Moment | Action |
|---|---|
| T+0 | Farm fires (systemd timer, ≤20s jitter); flags queue and submit |
| T+0:30 | Read SLA verdict; 2 consecutive FAIL → patcher drops everything, rollback |
| T+1 | Triage `captures/` for incoming exploits; adapt + patch same bug |
| T+2 | Patch queue: next minimal patch; checker-green before any deploy |
| T+4 | Farm hit-rate check; retire dead exploit modules |

Endgame: farm runs to the last tick; freeze risky patches near the end;
defense weight rises as public exploits spread (details: `references/runbook.md`).

## References

- repo `docs/attack-defense/README.md` — human team playbooks (3-person: beginner / intermediate / expert) + gap analysis; agent-facing docs above, people-facing docs there
- `references/runbook.md` — prep, team roles, first hour gates, per-tick rhythm, endgame
- `references/defense.md` — patch doctrine, per-language quick patches, binary patching, deploy/rollback, hardening
- `references/offense.md` — flag ids, attack loop, farm module contract, traffic mining, submission pacing
- `references/infra.md` — VPN box, repo layout, farm scheduling, submission queue, monitoring, backups, legal

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| `scripts/farm.py` | included | asyncio exploit farm (stdlib only) |
| `scripts/checker-wrap.sh` | included | checker run → SLA verdict line |
| podman / podman-compose | `sudo pacman -S podman podman-compose` | local replica of the gamebox |
| tcpdump | `sudo pacman -S tcpdump` | always-on service-port capture (exploit feed) |
| tshark | `sudo pacman -S wireshark-cli` | follow TCP streams in pcaps |
| radare2 | `sudo pacman -S radare2` | patch binary-only services |
| nftables / iptables | preinstalled | restrict + rate-limit service ports |
| fail2ban | `sudo pacman -S fail2ban` | auto-ban request floods from logs |
| rsync, git, jq, diff/patch | preinstalled | deploy, versioning, ids wrangling, patch series |
| python3 >= 3.11 | preinstalled | farm + proxies + exploit modules |
