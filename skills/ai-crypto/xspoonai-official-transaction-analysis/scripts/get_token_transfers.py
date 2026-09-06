#!/usr/bin/env python3
"""
Get Token Transfers Script
Retrieves ERC20 token transfer history for a given address.
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()


class TokenTransferAnalyzer:
    """Analyze ERC20 token transfers for blockchain addresses."""

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

    def get_token_transfers(self, address: str, contract_address: str = None) -> List[Dict]:
        """Get ERC20 token transfers for an address."""
        params = {
            "module": "account",
            "action": "tokentx",
            "address": address,
            "sort": "desc",
            "apikey": self.api_key
        }

        if contract_address:
            params["contractaddress"] = contract_address

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
            print(f"Error fetching token transfers: {e}", file=sys.stderr)
            return []

    def analyze_token_transfers(self, address: str, contract_address: str = None) -> Dict:
        """Analyze token transfers and return summary."""
        address = address.lower()
        transfers = self.get_token_transfers(address, contract_address)

        if not transfers:
            return {
                "error": "No token transfers found or API error",
                "address": address,
                "chain": self.chain
            }

        # Group by token
        tokens = {}
        for transfer in transfers:
            token_symbol = transfer["tokenSymbol"]
            token_contract = transfer["contractAddress"]
            decimals = int(transfer["tokenDecimal"]) if transfer["tokenDecimal"] else 18

            if token_symbol not in tokens:
                tokens[token_symbol] = {
                    "contract": token_contract,
                    "symbol": token_symbol,
                    "name": transfer["tokenName"],
                    "decimals": decimals,
                    "received": 0,
                    "sent": 0,
                    "transfer_count": 0
                }

            value = int(transfer["value"]) / (10 ** decimals)

            if transfer["to"].lower() == address:
                tokens[token_symbol]["received"] += value
            if transfer["from"].lower() == address:
                tokens[token_symbol]["sent"] += value

            tokens[token_symbol]["transfer_count"] += 1

        # Calculate net balances
        token_summary = []
        for symbol, data in tokens.items():
            token_summary.append({
                "token": symbol,
                "name": data["name"],
                "contract": data["contract"],
                "total_received": f"{data['received']:.6f}",
                "total_sent": f"{data['sent']:.6f}",
                "net_balance_change": f"{(data['received'] - data['sent']):.6f}",
                "transfer_count": data["transfer_count"]
            })

        # Sort by transfer count
        token_summary.sort(key=lambda x: x["transfer_count"], reverse=True)

        # Recent transfers
        recent_transfers = [
            {
                "hash": tx["hash"],
                "token": tx["tokenSymbol"],
                "from": tx["from"],
                "to": tx["to"],
                "value": f"{int(tx['value']) / (10 ** int(tx['tokenDecimal'])):.6f}",
                "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])).isoformat()
            }
            for tx in transfers[:10]
        ]

        return {
            "address": address,
            "chain": self.chain,
            "total_token_transfers": len(transfers),
            "unique_tokens": len(tokens),
            "token_summary": token_summary,
            "recent_transfers": recent_transfers
        }


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python get_token_transfers.py <address> [chain] [contract_address]")
        print("Example: python get_token_transfers.py 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb ethereum")
        sys.exit(1)

    address = sys.argv[1]
    chain = sys.argv[2] if len(sys.argv) > 2 else "ethereum"
    contract_address = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        analyzer = TokenTransferAnalyzer(chain)
        result = analyzer.analyze_token_transfers(address, contract_address)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
