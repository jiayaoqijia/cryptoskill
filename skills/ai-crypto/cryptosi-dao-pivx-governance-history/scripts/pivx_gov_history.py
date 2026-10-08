#!/usr/bin/env python3
"""PIVX governance history extractor. stdlib only. Python 3.8+.

Subcommands:
  proposals      Parse all past proposals (passed + failed) from pivx.org/proposals/past
                 plus current-cycle rows from pivx.org/proposals. Outputs JSON.
  date-threads   Fetch forum thread start dates for proposals missing them (adds thread_date).
  superblocks    Scan a block-height range on explorer.pivx.org for superblock payout txs.
  cycles         Group proposals into monthly cycles using superblock receipts + thread dates.

Examples:
  python3 pivx_gov_history.py proposals --out gov.json
  python3 pivx_gov_history.py date-threads --gov gov.json --out gov_dated.json --limit 60
  python3 pivx_gov_history.py superblocks --from-height 5586500 --to-height 5587100
  python3 pivx_gov_history.py cycles --gov gov_dated.json --out cycles.json
"""
import argparse
import html as html_mod
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
PAST_URL = "https://pivx.org/proposals/past"
CURRENT_URL = "https://pivx.org/proposals"
EXPLORER = "https://explorer.pivx.org/api/v2"


def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def get_json(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def strip_tags(s):
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def parse_rows(page):
    """Extract proposal rows from a pivx.org proposals page (past or current)."""
    out = []
    for m in re.finditer(r'<tr data-hash="([0-9a-f]+)" data-title="([^"]+)">(.*?)</tr>', page, re.S):
        g_hash, name, row = m.group(1), m.group(2), m.group(3)
        tds = re.findall(r"<td([^>]*)>(.*?)</td>", row, re.S)
        if len(tds) < 3:
            continue
        cells = [t[1] for t in tds]
        status_m = re.search(r'<b>\s*(Passing|Failing)', cells[0], re.I)
        status = None
        if status_m:
            status = "PASSING" if status_m.group(1).lower() == "passing" else "FAILING"
        else:
            st = strip_tags(cells[0]).lower()
            status = "PASSING" if "passing" in st else ("FAILING" if "failing" in st else None)
        link_m = re.search(r'href="(https://forum\.pivx\.org/threads/[^"]+|https?://[^"]+)"', cells[1])
        forum_url = link_m.group(1) if link_m else None
        thread_id_m = re.search(r"/threads/[^.?]+\.(\d+)", forum_url or "")
        thread_id = thread_id_m.group(1) if thread_id_m else None
        amt_m = re.search(r'data-order="([0-9.]+)"', tds[2][0]) if len(tds) > 2 else None
        amount_piv = float(amt_m.group(1)) if amt_m else None
        usd_m = re.search(r"US\$\s*([0-9,]+\.?[0-9]*)", cells[2]) if len(cells) > 2 else None
        usd = float(usd_m.group(1).replace(",", "")) if usd_m else None
        votes = {"yes": None, "no": None, "net_pct": None}
        net_m = re.search(r'data-order="(-?[0-9.]+)"', tds[0][0])
        if net_m:
            votes["net_pct"] = round(float(net_m.group(1)) * 100, 1)
        for c in cells[3:]:
            v = re.search(r"([0-9.]+)%\s*([0-9,]+)\s*/\s*([0-9,]+)", strip_tags(c))
            if v:
                votes = {
                    "net_pct": float(v.group(1)),
                    "yes": int(v.group(2).replace(",", "")),
                    "no": int(v.group(3).replace(",", "")),
                }
                break
        funded = "(FUNDED)" in cells[0] or "funded" in cells[0].lower()
        out.append({
            "name": name,
            "status": status,
            "funded_now": funded,
            "amount_piv": amount_piv,
            "amount_usd_at_capture": usd,
            "votes": votes,
            "forum_url": forum_url,
            "thread_id": thread_id,
            "proposal_hash": g_hash,
            "cycle": None,
            "thread_date": None,
        })
    return out


def cmd_proposals(args):
    past = parse_rows(http_get(PAST_URL))
    current = parse_rows(http_get(CURRENT_URL))
    for r in past:
        r["source"] = "past"
    for r in current:
        r["source"] = "current"
    result = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "past_count": len(past),
        "current_count": len(current),
        "proposals": past + current,
    }
    txt = json.dumps(result, indent=1)
    if args.out:
        open(args.out, "w").write(txt)
        print(f"wrote {args.out}: {len(past)} past + {len(current)} current")
    else:
        print(txt)


