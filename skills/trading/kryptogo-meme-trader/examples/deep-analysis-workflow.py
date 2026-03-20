#!/usr/bin/env python3
import os
import sys
import requests
from datetime import datetime, timedelta

# --- Configuration ---
API_BASE = "https://wallet-data.kryptogo.app"
API_KEY = os.environ.get("KRYPTOGO_API_KEY")

def die(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)

def get_token_overview(token_mint: str, chain_id: int):
    """Fetches token overview to get total supply and other metadata."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{API_BASE}/token-overview?address={token_mint}&chain_id={chain_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        die(f"Failed to get token overview: {response.status_code} {response.text}")
    data = response.json()
    if not data.get("total_supply"):
        die("Could not retrieve total_supply from token overview.")
    return float(data["total_supply"])

def get_key_addresses(token_mint: str, chain_id: int):
    """Fetches analysis data to extract cluster and smart money addresses."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{API_BASE}/analyze/{token_mint}?chain_id={chain_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        die(f"Failed to get analysis data: {response.status_code} {response.text}")
    
    data = response.json()
    
    cluster_wallets = []
    if data.get("clusters"):
        for cluster in data["clusters"]:
            for wallet in cluster.get("wallets", []):
                cluster_wallets.append(wallet["address"])

    smart_money_wallets = []
    if data.get("address_metadata"):
        for addr, meta in data["address_metadata"].items():
            if meta.get("label", "").startswith("smart-"):
                smart_money_wallets.append(addr)

    return list(set(cluster_wallets)), list(set(smart_money_wallets))

def get_balance_history(token_mint: str, chain_id: int, wallets: list, days: int = 7):
    """Fetches aggregated balance history for a list of wallets."""
    if not wallets:
        return []
        
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    url = f"{API_BASE}/balance-history"
    
    # Calculate start timestamp
    after_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())
    
    payload = {
        "chain_id": chain_id,
        "wallets": wallets,
        "token": token_mint,
        "bar": "1D",
        "limit": days + 1,
        "after": after_timestamp,
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        # API might fail if the list of wallets is too long.
        # In a real implementation, this should be batched.
        print(f"Warning: Failed to get balance history (maybe too many wallets): {response.text}", file=sys.stderr)
        return []
        
    return response.json()

def main():
    if not API_KEY:
        die("KRYPTOGO_API_KEY environment variable is not set.")
    if len(sys.argv) < 2:
        die("Usage: python deep-analysis-workflow.py <token_mint> [chain_id]")

    token_mint = sys.argv[1]
    chain_id = int(sys.argv[2]) if len(sys.argv) > 2 else 501

    print(f"🔬 Starting deep analysis for token: {token_mint} on chain: {chain_id}\n")

    # 1. Get Total Supply
    print("Step 1: Fetching token overview to get total supply...")
    total_supply = get_token_overview(token_mint, chain_id)
    print(f"✅ Total Supply: {total_supply:,.0f}\n")

    # 2. Get Key Addresses
    print("Step 2: Extracting Cluster and Smart Money addresses...")
    cluster_wallets, smart_money_wallets = get_key_addresses(token_mint, chain_id)
    print(f"✅ Found {len(cluster_wallets)} cluster addresses.")
    print(f"✅ Found {len(smart_money_wallets)} Smart Money addresses.\n")

    # 3. Analyze Cluster Holding Trend
    print("Step 3: Analyzing Cluster holding trend...")
    cluster_history = get_balance_history(token_mint, chain_id, cluster_wallets)
    if cluster_history:
        print("📈 Cluster Holding as % of Total Supply (past 7 days):")
        for record in cluster_history:
            balance = float(record['balance'])
            percentage = (balance / total_supply) * 100
            date = datetime.fromtimestamp(record['timestamp']).strftime('%Y-%m-%d')
            print(f"  {date}: {percentage:.2f}%")
        print()
    else:
        print("⚠️ Could not retrieve cluster history.\n")

    # 4. Analyze Smart Money Holding Trend
    print("Step 4: Analyzing Smart Money holding trend...")
    sm_history = get_balance_history(token_mint, chain_id, smart_money_wallets)
    if sm_history:
        print("🧠 Smart Money Holding as % of Total Supply (past 7 days):")
        for record in sm_history:
            balance = float(record['balance'])
            percentage = (balance / total_supply) * 100
            date = datetime.fromtimestamp(record['timestamp']).strftime('%Y-%m-%d')
            print(f"  {date}: {percentage:.2f}%")
        print()
    else:
        print("⚠️ Could not retrieve Smart Money history.\n")

if __name__ == "__main__":
    main()
