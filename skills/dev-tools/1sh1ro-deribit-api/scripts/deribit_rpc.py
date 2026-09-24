#!/usr/bin/env python3
"""Minimal Deribit JSON-RPC client."""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request


def parse_kv(value: str):
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected KEY=VALUE")
    key, val = value.split("=", 1)
    if not key:
        raise argparse.ArgumentTypeError("Empty key")
    return key, val


def coerce(v: str):
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    try:
        if "." in v:
            return float(v)
        return int(v)
    except Exception:
        return v


def main() -> int:
    parser = argparse.ArgumentParser(description="Call Deribit JSON-RPC API")
    parser.add_argument("method", help="Example: public/ticker")
    parser.add_argument("--endpoint", default="https://www.deribit.com/api/v2")
    parser.add_argument("--param", action="append", default=[], type=parse_kv)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    params = {k: coerce(v) for k, v in args.param}
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000) % 1_000_000_000,
        "method": args.method,
        "params": params,
    }

    req = urllib.request.Request(
        args.endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "deribit-skill/1.0",
        },
        method="POST",
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
