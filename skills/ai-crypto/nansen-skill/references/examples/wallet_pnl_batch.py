"""
Fetch PnL summary for N wallets (Profiler endpoint, 1 credit each).

For 100 wallets → 100 credits. Cheap by Nansen standards.

Usage:
    NANSEN_API_KEY=... python wallet_pnl_batch.py wallets.txt chain out.jsonl

    wallets.txt: one address per line
    chain: solana | ethereum | base | ...
    out.jsonl: resume-safe JSONL output
"""
import asyncio, aiohttp, os, sys, json

API = "https://api.nansen.ai"
KEY = os.environ["NANSEN_API_KEY"]
HEADERS = {"apiKey": KEY, "Content-Type": "application/json"}
SEMAPHORE = asyncio.Semaphore(15)  # safe under 20/s


async def fetch_pnl(session, address: str, chain: str) -> dict:
    body = {
        "address": address,
        "chains": [chain],
    }
    async with SEMAPHORE:
        for attempt in range(5):
            async with session.post(
                f"{API}/api/v1/profiler/address/pnl-summary",
                headers=HEADERS, json=body
            ) as r:
                if r.status == 429:
                    retry = int(r.headers.get("Retry-After", 2 ** attempt))
                    await asyncio.sleep(retry)
                    continue
                remaining = r.headers.get("X-Nansen-Credits-Remaining")
                if r.status != 200:
                    text = await r.text()
                    return {"address": address, "error": f"{r.status} {text[:200]}"}
                data = await r.json()
                return {
                    "address": address,
                    "chain": chain,
                    "credits_remaining": remaining,
                    "data": data,
                }
        return {"address": address, "error": "max retries"}


def load_done(path: str) -> set[str]:
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                try:
                    done.add(json.loads(line)["address"])
                except Exception:
                    pass
    return done


async def main(wallets: list[str], chain: str, out_path: str):
    done = load_done(out_path)
    todo = [w for w in wallets if w not in done]
    print(f"Total: {len(wallets)}, done: {len(done)}, todo: {len(todo)}")
    print(f"Expected cost: {len(todo)} credits")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pnl(session, w, chain) for w in todo]
        with open(out_path, "a") as f:
            for i, coro in enumerate(asyncio.as_completed(tasks), 1):
                result = await coro
                f.write(json.dumps(result) + "\n")
                f.flush()
                remaining = result.get("credits_remaining", "?")
                print(f"[{i}/{len(todo)}] {result['address'][:8]}… remaining: {remaining}")
                # Safety: stop if credits dangerously low
                try:
                    if int(remaining) < 200:
                        print("⚠️  Credits below 200, stopping batch.")
                        break
                except (ValueError, TypeError):
                    pass


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    wallets = [w.strip() for w in open(sys.argv[1]) if w.strip()]
    chain = sys.argv[2]
    out = sys.argv[3]
    asyncio.run(main(wallets, chain, out))
