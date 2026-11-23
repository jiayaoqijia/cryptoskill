#!/usr/bin/env python3
"""Template: localhost dashboard server (stdlib only).

Copy to ~/.hermes/scripts/<tool>_server.py, point SCAN/HTML/CONFIG at your data source,
then expose with templates/service_keeper.sh (cloudflared quick tunnel + cron).

Routes:  /  and  /<NAME>  -> page      /api/<data> -> JSON      /api/refresh -> force JSON
         /healthz -> {"ok":bool,"age_s":float}   (the keeper script polls this)
Env:     <TOOL>_PORT (default 8787) · <TOOL>_TTL (seconds, default 60) · <TOOL>_TOKEN ('' = open)
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

NAME = "zemiztracker"                       # public route name: /zemiztracker
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.expanduser("~"), ".hermes", "data")
HTML = os.path.join(HERE, "dashboard.html")  # self-contained page, no CDN
HISTORY = os.path.join(DATA, "dashboard_history.jsonl")
SCANNER = os.path.join(HERE, "scan.py")      # CLI tool whose functions we reuse
PORT = int(os.environ.get("DASH_PORT", "8787"))
TTL = int(os.environ.get("DASH_TTL", "60"))
TOKEN = os.environ.get("DASH_TOKEN", "").strip()
MAX_HISTORY = 576                            # ~24h at 2.5 min
WIB = timezone(timedelta(hours=7))
STATE: dict = {"data": None, "rows": [], "ts": 0.0, "err": None, "fetches": 0}
LOCK = threading.Lock()


def _load(path: str):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"tidak bisa load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scan() -> dict:
    """Pull fresh data. Reuse the CLI tool's own helpers so the page and the alerts agree."""
    tool = _load(SCANNER)
    cfg = json.load(open(os.path.join(DATA, "dashboard_config.json"), encoding="utf-8"))
    with ThreadPoolExecutor(max_workers=8) as ex:          # small pool: 54 HTTP reads in ~1.3s
        rows = [r for r in ex.map(lambda w: tool.fetch_one(w), cfg["items"]) if r]
    return {"summary": tool.aggregate(rows, cfg), "rows": rows}


def _append_history(agg: dict) -> None:
    try:
        with open(HISTORY, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ts": datetime.now(WIB).strftime("%Y-%m-%d %H:%M"),
                                 "value": round(float(agg.get("bias_pct", 0)), 2)}) + "\n")
        lines = open(HISTORY, encoding="utf-8").read().splitlines()[-MAX_HISTORY:]
        open(HISTORY, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    except Exception:
        pass


def refresh(force: bool = False) -> None:
    with LOCK:
        if not force and STATE["data"] and (time.time() - STATE["ts"]) < TTL:
            return
        try:
            res = scan()
            STATE.update(data=res["summary"], rows=res["rows"], ts=time.time(),
                         err=None, fetches=STATE["fetches"] + 1)
            _append_history(res["summary"])
        except Exception as exc:  # noqa: BLE001 - surface it in the page footer instead of dying
            STATE["err"] = f"{type(exc).__name__}: {exc}"[:200]


def _background() -> None:
    while True:
        try:
            refresh()
        except Exception:
            pass
        time.sleep(5)


def snapshot(force: bool = False) -> dict:
    refresh(force=force)
    with LOCK:
        return {"ok": STATE["err"] is None and STATE["data"] is not None, "error": STATE["err"],
                "age_s": round(time.time() - STATE["ts"], 1) if STATE["ts"] else None,
                "fetches": STATE["fetches"], "ttl_s": TTL, "name": NAME,
                "history": [json.loads(x) for x in
                            open(HISTORY, encoding="utf-8").read().splitlines()[-288:] if x.strip()]
                if os.path.exists(HISTORY) else [],
                "rows": STATE["rows"], "data": STATE["data"]}


class Handler(BaseHTTPRequestHandler):
    server_version = "LocalhostDashboard/1.0"

    def _ok_token(self, qs: dict) -> bool:
        if not TOKEN:
            return True
        return (qs.get("k") or [""])[0] == TOKEN or self.headers.get("X-Board-Token") == TOKEN

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")      # phone browsers cache hard
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_HEAD(self):  # noqa: N802
        self.do_GET()

    def do_GET(self):  # noqa: N802
        u = urlparse(self.path)
        qs = parse_qs(u.query)
        if not self._ok_token(qs):
            self._send(403, b"forbidden", "text/plain; charset=utf-8")
            return
        if u.path in ("/", "/index.html", f"/{NAME}"):
            self._send(200, open(HTML, encoding="utf-8").read().encode(), "text/html; charset=utf-8")
        elif u.path == "/api/data":
            self._send(200, json.dumps(snapshot(), ensure_ascii=False).encode(), "application/json")
        elif u.path == "/api/refresh":
            self._send(200, json.dumps(snapshot(force=True), ensure_ascii=False).encode(),
                       "application/json")
        elif u.path == "/healthz":
            self._send(200, json.dumps({"ok": STATE["err"] is None,
                                        "age_s": round(time.time() - STATE["ts"], 1) if STATE["ts"] else None,
                                        "name": NAME}).encode(), "application/json")
        else:
            self._send(404, b"not found", "text/plain; charset=utf-8")

    def log_message(self, format, *a):  # noqa: A002 - signature follows stdlib
        if "/healthz" in (self.path or ""):
            return                                          # keeper polls it; don't flood the log
        sys.stderr.write("[dash] %s %s\n" % (self.command, urlparse(self.path).path))


def main() -> int:
    threading.Thread(target=_background, daemon=True).start()
    print(f"[dash] live http://127.0.0.1:{PORT}/{NAME} · ttl {TTL}s · token "
          f"{'ON' if TOKEN else 'off'}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()   # 127.0.0.1 ONLY
    return 0


if __name__ == "__main__":
    sys.exit(main())
