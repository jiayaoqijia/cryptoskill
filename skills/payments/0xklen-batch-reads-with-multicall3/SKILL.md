---
name: batch-reads-with-multicall3
description: Use when you need to read many contracts or many values in one round trip to cut RPC calls and avoid partial failures aborting the whole batch.
---

# Batch reads with Multicall3

Multicall3 aggregates many `eth_call`s into one call, deployed at the same address on 100+
chains via a pre-signed transaction. Use `aggregate3` with `allowFailure` so one bad read does
not revert the batch.

## Procedure

1. Confirm Multicall3 is deployed at the canonical address on this chain.

       cast code 0xcA11bde05977b3631167028862bE2a173976CA11 --rpc-url $RPC | head -c 4
       # not 0x -> deployed; 0x -> not present, batch at the RPC level instead

2. Build `aggregate3` calls. Each element is `(address target, bool allowFailure, bytes callData)`.
   Encode an ERC-20 balanceOf call with the selector 0x70a08231 plus the 32-byte-padded holder.

       cast calldata "balanceOf(address)" 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
       cast call 0xcA11bde05977b3631167028862bE2a173976CA11 \
         "aggregate3((address,bool,bytes)[])((bool,bytes)[])" \
         "[(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48,true,0x70a08231000000000000000000000000d8dA6BF26964aF9D7eEd9e03E53415D37aA96045)]" \
         --rpc-url $RPC

3. In viem, the client does the encoding and decoding for you:

       const results = await client.multicall({
         contracts: [
           { address: usdc, abi: erc20Abi, functionName: 'balanceOf', args: [holder] },
           { address: weth, abi: erc20Abi, functionName: 'balanceOf', args: [holder] },
         ],
         allowFailure: true,
       })

4. Pin the block so every sub-read is consistent:

       cast call $MULTICALL "aggregate3((address,bool,bytes)[])((bool,bytes)[])" "[...]" \
         --block 18000000 --rpc-url $ARCHIVE_RPC

5. Handle per-call failure: with `allowFailure=true` the result is `(bool success, bytes returnData)`
   per entry; decode only the successful ones and report which failed.

## Pitfalls

- The older `aggregate((address,bytes)[])` (no allowFailure) reverts the entire batch if any
  single call reverts — use `aggregate3` with `allowFailure=true` for reads across unknown
  contracts.
- A revert inside `aggregate3` with `allowFailure=false` loses all results; with `true` the
  failed entry returns an empty `returnData` that you must guard before decoding.
- Multicall is still an `eth_call` at the RPC level; some providers count the whole batch as
  many compute units, so it saves round trips but not always quota.
- Multicall3 is *not* deployed on every chain — a few L2s/testnets need a one-time deploy.
  `cast code` returning `0x` means all your batched reads return nothing.
- All sub-reads share one block tag; if you need "latest" for each, you are implicitly pinning
  to one height and losing the notion of live data.

## Verification

    cast code 0xcA11bde05977b3631167028862bE2a173976CA11 --rpc-url $RPC | head -c 4   # not 0x
    # compare one aggregate3 result against a direct cast call to the same contract

Report the number of sub-calls batched, the block pinned, and each `(success, value)` pair;
confirm they match individual `cast call` reads.