def cmd_date_threads(args):
    gov = json.load(open(args.gov))
    props = gov["proposals"]
    todo = [p for p in props if p.get("forum_url") and "forum.pivx.org" in p["forum_url"]]
    if args.limit:
        todo = todo[: args.limit]
    session_cache = {}
    for i, p in enumerate(todo):
        u = p["forum_url"]
        try:
            if u not in session_cache:
                h = http_get(u)
                m = re.search(r'datetime="([0-9T:+\-]+)"', h)
                session_cache[u] = m.group(1) if m else None
                time.sleep(0.4)
            p["thread_date"] = session_cache[u]
        except Exception as e:
            p["thread_date_error"] = str(e)[:80]
    if args.out:
        json.dump(gov, open(args.out, "w"), indent=1)
        print(f"wrote {args.out}; dated {sum(1 for p in props if p.get('thread_date'))}")
    else:
        print(json.dumps(gov, indent=1))


def cmd_superblocks(args):
    """Scan [from,to] block range for superblock payout transactions.

    Heuristic: tx with >=2 DISTINCT recipient addresses, each single output
    >= 15,000 PIV, tx total >= 100,000 PIV. Consolidator sweeps (one address,
    many same-size outputs) are excluded.
    """
    base = EXPLORER

    def check(h):
        try:
            bh = get_json(f"{base}/block-index/{h}")["blockHash"]
            b = get_json(f"{base}/block/{bh}")
            hits = []
            for tx in b.get("txs", []):
                pays = {}
                for o in tx.get("vout", []):
                    v, a = o.get("value"), o.get("addresses")
                    if v and a and float(v) >= 15000e8:
                        pays.setdefault(a[0], 0.0)
                        pays[a[0]] += float(v)
                if len(pays) >= 2 and sum(pays.values()) > 100000e8:
                    hits.append({
                        "height": b["height"],
                        "time_utc": time.strftime("%Y-%m-%d %H:%M", time.gmtime(b["time"])),
                        "txid": tx["txid"],
                        "payees": {k: round(v / 1e8) for k, v in pays.items()},
                        "total_piv": round(sum(pays.values()) / 1e8),
                    })
            return hits
        except Exception:
            return []

    hits = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for res in ex.map(check, range(args.from_height, args.to_height + 1)):
            if res:
                hits.extend(res)
                print(json.dumps(res), flush=True)
    if args.out:
        json.dump(hits, open(args.out, "w"), indent=1)
        print(f"wrote {args.out} ({len(hits)} payout txs)")


def cmd_cycles(args):
    gov = json.load(open(args.gov))
    sbs = json.load(open(args.superblocks)) if args.superblocks else []
    props = gov["proposals"]
    # Bucket proposals by thread month as a first pass
    for p in props:
        d = p.get("thread_date") or ""
        p["cycle"] = d[:7] if d else None
    result = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "superblock_receipts": sbs,
        "by_cycle": {},
    }
    for p in props:
        result["by_cycle"].setdefault(p["cycle"] or "unknown", []).append({
            k: p[k] for k in ("name", "status", "amount_piv", "votes", "forum_url")
        })
    if args.out:
        json.dump(result, open(args.out, "w"), indent=1)
        print(f"wrote {args.out}; cycles: {sorted(result['by_cycle'])}")
    else:
        print(json.dumps(result, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("proposals")
    p.add_argument("--out")
    p.set_defaults(func=cmd_proposals)

    p = sub.add_parser("date-threads")
    p.add_argument("--gov", required=True)
    p.add_argument("--out")
    p.add_argument("--limit", type=int, default=0)
    p.set_defaults(func=cmd_date_threads)

    p = sub.add_parser("superblocks")
    p.add_argument("--from-height", type=int, required=True)
    p.add_argument("--to-height", type=int, required=True)
    p.add_argument("--workers", type=int, default=12)
    p.add_argument("--out")
    p.set_defaults(func=cmd_superblocks)

    p = sub.add_parser("cycles")
    p.add_argument("--gov", required=True)
    p.add_argument("--superblocks")
    p.add_argument("--out")
    p.set_defaults(func=cmd_cycles)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
