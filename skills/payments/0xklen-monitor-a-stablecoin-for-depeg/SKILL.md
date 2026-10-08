---
name: monitor-a-stablecoin-for-depeg
description: Use when watching a stablecoin for a peg break in production. Polls multiple price sources, watches pool depth and redemption queues, and fires only on confirmed divergence.
---

# Monitor a stablecoin for a depeg

A single pool price is noise; a peg break is a divergence confirmed across independent sources with depth draining behind it. This skill defines the signals and the thresholds that separate a wobble from a run.

## Procedure

1. Poll at least three independent references every block: a Chainlink feed, a Curve/Uniswap `get_dy`, and a centralised book.
   `cast call $FEED "latestAnswer()(int256)" --rpc-url $RPC`
   `cast call $CURVE "get_dy(int128,int128,uint256)(uint256)" 0 1 1000000000 --rpc-url $RPC`
2. Convert each to a unit price; a pool's `get_dy` for 1,000,000 units already embeds the slippage at the size you care about.
3. Track depth separately: an $11M pool showing $1.0005 for 100k is intact; the same pool showing $0.997 for a 1M swap is draining.
4. Watch the redemption queue for issuer-backed coins: the time to redeem at par and whether it is gated.
5. Alert only when the median of sources is off peg beyond the band AND depth has fallen more than 20% in an hour. A 0.1% wobble in one venue is not an event.
6. Record the timestamped price of every source so the postmortem has the actual divergence path.
   `echo "{\"t\":$(date +%s),\"p\":$P,\"depth\":$D}" >> depeg.jsonl`

## Pitfalls

- Chainlink stablecoin feeds have a deviation threshold (often 0.25%) and a heartbeat; they can lag a fast break by minutes.
- A stale pool with a locked last price reads as a peg break; check the last swap timestamp.
- Averaging a real break with an unbroken source hides it; use the median and watch the spread.
- Alerting on absolute cents instead of basis points blows up on a 6-decimal versus 8-decimal feed mismatch.
- A feed that stops updating (heartbeat exceeded) can freeze the last price near par while the market has already broken.
- Stablecoin prices quoted on a CEX include its own withdrawal gating, which may differ from on-chain reality.
- Depth measured in units, not USD, misreads a pool when the numeraire itself is off peg.
- Alerting only on price and not on redemption queue length misses the run that never shows in the pool.

## Verification

    jq -r 'select(.p < 0.995 or .p > 1.005)' depeg.jsonl | wc -l
    # expect 0 on a healthy day; any line is a confirmed divergence to review

Report the median price, the spread across sources, and pool depth, with the polling command behind them.
