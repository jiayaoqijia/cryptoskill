#!/usr/bin/env python3
"""Minimal Alternative.me GET client."""

import argparse
import json
import os
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
    parser = argparse.ArgumentParser(description="Call Alternative.me API")
    parser.add_argument("endpoint", help="Example: fng")
    parser.add_argument("--base-url", default=os.environ.get("ALTERNATIVE_ME_BASE_URL", "https://api.alternative.me"))
    parser.add_argument("--param", action="append", default=[], type=parse_kv)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    endpoint = args.endpoint.strip("/")
    url = f"{args.base_url.rstrip('/')}/{endpoint}/"
    if args.param:
        url = f"{url}?{urllib.parse.urlencode(args.param)}"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "alternative-me-skill/1.0",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as err:
        print(err.read().decode("utf-8", "ignore"))
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
