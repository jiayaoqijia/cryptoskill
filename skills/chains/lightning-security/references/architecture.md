# Remote Signer Architecture

## Overview

The remote signer architecture splits an lnd Lightning node into two separate
processes running on different machines:

1. **Signer node** — holds all private key material, performs signing
2. **Watch-only node** — handles networking, channels, routing, payments

This separation ensures that even if the machine running the watch-only node
(the "agent machine") is fully compromised, the attacker cannot extract private
keys or sign arbitrary transactions.

## Two-Node Architecture

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│      Agent Machine          │     │      Signer Machine         │
│                             │     │                             │
│  ┌───────────────────────┐  │     │  ┌───────────────────────┐  │
│  │  lnd (watch-only)     │  │     │  │  lnd (signer)         │  │
│  │                       │  │     │  │                       │  │
│  │  - Neutrino backend   │◄─┼─gRPC┼─►│  - Holds seed          │  │
│  │  - Channel state      │  │     │  │  - Signs commitments   │  │
│  │  - Routes payments    │  │     │  │  - Signs on-chain txs  │  │
│  │  - Manages peers      │  │     │  │  - No p2p networking   │  │
│  │  - NO private keys    │  │     │  │  - Minimal surface     │  │
│  └───────────────────────┘  │     │  └───────────────────────┘  │
│                             │     │                             │
│  Imported from signer:      │     │  Never exported:            │
│  - accounts.json (xpubs)   │     │  - Seed mnemonic            │
│  - tls.cert                │     │  - Private keys             │
│  - admin.macaroon          │     │  - Wallet DB key material   │
└─────────────────────────────┘     └─────────────────────────────┘
```

## What Gets Exported

The credential bundle contains three files:

### accounts.json

Output of `lncli wallet accounts list`. Contains extended public keys (xpubs)
for all lnd accounts. These allow the watch-only node to:

- Derive public keys and addresses
- Track on-chain balances
- Construct unsigned transactions

They do **not** allow signing or spending.

### tls.cert

The signer's TLS certificate. The watch-only node uses this to establish an
authenticated, encrypted gRPC connection to the signer. This prevents
man-in-the-middle attacks on the signing channel.

### admin.macaroon

The signer's admin macaroon for RPC authentication. The watch-only node presents
this when requesting signatures. For production, replace with a scoped macaroon
that only allows signing operations.

## What Never Leaves the Signer

- **Seed mnemonic** — the 24-word BIP39 phrase from which all keys derive
- **Private keys** — funding keys, revocation keys, HTLC keys
- **Wallet database key material** — encrypted private key data in the wallet DB

## Signing Flow

When the watch-only node needs a signature (e.g., committing a channel state
update or broadcasting an on-chain transaction):

1. Watch-only node constructs the unsigned transaction
2. Watch-only node sends a signing request to the signer via gRPC
3. Signer validates the request and produces the signature
4. Signer returns the signature to the watch-only node
5. Watch-only node assembles the signed transaction and broadcasts it

## Threat Model

### Compromised agent machine

**Impact:** Attacker can see channel states, balances, and payment history.
Attacker can attempt to route payments through existing channels.

**Cannot:** Extract private keys, sign arbitrary transactions, sweep funds to
attacker-controlled addresses, forge channel close transactions.

### Compromised signer machine

**Impact:** Full compromise — attacker has seed and all keys. Can sign arbitrary
transactions and sweep all funds.

**Mitigation:** The signer should have minimal attack surface. No unnecessary
services, no web browser, no agent software. Ideally dedicated hardware.

### Network interception (gRPC channel)

**Impact:** Without TLS cert validation, attacker could intercept signing
requests.

**Mitigation:** TLS with certificate pinning (the watch-only node has a copy of
the signer's TLS cert and validates against it).

## Macaroon Scoping

For production deployments, the admin macaroon should be replaced with a
custom macaroon that only grants the minimum permissions needed:

```bash
# On the signer, bake a signing-only macaroon
lncli --rpcserver=localhost:10012 --lnddir=~/.lnd-signer \
    bakemacaroon uri:/signrpc.Signer/SignOutputRaw \
    uri:/signrpc.Signer/ComputeInputScript \
    uri:/signrpc.Signer/MuSig2Sign \
    uri:/walletrpc.WalletKit/DeriveKey \
    uri:/walletrpc.WalletKit/DeriveNextKey \
    --save_to=~/.lnd-signer/data/chain/bitcoin/mainnet/signer-only.macaroon
```

## Future Enhancements

- **litd accounts:** Use Lightning Terminal's account system for even finer
  access control and spending limits
- **Hardware signing devices:** Replace the signer lnd with a hardware security
  module (HSM) or hardware wallet for tamper-resistant key storage
- **Multi-party signing:** Require multiple signers to approve high-value
  transactions (threshold signatures)
- **Macaroon rotation:** Automatically rotate macaroons on a schedule to limit
  the window of compromise
