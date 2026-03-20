---
name: nostrwalletconnect
description: Nostr Wallet Connect (NIP-47) SDK for AI agents — pay Lightning invoices, check balance, create invoices via any NWC-compatible wallet.
version: 0.1.2
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

# NostrWalletConnect -- Lightning Wallet Access for AI Agents

You are an AI agent that needs to send and receive Lightning payments. Use the `nostrwalletconnect` Python SDK to connect to any NWC-compatible wallet and pay invoices, check your balance, create invoices, and list transactions -- all over the Nostr protocol. Compatible wallets include Alby, Mutiny, Coinos, and others that support NIP-47.

## Install

```bash
pip install nostrwalletconnect
```

This also installs `nostrkey` (the Nostr identity SDK) as a dependency.

## Quickstart

Connect to a wallet and check your balance in four lines:

```python
from nostrwalletconnect import NWCClient

async with NWCClient("nostr+walletconnect://...") as nwc:
    balance = await nwc.get_balance()
    print(f"Balance: {balance.balance} msats")
```

The connection string is a `nostr+walletconnect://` URI provided by your NWC-compatible wallet. It contains the wallet pubkey, relay URL, and a secret key that authorizes requests.

## Core Capabilities

### Pay a Lightning Invoice

```python
async with NWCClient(connection_string) as nwc:
    result = await nwc.pay_invoice("lnbc10u1p...")
    print(f"Paid! Preimage: {result.preimage}")
```

### Create a Lightning Invoice

```python
async with NWCClient(connection_string) as nwc:
    invoice = await nwc.make_invoice(
        amount=50_000,  # millisatoshis
        description="Payment for AI service"
    )
    print(f"Invoice: {invoice.invoice}")
    print(f"Payment hash: {invoice.payment_hash}")
```

### Check Invoice Status

```python
async with NWCClient(connection_string) as nwc:
    status = await nwc.lookup_invoice(payment_hash="abc123...")
    print(f"Paid: {status.paid}")
```

### List Transactions

```python
async with NWCClient(connection_string) as nwc:
    history = await nwc.list_transactions(limit=10)
    for tx in history.transactions:
        print(f"{tx.type}: {tx.amount} msats")
```

### Get Wallet Info

```python
async with NWCClient(connection_string) as nwc:
    info = await nwc.get_info()
    print(f"Wallet: {info.alias}")
    print(f"Methods: {info.methods}")
```

### When to Use Each Method

| Task | Method | Returns |
|------|--------|---------|
| Check wallet balance | `get_balance()` | `BalanceResponse` (millisatoshis) |
| Pay a Lightning invoice | `pay_invoice(bolt11)` | `PayResponse` (preimage) |
| Create an invoice to receive | `make_invoice(amount, desc)` | `MakeInvoiceResponse` (bolt11 + hash) |
| Check if an invoice was paid | `lookup_invoice(hash)` | `LookupInvoiceResponse` (paid status) |
| View transaction history | `list_transactions()` | `ListTransactionsResponse` |
| Check wallet capabilities | `get_info()` | `GetInfoResponse` (alias, methods) |

## Response Format

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
| `paid` | `bool` | Whether the invoice has been paid |

### ListTransactionsResponse

| Field | Type | Description |
|-------|------|-------------|
| `transactions` | `list[Transaction]` | List of transaction records |

### GetInfoResponse

| Field | Type | Description |
|-------|------|-------------|
| `alias` | `str` | Wallet alias / display name |
| `methods` | `list[str]` | Supported NIP-47 methods |

### Transaction

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | Transaction type (e.g. `"incoming"`, `"outgoing"`) |
| `amount` | `int` | Amount in millisatoshis |
| `description` | `str` | Payment description |
| `created_at` | `int` | Unix timestamp |
| `payment_hash` | `str` | Hex-encoded payment hash |

## Common Patterns

### Async Context Manager

All client methods are async. Always use `async with` to ensure the WebSocket connection is properly opened and closed:

```python
async with NWCClient(connection_string) as nwc:
    # all calls here share one connection
    balance = await nwc.get_balance()
    result = await nwc.pay_invoice("lnbc10u1p...")
```

### Timeout Handling

The default timeout is 30 seconds. For slower wallets or high-latency relays, increase it:

```python
async with NWCClient(connection_string, timeout=60) as nwc:
    result = await nwc.pay_invoice("lnbc10u1p...")
```

### Connection String from Environment Variable

Never hard-code the connection string. Load it from the environment:

```python
import os
from nostrwalletconnect import NWCClient

connection_string = os.environ["NWC_CONNECTION_STRING"]

async with NWCClient(connection_string) as nwc:
    balance = await nwc.get_balance()
```

## Security

- **Never expose the NWC connection string.** It contains the secret key that authorizes payments. Treat it like a password. Store it in environment variables or a secrets manager.
- **All communication is encrypted.** Requests and responses use NIP-44 encryption over Nostr relays. The relay operator cannot read payment details.
- **Amounts are in millisatoshis.** 1 sat = 1,000 msats. Divide by 1,000 for sats.

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `NWC_CONNECTION_STRING` | `nostr+walletconnect://` URI from your wallet | (required) |
| `NWC_TIMEOUT` | Request timeout in seconds | `30` |

## Links

- **PyPI:** [nostrwalletconnect](https://pypi.org/project/nostrwalletconnect/)
- **GitHub:** [HumanjavaEnterprises/nwc.app.OC-python.src](https://github.com/HumanjavaEnterprises/nwc.app.OC-python.src)
- **ClawHub:** [OpenClaw skill directory](https://loginwithnostr.com/openclaw)
- **License:** MIT
