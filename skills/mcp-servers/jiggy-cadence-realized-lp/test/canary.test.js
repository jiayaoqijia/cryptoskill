/**
 * canary.test.js — prove the instrument can tell a win from a loss.
 *
 * Origin: our own trading stack scored an LP call +1.7% WIN when the real result was
 * about -14%, because resolution was fee income with no price term. Fee APR is always
 * positive, so the lane arithmetically could not lose. This test is the negative control
 * that failure never had.
 *
 * Run offline (pure math): node test/canary.test.js
 * Run with live data too:  GRAPH_API_KEY=xxx node test/canary.test.js --live
 */
import { impermanentLossPct, scorePool, summarize, gatewayUrl, fetchTopPools, fetchPoolFrom, positionRealized, priceCollapsed, isLive, pearson, spearman } from '../lib/realized.js';
import { concentratedIlPct, outOfRange } from '../lib/concentrated.js';
import { tickToPrice, tickRangeToWidth, describePosition, fetchWalletPositions, EFFECTIVELY_FULL_RANGE_SPAN, TICK_MIN, TICK_MAX } from '../packages/core/src/wallet.js';

let failed = 0;
const check = (name, got, want, tol = 0.01) => {
  const ok = (got === null || want === null)
    ? got === want
    : Math.abs(got - want) <= tol;
  if (!ok) failed++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : `  (got ${got}, want ${want})`}`);
};

console.log('--- concentrated (v3) IL: must converge to v2 AT THE ANALYTIC RATE ---');
// Do NOT assert "v3 == v2 within epsilon" for a large range. It does not, and picking an
// epsilon that passes is choosing a parameter. The error falls as O(1/sqrt(w)), so a 100x
// wider range must shrink it ~10x. That is a rate, and a rate cannot be fudged by a knob.
// This test was written after the naive epsilon version failed and nearly got the correct
// new math thrown away as broken (2026-09-07).
{
  const probe = [0.5, 0.8, 1.25, 2, 4];
  const err = (w) => Math.max(...probe.map((r) => Math.abs(concentratedIlPct(r, w) - impermanentLossPct(r))));
  let prev = null;
  for (const w of [1e2, 1e4, 1e6, 1e8]) {
    const e = err(w);
    if (prev !== null) {
      const shrink = prev / e;
      const ok = shrink > 8 && shrink < 12;
      if (!ok) failed++;
      console.log(`${ok ? 'PASS' : 'FAIL'}  w=1e${Math.log10(w)}: error shrank ${shrink.toFixed(1)}x per 100x range (expect ~10x)`);
    }
    prev = e;
  }
}
check('concentrated IL at r=1 is exactly 0 (tight range)', concentratedIlPct(1, 1.25), 0, 1e-9);
check('concentrated IL at r=1 is exactly 0 (wide range)', concentratedIlPct(1, 4), 0, 1e-9);
check('concentrated IL is never positive', [0.05, 0.5, 0.9, 1, 1.1, 2, 50].every((r) => concentratedIlPct(r, 2) <= 1e-9) ? 1 : 0, 1);
check('tighter range hurts more than wider at the same move', concentratedIlPct(1.5, 1.25) < concentratedIlPct(1.5, 4) ? 1 : 0, 1);
check('full-range v3 ~ v2 to 2 decimal places', concentratedIlPct(2, 1e8), impermanentLossPct(2), 0.01);
check('outOfRange true when price leaves the band', outOfRange(1.5, 1.25) ? 1 : 0, 1);
check('outOfRange false inside the band', outOfRange(1.1, 1.25) ? 1 : 0, 0);

console.log('\n--- correlation helpers: must find a signal that is known to be there ---');
check('pearson(x, x) = 1', pearson([1, 2, 3, 4, 9], [1, 2, 3, 4, 9]), 1, 1e-9);
check('pearson(x, -x) = -1', pearson([1, 2, 3, 4, 9], [-1, -2, -3, -4, -9]), -1, 1e-9);
check('spearman survives a monotone nonlinearity where pearson would not', spearman([1, 2, 3, 4], [1, 4, 9, 100]), 1, 1e-9);
check('degenerate input returns null, not NaN', pearson([1, 1, 1], [1, 2, 3]), null);

console.log('\n--- impermanent loss: known constant-product values ---');
check('IL at r=1 (no divergence) is exactly 0', impermanentLossPct(1), 0, 1e-9);
check('IL at r=2 (price doubled) ~ -5.72%', impermanentLossPct(2), -5.719);
check('IL at r=0.5 (price halved) ~ -5.72%', impermanentLossPct(0.5), -5.719);
check('IL at r=4 ~ -20.0%', impermanentLossPct(4), -20.0, 0.05);
check('IL at r=0.3 (down 70%) ~ -15.75%', impermanentLossPct(0.3), -15.75, 0.05);
check('IL of a dead token (r=0) is -100', impermanentLossPct(0), -100, 0);
check('IL is never positive', impermanentLossPct(1.0001) <= 0 ? 0 : 1, 0, 0);

console.log('\n--- NEGATIVE CONTROL: the real call that was scored a win ---');
// call_lp_1785388443061: 1233% advertised APR, held 12.13h, token was -70% over the hold.
{
  const feePnl = (1232.695836788408 / 365) * (12.13 / 24); // the +1.7% it was credited
  const il = impermanentLossPct(0.3);
  const net = feePnl + il;
  console.log(`  fees +${feePnl.toFixed(2)}%  IL ${il.toFixed(2)}%  net ${net.toFixed(2)}%`);
  check('re-scores as a LOSS', net < 0 ? 0 : 1, 0, 0);
  check('  ...and by a wide margin, not a rounding call', net < -10 ? 0 : 1, 0, 0);
}

console.log('\n--- unmeasurable must stay distinguishable from zero ---');
check('missing price -> measurable:false, not 0',
  scorePool({ id: '0x1', feeTier: '3000', token0: { symbol: 'A' }, token1: { symbol: 'B' },
    poolDayData: Array.from({ length: 30 }, () => ({ date: 1, volumeUSD: '1', feesUSD: '1', tvlUSD: '1000000', token0Price: '0' })) }).measurable ? 1 : 0, 0, 0);
check('short window -> measurable:false',
  scorePool({ id: '0x2', feeTier: '3000', token0: { symbol: 'A' }, token1: { symbol: 'B' },
    poolDayData: [{ date: 1, feesUSD: '1', tvlUSD: '1000000', token0Price: '1', volumeUSD: '1' }] }).measurable ? 1 : 0, 0, 0);

console.log('\n--- collapse detector: dead tokens must not pass the liveness gate ---');
// Shape modeled on UST/WETH: real activity/volume/TVL for months, price -> ~0.
// This is the exact pool that survived every activity-only gate on 2026-09-06.
{
  const collapsedPool = {
    id: '0xdead', feeTier: '3000', token0: { symbol: 'UST' }, token1: { symbol: 'WETH' },
    poolDayData: [
      // most-recent-first (desc), price near zero now
      ...Array.from({ length: 20 }, (_, i) => ({ date: i, feesUSD: '500', volumeUSD: '80000', tvlUSD: '2000000', token0Price: '0.0002' })),
      // older days at a normal ~$1 peg
      ...Array.from({ length: 20 }, (_, i) => ({ date: 20 + i, feesUSD: '500', volumeUSD: '80000', tvlUSD: '2000000', token0Price: '1.0' })),
    ],
  };
  check('priceCollapsed detects a >99% peak-to-current drop', priceCollapsed(collapsedPool) ? 0 : 1, 0, 0);
  const scored = scorePool(collapsedPool);
  check('collapsed pool is excluded by isLive() despite passing activity/volume/TVL',
    isLive(scored) ? 1 : 0, 0, 0);

  const ordinaryPool = {
    id: '0xalive', feeTier: '3000', token0: { symbol: 'LINK' }, token1: { symbol: 'WETH' },
    poolDayData: Array.from({ length: 30 }, (_, i) => ({ date: i, feesUSD: '500', volumeUSD: '80000', tvlUSD: '2000000', token0Price: String(1 + i * 0.002) })),
  };
  check('ordinary volatility (not a collapse) is NOT flagged', priceCollapsed(ordinaryPool) ? 1 : 0, 0, 0);
}

console.log('\n--- summarize() refuses to certify without a stable-pair canary ---');
{
  const noStables = summarize([{ measurable: true, stablePair: false, impermanentLossPct: -3, misleading: true,
    advertisedAprPct: 5, realizedAprPct: -2, gapPts: 7, currentTvlUsd: 1e6,
    liveness: { activeDays: 30, recent7dVolumeUsd: 1e6 } }]);
  check('canary.passed is false when no stable pair is present', noStables.canary.passed ? 1 : 0, 0, 0);
}

console.log('\n--- positionRealized: hand-verified against a fabricated position (Grok critique #4/Phase 2) ---');
{
  // Fabricated 10-day position, ascending order (fetchPoolFrom's native order), a price
  // move from 100 -> 150 (r=1.5), $50 total fees on $1M entry TVL.
  const fabricated = {
    id: '0xfab', feeTier: '3000', token0: { symbol: 'FOO' }, token1: { symbol: 'BAR' },
    poolDayData: Array.from({ length: 10 }, (_, i) => ({
      date: i * 86400, feesUSD: '5', volumeUSD: '80000', tvlUSD: '1000000', // date in seconds, one real day apart
      token0Price: String(100 + i * (50 / 9)), // linear 100 -> 150 over 10 days
    })),
  };
  const pos = positionRealized(fabricated, 2); // moderate range, w=2
  // Hand computation, independent of lib/concentrated.js's own code path:
  const r = 150 / 100, w = 2;
  const sa = Math.sqrt(1 / w), sb = Math.sqrt(w);
  const posVal = (r >= 1 / w && r <= w) ? 2 * Math.sqrt(r) - sa - r / sb : (r < 1 / w ? (1 / sa - 1 / sb) * r : sb - sa);
  const hodl = (1 - sa) + (1 - 1 / sb) * r;
  const handIl = (posVal / hodl - 1) * 100;
  const handFees = (50 / 1_000_000) * 100; // $50 fees / $1M entry TVL, as a %
  const handRealized = handFees + handIl;
  check('positionRealized is measurable', pos.measurable ? 1 : 0, 1, 0);
  check('positionRealized.impermanentLossPct matches independent hand calc', pos.impermanentLossPct, handIl, 1e-6);
  check('positionRealized.realizedReturnPct matches independent hand calc', pos.realizedReturnPct, handRealized, 1e-6);
  check('positionRealized.daysHeld', pos.daysHeld, 10, 0);
  check('positionRealized.entryDate is the FIRST day (ascending), not the last', pos.entryDate !== pos.latestDate ? 0 : 1, 0, 0);
}
{
  // Fewer than 2 days: must refuse, not fabricate a number from one data point.
  const tooShort = { id: '0x1', feeTier: '3000', token0: { symbol: 'A' }, token1: { symbol: 'B' },
    poolDayData: [{ date: 1, feesUSD: '5', tvlUSD: '1000000', token0Price: '100', volumeUSD: '1' }] };
  check('positionRealized refuses a 1-day window instead of dividing by nothing',
    positionRealized(tooShort, 2).measurable ? 1 : 0, 0, 0);
}
{
  // Price left the range entirely -> must flag outOfRange and say the loss is realized.
  const rangeExit = {
    id: '0x1', feeTier: '3000', token0: { symbol: 'A' }, token1: { symbol: 'B' },
    poolDayData: Array.from({ length: 5 }, (_, i) => ({
      date: i, feesUSD: '1', volumeUSD: '1000', tvlUSD: '1000000',
      token0Price: String(100 * Math.pow(3, i / 4)), // ends at 3x entry, range w=2 -> out
    })),
  };
  const pos = positionRealized(rangeExit, 2);
  check('positionRealized flags outOfRange when price left the band', pos.outOfRange ? 1 : 0, 1, 0);
  check('positionRealized carries an outOfRangeNote when out of range', pos.outOfRangeNote === null ? 1 : 0, 0, 0);
}

console.log('\n--- wallet: tick -> range classification ---');
// The bug this guards: an earlier version classified full-range ONLY by the literal +/-887272
// rail ticks, so positions spanning most of tick space without touching the rails came back as
// finite bands with widthX up to 1e26. Measured across 1000 live positions, above the span
// threshold the concentrated IL and full-range IL agree to 0.00pp -- they ARE full-range.
{
  const rails = tickRangeToWidth(TICK_MIN, TICK_MAX);
  check('rail-to-rail position is full-range', rails.fullRange ? 1 : 0, 1, 0);
  check('rail-to-rail position is flagged onRails', rails.onRails ? 1 : 0, 1, 0);
  check('full-range widthX is Infinity, not an overflowed finite number', Number.isFinite(rails.widthX) ? 1 : 0, 0, 0);

  // Spans most of tick space but never touches a rail: the case the old detector got wrong.
  const wide = tickRangeToWidth(-800000, 800000);
  check('near-rail wide position is ALSO full-range (not a 1e26 band)', wide.fullRange ? 1 : 0, 1, 0);
  check('near-rail wide position is NOT onRails', wide.onRails ? 1 : 0, 0, 0);

  // Ordinary managed bands must stay finite and exact.
  check('+/-2x band resolves to widthX 2', tickRangeToWidth(-6932, 6932).widthX, 2, 0.001);
  check('+/-1.25x band resolves to widthX 1.25', tickRangeToWidth(-2231, 2231).widthX, 1.25, 0.001);
  check('narrow band is not classified full-range', tickRangeToWidth(-6932, 6932).fullRange ? 1 : 0, 0, 0);
  check('tickToPrice(0) is 1', tickToPrice(0), 1, 1e-12);

  // A real position from the live corpus: huge span, but only 23% of tick space -> NOT full.
  const xor = tickRangeToWidth(-414400, 0);
  check('large-but-partial span stays a finite band', xor.fullRange ? 1 : 0, 0, 0);
  check('large-but-partial span reports spanFrac below the threshold',
    xor.spanFrac < EFFECTIVELY_FULL_RANGE_SPAN ? 1 : 0, 1, 0);

  // Garbage in must not produce a confident number.
  check('inverted tick range is rejected', tickRangeToWidth(100, 50) === null ? 1 : 0, 1, 0);
  check('non-numeric tick range is rejected', tickRangeToWidth('abc', 'def') === null ? 1 : 0, 1, 0);
}

console.log('\n--- wallet: uncollected fees must NEVER render as $0 ---');
// THE defect this project exists to expose, pointed at our own product. collectedFees* only
// populates on an explicit collect(). Measured live: of 150 positions with collectedFeesToken0
// == 0, SEVENTY-ONE had non-zero feeGrowthInside0LastX128 -- they earned fees and never
// collected. Reporting $0 for those would be a metric whose label lies about what it measures.
{
  const earnedNotCollected = describePosition({
    id: '1', owner: '0xabc', liquidity: '100',
    tickLower: { tickIdx: '-6932' }, tickUpper: { tickIdx: '6932' },
    collectedFeesToken0: '0', collectedFeesToken1: '0',
    feeGrowthInside0LastX128: '123456789', feeGrowthInside1LastX128: '0',
    depositedToken0: '10', depositedToken1: '0', withdrawnToken0: '0', withdrawnToken1: '0',
    pool: { id: '0xpool', feeTier: '3000', totalValueLockedUSD: '1000000' },
    token0: { symbol: 'A' }, token1: { symbol: 'B' },
  });
  check('earned-but-uncollected fees are NOT measurable', earnedNotCollected.fees.measurable ? 1 : 0, 0, 0);
  check('earned-but-uncollected fees are labelled as such',
    earnedNotCollected.fees.basis === 'earned-but-uncollected' ? 1 : 0, 1, 0);
  check('earned-but-uncollected fees carry NO zero-valued fee figure',
    earnedNotCollected.fees.collectedToken0 === undefined ? 1 : 0, 1, 0);
  check('earned-but-uncollected fees state a reason',
    typeof earnedNotCollected.fees.reason === 'string' && earnedNotCollected.fees.reason.length > 0 ? 1 : 0, 1, 0);

  const trulyCollected = describePosition({
    id: '2', owner: '0xabc', liquidity: '100',
    tickLower: { tickIdx: '-6932' }, tickUpper: { tickIdx: '6932' },
    collectedFeesToken0: '5.5', collectedFeesToken1: '2.25',
    feeGrowthInside0LastX128: '999', feeGrowthInside1LastX128: '999',
    depositedToken0: '10', depositedToken1: '5', withdrawnToken0: '0', withdrawnToken1: '0',
    pool: { id: '0xpool', feeTier: '3000', totalValueLockedUSD: '1000000' },
    token0: { symbol: 'A' }, token1: { symbol: 'B' },
  });
  check('actually-collected fees ARE measurable', trulyCollected.fees.measurable ? 1 : 0, 1, 0);
  check('actually-collected fees report the collected amount', trulyCollected.fees.collectedToken0, 5.5, 0.001);
  check('collected-fee basis is labelled "collected"', trulyCollected.fees.basis === 'collected' ? 1 : 0, 1, 0);

  // deposited*/withdrawn* are lifetime cumulative. They must never be presented as entry state.
  check('cumulative totals are namespaced away from entry value',
    trulyCollected.cumulative && typeof trulyCollected.cumulative.note === 'string' ? 1 : 0, 1, 0);
  check('position does not expose a top-level entry value',
    trulyCollected.entryValueUsd === undefined ? 1 : 0, 1, 0);
  check('position does not expose a computed pnl',
    trulyCollected.pnl === undefined && trulyCollected.pnlUsd === undefined ? 1 : 0, 1, 0);
}

console.log('\n--- wallet: address validation ---');
{
  const bad = await fetchWalletPositions('http://unused', 'not-an-address');
  check('malformed address is rejected before any network call', bad.ok ? 1 : 0, 0, 0);
  const bad2 = await fetchWalletPositions('http://unused', '0x123');
  check('short hex address is rejected', bad2.ok ? 1 : 0, 0, 0);
}

if (process.argv.includes('--live')) {
  console.log('\n--- LIVE: real pools from The Graph ---');
  const url = gatewayUrl(process.env.GRAPH_API_KEY);
  const pools = await fetchTopPools(url, { first: 120, days: 30 });
  const scored = pools.map(scorePool);
  const s = summarize(scored);
  console.log(`  fetched=${s.counts.fetched} measurable=${s.counts.measurable} liveVolatile=${s.counts.liveVolatile}`);
  console.log(`  canary: ${s.canary.stablePairsFound} stable pairs, worst |IL| = ${s.canary.worstAbsIlPct?.toFixed(4)}% -> ${s.canary.passed ? 'PASS' : 'FAIL'}`);
  console.log(`  misleading: ${s.misleadingCount}/${s.counts.liveVolatile} (${s.misleadingPct?.toFixed(0)}%)`);
  check('live canary passes', s.canary.passed ? 0 : 1, 0, 0);
  check('live sample produced measurable pools', s.counts.liveVolatile > 10 ? 0 : 1, 0, 0);

  console.log('\n--- LIVE: positionRealized against a real 45-day-old entry ---');
  const entryTs = Math.floor(Date.now() / 1000) - 45 * 86400;
  const livePool = await fetchPoolFrom(url, '0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640', entryTs);
  const livePos = positionRealized(livePool, 2);
  console.log(`  ${livePos.pair} entered ${livePos.entryDate}: fees ${livePos.feeReturnPct?.toFixed(3)}%  IL ${livePos.impermanentLossPct?.toFixed(3)}%  realized ${livePos.realizedReturnPct?.toFixed(3)}%`);
  check('live position is measurable', livePos.measurable ? 1 : 0, 1, 0);
  check('live position daysHeld is close to the requested window',
    Math.abs(livePos.daysHeld - 45) <= 1 ? 1 : 0, 1, 0);
}

console.log(`\n${failed ? `${failed} FAILED` : 'ALL PASS'}`);
process.exit(failed ? 1 : 0);
