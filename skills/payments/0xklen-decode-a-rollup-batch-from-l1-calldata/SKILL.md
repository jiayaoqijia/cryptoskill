---
name: decode-a-rollup-batch-from-l1-calldata
description: Use when reconstructing an L2 batch from the L1 batch-inbox transaction (calldata or blob) for indexing, verification, or a data-availability check.
---

# Decode a rollup batch from L1 calldata

The L1 batch-inbox transaction is the ground truth for an L2's data, but it is framed, often
compressed, and split across transactions — so decoding means reassembling frames into channels before
you can parse L2 blocks.

## Procedure

1. Locate the batch-posting transaction. On OP Stack everything sent to the batch inbox address
   `0x00...FF00000000000000000000000000000000000010` (the `BatchInboxAddress`, `0xFF` followed by
   zeros and `10`) is batcher data; find recent ones:

       cast logs --from-block $RECENT --to-block latest --address 0xFF00000000000000000000000000000000000010 --rpc-url $L1RPC

2. Fetch the raw input. Post-Dencun a batcher may post blobs; check the tx type and grab calldata or
   the blob sidecar:

       cast tx $BATCH_TX --json --rpc-url $L1RPC | jq '{type, input, blobVersionedHashes}'

3. Parse the channel frame format (OP Stack version 0): `channel_id (16 bytes) || frame_number (2) ||
   frame_data_length (4) || frame_data`. Frames of the same channel can be spread across transactions;
   reassemble by `channel_id`, concatenate frame data in `frame_number` order, and require all frames.

4. Decompress the reassembled channel. OP Stack channels are zlib-compressed, so inflate to get the
   batch stream. If you skipped a frame you will get a decompression error — that is the signal a frame
   is missing, not corrupt data:

       python3 - <<'PY'
       import zlib
       data = open('channel.bin','rb').read()
       print(len(zlib.decompress(data)))
       PY

5. Split the decompressed stream into batches (span-batch format version 1: block timestamp, block
   number, tx count, then per-tx fields), yielding the L2 blocks and their transactions.

6. Cross-check the reconstruction against the chain: the derived L2 block must hash to the state root
   that was committed, and the block header fields must match what the L2 RPC reports for that height.
   A mismatch means a decoding bug or a frame you missed.

7. Arbitrum instead uses a `SequencerInbox` batch with its own header and brotli compression; adjust
   the framer and decompressor to the chain's format rather than assuming the OP layout.

## Pitfalls

- Assuming one transaction is one channel; frames split across many L1 txs and must be joined by
  channel id, which is why a naive per-tx decode fails at block boundaries.
- Hard-coding zlib when the chain uses brotli (Arbitrum) or a different compression level.
- Reading calldata when the batch went in a blob; the tx input is empty and the data is in the sidecar.
- Losing the frame because you started from a later L1 block than the channel's first frame — always
  scan back a few hours for stragglers.
- Trusting the reconstructed blocks without the state-root check, missing a silent frame corruption.

## Verification

    cast tx $BATCH_TX --json --rpc-url $L1RPC | jq -r .input | cut -c1-100
    python3 -c "import zlib;d=open('channel.bin','rb').read();print('ok',len(zlib.decompress(d)))"
    # decoded L2 block header must match cast block $N --rpc-url $L2RPC

Report the batch-inbox tx hash, the number of frames/channels reassembled, the decompressed size, and
whether the derived block matches the committed state root.
