#!/usr/bin/env python3
"""Minimal Santiment GraphQL client."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Call Santiment GraphQL API")
    parser.add_argument("--url", default=os.environ.get("SANTIMENT_API_URL", "https://api.santiment.net/graphql"))
    parser.add_argument("--query", required=True)
    parser.add_argument("--variables", help="JSON object string")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("SANTIMENT_API_KEY")
    if not api_key:
        print("SANTIMENT_API_KEY is required", file=sys.stderr)
        return 2

    variables = json.loads(args.variables) if args.variables else {}
    payload = {
        "query": args.query,
        "variables": variables,
    }

    req = urllib.request.Request(
        args.url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "santiment-skill/1.0",
            "Authorization": f"Apikey {api_key}",
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
