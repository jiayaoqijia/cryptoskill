#!/usr/bin/env python3
"""Measure what an MCP server costs in context BEFORE registering it.

Usage:
    python3 mcp_context_cost.py -- npx -y <pkg>@<ver> mcp
    python3 mcp_context_cost.py --url https://host/mcp --bearer TOKEN   # remote HTTP

Prints, for the real advertised tool list:
  * tool count
  * full-schema size (chars -> ~tokens at 4 chars/token): the cost if every
    schema is loaded eagerly into the prompt
  * deferred-catalog size (name + first ~120 chars of description): the cost
    when the client lists tools but only fetches schemas on demand
  * the heaviest tools by description size (usually the real hogs)

Decision rule of thumb: >100 tools means default to enabled:false and flip the
server on only for the task that needs it.
"""
import argparse
import json
import subprocess
import sys
import urllib.request


def stdio_session(cmd, calls, timeout=240):
    proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, text=True,
    )
    payload = "\n".join(json.dumps(m) for m in calls) + "\n"
    out, _ = proc.communicate(payload, timeout=timeout)
    msgs = []
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                msgs.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return msgs


def http_session(url, calls, bearer=None, timeout=120):
    hdrs = {
        "content-type": "application/json",
        "accept": "application/json, text/event-stream",
    }
    if bearer:
        hdrs["authorization"] = f"Bearer {bearer}"
    msgs = []
    for body in calls:
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(), headers=hdrs, method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                line = line[5:].strip()
            if line.startswith("{"):
                try:
                    msgs.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return msgs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url")
    ap.add_argument("--bearer")
    ap.add_argument("cmd", nargs="*")
    args = ap.parse_args()

    calls = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                    "clientInfo": {"name": "cost-probe", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    ]

    if args.url:
        msgs = http_session(args.url, calls, args.bearer)
    elif args.cmd:
        msgs = stdio_session(args.cmd, calls)
    else:
        ap.error("pass --url or a command after --")

    tools, server = [], None
    for m in msgs:
        if m.get("id") == 1:
            server = m.get("result", {}).get("serverInfo")
        if m.get("id") == 2:
            tools = m.get("result", {}).get("tools", [])
    if not tools:
        print("no tools/tools-list response — server rejected the handshake", file=sys.stderr)
        return 1

    full = 0
    deferred = 0
    rows = []
    for t in tools:
        desc = t.get("description") or ""
        full += len(json.dumps({k: t.get(k) for k in ("name", "description", "inputSchema")}))
        deferred += len(t["name"]) + min(len(desc), 120) + 8
        rows.append((len(desc), t["name"]))

    print(f"server      : {server}")
    print(f"tools       : {len(tools)}")
    print(f"full schema : {full:,} chars  ~{full // 4:,} tokens (eager load)")
    print(f"deferred    : {deferred:,} chars  ~{deferred // 4:,} tokens per turn")
    print("heaviest by description:")
    for n, name in sorted(rows, reverse=True)[:8]:
        print(f"  {n:6d}  {name}")
    if len(tools) > 100:
        print("verdict     : >100 tools — register disabled, enable per task")
    return 0


if __name__ == "__main__":
    sys.exit(main())
