#!/usr/bin/env python3
"""Probe an MCP server's stdio handshake before registering it with an agent runtime.

Why: a repo's docs can advertise N tools while the published build exposes fewer, or fails to start
at all. One cheap handshake proves what you are actually wiring in — and the real tool count is also
the context cost you will pay in every future session.

Usage:
    python3 mcp_stdio_probe.py -- npx -y <pkg>@1.2.3 mcp
    python3 mcp_stdio_probe.py -- node ./server.js --stdio

Prints serverInfo (name/version), protocolVersion, capabilities, the real tool count and the first
N tool names, plus a stderr tail. Exit 0 when initialize succeeded, 2 when it did not.
Read-only: sends initialize + tools/list and calls no tools.
"""
from __future__ import annotations

import json
import subprocess
import sys
import threading
import time

TIMEOUT = 120        # seconds for the whole handshake (npx cold start can be slow)
PRINT_TOOLS = 20     # how many tool names to show


def main() -> int:
    args = sys.argv[1:]
    if "--" in args:
        args = args[args.index("--") + 1:]
    if not args:
        print(__doc__)
        return 2

    print("cmd:", " ".join(args), flush=True)
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)

    def _kill_later():
        time.sleep(TIMEOUT)
        try:
            proc.terminate()
        except Exception:
            pass

    threading.Thread(target=_kill_later, daemon=True).start()
    err_lines: list[str] = []
    threading.Thread(
        target=lambda: [err_lines.append(ln.rstrip()) for ln in proc.stderr],
        daemon=True).start()

    def send(obj: dict) -> None:
        try:
            proc.stdin.write(json.dumps(obj) + "\n")
            proc.stdin.flush()
        except Exception as exc:                      # server died early
            err_lines.append(f"<stdin closed: {exc}>")

    def read_reply(rid: int, budget: int = 2000):
        """Read stdout until the response with matching id arrives."""
        for _ in range(budget):
            line = proc.stdout.readline()
            if not line:
                return None
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                msg = json.loads(line)
            except Exception:
                continue
            if msg.get("id") == rid:
                return msg
        return None

    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                     "clientInfo": {"name": "hermes-probe", "version": "1.0"}}})
    init = read_reply(1)
    if not init:
        print("initialize: FAILED")
        print("stderr tail:", "\n".join(err_lines[-12:]) or "(empty)")
        return 2

    res = init.get("result") or {}
    info = res.get("serverInfo") or {}
    print(f"initialize: OK — {info.get('name')} {info.get('version')}")
    print(f"protocolVersion: {res.get('protocolVersion')}")
    print(f"capabilities: {sorted((res.get('capabilities') or {}).keys())}")

    send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    tools = (((read_reply(2) or {}).get("result")) or {}).get("tools") or []
    print(f"tools: {len(tools)}")
    for t in tools[:PRINT_TOOLS]:
        desc = (t.get("description") or "").strip().splitlines()
        print(f"  - {t.get('name')}" + (f"  · {desc[0][:80]}" if desc else ""))
    if len(tools) > PRINT_TOOLS:
        print(f"  … +{len(tools) - PRINT_TOOLS} more (filter in Python/jq, don't paste the whole list)")

    print("\nhint: report the count + a handful of names, not the full schema dump.")
    print("stderr tail:", "\n".join(err_lines[-8:]) or "(empty)")

    try:
        proc.terminate()
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
