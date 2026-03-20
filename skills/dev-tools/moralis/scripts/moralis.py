#!/usr/bin/env python3
"""Moralis CLI — Moralis — Web3 data, token prices, wallet history, NFTs, DeFi positions, and blockchain events.

Zero dependencies beyond Python stdlib.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

API_BASE = "https://deep-index.moralis.io/api/v2.2"


def get_env(name):
    val = os.environ.get(name, "")
    if not val:
        env_path = os.path.join(os.environ.get("WORKSPACE", os.path.expanduser("~/.openclaw/workspace")), ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(name + "="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
    return val


def req(method, url, data=None, headers=None, timeout=30):
    body = json.dumps(data).encode() if data else None
    r = urllib.request.Request(url, data=body, method=method)
    r.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            r.add_header(k, v)
    try:
        resp = urllib.request.urlopen(r, timeout=timeout)
        raw = resp.read().decode()
        return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(json.dumps({"error": True, "code": e.code, "message": err}), file=sys.stderr)
        sys.exit(1)


def api(method, path, data=None, params=None):
    """Make authenticated API request."""
    base = API_BASE
    token = get_env("MORALIS_API_KEY")
    if not token:
        print("Error: MORALIS_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{base}{path}"
    if params:
        qs = urllib.parse.urlencode({k: v for k, v in params.items() if v}, doseq=True)
        url = f"{url}{'&' if '?' in url else '?'}{qs}"
    return req(method, url, data=data, headers=headers)


def out(data):
    print(json.dumps(data, indent=2, default=str))


def cmd_get_native_balance(args):
    """Get native balance"""
    path = "/{address}/balance"
    path = path.replace("{address}", str(args.address or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_get_token_balances(args):
    """Get ERC-20 token balances"""
    path = "/{address}/erc20"
    path = path.replace("{address}", str(args.address or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_get_transactions(args):
    """Get wallet transactions"""
    path = "/{address}"
    path = path.replace("{address}", str(args.address or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_get_token_price(args):
    """Get token price"""
    path = "/erc20/{address}/price"
    path = path.replace("{address}", str(args.address or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_get_nfts(args):
    """Get NFTs for wallet"""
    path = "/{address}/nft"
    path = path.replace("{address}", str(args.address or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_get_nft_metadata(args):
    """Get NFT metadata"""
    path = "/nft/{address}/{token_id}"
    path = path.replace("{address}", str(args.address or ""))
    path = path.replace("{token-id}", str(args.token_id or ""))
    params = {}
    if args.token_id:
        params["token-id"] = args.token_id
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_get_nft_transfers(args):
    """Get NFT transfers"""
    path = "/nft/{address}/transfers"
    path = path.replace("{address}", str(args.address or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_get_token_transfers(args):
    """Get token transfers"""
    path = "/{address}/erc20/transfers"
    path = path.replace("{address}", str(args.address or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_get_defi_positions(args):
    """Get DeFi positions"""
    path = "/wallets/{address}/defi/positions"
    path = path.replace("{address}", str(args.address or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)

def cmd_resolve_domain(args):
    """Resolve ENS/Unstoppable domain"""
    path = "/resolve/{domain}"
    path = path.replace("{domain}", str(args.domain or ""))
    result = api("GET", path)
    out(result)

def cmd_search_token(args):
    """Search token by symbol"""
    path = "/erc20/metadata?symbols={symbol}"
    path = path.replace("{symbol}", str(args.symbol or ""))
    result = api("GET", path)
    out(result)

def cmd_get_block(args):
    """Get block details"""
    path = "/block/{block}"
    path = path.replace("{block}", str(args.block or ""))
    params = {}
    if args.chain:
        params["chain"] = args.chain
    result = api("GET", path, params=params)
    out(result)


def main():
    parser = argparse.ArgumentParser(description="Moralis CLI")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    p_get_native_balance = sub.add_parser("get-native-balance", help="Get native balance")
    p_get_native_balance.add_argument("--address", required=True)
    p_get_native_balance.add_argument("--chain", default="eth")
    p_get_native_balance.set_defaults(func=cmd_get_native_balance)

    p_get_token_balances = sub.add_parser("get-token-balances", help="Get ERC-20 token balances")
    p_get_token_balances.add_argument("--address", required=True)
    p_get_token_balances.add_argument("--chain", default="eth")
    p_get_token_balances.set_defaults(func=cmd_get_token_balances)

    p_get_transactions = sub.add_parser("get-transactions", help="Get wallet transactions")
    p_get_transactions.add_argument("--address", required=True)
    p_get_transactions.add_argument("--chain", default="eth")
    p_get_transactions.set_defaults(func=cmd_get_transactions)

    p_get_token_price = sub.add_parser("get-token-price", help="Get token price")
    p_get_token_price.add_argument("--address", required=True)
    p_get_token_price.add_argument("--chain", default="eth")
    p_get_token_price.set_defaults(func=cmd_get_token_price)

    p_get_nfts = sub.add_parser("get-nfts", help="Get NFTs for wallet")
    p_get_nfts.add_argument("--address", required=True)
    p_get_nfts.add_argument("--chain", default="eth")
    p_get_nfts.set_defaults(func=cmd_get_nfts)

    p_get_nft_metadata = sub.add_parser("get-nft-metadata", help="Get NFT metadata")
    p_get_nft_metadata.add_argument("--address", required=True)
    p_get_nft_metadata.add_argument("--token-id", required=True)
    p_get_nft_metadata.add_argument("--chain", default="eth")
    p_get_nft_metadata.set_defaults(func=cmd_get_nft_metadata)

    p_get_nft_transfers = sub.add_parser("get-nft-transfers", help="Get NFT transfers")
    p_get_nft_transfers.add_argument("--address", required=True)
    p_get_nft_transfers.add_argument("--chain", default="eth")
    p_get_nft_transfers.set_defaults(func=cmd_get_nft_transfers)

    p_get_token_transfers = sub.add_parser("get-token-transfers", help="Get token transfers")
    p_get_token_transfers.add_argument("--address", required=True)
    p_get_token_transfers.add_argument("--chain", default="eth")
    p_get_token_transfers.set_defaults(func=cmd_get_token_transfers)

    p_get_defi_positions = sub.add_parser("get-defi-positions", help="Get DeFi positions")
    p_get_defi_positions.add_argument("--address", required=True)
    p_get_defi_positions.add_argument("--chain", default="eth")
    p_get_defi_positions.set_defaults(func=cmd_get_defi_positions)

    p_resolve_domain = sub.add_parser("resolve-domain", help="Resolve ENS/Unstoppable domain")
    p_resolve_domain.add_argument("--domain", required=True)
    p_resolve_domain.set_defaults(func=cmd_resolve_domain)

    p_search_token = sub.add_parser("search-token", help="Search token by symbol")
    p_search_token.add_argument("--symbol", required=True)
    p_search_token.set_defaults(func=cmd_search_token)

    p_get_block = sub.add_parser("get-block", help="Get block details")
    p_get_block.add_argument("--block", required=True)
    p_get_block.add_argument("--chain", default="eth")
    p_get_block.set_defaults(func=cmd_get_block)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
