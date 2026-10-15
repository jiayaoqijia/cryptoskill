#!/usr/bin/env python3
"""
HANDOFF watcher — STATEFUL. Reports only NEW handoffs and STATUS CHANGES.

Runs as a no_agent cron script. To stay silent when nothing changes, it keeps
a state file of what it has already reported and only prints:
  - NEW open handoffs (appeared since last run)
  - RESOLVED handoffs (were open, now marked resolved — "cleared")
  - NEW recent completions (agents reporting what they shipped)

If nothing changed since the last run, it prints NOTHING → cron stays silent.
When every open item is resolved/cleared and there are no new completions,
it prints nothing too (Jordan isn't working on anything).

State file lives next to the script: handoff-watcher.state.json

Usage:
    python3 handoff-watcher.py [vault_path] [--days N] [--vault-name NAME] [--state PATH]
"""
import os
import re
import sys
import json
import datetime

VAULT = "/root/vaults/gentech"
INBOX = os.path.join(VAULT, "01-HANDOFFS", "INBOX")
HANDOFFS = os.path.join(VAULT, "01-HANDOFFS")

VAULT_NAME = "gentech"
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "handoff-watcher.state.json")

KNOWN_GROUPS = {"hq", "forge", "labs", "entertainment", "treasury", "gizmo"}

# Lanes that belong to a HUMAN. A handoff landing here is news; a handoff moving
# between two agents is transit — the agents' business, not Jordan's.
HUMAN_LANES = {"hq", "jordan", "jintech"}

# An open handoff older than this (by filename date) with no return note is
# STUCK — that is the thing worth interrupting a human for.
STUCK_AFTER_HOURS = 24

# Only report stuck items in lanes this seat owns ([] = all non-human lanes).
OWN_LANES = []

# Re-nag the same stuck item at most once per day, and cap the list per run.
STUCK_RENAG_HOURS = 24
MAX_STUCK_PER_RUN = 5

RESOLVED_MARKERS = (
    "status: [x]",
    "status: resolved",
    "status: done",
    "status: closed",
    "## resolved",
    "- [x]",
    "status:** resolved",   # bold form: **Status:** resolved
    "status:** done",       # bold form: **Status:** done
    "status:** [x]",
)

COMPLETION_FILES = {
    "gentech": "gentech-completions.md",
    "entertainment": "entertainment-completions.md",
    "treasury": "treasury-completions.md",
    "labs": "labs-completions.md",
    "gizmo": "gizmo-completions.md",
    "forge": "forge-completions.md",
    "hq": "hq-completions.md",
}


def is_resolved(path):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return False
    low = text.lower()
    return any(m in low for m in RESOLVED_MARKERS)


def obsidian_link(rel_path):
    from urllib.parse import quote
    file_part = quote(rel_path, safe="")
    return f"obsidian://open?vault={VAULT_NAME}&file={file_part}"


