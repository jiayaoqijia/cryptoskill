"""
Fetch top holders for a token via TGM holders endpoint.

Cost: 5 credits (10 if Free tier). Avoid setting premium_labels=true (→ 150 credits).

Usage:
    NANSEN_API_KEY=... python token_holders.py <token_address> <chain> [pages=3]
"""
import os, sys, json
import httpx

API = "https://api.nansen.ai"
KEY = os.environ["NANSEN_API_KEY"]
HEADERS = {"apiKey": KEY, "Content-Type": "application/json"}


def fetch_holders(token: str, chain: str, page: int = 1, per_page: int = 1000) -> tuple[list, dict]:
    body = {
        "chains": [chain],
        "token_address": token,
        "pagination": {"page": page, "per_page": per_page},
        # IMPORTANT: don't set "premium_labels": true unless explicitly needed — jumps cost from 5 to 150
    }
    r = httpx.post(f"{API}/api/v1/tgm/holders", headers=HEADERS, json=body, timeout=60)
    return r.json().get("data", []), dict(r.headers)


def main(token: str, chain: str, pages: int = 3):
    all_holders = []
    credits_used_total = 0
    for page in range(1, pages + 1):
        rows, headers = fetch_holders(token, chain, page=page)
        credits_used_total += int(headers.get("X-Nansen-Credits-Used", 0))
        remaining = headers.get("X-Nansen-Credits-Remaining", "?")
        print(f"Page {page}: {len(rows)} holders. Remaining: {remaining}")
        if not rows:
            break
        all_holders.extend(rows)
        if len(rows) < 1000:
            break

    print(f"\nTotal holders fetched: {len(all_holders)}")
    print(f"Total credits used: {credits_used_total}")
    print(f"\n{'Rank':<6}{'Address':<44}{'Amount':>20}{'Value USD':>15}")
    for h in all_holders[:20]:
        print(f"{h.get('rank', '?'):<6}"
              f"{(h.get('address') or '')[:40]:<44}"
              f"{h.get('amount', 0):>20,.2f}"
              f"{h.get('value_usd', 0):>15,.0f}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    token = sys.argv[1]
    chain = sys.argv[2]
    pages = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    main(token, chain, pages)
