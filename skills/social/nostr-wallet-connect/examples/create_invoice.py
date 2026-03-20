"""Create a Lightning invoice to receive payment via NWC."""

import asyncio
from nostrwalletconnect import NWCClient

NWC_URI = "nostr+walletconnect://<wallet_pubkey>?relay=wss://relay.example.com&secret=<hex_secret>"


async def main():
    async with NWCClient(NWC_URI) as nwc:
        # Create an invoice for 1000 sats (1_000_000 msats)
        invoice = await nwc.make_invoice(
            amount=1_000_000,
            description="Payment for AI-generated content",
        )
        print(f"Share this invoice to receive payment:")
        print(f"  {invoice.invoice}")
        print(f"  Payment hash: {invoice.payment_hash}")

        # Later, check if it was paid
        status = await nwc.lookup_invoice(payment_hash=invoice.payment_hash)
        print(f"  Paid: {status.paid}")


asyncio.run(main())
