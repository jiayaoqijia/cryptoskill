#!/usr/bin/env python3
"""decode_blob.py — identify and recursively decode encoded/encrypted text.

Audit tool for the crypto-review skill: given a blob (argument, file, or
--scan to extract candidates from a file), classify each layer and peel
it: base16/32/58/64/85 (std+url variants), URL-encoding, unicode escapes,
quoted-printable, gzip/zlib/bz2/lzma, ROT13/Caesar (all shifts, chi-square
scored), Atbash, single-byte XOR (256 keys scored), JWT payloads, and
format wrappers (Ansible Vault, OpenSSL/CryptoJS `Salted__`, PEM, K8s
secret bodies). One-way formats (hashes) are IDENTIFIED, never "decoded".

Honest limits (by design): modern encryption without the key is NOT
decodable — the tool prints the exact decrypt command to run once key
material is found (hardcoded keys are a secrets-detection finding).

Stdlib only. Usage:
  python3 decode_blob.py "<blob>"
  python3 decode_blob.py -f <file>
  python3 decode_blob.py --scan <file>     # find candidate blobs
  python3 decode_blob.py --selftest        # built-in round-trip vectors
"""
import argparse
import base64
import binascii
import codecs
import json
import math
import quopri
import re
import string
import sys
import urllib.parse
import zlib

PRINTABLE = set(bytes(string.printable, "ascii"))

# English letter frequencies (percent) for chi-square scoring
ENG_FREQ = {
    "a": 8.17, "b": 1.49, "c": 2.78, "d": 4.25, "e": 12.70, "f": 2.23,
    "g": 2.02, "h": 6.09, "i": 6.97, "j": 0.15, "k": 0.77, "l": 4.03,
    "m": 2.41, "n": 6.75, "o": 7.51, "p": 1.93, "q": 0.10, "r": 5.99,
    "s": 6.33, "t": 9.06, "u": 2.76, "v": 0.98, "w": 2.36, "x": 0.15,
    "y": 1.97, "z": 0.07, " ": 17.0,
}


def printable_ratio(b):
    if not b:
        return 0.0
    return sum(1 for x in b if x in PRINTABLE) / len(b)


def english_score(text, min_letters=15):
    """Lower chi-square = more English-like. Sparse-letter text scores INF
    (short/sparse strings are statistically meaningless — never 'English')."""
    t = text.lower()
    counts = {}
    n = 0
    for ch in t:
        if ch in ENG_FREQ:
            counts[ch] = counts.get(ch, 0) + 1
            n += 1
    if n < min_letters:
        return math.inf
    chi = 0.0
    for ch, freq in ENG_FREQ.items():
        expected = n * freq / 100.0
        chi += (counts.get(ch, 0) - expected) ** 2 / max(expected, 1e-9)
    return chi / n


def try_utf8(b):
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return None


# ---------------------------------------------------------------- layers

def d_hex(s):
    t = s.strip()
    if len(t) < 8 or len(t) % 2 or re.fullmatch(r"[0-9a-fA-F]+", t) is None:
        return None
    try:
        return bytes.fromhex(t)
    except ValueError:
        return None


def _strip_linebreaks(s):
    """Base64 in files may be line-wrapped (PEM style) — strip ONLY newlines,
    never spaces: a letters+spaces string is prose, not base64."""
    return s.replace("\r", "").replace("\n", "")


def d_b64(s):
    t = _strip_linebreaks(s)
    if len(t) < 8 or not re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", t):
        return None
    try:
        return base64.b64decode(t, validate=True)
    except (binascii.Error, ValueError):
        return None


def d_b64url(s):
    t = _strip_linebreaks(s)
    if len(t) < 8 or not re.fullmatch(r"[A-Za-z0-9_-]+={0,2}", t):
        return None
    try:
        return base64.urlsafe_b64decode(t + "=" * (-len(t) % 4))
    except (binascii.Error, ValueError):
        return None


def d_b32(s):
    t = _strip_linebreaks(s).upper()
    if len(t) < 16 or not re.fullmatch(r"[A-Z2-7]+={0,6}", t):
        return None
    try:
        return base64.b32decode(t)
    except (binascii.Error, ValueError):
        return None


