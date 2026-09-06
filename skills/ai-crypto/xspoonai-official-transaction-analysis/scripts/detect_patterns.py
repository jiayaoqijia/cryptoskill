#!/usr/bin/env python3
"""
Detect Patterns Script
Identifies recurring patterns and anomalies in transaction behavior.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict, Counter
from dotenv import load_dotenv

load_dotenv()


class PatternDetector:
    """Detect patterns and anomalies in blockchain transactions."""

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

    def detect_patterns(self, address: str) -> Dict:
        """Detect patterns and anomalies in transaction behavior."""
        address = address.lower()
        transactions = self.get_transactions(address)
        token_transfers = self.get_token_transfers(address)

        if not transactions and not token_transfers:
            return {
                "error": "No transactions found",
                "address": address,
                "chain": self.chain
            }

        patterns = []

        # 1. Detect recurring transfers
        recurring = self._detect_recurring_transfers(address, transactions, token_transfers)
        patterns.extend(recurring)

        # 2. Detect unusual large transactions
        unusual = self._detect_unusual_transactions(address, transactions, token_transfers)
        patterns.extend(unusual)

        # 3. Detect time-based patterns
        time_patterns = self._detect_time_patterns(transactions)
        patterns.extend(time_patterns)

        # 4. Detect frequent counterparties
        frequent = self._detect_frequent_counterparties(address, transactions)
        patterns.extend(frequent)

        return {
            "address": address,
            "chain": self.chain,
            "patterns_detected": len(patterns),
            "patterns": patterns
        }

    def _detect_recurring_transfers(self, address: str, transactions: List[Dict], token_transfers: List[Dict]) -> List[Dict]:
        """Detect recurring transfer patterns."""
        patterns = []

        # Check token transfers for recurring patterns
        token_counterparties = defaultdict(list)
        for tx in token_transfers:
            counterparty = tx["to"] if tx["from"].lower() == address else tx["from"]
            token_symbol = tx["tokenSymbol"]
            key = f"{token_symbol}:{counterparty}"
            token_counterparties[key].append({
                "timestamp": int(tx["timeStamp"]),
                "value": int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))
            })

        for key, transfers in token_counterparties.items():
            if len(transfers) >= 3:  # At least 3 transfers
                token, counterparty = key.split(":", 1)
                avg_value = sum(t["value"] for t in transfers) / len(transfers)

                # Check if transfers are regular (similar amounts)
                values = [t["value"] for t in transfers]
                if max(values) / min(values) < 2:  # Values within 2x range
                    patterns.append({
                        "type": "recurring_transfer",
                        "description": f"Regular {token} transfers to/from {counterparty[:10]}...",
                        "frequency": f"{len(transfers)} times",
                        "average_amount": f"{avg_value:.6f} {token}",
                        "severity": "low"
                    })

        return patterns

    def _detect_unusual_transactions(self, address: str, transactions: List[Dict], token_transfers: List[Dict]) -> List[Dict]:
        """Detect unusually large transactions."""
        patterns = []

        # Analyze ETH transactions
        eth_values = [int(tx["value"]) / 1e18 for tx in transactions if int(tx["value"]) > 0]
        if eth_values:
            avg_eth = sum(eth_values) / len(eth_values)
            for tx in transactions[:20]:  # Check recent 20 transactions
                value = int(tx["value"]) / 1e18
                if value > avg_eth * 10:  # 10x larger than average
                    patterns.append({
                        "type": "unusual_activity",
                        "description": f"Large ETH transfer ({value:.4f} ETH) detected",
                        "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])).isoformat(),
                        "transaction_hash": tx["hash"],
                        "severity": "high" if value > avg_eth * 50 else "medium"
                    })

        # Analyze token transfers
        token_values = defaultdict(list)
        for tx in token_transfers:
            token = tx["tokenSymbol"]
            decimals = int(tx["tokenDecimal"]) if tx["tokenDecimal"] else 18
            value = int(tx["value"]) / (10 ** decimals)
            token_values[token].append((value, tx))

        for token, values in token_values.items():
            if len(values) < 3:
                continue
            amounts = [v[0] for v in values]
            avg_amount = sum(amounts) / len(amounts)

            for value, tx in values[:10]:  # Check recent 10
                if value > avg_amount * 10:
                    patterns.append({
                        "type": "unusual_activity",
                        "description": f"Large {token} transfer ({value:.4f}) detected",
                        "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])).isoformat(),
                        "transaction_hash": tx["hash"],
                        "severity": "medium"
                    })

        return patterns

    def _detect_time_patterns(self, transactions: List[Dict]) -> List[Dict]:
        """Detect time-based patterns (e.g., regular intervals)."""
        patterns = []

        if len(transactions) < 5:
            return patterns

        # Group by day of week
        day_counts = Counter()
        hour_counts = Counter()

        for tx in transactions:
            dt = datetime.fromtimestamp(int(tx["timeStamp"]))
            day_counts[dt.strftime("%A")] += 1
            hour_counts[dt.hour] += 1

        # Find most active day
        if day_counts:
            most_active_day, count = day_counts.most_common(1)[0]
            if count > len(transactions) * 0.3:  # More than 30% on one day
                patterns.append({
                    "type": "time_pattern",
                    "description": f"Most transactions occur on {most_active_day}",
                    "frequency": f"{count} transactions ({count/len(transactions)*100:.1f}%)",
                    "severity": "low"
                })

        # Find most active hour
        if hour_counts:
            most_active_hour, count = hour_counts.most_common(1)[0]
            if count > len(transactions) * 0.2:  # More than 20% in one hour
                patterns.append({
                    "type": "time_pattern",
                    "description": f"Most transactions occur around {most_active_hour}:00",
                    "frequency": f"{count} transactions ({count/len(transactions)*100:.1f}%)",
                    "severity": "low"
                })

        return patterns

    def _detect_frequent_counterparties(self, address: str, transactions: List[Dict]) -> List[Dict]:
        """Detect frequently interacting addresses."""
        patterns = []

        counterparties = Counter()
        for tx in transactions:
            counterparty = tx["to"] if tx["from"].lower() == address else tx["from"]
            counterparties[counterparty] += 1

        # Find top counterparties
        for counterparty, count in counterparties.most_common(3):
            if count >= 5:  # At least 5 interactions
                patterns.append({
                    "type": "frequent_counterparty",
                    "description": f"Frequent interactions with {counterparty[:10]}...",
                    "frequency": f"{count} transactions",
                    "counterparty": counterparty,
                    "severity": "low"
                })

        return patterns


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python detect_patterns.py <address> [chain]")
        print("Example: python detect_patterns.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum")
        sys.exit(1)

    address = sys.argv[1]
    chain = sys.argv[2] if len(sys.argv) > 2 else "ethereum"

    try:
        detector = PatternDetector(chain)
        result = detector.detect_patterns(address)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
