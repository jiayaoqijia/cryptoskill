---
name: choose-calldata-vs-blob-for-batch-posting
description: Use when an L2 or application must decide whether to publish data to L1 as calldata or as EIP-4844 blobs, weighing cost, DA guarantee, and the retrieval window.
---

# Choose calldata vs blob for batch posting

Calldata is permanent and universally readable; blobs are cheaper but pruned after ~18 days and need a
consensus client to fetch — so the choice is a trade between cost and how long you can guarantee the
data is recoverable.

## Procedure

1. Price both options against the current market before deciding. Calldata costs 16 gas per non-zero
   byte (4 per zero byte) times the EIP-1559 base fee. Blobs use a separate blob-gas market.

       cast block latest --rpc-url $L1RPC --field baseFeePerGas
       cast rpc eth_blobBaseFee --rpc-url $L1RPC

2. Compute the calldata cost for your payload and the blob cost per blob. One blob is 131072 bytes
   (4096 field elements × 32); blob gas per blob is a protocol constant.

       python3 -c "bytes_=200000; base=30; print('calldata_eth', bytes_*16*base/1e9)"
       python3 -c "n=2; blobfee=1; print('blob_eth', n*131072*blobfee/1e9)"

3. Weigh the availability window, which is the real differentiator. EIP-4844 blobs are pruned after
   4096 epochs (~18.2 days), so an L2 that posts only blobs must keep the data elsewhere (its own
   storage, a DA layer) to let nodes reconstruct after pruning. Calldata lives forever in the chain
   history. If full-history DA is a hard requirement, calldata is the safe default.

4. Check the block blob limits that cap throughput: a block carries up to the max blob count (6
   pre-Pectra, 9 post-Pectra) with a target below it; a batch needing more blobs than fit must split
   across blocks and pay multiple blob fees.

5. Factor transparency and tooling. Calldata, though bigger, is readable by `eth_getTransactionByHash`
   and every explorer out of the box; blobs require a beacon-node sidecar fetch (see
   `verify-blob-data-availability-on-l1`), so your monitoring and any third-party verifier needs that
   path.

6. Decide per chain and per era, not once: the blob base fee can spike, and a chain that just migrated
   from calldata to blobs has a transition window where it must still serve old data. Record the
   choice with the fee snapshot and the pruning date.

## Pitfalls

- Assuming blobs are "permanent DA"; they are pruned, so a blob-only poster that does not archive is
  unavailable after ~18 days.
- Comparing byte costs without the compression an L2 batcher applies; raw calldata cost overstates the
  real cost, and blob channels are often compressed first.
- Ignoring the blob-count cap and planning a single batch larger than a block's blob budget.
- Forgetting that a blob transaction still pays normal calldata gas for its versioned hashes and
  signature.
- Migrating a chain to blobs without a fallback to calldata for when the blob market is expensive.

## Verification

    cl=$(cast block latest --rpc-url $L1RPC --field baseFeePerGas)
    bf=$(cast rpc eth_blobBaseFee --rpc-url $L1RPC)
    python3 -c "print('calldata_usd@16g', $cl*16/1e9*2000*ENTER_BYTES, 'blob_usd', $bf*131072/1e9*2000)"
    # verify ENTER_BYTES against your actual compressed batch size

Report the two cost figures, the number of blobs required, the availability-window consequence, and
the block-limit check, each tied to the RPC call it came from.
