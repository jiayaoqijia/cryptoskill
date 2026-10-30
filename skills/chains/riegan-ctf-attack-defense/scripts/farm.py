#!/usr/bin/env python3
"""farm.py — asyncio exploit farm for tick-based attack-defense CTFs.

Stdlib only. Exploit modules may import anything (pwntools, ...) — they run
inside this process, so keep them asyncio-friendly; a module that fails at
import is logged and skipped, never fatal.

Layout (resolved under --root, default cwd):
  teams.txt        one target host per line ('#' comments, blanks ignored)
  ids.json         JSON object: host -> flag id (string/number/object),
                   exactly the hosts used in teams.txt; missing -> None
  exploits/*.py    each module (not starting with '_') exposes:
                       async def exploit(host, flag_id, timeout) -> str | None
                   return the captured flag string, or None on a miss
  farm-state.json  persisted ledger: seen flags, pending submit queue,
                   submitted/failed flags, cumulative per-exploit stats

One cycle = every (team, exploit) pair runs under bounded concurrency with a
per-attempt timeout -> new flags deduped against history -> the submission
queue drains with cooldown, retries with backoff. Default is a single cycle
(drive it from cron/systemd per tick); --interval SECONDS loops forever.

Submission: --submit-cmd 'SHELL CMD' runs with $FLAG in the environment;
exit 0 = accepted, anything else = retry later. Without --submit-cmd, or
with --dry-run, flags are only printed. --dry-run is fully stateless: it
never reads or writes farm-state.json, so every cycle prints every flag it
captures (flags rotate per tick anyway).
"""

import argparse
import asyncio
import importlib.util
import inspect
import json
import os
import re
import sys
import time
from pathlib import Path


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="farm.py",
        description="Tick-based exploit farm: run exploits/ against every "
                     "team in teams.txt, dedupe flags, submit with cooldown.")
    p.add_argument("--root", default=".",
                   help="event dir holding teams.txt/ids.json/exploits (default: cwd)")
    p.add_argument("--teams", default="teams.txt",
                   help="one host per line (default: teams.txt)")
    p.add_argument("--ids", default="ids.json",
                   help="JSON object host -> flag id (default: ids.json)")
    p.add_argument("--exploits", default="exploits",
                   help="dir of exploit modules (default: exploits/)")
    p.add_argument("--state", default="farm-state.json",
                   help="persistent ledger file (default: farm-state.json)")
    p.add_argument("--submit-cmd", metavar="CMD", default=None,
                   help="shell command run with $FLAG in env; exit 0 = "
                        "accepted, non-zero = retry "
                        "(e.g. 'curl -sf -X POST -d \"flag=$FLAG\" https://ad/submit')")
    p.add_argument("--cooldown", type=float, default=2.0,
                   help="min seconds between submissions (default: 2)")
    p.add_argument("--max-retries", type=int, default=5,
                   help="submission attempts before a flag is abandoned (default: 5)")
    p.add_argument("--backoff", type=float, default=5.0,
                   help="base retry delay seconds, doubles each retry (default: 5)")
    p.add_argument("--timeout", type=float, default=20.0,
                   help="per (team, exploit) attempt timeout (default: 20)")
    p.add_argument("--concurrency", type=int, default=8,
                   help="max in-flight exploit attempts (default: 8)")
    p.add_argument("--flag-regex", metavar="RE", default=None,
                   help="only queue flags matching this regex, "
                        "e.g. 'flag\\{[^}]+\\}'")
    p.add_argument("--exploit", action="append", metavar="NAME",
                   help="run only this exploit module (repeatable); default: all")
    p.add_argument("--interval", type=float, metavar="SECS", default=None,
                   help="loop forever, sleeping SECS between cycles; "
                        "omit for a single cycle (cron/systemd driven)")
    p.add_argument("--dry-run", action="store_true",
                   help="print flags, submit nothing, never touch state")
    return p.parse_args(argv)


def resolve(root, p):
    q = Path(p)
    return q if q.is_absolute() else root / q


