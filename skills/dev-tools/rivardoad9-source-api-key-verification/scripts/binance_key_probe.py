#!/usr/bin/env python3
"""Is this prefixless 64-char string a Binance API Key, or its Secret Key?

Read-only, no side effects, prints nothing but masked info, persists nothing.

    python3 binance_key_probe.py <candidate>
    BINANCE_KEY_CANDIDATE=<candidate> python3 binance_key_probe.py

How it works (differential probe, verified 5 Okt 2026):
  Binance validates, in order: API key exists -> IP allowed -> signature valid.
  We send the candidate as X-MBX-APIKEY on a signed GET /api/v3/account with a
  deliberately WRONG signature (HMAC of a dummy secret), plus a known-fake key
  as the control.

    -1022 (HTTP 400) "Signature for this request is not valid"
        -> the key was RECOGNISED (passed lookup + IP check): candidate IS a
           live API Key. Also proves this host's IP passes the whitelist.
    -2015 (HTTP 401) "Invalid API-key, IP, or permissions", same as the control
        -> NOT an API key (usually the Secret Key), or this host is outside the
           key's IP whitelist.
    -2014 "API-key format invalid"
        -> invisible characters; strip whitespace/zero-width and re-measure.

Never send a candidate to a state-mutating endpoint to "test" it, and rm any
temp copy of this script once the check is done if a real key was inlined.
"""
import hashlib
import hmac
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://api.binance.com"          # fallback: https://api1..api4.binance.com
ACCOUNT = "/api/v3/account"               # read-only, signature required


def clean(raw: str) -> str:
    """Strip whitespace and zero-width characters (Telegram/chat paste artefacts)."""
    s = "".join(raw.split())
    for ch in ("\u200b", "\u200c", "\u200d", "\ufeff", "\u2060"):
        s = s.replace(ch, "")
    return s


def probe(key: str, label: str) -> str:
    qs = "timestamp=%d&recvWindow=5000" % int(time.time() * 1000)
    sig = hmac.new(b"dummy-secret-not-real", qs.encode(), hashlib.sha256).hexdigest()
    req = urllib.request.Request(
        f"{BASE}{ACCOUNT}?{qs}&signature={sig}", headers={"X-MBX-APIKEY": key})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"[{label}] HTTP {r.status} (unexpected success!) {r.read().decode()[:200]}")
            return "OK"
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            j = json.loads(body)
            code, msg = j.get("code"), j.get("msg")
        except Exception:
            code, msg = "?", body[:120]
        print(f"[{label}] HTTP {e.code} code={code} msg={msg}")
        return str(code)
    except Exception as e:                                    # noqa: BLE001
        print(f"[{label}] ERR {type(e).__name__}: {str(e)[:140]}")
        return "ERR"


def main() -> int:
    raw = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BINANCE_KEY_CANDIDATE", ""))
    if not raw.strip():
        print(__doc__)
        return 2

    key = clean(raw)
    non = [repr(c) for c in key if not re.fullmatch(r"[A-Za-z0-9]", c)]
    print(f"panjang raw={len(raw)} | bersih={len(key)} (Binance = 64) | non-alnum: {non or 'tidak ada'}")
    print(f"mask: {key[:6]}\u2026{key[-4:]}")
    if len(key) != 64:
        print("PERINGATAN: panjang bukan 64 -> kemungkinan ke-copy sebagian / kelebihan karakter.")

    ctl = probe("X" * 64, "KONTROL (key palsu)")
    got = probe(key, "CANDIDATE")

    print()
    if got == "-1022":
        print("=> CANDIDATE adalah API KEY (valid & live). Butuh SECRET KEY untuk endpoint akun.")
        print("   Bonus: IP host ini lolos whitelist (atau whitelist tidak dipasang).")
        rc = 0
    elif got == ctl:
        print("=> CANDIDATE bukan API key (kemungkinan SECRET KEY), atau IP host ini di luar whitelist.")
        rc = 1
    elif got == "-2014":
        print("=> Format key invalid: ada karakter aneh. Bersihkan lalu ulangi.")
        rc = 1
    else:
        print(f"=> Hasil tidak lazim ({got}); baca pesan di atas.")
        rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
