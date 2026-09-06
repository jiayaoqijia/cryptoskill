---
name: wallet-monitor
description: Monitors specific cryptocurrency wallet addresses for balance changes and transactions on-chain using Web3 and RPC endpoints. Use when the user wants to track activity of specific wallets or receive alerts on balance updates.
version: 1.0.0
author: with-philia
license: MIT
tags: [Web3, Wallet, Monitor, Blockchain, Ethereum]
dependencies: [axios]
allowed-tools: Node(scripts/monitor.js)
---

# Wallet Monitor

This skill provides the capability to monitor specific blockchain wallets for activity, such as balance changes or large transactions. It connects to public RPC endpoints to fetch real-time data.

## Workflow

1.  **Define Wallets**: Specify the list of wallet addresses to monitor in `scripts/monitor.js` or pass them as arguments.
2.  **Set Threshold**: Configure the minimum balance or transaction value to trigger an alert.
3.  **Run Monitor**: Execute the `scripts/monitor.js` script to check current status.
4.  **Schedule**: Use a scheduler (like cron) to run the monitor periodically for continuous tracking.

## Scripts

- `scripts/monitor.js`: The core Node.js script that queries the blockchain via RPC to check wallet balances.

## References

- `references/wallets.md`: A reference list of notable wallet addresses (e.g., exchanges, foundations) for testing and monitoring.

## Configuration

The script uses a public RPC endpoint by default. For higher reliability and rate limits, consider using a dedicated RPC provider (e.g., Alchemy, Infura) and setting the `RPC_URL` environment variable.
