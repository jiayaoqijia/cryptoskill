#!/usr/bin/env python3
"""xorfind.py — single/multi-byte XOR solver, crib search, keystream recovery.

Input is a file (or '-' for stdin) of raw bytes; hex and base64 text is
auto-detected and decoded first.

Modes:
  default            brute all 256 single-byte keys, rank by English score
  --keylen N         repeating-key XOR: solve each key column by frequency
  --key HEXKEY       XOR with a known key (hex), print result
  --crib STR         try the crib at every offset for every single-byte key,
                     and against repeating-key candidates found via --keylen
  --key-prefix STR   known-plaintext prefix: print keystream = data ^ prefix
                     (reveals a repeating key when prefix >= keylen)
Stdlib only.
"""
import argparse
import base64
import binascii
import re
import string
import sys

# relative letter frequency in English text (percent), a..z
FREQ = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23,
    'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03,
    'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99,
    's': 6.33, 't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15,
    'y': 1.97, 'z': 0.07, ' ': 15.0,
}
PRINTABLE = set(string.printable.encode())


def score(b):
    """Higher is more English-like."""
    s = 0.0
    for c in b:
        ch = chr(c)
        if c in PRINTABLE:
            s += FREQ.get(ch.lower() if ch.isalpha() else None, 0.0)
            if ch in ' \n':
                s += 2.0
        else:
            s -= 20.0
    return s


def xor(data, key):
    return bytes(c ^ key[i % len(key)] for i, c in enumerate(data))


def autodecode(data):
    """If data looks like hex or base64 text, decode it. Return bytes + label."""
    try:
        text = data.decode('ascii').strip()
    except UnicodeDecodeError:
        return data, 'raw'
    compact = re.sub(r'\s+', '', text)
    if re.fullmatch(r'(0x)?[0-9a-fA-F]+', compact) and len(compact) % 2 == 0:
        prefix = '0x' if compact.lower().startswith('0x') else ''
        return binascii.unhexlify(compact[len(prefix):]), 'hex'
    if re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', compact) and len(compact) % 4 == 0:
        try:
            return base64.b64decode(compact), 'base64'
        except (binascii.Error, ValueError):
            pass
    return data, 'raw'


def best_single(data):
    ranked = sorted(((score(xor(data, bytes([k]))), k) for k in range(256)),
                    reverse=True)
    return ranked[0], ranked[:5]


def show(data, limit=400):
    try:
        t = data.decode('utf-8')
    except UnicodeDecodeError:
        t = data.decode('latin-1')
    t = t[:limit]
    return t + ('\n[... truncated]' if len(data) > limit else '')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('file', help="input file, or '-' for stdin")
    ap.add_argument('--keylen', type=int, metavar='N',
                    help='repeating-key XOR with key length N')
    ap.add_argument('--key', metavar='HEXKEY', help='known hex key; just XOR')
    ap.add_argument('--crib', metavar='STR',
                    help='search for this plaintext fragment')
    ap.add_argument('--key-prefix', metavar='STR', dest='key_prefix',
                    help='known plaintext prefix; print keystream bytes')
    args = ap.parse_args()

    raw = sys.stdin.buffer.read() if args.file == '-' else open(args.file, 'rb').read()
    data, label = autodecode(raw)
    print(f"[*] input: {len(raw)} bytes -> {len(data)} bytes ({label})", file=sys.stderr)

    if args.key:
        k = binascii.unhexlify(args.key)
        out = xor(data, k)
        print(f"key = {k.hex()}")
        print(show(out))
        return

    if args.key_prefix:
        crib = args.key_prefix.encode()
        ks = xor(data[:len(crib)], crib)
        print(f"keystream prefix ({len(ks)} bytes) = {ks.hex()}")
        print("as text (may repeat if key shorter than prefix):")
        print(show(ks))
        # show periodicity hint
        for p in range(1, len(ks)):
            if len(ks) >= 2 * p and ks[: len(ks) - p] == ks[p:]:
                print(f"[*] keystream is periodic with period {p} — key: {ks[:p].hex()}")
                break
        return

    if args.keylen:
        kl = args.keylen
        key = bytearray()
        for col in range(kl):
            column = data[col::kl]
            (_, k), _ = best_single(column)
            key.append(k)
        out = xor(data, bytes(key))
        print(f"key = {bytes(key).hex()}  (ascii: {''.join(chr(c) if chr(c).isprintable() else '.' for c in key)})")
        print(show(out))
        if args.crib:
            c = args.crib.encode()
            i = out.find(c)
            print(f"crib {args.crib!r}: {'FOUND at offset ' + str(i) if i >= 0 else 'not found'}")
        return

    # single-byte mode
    (best, bk), top5 = best_single(data)
    print("top 5 single-byte keys:")
    for s, k in top5:
        print(f"  key 0x{k:02x} ({chr(k) if chr(k).isprintable() else '.'}) score {s:.1f}: {show(xor(data, bytes([k])), 80)!r}")
    print(f"\nbest (0x{bk:02x}) full plaintext:")
    print(show(xor(data, bytes([bk]))))

    if args.crib:
        c = args.crib.encode()
        hits = []
        for k in range(256):
            pt = xor(data, bytes([k]))
            start = 0
            while True:
                i = pt.find(c, start)
                if i < 0:
                    break
                hits.append((k, i))
                start = i + 1
        if hits:
            for k, i in hits[:20]:
                print(f"crib hit: key 0x{k:02x} at offset {i}: {show(xor(data, bytes([k]))[max(0,i-16):i+len(c)+16])!r}")
        else:
            print("crib not found under any single-byte key; try --keylen N --crib ...")


if __name__ == '__main__':
    main()
