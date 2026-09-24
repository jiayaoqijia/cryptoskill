from __future__ import annotations

import fcntl
import glob
import http.client
import json
import os
import socket
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, Optional
from urllib.parse import quote, urlparse


@dataclass(frozen=True)
class RouteStatus:
    active: bool
    selector: str
    proxy: str
    error: Optional[str] = None


def route_prefix_for_url(url: str) -> Optional[str]:
    host = (urlparse(url).hostname or "").lower()
    if host == "binance.com" or host.endswith(".binance.com"):
        return "BINANCE"
    if host == "bybit.com" or host.endswith(".bybit.com"):
        return "BYBIT"
    return None


class _UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, socket_path: Path, timeout: int = 5) -> None:
        super().__init__("localhost", timeout=timeout)
        self.socket_path = socket_path

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(str(self.socket_path))


def _controller_request(
    socket_path: Path,
    method: str,
    endpoint: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    body = None if payload is None else json.dumps(payload, separators=(",", ":")).encode("utf-8")
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    conn = _UnixHTTPConnection(socket_path)
    try:
        conn.request(method, endpoint, body=body, headers=headers)
        response = conn.getresponse()
        raw = response.read()
        if response.status >= 400:
            detail = raw.decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"Mihomo controller HTTP {response.status}: {detail[:200]}")
        return json.loads(raw.decode("utf-8")) if raw else {}
    finally:
        conn.close()


def _discover_socket(explicit: str = "") -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if path.is_socket():
            return path
        raise RuntimeError("configured Mihomo control socket is unavailable")
    candidates = [Path(p) for p in glob.glob("/tmp/mihomo-party-*.sock")]
    candidates = [p for p in candidates if p.is_socket()]
    if not candidates:
        raise RuntimeError("Mihomo Party control socket was not found")
    return max(candidates, key=lambda p: p.stat().st_mtime)


@contextmanager
def optional_mihomo_route(env_prefix: str = "BYBIT") -> Iterator[RouteStatus]:
    """Temporarily select one Mihomo proxy and always restore the prior selector."""

    mode = (os.getenv(f"{env_prefix}_MIHOMO_MODE") or "auto").strip().lower()
    if mode not in {"auto", "off", "required"}:
        raise RuntimeError(f"{env_prefix}_MIHOMO_MODE must be auto, off, or required")
    selector = (os.getenv(f"{env_prefix}_MIHOMO_SELECTOR") or "GLOBAL").strip()
    proxy = (os.getenv(f"{env_prefix}_MIHOMO_PROXY") or "JP-Dedicated-B1-1").strip()
    if mode == "off" or not proxy:
        yield RouteStatus(False, selector, proxy)
        return

    switched = False
    previous = ""
    lock_file = None
    socket_path = Path()
    selector_path = ""
    lock_path = Path(os.getenv(f"{env_prefix}_MIHOMO_LOCK") or "/tmp/cex-daily-mihomo-route.lock")
    try:
        socket_path = _discover_socket((os.getenv(f"{env_prefix}_MIHOMO_SOCKET") or "").strip())
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_file = lock_path.open("a+", encoding="utf-8")
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        selector_path = f"/proxies/{quote(selector, safe='')}"
        current = _controller_request(socket_path, "GET", selector_path)
        previous = str(current.get("now") or "")
        choices = current.get("all") if isinstance(current.get("all"), list) else []
        if not previous:
            raise RuntimeError(f"Mihomo selector {selector!r} has no current proxy")
        if proxy not in choices:
            raise RuntimeError(f"Mihomo proxy {proxy!r} is not available in selector {selector!r}")
        target = _controller_request(socket_path, "GET", f"/proxies/{quote(proxy, safe='')}")
        if target.get("alive") is False:
            raise RuntimeError(f"Mihomo proxy {proxy!r} is not alive")
        if previous != proxy:
            _controller_request(socket_path, "PUT", selector_path, {"name": proxy})
            switched = True
            selected = _controller_request(socket_path, "GET", selector_path)
            if selected.get("now") != proxy:
                raise RuntimeError(f"Mihomo selector {selector!r} did not switch to {proxy!r}")
    except Exception as exc:
        if lock_file is not None:
            if switched and previous:
                try:
                    _controller_request(socket_path, "PUT", selector_path, {"name": previous})
                except Exception:
                    pass
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            lock_file.close()
        if mode == "required":
            raise
        yield RouteStatus(False, selector, proxy, str(exc))
        return

    try:
        yield RouteStatus(True, selector, proxy)
    finally:
        try:
            if switched:
                _controller_request(socket_path, "PUT", selector_path, {"name": previous})
        finally:
            if lock_file is not None:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                lock_file.close()


@contextmanager
def optional_url_route(url: str) -> Iterator[RouteStatus]:
    prefix = route_prefix_for_url(url)
    if prefix is None:
        yield RouteStatus(False, "", "")
        return
    with optional_mihomo_route(prefix) as status:
        yield status
