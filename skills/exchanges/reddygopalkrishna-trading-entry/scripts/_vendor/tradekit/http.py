"""Minimal HTTP client on urllib with retries and JSON helpers."""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

USER_AGENT = "Mozilla/5.0 (compatible; trading-skills/0.2; +https://github.com/reddygopalkrishna/trading-skills)"

# Well-known OS certificate bundles. Some Python builds (notably the python.org macOS
# installer before "Install Certificates.command" is run) ship with an empty CA store.
SYSTEM_CA_BUNDLES = (
    "/etc/ssl/cert.pem",                    # macOS, Alpine, BSD
    "/etc/ssl/certs/ca-certificates.crt",   # Debian/Ubuntu
    "/etc/pki/tls/certs/ca-bundle.crt",     # Fedora/RHEL
    "/etc/ssl/ca-bundle.pem",               # openSUSE
)

_SSL_CONTEXT: Optional[ssl.SSLContext] = None


def ssl_context() -> ssl.SSLContext:
    """A verifying SSL context. Falls back to the OS bundle when Python's own store is empty.

    Certificate verification is never disabled. SSL_CERT_FILE / SSL_CERT_DIR still win.
    """
    global _SSL_CONTEXT
    if _SSL_CONTEXT is None:
        ctx = ssl.create_default_context()
        if not ctx.get_ca_certs() and not os.environ.get("SSL_CERT_FILE") and not os.environ.get("SSL_CERT_DIR"):
            for bundle in SYSTEM_CA_BUNDLES:
                if os.path.isfile(bundle):
                    try:
                        ctx.load_verify_locations(cafile=bundle)
                        break
                    except (ssl.SSLError, OSError):
                        continue
        _SSL_CONTEXT = ctx
    return _SSL_CONTEXT


class HTTPError(RuntimeError):
    def __init__(self, status: int, message: str, body: str = ""):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status
        self.body = body


def request(method: str, url: str, params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None,
            timeout: float = 20.0, retries: int = 2, backoff: float = 1.5,
            json_body: Optional[Any] = None) -> bytes:
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(clean, doseq=True)
    body = None
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json, text/csv, */*"}
    if headers:
        hdrs.update(headers)
    if json_body is not None:
        body = json.dumps(json_body).encode()
        hdrs.setdefault("Content-Type", "application/json")
    elif data is not None:
        body = urllib.parse.urlencode({k: v for k, v in data.items() if v is not None}).encode()
        hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")
    last_err: Optional[Exception] = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body, method=method.upper(), headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")[:2000]
            # retry only on throttling / transient server errors, never on order endpoints' 4xx
            if e.code in (429, 500, 502, 503, 504) and attempt < retries and method.upper() == "GET":
                time.sleep(backoff * (attempt + 1))
                last_err = HTTPError(e.code, e.reason, text)
                continue
            raise HTTPError(e.code, str(e.reason), text) from None
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = e
            if attempt < retries and method.upper() == "GET":
                time.sleep(backoff * (attempt + 1))
                continue
            hint = ""
            if "CERTIFICATE_VERIFY_FAILED" in str(e):
                hint = (" | Python cannot find root certificates. On macOS run 'Install Certificates.command' "
                        "from your Python folder, or set SSL_CERT_FILE to a CA bundle.")
            raise RuntimeError(f"network error for {urllib.parse.urlsplit(url).netloc}: {e}{hint}") from None
    raise RuntimeError(f"request failed: {last_err}")


def get_json(url: str, **kw) -> Any:
    return json.loads(request("GET", url, **kw).decode("utf-8"))
