#!/usr/bin/env python3
"""Probe a stdio MCP server: does it handshake, and how many tools does it REALLY advertise?

Usage:
    python3 mcp_handshake_probe.py npx -y some-pkg@1.2.3 mcp
    python3 mcp_handshake_probe.py python3 /path/to/server.py --flag

Why: README tool counts and "works with your agent" claims are marketing. This proves the server speaks
JSON-RPC over stdio (what `hermes mcp add <name> --command <cmd> --args ...` needs) and prints the runtime
tool list, so you can enable a relevant SUBSET instead of every tool (each tool costs context in every
future session).

Exit: 0 = handshake OK, 1 = no handshake / server died, 2 = usage error.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time

INIT_TIMEOUT = 120


def read_message(proc: subprocess.Popen, timeout: float):
    """Read one JSON-RPC object from stdout (stdio transport is newline-delimited)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            if proc.poll() is not None:
                return None
            time.sleep(0.05)
            continue
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return None


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1:]
    print(f"spawning: {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    rc = 1
    try:
        def send(obj):
            proc.stdin.write(json.dumps(obj) + "\n")
            proc.stdin.flush()

        send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
              "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                         "clientInfo": {"name": "mcp-handshake-probe", "version": "1.0"}}})
        init = read_message(proc, INIT_TIMEOUT)
        if not (init and "result" in init):
            print("initialize FAILED:", json.dumps(init)[:300] if init else "no reply")
            return rc
        print("initialize ok")
        print("serverInfo:", json.dumps(init["result"].get("serverInfo", {}))[:200])
        print("protocolVersion:", init["result"].get("protocolVersion"))

        send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        listing = read_message(proc, INIT_TIMEOUT)
        if not (listing and "result" in listing):
            print("tools/list FAILED:", json.dumps(listing)[:300] if listing else "no reply")
            return rc

        names = [t.get("name", "?") for t in listing["result"].get("tools", [])]
        print(f"tools advertised at runtime: {len(names)}")
        for n in names[:15]:
            print("  -", n)
        if len(names) > 15:
            print(f"  ... (+{len(names) - 15} more)")
        rc = 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        err = (proc.stderr.read() or "")[:400]
        if err and rc != 0:
            print("server stderr:", err)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
