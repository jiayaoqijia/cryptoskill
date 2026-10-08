---
name: measure-on-chain-svg-gas-cost
description: Use when a generative NFT renders SVG or JSON inside the contract and tokenURI gas must stay under a viewer's call limit. Measures the real cost and the dominant contributor before optimizing.
---

# Measure on-chain SVG gas cost

Rendering an SVG inside the contract pushes bytes into `tokenURI`; naive concatenation can cost hundreds of thousands of gas per call and blow the `eth_call` gas limit some wallets use.

## Procedure

1. Baseline the byte size of a metadata read:

   ```
   cast call $NFT "tokenURI(uint256)(string)" 1 --rpc-url $RPC | wc -c
   cast call $NFT "tokenURI(uint256)(string)" 1 --rpc-url $RPC --gas-limit 50000000 >/dev/null && echo "renders"
   ```

2. Measure the actual gas with forge:

   ```
   forge test --match-test testTokenURIGas --gas-report
   ```

   or in a script: `forge script script/UriGas.s.sol --gas-limit 50000000`.

3. Decompose the cost. Static bytes read from storage are cheap; repeated `string.concat` in a loop grows O(n²) because each concat copies the whole running string. Prefer one `abi.encodePacked` pass.

4. Compare storage strategies per byte: a `bytes` slot costs 20000 gas SSTORE per 32-byte word, while SSTORE2 bytecode costs ~200 gas to deploy per byte and ~200 to read — cheaper for large static blobs read rarely.

5. Benchmark the base64 encoder separately. Pure-Solidity base64 of a fixed string is fine; encoding a long dynamic string in the same call nearly doubles the work.

6. Verify the rendered output parses before optimizing further:

   ```
   cast call $NFT "tokenURI(uint256)(string)" 1 --rpc-url $RPC \
     | jq -r '.image' | sed 's#data:image/svg+xml;base64,##' | base64 -d | xmllint --noout -
   ```

7. Set a budget: if `tokenURI` exceeds ~30M gas, some RPCs and wallets drop the call and the collection renders blank. Cut bytes, not promises.

## Pitfalls

- Optimizing storage misses the true cost: string concatenation and base64 dominate.
- SVG path data stored as `string[]` becomes one SLOAD per element per trait; pack the whole drawing into a single blob.
- `tokenURI` that reverts on a gas limit makes every token render blank across marketplaces at once.
- Off-by-one in base64 padding silently corrupts the image while still returning text.
- Gas measured by `eth_estimateGas` excludes part of the read path; measure with `eth_call` at an explicit high gas.

## Verification

    forge test --match-test testTokenURIGas --gas-report | grep -i tokenURI

Pass: the reported `tokenURI` gas is under your budget and `xmllint --noout -` exits 0 on the decoded SVG. Report the measured gas, the biggest cost contributor, and the storage strategy chosen.
