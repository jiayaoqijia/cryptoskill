---
name: compute-blob-posting-cost-break-even
description: Use when choosing how many blobs to use or comparing blob versus calldata posting cost for an L2 batch under current L1 conditions.
---

# Compute blob posting cost break-even

Blobs and calldata are priced on different markets at different rates, so the only honest comparison
is done live against both base fees, with the break-even compression ratio derived rather than assumed.

## Procedure

1. Pull the two price inputs from the node. Calldata rides the EIP-1559 base fee; blobs ride the
   separate `blobBaseFee`, which is largely decoupled and can be near-zero or spiking independently.

       B=$(cast block latest --rpc-url $L1RPC --field baseFeePerGas)
       BF=$(cast rpc eth_blobBaseFee --rpc-url $L1RPC)

2. Model calldata cost. Gas per byte is 16 for non-zero and 4 for zero; a well-compressed batch is
   mostly non-zero. `calldata_gas = bytes × 16`; `calldata_eth = calldata_gas × B / 1e9`.

3. Model blob cost. Blob gas per blob is 131072 and the price is `blobBaseFee` in wei per blob-gas:
   `blob_eth = n_blobs × 131072 × BF / 1e9`. A batch needs `n_blobs = ceil(payload_bytes / 131072)`
   for uncompressed payload, but channels are compressed before posting, so use the compressed size.

4. Compute the break-even. Blobs win when
   `payload_bytes × 16 × B > ceil(bytes/131072) × 131072 × BF`. Solve for the compression ratio at
   which a blob batch becomes cheaper than carrying the equivalent calldata.

       python3 - <<'PY'
       B, BF = 30, 1          # gwei base fee, wei blob base fee (fill from the RPC calls)
       for payload in (64_000, 131_072, 400_000, 1_000_000):
           calldata = payload*16*B/1e9
           blobs = -(-payload//131_072)
           blob = blobs*131_072*BF/1e9
           print(payload, 'calldata', round(calldata,6), 'blobs', blobs, 'blob', round(blob,6))
       PY

5. Add the fixed overhead both sides share: the transaction's intrinsic calldata gas, the versioned
   hashes for blobs, and the signature. These matter at small batch sizes.

6. Report the choice as a function of payload size and both fees, plus the tier boundaries (at what
   byte count each option flips), so the decision survives a fee change rather than being a point
   snapshot.

## Pitfalls

- Comparing uncompressed payload sizes; L2 batchers compress, so the blob count is usually lower than
  `ceil(raw/131072)`.
- Holding `blobBaseFee` constant; it is far more volatile than the Execution base fee and can flip the
  decision within a few blocks.
- Ignoring the blob-count cap per block — a batch needing more blobs than the block allows must span
  blocks and pay fees twice.
- Using a fixed ETH/USD price; the comparison is gas-denominated and only converts to USD at the end.
- Forgetting that blob data is pruned, so the "cheaper" option may carry an archival cost the calldata
  path does not.

## Verification

    B=$(cast block latest --rpc-url $L1RPC --field baseFeePerGas); BF=$(cast rpc eth_blobBaseFee --rpc-url $L1RPC)
    echo "base=$B blobBaseFee=$BF"; python3 - <<'PY'
    B,BF=30,1  # replace with the echoed values
    bytes_=200_000; blobs=-(-bytes_//131_072)
    print('calldata', bytes_*16*B/1e9, 'blob', blobs*131_072*BF/1e9)
    PY

Report the live base fees used, the per-size cost for both options, the break-even byte count, and
the compression assumption behind it.
