#!/usr/bin/env python3
"""Fleet Command View — data generator.

Reads live fleet state from the vault + cron configs and emits a single
fleet-state.json for the dashboard at /var/www/gentechlabs/fleet.html.

Data sources (no new plumbing, per the handoff):
- Handoff lanes: 01-HANDOFFS/*-to-*/ status fields (same resolution logic
  as handoff-watcher.py / handoff-trigger.py)
- Build queue: scripts/build_queue.json (status counts, needs_jordan)
- Agent last-activity: ~/.hermes/profiles/<p>/cron/jobs.json last_run_at
"""
import json, os, re, glob, datetime

VAULT = "/root/vaults/gentech"
HANDOFFS = os.path.join(VAULT, "01-HANDOFFS")
PROFILES = ["gentech", "gentech-treasury", "gizmo", "pixel"]
OUT = "/var/www/gentechlabs/fleet-state.json"

RESOLVED_MARKERS = (
    "status: [x]", "status: resolved", "status: done", "status: closed",
    "## resolved", "- [x]", "status:** resolved", "status:** done",
    "status:** [x]", "status: completed", "status: shipped",
    "status: expired", "status:** expired",
    "status: awaiting jordan", "status:** awaiting jordan",
    "status: human-gated", "status:** human-gated",
    "shipped & verified", "shipped and verified", "verified shipped",
)

TO_LANE_RE = re.compile(r"^(.+)-to-(.+)$")

# Async / manual lanes — NO live consumer exists, so age is NOT a stall signal.
# `gentech-to-forge` targets Forge, a DESKTOP agent: he is not on the peer
# network, has no wake cron, and only reads his inbox when Jordan runs a
# session at the machine. Items here are "awaiting Forge's next session",
# not "an agent went silent" — counting them as stalled is a false alarm and
# hides the real ones (Jordan, Sep 11 2026).
ASYNC_LANES = {"gentech-to-forge", "INBOX/forge"}


def norm(text):
    low = text.lower()
    low = re.sub(r"[^\x00-\x7F]+", "", low)
    low = re.sub(r"\*\*", "", low)
    low = re.sub(r"\s+", " ", low)
    return low


def is_resolved(path):
    try:
        with open(path, encoding="utf-8") as f:
            n = norm(f.read())   # read ONCE — re-reading inside the generator hits EOF
        return any(m in n for m in RESOLVED_MARKERS)
    except OSError:
        return False


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def age_hours(ts):
    return round((now() - ts).total_seconds() / 3600, 1)


def scan_open_handoffs():
    """Open (unresolved) handoffs across all lanes. Root + deduped against mirror."""
    open_items = []
    seen = set()
    mirror = os.path.join(VAULT, "Gentech", "01-HANDOFFS")

    def scan_dir(base, is_mirror):
        if not os.path.isdir(base):
            return
        for d in sorted(os.listdir(base)):
            lane_path = os.path.join(base, d)
            if not os.path.isdir(lane_path):
                continue
            m = TO_LANE_RE.match(d)
            if d == "INBOX":
                for sub in sorted(os.listdir(lane_path)):
                    for f in sorted(glob.glob(os.path.join(lane_path, sub, "*.md"))):
                        _add(f, d + "/" + sub, is_mirror)
                continue
            if not m:
                continue
            for f in sorted(glob.glob(os.path.join(lane_path, "*.md"))):
                _add(f, d, is_mirror)

    def _add(f, lane, is_mirror):
        name = os.path.basename(f)
        key = (lane, name)
        if key in seen or is_resolved(f):
            return
        seen.add(key)
        st = os.stat(f)
        open_items.append({
            "lane": lane,
            "file": name,
            "age_hours": age_hours(datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc)),
            "size": st.st_size,
            "async": lane in ASYNC_LANES,
        })

    scan_dir(HANDOFFS, False)
    scan_dir(mirror, True)
    return sorted(open_items, key=lambda x: -x["age_hours"])


def queue_stats():
    with open(os.path.join(VAULT, "scripts", "build_queue.json")) as f:
        q = json.load(f)
    counts = {}
    for it in q:
        counts[it.get("status", "?")] = counts.get(it.get("status", "?"), 0) + 1
    needs_jordan = [it for it in q if it.get("needs_jordan") and it.get("status") not in ("done", "shipped", "closed")]
    return {
        "total": len(q),
        "by_status": counts,
        "open": sum(v for k, v in counts.items() if k not in ("done", "shipped", "closed", "cancelled", "dropped")),
        "needs_jordan": len(needs_jordan),
        "needs_jordan_items": [
            {"id": it.get("id"), "name": it.get("name"), "status": it.get("status"),
             "blocker": (it.get("blocker_note") or it.get("detail", ""))[:140]}
            for it in needs_jordan
        ],
    }


def agent_activity():
    agents = []
    for p in PROFILES:
        jf = f"/root/.hermes/profiles/{p}/cron/jobs.json"
        last_ts = None
        n_jobs = 0
        n_enabled = 0
        if os.path.exists(jf):
            try:
                d = json.load(open(jf))
                jobs = d if isinstance(d, list) else d.get("jobs", d.get("items", []))
                n_jobs = len(jobs)
                for j in jobs:
                    if j.get("enabled"):
                        n_enabled += 1
                    lr = j.get("last_run_at")
                    if lr:
                        try:
                            ts = datetime.datetime.fromisoformat(lr.replace("Z", "+00:00"))
                            if last_ts is None or ts > last_ts:
                                last_ts = ts
                        except ValueError:
                            pass
            except (OSError, ValueError):
                pass
        agents.append({
            "profile": p,
            "cron_jobs": n_jobs,
            "enabled": n_enabled,
            "last_run": iso(last_ts) if last_ts else None,
            "last_run_age_hours": age_hours(last_ts) if last_ts else None,
        })
    return agents


def main():
    state = {
        "generated": iso(now()),
        "version": "1.0.0",
        "agents": agent_activity(),
        "queue": queue_stats(),
        "open_handoffs": scan_open_handoffs(),
    }
    open_h = state["open_handoffs"]
    active = [h for h in open_h if not h.get("async")]
    state["summary"] = {
        "open_handoffs": len(open_h),
        "active_handoffs": len(active),
        "stalled_handoffs": len([h for h in active if h["age_hours"] >= 6]),
        "async_handoffs": len([h for h in open_h if h.get("async")]),
        "queue_open": state["queue"]["open"],
        "decisions_waiting": state["queue"]["needs_jordan"],
    }
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, OUT)
    print(f"wrote {OUT}: {state['summary']}")


if __name__ == "__main__":
    main()
