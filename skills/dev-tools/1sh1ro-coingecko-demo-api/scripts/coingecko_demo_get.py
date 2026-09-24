#!/usr/bin/env python3
"""Minimal CoinGecko Demo GET client."""

import argparse
import json
import os
import sys
import time
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


def build_url(base_url: str, endpoint: str, params):
    endpoint = endpoint.lstrip("/")
    url = f"{base_url.rstrip('/')}/{endpoint}"
    if params:
        query = urllib.parse.urlencode(params)
        url = f"{url}?{query}"
    return url


def run_get(req: urllib.request.Request, retries: int, backoff: float, timeout: float):
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.getcode(), resp.headers, resp.read()
        except urllib.error.HTTPError:
            raise
        except urllib.error.URLError:
            if attempt >= retries:
                raise
            time.sleep(backoff * (2 ** attempt))


def main() -> int:
    parser = argparse.ArgumentParser(description="Call CoinGecko Demo/Public API")
    parser.add_argument("endpoint", help="Example: global or coins/markets")
    parser.add_argument("--base-url", default=os.environ.get("COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3"))
    parser.add_argument("--param", action="append", default=[], type=parse_kv)
    parser.add_argument("--header", action="append", default=[], type=parse_kv)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--backoff", type=float, default=1.0)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    headers = {"Accept": "application/json", "User-Agent": "coingecko-demo-skill/1.0"}
    key = os.environ.get("COINGECKO_API_KEY")
    if key:
        headers["x-cg-demo-api-key"] = key

    for k, v in args.header:
        headers[k] = v

    url = build_url(args.base_url, args.endpoint, args.param)
    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        status, resp_headers, body = run_get(req, args.retries, args.backoff, args.timeout)
    except urllib.error.HTTPError as err:
        text = err.read().decode("utf-8", "ignore")
        print(text)
        return 1
    except Exception as err:
        print(f"Request failed: {err}", file=sys.stderr)
        return 1

    text = body.decode("utf-8", "ignore")
    if args.pretty and "application/json" in resp_headers.get("Content-Type", ""):
        try:
            text = json.dumps(json.loads(text), ensure_ascii=False, indent=2)
        except Exception:
            pass

    print(text)
    return 0 if status == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main())