def read_teams(path):
    teams = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            teams.append(line)
    return list(dict.fromkeys(teams))          # dedupe, keep order


def read_ids(path):
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise SystemExit(f"[!] {path}: expected a JSON object host -> flag id")
    return data


def load_exploits(exploits_dir, only=None):
    mods = []
    if not exploits_dir.is_dir():
        return mods
    for path in sorted(exploits_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        name = path.stem
        if only and name not in only:
            continue
        spec = importlib.util.spec_from_file_location(f"ad_exploit_{name}", path)
        if spec is None or spec.loader is None:
            print(f"[!] {name}: cannot load module", file=sys.stderr)
            continue
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as exc:                       # team code, tolerate
            print(f"[!] {name}: import failed: {exc}", file=sys.stderr)
            continue
        fn = getattr(mod, "exploit", None)
        if fn is None or not inspect.iscoroutinefunction(fn):
            print(f"[!] {name}: needs 'async def exploit(host, flag_id, "
                  f"timeout)' — skipped", file=sys.stderr)
            continue
        mods.append((name, fn))
    return mods


def new_state():
    return {"cycles": 0, "seen": {}, "queue": [],
            "submitted": {}, "failed": {}, "stats": {}}


def load_state(path):
    if not path.exists():
        return new_state()
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[!] {path}: unreadable ({exc}) — starting fresh", file=sys.stderr)
        return new_state()
    if not isinstance(data, dict):
        return new_state()
    st = new_state()
    st.update({k: v for k, v in data.items() if k in st})
    return st


def save_state(path, state):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True))
    tmp.replace(path)


def coerce_flag(result, flag_re):
    """Return (flag, reason): flag str if accepted, else reason (None = miss)."""
    if result is None:                          # clean miss, stay quiet
        return None, None
    if isinstance(result, bytes):
        result = result.decode("utf-8", "replace")
    if not isinstance(result, str):
        return None, f"non-string return: {type(result).__name__}"
    flag = result.strip()
    if not flag:
        return None, None
    if flag_re is not None and not flag_re.search(flag):
        return None, f"regex reject: {flag[:60]!r}"
    return flag, None


async def attempt(name, fn, host, flag_id, timeout, sem, stats, flag_re):
    async with sem:
        stats[name]["attempts"] += 1
        try:
            # exploit self-limits with `timeout`; hard stop a bit later
            res = await asyncio.wait_for(fn(host, flag_id, timeout),
                                         timeout=timeout + 5.0)
        except asyncio.TimeoutError:
            stats[name]["errors"] += 1
            print(f"[!] {name} @ {host}: timeout({timeout:.0f}s)", file=sys.stderr)
            return None
        except Exception as exc:
            stats[name]["errors"] += 1
            print(f"[!] {name} @ {host}: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            return None
    flag, why = coerce_flag(res, flag_re)
    if flag is None:
        if why:
            print(f"[!] {name} @ {host}: dropped ({why})", file=sys.stderr)
        return None
    stats[name]["flags"] += 1
    print(f"[flag] {name} @ {host}: {flag}")
    return flag


async def submit_once(cmd, flag):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env={**os.environ, "FLAG": flag},
    )
    out = (await proc.communicate())[0].decode("utf-8", "replace").strip()
    return proc.returncode, out


async def drain_queue(args, state):
    """Submit due queue entries. Returns (submitted, failed) counts."""
    now = time.time()
    due, later = [], []
    for it in state["queue"]:
        (due if it["next_try"] <= now else later).append(it)
    state["queue"] = later
    submitted = failed = kept = 0
    for i, item in enumerate(due):
        flag = item["flag"]
        if args.dry_run or not args.submit_cmd:
            mode = "dry-run" if args.dry_run else "no-submit-cmd"
            print(f"[{mode}] would submit: {flag}")
            state["queue"].append(item)        # keep queued for a real run
            kept += 1
            continue
        if i:
            await asyncio.sleep(args.cooldown)
        rc, out = await submit_once(args.submit_cmd, flag)
        if rc == 0:
            print(f"[submit] ok: {flag}")
            state["submitted"][flag] = int(now)
            submitted += 1
        else:
            item["retries"] += 1
            if item["retries"] >= args.max_retries:
                print(f"[submit] GAVE UP after {item['retries']} tries: "
                      f"{flag} ({out[:120]})", file=sys.stderr)
                state["failed"][flag] = out[:200]
                failed += 1
            else:
                delay = args.backoff * (2 ** (item["retries"] - 1))
                item["next_try"] = now + delay
                state["queue"].append(item)
                print(f"[submit] retry {item['retries']}/{args.max_retries} "
                      f"in {delay:.0f}s: {flag} (rc={rc}: {out[:80]})",
                      file=sys.stderr)
    return submitted, failed


