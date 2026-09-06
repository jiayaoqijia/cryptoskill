"""
Fetch complete wallet tx history using Helius Enhanced Transactions API.

`getTransactionsForAddress` (Helius) is preferred over standard `getSignaturesForAddress`
because it includes token-account activity and returns parsed/labeled data.

Requires a Helius RPC URL. For non-Helius providers, fall back to getSignaturesForAddress
+ batched getTransaction (see fetch_tx_batch.py).

Usage:
    SOLANA_RPC_URL=https://mainnet.helius-rpc.com/?api-key=YOUR_KEY \\
        python wallet_full_history.py <wallet> out.jsonl [limit_per_page=100] [max_pages=50]
"""
import os, sys, json, time
import httpx

RPC_URL = os.environ["SOLANA_RPC_URL"]

if "helius-rpc.com" not in RPC_URL:
    print("WARNING: This script uses Helius Enhanced Transactions API.")
    print("Your SOLANA_RPC_URL is not a Helius endpoint. Script will fail.")
    print("For non-Helius: use fetch_tx_batch.py with output of getSignaturesForAddress.")
    sys.exit(1)


def get_transactions_for_address(address: str, before: str | None = None, limit: int = 100) -> list:
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransactionsForAddress",
        "params": [
            address,
            {
                "limit": limit,
                "before": before,
                "commitment": "confirmed",
            },
        ],
    }
    r = httpx.post(RPC_URL, json=body, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data.get("result") or []


def main(wallet: str, out_path: str, limit: int = 100, max_pages: int = 50):
    before = None
    total = 0
    # Resume: read last-stored sig and use as starting cursor
    if os.path.exists(out_path):
        with open(out_path) as f:
            lines = f.readlines()
        if lines:
            last = json.loads(lines[-1])
            before = last.get("signature")
            total = len(lines)
            print(f"Resuming from signature {before[:16]}…, already have {total} txs")

    with open(out_path, "a") as f:
        for page in range(max_pages):
            txs = get_transactions_for_address(wallet, before=before, limit=limit)
            if not txs:
                print(f"Page {page + 1}: empty, done.")
                break
            for tx in txs:
                f.write(json.dumps(tx) + "\n")
            f.flush()
            total += len(txs)
            before = txs[-1].get("signature")
            print(f"Page {page + 1}: +{len(txs)} txs (total: {total})")
            if len(txs) < limit:
                print("Last page (short response)")
                break
            time.sleep(0.1)  # gentle throttle

    print(f"Done: {total} txs → {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    wallet = sys.argv[1]
    out = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    max_pages = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    main(wallet, out, limit, max_pages)
