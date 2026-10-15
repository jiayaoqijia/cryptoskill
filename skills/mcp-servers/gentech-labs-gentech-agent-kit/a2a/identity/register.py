#!/usr/bin/env python3
"""
GenTech Labs — ERC-8004 Agent Registration Script

Registers GenTech Labs as an on-chain AI agent via the ERC-8004 Identity Registry.
Contract: 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432 (same on all chains via CREATE2)

Usage:
  python3 register.py --network base --private-key <key>
  python3 register.py --network base --dry-run  # preview without sending

Requirements:
  pip install web3 eth-account
"""

import argparse
import json
import sys
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────────

IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
METADATA_PATH = Path(__file__).parent / "agent-metadata.json"

NETWORKS = {
    "base": {
        "chain_id": 8453,
        "rpc": "https://mainnet.base.org",
        "explorer": "https://basescan.org",
        "name": "Base",
    },
    "ethereum": {
        "chain_id": 1,
        "rpc": "https://eth.llamarpc.com",
        "explorer": "https://etherscan.io",
        "name": "Ethereum",
    },
    "arbitrum": {
        "chain_id": 42161,
        "rpc": "https://arb1.arbitrum.io/rpc",
        "explorer": "https://arbiscan.io",
        "name": "Arbitrum",
    },
    "polygon": {
        "chain_id": 137,
        "rpc": "https://polygon-rpc.com",
        "explorer": "https://polygonscan.com",
        "name": "Polygon",
    },
    "optimism": {
        "chain_id": 10,
        "rpc": "https://mainnet.optimism.io",
        "explorer": "https://optimistic.etherscan.io",
        "name": "Optimism",
    },
    "bnb": {
        "chain_id": 56,
        "rpc": "https://bsc-dataseed.binance.org",
        "explorer": "https://bscscan.com",
        "name": "BNB Smart Chain",
    },
}

# ERC-8004 Identity Registry ABI (register + setAgentURI)
IDENTITY_ABI = [
    {
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "agentURI", "type": "string"},
        ],
        "name": "register",
        "outputs": [{"name": "agentId", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"name": "agentId", "type": "uint256"},
            {"name": "agentURI", "type": "string"},
        ],
        "name": "setAgentURI",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"name": "agentId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "agentId", "type": "uint256"},
            {"indexed": True, "name": "owner", "type": "address"},
        ],
        "name": "Registered",
        "type": "event",
    },
]


def load_metadata() -> dict:
    """Load agent metadata JSON."""
    with open(METADATA_PATH) as f:
        return json.load(f)


def upload_metadata_to_github(metadata: dict) -> str:
    """
    Returns the GitHub raw URL where metadata will be hosted.
    In practice, we push agent-metadata.json to the repo and use the raw URL.
    """
    repo = "Gentech-Labs/genTech-agent-kit"
    branch = "main"
    path = "a2a/identity/agent-metadata.json"
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"


def preview_registration(network: str, metadata: dict):
    """Preview what will be registered."""
    net = NETWORKS[network]
    metadata_url = upload_metadata_to_github(metadata)

    print("=" * 60)
    print("  GenTech Labs — ERC-8004 Registration Preview")
    print("=" * 60)
    print()
    print(f"  Network:      {net['name']} (chain {net['chain_id']})")
    print(f"  Contract:     {IDENTITY_REGISTRY}")
    print(f"  Metadata URL: {metadata_url}")
    print()
    print("  Agent Details:")
    print(f"    Name:        {metadata['name']}")
    print(f"    Description: {metadata['description'][:80]}...")
    print(f"    Services:    {len(metadata['services'])}")
    for s in metadata["services"]:
        pricing = s.get("pricing", {})
        price_str = f"${pricing.get('amount', 0)}/{pricing.get('model', 'free')}"
        print(f"      - {s['name']} ({s['type']}) — {price_str}")
    print()
    print(f"  Estimated gas: ~$0.01 on {net['name']}")
    print()
    print("  Metadata will be uploaded to GitHub before registration.")
    print("  The on-chain URI will point to the raw GitHub URL.")
    print()