B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def d_b58(s):
    t = _strip_linebreaks(s)
    if len(t) < 10 or not re.fullmatch(f"[{B58_ALPHABET}]+", t):
        return None
    n = 0
    for ch in t:
        n = n * 58 + B58_ALPHABET.index(ch)
    out = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b"\x00" * (len(t) - len(t.lstrip("1"))) + out  # leading 1s = 0x00


def d_b85(s):
    t = _strip_linebreaks(s)
    if len(t) < 10 or len(t) % 5 or not re.fullmatch(r"[!-u]+", t):
        return None
    try:
        return base64.a85decode(t)
    except (binascii.Error, ValueError):
        return None


def d_url(s):
    if not re.search(r"%[0-9a-fA-F]{2}", s):
        return None
    out = urllib.parse.unquote(s, errors="strict")
    return out.encode("utf-8", "surrogateescape")


def d_unicode_esc(s):
    if not re.search(r"(\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}){2,}", s):
        return None
    try:
        return codecs.decode(s, "unicode_escape").encode("latin-1", "ignore")
    except Exception:
        return None


def d_qp(s):
    if not re.search(r"=[0-9A-F]{2}", s) or "=" not in s:
        return None
    try:
        return quopri.decodestring(s.encode("utf-8", "ignore"))
    except Exception:
        return None


def d_gzip(b):
    if b[:2] == b"\x1f\x8b":
        import gzip
        try:
            return gzip.decompress(b)
        except OSError:
            return None
    return None


def d_zlib(b):
    if b[:1] == b"\x78":
        try:
            return zlib.decompress(b)
        except zlib.error:
            return None
    return None


def d_bz2(b):
    if b[:3] == b"BZh":
        import bz2
        try:
            return bz2.decompress(b)
        except OSError:
            return None
    return None


def d_lzma(b):
    if b[:6] == b"\xfd7zXZ\x00":
        import lzma
        try:
            return lzma.decompress(b)
        except lzma.LZMAError:
            return None
    return None


def d_rot13(s):
    t = codecs.encode(s, "rot13")
    # only claim a layer if the rotation changes something and yields text
    if t != s and re.search(r"[a-zA-Z]", s):
        return t.encode()
    return None


def d_caesar_best(s):
    """All-shift Caesar; returns (bytes, shift) when a shift clearly wins."""
    in_score = english_score(s)
    best, best_score, best_shift = None, math.inf, None
    for shift in range(1, 26):
        table = str.maketrans(
            string.ascii_lowercase + string.ascii_uppercase,
            string.ascii_lowercase[shift:] + string.ascii_lowercase[:shift]
            + string.ascii_uppercase[shift:] + string.ascii_uppercase[:shift])
        cand = s.translate(table)
        sc = english_score(cand)
        if sc < best_score:
            best, best_score, best_shift = cand.encode(), sc, shift
    if best is not None and best_score < in_score * 0.4 and best_score < 3.0:
        return best, best_shift
    return None, None


def d_xor_best(b, in_score=math.inf):
    """Single-byte XOR: printable candidates ranked by English statistics;
    accepted only when the result is TWICE as English-like as the input —
    small keys on short ASCII oscillate (garbage <-> text) otherwise."""
    best, best_score, best_key = None, math.inf, None
    for k in range(1, 256):
        cand = bytes(x ^ k for x in b)
        if printable_ratio(cand) < 0.95:
            continue
        text = try_utf8(cand)
        if text is None:
            continue
        sc = english_score(text)
        if sc < best_score:
            best, best_score, best_key = cand, sc, k
    if best is not None and best_score < 3.0 and best_score < in_score * 0.5:
        return best, best_key
    return None, None


def d_atbash(s):
    tbl = str.maketrans(
        string.ascii_lowercase + string.ascii_uppercase,
        string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1])
    t = s.translate(tbl)
    if t != s:
        return t.encode()
    return None


# ------------------------------------------------------------ identifiers

def looks_like_jwt(s):
    parts = s.strip().split(".")
    return len(parts) == 3 and all(len(p) >= 8 for p in parts[:2])


