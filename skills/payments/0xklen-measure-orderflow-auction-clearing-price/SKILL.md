---
name: measure-orderflow-auction-clearing-price
description: Use when auditing what an orderflow auction actually paid a user, or pricing a bid into one: reading MEV-Share/MEV-Blocker refunds, reconstructing the clearing bid, and comparing against a counterfactual public-mempool execution.
---

# Measure an orderflow auction's clearing price

An orderflow auction is only worth using if its clearing price beats the counterfactual — a private route that saves you from a sandwich but pays back nothing can still be worse than a tight-slippage public swap.

## Procedure

1. Identify the flow path. For MEV-Share, transactions are submitted to `https://mev-share.flashbots.net`; the refunds arrive as separate ETH transfers to the user address in the same block. For MEV Blocker, refunds come from the `MEVBlocker` contract.

2. Find the refund. List inbound ETH transfers to the user in block N:

   ```bash
   cast receipt $TXHASH --rpc-url $RPC | grep -iE "from|to|value"
   ```

   and, for internal transfers, replay the block with traces:

   ```bash
   cast run $TXHASH --rpc-url $RPC --trace
   ```

3. Reconstruct the clearing price: `refund / extracted_value`. The extracted value is the price improvement the searcher earned net of the user's slippage limit. If the user set `amountOutMin` at the true mid, the refund is the entire surplus.

4. Build the counterfactual. Take the same swap, quote it at the prior block's mid (no sandwich) and at the prior block's mid minus a plausible sandwich (front-run to `amountOutMin`). The auction is only a win if the refund puts the realized rate closer to the no-sandwich mid than the counterfactual.

5. Convert to basis points: `saving_bps = (realized_rate / no_sandwich_mid - 1) * 10000`. A refund worth less than 5 bps on a competitive pair is within noise once gas is counted.

6. Track it over 50 transactions. A median refund of exactly zero means the auction never had competing bids — you are paying the latency cost for nothing and should route elsewhere.

7. Compare auctions pairwise for the same pair and size: run the identical swap through two OFAs and diff the realized rates. The higher clearing price is the one to keep.

## Pitfalls

- Counting a refund that is really gas rebate from the relay, not auction proceeds. Check the sender contract is the auction, not the user's own bundler.
- Assuming a large refund means a good route. A refund can be large while the fill is still worse than a public swap with 0.1% slippage.
- Ignoring that MEV-Share refunds require opting in to share the calldata hints; without hints the auction has nothing to bid on and pays nothing.
- Measuring one block. Clearing prices spike on volatile blocks and are flat on quiet ones, so a single sample proves nothing.
- Forgetting that the counterfactual itself uses a private route; comparing to a public sandwich you were never going to get overstates the benefit.

## Verification

    cast run $TXHASH --rpc-url $RPC --trace | grep -iE "value|transfer"

Sum inbound refunds and divide by the extracted amount to get the clearing share; confirm it is nonzero and exceeds the counterfactual gap. Report realized rate, counterfactual rate, refund, and saving in bps across the sample.
