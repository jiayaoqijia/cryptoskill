#!/usr/bin/env python3
import json
from snaptrade_common import load_config
from snaptrade_client.api_client import ApiClient
from snaptrade_client.configuration import Configuration
from snaptrade_client.apis.paths.snap_trade_partners import SnapTradePartners


def main():
    cfg = load_config()
    config = Configuration(client_id=cfg.get("client_id"), consumer_key=cfg.get("consumer_key"))
    api_client = ApiClient(config)
    partners = SnapTradePartners(api_client)
    resp = partners.get()
    body = getattr(resp, "body", resp)
    allowed = body.get("allowed_brokerages") if isinstance(body, dict) else None
    if not allowed:
        print("[]")
        return
    # Return a simple list of broker display names
    names = []
    for b in allowed:
        name = b.get("display_name") or b.get("name")
        if name:
            names.append(name)
    print(json.dumps(sorted(names), indent=2))


if __name__ == "__main__":
    main()
