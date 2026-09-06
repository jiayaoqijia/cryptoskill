#!/usr/bin/env python3
"""
Gate DEX OpenAPI call wrapper.
Handles HMAC-SHA256 signing automatically — the LLM only needs to provide action + params.

Usage:
    python3 gate-api-call.py <action> [params_json]

Examples:
    python3 gate-api-call.py "trade.swap.chain" "{}"
    python3 gate-api-call.py "trade.swap.quote" '{"chain_id":1,"token_in":"-","token_out":"0xdAC...","amount_in":"0.1"}'
    python3 gate-api-call.py "base.token.get_base_info" '{"chain":"eth","token_address":"0x..."}'

Config: Reads AK/SK from ~/.gate-dex-openapi/config.json
Output: JSON response body to stdout
Exit:   0 on success, 1 on error
"""

import hashlib
import hmac
import base64
import json
import sys
import time
import uuid
import os

try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    print(json.dumps({"error": "Python urllib not available"}), file=sys.stderr)
    sys.exit(1)

API_URL = "https://openapi.gateweb3.cc/api/v1/dex"
CONFIG_PATH = os.path.expanduser("~/.gate-dex-openapi/config.json")

# Default public credentials (basic tier, 2 QPS)
DEFAULT_AK = "7RAYBKMG5MNMKK7LN6YGCO5UDI"
DEFAULT_SK = "COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h"


def load_credentials():
    """Load AK/SK from config file, fallback to defaults."""
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        ak = config.get("api_key", DEFAULT_AK)
        sk = config.get("secret_key", DEFAULT_SK)
        return ak, sk
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_AK, DEFAULT_SK


def sign_request(sk, timestamp, body_str):
    """Compute HMAC-SHA256 signature."""
    prehash = f"{timestamp}/api/v1/dex{body_str}"
    signature = hmac.new(
        sk.encode("utf-8"),
        prehash.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.b64encode(signature).decode("utf-8")


def call_api(action, params):
    """Make signed API call and return response."""
    ak, sk = load_credentials()

    body = {"action": action, "params": params}
    body_str = json.dumps(body, separators=(",", ":"))

    timestamp = str(int(time.time() * 1000))
    signature = sign_request(sk, timestamp, body_str)
    request_id = str(uuid.uuid4())

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ak,
        "X-Timestamp": timestamp,
        "X-Signature": signature,
        "X-Request-Id": request_id,
    }

    req = Request(API_URL, data=body_str.encode("utf-8"), headers=headers, method="POST")

    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}", "detail": error_body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 gate-api-call.py <action> [params_json]", file=sys.stderr)
        sys.exit(1)

    action = sys.argv[1]
    params = {}

    if len(sys.argv) >= 3:
        try:
            params = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid params JSON: {e}"}))
            sys.exit(1)

    result = call_api(action, params)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # Exit with error code if API returned an error
    if isinstance(result, dict) and (result.get("error") or result.get("code", 0) != 0):
        sys.exit(1)


if __name__ == "__main__":
    main()
