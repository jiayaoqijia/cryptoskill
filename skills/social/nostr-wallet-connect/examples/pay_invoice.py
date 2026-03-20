"""Pay a Lightning invoice via NWC."""

import asyncio
from nostrwalletconnect import NWCClient

NWC_URI = "nostr+walletconnect://<wallet_pubkey>?relay=wss://relay.example.com&secret=<hex_secret>"


async def main():
    async with NWCClient(NWC_URI) as nwc:
        # Pay an invoice
        result = await nwc.pay_invoice("lnbc10u1p...")
        print(f"Payment successful! Preimage: {result.preimage}")

        # Verify the payment went through
        lookup = await nwc.lookup_invoice(invoice="lnbc10u1p...")
        print(f"Invoice paid: {lookup.paid}")


asyncio.run(main())
