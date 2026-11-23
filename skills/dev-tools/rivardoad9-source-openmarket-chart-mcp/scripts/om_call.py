#!/usr/bin/env python3
"""Minimal OpenMarket MCP client for Hermes (uses the stored OAuth token).

Run with the venv that carries mcp 2.0 (see the skill's section 3).

Usage:
  om_call.py <tool> ['{"json":"args"}'] [<tool2> '{}' ...]
Prints each tool result as JSON (structuredContent first, then text content).
"""
from __future__ import annotations

import asyncio
import json
import sys
import time
from pathlib import Path

TOKENS = Path.home() / ".hermes" / "mcp-tokens"
URL = "https://mcp.openmarket.xyz/"
NAME = "openmarket"


def load_token() -> str:
    data = json.loads((TOKENS / f"{NAME}.json").read_text())
    exp = float(data.get("expires_at") or 0)
    if exp and exp - time.time() < 120:
        data = refresh(data)
    return data["access_token"]


def refresh(data: dict) -> dict:
    import httpx

    meta = json.loads((TOKENS / f"{NAME}.meta.json").read_text())
    client = json.loads((TOKENS / f"{NAME}.client.json").read_text())
    r = httpx.post(
        meta["token_endpoint"],
        data={
            "grant_type": "refresh_token",
            "refresh_token": data["refresh_token"],
            "client_id": client["client_id"],
            "resource": URL,
        },
        timeout=30,
    )
    r.raise_for_status()
    new = r.json()
    data.update(
        access_token=new["access_token"],
        refresh_token=new.get("refresh_token", data.get("refresh_token")),
        expires_in=new.get("expires_in"),
        expires_at=time.time() + float(new.get("expires_in") or 0),
        scope=new.get("scope", data.get("scope")),
    )
    (TOKENS / f"{NAME}.json").write_text(json.dumps(data, indent=2))
    (TOKENS / f"{NAME}.json").chmod(0o600)
    return data


def render(res) -> str:
    out = []
    sc = getattr(res, "structuredContent", None)
    if sc:
        out.append(json.dumps(sc, indent=2, ensure_ascii=False))
    for c in getattr(res, "content", []) or []:
        txt = getattr(c, "text", None)
        if txt:
            out.append(txt)
    if getattr(res, "isError", False):
        out.append("[isError=true]")
    return "\n".join(out) if out else json.dumps(str(res))


async def main(pairs: list[tuple[str, dict]]) -> None:
    import httpx2
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    token = load_token()
    async with httpx2.AsyncClient(headers={"Authorization": f"Bearer {token}"}, timeout=60) as http:
        async with streamable_http_client(URL, http_client=http) as (r, w):
            async with ClientSession(r, w) as session:
                await session.initialize()
                for tool, args in pairs:
                    res = await session.call_tool(tool, args)
                    print(f"=== {tool} {json.dumps(args, ensure_ascii=False)} ===")
                    print(render(res))
                    print()


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        sys.exit(1)
    items: list[tuple[str, dict]] = []
    i = 0
    while i < len(argv):
        tool = argv[i]
        if i + 1 < len(argv) and argv[i + 1].strip().startswith("{"):
            args = json.loads(argv[i + 1])
            i += 2
        else:
            args = {}
            i += 1
        items.append((tool, args))
    asyncio.run(main(items))
