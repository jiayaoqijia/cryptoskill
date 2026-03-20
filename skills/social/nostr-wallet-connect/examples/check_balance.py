"""Check wallet balance via NWC."""

import asyncio
from nostrwalletconnect import NWCClient

NWC_URI = "nostr+walletconnect://<wallet_pubkey>?relay=wss://relay.example.com&secret=<hex_secret>"


async def main():
    async with NWCClient(NWC_URI) as nwc:
        balance = await nwc.get_balance()
        print(f"Balance: {balance.balance} msats ({balance.balance // 1000} sats)")


asyncio.run(main())