async def run_cycle(args, mods, teams, ids, state, flag_re):
    sem = asyncio.Semaphore(args.concurrency)
    cyc = {name: {"attempts": 0, "flags": 0, "errors": 0} for name, _ in mods}
    results = await asyncio.gather(*(
        attempt(name, fn, host, ids.get(host), args.timeout, sem, cyc, flag_re)
        for host in teams for name, fn in mods))
    new = 0
    for flag in results:
        if flag and flag not in state["seen"]:
            state["seen"][flag] = int(time.time())
            state["queue"].append({"flag": flag, "retries": 0, "next_try": 0.0})
            new += 1
    submitted, failed = await drain_queue(args, state)
    for name, s in cyc.items():               # merge into cumulative stats
        agg = state["stats"].setdefault(
            name, {"attempts": 0, "flags": 0, "errors": 0})
        for k in s:
            agg[k] += s[k]
    return cyc, new, submitted, failed


def print_summary(cyc, new, submitted, failed, pending, n_teams, n_mods):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"== {stamp}  cycle: {n_teams} teams x {n_mods} exploits")
    for name in sorted(cyc):
        s = cyc[name]
        print(f"   {name:<28} attempts {s['attempts']:<4} flags "
              f"{s['flags']:<3} errors {s['errors']}")
    print(f"   new {new} | submitted {submitted} | failed {failed} "
          f"| pending {pending}")


def main(argv=None):
    args = parse_args(argv)
    root = Path(args.root).resolve()
    teams_path = resolve(root, args.teams)
    ids_path = resolve(root, args.ids)
    exploits_dir = resolve(root, args.exploits)

    if not teams_path.exists():
        print(f"[!] {teams_path} not found — one host per line", file=sys.stderr)
        return 2
    teams = read_teams(teams_path)
    if not teams:
        print(f"[!] {teams_path} is empty", file=sys.stderr)
        return 2
    only = set(args.exploit) if args.exploit else None
    mods = load_exploits(exploits_dir, only)
    if not mods:
        print(f"[!] no usable exploit modules in {exploits_dir}", file=sys.stderr)
        return 2
    for want in sorted(only - {n for n, _ in mods}) if only else ():
        print(f"[!] exploit '{want}' not found in {exploits_dir}", file=sys.stderr)
    ids = read_ids(ids_path)
    if not ids:
        print(f"[!] {ids_path} missing/empty — every flag_id is None",
              file=sys.stderr)
    try:
        flag_re = re.compile(args.flag_regex) if args.flag_regex else None
    except re.error as exc:
        print(f"[!] bad --flag-regex: {exc}", file=sys.stderr)
        return 2

    state_path = None if args.dry_run else resolve(root, args.state)
    state = new_state() if state_path is None else load_state(state_path)
    if not args.submit_cmd and not args.dry_run:
        print("[!] no --submit-cmd: flags stay queued, nothing is submitted",
              file=sys.stderr)

    try:
        while True:
            state["cycles"] += 1
            cyc, new, submitted, failed = asyncio.run(
                run_cycle(args, mods, teams, ids, state, flag_re))
            pending = len(state["queue"])
            print_summary(cyc, new, submitted, failed, pending,
                          len(teams), len(mods))
            if state_path is not None:
                save_state(state_path, state)
            if args.interval is None:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[!] interrupted; state persisted" if state_path else
              "\n[!] interrupted", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
