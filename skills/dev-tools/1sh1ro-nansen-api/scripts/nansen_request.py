#!/usr/bin/env python3
"""Configurable Nansen HTTP request client."""

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
    parser = argparse.ArgumentParser(description="Call Nansen API")
    parser.add_argument("path", help="Endpoint path, e.g. /health")
    parser.add_argument("--method", choices=["GET", "POST"], default="GET")
    parser.add_argument("--base-url", default=os.environ.get("NANSEN_BASE_URL", "https://api.nansen.ai"))
    parser.add_argument("--param", action="append", default=[], type=parse_kv)
    parser.add_argument("--header", action="append", default=[], type=parse_kv)
    parser.add_argument("--json", help="JSON body for POST")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("NANSEN_API_KEY")
    if not api_key:
        print("NANSEN_API_KEY is required", file=sys.stderr)
        return 2

    # Nansen docs typically use `apikey`; keep override for account-specific variants.
    api_key_header = os.environ.get("NANSEN_API_KEY_HEADER", "apikey")
    path = args.path if args.path.startswith("/") else f"/{args.path}"
    url = f"{args.base_url.rstrip('/')}{path}"
    if args.param:
        url = f"{url}?{urllib.parse.urlencode(args.param)}"

    headers = {
        "Accept": "application/json",
        "User-Agent": "nansen-skill/1.0",
        api_key_header: api_key,
    }
    for k, v in args.header:
        headers[k] = v

    data = None
    if args.method == "POST":
        payload = json.loads(args.json) if args.json else {}
        data = json.dumps(payload).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")

    req = urllib.request.Request(url, data=data, headers=headers, method=args.method)

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
