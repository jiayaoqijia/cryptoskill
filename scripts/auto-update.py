#!/usr/bin/env python3
"""Fetch real skill bundles and refresh existing recorded sources.

Run refresh-registry.py --fetch to also rebuild the catalog, scores and site.
No commits, pushes, upstream programs or LLM-generated listings are executed.
"""
from __future__ import annotations

import argparse
import json
import logging
import urllib.parse
from datetime import datetime, timedelta, timezone

from sync_sources import ROOT, fetch, read_json, sync_registry, write_json

OFFICIAL_REPOS = [
    {"org": "binance", "repo": "binance-skills-hub", "category": "exchanges", "prefix": "binance-official-", "skills_dir": "skills"},
    {"org": "okx", "repo": "onchainos-skills", "category": "exchanges", "prefix": "okx-official-", "skills_dir": "skills"},
    {"org": "okx", "repo": "agent-skills", "category": "exchanges", "prefix": "okx-official-", "skills_dir": "skills"},
    {"org": "BitgetLimited", "repo": "agent_hub", "category": "exchanges", "prefix": "bitget-official-", "skills_dir": "skills"},
    {"org": "Kucoin", "repo": "kucoin-skills-hub", "category": "exchanges", "prefix": "kucoin-official-", "skills_dir": "skills"},
    {"org": "krakenfx", "repo": "kraken-cli", "category": "exchanges", "prefix": "kraken-official-", "skills_dir": "skills"},
    {"org": "Uniswap", "repo": "uniswap-ai", "category": "defi", "prefix": "uniswap-official-", "skills_dir": "skills"},
    {"org": "bnb-chain", "repo": "bnbchain-skills", "category": "chains", "prefix": "bnb-official-", "skills_dir": "skills"},
    {"org": "coinbase", "repo": "agentkit", "category": "mcp-servers", "prefix": "coinbase-"},
    {"org": "alchemyplatform", "repo": "alchemy-mcp-server", "category": "mcp-servers", "prefix": "alchemy-"},
    {"org": "solana-foundation", "repo": "solana-mcp-official", "category": "mcp-servers", "prefix": "solana-"},
    {"org": "base", "repo": "base-mcp", "category": "mcp-servers", "prefix": "base-"},
    {"org": "monad-developers", "repo": "monad-mcp", "category": "mcp-servers", "prefix": "monad-"},
    {"org": "aptos-labs", "repo": "aptos-npm-mcp", "category": "mcp-servers", "prefix": "aptos-"},
    {"org": "blockscout", "repo": "mcp-server", "category": "mcp-servers", "prefix": "blockscout-"},
    {"org": "nearai", "repo": "near-mcp", "category": "mcp-servers", "prefix": "near-"},
    {"org": "coingecko", "repo": "coingecko-typescript", "category": "mcp-servers", "prefix": "coingecko-"},
]

# GitHub search queries to discover NEW official crypto skill/MCP repos
GITHUB_SEARCH_QUERIES = [
    "crypto MCP server official language:TypeScript pushed:>{cutoff}",
    "blockchain skills agent official language:TypeScript pushed:>{cutoff}",
    "crypto agent skills language:Python pushed:>{cutoff}",
    "DeFi MCP server pushed:>{cutoff}",
]

# Crypto keyword buckets for detection and categorisation
KEYWORDS = {
    "exchanges": [
        "binance", "okx", "coinbase", "kraken", "bybit", "gate", "bitget",
        "kucoin", "mexc", "hyperliquid", "bitfinex", "crypto.com",
    ],
    "chains": [
        "ethereum", "solana", "bitcoin", "polygon", "arbitrum", "base", "sui",
        "aptos", "monad", "ton", "near", "tron", "starknet", "zksync",
        "avalanche", "cosmos", "polkadot", "cardano", "hedera", "stellar",
        "lightning", "filecoin", "sei", "mantle", "celestia", "blast",
    ],
    "defi": [
        "defi", "swap", "uniswap", "aave", "lido", "compound", "makerdao",
        "curve", "pancakeswap", "raydium", "jupiter", "pump", "sushiswap",
        "opensea", "lending", "liquidity", "yield", "amm",
    ],
    "trading": [
        "trading", "bot", "signal", "arbitrage", "grid", "dca", "whale",
        "sniper", "mev", "alpha",
    ],
    "analytics": [
        "dune", "coingecko", "coinmarketcap", "etherscan", "nansen",
        "defillama", "thegraph", "zapper", "zerion", "debank",
    ],
    "wallets": ["wallet", "metamask", "phantom", "ledger", "trezor", "mpc"],
    "payments": ["x402", "payment", "micropayment"],
    "prediction-markets": ["polymarket", "prediction"],
    "social": ["farcaster", "nostr", "xmtp", "lens"],
    "ai-crypto": ["bittensor", "virtuals", "eliza", "ai-agent", "ai agent"],
    "identity": ["8004", "erc-8004", "identity", "did"],
    "mcp-servers": ["mcp server", "mcp-server"],
}

ALL_CRYPTO_KEYWORDS = []
for kws in KEYWORDS.values():
    ALL_CRYPTO_KEYWORDS.extend(kws)