def decode_jwt(s):
    parts = s.strip().split(".")
    out = {}
    try:
        out["header"] = json.loads(d_b64url(parts[0]))
        out["payload"] = json.loads(d_b64url(parts[1]))
        return out
    except Exception:
        return None


HASH_SHAPES = [
    (re.compile(r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$"), "bcrypt (one-way)"),
    (re.compile(r"^\$argon2(id|i|d)\$[a-z0-9=,+:/$-]{20,}$"), "argon2 (one-way)"),
    (re.compile(r"^[a-f0-9]{32}$"), "MD5 or NTLM hex (one-way)"),
    (re.compile(r"^[a-f0-9]{40}$"), "SHA-1 hex (one-way)"),
    (re.compile(r"^[a-f0-9]{64}$"), "SHA-256 hex (one-way)"),
    (re.compile(r"^[a-f0-9]{128}$"), "SHA-512 hex (one-way)"),
]


def identify_hash(s):
    t = s.strip()
    for rx, name in HASH_SHAPES:
        if rx.match(t):
            return name
    return None


KEYED_HINTS = {
    "ansible_vault": (
        "Ansible Vault payload — key REQUIRED (vault password). Decrypt with:\n"
        "  echo <blob> | ansible-vault decrypt  # or edit the vault file in place"),
    "salted_openssl": (
        "OpenSSL/CryptoJS `Salted__` KDF envelope — passphrase REQUIRED.\n"
        "Try (modern pbkdf2):\n"
        "  openssl enc -d -aes-256-cbc -pbkdf2 -in blob.bin -pass pass:'<KEY>'\n"
        "Try (legacy MD5 KDF, common for CryptoJS):\n"
        "  openssl enc -d -aes-256-cbc -md md5 -in blob.bin -pass pass:'<KEY>'\n"
        "A hardcoded <KEY> in the repo + this blob = CRITICAL finding chain."),
    "age": (
        "age encrypted file (age-encryption.org header) — recipient key REQUIRED."),
}


def check_keyed(b):
    if b.startswith(b"Salted__"):
        return "salted_openssl"
    if b.startswith(b"age-encryption.org/"):
        return "age"
    return None


PEM_RE = re.compile(r"-----BEGIN ([A-Z0-9 ]+)-----")


def check_pem(s):
    m = PEM_RE.search(s)
    return m.group(1) if m else None


ANSIBLE_RE = re.compile(r"\$ANSIBLE_VAULT;\d(?:\.\d)?;AES256")


def check_ansible(s):
    return bool(ANSIBLE_RE.search(s))


# ---------------------------------------------------------------- engine

TEXT_DECODERS_STRONG = [
    ("hex", d_hex),
    ("base64", d_b64),          # regex requires +/= or mixed charset
    ("base32", d_b32),
    ("base58", d_b58),
    ("base85", d_b85),
    ("url-encoding", d_url),
    ("unicode-escapes", d_unicode_esc),
    ("quoted-printable", d_qp),
    # base64url only carries a strong signature with url-safe symbols/pad;
    # pure-alnum input is ambiguous (matches prose) → weak list
]


def d_b64_alnum(s):
    """Ambiguous pure-alnum base64(url) — gated on score improvement."""
    t = _strip_linebreaks(s)
    if len(t) < 16 or len(t) % 4 != 0 or not re.fullmatch(r"[A-Za-z0-9]+", t):
        return None
    for fn in (base64.b64decode,):
        try:
            return fn(t, validate=True)
        except (binascii.Error, ValueError):
            return None


TEXT_DECODERS_WEAK = [
    ("base64(pure-alnum)", d_b64_alnum),
    ("atbash", d_atbash),
]


def _english_like(b):
    t = try_utf8(b)
    return t is not None and english_score(t) < 1.5
BIN_DECODERS = [
    ("gzip", d_gzip), ("zlib", d_zlib), ("bz2", d_bz2), ("lzma", d_lzma),
]


def _has_known_magic(b):
    """Byte prefixes that justify accepting a low-printable decode step."""
    magics = (b"\x1f\x8b", b"\x78", b"BZh", b"\xfd7zXZ\x00", b"PK\x03\x04",
              b"Salted__", b"age-encryption.org/", b"{", b"[")
    return any(b.startswith(m) for m in magics)


def peel_layer(data):
    """One peel step: returns (label, decoded, note) or None."""
    text = try_utf8(data)

    # keyed / wrapper formats first (identification, not decode)
    if text:
        if check_ansible(text):
            return ("identify", None, KEYED_HINTS["ansible_vault"])
        pem = check_pem(text)
        if pem:
            return ("identify", None,
                    f"PEM block: {pem} — parse with `openssl <cmd> -noout -text -in <file>`"
                    + ("  [ENCRYPTED key: passphrase required]" if "ENCRYPTED" in pem else ""))
        if looks_like_jwt(text):
            jwt = decode_jwt(text)
            if jwt:
                payload = json.dumps(jwt, indent=1)
                return ("jwt", payload.encode(),
                        "JWT decoded (header+payload). Signature NOT verified by this tool — "
                        "see crypto-review §3: verify with the issuer's public key / jwt.io")
    keyed = check_keyed(data)
    if keyed:
        return ("identify", None, KEYED_HINTS[keyed])

    # compression
    for name, fn in BIN_DECODERS:
        out = fn(data)
        if out is not None:
            return (name, out, None)

    # text-layer decoders: strong signatures accept directly
    if text is not None:
        in_score = english_score(text)
        for name, fn in TEXT_DECODERS_STRONG:
            out = fn(text)
            if out and out != data:
                return (name, out, None)
        # ambiguous shapes must prove they revealed English/structured text
        for name, fn in TEXT_DECODERS_WEAK:
            out = fn(text)
            if not (out and out != data):
                continue
            if _has_known_magic(out) or printable_ratio(out) > printable_ratio(data) + 0.1 \
                    or _english_like(out):
                return (name, out, None)
        # classical best-effort
        letters = sum(1 for c in text if c.isalpha())
        if in_score >= 1.2:
            # caesar: letter-rich text only (short mixed-charset strings are
            # statistically ambiguous)
            if letters >= 30 and letters / max(len(text), 1) >= 0.6:
                best, shift = d_caesar_best(text)
                if best is not None:
                    return (f"caesar(+{shift})", best, "chi-square best shift — verify plausibility")
            # single-byte XOR: safe on any printable non-English text — must
            # improve English-likeness 2x or reveal structure
            best, key = d_xor_best(data, in_score)
            if best is not None:
                return (f"single-byte-xor(0x{key:02x})", best,
                        "printability-scored — verify plausibility")
    return None


def decode_blob(initial, max_depth=8, verbose=False):
    lines = []
    data = initial if isinstance(initial, bytes) else initial.encode("utf-8", "ignore")
    # one-way hash check: hex-shaped values that do NOT decode to text are
    # digests; hex that peels to ASCII is an encoding layer, not a hash
    text0 = try_utf8(data)
    if text0 is not None:
        hname = identify_hash(text0)
        hx = d_hex(text0)
        if hname and (hx is None or printable_ratio(hx) < 0.6):
            lines.append(f"input  : {data[:60]!r}")
            lines.append(f"result : ONE-WAY HASH — {hname}")
            lines.append("note   : hashes are not decodable; check wordlists/lookup tables "
                         "offline (crypto-review §2 purpose rules apply)")
            return "\n".join(lines)

    for depth in range(max_depth + 1):
        preview = (try_utf8(data) or repr(data))
        lines.append(f"layer {depth}: {preview[:100]}{'…' if len(preview) > 100 else ''}")
        # STOP FIRST: plain text with English statistics is an endpoint —
        # peeling English through base64 decoders only produces garbage
        text = try_utf8(data)
        # structured-data endpoints: valid JSON, key=value tokens, URLs
        if text is not None and text[:1] in "{[":
            try:
                json.loads(text)
                lines.append(f"stop   : structured data (JSON, {len(data)} bytes) — "
                             "decode complete")
                break
            except Exception:
                pass
        if text is not None and re.search(r"[\w.-]+=[^\s]{6,}", text):
            lines.append(f"stop   : structured token/credential shape ({len(data)} bytes) — "
                         "decode complete; apply secrets-detection rules to the plaintext")
            break
        wrapper_present = bool(
            text and (check_ansible(text) or check_pem(text) or looks_like_jwt(text)
                      or re.search(r"%[0-9a-fA-F]{2}", text)))  # %-encoding is a
        # syntactic encoding signature: it overrides the plain-text stop
        if text is not None and not wrapper_present and printable_ratio(data) >= 0.85 \
                and english_score(text) < 1.2:
            lines.append(f"stop   : plain text ({len(data)} bytes) — no further layers")
            break
        step = peel_layer(data)
        if step is None:
            if printable_ratio(data) >= 0.85:
                lines.append(f"stop   : plain text ({len(data)} bytes) — no further layers")
            else:
                lines.append("stop   : binary data, no known layer applies — "
                             "possibly raw encryption (key needed) or an unknown format")
            break
        label, out, note = step
        if label == "identify":
            lines.append(f"stop   : {note}")
            break
        if out is None:
            break
        lines.append(f"  ↳ {label}")
        if note:
            lines.append(f"    ({note})")
        data = out
    else:
        lines.append("stop   : max depth reached — inspect manually")
    return "\n".join(lines)


BLOB_RE = re.compile(r"(?<![\w./-])[A-Za-z0-9+/=_-]{24,}(?![\w./-])")


def scan_file(path):
    found = []
    # blind hygiene: never surface ground-truth or report files as candidates
    if path.endswith(("expected-findings.md", "SECURITY-AUDIT.md")):
        return found
    text = open(path, encoding="utf-8", errors="replace").read()
    for m in BLOB_RE.finditer(text):
        cand = m.group(0)
        # entropy signal required: a digit or base64 symbol — pure words are prose
        if re.search(r"[0-9+/=]", cand):
            found.append((m.start(), cand))
    return found


SELFTEST_VECTORS = [
    ("plain", "hello world audit", "plain text"),
    ("b64", lambda: base64.b64encode(b"decoded-secret-token").decode(),
     "decoded-secret-token"),
    ("b64->zlib", lambda: base64.b64encode(zlib.compress(b'{"user":"admin","role":"superuser"}')).decode(),
     '"role":"superuser"'),
    ("hex double", lambda: (b"4927626f756e6420612072617468626f6e65".hex()).encode().hex(),
     "rathbone"),
    ("rot13 (long)", "Gur cynpr npghnyyl unir n cynpr bs orvat n cynpr jurer crbcyr pna tb gb trg rgureq cynprf naq znal bgure cynprf",
     "actually"),
    ("jwt", "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
     '"alg": "HS256"'),
    ("hash-close", "$2b$12$KIXQxJ9d8C1oQ9w8e7r6tOuARoP0THsR8UdozjgNryP4J3jVmNHl0", "ONE-WAY HASH"),
    ("hex-is-not-a-hash", lambda: b"just plain ascii here".hex(), "plain text"),
]


def selftest():
    ok = 0
    for name, val, expect in SELFTEST_VECTORS:
        blob = val() if callable(val) else val
        out = decode_blob(blob)
        good = expect in out
        print(f"[{'OK' if good else 'FAIL'}] {name} (expect {expect!r})\n{out}\n")
        ok += good
    print(f"decode_blob selftest: {ok}/{len(SELFTEST_VECTORS)} vectors decoded with expected content")
    return 0 if ok == len(SELFTEST_VECTORS) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("blob", nargs="?", help="the blob to decode")
    ap.add_argument("-f", "--file", help="read blob from file (first non-empty line)")
    ap.add_argument("--scan", help="extract candidate blobs from a file and decode each")
    ap.add_argument("--max-depth", type=int, default=8)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.scan:
        for off, blob in scan_file(args.scan):
            print(f"--- candidate @{off} ---")
            print(decode_blob(blob, args.max_depth))
            print()
        return 0
    if args.file:
        blob = next((l.strip() for l in open(args.file, encoding="utf-8",
                                             errors="replace") if l.strip()), None)
        if not blob:
            print("no content", file=sys.stderr)
            return 2
    elif args.blob:
        blob = args.blob
    else:
        ap.error("provide a blob, -f FILE, --scan FILE, or --selftest")
    print(decode_blob(blob, args.max_depth))
    return 0


if __name__ == "__main__":
    sys.exit(main())
