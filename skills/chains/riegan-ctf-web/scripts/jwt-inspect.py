#!/usr/bin/env python3
"""jwt-inspect.py — decode and triage JWTs; optional HMAC wordlist crack.

Given one or more JWTs (args, or '-' for stdin, one per line):
  - splits header.payload.signature, base64url-decodes each part
  - pretty-prints header and payload JSON
  - flags suspicious combinations:
      alg "none" (unsigned-token attack surface)
      HS* alg together with jwk/jku/x5u header params (key-confusion / SSRF bait)
      RS*/ES* alg (try re-signing as HS256 with the public key)
      exp claim missing, in the past, or absurdly far out
      iat in the future, sub/role/admin-style claims worth flipping

With --crack WORDLIST, tries HMAC-SHA256/384/512 (per the alg header) over every
word in the list using hashlib+hmac only; prints the secret on match and then
verifies the token with it.

Stdlib only. Usage: jwt-inspect.py TOKEN... | jwt-inspect.py - --crack wl.txt
"""
import argparse
import base64
import hashlib
import hmac
import json
import sys
import time

DIGESTS = {
    "HS256": hashlib.sha256,
    "HS384": hashlib.sha384,
    "HS512": hashlib.sha512,
}


def b64u_decode(seg):
    """Decode a base64url segment, tolerating missing padding and ASCII errors."""
    if isinstance(seg, str):
        seg = seg.encode()
    seg = seg.strip()
    pad = (-len(seg)) % 4
    try:
        return base64.urlsafe_b64decode(seg + b"=" * pad)
    except ValueError as e:
        raise ValueError(f"invalid base64url: {e}") from e


def load_tokens(args):
    toks = []
    for item in args.tokens:
        if item == "-":
            toks.extend(ln.strip() for ln in sys.stdin if ln.strip())
        else:
            toks.append(item.strip())
    if not toks:
        raise SystemExit("error: no token supplied (positional arg or '-')")
    return toks


def split_token(token):
    parts = token.strip().strip('"').split(".")
    if len(parts) not in (2, 3):
        raise ValueError(f"expected 2 or 3 dot-separated parts, got {len(parts)}")
    return parts


def decode_part(name, seg):
    raw = b64u_decode(seg)
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def findings_for(header, payload):
    """Return a list of (severity, note) tuples worth reporting."""
    out = []
    alg = str(header.get("alg", "")).lower()
    exp = payload.get("exp") if isinstance(payload, dict) else None
    iat = payload.get("iat") if isinstance(payload, dict) else None
    now = time.time()

    if alg in ("none", "") or header.get("alg") in (None, "none"):
        out.append(("HIGH", 'alg is "none"/missing — try sending an unsigned token'))
    if alg.startswith("hs"):
        for p in ("jwk", "jku", "x5u", "x5c"):
            if p in header:
                out.append(("HIGH", f"HS alg with {p} present — {p} tampering / SSRF bait"))
    if alg.startswith(("rs", "es", "ps")):
        out.append(("MED", f"{header.get('alg')} — try RS256->HS256 key confusion "
                           "(re-sign as HS256, secret = public key bytes)"))
    if "kid" in header:
        out.append(("MED", "kid header present — try SQLi or path traversal in kid"))
    if isinstance(exp, (int, float)):
        if exp < now:
            out.append(("LOW", f"exp is in the past ({int(exp)}) — server may not check it"))
        elif exp > now + 365 * 24 * 3600:
            out.append(("LOW", "exp absurdly far out — forged-looking token"))
    elif exp is None and isinstance(payload, dict):
        out.append(("MED", "no exp claim — token may never expire / exp never checked"))
    if isinstance(iat, (int, float)) and iat > now + 300:
        out.append(("LOW", "iat is in the future"))
    if isinstance(payload, dict):
        for key in payload:
            if str(key).lower() in ("role", "roles", "isadmin", "admin", "priv",
                                    "permissions", "group", "is_staff", "usertype"):
                out.append(("LOW", f"privilege claim '{key}' present — flip it after forging"))
                break
    return out


def crack(token, header, wordlist_path):
    """Try HMAC wordlist crack per the alg header. Returns secret or None."""
    alg = str(header.get("alg", "")).upper()
    if alg not in DIGESTS:
        print(f"  [crack] alg {header.get('alg')!r} is not HMAC — nothing to crack",
              file=sys.stderr)
        return None
    try:
        head, payload, sig = token.split(".")
    except ValueError:
        head, payload, sig = token.split(".")[:2] + [""]
        # 2-part token has no signature to verify
        print("  [crack] no signature part present", file=sys.stderr)
        return None
    signing_input = f"{head}.{payload}".encode()
    try:
        target = b64u_decode(sig)
    except ValueError as e:
        print(f"  [crack] bad signature encoding: {e}", file=sys.stderr)
        return None
    tried = 0
    try:
        with open(wordlist_path, "r", errors="replace") as fh:
            for line in fh:
                secret = line.rstrip("\r\n")
                tried += 1
                digest = hmac.new(secret.encode(), signing_input, DIGESTS[alg]).digest()
                if hmac.compare_digest(digest, target):
                    print(f"  [crack] FOUND secret ({tried} tries): {secret!r}")
                    print(f"  [crack] forge with alg {alg} + this secret")
                    return secret
    except OSError as e:
        print(f"  [crack] cannot read wordlist: {e}", file=sys.stderr)
        return None
    print(f"  [crack] no match in {tried} words (alg {alg})", file=sys.stderr)
    return None


def process(token, want_crack):
    print("=" * 72)
    print(f"token ({len(token)} chars): {token[:100]}{'...' if len(token) > 100 else ''}")
    try:
        parts = split_token(token)
    except ValueError as e:
        print(f"  [!] not a JWT: {e}")
        return
    header = decode_part("header", parts[0])
    payload = decode_part("payload", parts[1])
    sig = parts[2] if len(parts) == 3 else "(none)"
    if header is None:
        print("  [!] header did not decode to JSON; raw:")
        print("     ", b64u_decode(parts[0])[:200])
        header = {}
    if payload is None:
        print("  [!] payload did not decode to JSON; raw:")
        print("     ", b64u_decode(parts[1])[:200])
        payload = {}
    print("--- header")
    print(json.dumps(header, indent=2, sort_keys=True))
    print("--- payload")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"--- signature (b64url): {sig[:60]}{'...' if len(sig) > 60 else ''}")
    for sev, note in findings_for(header, payload):
        print(f"  [{sev}] {note}")
    if want_crack:
        crack(token, header, want_crack)
    print()


def main():
    ap = argparse.ArgumentParser(
        prog="jwt-inspect.py",
        description="Decode and triage JWTs; optional HMAC wordlist crack.",
        epilog="Examples: jwt-inspect.py 'eyJhbG...' "
               "| jwt-inspect.py - --crack /usr/share/seclists/Passwords/probable-v2-top1575.txt",
    )
    ap.add_argument("tokens", nargs="+", metavar="TOKEN",
                    help="JWT strings, or '-' to read tokens from stdin")
    ap.add_argument("--crack", metavar="WORDLIST",
                    help="HMAC wordlist crack attempt (HS256/384/512 only)")
    args = ap.parse_args()
    for tok in load_tokens(args):
        process(tok, args.crack)


if __name__ == "__main__":
    main()