ALL_CRYPTO_KEYWORDS.extend([
    "crypto", "blockchain", "token", "nft", "staking", "bridge", "oracle",
    "moralis", "alchemy", "foundry", "hardhat", "wagmi", "viem", "web3",
    "on-chain", "onchain",
])


def discover_repositories(lookback_days, watchlist):
    """Keep API-verified candidates separate from executable skill bundles."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).strftime('%Y-%m-%d')
    queries = [(q.format(cutoff=cutoff), None) for q in GITHUB_SEARCH_QUERIES]
    for projects in watchlist.values():
        if not isinstance(projects, list):
            continue
        for project in projects:
            if project.get('github') and project.get('status') in ('missing', 'watch', 'community-only'):
                org = project['github']
                queries.append((f'org:{org} (mcp OR skill OR agent)', org))
    candidates, outcomes = {}, []
    for index, (query, official_org) in enumerate(queries):
        url = 'https://api.github.com/search/repositories?' + urllib.parse.urlencode(
            {'q': query, 'sort': 'updated', 'per_page': 5})
        try:
            data = json.loads(fetch(url, 4 * 1024 * 1024))
            outcomes.append({'query': query, 'status': 'checked'})
            for repo in data.get('items', []):
                if repo.get('archived') or repo.get('fork'):
                    continue
                blob = (repo['name'] + ' ' + (repo.get('description') or '')).lower()
                if not any(word in blob for word in ALL_CRYPTO_KEYWORDS):
                    continue
                owner, name = repo['full_name'].split('/')
                category = 'mcp-servers' if 'mcp' in blob else next(
                    (cat for cat, words in KEYWORDS.items() if any(w in blob for w in words)), 'dev-tools')
                candidates[repo['full_name'].lower()] = {
                    'org': owner, 'repo': name, 'category': category,
                    'prefix': owner.lower() + '-',
                    'official': bool(official_org and owner.lower() == official_org.lower()),
                }
        except Exception as error:
            outcomes.append({'query': query, 'status': 'unavailable', 'detail': str(error)})
            logging.warning('Discovery query unavailable: %s', error)
            # Avoid repeatedly hammering a rate-limited endpoint.
            if getattr(error, 'code', None) in (403, 429):
                outcomes.extend({'query': pending, 'status': 'skipped',
                                 'detail': 'GitHub discovery rate limit reached'}
                                for pending, _ in queries[index + 1:])
                break
    return list(candidates.values()), outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Fetch and validate without writing registry files')
    parser.add_argument('--workers', type=int, default=4, choices=range(1, 9), metavar='1..8')
    parser.add_argument('--repo', help='Refresh one GitHub owner/repository')
    parser.add_argument('--skip-clawhub', '--skip-openclaw', action='store_true', dest='skip_clawhub')
    parser.add_argument('--no-discover', action='store_true', help='Refresh existing entries only')
    parser.add_argument('--discover-github', action='store_true', help='Also search GitHub and missing watchlist projects')
    parser.add_argument('--lookback-days', type=int, default=7)
    parser.add_argument('--no-push', action='store_true', help='Compatibility flag; this command never commits or pushes')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    configs = list(OFFICIAL_REPOS)
    watchlist = read_json(ROOT / 'scripts/watchlist.json')
    for projects in watchlist.values():
        if not isinstance(projects, list):
            continue
        for project in projects:
            repo = project.get('skills_repo')
            if not repo or repo.count('/') != 1:
                continue
            owner, name = repo.split('/')
            if any(r['org'].lower() == owner.lower() and r['repo'].lower() == name.lower() for r in configs):
                continue
            configs.append({'org': owner, 'repo': name, 'category': 'dev-tools', 'prefix': owner.lower() + '-official-'})
    if args.discover_github:
        candidates, outcomes = discover_repositories(args.lookback_days, watchlist)
        known = {f"{r['org']}/{r['repo']}".lower() for r in configs}
        configs.extend(r for r in candidates if f"{r['org']}/{r['repo']}".lower() not in known)
        if not args.dry_run:
            write_json(ROOT / 'docs/discovery-report.json', {'candidates': candidates, 'queries': outcomes})
    report = sync_registry(official_repos=configs, dry_run=args.dry_run, workers=args.workers,
                           only_repo=args.repo, skip_clawhub=args.skip_clawhub, discover=not args.no_discover)
    if not args.dry_run:
        checked_orgs = {repo.split('/')[0].lower() for repo, outcome in report['repositories'].items()
                        if outcome['status'] in ('fetched', 'unchanged')}
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        for projects in watchlist.values():
            if not isinstance(projects, list):
                continue
            for project in projects:
                if (project.get('github') or '').lower() in checked_orgs:
                    project['last_checked'] = today
        write_json(ROOT / 'scripts/watchlist.json', watchlist)
    print(json.dumps(report['summary'], indent=2))
    # A complete network outage must fail CI instead of looking like a clean refresh.
    attempted = list(report['repositories'].values())
    if attempted and all(r['status'] == 'unavailable' for r in attempted):
        raise SystemExit('No upstream repository could be fetched; see docs/sync-report.json')


if __name__ == '__main__':
    main()
