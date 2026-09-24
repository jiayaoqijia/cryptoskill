#!/usr/bin/env python3
"""Minimal Coinglass GET client."""

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
    parser = argparse.ArgumentParser(description="Call Coinglass Open API")
    parser.add_argument("endpoint", help="Example: futures/funding-rate/history")
    parser.add_argument("--base-url", default=os.environ.get("COINGLASS_BASE_URL", "https://open-api-v4.coinglass.com/api"))
    parser.add_argument("--param", action="append", default=[], type=parse_kv)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("COINGLASS_API_KEY")
    if not api_key:
        print("COINGLASS_API_KEY is required", file=sys.stderr)
        return 2

    endpoint = args.endpoint.lstrip("/")
    url = f"{args.base_url.rstrip('/')}/{endpoint}"
    if args.param:
        url = f"{url}?{urllib.parse.urlencode(args.param)}"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "coinglass-skill/1.0",
            "CG-API-KEY": api_key,
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
