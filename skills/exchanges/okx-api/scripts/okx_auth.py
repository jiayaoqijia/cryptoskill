"""
OKX API v5 — Reusable auth/request helper.

Usage:
    from okx_auth import make_request

    # GET with query params
    data = make_request("GET", "/api/v5/account/balance", params={"ccy": "USDT"})

    # POST with body
    data = make_request("POST", "/api/v5/trade/order", body={
        "instId": "BTC-USDT",
        "tdMode": "cash",
        "side": "buy",
        "ordType": "limit",
        "px": "42000",
        "sz": "0.001",
    })

Environment variables required for private endpoints:
    OKX_API_KEY       — your API key
    OKX_SECRET_KEY    — your secret key
    OKX_PASSPHRASE    — your passphrase
    OKX_DEMO          — set to "1" to enable simulated trading (sandbox)
"""

import hashlib
import hmac
import json
import os
from base64 import b64encode
from datetime import datetime, timezone
from urllib.parse import urlencode

import requests

BASE_URL = "https://www.okx.com"


def _timestamp() -> str:
    """ISO 8601 UTC timestamp with millisecond precision."""
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


def _sign(secret: str, timestamp: str, method: str, path: str, body: str) -> str:
    pre_sign = timestamp + method.upper() + path + body
    mac = hmac.new(secret.encode(), pre_sign.encode(), hashlib.sha256)
    return b64encode(mac.digest()).decode()


def make_request(
    method: str,
    path: str,
    params: dict | None = None,
    body: dict | None = None,
) -> list | dict:
    """
    Make an authenticated OKX API v5 request.

    Args:
        method: "GET" or "POST"
        path:   API path, e.g. "/api/v5/account/balance"
        params: Query parameters (GET only — appended to path for signing)
        body:   Request body as dict (POST only — serialized as JSON)

    Returns:
        Parsed JSON `data` field from the response.

    Raises:
        RuntimeError: If the API returns a non-zero error code.
        requests.HTTPError: If the HTTP request itself fails.
    """
    method = method.upper()
    api_key = os.environ.get("OKX_API_KEY", "")
    secret = os.environ.get("OKX_SECRET_KEY", "")
    passphrase = os.environ.get("OKX_PASSPHRASE", "")
    demo = os.environ.get("OKX_DEMO", "0") == "1"

    # Build full path including query string (needed for signing)
    query_string = ""
    if params:
        query_string = "?" + urlencode(params)
    full_path = path + query_string

    # Serialize body
    body_str = ""
    if body and method == "POST":
        body_str = json.dumps(body)

    timestamp = _timestamp()

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": _sign(secret, timestamp, method, full_path, body_str),
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase,
    }

    if method == "POST":
        headers["Content-Type"] = "application/json"

    if demo:
        headers["x-simulated-trading"] = "1"

    url = BASE_URL + full_path
    response = requests.request(
        method,
        url,
        headers=headers,
        data=body_str if method == "POST" else None,
        timeout=10,
    )
    response.raise_for_status()

    result = response.json()
    code = result.get("code", "-1")
    if code != "0":
        raise RuntimeError(
            f"OKX API error {code}: {result.get('msg', 'unknown error')}\n"
            f"Full response: {json.dumps(result, indent=2)}"
        )

    return result.get("data", result)


if __name__ == "__main__":
    # Quick smoke test: fetch account balance
    import sys

    print("Testing OKX API connection...")
    try:
        data = make_request("GET", "/api/v5/account/balance")
        print("Success! Account details:")
        for item in data:
            total_eq = item.get("totalEq", "N/A")
            print(f"  Total equity (USD): {total_eq}")
            for detail in item.get("details", [])[:5]:
                ccy = detail.get("ccy")
                eq = detail.get("eq")
                if float(eq or 0) > 0:
                    print(f"    {ccy}: {eq}")
    except RuntimeError as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)
