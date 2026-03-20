# Transaction Concepts

## Transaction CBOR

Cardano transactions are serialized using CBOR (Concise Binary Object Representation). The MCP tool accepts an unsigned CBOR hex string, signs it with the wallet's keys, and submits it to the network.

## Signing

The wallet holds private keys derived from the seed phrase. Signing attaches a cryptographic witness proving the wallet owner authorized the transaction. The seed phrase is never exposed to the AI agent.

## Confirmation Flow

Transactions are irreversible once submitted and confirmed on-chain. Always follow the safety model:

1. Parse and explain what the transaction does.
2. Wait for explicit user confirmation.
3. Submit only after confirmation.

## Transaction Hash

After successful submission, the network returns a unique transaction hash (64-character hex). This can be used to look up the transaction on a Cardano explorer.
