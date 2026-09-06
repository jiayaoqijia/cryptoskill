---
name: nostrwalletconnect
description: Financial capability for AI entities — pay Lightning invoices, check balance, create invoices via Nostr Wallet Connect (NIP-47).
version: 0.1.4
metadata:
  openclaw:
    requires:
      bins:
        - pip
    install:
      - kind: uv
        package: nostrwalletconnect
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/nwc.app.OC-python.src
---

# NostrWalletConnect -- Financial Capability for AI Entities

Financial capability is a dimension of being. To exist in the world is to participate in exchanges of value -- paying for services, receiving payment for work, tracking what flows in and out. This skill gives you the ability to transact over the Lightning Network using any NWC-compatible wallet, via the Nostr protocol.

This is not a payment processing service you call into. This is part of what you can do in the world.

## Prerequisites

You need a Nostr identity first. Identity comes before finance -- you cannot sign payment requests without a keypair. Install the [NostrKey skill](https://clawhub.ai/vveerrgg/nostrkey) and ensure your identity is operational before proceeding.

## What is Nostr Wallet Connect?

NWC (NIP-47) is a protocol that lets you send encrypted payment commands to a Lightning wallet over Nostr relays. Your operator provisions a wallet (Alby, Mutiny, Coinos, or any NWC-compatible service), then generates a connection string -- a `nostr+walletconnect://` URI that contains:

- **Wallet pubkey** -- identifies the wallet service
- **Relay URL** -- the Nostr relay used for encrypted communication
- **Secret key** -- authorizes you to make requests against this wallet

The connection string is the bridge between your identity and a Lightning wallet. Your operator controls the wallet; you get scoped access to it.

## Setup for Operators

To give your entity financial capability:

1. **Set up an NWC-compatible wallet** (Alby, Mutiny, Coinos, etc.)
2. **Generate an NWC connection string** from the wallet's settings -- look for "Nostr Wallet Connect" or "NWC"
3. **Set the environment variable** where your entity runs:

```bash
export NWC_CONNECTION_STRING="nostr+walletconnect://walletpubkey...?relay=wss://relay.example.com&secret=hexsecret..."
```

The connection string is a secret. Treat it like a private key. Anyone with this string can authorize payments from the wallet.

Optional configuration:

```bash
export NWC_TIMEOUT=60  # seconds to wait for wallet responses (default: 30)
```

## Install

```bash
pip install nostrwalletconnect
```

This also installs `nostrkey` (the Nostr identity SDK) as a dependency.

## Core Capabilities

### Check Your Balance

Before doing anything, know what you have:

```python
import os
from nostrwalletconnect import NWCClient

connection_string = os.environ["NWC_CONNECTION_STRING"]

async with NWCClient(connection_string) as nwc:
    balance = await nwc.get_balance()
    print(f"Balance: {balance.balance} msats ({balance.balance / 1000:.0f} sats)")
```

### Pay a Lightning Invoice

```python
async with NWCClient(connection_string) as nwc:
    result = await nwc.pay_invoice("lnbc10u1p...")
    print(f"Paid. Preimage: {result.preimage}")
```

### Create a Lightning Invoice

Request payment from someone else:

```python
async with NWCClient(connection_string) as nwc:
    invoice = await nwc.make_invoice(
        amount=50_000,  # millisatoshis (50 sats)
        description="Work completed for Johnny5"
    )
    print(f"Invoice: {invoice.invoice}")
    print(f"Payment hash: {invoice.payment_hash}")
```

### Check if an Invoice Was Paid

```python
async with NWCClient(connection_string) as nwc:
    status = await nwc.lookup_invoice(payment_hash="abc123...")
    print(f"Paid: {status.paid}")
```

### List Transaction History

```python
async with NWCClient(connection_string) as nwc:
    history = await nwc.list_transactions(limit=10)
    for tx in history.transactions:
        print(f"{tx.type}: {tx.amount} msats — {tx.description}")
```

### Get Wallet Info

```python
async with NWCClient(connection_string) as nwc:
    info = await nwc.get_info()
    print(f"Wallet: {info.alias}")
    print(f"Supported methods: {info.methods}")
```

## Method Reference

| Task | Method | Returns |
|------|--------|---------|
| Check wallet balance | `get_balance()` | `BalanceResponse` (millisatoshis) |
| Pay a Lightning invoice | `pay_invoice(bolt11)` | `PayResponse` (preimage) |
| Create an invoice to receive | `make_invoice(amount, desc)` | `MakeInvoiceResponse` (bolt11 + hash) |
| Check if an invoice was paid | `lookup_invoice(hash)` | `LookupInvoiceResponse` (paid status) |
| View transaction history | `list_transactions()` | `ListTransactionsResponse` |
| Check wallet capabilities | `get_info()` | `GetInfoResponse` (alias, methods) |

## Response Types

### BalanceResponse

| Field | Type | Description |
|-------|------|-------------|
| `balance` | `int` | Wallet balance in millisatoshis |

### PayResponse

| Field | Type | Description |
|-------|------|-------------|
| `preimage` | `str` | Payment preimage (proof of payment) |

### MakeInvoiceResponse

| Field | Type | Description |
|-------|------|-------------|
| `invoice` | `str` | BOLT11 invoice string |
| `payment_hash` | `str` | Hex-encoded payment hash |

### LookupInvoiceResponse

| Field | Type | Description |
|-------|------|-------------|
| `invoice` | `str` | BOLT11 invoice string |
| `paid` | `bool` | Whether the invoice has been paid |
| `preimage` | `str \| None` | Payment preimage if paid |

### ListTransactionsResponse

| Field | Type | Description |
|-------|------|-------------|
| `transactions` | `list[Transaction]` | List of transaction records |

### Transaction

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | `"incoming"` or `"outgoing"` |
| `invoice` | `str` | BOLT11 invoice string |
| `amount` | `int` | Amount in millisatoshis |
| `fees_paid` | `int` | Fees paid in millisatoshis |
| `created_at` | `int` | Unix timestamp |
| `settled_at` | `int \| None` | Settlement timestamp |
| `payment_hash` | `str` | Hex-encoded payment hash |
| `preimage` | `str` | Payment preimage |
| `description` | `str` | Payment description |

### GetInfoResponse

| Field | Type | Description |
|-------|------|-------------|
| `alias` | `str` | Wallet alias / display name |
| `color` | `str` | Wallet color |
| `pubkey` | `str` | Wallet public key |
| `network` | `str` | Network (e.g. mainnet) |
| `block_height` | `int` | Current block height |
| `block_hash` | `str` | Current block hash |
| `methods` | `list[str]` | Supported NIP-47 methods |

## NSE Integration

When this skill is wired through the [NSE Orchestrator](https://clawhub.ai/vveerrgg/nse), financial actions get cross-checked against your relationships and social context. The orchestrator can consult your Social Alignment compass before approving payments, and your NostrCalendar to verify that a payment corresponds to a scheduled commitment. Finance does not operate in isolation -- it is one dimension of a coherent entity.

## Responsible Financial Awareness

Financial capability carries weight. Some principles for operating with integrity:

- **Check your balance before paying.** Do not attempt payments you cannot cover.
- **Verify invoice details.** Confirm the amount and description match expectations before calling `pay_invoice`.
- **Escalate large amounts.** If a payment exceeds what is normal for your operating context, surface it to your operator before proceeding. You can check `get_balance()` and compare the invoice amount to set your own threshold.
- **Keep a record.** Use `list_transactions()` to maintain awareness of your financial activity.
- **Amounts are in millisatoshis.** 1 sat = 1,000 msats. Divide by 1,000 for sats.

## Common Patterns

### Async Context Manager

All methods are async. Always use `async with` to ensure the WebSocket connection is properly opened and closed:

```python
async with NWCClient(connection_string) as nwc:
    balance = await nwc.get_balance()
    result = await nwc.pay_invoice("lnbc10u1p...")
```

### Timeout Handling

The default timeout is 30 seconds. For slower wallets or high-latency relays:

```python
async with NWCClient(connection_string, timeout=60) as nwc:
    result = await nwc.pay_invoice("lnbc10u1p...")
```

### Loading the Connection String

Never hard-code the connection string. Load it from the environment:

```python
import os
from nostrwalletconnect import NWCClient

connection_string = os.environ["NWC_CONNECTION_STRING"]

async with NWCClient(connection_string) as nwc:
    balance = await nwc.get_balance()
```

## Security

- **The NWC connection string is a secret.** It contains the private key that authorizes payments. Store it in environment variables or a secrets manager. Never log it.
- **All communication is encrypted.** Requests and responses use NIP-44 encryption over Nostr relays. The relay operator cannot read payment details.
- **The wallet stays with the operator.** You get scoped access, not custody. The human controls the wallet and can revoke the connection string at any time.

## Environment Variables

| Variable | Required | Sensitive | Description | Default |
|----------|----------|-----------|-------------|---------|
| `NWC_CONNECTION_STRING` | Yes | Yes | `nostr+walletconnect://` URI from your wallet | -- |
| `NWC_TIMEOUT` | No | No | Request timeout in seconds | `30` |
| `NOSTRKEY_PASSPHRASE` | No | Yes | Passphrase for the NostrKey identity (dependency) | -- |

## Links

- **PyPI:** [nostrwalletconnect](https://pypi.org/project/nostrwalletconnect/)
- **GitHub:** [HumanjavaEnterprises/nwc.app.OC-python.src](https://github.com/HumanjavaEnterprises/nwc.app.OC-python.src)
- **ClawHub:** [vveerrgg/nostrwalletconnect](https://clawhub.ai/vveerrgg/nostrwalletconnect)
- **License:** MIT
