#!/usr/bin/env python3
"""Alchemy CLI — Alchemy — blockchain data, NFTs, token balances, transactions, gas prices, and webhooks.

Zero dependencies beyond Python stdlib.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

API_BASE = "https://eth-mainnet.g.alchemy.com/v2/{api_key}"


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
    api_key = get_env("ALCHEMY_API_KEY")
    if not api_key:
        print("Error: ALCHEMY_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    base = f"https://eth-mainnet.g.alchemy.com/v2/{api_key}"
    headers = {}
    url = f"{base}{path}"
    if params:
        qs = urllib.parse.urlencode({k: v for k, v in params.items() if v}, doseq=True)
        url = f"{url}{'&' if '?' in url else '?'}{qs}"
    return req(method, url, data=data, headers=headers)


def out(data):
    print(json.dumps(data, indent=2, default=str))


def cmd_get_balance(args):
    """Get ETH balance"""
    path = "/"
    data = {}
    if args.address:
        data["address"] = args.address
    result = api("POST", path, data=data)
    out(result)

def cmd_get_token_balances(args):
    """Get ERC-20 token balances"""
    path = "/"
    data = {}
    if args.address:
        data["address"] = args.address
    result = api("POST", path, data=data)
    out(result)

def cmd_get_transaction(args):
    """Get transaction by hash"""
    path = "/"
    data = {}
    if args.hash:
        data["hash"] = args.hash
    result = api("POST", path, data=data)
    out(result)

def cmd_get_block(args):
    """Get block by number"""
    path = "/"
    data = {}
    if args.block:
        data["block"] = args.block
    result = api("POST", path, data=data)
    out(result)

def cmd_get_nfts(args):
    """Get NFTs for address"""
    path = "/getNFTs?owner={address}"
    path = path.replace("{address}", str(args.address or ""))
    result = api("GET", path)
    out(result)

def cmd_get_nft_metadata(args):
    """Get NFT metadata"""
    path = "/getNFTMetadata?contractAddress={contract}&tokenId={token_id}"
    path = path.replace("{contract}", str(args.contract or ""))
    path = path.replace("{token-id}", str(args.token_id or ""))
    params = {}
    if args.token_id:
        params["token-id"] = args.token_id
    result = api("GET", path, params=params)
    out(result)

def cmd_get_token_metadata(args):
    """Get token metadata"""
    path = "/"
    data = {}
    if args.contract:
        data["contract"] = args.contract
    result = api("POST", path, data=data)
    out(result)

def cmd_get_gas_price(args):
    """Get current gas price"""
    path = "/"
    data = {}
    result = api("POST", path, data=data)
    out(result)

def cmd_get_block_number(args):
    """Get latest block number"""
    path = "/"
    data = {}
    result = api("POST", path, data=data)
    out(result)

def cmd_get_logs(args):
    """Get event logs"""
    path = "/"
    data = {}
    if args.address:
        data["address"] = args.address
    if args.from_block:
        data["from-block"] = args.from_block
    if args.to_block:
        data["to-block"] = args.to_block
    if args.topics:
        data["topics"] = args.topics
    result = api("POST", path, data=data)
    out(result)

def cmd_get_asset_transfers(args):
    """Get asset transfers for address"""
    path = "/"
    data = {}
    if args.address:
        data["address"] = args.address
    if args.category:
        data["category"] = args.category
    result = api("POST", path, data=data)
    out(result)

def cmd_get_floor_price(args):
    """Get NFT floor price"""
    path = "/getFloorPrice?contractAddress={contract}"
    path = path.replace("{contract}", str(args.contract or ""))
    result = api("GET", path)
    out(result)


def main():
    parser = argparse.ArgumentParser(description="Alchemy CLI")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    p_get_balance = sub.add_parser("get-balance", help="Get ETH balance")
    p_get_balance.add_argument("--address", required=True)
    p_get_balance.set_defaults(func=cmd_get_balance)

    p_get_token_balances = sub.add_parser("get-token-balances", help="Get ERC-20 token balances")
    p_get_token_balances.add_argument("--address", required=True)
    p_get_token_balances.set_defaults(func=cmd_get_token_balances)

    p_get_transaction = sub.add_parser("get-transaction", help="Get transaction by hash")
    p_get_transaction.add_argument("--hash", required=True)
    p_get_transaction.set_defaults(func=cmd_get_transaction)

    p_get_block = sub.add_parser("get-block", help="Get block by number")
    p_get_block.add_argument("--block", default="latest")
    p_get_block.set_defaults(func=cmd_get_block)

    p_get_nfts = sub.add_parser("get-nfts", help="Get NFTs for address")
    p_get_nfts.add_argument("--address", required=True)
    p_get_nfts.set_defaults(func=cmd_get_nfts)

    p_get_nft_metadata = sub.add_parser("get-nft-metadata", help="Get NFT metadata")
    p_get_nft_metadata.add_argument("--contract", required=True)
    p_get_nft_metadata.add_argument("--token-id", required=True)
    p_get_nft_metadata.set_defaults(func=cmd_get_nft_metadata)

    p_get_token_metadata = sub.add_parser("get-token-metadata", help="Get token metadata")
    p_get_token_metadata.add_argument("--contract", required=True)
    p_get_token_metadata.set_defaults(func=cmd_get_token_metadata)

    p_get_gas_price = sub.add_parser("get-gas-price", help="Get current gas price")
    p_get_gas_price.set_defaults(func=cmd_get_gas_price)

    p_get_block_number = sub.add_parser("get-block-number", help="Get latest block number")
    p_get_block_number.set_defaults(func=cmd_get_block_number)

    p_get_logs = sub.add_parser("get-logs", help="Get event logs")
    p_get_logs.add_argument("--address", required=True)
    p_get_logs.add_argument("--from-block", default="0x0")
    p_get_logs.add_argument("--to-block", default="latest")
    p_get_logs.add_argument("--topics", required=True)
    p_get_logs.set_defaults(func=cmd_get_logs)

    p_get_asset_transfers = sub.add_parser("get-asset-transfers", help="Get asset transfers for address")
    p_get_asset_transfers.add_argument("--address", required=True)
    p_get_asset_transfers.add_argument("--category", default="external,erc20")
    p_get_asset_transfers.set_defaults(func=cmd_get_asset_transfers)

    p_get_floor_price = sub.add_parser("get-floor-price", help="Get NFT floor price")
    p_get_floor_price.add_argument("--contract", required=True)
    p_get_floor_price.set_defaults(func=cmd_get_floor_price)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
