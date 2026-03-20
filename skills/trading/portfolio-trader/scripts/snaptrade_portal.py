#!/usr/bin/env python3
import json
import os
import sys
from typing import Any, Dict

from snaptrade_common import load_config, save_config, get_client


def pick_user_id(cfg: Dict[str, Any]) -> str:
    user_id = cfg.get("user_id")
    if user_id:
        return user_id
    # generate a random user_id on first run
    import uuid
    user_id = str(uuid.uuid4())
    cfg["user_id"] = user_id
    return user_id


def ensure_user(cfg: Dict[str, Any]) -> Dict[str, Any]:
    client = get_client(cfg)
    user_id = pick_user_id(cfg)
    if cfg.get("user_secret"):
        return cfg
    # register user
    resp = client.authentication.register_snap_trade_user(user_id=user_id)
    body = getattr(resp, "body", resp)
    # body may be dict-like
    user_secret = None
    if isinstance(body, dict):
        user_secret = body.get("userSecret") or body.get("user_secret")
    else:
        # try attribute access
        user_secret = getattr(body, "user_secret", None) or getattr(body, "userSecret", None)
    if not user_secret:
        raise RuntimeError("Failed to retrieve user_secret from SnapTrade response")
    cfg["user_secret"] = user_secret
    save_config(cfg)
    return cfg


def create_portal_link(cfg: Dict[str, Any]) -> str:
    client = get_client(cfg)
    user_id = cfg["user_id"]
    user_secret = cfg["user_secret"]
    resp = client.authentication.login_snap_trade_user(
        user_id=user_id,
        user_secret=user_secret,
        connection_type="read",
        connection_portal_version="v4",
        immediate_redirect=False,
        show_close_button=True,
    )
    body = getattr(resp, "body", resp)
    if isinstance(body, dict):
        url = body.get("redirectURI") or body.get("redirect_uri")
    else:
        url = getattr(body, "redirectURI", None) or getattr(body, "redirect_uri", None)
    if not url:
        raise RuntimeError("Failed to retrieve connection portal URL from response")
    return url


def main():
    cfg = load_config()
    cfg = ensure_user(cfg)
    url = create_portal_link(cfg)
    print(url)


if __name__ == "__main__":
    main()
