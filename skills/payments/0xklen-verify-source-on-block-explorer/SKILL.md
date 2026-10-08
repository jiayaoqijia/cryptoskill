---
name: verify-source-on-block-explorer
description: Use when you need to confirm a deployed contract is source-verified, that the verified source matches the deployer's code, and whether it is a proxy.
---

# Verify source on a block explorer

An unverified contract is a black box; a verified one can still be wrong if it is a proxy or
compiled with different settings. Pull the verified metadata and the source, then check the
match quality rather than trusting the green checkmark.

## Procedure

1. Fetch the verified metadata from Etherscan API v2 (one key, `chainid` selects the chain).

       curl -s "https://api.etherscan.io/v2/api?chainid=1&module=contract&action=getsourcecode\
       &address=$ADDR&apikey=$ETHERSCAN_API_KEY" \
         | jq -r '.result[0] | {ContractName, CompilerVersion, OptimizationUsed, Runs,
                              Proxy, Implementation, EVMVersion, Match}'

   `Match` is `"exact"` for a full bytecode match, `"similar"` for a partial/partial-match
   verification, and blank when the contract is not verified.

2. Download the source tree and read it locally.

       cast etherscan-source $ADDR -d /tmp/src_$ADDR
       find /tmp/src_$ADDR -name '*.sol' | head

3. Independent check via Sourcify (a second verification registry, no API key):

       curl -s "https://sourcify.dev/server/check-by-addresses?addresses=$ADDR&chainIds=1" \
         | jq -r '.[0] | {status, match}'

   `status: "perfect"` means the recompiled bytecode matches on-chain exactly.

4. For a proxy, verify the *implementation* contract, not the proxy shell. If the proxy is
   transparent/UUPS the implementation address is in the EIP-1967 slot; verify that address
   has its own verified source.
5. Recompile locally and compare bytecode if anything is off:

       forge build --root /tmp/src_$ADDR
       cast keccak "$(cast code $ADDR --rpc-url $ETH_RPC)"
       # compare against the compiled artifact's deployedBytecode

6. On chains Etherscan does not index, use Blockscout
   (`https://<chain>.blockscout.com/api/v2/smart-contracts/$ADDR`) or Sourcify directly.

## Pitfalls

- A verified proxy often shows the *proxy* ABI (just `upgradeTo`, `admin`); the real logic is
  in the implementation, which may be unverified or behind a different address.
- `Match: "similar"` means metadata or constructor args differ — do not treat it as exact.
- Constructor arguments are stored in the creation tx and are not in the .sol file; a mismatch
  there produces a bytecode diff at the tail.
- Some contracts are verified against a different compiler patch version or `via_ir` setting;
  comparing bytecode without matching settings produces false mismatches.
- Explorer caches: right after a deploy or upgrade the page may show stale or "pending
  verification". Re-query the API instead of trusting the rendered page.
- Blockscout and Etherscan can disagree on verification status; report both.

## Verification

    curl -s ".../getsourcecode...&address=$ADDR" | jq -r '.result[0].ContractName, .result[0].Match'
    curl -s "https://sourcify.dev/server/check-by-addresses?addresses=$ADDR&chainIds=1" | jq -r '.[0].status'

Report the contract name, the `Match` value from Etherscan, the Sourcify status, and the
implementation address if the target is a proxy.
