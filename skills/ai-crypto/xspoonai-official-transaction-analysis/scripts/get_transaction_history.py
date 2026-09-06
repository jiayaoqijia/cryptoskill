#!/usr/bin/env python3
"""
Get Transaction History Script
Retrieves complete transaction history for a given address on Ethereum or Polygon.
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class TransactionHistoryAnalyzer:
    """Analyze transaction history for blockchain addresses."""

    def __init__(self, chain: str = "ethereum"):
        self.chain = chain.lower()

        if self.chain == "ethereum":
            self.api_key = os.getenv("ETHERSCAN_API_KEY")
            self.api_url = "https://api.etherscan.io/api"
            self.rpc_url = os.getenv("ETHEREUM_RPC", "https://eth.llamarpc.com")
        elif self.chain == "polygon":
            self.api_key = os.getenv("POLYGONSCAN_API_KEY")
            self.api_url = "https://api.polygonscan.com/api"
            self.rpc_url = os.getenv("POLYGON_RPC", "https://polygon.llamarpc.com")
        else:
            raise ValueError(f"Unsupported chain: {chain}")

        if not self.api_key:
            raise ValueError(f"API key not found for {chain}")

    def get_transactions(self, address: str, start_block: int = 0, end_block: int = 99999999) -> List[Dict]:
        """Get all transactions for an address."""
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "sort": "desc",
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data["status"] == "1":
                return data["result"]
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}", file=sys.stderr)
                return []
        except Exception as e:
            print(f"Error fetching transactions: {e}", file=sys.stderr)
            return []

    def analyze_transactions(self, address: str) -> Dict:
        """Analyze transaction history and return summary."""
        address = address.lower()
        transactions = self.get_transactions(address)

        if not transactions:
            return {
                "error": "No transactions found or API error",
                "address": address,
                "chain": self.chain
            }

        # Calculate statistics
        total_txs = len(transactions)
        sent_txs = [tx for tx in transactions if tx["from"].lower() == address]
        received_txs = [tx for tx in transactions if tx["to"].lower() == address]

        total_eth_sent = sum(int(tx["value"]) for tx in sent_txs) / 1e18
        total_eth_received = sum(int(tx["value"]) for tx in received_txs) / 1e18
        total_gas_used = sum(int(tx["gasUsed"]) * int(tx["gasPrice"]) for tx in sent_txs) / 1e18

        # Get first and last transaction timestamps
        first_tx = transactions[-1] if transactions else None
        last_tx = transactions[0] if transactions else None

        first_tx_date = datetime.fromtimestamp(int(first_tx["timeStamp"])).isoformat() if first_tx else None
        last_tx_date = datetime.fromtimestamp(int(last_tx["timeStamp"])).isoformat() if last_tx else None

        # Find most frequent counterparties
        counterparties = {}
        for tx in transactions:
            counterparty = tx["to"] if tx["from"].lower() == address else tx["from"]
            counterparties[counterparty] = counterparties.get(counterparty, 0) + 1

        top_counterparties = sorted(counterparties.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "address": address,
            "chain": self.chain,
            "summary": {
                "total_transactions": total_txs,
                "sent_transactions": len(sent_txs),
                "received_transactions": len(received_txs),
                "first_transaction": first_tx_date,
                "last_transaction": last_tx_date,
                "total_eth_sent": f"{total_eth_sent:.6f}",
                "total_eth_received": f"{total_eth_received:.6f}",
                "net_eth_balance_change": f"{(total_eth_received - total_eth_sent):.6f}",
                "total_gas_spent": f"{total_gas_used:.6f}"
            },
            "top_counterparties": [
                {"address": addr, "transaction_count": count}
                for addr, count in top_counterparties
            ],
            "recent_transactions": [
                {
                    "hash": tx["hash"],
                    "from": tx["from"],
                    "to": tx["to"],
                    "value": f"{int(tx['value']) / 1e18:.6f}",
                    "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])).isoformat(),
                    "status": "success" if tx["txreceipt_status"] == "1" else "failed"
                }
                for tx in transactions[:10]
            ]
        }


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python get_transaction_history.py <address> [chain]")
        print("Example: python get_transaction_history.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum")
        sys.exit(1)

    address = sys.argv[1]
    chain = sys.argv[2] if len(sys.argv) > 2 else "ethereum"

    try:
        analyzer = TransactionHistoryAnalyzer(chain)
        result = analyzer.analyze_transactions(address)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
