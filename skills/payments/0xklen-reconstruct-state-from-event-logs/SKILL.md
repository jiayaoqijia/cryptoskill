---
name: reconstruct-state-from-event-logs
description: Use when you must rebuild historical state (balances, totals, ownership) at a past block from emitted events, without an archive node.
---

# Reconstruct state from event logs

Event logs are the durable, full-node-queryable record of every state change. Replay them
from the deploy block up to a target block to reconstruct a mapping the contract does not
expose historically.

## Procedure

1. Find the deploy block so you never miss genesis state.

       cast tx $CREATION_TX --rpc-url $ETH_RPC --json | jq -r .blockNumber

2. Compute the event topic0 (indexed signature hash), then fetch logs in ranges. Free RPCs cap
   `eth_getLogs` spans (commonly 2k–10k blocks or 10k results) — chunk accordingly.

       SIG=$(cast keccak "Transfer(address,address,uint256)")
       for B in $(seq $START 1000 $END); do
         cast logs --from-block $B --to-block $((B+999)) \
           --address $TOKEN "$SIG" --rpc-url $RPC --json
       done > logs.json

3. Parse each log: `topics[0]` is the signature, `topics[1..]` are the indexed args
   (addresses are left-padded to 32 bytes), `data` holds the non-indexed args ABI-encoded.

       jq -r '.[] | [.blockNumber, .logIndex, .topics[1], .topics[2], .data] | @tsv' logs.json

4. Replay in `(blockNumber, logIndex)` order, applying the delta. For a plain ERC-20 Transfer,
   subtract `value` from `from` and add it to `to`:

       python3 - <<'PY'
       import json
       from collections import defaultdict
       bal = defaultdict(int)
       for l in json.load(open("logs.json")):
           v = int(l["data"], 16)
           frm = "0x" + l["topics"][1][-40:]
           to  = "0x" + l["topics"][2][-40:]
           bal[frm] -= v; bal[to] += v
       print(len(bal), sum(bal.values()))
       PY

5. Stop exactly at the target block, inclusive. If you fetched past it, filter out later logs.
6. Cross-check the reconstruction against a value the contract *does* expose now if the target
   block is the latest one (`cast call $TOKEN "totalSupply()(uint256)"`).

## Pitfalls

- Unordered logs: some providers return logs unsorted. Sort by `(blockNumber, logIndex)`
  before replay, or balances corrupt silently.
- Missing the deploy block omits the initial mint and every reconstructed balance is short.
- Fee-on-transfer / rebasing / reflection tokens emit extra Transfers or burn-to-self pairs;
  the naive `from -= v; to += v` model gives wrong balances for them.
- Logs from other contracts that use the same topic0 are included if you do not scope
  `--address`; filter by the exact emitting contract.
- `eth_getLogs` on a full node is fine (logs are indexed by block), but the block *range*
  limits are per-provider and per-plan — a silent empty result often means "range too wide",
  not "no events".
- State at an old block cannot be read this way for anything not derivable from events
  (e.g. internal balances kept in storage only via admin calls that emitted nothing).

## Verification

    cast call $TOKEN "totalSupply()(uint256)" --block $TARGET --rpc-url $ARCHIVE_RPC
    # equals the sum of all minted-minus-burned value from the replay

Report the block range scanned, the number of logs replayed, and the reconstructed total,
plus the matching on-chain `totalSupply` read if available.
