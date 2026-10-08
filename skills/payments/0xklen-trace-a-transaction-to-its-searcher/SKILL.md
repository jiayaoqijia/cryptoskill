---
name: trace-a-transaction-to-its-searcher
description: Use when attributing MEV extraction to a specific searcher: linking profit-taking transactions to funding sources, bundler contracts, and relay bid traces to identify the operator behind an address.
---

# Trace a transaction to its searcher

A searcher address is thrown away after each campaign, so identification comes from the infrastructure around it — funding edges, shared bundler contracts, and the relay bids a bundle must have carried to be included.

## Procedure

1. Identify the profit-taking transaction in the block. Look for a transaction whose sender's balance increase exceeds any plausible transfer: the delta on the searcher address at block boundaries.

2. Hop one funding edge back. Trace where the gas for the searcher came from:

   ```bash
   cast run $TXHASH --rpc-url $RPC --trace | grep -iE "staticcall|transfer|value"
   ```

   Automated searchers are usually funded from a common hot wallet, so the funding wallet is the more stable identifier than the throwaway.

3. Cluster by deployment. Pull the contracts the searcher called and check their deployer; searcher bots often share one factory or one deployer address across many throwaway EOAs.

4. Cross-reference the block's relay bid traces. For a Flashbots-included bundle, the builder block data lists the winning searchers' payment and sometimes their signature:

   ```bash
   curl -s "https://relay.flashbots.net/relay/v1/data/bidtraces/builder_blocks_received?block_number=$N"
   ```

5. Match timing. A searcher's inclusion lag from the triggering swap is a fingerprint; if address A always lands one block after a specific app's transactions, it is a specialised bot for that app.

6. Build a graph: searcher → funder → deployer → bundler → relay. Two addresses sharing a funder and a deployer are the same operator with high confidence; sharing only a funder is weaker.

7. State the confidence. Address-level attribution is a probabilistic claim; report the edges you used and the alternative explanation (e.g. a shared non-digging backend).

## Pitfalls

- Treating a funded EOA as the operator. Funders and deployers outlast the throwaway and should be the anchor identity.
- Ignoring that a profitable transaction can be a copy of another operator's; attribution is about who landed it, not who found it.
- Matching on calldata alone; many searchers use the same public arb router, so identical calldata is not identity.
- Assuming the bundler contract is unique. Popular builders' contracts are shared across hundreds of searchers.
- Over-reading a single funding edge; mixers and CEX withdrawals create false shared-funder links.

## Verification

    cast run $TXHASH --rpc-url $RPC --trace | grep -iE "from|to|value"

List the funding edge, deployer, and bid trace for the address; two independent edges (funder and deployer) agreeing is the threshold for a confident attribution. Report the address, edges, and confidence.
