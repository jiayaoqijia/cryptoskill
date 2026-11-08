#!/usr/bin/env python3
"""Build and optionally execute secure MEXC Futures REST requests."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mexc_common import (  # noqa: E402
    DEFAULT_SENSITIVE_KEYS,
    ensure_no_signed_query,
    format_http_response,
    load_json_params,
    normalize_method,
    normalize_path,
    open_mexc_request,
    read_mexc_credentials,
    redact_headers as redact_auth_headers,
    redact_json_text,
    redact_query_params,
    strip_wrapping_quotes,
    validate_base_url,
    validate_live_execution,
    validate_mexc_request_url,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_URL = "https://api.mexc.com"
AUTHENTICATED_HOSTS = {"api.mexc.com"}
EXAMPLES = "examples: GET /api/v1/contract/ping | GET /api/v1/private/account/assets --signed"
SELF_TEST_ACCESS_KEY = "test-key"
SELF_TEST_SECRET = "test-secret"
SELF_TEST_TIMESTAMP = "1761875313209"
SELF_TEST_GET_PARAMS = {"vol": "1", "symbol": "BTC_USDT"}
SELF_TEST_GET_SIGNATURE = "b3e1e8095fea63fafbd9b77d997965546505943c08842efe730397d4ea5adb3e"
SELF_TEST_POST_BODY = {"symbol": "BTC_USDT", "vol": 1}
SELF_TEST_POST_SIGNATURE = "1c744783288e2f74ee97bfde3c7db85707f5241a87d2758dabc17fde7e4a6ca0"


def load_params(raw: str | None) -> Any:
    return load_json_params(raw, allow_array=True)


def env_credentials() -> tuple[str, str]:
    return read_mexc_credentials()


def encode_sorted_params(params: dict[str, Any]) -> str:
    pairs = [(k, v) for k, v in sorted(params.items()) if v is not None]
    return urllib.parse.urlencode(pairs, doseq=True)


def compact_json(params: Any) -> str:
    return json.dumps(params, separators=(",", ":"), ensure_ascii=True)


def sign(access_key: str, timestamp: str, parameter_string: str, secret: str) -> str:
    target = f"{access_key}{timestamp}{parameter_string}"
    return hmac.new(
        secret.encode("utf-8"),
        target.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    return redact_auth_headers(headers, {"ApiKey", "Signature"})


def build_request(args: argparse.Namespace) -> tuple[str, str, dict[str, str], bytes | None, str]:
    method = normalize_method(args.method)
    path = normalize_path(args.path)
    ensure_no_signed_query(path, args.signed)
    url = validate_base_url(
        args.base_url, authenticated=args.signed,
        allowed_authenticated_hosts=AUTHENTICATED_HOSTS,
    ) + path
    params = load_params(args.params)
    headers: dict[str, str] = {"User-Agent": "codex-mexc-futures-helper/1.0"}
    body: bytes | None = None
    printable_body = ""

    if method in {"GET", "DELETE"}:
        if not isinstance(params, dict):
            raise SystemExit("--params must be a JSON object for GET and DELETE requests")
        parameter_string = encode_sorted_params(params)
        if parameter_string:
            url = f"{url}?{parameter_string}"
    else:
        parameter_string = compact_json(params) if params else ""
        printable_body = parameter_string
        headers["Content-Type"] = "application/json"
        body = parameter_string.encode("utf-8") if parameter_string else None

    if args.signed:
        api_key, secret = env_credentials()
        timestamp = str(args.timestamp or int(time.time() * 1000))
        headers["Content-Type"] = "application/json"
        headers["ApiKey"] = api_key
        headers["Request-Time"] = timestamp
        headers["Recv-Window"] = str(args.recv_window)
        headers["Signature"] = sign(api_key, timestamp, parameter_string, secret)

    return method, url, headers, body, printable_body


def execute(
    method: str, url: str, headers: dict[str, str], body: bytes | None,
    *, authenticated: bool, show_private_response: bool,
) -> int:
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with open_mexc_request(request, timeout=20, authenticated=authenticated) as response:
            status = int(response.status)
            text = response.read().decode("utf-8", errors="replace")
            sys.stdout.write(format_http_response(
                text, status=status, authenticated=authenticated,
                show_private_response=show_private_response,
            ))
            return 0 if 200 <= status < 300 else 1
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        sys.stderr.write(format_http_response(
            text, status=int(exc.code), authenticated=authenticated,
            show_private_response=show_private_response,
        ))
        return 1
    except (urllib.error.URLError, TimeoutError):
        sys.stderr.write("Network request failed; signed URL and request details were suppressed.\n")
        return 1


def self_test() -> None:
    get_params = encode_sorted_params(SELF_TEST_GET_PARAMS)
    get_sig = sign(SELF_TEST_ACCESS_KEY, SELF_TEST_TIMESTAMP, get_params, SELF_TEST_SECRET)
    if get_sig != SELF_TEST_GET_SIGNATURE:
        raise SystemExit("Futures GET signature self-test failed")
    post_body = compact_json(SELF_TEST_POST_BODY)
    post_sig = sign(SELF_TEST_ACCESS_KEY, SELF_TEST_TIMESTAMP, post_body, SELF_TEST_SECRET)
    if post_sig != SELF_TEST_POST_SIGNATURE:
        raise SystemExit("Futures POST signature self-test failed")
    if strip_wrapping_quotes("'abc123'") != "abc123":
        raise SystemExit("Futures credential quote stripping self-test failed")
    validate_mexc_request_url(f"{BASE_URL}/api/v1/contract/ping")
    for unsafe_url in (
        "file:///etc/passwd",
        "http://api.mexc.com/api/",
        "https://api.mexc.com@evil.example/api/",
    ):
        try:
            validate_mexc_request_url(unsafe_url)
        except urllib.error.URLError:
            continue
        raise SystemExit("Futures URL allowlist self-test failed")
    print("futures self-test ok")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("method", nargs="?", help="HTTP method, e.g. GET or POST")
    parser.add_argument("path", nargs="?", help="API path, e.g. /api/v1/contract/ping")
    parser.add_argument("--params", help="JSON object of business parameters")
    parser.add_argument("--signed", action="store_true", help="Sign request using env credentials")
    parser.add_argument("--execute", action="store_true", help="Send the request. Default is dry-run.")
    parser.add_argument("--confirm-live", action="store_true", help="Allow live signed non-GET requests")
    parser.add_argument(
        "--show-private-response", action="store_true",
        help="Print a redacted private response instead of the default metadata-only summary",
    )
    parser.add_argument("--recv-window", default="10", help="Futures Recv-Window header in seconds")
    parser.add_argument("--timestamp", help="Override timestamp in milliseconds, mainly for tests")
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return args
    if not args.method or not args.path:
        parser.error("method and path are required unless --self-test is used")
    return args


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        return 0
    method = normalize_method(args.method)
    path = normalize_path(args.path)
    validate_live_execution(
        execute=args.execute,
        confirm_live=args.confirm_live,
        method=method,
        path=path,
        authenticated=args.signed,
    )
    method, url, headers, body, printable_body = build_request(args)
    if not args.execute:
        parsed_url = urllib.parse.urlsplit(url)
        redacted_query = redact_query_params(parsed_url.query, DEFAULT_SENSITIVE_KEYS)
        safe_url = urllib.parse.urlunsplit(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, redacted_query, parsed_url.fragment)
        )
        print(json.dumps(
            {
                "dry_run": True,
                "method": method,
                "url": safe_url,
                "headers": redact_headers(headers),
                "body": redact_json_text(printable_body),
            },
            indent=2,
        ))
        return 0
    return execute(
        method, url, headers, body, authenticated=args.signed,
        show_private_response=args.show_private_response,
    )


if __name__ == "__main__":
    raise SystemExit(main())
