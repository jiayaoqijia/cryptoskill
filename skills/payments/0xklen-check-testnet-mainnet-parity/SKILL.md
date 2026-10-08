---
name: check-testnet-mainnet-parity
description: Use when a protocol works on a testnet and you must decide whether it will behave identically on mainnet, or when porting addresses and config between networks.
---

# Check testnet/mainnet parity

Testnet success is not mainnet success. Gas, block time, reorg depth, available opcodes,
oracle and token addresses, and contract bytecode all differ. Verify each axis instead of
assuming the networks are interchangeable.

## Procedure

1. Compare the deployed bytecode of the same "address" on both networks. Identical code means a
   deterministic (CREATE2) deploy; different code means you are looking at two contracts.

       cast code $ADDR --rpc-url $SEPOLIA_RPC | cast keccak
       cast code $ADDR --rpc-url $MAINNET_RPC  | cast keccak

2. Verify chain-specific constants. WETH, USDC, Chainlink feeds and multicall are *not* the same
   address across chains. Read them from a config keyed by chain id, never hardcode.

       cast call $WETH "symbol()(string)" --rpc-url $MAINNET_RPC
       # WETH9 mainnet 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
       # WETH9 sepolia 0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14

3. Compare execution economics: block time, base fee, gas limits, and EIP-1559 status.

       cast block latest --json --rpc-url $MAINNET_RPC | jq -r '.timestamp, .gasLimit, .baseFeePerGas'
       cast block latest --json --rpc-url $SEPOLIA_RPC | jq -r '.timestamp, .gasLimit, .baseFeePerGas'

4. Check opcode/feature availability on the target chain (L2s and older testnets lag): `PUSH0`
   (Shanghai), transient storage (`TSTORE`/`TLOAD`, Cancun), and blob transactions differ.
   Deploying bytecode compiled for a newer EVM to an older chain reverts on the first `PUSH0`.
5. Run the project's own tests against a mainnet fork, then against the testnet, and diff the
   outcomes:

       forge test --fork-url $MAINNET_RPC -vvv
       forge test --fork-url $SEPOLIA_RPC -vvv --no-match-test "MainnetOnly"

6. Confirm deployment addresses match your expected list by reading them back, not by trusting
   a shared `deployments.json` (which frequently mixes networks).

## Pitfalls

- Testnet reorgs are far more frequent and deeper than mainnet; a tx confirmed on Sepolia can
  still be reorged out minutes later. Wait more confirmations on testnets, not fewer.
- Faucet/sandbox testnets reset; addresses and state vanish without notice. Never treat testnet
  state as persistent.
- Chainlink feeds exist at different addresses per network and some testnets run different
  heartbeat intervals — an oracle that updates hourly on mainnet may go stale for days on a
  testnet.
- Gas price assumptions ported from testnet (often ~0) break on mainnet; always estimate on the
  target chain.
- Same-nonce deployments produce the same address only if both the deployer and nonce match;
  reusing a nonce value across chains with different prior txs yields different addresses.

## Verification

    cast code $ADDR --rpc-url $MAINNET_RPC | cast keccak
    cast code $ADDR --rpc-url $SEPOLIA_RPC | cast keccak
    # equal hashes -> deterministic deploy; unequal -> different contract

Report each parity axis (bytecode hash, chain constants, gas params, EVM feature set) and mark
any divergence that could change behaviour.
