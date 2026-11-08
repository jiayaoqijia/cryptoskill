#!/usr/bin/env python3
"""Print one local MEXC Futures REST recipe/reference slice."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELPER = Path(__file__).resolve().with_name("mexc_futures_request.py")
RECIPES = ROOT / "references" / "recipes.md"
ENDPOINTS = ROOT / "references" / "endpoints.md"
SECTION_ALIASES = {
    "Market Data": "market contract public price ticker depth kline funding",
    "Assets And Account": "account asset assets balance balances risk fee",
    "Positions": "position positions leverage margin funding",
    "Orders": "order orders cancel deal externaloid history",
    "Plan, TP/SL, And Trailing Orders": "plan tp sl stoploss takeprofit trailing stoporder planorder",
    "STP And Matching Controls": "stp selftrade prevention matching",
}


def norm(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def sections(text: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    title = ""
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if title:
                found.append((title, "\n".join(body).strip()))
            title = line[3:].strip()
            body = []
        elif title:
            body.append(line)
    if title:
        found.append((title, "\n".join(body).strip()))
    return found


def direct_section_matches(title: str, query: str) -> bool:
    choices = [title, *SECTION_ALIASES.get(title, "").split()]
    return norm(query) in {norm(choice) for choice in choices}


def topic_matches(title: str, body: str, query: str) -> bool:
    return norm(query) in norm(f"{title}\n{body}")


def print_body(body: str) -> None:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and stripped != "```bash" and stripped != "```":
            print(line)


def usage() -> int:
    topics = ", ".join(SECTION_ALIASES)
    print(f"usage: lookup.py <topic-or-search>\ntopics: {topics}")
    return 2


def main() -> int:
    if len(sys.argv) < 2:
        return usage()
    query = " ".join(sys.argv[1:])
    recipe_sections = sections(RECIPES.read_text(encoding="utf-8"))
    matches = [(t, b) for t, b in recipe_sections if direct_section_matches(t, query)]
    if not matches:
        matches = [(t, b) for t, b in recipe_sections if topic_matches(t, b, query)]
    if matches:
        print(f"helper: python {HELPER}")
        for title, body in matches:
            print(f"\n## {title}")
            print_body(body)
        return 0

    endpoint_text = ENDPOINTS.read_text(encoding="utf-8")
    if norm(query) in norm(endpoint_text):
        print(endpoint_text)
        return 0

    print(f"No Futures REST recipe matched: {query}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
