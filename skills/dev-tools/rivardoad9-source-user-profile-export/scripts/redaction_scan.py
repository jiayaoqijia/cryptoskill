#!/usr/bin/env python3
"""Flag anything in an export document that must not leave the machine.

Usage: python3 redaction_scan.py <file.md>
Exit code 1 if any category is hit, so it can gate a send.
"""
import re
import sys

CHECKS = {
    "wallet address": r"0x[0-9a-fA-F]{6,}",
    "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "url": r"https?://",
    "long number": r"\b\d{5,}\b",
    "filesystem path": r"(/home/|~/\.hermes|\.hermes/)",
    "credential word": r"(api[ _]?key|secret|token|private key|seed phrase|mnemonic|password)",
    "broker/exchange": r"\b(Binance|Stockbit|Ajaib|BCA|Mandiri|BRI|Gmail|Indodax|Tokocrypto)\b",
    "chat/user id": r"\b\d{9,12}\b",
    "handle": r"@\w{3,}",
}


def main(path: str) -> int:
    text = open(path, encoding="utf-8").read()
    hits = 0
    for name, pattern in CHECKS.items():
        found = re.findall(pattern, text, re.I)
        if found:
            hits += len(found)
            sample = ", ".join(dict.fromkeys(map(str, found)))[:120]
            print(f"HIT  {name}: {sample}")
    print(f"\nchars={len(text)} words={len(text.split())} flagged={hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: redaction_scan.py <file.md>")
    sys.exit(main(sys.argv[1]))
