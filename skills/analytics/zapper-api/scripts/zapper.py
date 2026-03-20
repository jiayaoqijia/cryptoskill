#!/usr/bin/env python3
"""
Zapper CLI
Query DeFi portfolios, NFTs, and transactions via Zapper's GraphQL API
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

CONFIG_FILE = os.path.expanduser("~/.config/zapper/addresses.json")
GRAPHQL_URL = "https://public.zapper.xyz/graphql"


# =============================================================================
# Config & API
# =============================================================================

def get_config():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except:
        return {"wallets": [], "apiKey": None}


def get_api_key():
    return os.environ.get("ZAPPER_API_KEY") or get_config().get("apiKey")


def get_wallets():
    return get_config().get("wallets", [])


def graphql_request(query, variables):
    api_key = get_api_key()
    if not api_key:
        return {"error": "No API key. Set ZAPPER_API_KEY or add apiKey to config."}

    payload = json.dumps({"query": query, "variables": variables}).encode()
    headers = {
        "Content-Type": "application/json",
        "x-zapper-api-key": api_key,
        "User-Agent": "ZapperSkill/1.0"
    }

    try:
        req = urllib.request.Request(GRAPHQL_URL, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            if data.get("errors"):
                return {"error": data["errors"][0].get("message", "GraphQL error")}
            return data
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return {"error": "Access denied - this endpoint may require a paid API tier"}
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def resolve_address(address_or_label):
    """Resolve address from argument or wallet label."""
    if address_or_label and address_or_label.startswith("0x"):
        return [address_or_label]

    wallets = get_wallets()
    if address_or_label:
        # Try to find by label
        for w in wallets:
            if w.get("label", "").lower() == address_or_label.lower():
                return [w["address"]]
        print(f"Error: Wallet '{address_or_label}' not found in config")
        sys.exit(1)

    if wallets:
        return [w["address"] for w in wallets]

    print("No address provided and no wallets configured.")
    print(f"Add wallets to {CONFIG_FILE} or pass an address.")
    sys.exit(1)


# =============================================================================
# Fetch Functions
# =============================================================================

def fetch_portfolio(addresses, limit=10):
    query = """
    query Portfolio($addresses: [Address!]!, $first: Int) {
      portfolioV2(addresses: $addresses) {
        tokenBalances {
          totalBalanceUSD
          byToken(first: $first) {
            totalCount
            edges {
              node {
                name
                symbol
                price
                balance
                balanceUSD
                network { name }
                onchainMarketData {
                  priceChange24h
                  marketCap
                }
              }
            }
          }
        }
        appBalances {
          totalBalanceUSD
          byApp(first: 10) {
            edges {
              node {
                app { displayName }
                balanceUSD
                network { name }
              }
            }
          }
        }
      }
    }
    """
    result = graphql_request(query, {"addresses": addresses, "first": limit})
    if "error" in result:
        return result
    return result.get("data", {}).get("portfolioV2", {})


def fetch_tokens(addresses, limit=20):
    query = """
    query Tokens($addresses: [Address!]!, $first: Int) {
      portfolioV2(addresses: $addresses) {
        tokenBalances {
          totalBalanceUSD
          byToken(first: $first) {
            totalCount
            edges {
              node {
                name
                symbol
                price
                balance
                balanceUSD
                network { name }
                onchainMarketData {
                  priceChange24h
                  marketCap
                }
              }
            }
          }
        }
      }
    }
    """
    result = graphql_request(query, {"addresses": addresses, "first": limit})
    if "error" in result:
        return result
    return result.get("data", {}).get("portfolioV2", {}).get("tokenBalances", {})


def fetch_apps(addresses, limit=20):
    query = """
    query Apps($addresses: [Address!]!, $first: Int) {
      portfolioV2(addresses: $addresses) {
        appBalances {
          totalBalanceUSD
          byApp(first: $first) {
            edges {
              node {
                app { displayName }
                balanceUSD
                network { name }
              }
            }
          }
        }
      }
    }
    """
    result = graphql_request(query, {"addresses": addresses, "first": limit})
    if "error" in result:
        return result
    return result.get("data", {}).get("portfolioV2", {}).get("appBalances", {})


def fetch_nfts(addresses, limit=10):
    query = """
    query NFTs($addresses: [Address!]!, $first: Int) {
      portfolioV2(addresses: $addresses) {
        nftBalances {
          totalBalanceUSD
          totalTokensOwned
          byToken(first: $first, order: {by: USD_WORTH}) {
            edges {
              node {
                token {
                  tokenId
                  name
                  estimatedValue { valueUsd }
                  collection { name address network }
                }
              }
            }
          }
        }
      }
    }
    """
    result = graphql_request(query, {"addresses": addresses, "first": limit})
    if "error" in result:
        return result
    return result.get("data", {}).get("portfolioV2", {}).get("nftBalances", {})


def fetch_transactions(addresses, limit=20):
    end_date = int(time.time() * 1000)
    start_date = end_date - (30 * 24 * 60 * 60 * 1000)  # 30 days

    query = """
    query Transactions($addresses: [Address!]!, $first: Int, $startDate: Timestamp!, $endDate: Timestamp!) {
      transactionHistoryV2(
        subjects: $addresses
        first: $first
        filters: {
          orderByDirection: DESC
          startDate: $startDate
          endDate: $endDate
        }
      ) {
        edges {
          node {
            ... on TimelineEventV2 {
              transaction { hash timestamp network }
              interpretation { processedDescription }
            }
          }
        }
      }
    }
    """
    result = graphql_request(query, {
        "addresses": addresses,
        "first": limit,
        "startDate": start_date,
        "endDate": end_date
    })
    if not result or "error" in result:
        return result or {"error": "No response from API"}
    return result.get("data", {}).get("transactionHistoryV2", {})


def fetch_price(symbol):
    # Common token addresses (Ethereum mainnet)
    TOKEN_ADDRESSES = {
        "ETH": ("0x0000000000000000000000000000000000000000", 1),
        "WETH": ("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", 1),
        "USDC": ("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", 1),
        "USDT": ("0xdac17f958d2ee523a2206206994597c13d831ec7", 1),
        "DAI": ("0x6b175474e89094c44da98b954eedeac495271d0f", 1),
        "WBTC": ("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", 1),
        "LINK": ("0x514910771af9ca656af840dff83e8264ecf986ca", 1),
        "UNI": ("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", 1),
        "AAVE": ("0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9", 1),
        "MKR": ("0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2", 1),
    }

    symbol_upper = symbol.upper()
    if symbol_upper not in TOKEN_ADDRESSES:
        return {"error": f"Unknown token symbol. Supported: {', '.join(TOKEN_ADDRESSES.keys())}"}

    address, chain_id = TOKEN_ADDRESSES[symbol_upper]

    query = """
    query Price($address: Address!, $chainId: Int!) {
      fungibleTokenV2(address: $address, chainId: $chainId) {
        symbol
        name
        priceData {
          price
          priceChange24h
          marketCap
          volume24h
        }
      }
    }
    """
    result = graphql_request(query, {"address": address, "chainId": chain_id})
    if "error" in result:
        return result
    token = result.get("data", {}).get("fungibleTokenV2", {})
    if not token:
        return {"error": "Token not found"}
    price_data = token.get("priceData", {})
    return {
        "symbol": token.get("symbol"),
        "name": token.get("name"),
        "price": price_data.get("price"),
        "priceChange24h": price_data.get("priceChange24h"),
        "marketCap": price_data.get("marketCap"),
        "volume24h": price_data.get("volume24h"),
    }


def fetch_claimables(addresses):
    # Claimables are in positionBalances - look for type containing "claimable"
    query = """
    query Claimables($addresses: [Address!]!) {
      portfolioV2(addresses: $addresses) {
        appBalances {
          byApp(first: 50) {
            edges {
              node {
                app { displayName }
                network { name }
                positionBalances(first: 100) {
                  edges {
                    node {
                      ... on AppTokenPositionBalance {
                        balanceUSD
                        tokens {
                          type
                          symbol
                          balance
                          balanceUSD
                        }
                      }
                      ... on ContractPositionBalance {
                        balanceUSD
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    result = graphql_request(query, {"addresses": addresses})
    if "error" in result:
        return result

    # Extract claimable tokens (type contains "claimable")
    claimables = []
    total_usd = 0

    apps = result.get("data", {}).get("portfolioV2", {}).get("appBalances", {}).get("byApp", {}).get("edges", [])
    for app_edge in apps:
        app_node = app_edge.get("node", {})
        app_name = app_node.get("app", {}).get("displayName", "Unknown")
        network = app_node.get("network", {}).get("name", "")

        positions = app_node.get("positionBalances", {}).get("edges", [])
        for pos_edge in positions:
            pos_node = pos_edge.get("node", {})
            tokens = pos_node.get("tokens", [])

            for t in tokens:
                token_type = t.get("type", "").lower()
                if "claimable" in token_type or "reward" in token_type:
                    value = t.get("balanceUSD", 0)
                    if value > 0.01:  # Skip dust
                        total_usd += value
                        claimables.append({
                            "symbol": t.get("symbol", "?"),
                            "balance": t.get("balance", 0),
                            "balanceUSD": value,
                            "app": app_name,
                            "network": network,
                        })

    return {"totalBalanceUSD": total_usd, "claimables": claimables}


# =============================================================================
# Format Functions
# =============================================================================

def format_portfolio(data, short=False, onchain=False):
    if "error" in data:
        return f"Error: {data['error']}"

    total_tokens = data.get("tokenBalances", {}).get("totalBalanceUSD", 0)
    total_apps = data.get("appBalances", {}).get("totalBalanceUSD", 0)
    total = total_tokens + total_apps

    if short:
        return f"${total:,.2f}"

    lines = [f"Total: ${total:,.2f}"]
    lines.append(f"  Tokens: ${total_tokens:,.2f} | DeFi: ${total_apps:,.2f}")

    tokens = data.get("tokenBalances", {}).get("byToken", {}).get("edges", [])
    if tokens:
        lines.append("\nTokens:")
        for edge in tokens[:10]:
            node = edge.get("node", {})
            symbol = node.get("symbol", "?")
            value = node.get("balanceUSD", 0)
            network = node.get("network", {}).get("name", "")
            if onchain:
                change = (node.get("onchainMarketData") or {}).get("priceChange24h", 0)
                sign = "+" if change > 0 else ""
                lines.append(f"  {symbol}: ${value:,.2f} ({sign}{change:.1f}%) [{network}]")
            else:
                lines.append(f"  {symbol}: ${value:,.2f} [{network}]")

    apps = data.get("appBalances", {}).get("byApp", {}).get("edges", [])
    if apps:
        lines.append("\nDeFi:")
        for edge in apps[:5]:
            node = edge.get("node", {})
            name = node.get("app", {}).get("displayName", "?")
            value = node.get("balanceUSD", 0)
            network = node.get("network", {}).get("name", "")
            lines.append(f"  {name}: ${value:,.2f} [{network}]")

    return "\n".join(lines)


def format_tokens(data, onchain=False):
    if "error" in data:
        return f"Error: {data['error']}"

    total = data.get("totalBalanceUSD", 0)
    count = data.get("byToken", {}).get("totalCount", 0)
    lines = [f"Token Value: ${total:,.2f} ({count} tokens)"]

    tokens = data.get("byToken", {}).get("edges", [])
    if tokens:
        lines.append("")
        for edge in tokens:
            node = edge.get("node", {})
            symbol = node.get("symbol", "?")
            name = node.get("name", "")
            balance = node.get("balance", 0)
            value = node.get("balanceUSD", 0)
            price = node.get("price", 0)
            network = node.get("network", {}).get("name", "")

            if onchain:
                change = (node.get("onchainMarketData") or {}).get("priceChange24h", 0)
                sign = "+" if change > 0 else ""
                lines.append(f"  {symbol}: {balance:,.4f} (${value:,.2f}) @ ${price:.4f} ({sign}{change:.1f}%) [{network}]")
            else:
                lines.append(f"  {symbol}: {balance:,.4f} (${value:,.2f}) @ ${price:.4f} [{network}]")

    return "\n".join(lines)


def format_apps(data):
    if "error" in data:
        return f"Error: {data['error']}"

    total = data.get("totalBalanceUSD", 0)
    lines = [f"DeFi Value: ${total:,.2f}"]

    apps = data.get("byApp", {}).get("edges", [])
    if apps:
        lines.append("")
        for edge in apps:
            node = edge.get("node", {})
            name = node.get("app", {}).get("displayName", "?")
            value = node.get("balanceUSD", 0)
            network = node.get("network", {}).get("name", "")
            lines.append(f"  {name}: ${value:,.2f} [{network}]")
    else:
        lines.append("  No DeFi positions found")

    return "\n".join(lines)


def format_nfts(data):
    if "error" in data:
        return f"Error: {data['error']}"

    total = data.get("totalBalanceUSD", 0)
    count = data.get("totalTokensOwned", "0")
    lines = [f"NFT Value: ${total:,.2f} ({count} tokens)"]

    tokens = data.get("byToken", {}).get("edges", [])
    if tokens:
        lines.append("")
        for edge in tokens:
            token = edge.get("node", {}).get("token", {})
            name = token.get("name", "Unknown")
            token_id = token.get("tokenId", "?")
            value = token.get("estimatedValue", {}).get("valueUsd", 0)
            coll = token.get("collection", {})
            coll_name = coll.get("name", "")
            network = coll.get("network", "")
            lines.append(f"  {coll_name} #{token_id}: ${value:,.2f} [{network}]")
    else:
        lines.append("  No NFTs found")

    return "\n".join(lines)


def format_transactions(data):
    if "error" in data:
        return f"Error: {data['error']}"

    edges = data.get("edges", [])
    if not edges:
        return "No recent transactions"

    lines = ["Recent Transactions (30 days):"]
    for edge in edges:
        node = edge.get("node", {})
        tx = node.get("transaction", {})
        ts_ms = tx.get("timestamp")
        ts = datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M") if ts_ms else ""
        network = tx.get("network", "")
        tx_hash = tx.get("hash", "")[:10] if tx.get("hash") else ""
        desc = node.get("interpretation", {}).get("processedDescription", "")

        if desc:
            lines.append(f"  [{ts}] {desc} [{network}] {tx_hash}...")

    return "\n".join(lines)


def format_price(data):
    if not data or "error" in data:
        return f"Error: {data.get('error', 'Token not found')}"

    symbol = data.get("symbol", "?")
    name = data.get("name", "")
    price = data.get("price", 0)
    change = data.get("priceChange24h", 0)
    mcap = data.get("marketCap", 0)
    volume = data.get("volume24h", 0)

    sign = "+" if change > 0 else ""
    lines = [
        f"{symbol} ({name})",
        f"  Price: ${price:,.6f}" if price < 1 else f"  Price: ${price:,.2f}",
        f"  24h Change: {sign}{change:.2f}%",
    ]
    if mcap:
        lines.append(f"  Market Cap: ${mcap/1e9:.2f}B" if mcap > 1e9 else f"  Market Cap: ${mcap/1e6:.2f}M")
    if volume:
        lines.append(f"  24h Volume: ${volume/1e6:.2f}M")

    return "\n".join(lines)


def format_claimables(data):
    if "error" in data:
        return f"Error: {data['error']}"

    total = data.get("totalBalanceUSD", 0)
    lines = [f"Claimable Rewards: ${total:,.2f}"]

    claimables = data.get("claimables", [])
    if claimables:
        lines.append("")
        for c in claimables:
            symbol = c.get("symbol", "?")
            balance = c.get("balance", 0)
            value = c.get("balanceUSD", 0)
            app = c.get("app", "")
            network = c.get("network", "")
            if isinstance(balance, (int, float)):
                lines.append(f"  {symbol}: {balance:,.4f} (${value:,.2f}) from {app} [{network}]")
            else:
                lines.append(f"  {symbol}: {balance} (${value:,.2f}) from {app} [{network}]")
    else:
        lines.append("  No claimable rewards found")

    return "\n".join(lines)


# =============================================================================
# Command Handlers
# =============================================================================

def cmd_portfolio(args):
    if args.per_wallet:
        wallets = get_wallets()
        if not wallets:
            print("No wallets configured for --per-wallet")
            return
        total_all = 0
        all_data = []
        for w in wallets:
            data = fetch_portfolio([w["address"]], args.limit)
            all_data.append({"wallet": w, "data": data})
            if "error" not in data:
                total_all += data.get("tokenBalances", {}).get("totalBalanceUSD", 0)
                total_all += data.get("appBalances", {}).get("totalBalanceUSD", 0)

        if args.json:
            print(json.dumps(all_data, indent=2))
        else:
            for item in all_data:
                w = item["wallet"]
                addr = w['address']
                print(f"\n{w['label']} ({addr[:8]}...{addr[-6:]})")
                print(format_portfolio(item["data"], onchain=args.show_24h))
            print(f"\nGrand Total: ${total_all:,.2f}")
    else:
        addresses = resolve_address(args.address)
        data = fetch_portfolio(addresses, args.limit)
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(format_portfolio(data, short=args.short, onchain=args.show_24h))


def cmd_tokens(args):
    addresses = resolve_address(args.address)
    data = fetch_tokens(addresses, args.limit)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_tokens(data, onchain=args.show_24h))


def cmd_apps(args):
    addresses = resolve_address(args.address)
    data = fetch_apps(addresses, args.limit)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_apps(data))


def cmd_nfts(args):
    addresses = resolve_address(args.address)
    data = fetch_nfts(addresses, args.limit)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_nfts(data))


def cmd_tx(args):
    addresses = resolve_address(args.address)
    data = fetch_transactions(addresses, args.limit)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_transactions(data))


def cmd_price(args):
    data = fetch_price(args.symbol)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_price(data))


def cmd_claimables(args):
    addresses = resolve_address(args.address)
    data = fetch_claimables(addresses)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_claimables(data))


def cmd_config(args):
    config = get_config()
    api_key = get_api_key()
    print(f"Config: {CONFIG_FILE}")
    print(f"API Key: {'Set' if api_key else 'Missing'}")
    print(f"Wallets: {len(config.get('wallets', []))}")
    for w in config.get('wallets', []):
        addr = w.get('address', '')
        print(f"  - {w.get('label', 'Unnamed')}: {addr[:8]}...{addr[-6:]}")


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Zapper CLI - Query DeFi data across 50+ chains",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  zapper.py portfolio 0x123...          Portfolio summary
  zapper.py tokens 0x123... --24h       Token holdings with 24h change
  zapper.py apps 0x123...               DeFi positions
  zapper.py nfts 0x123...               NFT holdings
  zapper.py tx 0x123...                 Recent transactions
  zapper.py price ETH                   Token price lookup
  zapper.py claimables 0x123...         Unclaimed rewards
  zapper.py config                      Show configuration
"""
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # portfolio
    p = subparsers.add_parser("portfolio", help="Portfolio summary (tokens + DeFi)")
    p.add_argument("address", nargs="?", help="Address or wallet label")
    p.add_argument("--short", action="store_true", help="Show only total value")
    p.add_argument("--per-wallet", action="store_true", help="Show each configured wallet")
    p.add_argument("--24h", dest="show_24h", action="store_true", help="Show 24h price changes")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--limit", type=int, default=10, help="Max tokens to show")
    p.set_defaults(func=cmd_portfolio)

    # tokens
    p = subparsers.add_parser("tokens", help="Token holdings")
    p.add_argument("address", nargs="?", help="Address or wallet label")
    p.add_argument("--24h", dest="show_24h", action="store_true", help="Show 24h price changes")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--limit", type=int, default=20, help="Max tokens to show")
    p.set_defaults(func=cmd_tokens)

    # apps
    p = subparsers.add_parser("apps", help="DeFi positions (LPs, lending, staking)")
    p.add_argument("address", nargs="?", help="Address or wallet label")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--limit", type=int, default=20, help="Max apps to show")
    p.set_defaults(func=cmd_apps)

    # nfts
    p = subparsers.add_parser("nfts", help="NFT holdings")
    p.add_argument("address", nargs="?", help="Address or wallet label")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--limit", type=int, default=10, help="Max NFTs to show")
    p.set_defaults(func=cmd_nfts)

    # tx
    p = subparsers.add_parser("tx", help="Recent transactions")
    p.add_argument("address", nargs="?", help="Address or wallet label")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--limit", type=int, default=20, help="Max transactions to show")
    p.set_defaults(func=cmd_tx)

    # price
    p = subparsers.add_parser("price", help="Token price lookup")
    p.add_argument("symbol", help="Token symbol (e.g., ETH, BTC)")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.set_defaults(func=cmd_price)

    # claimables
    p = subparsers.add_parser("claimables", help="Unclaimed rewards")
    p.add_argument("address", nargs="?", help="Address or wallet label")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.set_defaults(func=cmd_claimables)

    # config
    p = subparsers.add_parser("config", help="Show configuration")
    p.set_defaults(func=cmd_config)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