def find_open():
    """Return dict {relative_path: (group, filename)} of still-open handoffs."""
    open_notes = {}
    if not os.path.isdir(INBOX):
        return open_notes
    for group in sorted(os.listdir(INBOX)):
        if group not in KNOWN_GROUPS:
            continue
        gdir = os.path.join(INBOX, group)
        if not os.path.isdir(gdir):
            continue
        for name in sorted(os.listdir(gdir)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(gdir, name)
            if is_resolved(path):
                continue
            rel = os.path.relpath(path, VAULT)
            open_notes[rel] = (group, name, path)
    return open_notes


def recent_completions(days=2):
    """Return {snippet: group} for completion lines dated within the window."""
    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    recent = {}
    for grp, fname in COMPLETION_FILES.items():
        fpath = os.path.join(HANDOFFS, fname)
        if not os.path.isfile(fpath):
            continue
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("-"):
                continue
            m = re.search(r"(20\d\d-\d\d-\d\d)", line)
            if m:
                try:
                    d = datetime.date.fromisoformat(m.group(1))
                except ValueError:
                    continue
                if d >= cutoff:
                    snippet = line.lstrip("- ").strip()
                    key = (grp, snippet[:120])
                    recent[key] = grp
    return recent


def load_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(state):
    try:
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except OSError:
        pass


def main():
    global VAULT, INBOX, HANDOFFS, VAULT_NAME, STATE_PATH
    argv = sys.argv[1:]
    days = 2
    while argv:
        a = argv.pop(0)
        if a == "--days" and argv:
            days = int(argv.pop(0))
        elif a == "--vault-name" and argv:
            VAULT_NAME = argv.pop(0)
        elif a == "--state" and argv:
            STATE_PATH = argv.pop(0)
        elif a.startswith("/") and os.path.isdir(a):
            VAULT = a
            INBOX = os.path.join(VAULT, "01-HANDOFFS", "INBOX")
    HANDOFFS = os.path.join(VAULT, "01-HANDOFFS")

    prev = load_state()
    prev_open = set(prev.get("open", []))
    # completions are stored as [grp, snippet] lists in JSON; convert to tuples
    prev_completions = set(tuple(c) if isinstance(c, list) else c
                           for c in prev.get("completions", []))

    cur_open = find_open()          # rel -> (group, name, path)
    cur_open_keys = set(cur_open.keys())
    cur_completions = recent_completions(days)
    cur_completion_keys = set(cur_completions.keys())

    lines = []

    # ── Report EXCEPTIONS, not TRANSIT ──────────────────────────────────────
    # Jordan (Sep 11): "It's just telling me that the message was sent."
    # A handoff moving between two agents is not news — it is the system
    # working. Only two things earn a human's attention:

    # (1) NEW handoffs ADDRESSED TO A HUMAN. These are actually for Jordan.
    new_open = cur_open_keys - prev_open
    human_new = [r for r in new_open if cur_open[r][0] in HUMAN_LANES]
    if human_new:
        lines.append("📨 FOR YOU:")
        for rel in sorted(human_new):
            grp, name, path = cur_open[rel]
            lines.append(f"• {name}")
            lines.append(f"    {obsidian_link(rel)}")

    # (2) STUCK items — open a long time with no return. These need chasing, and
    #     they are the reason a human would want to be interrupted at all.
    now = datetime.datetime.now()

    # Only report stuck items in lanes this seat owns. Without this, every agent
    # scans the same vault and mails the same vault-wide list — three copies of
    # one fact. Empty OWN_LANES = every non-human lane (kit default).
    # Never re-nag the same item more than once per day: a NEW stuck item alerts
    # immediately; an OLD one reminds daily, not every 15 minutes.
    prev_nagged = prev.get("stuck_nagged", {}) or {}

    stuck = []
    for rel in sorted(cur_open_keys):
        grp, name, path = cur_open[rel]
        if grp in HUMAN_LANES:
            continue                      # already surfaced above, as yours
        if OWN_LANES and grp not in OWN_LANES:
            continue                      # not this seat's lane
        m = re.match(r"^(20\d\d-\d\d-\d\d)", name)
        if not m:
            continue
        try:
            opened = datetime.datetime.strptime(m.group(1), "%Y-%m-%d")
        except ValueError:
            continue
        age_h = (now - opened).total_seconds() / 3600
        if age_h < STUCK_AFTER_HOURS:
            continue
        last = prev_nagged.get(rel)
        if last:
            try:
                since_h = (now - datetime.datetime.fromisoformat(last)).total_seconds() / 3600
                if since_h < STUCK_RENAG_HOURS:
                    continue          # already nagged recently — stay quiet
            except ValueError:
                pass
        stuck.append((int(age_h // 24), grp, name, rel))

    cur_nagged = {rel: now.isoformat() for _, _, _, rel in stuck}

    if stuck:
        total = len(stuck)
        shown = stuck[:MAX_STUCK_PER_RUN]
        lines.append("")
        lines.append("\U0001f6a9 STUCK (%d \u2014 open >%dh, no return):" % (total, STUCK_AFTER_HOURS))
        for days, grp, name, rel in shown:
            lines.append("\u2022 [%s] %dd \u2014 %s" % (grp, days, name))
            lines.append("    " + obsidian_link(rel))
        if total > len(shown):
            lines.append("    \u2026and %d more (see INBOX/)" % (total - len(shown)))

    # CLEARED and NEW-completions lines are deliberately GONE: they are transit
    # and vanity respectively. Completions belong in the daily wrap, not a
    # real-time ping. An alert that fires when nothing is wrong trains people
    # to ignore the one that matters.

    # Update state
    merged_nagged = {k: v for k, v in (prev.get("stuck_nagged", {}) or {}).items()
                     if k in cur_open_keys and k not in cur_nagged}
    merged_nagged.update(cur_nagged)
    save_state({"open": sorted(cur_open_keys),
                "completions": sorted(cur_completion_keys),
                "stuck_nagged": merged_nagged})

    if not lines:
        # nothing changed — print nothing (silent)
        return 0

    print("\n".join(lines))
    return 0


import datetime

if __name__ == "__main__":
    sys.exit(main())
