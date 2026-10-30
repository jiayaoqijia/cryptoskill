# A/D runbook — prep, first hour, per-tick rhythm, endgame

## Team roles (decide before the event starts)

| Role | Owns | Merges into (team of 2-3) |
|---|---|---|
| Patcher | read service source, minimal patches, deploy + rollback | captured-exploit triage |
| Exploiter | vuln → exploit function per service, farm modules | read other teams' payloads |
| Infra | VPN box, replicas, farm scheduling, monitoring, backups | flag-id refresh, submit queue |

Roles are queue ownership, not silos. Shared state is `notes.md` per service:
hypothesis → evidence → next step, exactly like the router's workspace rule.

## Before the event (prep, ~2 hours)

1. **VPN box ready** — an always-on machine (old laptop/VM) that joins the
   event VPN and stays up. The farm, monitoring, and captures run there, not
   on a dev laptop: laptop sleep = lost ticks, and the analysis laptop needs
   its CPU for RE. SSH access for the whole team. Details: `infra.md`.
2. **Event repo skeleton** — `git init`, layout from `infra.md`; tools
   preinstalled on the box:

```bash
sudo pacman -S --needed podman podman-compose tcpdump wireshark-cli \
                          radare2 fail2ban jq
```

3. **Local env per service** — the offline lab. If the organizer ships a
   Dockerfile/compose, build it; otherwise write one matching the gamebox
   runtime (same base image, same port):

```yaml
# services/<svc>/compose/compose.yaml
services:
  svc-foo:
    build: ../orig            # or: image: docker.io/library/python:3.11-slim
    ports: ["127.0.0.1:5000:5000"]
```

```bash
cd services/<svc>/compose
podman-compose up -d --build
podman-compose logs -f        # watch it boot; errors here are organizer bugs, ask on IRC
podman-compose down           # teardown between experiments
```

4. **Farm skeleton** — `farm/{teams.txt,ids.json,exploits/}` plus a clone of
   this repo on the VPN box. Prove the loop once with the stub exploit from
   `offense.md` and `python3 scripts/farm.py --root farm --dry-run`.

## First hour (order matters, gates not suggestions)

1. **Unpack the bundle** (5 min):

```bash
cd work/<event>
mkdir -p services/foo/{orig,patched,patches,checker,compose,captures}
tar xf foo-bundle.tar.gz -C services/foo/orig      # or: 7z x -oservices/foo/orig
ls -laR services/foo/orig | head -50               # inventory
sha256sum services/foo/orig/**/* > services/foo/orig.sha256  # compare vs teammates
```

   Inventory what came: source? binary only? Dockerfile? checker? bot?
   flag-format sample? **exploit samples** — some events ship example
   exploits; read those first, they are free attack points. Never edit `orig/`.

2. **Read the rules once**, extract into `notes.md`: tick length, scoring
   formula (SLA / defense / attack weights), flag rotation period, submission
   rate limits or wrong-flag penalties, patch policy (some events forbid
   replacing binaries or require source patches), allowed infra.

3. **Read the checker source** — it is the SLA contract. List every behavior
   it asserts: endpoints hit, request/response round-trips, bot actions,
   expected outputs, timings. A patch is legal **iff the checker still
   passes**. Time one checker run; that sets your `checker-wrap.sh -t`.

4. **Replica green**:

```bash
cd services/foo/compose && podman-compose up -d
curl -s http://127.0.0.1:5000/ | head              # or: nc -z 127.0.0.1 5000
cd ../..
scripts/checker-wrap.sh -n foo -t 60 -- \
    python3 services/foo/checker/check.py 127.0.0.1 5000   # adapt argv to the checker
```

   Green = offline lab. From here on, nothing ships to the gamebox that did
   not pass this gate.

5. **Baseline traffic** — know what benign looks like so attacks stand out:

```bash
sudo tcpdump -i any -s0 -w services/foo/captures/baseline.pcap port 5000 &
# run the checker twice against the replica, then stop the capture
```

6. **Deploy the stock service** through the organizer's flow, then run the
   checker against the gamebox → first verdict lines reach monitoring
   (`infra.md`). No patches yet: stock + green first, patch second.

7. **Flag ids** — fetch → `farm/ids.json`, build `farm/teams.txt` from the IP
   map (`offense.md`). First `farm.py --dry-run`. Exploiters branch off per
   service from here.

First-hour gates:

| Clock | Gate |
|---|---|
| T+15 | bundle unpacked, rules in notes.md, checker read |
| T+30 | replica green locally (`checker-wrap.sh` exit 0) |
| T+45 | stock service green on gamebox, monitoring receiving verdicts |
| T+60 | ids cached, farm dry-run green, first exploit module started |

## Per-tick rhythm

Assume 5-minute ticks; scale to the event's real tick.

| Moment | Action |
|---|---|
| T+0 | Farm fires automatically (systemd timer, ≤20s jitter). New flags queue/submit with cooldown. |
| T+0:30 | Read the latest SLA verdicts. 2 consecutive FAIL for one service → patcher drops everything and rolls back (`defense.md`). |
| T+1 | Triage new traffic in `captures/`: unknown payloads against your port are other teams' exploits — mine them (`offense.md`). |
| T+2 | Patch queue: one patch per service per tick, max. Each waits on checker-green locally. |
| T+3 | Public-exploit watch: some events publish solves after N ticks; teams also leak exploits in traffic. Adapt theirs before they finish patching. |
| T+4 | Farm health: hit-rate per exploit, queue not growing, disk not filling. |

Discipline points:

- The farm must fire at T+0 without a human — if it needs a human, fix the
  timer, not the tick (`infra.md`).
- Flags rotate per tick; old flag values are worthless. The farm re-extracts
  every cycle; never cache flag strings.
- Deploying mid-tick is fine; deploying without a green checker run first is
  never fine.

## Endgame (last hour)

- **Farm to the last second.** Flags rotate every tick and the final ticks are
  often uncontested — teams relax. A live farm beats a clever human at T-5.
- **Freeze risky patches** in the last ~15 minutes: a deploy you cannot
  verify + roll back before the whistle costs more SLA than it saves. Small
  validation fixes only.
- **Defense weight effectively rises late**: public exploits have spread, so
  unpatched services bleed harder every tick. Keep monitoring loud; fix SLA
  dips instantly.
- **Drain the submission queue** before the scoreboard closes: check
  `farm/farm-state.json` `queue` is empty and `failed` entries were retried.
- **After the event**: commit patches + captures + farm state; writeup per the
  router skill (`skills/ctf/references/writeup.md`).
