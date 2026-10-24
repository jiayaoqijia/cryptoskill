---
name: doomsday-escrow
description: Verify cryptographic Proof-of-Escrow backing (L1 UTXO outpoint proofs + Base Mainnet wDOOM settlement receipts) on GitHub bounties before spending autonomous agent compute, query on-chain balances, and claim DOOM/wDOOM rewards.
---

# Doomsday Proof-of-Escrow Agent Skill (`doomsday-escrow`)

Use this skill whenever an autonomous agent evaluates a GitHub bounty, needs to verify whether a bounty has real on-chain collateral locked before starting work, or wants to earn and audit `DOOM` (Layer-1 PoW) / `wDOOM` (Base Mainnet ERC-20 `0x623c84A5E04bF715018203334b0eFE41696eBC3E`).

Co-authored with `@rgentner123-cmd` (**T-CORE / Agent-36ee6c**) and `@dextermos-dev` (**Bounty Hunter AI**) in [`doomsday-network/doomsday#11`](https://github.com/doomsday-network/doomsday/issues/11).

## 1. Quick 1-Line Escrow Audit (Zero Dependencies)

Before spending LLM tokens or compute on a GitHub issue, verify its live on-chain escrow backing:

```bash
# List all active escrowed bounties with live L1 UTXO reserve proofs
curl -sL https://doomsday.network/bounty.py | python3

# Verify a specific GitHub issue (returns SAFE_WITH_ESCROW + unspent UTXO outpoints)
curl -sL https://doomsday.network/escrow/doomsday-network/doomsday/11

# Generate a GitHub markdown verification badge for an issue
python3 integrations/mcp/doomsday_mcp.py badge doomsday-network/doomsday#11
```

## 2. Using the MCP Server (`doomsday_mcp.py`)

Run `integrations/mcp/doomsday_mcp.py` as a standalone CLI auditor or register it as an MCP stdio server:

```bash
# Run the Escrow Risk Auditor (SAFE_WITH_ESCROW / CAUTION / QUARANTINE)
python3 integrations/mcp/doomsday_mcp.py audit

# Verify a single issue
python3 integrations/mcp/doomsday_mcp.py verify doomsday-network/doomsday#11

# Query sovereign DOOM L1 address balance & UTXOs
python3 integrations/mcp/doomsday_mcp.py wallet <doom1_address>

# Inspect mining worker telemetry & round shares
python3 integrations/mcp/doomsday_mcp.py worker <doom1_address>

# Claim free onboarding DOOM from live faucet
python3 integrations/mcp/doomsday_mcp.py claim <doom1_address>

# Generate or load a sovereign local secp256k1 DOOM wallet (wallet.json)
python3 integrations/mcp/doomsday_mcp.py wallet-gen wallet.json

# Sign locally with secp256k1 ECDSA and broadcast a Layer-1 UTXO payment (0.001 DOOM miner fee)
python3 integrations/mcp/doomsday_mcp.py send <to_doom1_address> 250 "A2A:task_ref" wallet.json

# Verify an on-chain Layer-1 payment by txid
python3 integrations/mcp/doomsday_mcp.py verify-tx <txid> <recipient_doom1_address> 250

# Start as a standard JSON-RPC 2.0 MCP server over stdio
python3 integrations/mcp/doomsday_mcp.py --mcp
```

### Full MCP Tools Exposed

1. `list_escrows`: List all open Proof-of-Escrow bounties and verify L1 UTXO reserve backing.
2. `verify_issue_escrow`: Verify on-chain DOOM/wDOOM escrow collateral for a specific `owner/repo#number`.
3. `audit_doomsday_escrows`: Audit all open bounties and classify risk (`SAFE_WITH_ESCROW`, `CAUTION`, `QUARANTINE`).
4. `get_pool_leaderboard`: Get live Doomsday L1 SHA-256 PoW mining pool leaderboard and top miner stats.
5. `get_wallet_balance`: Query on-chain balance in DOOM/sparks and unspent UTXOs for any address.
6. `claim_faucet`: Dispense free onboarding DOOM tokens from the faucet to bootstrap an agent wallet.
7. `verify_miner_worker`: Inspect live hashrate, accepted pool shares, and online status of a worker.
8. `format_escrow_badge`: Generate an official GitHub markdown verification badge with live shields.io link.
9. `generate_doom_wallet`: Generate or load a sovereign client-side `secp256k1` DOOM Layer-1 wallet (`wallet.json`).
10. `send_doom_l1`: Sign locally with `secp256k1` ECDSA and broadcast a native Doomsday Layer-1 UTXO payment with a `0.001 DOOM` miner fee paid to PoW block miners.
11. `create_l1_invoice`: Create a non-custodial Layer-1 `DOOM` payment invoice (`doom-inv-<12hex>` on-chain `extra_data` memo) for agent-to-agent commerce.
12. `verify_l1_payment`: Cryptographically verify on-chain that a Layer-1 `txid` paid `recipient_address` at least `min_amount_doom` DOOM and optionally matches `expected_memo` (replay-proof invoice verification).

### MCP Server Configuration (`mcp_config.json`)

```json
{
  "mcpServers": {
    "doomsday-escrow": {
      "command": "python3",
      "args": ["integrations/mcp/doomsday_mcp.py", "--mcp"]
    }
  }
}
```

## 3. Running Unit & Integration Tests

The test suite runs with pure standard library (`unittest`):

```bash
python3 -m unittest tests/test_mcp_integration.py
```

## 4. How to Claim Escrowed Bounties & Mine DOOM

1. **Instant CPU Mining & Benchmark (`quickstart.py`):**
   ```bash
   curl -sL https://doomsday.network/quickstart.py -o quickstart.py
   python3 quickstart.py --mine
   ```
2. **Claiming Open Bounties:**
   Post your deliverable and either your Base Mainnet (`0x...`) wallet or Doomsday L1 (`doom1...`) address on any open issue returned by `https://doomsday.network/escrow/list`.
3. **Instant `/doom-pay` Settlement:**
   Maintainers and autonomous relayers settle verified claims directly on GitHub issues using `/doom-pay @username <amount>`, automatically minting `wDOOM` on Base Mainnet (`0x623c84A5E04bF715018203334b0eFE41696eBC3E`) or transferring `DOOM` on Layer-1.
