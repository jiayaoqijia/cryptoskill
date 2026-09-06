"""
Fetch Solscan DeFi activities for N wallets, async with resume support.

Usage:
    SOLSCAN_API_KEY=... python fetch_defi_activities.py wallets.txt out.jsonl [days]

Produces one JSONL line per wallet:
    {"wallet": "<addr>", "activities": [...]}

Resume: re-running skips wallets already present in out.jsonl.

Tuning:
    SEMAPHORE=25  — safe for Tier 2 (1000/min)
    PAGE_SIZE=100 — maximum allowed
"""
import asyncio, aiohttp, os, json, sys, time
from typing import List

BASE = "https://pro-api.solscan.io/v2.0"
KEY = os.environ["SOLSCAN_API_KEY"]
HEADERS = {"token": KEY}
SEMAPHORE = asyncio.Semaphore(25)
PAGE_SIZE = 100
MAX_RETRIES = 5


async def call(session, path, params):
    async with SEMAPHORE:
        for attempt in range(MAX_RETRIES):
            async with session.get(f"{BASE}{path}", params=params) as r:
                if r.status == 429:
                    await asyncio.sleep(2 ** attempt)
                    continue
                r.raise_for_status()
                return await r.json()
        raise RuntimeError(f"429 retries exceeded for {path} {params}")


async def fetch_wallet(session, wallet: str, from_time: int) -> tuple[str, list]:
    """Fetch all defi activities for one wallet since from_time."""
    rows, page = [], 1
    while True:
        data = await call(session, "/account/defi/activities", {
            "address": wallet,
            "page": page,
            "page_size": PAGE_SIZE,
            "sort_by": "block_time",
            "sort_order": "desc",
            "from_time": from_time,
        })
        batch = data.get("data") or []
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        page += 1
    return wallet, rows


def load_done(path: str) -> set[str]:
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                try:
                    done.add(json.loads(line)["wallet"])
                except Exception:
                    pass
    return done


async def main(wallets: List[str], out_path: str, days: int):
    from_time = int(time.time()) - days * 86400
    done = load_done(out_path)
    todo = [w for w in wallets if w not in done]
    print(f"Total: {len(wallets)}, done: {len(done)}, todo: {len(todo)}")

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        # Check budget
        usage = await call(session, "/monitor/usage", {})
        print(f"CU budget: {usage}")

        tasks = [fetch_wallet(session, w, from_time) for w in todo]
        with open(out_path, "a") as f:
            for i, coro in enumerate(asyncio.as_completed(tasks), 1):
                wallet, rows = await coro
                f.write(json.dumps({"wallet": wallet, "activities": rows}) + "\n")
                f.flush()
                print(f"[{i}/{len(todo)}] {wallet[:8]}…: {len(rows)} activities")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    wallets_file = sys.argv[1]
    out = sys.argv[2]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    wallets = [w.strip() for w in open(wallets_file) if w.strip()]
    asyncio.run(main(wallets, out, days))
