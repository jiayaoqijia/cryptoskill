"""api-audit.py — Audit any GenTech x402/API service for dead or placeholder endpoints.

Encodes the API health-audit pattern (discovered Aug 3, 2026): probe every
live service, report status + body length + snippet, and FLAG endpoints that
return hardcoded placeholder data (zeros / empty stubs) — those can't earn
revenue even if a client pays the x402 challenge.

Usage:
    python3 api-audit.py                 # audit all services defined in TARGETS
    python3 api-audit.py --url http://localhost:8080/v1/price/BTC   # single probe
    python3 api-audit.py --health-only   # just check health endpoints

Output flags:
    ✅ HEALTHY  — real data / proper 402 payment challenge
    ❌ PLACEHOLDER — returns hardcoded zeros/empty (fix these first)
    ⚠️  STUB      — empty array/dict shell
    🔗 REDIRECT  — 3xx (follow with --follow)

Why it matters: a placeholder API returns garbage even when paid, so it sits
on the Bazaar/registry looking live but cannot convert. Auditing is the
first step to closing dead revenue surface.
"""
import json
import sys
import subprocess
import argparse
import urllib.request
import urllib.error

# Default targets: (name, url, expected_kind)
#   kind: "data" -> should return real data or 402 challenge
#         "health" -> just /v1/health
TARGETS = [
    ("deal-tracker /v1/deals", "http://localhost:8080/v1/deals?title=Gears", "data"),
    ("crypto-price /v1/price/BTC", "http://localhost:8082/v1/price/BTC", "data"),
    ("gas-price /v1/gas", "http://localhost:8084/v1/gas", "data"),
    ("token-security /v1/score/mint", "http://localhost:8086/v1/score/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "data"),
    ("rugcheck /v1/stats", "http://localhost:8088/v1/stats", "data"),
    ("x402 /status", "http://localhost:8090/status", "data"),
]

# Placeholder signals that indicate an endpoint returns junk.
# NOTE: match exact zero values (`:0}`, `:0,`, `:0 `) NOT `:0.xx` which is real.
PLACEHOLDER_TOKENS = [
    '"source":"placeholder"',
    '"source": "placeholder"',
    '"price":0}',
    '"price":0,',
    '"price": 0}',
    '"price": 0,',
    '"score":0}',
    '"score":0,',
    '"score": 0}',
    '"score": 0,',
    '"level":"unknown"',
    '"ethereum":0}',
    '"ethereum":0,',
    '"ethereum": 0}',
    '"ethereum": 0,',
    '"base":0}',
    '"base":0,',
    '"polygon":0}',
    '"polygon":0,',
    '"deals":[]',
    '"deals": []',
    '"watches":[]',
    '"risk_factors":{}',
]


def classify(body: str, status: int) -> str:
    """Classify an endpoint response as HEALTHY / PLACEHOLDER / STUB / REDIRECT."""
    if status >= 300 and status < 400:
        return "🔗 REDIRECT"
    if status >= 400:
        # 402 payment challenge is HEALTHY for a paid endpoint.
        if status == 402:
            return "✅ HEALTHY (402 payment challenge)"
        return f"⚠️ HTTP {status}"
    if body.startswith("{"):
        try:
            d = json.loads(body)
        except Exception:
            d = None
        if d is not None:
            if "error" in d and "payment_required" in str(d.get("error")):
                return "✅ HEALTHY (402 payment challenge)"
            # Flag placeholders
            for tok in PLACEHOLDER_TOKENS:
                if tok in body:
                    return "❌ PLACEHOLDER"
            # Empty dict shell
            if len(d) == 0:
                return "⚠️ STUB (empty dict)"
    elif body.startswith("["):
        try:
            arr = json.loads(body)
            if len(arr) == 0:
                return "⚠️ STUB (empty array)"
        except Exception:
            pass
    return "✅ HEALTHY"


def probe(name: str, url: str, follow: bool = False):
    """Probe a single URL and print a classified result."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        body = resp.read().decode()
        status = resp.getcode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        status = e.code
    except Exception as e:
        print(f"  {name:<42} ❌ ERROR: {e}")
        return

    kind = classify(body, status)
    snippet = body.replace("\n", " ")[:150]
    print(f"  {name:<42} HTTP:{status} len:{len(body)} | {kind}")
    if snippet and status != 402:
        print(f"      {snippet}")


def main():
    ap = argparse.ArgumentParser(description="Audit GenTech APIs for dead/placeholder endpoints.")
    ap.add_argument("--url", help="Probe a single URL")
    ap.add_argument("--follow", action="store_true", help="Follow 3xx redirects")
    ap.add_argument("--health-only", action="store_true", help="Only check health endpoints")
    args = ap.parse_args()

    if args.url:
        print(f"Probing {args.url}")
        probe("single", args.url, follow=args.follow)
        return

    print("===== GenTech API Health Audit =====")
    print("(❌ PLACEHOLDER = returns junk, fix first | ⚠️ STUB = empty shell)\n")
    for name, url, kind in TARGETS:
        if args.health_only and kind != "health":
            continue
        print(f"● {name}")
        probe(name, url, follow=args.follow)

    print("\nLegend:")
    print("  ✅ HEALTHY  — returns real data or a proper 402 payment challenge")
    print("  ❌ PLACEHOLDER — hardcoded zeros/empty (cannot earn even when paid)")
    print("  ⚠️  STUB      — empty array/dict shell")
    print("  🔗 REDIRECT  — 3xx (re-run with --follow)")
    print("\nFix pattern: replace placeholder bodies with a real data source "
          "(CoinGecko/Etherscan/working internal engine), add a test, restart the service, re-audit.")


if __name__ == "__main__":
    main()
