#!/usr/bin/env python3
"""
Analyze Counterparties Script
Identifies and analyzes frequent transaction counterparties.
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


class CounterpartyAnalyzer:
    """Analyze transaction counterparties for blockchain addresses."""

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

    def analyze_counterparties(self, address: str) -> Dict:
        """Analyze transaction counterparties and relationships."""
        address = address.lower()
        transactions = self.get_transactions(address)
        token_transfers = self.get_token_transfers(address)

        if not transactions and not token_transfers:
            return {
                "error": "No transactions found",
                "address": address,
                "chain": self.chain
            }

        # Analyze ETH transaction counterparties
        eth_counterparties = defaultdict(lambda: {
            "sent_count": 0,
            "received_count": 0,
            "sent_value": 0,
            "received_value": 0,
            "first_interaction": None,
            "last_interaction": None
        })

        for tx in transactions:
            counterparty = tx["to"] if tx["from"].lower() == address else tx["from"]
            if not counterparty:
                continue

            value = int(tx["value"]) / 1e18
            timestamp = datetime.fromtimestamp(int(tx["timeStamp"])).isoformat()

            if tx["from"].lower() == address:
                eth_counterparties[counterparty]["sent_count"] += 1
                eth_counterparties[counterparty]["sent_value"] += value
            else:
                eth_counterparties[counterparty]["received_count"] += 1
                eth_counterparties[counterparty]["received_value"] += value

            if not eth_counterparties[counterparty]["first_interaction"]:
                eth_counterparties[counterparty]["first_interaction"] = timestamp
            eth_counterparties[counterparty]["last_interaction"] = timestamp

        # Analyze token transfer counterparties
        token_counterparties = defaultdict(lambda: defaultdict(lambda: {
            "sent_count": 0,
            "received_count": 0,
            "sent_value": 0,
            "received_value": 0
        }))

        for tx in token_transfers:
            counterparty = tx["to"] if tx["from"].lower() == address else tx["from"]
            token = tx["tokenSymbol"]
            decimals = int(tx["tokenDecimal"]) if tx["tokenDecimal"] else 18
            value = int(tx["value"]) / (10 ** decimals)

            if tx["from"].lower() == address:
                token_counterparties[counterparty][token]["sent_count"] += 1
                token_counterparties[counterparty][token]["sent_value"] += value
            else:
                token_counterparties[counterparty][token]["received_count"] += 1
                token_counterparties[counterparty][token]["received_value"] += value

        # Format ETH counterparties
        eth_counterparty_list = []
        for cp, data in eth_counterparties.items():
            total_interactions = data["sent_count"] + data["received_count"]
            eth_counterparty_list.append({
                "address": cp,
                "total_interactions": total_interactions,
                "sent_transactions": data["sent_count"],
                "received_transactions": data["received_count"],
                "total_eth_sent": f"{data['sent_value']:.6f}",
                "total_eth_received": f"{data['received_value']:.6f}",
                "net_eth_flow": f"{(data['received_value'] - data['sent_value']):.6f}",
                "first_interaction": data["first_interaction"],
                "last_interaction": data["last_interaction"],
                "relationship_type": self._classify_relationship(data)
            })

        # Sort by total interactions
        eth_counterparty_list.sort(key=lambda x: x["total_interactions"], reverse=True)

        # Format token counterparties
        token_counterparty_list = []
        for cp, tokens in token_counterparties.items():
            for token, data in tokens.items():
                total_interactions = data["sent_count"] + data["received_count"]
                if total_interactions >= 2:  # Only include if at least 2 interactions
                    token_counterparty_list.append({
                        "address": cp,
                        "token": token,
                        "total_interactions": total_interactions,
                        "sent_transactions": data["sent_count"],
                        "received_transactions": data["received_count"],
                        "total_sent": f"{data['sent_value']:.6f}",
                        "total_received": f"{data['received_value']:.6f}",
                        "net_flow": f"{(data['received_value'] - data['sent_value']):.6f}"
                    })

        token_counterparty_list.sort(key=lambda x: x["total_interactions"], reverse=True)

        # Identify relationship patterns
        patterns = self._identify_patterns(eth_counterparty_list, token_counterparty_list)

        return {
            "address": address,
            "chain": self.chain,
            "summary": {
                "unique_eth_counterparties": len(eth_counterparties),
                "unique_token_counterparties": len(token_counterparties),
                "total_eth_transactions": len(transactions),
                "total_token_transfers": len(token_transfers)
            },
            "top_eth_counterparties": eth_counterparty_list[:10],
            "top_token_counterparties": token_counterparty_list[:10],
            "relationship_patterns": patterns
        }

    def _classify_relationship(self, data: Dict) -> str:
        """Classify the type of relationship based on transaction patterns."""
        sent = data["sent_count"]
        received = data["received_count"]
        total = sent + received

        if total == 1:
            return "one-time"
        elif sent == 0:
            return "sender-only"
        elif received == 0:
            return "recipient-only"
        elif abs(sent - received) / total < 0.2:
            return "bidirectional"
        elif sent > received * 2:
            return "primarily-outgoing"
        else:
            return "primarily-incoming"

    def _identify_patterns(self, eth_counterparties: List[Dict], token_counterparties: List[Dict]) -> List[Dict]:
        """Identify interesting patterns in counterparty relationships."""
        patterns = []

        # Find most active counterparty
        if eth_counterparties:
            most_active = eth_counterparties[0]
            if most_active["total_interactions"] >= 10:
                patterns.append({
                    "type": "highly_active_counterparty",
                    "description": f"Very frequent interactions with {most_active['address'][:10]}...",
                    "details": f"{most_active['total_interactions']} transactions",
                    "relationship": most_active["relationship_type"]
                })

        # Find one-sided relationships
        one_sided = [cp for cp in eth_counterparties if cp["relationship_type"] in ["sender-only", "recipient-only"]]
        if len(one_sided) > len(eth_counterparties) * 0.5:
            patterns.append({
                "type": "one_sided_relationships",
                "description": "Most counterparties have one-directional relationships",
                "details": f"{len(one_sided)} out of {len(eth_counterparties)} counterparties"
            })

        # Find token-specific relationships
        token_specific = defaultdict(set)
        for cp in token_counterparties:
            token_specific[cp["token"]].add(cp["address"])

        for token, addresses in token_specific.items():
            if len(addresses) >= 5:
                patterns.append({
                    "type": "token_ecosystem",
                    "description": f"Active in {token} ecosystem",
                    "details": f"Interacts with {len(addresses)} different addresses for {token}"
                })

        return patterns


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_counterparties.py <address> [chain]")
        print("Example: python analyze_counterparties.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum")
        sys.exit(1)

    address = sys.argv[1]
    chain = sys.argv[2] if len(sys.argv) > 2 else "ethereum"

    try:
        analyzer = CounterpartyAnalyzer(chain)
        result = analyzer.analyze_counterparties(address)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
