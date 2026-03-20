#!/usr/bin/env python3
import sys
from typing import Any

from snaptrade_common import load_config, get_client


def main():
    cfg = load_config()
    client = get_client(cfg)

    # Find connections
    resp = client.connections.list_brokerage_authorizations(user_id=cfg["user_id"], user_secret=cfg["user_secret"])
    conns = getattr(resp, "body", resp)
    if not isinstance(conns, list):
        conns = list(conns) if conns is not None else []

    connections = []
    disabled = []
    for c in conns:
        disabled_flag = c.get("disabled") if isinstance(c, dict) else getattr(c, "disabled", None)
        brokerage = c.get("brokerage") if isinstance(c, dict) else getattr(c, "brokerage", None)
        name = None
        if isinstance(brokerage, dict):
            name = brokerage.get("display_name") or brokerage.get("name")
        else:
            name = getattr(brokerage, "display_name", None) or getattr(brokerage, "name", None)
        item = {"id": c.get("id") if isinstance(c, dict) else getattr(c, "id", None), "name": name}
        connections.append(item)
        if disabled_flag:
            disabled.append(item)

    if not connections:
        print("NO_CONNECTIONS")
        return

    # If a brokerage name was provided, try to match it from all connections
    target = None
    if len(sys.argv) > 1:
        wanted = sys.argv[1].lower()
        for d in connections:
            if d["name"] and wanted in d["name"].lower():
                target = d
                break
    if target is None:
        # fallback to first disabled, else first connection
        target = disabled[0] if disabled else connections[0]

    resp = client.authentication.login_snap_trade_user(
        user_id=cfg["user_id"],
        user_secret=cfg["user_secret"],
        reconnect=target["id"],
        connection_type="trade",
        connection_portal_version="v4",
        immediate_redirect=False,
        show_close_button=True,
    )
    body = getattr(resp, "body", resp)
    if isinstance(body, dict):
        url = body.get("redirectURI") or body.get("redirect_uri")
    else:
        url = getattr(body, "redirectURI", None) or getattr(body, "redirect_uri", None)
    print(url)


if __name__ == "__main__":
    main()
