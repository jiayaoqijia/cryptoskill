---
name: submit-transaction-through-private-mempool
description: Use when a transaction must not be front-runnable: sending to Flashbots Protect, MEV Blocker, or a builder bundle. Covers RPC endpoints, the send calls, and verifying non-public inclusion.
---

# Submit a transaction through a private mempool

A private mempool keeps your signed transaction out of the public gossip layer so searchers cannot see and front-run it; the cost is that inclusion is not guaranteed and depends on a builder choosing the bundle.

## Procedure

1. Choose an endpoint: Flashbots Protect `https://rpc.flashbots.net`, MEV Blocker `https://rpc.mevblocker.io`, or a bloXroute Protect endpoint with auth. These are drop-in JSON-RPC URLs.

2. Point the client at it — no code change beyond the URL:

   ```javascript
   const provider = new ethers.JsonRpcProvider("https://rpc.flashbots.net");
   const tx = await wallet.sendTransaction({ to, data, value, gasLimit, maxBlockNumber });
   ```

   or, with cast:

   cast send $TO --value 1ether --private-key $PK --rpc-url https://rpc.flashbots.net

3. For an explicit bundle, sign raw transactions and submit:

   curl -s https://relay.flashbots.net -X POST -H "Content-Type: application/json" \
     --data '{"jsonrpc":"2.0","id":1,"method":"eth_sendBundle","params":[{"txs":["0x..."],"blockNumber":"0x'$NEXT'"}]}'

4. For a single private tx use `eth_sendPrivateTransaction` with `maxBlockNumber`. Always set the expiry — a private tx with no expiry can land days later at a stale price.

5. Verify non-public inclusion: the tx will not appear in a public `txpool_content` call, and inclusion usually comes from a builder block. Check the receipt against the private endpoint:

   curl -s https://rpc.flashbots.net -X POST -H "Content-Type: application/json" \
     --data '{"jsonrpc":"2.0","id":1,"method":"eth_getTransactionReceipt","params":["0x'$HASH'"]}'

6. Set `maxPriorityFeePerGas` and `maxFeePerGas` explicitly; private relays still require a tip. On mainnet a 0.05–0.2 gwei tip plus a fee above base is typical; too low and the bundle is dropped silently.

## Pitfalls

- Assuming privacy: a "protected" RPC that forwards to the public mempool on failure leaks the tx. Check the provider's documented fallback.
- Bundles are atomic: if any tx would revert, the whole bundle is dropped. Simulate first with `cast call` before submitting.
- Private inclusion can span multiple blocks; no receipt after `maxBlockNumber` means it expired — resubmit or raise the tip.

## Verification

    curl -s https://rpc.flashbots.net -X POST -H "Content-Type: application/json" \
      --data '{"jsonrpc":"2.0","id":1,"method":"eth_getTransactionReceipt","params":["0x'$HASH'"]}'

A receipt from the private endpoint, absent from a public node, confirms private routing.

Report the endpoint, `maxBlockNumber`, tip, and the receipt block.
