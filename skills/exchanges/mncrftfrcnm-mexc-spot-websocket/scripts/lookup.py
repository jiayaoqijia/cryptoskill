#!/usr/bin/env python3
"""Print one local MEXC Spot WebSocket reference slice."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STREAMS = ROOT / "references" / "streams.md"
SECTION_ALIASES = {
    "Bases": "base url websocket endpoint public private",
    "Public Streams": "public stream trade ticker depth kline book protobuf",
    "Private Streams": "private listen key listenkey account order balance user data",
    "Depth And Order Books": "depth order book snapshot sequence gap version",
    "Lifecycle And Limits": "ping pong reconnect limit subscribe unsubscribe lifecycle",
}


def read_reference() -> str:
    if not STREAMS.exists():
        raise SystemExit(f"Missing reference file: {STREAMS}")
    return STREAMS.read_text(encoding="utf-8")


def sections(markdown: str) -> dict[str, str]:
    result: dict[str, list[str]] = {}
    current = "Overview"
    result[current] = []
    for line in markdown.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            result[current] = [line]
        else:
            result.setdefault(current, []).append(line)
    return {name: "\n".join(lines).strip() for name, lines in result.items()}


def choose_section(topic: str, available: dict[str, str]) -> str:
    normalized = topic.lower().strip()
    if not normalized:
        return "Overview"
    for section in available:
        if normalized == section.lower():
            return section
    for section, aliases in SECTION_ALIASES.items():
        haystack = f"{section} {aliases}".lower()
        if any(part in haystack for part in normalized.split()):
            if section in available:
                return section
    for section, body in available.items():
        if normalized in body.lower():
            return section
    raise SystemExit(
        "No matching Spot WebSocket section. Available sections: "
        + ", ".join(available)
    )


def main(argv: list[str]) -> int:
    topic = " ".join(argv[1:]).strip()
    available = sections(read_reference())
    section = choose_section(topic, available)
    print(available[section])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
