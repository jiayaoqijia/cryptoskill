---
name: track-erc4337-userops
description: Use when following an ERC-4337 UserOperation from submission to inclusion, decoding EntryPoint events, or debugging why a sponsored transaction reverted.
---

# Track ERC-4337 UserOperations

A UserOperation is a signed intent that a bundler wraps into a real transaction calling
`EntryPoint.handleOps`. Its success is reported by the `UserOperationEvent`, not by the
transaction receipt alone.

## Procedure

1. Know the EntryPoint per version — the address is part of every hash:

       # v0.7: 0x0000000071727De22E5E9d8BAf0edAc6f37da032
       # v0.6: 0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789
       cast call $ENTRYPOINT "getUserOpHash((address,uint256,bytes,bytes,bytes32,uint256,uint256,uint256,uint256,uint256,bytes,bytes))(bytes32)" \
         "(0x...,1,0x,0x,0x0000...00,100000,100000,21000,1,1,0x,0x)" --rpc-url $RPC

2. Ask the bundler for the op by hash (JSON-RPC on a bundler endpoint, not a node):

       curl -s -X POST "$BUNDLER" -H 'content-type: application/json' \
         --data '{"jsonrpc":"2.0","id":1,"method":"eth_getUserOperationByHash",
                  "params":["0x<userOpHash>"]}' | jq .
       curl -s -X POST "$BUNDLER" -H 'content-type: application/json' \
         --data '{"jsonrpc":"2.0","id":1,"method":"eth_getUserOperationReceipt",
                  "params":["0x<userOpHash>"]}' | jq -r '.result.success, .result.receipt.transactionHash'

3. Cross-check on-chain by decoding the EntryPoint logs. The authoritative event is
   `UserOperationEvent(bytes32,address,address,uint256,bool,uint256,uint256)`:

       TOPIC=$(cast keccak "UserOperationEvent(bytes32,address,address,uint256,bool,uint256,uint256)")
       cast logs --address $ENTRYPOINT "$TOPIC" --from-block $B --to-block $((B+5)) \
         --rpc-url $RPC --json | jq -r '.[] | [.topics[1], .topics[2], .data] | @tsv'

4. Estimate gas for a new op through the bundler before sending:

       curl -s -X POST "$BUNDLER" -H 'content-type: application/json' \
         --data '{"jsonrpc":"2.0","id":1,"method":"eth_estimateUserOperationGas",
                  "params":[{"sender":"0x...","callData":"0x...","nonce":"0x0"},$ENTRYPOINT]}' | jq .

5. On failure, look for `UserOperationRevertReason(bytes32,address,uint256,bytes)` and
   `PostOpRevertReason`, decode the inner revert, and check `success: false` in the event.

## Pitfalls

- `UserOperationEvent.success == false` means the outer op was *included* but the account's
  inner call reverted; the tx receipt still shows `status 0x1`. Do not equate tx success with
  op success.
- v0.6 vs v0.7 packing differs (the userOpHash and the `paymasterAndData` layout changed).
  A hash computed with the wrong version never matches on-chain.
- The nonce is 256 bits: a 192-bit key plus a 64-bit sequence. Reusing the key with a
  non-sequential value makes the op invalid.
- A revert in `postOp` (or an out-of-gas postOp) reverts the entire UserOperation even though
  validation passed; check `PostOpRevertReason`.
- Bundlers simulate against a slightly different state than the eventual block; an estimate
  that passes can still fail at inclusion under changed balances or allowances.

## Verification

    cast logs --address $ENTRYPOINT "$(cast keccak "UserOperationEvent(bytes32,address,address,uint256,bool,uint256,uint256)")" \
      --from-block $B --to-block $((B+10)) --rpc-url $RPC --json \
      | jq -r '.[0].data'   # last word region encodes success flag

Report the userOpHash, the inclusion tx hash, the `success` flag from
`eth_getUserOperationReceipt`, and any `UserOperationRevertReason`.
