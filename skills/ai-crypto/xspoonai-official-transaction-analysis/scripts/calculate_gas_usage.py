#!/usr/bin/env python3
"""
Calculate Gas Usage Script
Analyzes gas consumption and identifies optimization opportunities.
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()


class GasAnalyzer:
    """Analyze gas usage for blockchain addresses."""

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

    def analyze_gas_usage(self, address: str) -> Dict:
        """Analyze gas usage and provide optimization insights."""
        address = address.lower()
        transactions = self.get_transactions(address)

        # Filter only transactions sent by this address
        sent_txs = [tx for tx in transactions if tx["from"].lower() == address]

        if not sent_txs:
            return {
                "error": "No outgoing transactions found",
                "address": address,
                "chain": self.chain
            }

        # Calculate gas statistics
        total_gas_used = 0
        total_gas_cost = 0
        gas_prices = []
        failed_txs = []

        for tx in sent_txs:
            gas_used = int(tx["gasUsed"])
            gas_price = int(tx["gasPrice"])
            gas_cost = gas_used * gas_price / 1e18

            total_gas_used += gas_used
            total_gas_cost += gas_cost
            gas_prices.append(gas_price / 1e9)  # Convert to Gwei

            if tx["txreceipt_status"] == "0":
                failed_txs.append({
                    "hash": tx["hash"],
                    "gas_wasted": f"{gas_cost:.6f}",
                    "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])).isoformat()
                })

        avg_gas_price = sum(gas_prices) / len(gas_prices) if gas_prices else 0
        min_gas_price = min(gas_prices) if gas_prices else 0
        max_gas_price = max(gas_prices) if gas_prices else 0

        # Identify high gas transactions
        high_gas_txs = []
        for tx in sent_txs[:50]:  # Check recent 50
            gas_cost = int(tx["gasUsed"]) * int(tx["gasPrice"]) / 1e18
            if gas_cost > total_gas_cost / len(sent_txs) * 5:  # 5x average
                high_gas_txs.append({
                    "hash": tx["hash"],
                    "gas_cost": f"{gas_cost:.6f}",
                    "gas_price_gwei": f"{int(tx['gasPrice']) / 1e9:.2f}",
                    "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])).isoformat()
                })

        # Gas optimization recommendations
        recommendations = []

        if avg_gas_price > 50:  # High average gas price
            recommendations.append({
                "type": "timing",
                "description": "Consider transacting during off-peak hours to reduce gas costs",
                "potential_savings": "20-50%"
            })

        if len(failed_txs) > len(sent_txs) * 0.05:  # More than 5% failed
            recommendations.append({
                "type": "transaction_simulation",
                "description": "Use transaction simulation tools to avoid failed transactions",
                "potential_savings": f"{sum(float(tx['gas_wasted']) for tx in failed_txs):.6f} ETH"
            })

        if max_gas_price > avg_gas_price * 3:
            recommendations.append({
                "type": "gas_price_monitoring",
                "description": "Monitor gas prices before transacting to avoid overpaying",
                "potential_savings": "30-70%"
            })

        # Group by contract interaction
        contract_gas = defaultdict(lambda: {"count": 0, "total_gas": 0})
        for tx in sent_txs:
            if tx["to"]:
                contract = tx["to"]
                gas_cost = int(tx["gasUsed"]) * int(tx["gasPrice"]) / 1e18
                contract_gas[contract]["count"] += 1
                contract_gas[contract]["total_gas"] += gas_cost

        top_gas_contracts = sorted(
            [{"contract": k, "transaction_count": v["count"], "total_gas_spent": f"{v['total_gas']:.6f}"}
             for k, v in contract_gas.items()],
            key=lambda x: float(x["total_gas_spent"]),
            reverse=True
        )[:5]

        return {
            "address": address,
            "chain": self.chain,
            "summary": {
                "total_transactions": len(sent_txs),
                "total_gas_used": total_gas_used,
                "total_gas_cost_eth": f"{total_gas_cost:.6f}",
                "average_gas_cost_per_tx": f"{total_gas_cost / len(sent_txs):.6f}",
                "failed_transactions": len(failed_txs),
                "gas_wasted_on_failures": f"{sum(float(tx['gas_wasted']) for tx in failed_txs):.6f}"
            },
            "gas_price_statistics": {
                "average_gwei": f"{avg_gas_price:.2f}",
                "min_gwei": f"{min_gas_price:.2f}",
                "max_gwei": f"{max_gas_price:.2f}"
            },
            "high_gas_transactions": high_gas_txs[:5],
            "failed_transactions": failed_txs[:5],
            "top_gas_consuming_contracts": top_gas_contracts,
            "optimization_recommendations": recommendations
        }


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python calculate_gas_usage.py <address> [chain]")
        print("Example: python calculate_gas_usage.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum")
        sys.exit(1)

    address = sys.argv[1]
    chain = sys.argv[2] if len(sys.argv) > 2 else "ethereum"

    try:
        analyzer = GasAnalyzer(chain)
        result = analyzer.analyze_gas_usage(address)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
