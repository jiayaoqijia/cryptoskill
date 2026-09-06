"""
Fetch transaction details for many signatures using /transaction/detail/multi.

This saves 50× CU vs calling /transaction/detail once per signature:
    Naive: N × 100 CU
    Multi: ceil(N / 50) × 100 CU

Usage:
    SOLSCAN_API_KEY=... python batch_tx_details.py signatures.txt out.jsonl
"""
import asyncio, aiohttp, os, json, sys

BASE = "https://pro-api.solscan.io/v2.0"
KEY = os.environ["SOLSCAN_API_KEY"]
HEADERS = {"token": KEY}
SEMAPHORE = asyncio.Semaphore(50)
BATCH = 50  # max per multi call
MAX_RETRIES = 5


async def call_multi(session, signatures: list[str]) -> list:
    # pass tx as repeated query param
    params = [("tx", s) for s in signatures]
    async with SEMAPHORE:
        for attempt in range(MAX_RETRIES):
            async with session.get(f"{BASE}/transaction/detail/multi", params=params) as r:
                if r.status == 429:
                    await asyncio.sleep(2 ** attempt)
                    continue
                r.raise_for_status()
                data = await r.json()
                return data.get("data") or []
        raise RuntimeError("429 retries exceeded")


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def load_done(path: str) -> set[str]:
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                try:
                    done.add(json.loads(line)["tx_hash"])
                except Exception:
                    pass
    return done


async def main(signatures: list[str], out_path: str):
    done = load_done(out_path)
    todo = [s for s in signatures if s not in done]
    print(f"Total: {len(signatures)}, done: {len(done)}, todo: {len(todo)}")
    print(f"CU cost (multi): {len(todo) // BATCH + 1} × 100 = {(len(todo) // BATCH + 1) * 100}")
    print(f"CU cost (naive): {len(todo) * 100}")

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [call_multi(session, batch) for batch in chunks(todo, BATCH)]
        with open(out_path, "a") as f:
            for i, coro in enumerate(asyncio.as_completed(tasks), 1):
                rows = await coro
                for row in rows:
                    f.write(json.dumps(row) + "\n")
                f.flush()
                print(f"[{i}] wrote {len(rows)} tx details")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    sigs_file = sys.argv[1]
    out = sys.argv[2]
    sigs = [s.strip() for s in open(sigs_file) if s.strip()]
    asyncio.run(main(sigs, out))