def register_agent(network: str, private_key: str, dry_run: bool = False):
    """Register GenTech Labs on ERC-8004 Identity Registry."""
    from web3 import Web3

    net = NETWORKS[network]
    metadata = load_metadata()
    metadata_url = upload_metadata_to_github(metadata)

    preview_registration(network, metadata)

    if dry_run:
        print("  ✅ Dry run complete. No transaction sent.")
        print()
        print("  Next steps:")
        print("  1. Push agent-metadata.json to GitHub")
        print("  2. Run without --dry-run to register on-chain")
        print("  3. Verify on Agentscan: https://agentscan.info/agents")
        return

    # Connect to network
    w3 = Web3(Web3.HTTPProvider(net["rpc"]))
    if not w3.is_connected():
        print(f"  ❌ Cannot connect to {net['name']} RPC: {net['rpc']}")
        sys.exit(1)

    # Load account
    account = w3.eth.account.from_key(private_key)
    print(f"  Owner address: {account.address}")
    print(f"  Balance:       {w3.from_wei(w3.eth.get_balance(account.address), 'ether')} ETH")

    # Build transaction
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(IDENTITY_REGISTRY),
        abi=IDENTITY_ABI,
    )

    # estimate gas
    try:
        gas_estimate = contract.functions.register(
            account.address,
            metadata_url,
        ).estimate_gas({"from": account.address})
    except Exception as e:
        print(f"  ❌ Gas estimation failed: {e}")
        sys.exit(1)

    gas_price = w3.eth.gas_price
    gas_cost = w3.from_wei(gas_estimate * gas_price, "ether")

    print(f"  Gas estimate:  {gas_estimate}")
    print(f"  Gas price:     {w3.from_wei(gas_price, 'gwei')} gwei")
    print(f"  Total cost:    {gas_cost} ETH")
    print()

    # Build, sign, send
    tx = contract.functions.register(
        account.address,
        metadata_url,
    ).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": int(gas_estimate * 1.2),  # 20% buffer
        "gasPrice": gas_price,
        "chainId": net["chain_id"],
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print(f"  📤 Transaction sent: {tx_hash.hex()}")
    print(f"  🔍 Explorer: {net['explorer']}/tx/{tx_hash.hex()}")
    print()

    # Wait for receipt
    print("  ⏳ Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    if receipt.status == 1:
        # Parse Registered event
        logs = contract.events.Registered().process_receipt(receipt)
        agent_id = logs[0]["args"]["agentId"] if logs else "unknown"

        print(f"  ✅ Registration successful!")
        print(f"  🆔 Agent ID: {agent_id}")
        print(f"  🔗 Tx: {net['explorer']}/tx/{tx_hash.hex()}")
        print()
        print("  Next steps:")
        print(f"  1. Verify on Agentscan: https://agentscan.info/agents")
        print(f"  2. Submit feedback to build reputation")
        print(f"  3. List APIs on x402 Bazaar")
    else:
        print(f"  ❌ Transaction failed!")
        print(f"  🔍 Check: {net['explorer']}/tx/{tx_hash.hex()}")
        sys.exit(1)


def main():
    import os
    parser = argparse.ArgumentParser(description="Register GenTech Labs on ERC-8004")
    parser.add_argument(
        "--network",
        choices=list(NETWORKS.keys()),
        default="base",
        help="Network to register on (default: base)",
    )
    parser.add_argument(
        "--private-key",
        help="Private key for signing (or set ERC8004_PRIVATE_KEY env var)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview registration without sending transaction",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show registration details and exit",
    )

    args = parser.parse_args()
    metadata = load_metadata()

    if args.preview:
        preview_registration(args.network, metadata)
        return

    private_key: str = args.private_key or os.environ.get("ERC8004_PRIVATE_KEY", "")
    if not private_key and not args.dry_run:
        print("  ❌ Private key required. Use --private-key or ERC8004_PRIVATE_KEY env var")
        sys.exit(1)

    register_agent(args.network, private_key, args.dry_run)


if __name__ == "__main__":
    import os
    main()
