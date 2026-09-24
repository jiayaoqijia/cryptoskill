#!/usr/bin/env python3
"""Lightweight CoinGecko API GET client.

Defaults to the public API base URL but can be overridden by env or flags.
"""

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
        raise argparse.ArgumentTypeError("Empty key in KEY=VALUE")
    return key, val


def build_url(base_url: str, endpoint: str, params):
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        url = endpoint
    else:
        base = base_url.rstrip("/")
        path = endpoint.lstrip("/")
        url = f"{base}/{path}"

    if params:
        query = urllib.parse.urlencode(params)
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}{query}"
    return url


def request_with_retries(req: urllib.request.Request, retries: int, backoff: float, timeout: float):
    last_err = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.getcode(), resp.headers, resp.read()
        except urllib.error.HTTPError as err:
            last_err = err
            status = getattr(err, "code", None)
            if status in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(backoff * (2 ** attempt))
                continue
            raise
        except urllib.error.URLError as err:
            last_err = err
            if attempt < retries:
                time.sleep(backoff * (2 ** attempt))
                continue
            raise
    if last_err:
        raise last_err
    raise RuntimeError("Request failed without an explicit error")


def main():
    parser = argparse.ArgumentParser(description="Call CoinGecko API endpoints (GET).")
    parser.add_argument("endpoint", help="Endpoint path (e.g. simple/price) or full URL")
    parser.add_argument("--base-url", default=os.environ.get("COINGECKO_BASE_URL", "https://api.coingecko.com/api/v3"))
    parser.add_argument("--param", action="append", default=[], type=parse_kv, help="Query parameter KEY=VALUE (repeatable)")
    parser.add_argument("--header", action="append", default=[], type=parse_kv, help="Header KEY=VALUE (repeatable)")
    parser.add_argument("--api-key", default=os.environ.get("COINGECKO_API_KEY"), help="API key value (optional)")
    parser.add_argument("--api-key-header", default=os.environ.get("COINGECKO_API_KEY_HEADER", "x-cg-pro-api-key"), help="API key header name")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds")
    parser.add_argument("--retries", type=int, default=2, help="Retries for 429/5xx or transient errors")
    parser.add_argument("--backoff", type=float, default=1.0, help="Backoff base seconds (exponential)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--raw", action="store_true", help="Output raw body without JSON parsing")
    parser.add_argument("--out", help="Write output to file instead of stdout")
    parser.add_argument("--dry-run", action="store_true", help="Print URL and headers without sending")

    args = parser.parse_args()

    params = args.param
    headers = {"Accept": "application/json"}

    for key, val in args.header:
        headers[key] = val

    if args.api_key:
        headers.setdefault(args.api_key_header, args.api_key)

    url = build_url(args.base_url, args.endpoint, params)

    if args.dry_run:
        print("URL:", url)
        print("Headers:")
        for key in sorted(headers):
            print(f"  {key}: {headers[key]}")
        return 0

    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        status, resp_headers, body = request_with_retries(req, args.retries, args.backoff, args.timeout)
    except Exception as err:
        print(f"Request failed: {err}", file=sys.stderr)
        return 1

    content_type = resp_headers.get("Content-Type", "")
    output_text = None

    if not args.raw and "application/json" in content_type:
        try:
            data = json.loads(body.decode("utf-8"))
            if args.pretty:
                output_text = json.dumps(data, indent=2, sort_keys=True)
            else:
                output_text = json.dumps(data)
        except Exception:
            output_text = body.decode("utf-8", errors="replace")
    else:
        output_text = body.decode("utf-8", errors="replace")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output_text)
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
