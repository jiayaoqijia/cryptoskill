---
name: submit-an-atomic-bundle-to-a-relay
description: Use when dispatching a signed bundle to a builder relay via eth_sendBundle, replacing a stale bundle, or cancelling one. Covers the signature header, replacementUuid, target block selection, and reading relay responses.
---

# Submit an atomic bundle to a builder relay

`eth_sendBundle` is a single HTTP POST that either gets picked by a builder in the named block or expires; there is no mempool to fall back on, so every field you send is the whole contract you have with the relay.

## Procedure

1. Sign the request body with your searcher key. The signature is over `keccak256(body)` produced by `flashbots.sign_bundle`, giving a header of the form `X-Flashbots-Signature: 0xAddr:0xSig`.

2. Build the params payload with only the fields you need:

   ```bash
   curl -s https://relay.flashbots.net -X POST -H "Content-Type: application/json" \
     -H "X-Flashbots-Signature: $FB_ADDR:$FB_SIG" \
     --data '{"jsonrpc":"2.0","id":1,"method":"eth_sendBundle","params":[{
       "txs":["0x.."], "blockNumber":"0x1299a20",
       "replacementUuid":"'$UUID'",
       "minTimestamp":0, "maxTimestamp":0 }]}'
   ```

3. Set `blockNumber` to one block, not a range. A range is only for `eth_sendBundle` targets in some relays; most builders reject multi-block targeting, and a bundle aimed too far ahead is discarded at zero cost to them and total cost to you.

4. Never mix different accounts' nonces in a way that only works if one leg lands. Bundles are evaluated as a unit; a nonce gap reverts the later leg and voids the whole bundle.

5. To replace a bundle you already sent, reuse the same `replacementUuid` and a strictly higher bid. Relays keep the highest-bid bundle per UUID, so a lower-bid replacement silently loses.

6. To cancel, send an empty `txs` array with the existing UUID and a higher bid; this is the only way to withdraw a bundle before its target block.

7. Read the response: `{"result": {"bundleHash": "0x.."}}` means accepted for consideration. An `error` object means the relay rejected it before any builder saw it — fix and resubmit, do not assume it is queued.

8. Retarget on every new head if the opportunity persists; a bundle for block N is dead the moment N is mined, unless the relay treats it as repeatable, which most do not.

## Pitfalls

- Reusing a `replacementUuid` from a different bundle shape. The relay replaces the whole payload, so you can accidentally delete a profitable bundle with a cheap one.
- Sending `blockNumber` far in the future to "keep options open". This spreads the bid across blocks and reduces the chance any single builder picks it.
- Assuming acceptance equals inclusion. `bundleHash` only confirms the relay parsed and stored it.
- Forgetting a bundle can be included in a block mined by a builder that never saw your second send; only the highest bid per UUID survives.

## Verification

    curl -s https://relay.flashbots.net -X POST -H "Content-Type: application/json" -H "X-Flashbots-Signature: $FB_ADDR:$FB_SIG" --data '{"jsonrpc":"2.0","id":1,"method":"eth_sendBundle","params":[{"txs":["0x.."],"blockNumber":"0x'$NEXT'"}]}'

A `bundleHash` in the result with no error field means accepted. Then confirm inclusion by fetching the block and grepping for your tx hash. Report the UUID, target block, bid, and whether the hash landed.
