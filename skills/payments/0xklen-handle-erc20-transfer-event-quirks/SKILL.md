---
name: handle-erc20-transfer-event-quirks
description: Use when indexing ERC-20 Transfer and Approval events. Handles tokens that return no value, move funds without a compliant event, or use non-standard decimals so balances stay correct.
---

# Handle ERC-20 event quirks

Not every token emits a canonical `Transfer`. Indexing by event alone under-counts tokens that move funds without one, and mis-scales those with unusual decimals.

## Procedure

1. Match the canonical topic, remembering ERC-20 amounts are not indexed here:
   `topic0 = keccak("Transfer(address,address,uint256)") = 0xddf252ad...23b3ef`; `from` and `to` are indexed, `value` sits in data.
2. Tokens that return no boolean (USDT-style) cannot be judged by a call's return; the event is the record. Do not require a return value.
3. Read `decimals()` once per token and store it; an 18-decimal default is wrong for USDC (6) and WBTC (8):
   `cast call $TOKEN "decimals()(uint8)" --rpc-url $RPC`
4. For fee-on-transfer tokens, trust the emitted `value` over a computed balance delta; index the event amount.
5. Detect event-less movers by comparing indexed balance deltas against event sums per block; flag tokens where they diverge.
6. Store the raw amount and the decimals; render human units from both, never bake the scaled value into storage.
7. Cache `decimals()` and `symbol()` per token in a metadata table so re-indexing does not spam `eth_call`.
8. For tokens whose `Transfer` topic differs, match the exact 32-byte topic0, not a prefix.

## Pitfalls

- Assuming every token has 18 decimals scales USDC by 1e12 wrongly.
- Requiring a boolean return treats USDT-like tokens (which return nothing) as failures and drops real transfers.
- Rebase tokens change balances with no `Transfer`; event-only indexing misses them.
- Proxy tokens emit `Transfer` from the proxy or the implementation; filter on both when the token was upgraded.
- A token upgraded behind a proxy can change `decimals()` mid-history; store decimals per block range if it ever changes.
- Assuming `value` is uint256 for a signed-amount token mis-decodes; check the ABI rather than the convention.

## Verification

    cast call $TOKEN "decimals()(uint8)" --rpc-url $RPC
    psql -c "SELECT sum(value) FROM transfers WHERE token=$TOKEN AND block_number BETWEEN $A AND $B;"
    # compare against the holder balanceOf delta across the same range

Report the token's decimals, whether it returns a boolean, and event-sum versus balance-delta agreement.
