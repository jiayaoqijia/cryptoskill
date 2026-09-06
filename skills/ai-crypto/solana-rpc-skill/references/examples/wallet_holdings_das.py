"""
Get wallet's complete holdings (SOL + SPL tokens + NFTs + cNFTs with metadata)
using DAS API `getAssetsByOwner` with showFungible and showNativeBalance.

Works with Helius and QuickNode (with DAS addon enabled).

Usage:
    SOLANA_RPC_URL=... python wallet_holdings_das.py <wallet_address>
"""
import os, sys, json
import httpx

RPC_URL = os.environ["SOLANA_RPC_URL"]


def get_assets_by_owner(owner: str, page: int = 1, limit: int = 1000) -> dict:
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAssetsByOwner",
        "params": {
            "ownerAddress": owner,
            "page": page,
            "limit": limit,
            "displayOptions": {
                "showFungible": True,           # include SPL tokens
                "showNativeBalance": True,      # include SOL balance
                "showCollectionMetadata": True, # parent collection info
            },
        },
    }
    r = httpx.post(RPC_URL, json=body, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data["result"]


def main(wallet: str):
    print(f"Fetching holdings for {wallet}…")
    page = 1
    all_items = []
    native = None

    while True:
        result = get_assets_by_owner(wallet, page=page)
        items = result.get("items", [])
        if not items and page == 1:
            print("No assets found.")
            break
        all_items.extend(items)
        if native is None:
            native = result.get("nativeBalance")
        total = result.get("total", 0)
        print(f"Page {page}: {len(items)} items (running total {len(all_items)}/{total})")
        if len(all_items) >= total or not items:
            break
        page += 1

    # Categorize
    fungibles = [a for a in all_items if a.get("interface") in ("FungibleToken", "FungibleAsset")]
    nfts = [a for a in all_items if a.get("interface") == "V1_NFT" or a.get("compression", {}).get("compressed") is False and a.get("interface") != "FungibleToken"]
    cnfts = [a for a in all_items if a.get("compression", {}).get("compressed")]

    print(f"\n=== Holdings summary for {wallet[:8]}… ===")
    if native:
        lamports = native.get("lamports", 0)
        print(f"SOL: {lamports / 1e9:.4f} ({native.get('total_price', '?')} USD)")
    print(f"Fungible tokens: {len(fungibles)}")
    print(f"NFTs (uncompressed): {len(nfts)}")
    print(f"cNFTs (compressed): {len(cnfts)}")

    print(f"\n=== Top tokens by USD value ===")
    ranked = sorted(fungibles, key=lambda a: (a.get("token_info", {}).get("price_info", {}).get("total_price") or 0), reverse=True)
    for a in ranked[:15]:
        sym = a.get("content", {}).get("metadata", {}).get("symbol", "?")
        ti = a.get("token_info", {})
        balance = ti.get("balance", 0)
        decimals = ti.get("decimals", 0)
        price = ti.get("price_info", {}).get("price_per_token") or 0
        total = ti.get("price_info", {}).get("total_price") or 0
        ui_balance = balance / (10 ** decimals) if decimals else balance
        print(f"  {sym:<10} {ui_balance:>15,.4f}  @ ${price:>10,.4f}  = ${total:>12,.2f}")

    print(f"\nFull data: {len(all_items)} total assets")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
