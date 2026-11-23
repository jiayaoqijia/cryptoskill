#!/usr/bin/env python3
"""Probe ANY stdio MCP server: handshake + real tool inventory.

Why: README/katalog sering nulis angka yang beda dari yang beneran di-advertise
server (contoh nyata: katalog bilang 131 tool, runtime advertise 125). Angka itu
wajib diukur, bukan dikutip. Sekaligus bukti "bisa nyantol ke Hermes" (protokol
JSON-RPC stdio, sama yang dipakai `hermes mcp add --command ...`).

Usage:
    python3 mcp_stdio_probe.py npx -y rea-agents@4.1.0 mcp
    python3 mcp_stdio_probe.py --grep javascript,web,artifact -- npx -y pkg@1.0.0 mcp
    python3 mcp_stdio_probe.py --timeout 60 -- node ./dist/server.js

Output: serverInfo, protocolVersion, jumlah tool, nama tool yang match --grep
(biar server 125-tool nggak ngebanjirin terminal/konteks), plus satu baris
SUMMARY_JSON buat dikutip di laporan.

Exit code: 124 kalau server nggak jawab (timeout); 0 kalau handshake sukses.
Script ini yang ngebunuh child-nya sendiri di finally (jangan andelin shell).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time


def read_msg(proc: subprocess.Popen, timeout: float):
    """Read the first newline-delimited JSON-RPC message within timeout."""
    end = time.time() + timeout
    while time.time() < end:
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--grep", default="", help="comma-separated keywords to filter tool names")
    ap.add_argument("--timeout", type=float, default=120.0, help="per-message timeout (s)")
    ap.add_argument("--limit", type=int, default=15, help="max filtered tool names to print")
    ap.add_argument("cmd", nargs=argparse.REMAINDER,
                    help="-- server command (e.g. npx -y pkg@1.0.0 mcp)")
    args = ap.parse_args()

    cmd = args.cmd[1:] if args.cmd and args.cmd[0] == "--" else args.cmd
    if not cmd:
        print("error: no server command (use: ... -- npx -y pkg@1.0.0 mcp)", file=sys.stderr)
        return 2

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)

    def send(obj):
        proc.stdin.write(json.dumps(obj) + "\n")
        proc.stdin.flush()

    summary = {"command": " ".join(cmd), "handshake": False, "server_info": None,
               "protocol_version": None, "tool_count": 0, "relevant_tools": []}
    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
              "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                         "clientInfo": {"name": "hermes-probe", "version": "1.0"}}})
        init = read_msg(proc, args.timeout)
        if not (init and "result" in init):
            print("initialize FAILED:", json.dumps(init)[:300] if init else "no reply")
            return 124
        summary["handshake"] = True
        summary["server_info"] = init["result"].get("serverInfo")
        summary["protocol_version"] = init["result"].get("protocolVersion")
        print("initialize ok:", True)
        print("serverInfo:", json.dumps(summary["server_info"])[:200])
        print("protocolVersion:", summary["protocol_version"])

        send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        tl = read_msg(proc, args.timeout)
        if not (tl and "result" in tl):
            print("tools/list FAILED:", json.dumps(tl)[:300] if tl else "no reply")
            return 124
        names = [t.get("name", "") for t in tl["result"].get("tools", [])]
        summary["tool_count"] = len(names)
        print("tools advertised:", len(names))
        for n in names[:10]:
            print("  -", n)
        keys = [k.strip().lower() for k in args.grep.split(",") if k.strip()]
        if keys:
            hit = [n for n in names if any(k in n.lower() for k in keys)]
            summary["relevant_tools"] = hit
            print(f"relevant tools ({'/'.join(keys)}): {json.dumps(hit[:args.limit])}")
        print("SUMMARY_JSON:", json.dumps(summary))
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        err = proc.stderr.read()[:400] if proc.stderr else ""
        if err:
            print("stderr:", err, file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
