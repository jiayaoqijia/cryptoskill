#!/usr/bin/env python3
"""Minimal Stitch MCP client (JSON-RPC over HTTP) for when the server is not
registered as a Hermes tool yet.

Usage:
  python3 stitch_rpc.py list
  python3 stitch_rpc.py call <tool> '<json args>'
  python3 stitch_rpc.py push-html <screen resource name> <file.html>
  python3 stitch_rpc.py screenshot <file resource name> <out.png>

Key is read from ~/.hermes/secrets/stitch_api_key (mode 600) or $STITCH_API_KEY.
"""
import base64
import json
import os
import sys
import urllib.request

URL = "https://stitch.googleapis.com/mcp"


def api_key():
    k = os.environ.get("STITCH_API_KEY")
    if k:
        return k.strip()
    path = os.path.expanduser("~/.hermes/secrets/stitch_api_key")
    return open(path).read().strip()


def rpc(method, params=None, rid=1, timeout=300):
    body = json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(URL, data=body, method="POST")
    for k, v in {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "X-Goog-Api-Key": api_key(),
    }.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode()
    if raw.startswith("event:") or raw.startswith("data:"):
        raw = "\n".join(l[5:].strip() for l in raw.splitlines() if l.startswith("data:"))
    return json.loads(raw)


def call(tool, args, timeout=300):
    if not getattr(call, "_init", False):
        rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                           "clientInfo": {"name": "hermes", "version": "1"}})
        call._init = True
    r = rpc("tools/call", {"name": tool, "arguments": args}, timeout=timeout)
    if "error" in r:
        raise SystemExit(json.dumps(r["error"])[:500])
    res = r.get("result", {})
    return res.get("structuredContent") or res


def push_html(screen_name, path):
    html = open(path, "rb").read()
    return call("update_screen", {
        "name": screen_name,
        "htmlCodeBase64": base64.b64encode(html).decode(),
        "updateMask": ["html_code"],
    })


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    cmd = argv[1]
    if cmd == "list":
        tools = rpc("tools/list", {}, 2).get("result", {}).get("tools", [])
        for t in tools:
            print(t["name"], "|", (t.get("description") or "").split("\n")[0][:80])
    elif cmd == "call":
        print(json.dumps(call(argv[2], json.loads(argv[3])), ensure_ascii=False)[:4000])
    elif cmd == "push-html":
        print(json.dumps(push_html(argv[2], argv[3]), ensure_ascii=False)[:800])
    elif cmd == "screenshot":
        res = call("download_file", {"name": argv[2]})
        data = res.get("data") or res.get("content", [{}])[0].get("data")
        open(argv[3], "wb").write(base64.b64decode(data))
        print("written", argv[3], os.path.getsize(argv[3]))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
