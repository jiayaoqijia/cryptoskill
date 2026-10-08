---
name: nonce-management-under-retries
description: Use when a transaction is stuck or you are retrying a send. Reads the pending nonce, replaces with the same nonce at a higher fee, and prevents two in-flight txs from the same account colliding.
---

# Manage nonces under retries

Every resend from the same account is either a replacement or a new transaction, and picking the wrong one leaves a stuck nonce that blocks everything behind it. This skill pins the nonce, replaces deliberately, and keeps only one in-flight transaction per account.

## Procedure

1. Read the nonce that includes pending transactions, not the mined one:
   `cast nonce $SENDER --block pending --rpc-url $RPC`
   `--block latest` omits your own pending txs and will produce a nonce collision.
2. To replace a stuck tx, reuse the same nonce with a higher fee. Nodes accept a replacement only above a bump threshold (commonly 10-12%):
   `cast send $TO "transfer(address,uint256)" $RECIPIENT 1000 --nonce 42 --max-fee-per-gas 40gwei --account deployer --rpc-url $RPC`
3. Never send two different transactions with the same nonce from the same key. The second either replaces the first or is dropped; either way one payload is silently lost.
4. Serialize sends per account. If a tool sends in parallel, set the nonce explicitly for each and wait for each to be mined before starting the next.
5. For a batch, check the head nonce once, increment locally, then verify against `pending` after each accept:
   `cast nonce $SENDER --block pending --rpc-url $RPC`
6. If you must abandon a nonce, cancel it with a self-transfer of value 0 at that nonce rather than leaving the gap.
7. After recovery, confirm the head nonce equals your local count so no gap remains.

## Pitfalls

- A gap in nonces stalls every later tx from that account until the missing one is mined; a dropped tx creates exactly that gap.
- Some RPCs return `latest` for `pending`, under-reporting your own in-flight sends. Cross-check two providers when retrying.
- A replacement must raise the fee by the node's minimum bump; a 1% increase is rejected as "replacement transaction underpriced".
- Sending from the same key on two chains is fine (per-chain nonces), but reusing the signed tx bytes across chains is a replay bug, not a nonce one.
- A pending tx that never mines holds its nonce indefinitely; without a cancel it blocks the whole account.

- A cancel tx that itself gets stuck holds the nonce open; escalate its fee until it lands.
- Tools that estimate nonces locally drift from the chain after a failed send; always re-read from `pending`.
- Two processes sharing one key will collide; give each process its own account or a strict lock.

## Verification

    cast nonce $SENDER --block pending --rpc-url $RPC && cast nonce $SENDER --block latest --rpc-url $RPC
    # expect pending to exceed latest by exactly the number of your in-flight txs

Report the pending nonce, the latest nonce, and the in-flight count, quoting the commands.
