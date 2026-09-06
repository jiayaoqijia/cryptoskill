#!/usr/bin/env python3
"""
Analyze Fund Flow Script
Tracks ETH and token movements to identify fund flow patterns.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()


class FundFlowAnalyzer:
    """Analyze fund flows for blockchain addresses."""

    def __init__(self, chain: str = "ethereum"):
        self.chain = chain.lower()

        if self.chain == "ethereum":
            self.api_key = os.getenv("ETHERSCAN_API_KEY")
            self.api_url = "https://api.etherscan.io/api"
        elif self.chain == "polygon":
            self.api_key = os.getenv("POLYGONSCAN_API_KEY")
            self.api_url = "https://api.polygonscan.com/api"
        else:
            raise ValueError(f"Unsupported chain: {chain}")

        if not self.api_key:
            raise ValueError(f"API key not found for {chain}")

    def get_transactions(self, address: str) -> List[Dict]:
        """Get all transactions for an address."""
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "sort": "desc",
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["result"] if data["status"] == "1" else []
        except Exception as e:
            print(f"Error fetching transactions: {e}", file=sys.stderr)
            return []

    def get_token_transfers(self, address: str) -> List[Dict]:
        """Get token transfers for an address."""
        params = {
            "module": "account",
            "action": "tokentx",
            "address": address,
            "sort": "desc",
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["result"] if data["status"] == "1" else []
        except Exception as e:
            print(f"Error fetching token transfers: {e}", file=sys.stderr)
            return []

    def analyze_fund_flow(self, address: str, days: int = 30) -> Dict:
        """Analyze fund flows over a specified time period."""
        address = address.lower()
        cutoff_time = datetime.now() - timedelta(days=days)
        cutoff_timestamp = int(cutoff_time.timestamp())

        # Get transactions and token transfers
        transactions = self.get_transactions(address)
        token_transfers = self.get_token_transfers(address)

        # Filter by time period
        recent_txs = [tx for tx in transactions if int(tx["timeStamp"]) >= cutoff_timestamp]
        recent_tokens = [tx for tx in token_transfers if int(tx["timeStamp"]) >= cutoff_timestamp]

        # Analyze ETH flows
        eth_inflows = defaultdict(float)
        eth_outflows = defaultdict(float)

        for tx in recent_txs:
            value = int(tx["value"]) / 1e18
            if value > 0:
                if tx["to"].lower() == address:
                    eth_inflows[tx["from"]] += value
                elif tx["from"].lower() == address:
                    eth_outflows[tx["to"]] += value

        # Analyze token flows
        token_inflows = defaultdict(lambda: defaultdict(float))
        token_outflows = defaultdict(lambda: defaultdict(float))

        for tx in recent_tokens:
            token = tx["tokenSymbol"]
            decimals = int(tx["tokenDecimal"]) if tx["tokenDecimal"] else 18
            value = int(tx["value"]) / (10 ** decimals)

            if tx["to"].lower() == address:
                token_inflows[token][tx["from"]] += value
            elif tx["from"].lower() == address:
                token_outflows[token][tx["to"]] += value

        # Top ETH sources and destinations
        top_eth_sources = sorted(eth_inflows.items(), key=lambda x: x[1], reverse=True)[:5]
        top_eth_destinations = sorted(eth_outflows.items(), key=lambda x: x[1], reverse=True)[:5]

        # Top token flows
        token_flow_summary = []
        all_tokens = set(token_inflows.keys()) | set(token_outflows.keys())

        for token in all_tokens:
            total_in = sum(token_inflows[token].values())
            total_out = sum(token_outflows[token].values())

            token_flow_summary.append({
                "token": token,
                "total_received": f"{total_in:.6f}",
                "total_sent": f"{total_out:.6f}",
                "net_flow": f"{(total_in - total_out):.6f}",
                "top_sources": [
                    {"address": addr, "amount": f"{amt:.6f}"}
                    for addr, amt in sorted(token_inflows[token].items(), key=lambda x: x[1], reverse=True)[:3]
                ],
                "top_destinations": [
                    {"address": addr, "amount": f"{amt:.6f}"}
                    for addr, amt in sorted(token_outflows[token].items(), key=lambda x: x[1], reverse=True)[:3]
                ]
            })

        return {
            "address": address,
            "chain": self.chain,
            "analysis_period_days": days,
            "eth_flows": {
                "total_received": f"{sum(eth_inflows.values()):.6f}",
                "total_sent": f"{sum(eth_outflows.values()):.6f}",
                "net_flow": f"{(sum(eth_inflows.values()) - sum(eth_outflows.values())):.6f}",
                "top_sources": [
                    {"address": addr, "amount": f"{amt:.6f}"}
                    for addr, amt in top_eth_sources
                ],
                "top_destinations": [
                    {"address": addr, "amount": f"{amt:.6f}"}
                    for addr, amt in top_eth_destinations
                ]
            },
            "token_flows": token_flow_summary,
            "transaction_count": {
                "eth_transactions": len(recent_txs),
                "token_transfers": len(recent_tokens)
            }
        }


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_fund_flow.py <address> [chain] [days]")
        print("Example: python analyze_fund_flow.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum 30")
        sys.exit(1)

    address = sys.argv[1]
    chain = sys.argv[2] if len(sys.argv) > 2 else "ethereum"
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 30

    try:
        analyzer = FundFlowAnalyzer(chain)
        result = analyzer.analyze_fund_flow(address, days)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
