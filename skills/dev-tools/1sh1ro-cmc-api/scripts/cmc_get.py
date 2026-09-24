#!/usr/bin/env python3
"""Minimal CMC GET client."""

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
    parser = argparse.ArgumentParser(description="Call CMC API")
    parser.add_argument("path", help="Example: /global-metrics/quotes/latest")
    parser.add_argument("--base-url", default="https://pro-api.coinmarketcap.com/v1")
    parser.add_argument("--param", action="append", default=[], type=parse_kv)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("CMC_API_KEY") or os.environ.get("CMC_PRO_API_KEY")
    if not api_key:
        print("CMC_API_KEY or CMC_PRO_API_KEY is required", file=sys.stderr)
        return 2

    path = args.path if args.path.startswith("/") else f"/{args.path}"
    url = f"{args.base_url.rstrip('/')}{path}"
    if args.param:
        url = f"{url}?{urllib.parse.urlencode(args.param)}"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "cmc-skill/1.0",
            "X-CMC_PRO_API_KEY": api_key,
        },
        method="GET",
    )

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
