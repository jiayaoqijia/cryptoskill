"""
Fetch Smart Money netflows on Solana — find what funds are accumulating/distributing.

Cost: 5 credits per call. With per_page=1000 one call is usually enough for top tokens.

Usage:
    NANSEN_API_KEY=... python smart_money_flows.py [solana|ethereum|all] [days=7]
"""
import os, sys, json
import httpx

API = "https://api.nansen.ai"
KEY = os.environ["NANSEN_API_KEY"]
HEADERS = {"apiKey": KEY, "Content-Type": "application/json"}


def main(chain: str = "solana", days: int = 7):
    # Map days → sort field
    sort_field = {1: "net_flow_24h_usd", 7: "net_flow_7d_usd", 30: "net_flow_30d_usd"}.get(days, "net_flow_7d_usd")

    body = {
        "chains": [chain] if chain != "all" else ["all"],
        "filters": {
            "include_smart_money_labels": ["Fund", "Smart Trader"],
            "market_cap_usd": {"min": 1_000_000},  # filter dust tokens
            "include_stablecoins": False,
            "include_native_tokens": False,
        },
        "pagination": {"page": 1, "per_page": 100},
        "order_by": [{"field": sort_field, "direction": "DESC"}],
    }

    r = httpx.post(f"{API}/api/v1/smart-money/netflow", headers=HEADERS, json=body, timeout=60)
    print(f"Credits used: {r.headers.get('X-Nansen-Credits-Used')}")
    print(f"Credits remaining: {r.headers.get('X-Nansen-Credits-Remaining')}")
    r.raise_for_status()
    data = r.json()

    print(f"\nTop accumulating tokens ({chain}, {days}d):")
    print(f"{'Symbol':<12}{'Net flow USD':>15}{'Traders':>10}{'Age(d)':>8}  {'Sectors'}")
    for row in data["data"][:30]:
        sectors = ",".join(row.get("token_sectors", []))[:30]
        print(f"{row['token_symbol']:<12}"
              f"{row[sort_field]:>15,.0f}"
              f"{row['trader_count']:>10}"
              f"{row['token_age_days']:>8}  {sectors}")


if __name__ == "__main__":
    chain = sys.argv[1] if len(sys.argv) > 1 else "solana"
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    main(chain, days)
