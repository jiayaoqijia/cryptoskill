#!/usr/bin/env python3
"""Minimal Glassnode GET client."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def parse_kv(value: str):
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected KEY=VALUE")
    key, val = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("Empty key")
    return key, val


def main() -> int:
    parser = argparse.ArgumentParser(description="Call Glassnode API")
    parser.add_argument("path", help="Example: /v1/metrics/market/price_usd_close")
    parser.add_argument("--base-url", default=os.environ.get("GLASSNODE_BASE_URL", "https://api.glassnode.com"))
    parser.add_argument("--param", action="append", default=[], type=parse_kv)
    parser.add_argument("--auth-mode", choices=["query", "header"], default="query")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("GLASSNODE_API_KEY")
    if not api_key:
        print("GLASSNODE_API_KEY is required", file=sys.stderr)
        return 2

    path = args.path if args.path.startswith("/") else f"/{args.path}"
    params = dict(args.param)
    headers = {
        "Accept": "application/json",
        "User-Agent": "glassnode-skill/1.0",
    }
    if args.auth_mode == "query":
        params.setdefault("api_key", api_key)
    else:
        headers["X-Api-Key"] = api_key

    url = f"{args.base_url.rstrip('/')}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as err:
        print(err.read().decode("utf-8", "ignore"))
        return 1
    except Exception as err:
        print(f"Request failed: {err}", file=sys.stderr)
        return 1

    if args.pretty:
        try:
            print(json.dumps(json.loads(text), ensure_ascii=False, indent=2))
            return 0
        except Exception:
            pass
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
