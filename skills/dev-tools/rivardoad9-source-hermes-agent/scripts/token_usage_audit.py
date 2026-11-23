#!/usr/bin/env python3
"""Token/cost audit for a Hermes install.

Usage:
    python3 token_usage_audit.py [--db PATH] [--days N] [--top N] [--tz-offset-h N]

Reads $HERMES_HOME/state.db (default ~/.hermes/state.db) read-only and prints the
five cuts described in references/token-usage-and-cost-audit.md. Safe to run while
the gateway is live.
"""
import argparse
import datetime as dt
import os
import sqlite3
import sys


def fmt(n):
    return f"{(n or 0) / 1e6:.1f}M"


def main():
    home = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join(home, "state.db"))
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--tz-offset-h", type=int, default=7,
                    help="server local-time offset used for the per-day cut")
    a = ap.parse_args()

    if not os.path.exists(a.db):
        sys.exit(f"no state.db at {a.db} — pass --db or set HERMES_HOME")
    con = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    cur = con.cursor()
    off = f"{a.tz_offset_h:+d} hours"

    cur.execute("""select sum(api_call_count), sum(input_tokens), sum(output_tokens),
                          sum(cache_read_tokens), sum(reasoning_tokens)
                   from session_model_usage""")
    call, inp, out, cache, reason = cur.fetchone()
    total = (inp or 0) + (out or 0) + (cache or 0)
    print("=== all time ===")
    print(f"api calls {call or 0:,} | input {fmt(inp)} | output {fmt(out)} | "
          f"cache_read {fmt(cache)} | reasoning {fmt(reason)}")
    print(f"total processed {fmt(total)}")

    print(f"\n=== per day (last {a.days}) ===")
    cur.execute(f"""select date(started_at,'unixepoch','{off}') d, count(*), sum(message_count),
                           sum(api_call_count), sum(input_tokens), sum(output_tokens),
                           sum(cache_read_tokens)
                    from sessions where started_at > strftime('%s','now') - ?*86400
                    group by d order by d""", (a.days,))
    for d, n, msg, c, i, o, ca in cur.fetchall():
        print(f"{d} | sessions {n:>3} | msgs {msg or 0:>6} | calls {c or 0:>5} | "
              f"in {fmt(i):>7} | out {fmt(o):>7} | cache {fmt(ca):>7} | "
              f"total {fmt((i or 0)+(o or 0)+(ca or 0)):>7}")

    print(f"\n=== top {a.top} sessions by tokens ===")
    cur.execute("""select source, title, message_count, api_call_count, input_tokens, output_tokens,
                          cache_read_tokens, started_at
                   from sessions
                   order by (coalesce(input_tokens,0)+coalesce(cache_read_tokens,0)
                             +coalesce(output_tokens,0)) desc limit ?""", (a.top,))
    for src, title, msg, c, i, o, ca, st in cur.fetchall():
        when = dt.datetime.fromtimestamp(st).strftime("%d %b %H:%M") if st else "?"
        tot = (i or 0) + (o or 0) + (ca or 0)
        per_call = (ca or 0) / c if c else 0
        print(f"{fmt(tot):>7} | {when} | calls {c or 0:>4} | ~{per_call/1e3:.0f}k ctx/call | "
              f"{src} | {str(title or '')[:56]}")

    cur.execute("""select count(*), sum(input_tokens), sum(output_tokens), sum(cache_read_tokens)
                   from sessions where source='cron'
                     and started_at > strftime('%s','now') - ?*86400""", (a.days,))
    n, i, o, ca = cur.fetchone()
    cron_total = (i or 0) + (o or 0) + (ca or 0)
    print(f"\n=== cron slice (last {a.days} d) ===")
    print(f"sessions {n or 0} | total {fmt(cron_total)}")
    cur.execute("""select sum(input_tokens+coalesce(cache_read_tokens,0)+output_tokens)
                   from sessions where started_at > strftime('%s','now') - ?*86400""", (a.days,))
    all_total = cur.fetchone()[0] or 0
    if all_total:
        print(f"share of all usage: {cron_total / all_total * 100:.1f}%")

    print("\n=== by work type ===")
    cur.execute("""select coalesce(nullif(task,''),'(main turns)') t, count(*), sum(api_call_count),
                          sum(input_tokens), sum(output_tokens), sum(cache_read_tokens)
                   from session_model_usage group by t
                   order by sum(coalesce(input_tokens,0)+coalesce(cache_read_tokens,0)
                                +coalesce(output_tokens,0)) desc limit 10""")
    for t, rows, c, i, o, ca in cur.fetchall():
        tot = (i or 0) + (o or 0) + (ca or 0)
        per_call = (ca or 0) / c if c else 0
        print(f"{fmt(tot):>7} | rows {rows:>4} | calls {c or 0:>6} | ~{per_call/1e3:.0f}k ctx/call | {t}")


if __name__ == "__main__":
    main()
