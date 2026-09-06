"""
Fetch Solana transactions in JSON-RPC batches of 100.

Works with any Solana RPC provider (Helius, QuickNode, Triton, Ankr, public).
Uses standard JSON-RPC array requests — minimum HTTP overhead.

Usage:
    SOLANA_RPC_URL=... python fetch_tx_batch.py signatures.txt out.jsonl
"""
import asyncio, aiohttp, os, sys, json

RPC_URL = os.environ["SOLANA_RPC_URL"]
BATCH_SIZE = 100
SEMAPHORE = asyncio.Semaphore(15)
MAX_RETRIES = 5

TX_CONFIG = {
    "encoding": "jsonParsed",
    "commitment": "confirmed",
    "maxSupportedTransactionVersion": 0,
}


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


async def post_batch(session, body: list) -> list:
    async with SEMAPHORE:
        for attempt in range(MAX_RETRIES):
            async with session.post(RPC_URL, json=body, timeout=60) as r:
                if r.status == 429:
                    retry = int(r.headers.get("Retry-After", 2 ** attempt))
                    await asyncio.sleep(retry)
                    continue
                r.raise_for_status()
                return await r.json()
        raise RuntimeError("Max retries exceeded")


async def fetch_signatures(session, signatures: list[str]) -> list:
    body = [
        {"jsonrpc": "2.0", "id": i, "method": "getTransaction", "params": [sig, TX_CONFIG]}
        for i, sig in enumerate(signatures)
    ]
    resp = await post_batch(session, body)
    # Keep ordering: body id corresponds to signatures index
    # Response may be out of order — re-order by id
    result_by_id = {item.get("id"): item for item in resp}
    return [
        {
            "signature": sig,
            "result": result_by_id.get(i, {}).get("result"),
            "error": result_by_id.get(i, {}).get("error"),
        }
        for i, sig in enumerate(signatures)
    ]


def load_done(path: str) -> set[str]:
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                try:
                    done.add(json.loads(line)["signature"])
                except Exception:
                    pass
    return done


async def main(sigs: list[str], out_path: str):
    done = load_done(out_path)
    todo = [s for s in sigs if s not in done]
    print(f"Total: {len(sigs)}, done: {len(done)}, todo: {len(todo)}")
    print(f"Batches of {BATCH_SIZE}: {(len(todo) + BATCH_SIZE - 1) // BATCH_SIZE}")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_signatures(session, batch) for batch in chunks(todo, BATCH_SIZE)]
        with open(out_path, "a") as f:
            for i, coro in enumerate(asyncio.as_completed(tasks), 1):
                rows = await coro
                for row in rows:
                    f.write(json.dumps(row) + "\n")
                f.flush()
                errors = sum(1 for r in rows if r.get("error"))
                missing = sum(1 for r in rows if r.get("result") is None and not r.get("error"))
                print(f"[{i}] wrote {len(rows)} rows (errors: {errors}, missing: {missing})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    sigs = [s.strip() for s in open(sys.argv[1]) if s.strip()]
    asyncio.run(main(sigs, sys.argv[2]))
