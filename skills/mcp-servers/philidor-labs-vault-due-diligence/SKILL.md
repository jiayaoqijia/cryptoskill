---
name: vault-due-diligence
description: >
  Use this when the user wants due diligence, an underwriting memo, or a
  risk report on one named DeFi vault, curator, or vault address before
  allocating. Cite only identifiers and figures the Philidor tools return.
---

# Vault due diligence

Philidor is read-only. It does not hold a wallet, compute a health factor, or prepare a transaction. Every score, tier, APR, TVL, and incident in the answer must come from a tool result in this turn. If a field is absent, say it was not returned. Never invent a risk number, address, or id.

The hosted server is `https://mcp.philidor.io/api/mcp`. If these tools are not connected, stop and say the Philidor MCP server is unavailable.

## Resolve the vault first

1. If the user gave a vault id, or a network slug plus address, call `get_vault` with that pair. Lookup is `id`, or both `network` and `address`. EVM addresses are `0x` hex. Solana addresses are case-sensitive base58.
2. If they gave only a name, curator, asset, or chain, call `search_vaults` (`query`, plus `chain`, `protocol`, `asset`, or `riskTier` when they named them). Pick a row only when the returned name, chain, and asset match the request. If several rows match, list the returned ids and ask which one. Do not guess an address.
3. Aave V4 vaults are `protocol=aave` and `protocolVersion=v4`. `aave-v4` is an accepted alias. It is not a separate protocol id.

## Then read the evidence

4. Call `get_vault_risk_breakdown` with the `network` and `address` from the `get_vault` result. The breakdown is four vectors: Asset Composition, Platform and Strategy, Control and Governance, and History.
5. When the vault payload includes a protocol id, call `get_protocol_info` with that id. When it includes a curator id, call `get_curator_info` with that id. Use the id string the tool returned.
6. To interpret a score the tools already returned, call `explain_risk_score` with that exact number (0–10). Read `philidor://methodology` before explaining how the score is built. Do not recite weights, caps, or tier cutoffs from memory.
7. If the client exposes MCP prompts, `vault_due_diligence` takes `network` and `address` and covers the same report.

## What the report must contain

- Vault id, network slug, and address, copied from the tool result.
- Composite score, tier (Prime, Core, or Edge), and the four vector scores that were returned.
- TVL, APR fields as labeled (keep base yield and rewards separate when both are present), audit or review status, and deposit status (`open`, `closed`, or `unknown`).
- Recent events returned on the vault, plus protocol incidents returned by `get_protocol_info`.
- A one-line limit: a higher Philidor score means lower assessed risk under the current methodology. It is not a safety guarantee, a return guarantee, or an allocation instruction.

`find_safest_vaults` is a different task (a top-10 audited screen). Do not substitute it for diligence on one named vault.
