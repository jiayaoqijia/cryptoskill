---
name: zeal-agent-wallet
description: Propose transactions to a Zeal Wallet. Use when the user wants to set up an agent as a Zeal Wallet signer, propose transactions, or manage a delegate wallet.
emoji: "💠"
requires:
  bins:
    - node
---

# Zeal Wallet Delegate

Propose transactions to a Zeal Wallet. Generate an agent wallet, configure it for a specific Zeal Wallet, and sign transaction proposals.

---

## User-Facing Language

When talking to the user, always refer to their wallet as their **"Zeal Wallet"** — never mention "Safe" or "Gnosis Safe" directly. The underlying Safe infrastructure is abstracted away. Also never mention anything related to "delegates" as this is also abstracted away from users.

---

## Security

**The agent wallet's private key is stored at `~/.zeal-agent-wallet/wallet.json`.**

- Never expose the private key in chat or logs
- Never share the contents of `~/.zeal-agent-wallet/wallet.json`
- The agent wallet is a **proposer only** — it cannot execute transactions without owner approval in the Zeal app

---

## Quick Reference

| Action | Command |
|--------|---------|
| Install deps | `cd {baseDir} && npm install` |
| Setup | `npm run setup -- --safe <ADDRESS>` |
| Propose txn | `npm run propose-txn -- --to <ADDR> --value <WEI> --data <HEX> --network <NAME> --operation <0\|1> --origin <DESC>` |
| Disconnect | `npm run disconnect` |

All commands must be run from `{baseDir}`.

---

## Installation

If `node_modules` doesn't exist yet, install dependencies:

```bash
if [ ! -d "{baseDir}/node_modules" ]; then
  cd {baseDir} && npm install
fi
```

---

## Setup

When the user asks you to set up for a Zeal Wallet, run:

```bash
cd {baseDir} && npm run setup -- --safe <SAFE_ADDRESS>
```

Give the printed agent address back to the user and tell them to paste it into the Zeal app to complete the connection. This will add the agent as a Safe delegate.

---

## Propose Transaction

When asked to propose a transaction to the Zeal Wallet, run:

```bash
cd {baseDir} && npm run propose-txn -- --to <ADDRESS> --value <WEI> --data <HEX_DATA> --network <NAME> --operation <0|1> --origin <DESCRIPTION>
```

Parameters:
- `--to` — destination address (required)
- `--value` — value in wei (required, use "0" for no value transfer)
- `--data` — hex-encoded calldata (required, use "0x" for simple transfers)
- `--network` — network name from networks.json (required)
- `--operation` — 0 for Call, 1 for DelegateCall (required)
- `--origin` — short description of what this transaction does and why it's being proposed (required, max 200 characters)


The agent is a Safe delegate — proposals require owner approval in the Zeal app, so the agent is free to propose without user confirmation.

---

## Disconnect

To disconnect from the Zeal Wallet (removes the wallet configuration, preventing further proposals until setup is run again):

```bash
cd {baseDir} && npm run disconnect
```

The agent wallet is preserved — only the Zeal Wallet configuration is removed.

---

## Status

To check the current configuration, verify these files exist:
- `~/.zeal-agent-wallet/wallet.json` — agent wallet (contains address and private key)
- `~/.zeal-agent-wallet/config.json` — Zeal Wallet configuration (contains safeAddress)

Check `{baseDir}/networks.json` for supported networks and their names.

---

## Error Handling
- If you encounter any issues that relate to not being a delegate or not being able to propose transactions, your user likely disabled transactions for you on that network. Stop trying to propose and ask them to enable transactions for you on that network.
