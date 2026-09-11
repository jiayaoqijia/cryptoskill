#!/usr/bin/env node
/**
 * realized-lp-mcp — MCP server exposing LP ground truth from The Graph.
 *
 * Tools:
 *   realized_return(poolId, days)  -> what LPs actually earned vs what the UI advertises
 *   audit_pools(limit, gate)       -> corpus-wide audit + canary + sensitivity
 *   explain_gap(poolId)            -> plain-language verdict with the evidence chain
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import {
  gatewayUrl, fetchPool, fetchPoolFrom, fetchTopPools, scorePool, positionRealized, simulateExit, summarize, sensitivity, isLive, DEFAULT_LIVENESS,
} from '../lib/realized.js';
import { concentratedIlPct, outOfRange, RANGES } from '../lib/concentrated.js';
import { exitGasCost } from '../packages/core/src/oneinch.js';

const API_KEY = process.env.GRAPH_API_KEY;
const URL = () => gatewayUrl(API_KEY);

const TOOLS = [
  {
    name: 'find_pool',
    description:
      'START HERE when the user names tokens rather than an address. Resolves "WETH/USDC" or '
      + '"PEPE" to concrete poolIds ranked by TVL.\n\n'
      + 'WHEN TO USE: any request that mentions a pair or token but no 0x address.\n'
      + 'NEXT STEP: pass matches[0].poolId into position_realized (if the user gave an entry date) '
      + 'or realized_return (for a recent-window average).\n'
      + 'RETURNS: { query, source: "cache"|"live:uniswap-v3/mainnet", matches: [{pair, poolId, tvl, fee}] }.\n'
      + 'EMPTY RESULT: matches:[] means no match in the cached corpus or a live mainnet lookup -- tell '
      + 'the user the pair was not found; do NOT guess an address.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Token symbol or pair, case-insensitive, e.g. "WETH/USDC" or "PEPE"' },
        limit: { type: 'number', description: 'Max candidates to return (default 5)', default: 5 },
      },
      required: ['query'],
    },
  },
  {
    name: 'realized_return',
    description:
      'What the AVERAGE LP earned in a pool over a recent trailing window: fee income PLUS impermanent '
      + 'loss (IL is <= 0), from The Graph. Compare against the fees-only APR a DEX advertises, which is '
      + 'positive by construction and cannot report a loss.\n\n'
      + 'WHEN TO USE: "is this pool profitable", "is this APR real" -- a question about the POOL.\n'
      + 'WHEN NOT TO USE: the user has their own entry date -> use position_realized instead. That is a '
      + 'different question and this tool will answer it wrongly.\n'
      + 'RETURNS: { measurable, advertisedAprPct, feeReturnPct, impermanentLossPct, realizedReturnPct, realizedAprPct }.\n'
      + 'HONESTY CONTRACT: measurable:false means the window could not be priced. Report it as '
      + '"could not measure", NEVER as zero or "no loss". Always state the rangeWidthX you used -- the '
      + 'same pool can be honest full-range and misleading at +/-1.25x.',
    inputSchema: {
      type: 'object',
      properties: {
        poolId: { type: 'string', description: 'Uniswap v3 pool address (0x...)' },
        days: { type: 'number', description: 'Window length in days (default 30)', default: 30 },
        rangeWidthX: {
          type: 'number',
          description: 'Your concentrated-liquidity range as a half-width factor: 1.25 = a tight +/-25% band, '
            + '2 = a typical managed position, 4 = wide, omit for full-range. This MATTERS: v3 IL is amplified '
            + 'inside a band, and if price left your band the loss is realized, not impermanent. Full-range is '
            + 'the most generous case for the pool.',
        },
      },
      required: ['poolId'],
    },
  },
  {
    name: 'position_realized',
    description:
      'THE MAIN TOOL for a real user with a real position. "I entered THIS pool on THIS date at THIS '
      + 'range -- what have I actually made since?" Anchors to a calendar entry date, not a fixed lookback.\n\n'
      + 'WHEN TO USE: the user mentions when they entered, or says "my position" / "I put money in".\n'
      + 'GET THE RANGE RIGHT: if you have their wallet address, call the /api/wallet/{address} HTTP '
      + 'endpoint first and use the real range.widthX from their Position NFT. Assuming +/-2x when the '
      + 'actual band is different produces a confidently wrong number.\n'
      + 'RETURNS: { measurable, pair, entryDate, daysHeld, entryPrice, currentPrice, feeReturnPct, '
      + 'impermanentLossPct, realizedReturnPct, realizedAprPct, outOfRange, dailySeries[] }.\n'
      + 'HONESTY CONTRACT: fewer than 2 days since entry returns measurable:false -- there is nothing to '
      + 'measure yet and 0% is not the honest answer. If outOfRange is true the loss is REALIZED, not '
      + 'impermanent: say so, it changes the advice.\n'
      + 'DO NOT annualize realizedReturnPct yourself for short holds. A 30-day -81% loss annualizes to '
      + '-988%, which cannot happen -- an LP cannot lose more than the stake.',
    inputSchema: {
      type: 'object',
      properties: {
        poolId: { type: 'string', description: 'Uniswap v3 pool address (0x...)' },
        entryDate: { type: 'string', description: 'ISO date (YYYY-MM-DD) or unix timestamp (seconds) you entered the position' },
        rangeWidthX: {
          type: 'number',
          description: 'Your concentrated range as a half-width factor: 1.25 tight, 2 typical, 4 wide, '
            + '1e8 or omit for full-range. If price left this band the loss is realized, not impermanent.',
          default: 2,
        },
      },
      required: ['poolId', 'entryDate'],
    },
  },
  {
    name: 'simulate_exit',
    description:
      'DECISION SUPPORT for closing a position TODAY. Not a new claim -- reframes the exact same '
      + 'position_realized math around the question a holder actually has at the moment of deciding: '
      + '"if I closed this right now, what would I walk away with, in dollars, on a stake this size?"\n\n'
      + 'WHEN TO USE: the user is deciding whether to exit, not just checking historical performance.\n'
      + 'RETURNS: { measurable, stakeUsd, feesUsd, impermanentLossUsd, netUsd, netPct, outOfRange, '
      + 'gas:{unavailable,reason}, slippage:{unavailable,reason}, verdict }.\n'
      + 'GAS is real: live gas price from 1inch x estimated gas units for decreaseLiquidity + collect. '
      + 'The PRICE is measured, the UNITS are an estimate, so report the dollar figure as approximate.\n'
      + 'SLIPPAGE: closing a v3 position is NOT a swap -- decreaseLiquidity + collect returns BOTH tokens '
      + 'at the current tick, so price impact is a measured ZERO, not an unavailable field. Slippage only '
      + 'applies if the user then chooses to swap one side into the other; pass consolidate:true for that '
      + 'case and the estimate is explicitly a LOWER BOUND (modelled against total pool TVL, while a '
      + 'concentrated pool\'s depth at the active tick is thinner).\n'
      + 'netAfterCostsUsd is only populated when BOTH gas and slippage are known; it is null otherwise '
      + 'rather than a partial subtraction presented as a complete figure.\n'
      + 'If outOfRange is true, say plainly that the loss is locked in regardless of timing -- waiting '
      + 'does not un-realize it.',
    inputSchema: {
      type: 'object',
      properties: {
        poolId: { type: 'string', description: 'Uniswap v3 pool address (0x...)' },
        entryDate: { type: 'string', description: 'ISO date (YYYY-MM-DD) or unix timestamp (seconds) you entered the position' },
        rangeWidthX: { type: 'number', description: 'Your concentrated range as a half-width factor: 1.25 tight, 2 typical, 4 wide, 1e8 or omit for full-range.', default: 2 },
        stakeUsd: { type: 'number', description: 'Your position size in USD, for a dollar-denominated answer instead of only percentages.', default: 10000 },
        consolidate: { type: 'boolean', description: 'Set true ONLY if the user intends to swap one token into the other after closing. Closing alone is not a swap and costs zero slippage.', default: false },
      },
      required: ['poolId', 'entryDate'],
    },
  },
  {
    name: 'audit_pools',
    description:
      'Corpus-wide sweep: across many live pools, how many advertise a positive APR while LPs actually '
      + 'went backwards? Use for "how common is this" / "is this systemic" questions.\n\n'
      + 'RETURNS: { pools, misleadingPct, canary:{pass, worstAbsIlPct}, sensitivity:[3 liveness gates] }.\n'
      + 'CHECK THE CANARY BEFORE QUOTING ANY AGGREGATE. canary.pass=false means stable/stable pairs '
      + 'failed to show ~0 impermanent loss, the instrument is unproven, and every number in that '
      + 'response is untrusted. Say so rather than quoting it.\n'
      + 'The sensitivity table reports the headline at three cutoffs. If the answer flips across them it '
      + 'is a parameter, not a finding -- report it that way.',
    inputSchema: {
      type: 'object',
      properties: {
        limit: { type: 'number', description: 'How many pools to fetch (default 250)', default: 250 },
        days: { type: 'number', default: 30 },
      },
    },
  },
  {
    name: 'explain_gap',
    description:
      'Plain-language verdict for ONE pool plus the evidence chain that produced it. Use when the user '
      + 'wants the reasoning ("why is this pool misleading?"), not just the figure. Returns the verdict '
      + 'with advertised vs realized and the gap in percentage points, phrased for a human.',
    inputSchema: {
      type: 'object',
      properties: { poolId: { type: 'string' }, days: { type: 'number', default: 30 } },
      required: ['poolId'],
    },
  },
  {
    name: 'rank_pools',
    description:
      'Rank live pools by what LPs ACTUALLY took home (fees + impermanent loss) instead of by advertised '
      + 'APR. This is what a yield dashboard or an allocating agent should call INSTEAD of sorting by APR.\n\n'
      + 'THIS IS A TRACK RECORD, NOT A FORECAST. It reports what already happened over the measured '
      + 'window. Do NOT present it to a user as a prediction of which pools will pay next. We tested '
      + 'predictive selection directly: an apparent +1.64pp edge on one split failed a pre-registered bar '
      + 'across 112 walk-forward windows, five times, and a noise decoy scored comparably. It was deleted '
      + 'rather than shipped.\n'
      + 'trustLabel values: "historically honest" (advertised tracked realized within 2pts), "gap-prone" '
      + '(real gap, sign intact), "routinely misleading" (advertised positive while LPs lost money), '
      + '"unmeasurable" (never a fabricated zero).\n'
      + 'GOOD USE: screening OUT pools whose advertised number has been unreliable. That is avoidance, '
      + 'which the data supports. Claiming the top row will pay best next month is not.',
    inputSchema: {
      type: 'object',
      properties: {
        limit: { type: 'number', description: 'How many pools to consider (default 250)', default: 250 },
        top: { type: 'number', description: 'How many ranked results to return (default 10)', default: 10 },
        days: { type: 'number', description: 'Window length in days', default: 30 },
        rangeWidthX: { type: 'number', description: 'Position range width; 2 = a typical managed +/-2x band', default: 2 },
        excludeMisleading: {
          type: 'boolean',
          description: 'Drop pools whose advertised APR is currently positive while realized is negative',
          default: false,
        },
      },
    },
  },
];

const GATES = [
  { label: 'loose  (>=20d, $10k 7d vol, $100k TVL)', gate: { minActiveDays: 20, minRecent7dVolumeUsd: 10_000, minTvlUsd: 100_000 } },
  { label: 'mid    (>=25d, $50k 7d vol, $250k TVL)', gate: DEFAULT_LIVENESS },
  { label: 'strict (>=28d, $250k 7d vol, $1M TVL)', gate: { minActiveDays: 28, minRecent7dVolumeUsd: 250_000, minTvlUsd: 1_000_000 } },
];

const ok = (obj) => {
  // An error is not a successful tool call. MCP clients branch on isError; without it
  // a failure renders as a green result whose text happens to say "error", and the model
  // on the other end has no way to tell the difference.
  const payload = { content: [{ type: 'text', text: JSON.stringify(obj, null, 2) }] };
  if (obj && typeof obj === 'object' && obj.error) payload.isError = true;
  return payload;
};

// Never hand a raw exception string to a caller: fetch() failures can carry the
// request URL, and our gateway URL embeds the Graph API key.
const safeError = (e) => {
  const raw = String((e && e.message) || e);
  const key = process.env.GRAPH_API_KEY;
  const scrubbed = key ? raw.split(key).join('<redacted>') : raw;
  return scrubbed.replace(/gateway\.thegraph\.com\/api\/[^/\s]+/g, 'gateway.thegraph.com/api/<redacted>');
};

async function findPool({ query: q, limit = 5 }) {
  if (!q || !q.trim()) return { error: 'query is required, e.g. "WETH/USDC" or "PEPE"' };
  const terms = q.toUpperCase().split(/[/\s-]+/).filter(Boolean);
  // Reuse the same top-pools fetch the audit uses -- one code path, no second query shape
  // to drift out of sync with what audit_pools/the app actually see.
  const pools = await fetchTopPools(URL(), { first: 500, minTvlUsd: 10_000 });
  const matches = pools
    .map((p) => ({ p, sym0: (p.token0?.symbol || '').toUpperCase(), sym1: (p.token1?.symbol || '').toUpperCase() }))
    .filter(({ sym0, sym1 }) => terms.every((t) => sym0.includes(t) || sym1.includes(t)))
    .sort((a, b) => Number(b.p.totalValueLockedUSD) - Number(a.p.totalValueLockedUSD))
    .slice(0, limit)
    .map(({ p, sym0, sym1 }) => ({
      poolId: p.id,
      pair: `${sym0}/${sym1}`,
      feeTierPct: Number(p.feeTier) / 10_000,
      tvlUsd: Math.round(Number(p.totalValueLockedUSD)),
    }));
  if (!matches.length) {
    return { query: q, matches: [], note: 'no pool found among the top 500 mainnet pools by TVL for that query' };
  }
  return {
    query: q,
    matches,
    note: 'pass any matches[].poolId into realized_return or explain_gap',
  };
}

async function realizedReturn({ poolId, days = 30, rangeWidthX }) {
  const pool = await fetchPool(URL(), poolId, days);
  if (!pool) return { error: `pool ${poolId} not found in the Uniswap v3 subgraph` };
  const scored = scorePool(pool);
  if (!scored.measurable || !(rangeWidthX > 1)) return scored;
  const il = concentratedIlPct(scored.priceRatio, rangeWidthX);
  const realizedPct = scored.feeReturnPct + il;
  const realizedApr = (realizedPct / scored.windowDays) * 365;
  const left = outOfRange(scored.priceRatio, rangeWidthX);
  return {
    ...scored,
    yourRange: {
      rangeWidthX,
      impermanentLossPct: il,
      realizedReturnPct: realizedPct,
      realizedAprPct: realizedApr,
      outOfRange: left,
      note: left
        ? 'Price LEFT your band during this window. You are fully converted into the losing asset — this loss is realized, not impermanent.'
        : 'Price stayed inside your band for the whole window.',
    },
  };
}

async function positionRealizedTool({ poolId, entryDate, rangeWidthX = 2 }) {
  if (!poolId) return { error: 'poolId is required' };
  if (!entryDate) return { error: 'entryDate is required, e.g. "2026-08-01" or a unix timestamp' };
  let ts;
  if (/^\d+$/.test(String(entryDate))) {
    ts = Number(entryDate);
  } else {
    const d = new Date(entryDate);
    if (Number.isNaN(d.getTime())) return { error: `could not parse entryDate "${entryDate}" as an ISO date or unix timestamp` };
    ts = Math.floor(d.getTime() / 1000);
  }
  const pool = await fetchPoolFrom(URL(), poolId, ts);
  if (!pool) return { error: `pool ${poolId} not found in the Uniswap v3 subgraph` };
  const pos = positionRealized(pool, rangeWidthX);
  if (!pos.measurable) return pos;
  return {
    ...pos,
    verdict: pos.outOfRange
      ? `Price left your +/-${rangeWidthX}x range: realized ${pos.realizedAprPct.toFixed(1)}% annualized, and this loss is LOCKED IN, not impermanent.`
      : `In-range the whole time: realized ${pos.realizedAprPct.toFixed(1)}% annualized (fees ${pos.feeReturnPct.toFixed(2)}% + IL ${pos.impermanentLossPct.toFixed(2)}%).`,
  };
}

async function simulateExitTool({ poolId, entryDate, rangeWidthX = 2, stakeUsd = 10_000, consolidate = false }) {
  if (!poolId) return { error: 'poolId is required' };
  if (!entryDate) return { error: 'entryDate is required, e.g. "2026-08-01" or a unix timestamp' };
  let ts;
  if (/^\d+$/.test(String(entryDate))) {
    ts = Number(entryDate);
  } else {
    const d = new Date(entryDate);
    if (Number.isNaN(d.getTime())) return { error: `could not parse entryDate "${entryDate}" as an ISO date or unix timestamp` };
    ts = Math.floor(d.getTime() / 1000);
  }
  const stake = Number(stakeUsd);
  if (!(stake > 0)) return { error: 'stakeUsd must be a positive number' };
  const pool = await fetchPoolFrom(URL(), poolId, ts);
  if (!pool) return { error: `pool ${poolId} not found in the Uniswap v3 subgraph` };
  const gas = await exitGasCost({ chain: 'mainnet' });
  return simulateExit(pool, rangeWidthX, stake, { gas, consolidate });
}

async function auditPools({ limit = 250, days = 30 }) {
  const pools = await fetchTopPools(URL(), { first: limit, days });
  const scored = pools.map(scorePool);
  const s = summarize(scored);
  return {
    ...s,
    sensitivity: sensitivity(scored, GATES),
    interpretation: s.canary.passed
      ? `${s.misleadingCount}/${s.counts.liveVolatile} live pools advertise a positive APR while realized return (fees - IL) was negative.`
      : 'CANARY FAILED OR UNPROVEN — do not quote these numbers.',
  };
}

async function explainGap({ poolId, days = 30 }) {
  const r = await realizedReturn({ poolId, days });
  if (r.error || r.measurable === false) return r;
  const verdict = r.misleading
    ? `MISLEADING: advertises ${r.advertisedAprPct.toFixed(1)}% APR, LPs actually realized ${r.realizedAprPct.toFixed(1)}% annualized.`
    : `Consistent: advertised ${r.advertisedAprPct.toFixed(1)}% APR vs realized ${r.realizedAprPct.toFixed(1)}% annualized.`;
  return {
    ...r,
    verdict,
    evidence: [
      `window: ${r.windowDays} days of poolDayData from The Graph`,
      `fees earned: $${Math.round(r.totalFeesUsd).toLocaleString()} on $${Math.round(r.entryTvlUsd).toLocaleString()} entry TVL = ${r.feeReturnPct.toFixed(2)}%`,
      `price ratio ${r.priceRatio.toFixed(4)} -> impermanent loss ${r.impermanentLossPct.toFixed(2)}% (full-range)`,
      `realized = ${r.feeReturnPct.toFixed(2)}% + (${r.impermanentLossPct.toFixed(2)}%) = ${r.realizedReturnPct.toFixed(2)}%`,
      'advertised APR is fees-only and annualized: it has no price term and cannot be negative.',
      r.byRange
        ? `concentrated: tight(+/-1.25x) ${r.byRange.tight?.realizedReturnPct?.toFixed(2)}%${r.byRange.tight?.outOfRange ? ' OUT OF RANGE' : ''}, `
          + `moderate(+/-2x) ${r.byRange.moderate?.realizedReturnPct?.toFixed(2)}%${r.byRange.moderate?.outOfRange ? ' OUT OF RANGE' : ''} `
          + '— full-range is the generous case; real v3 LPs concentrate and eat amplified IL.'
        : '',
    ],
  };
}

// Say what the sample ACTUALLY shows, including when it shows nothing. An earlier version of
// this always printed "sorting by APR puts X first, sorting by realized puts Y first" -- which
// on a sample where X === Y rendered as a punchline with no joke: a null result wearing the
// costume of evidence. If the naive ranking and the honest one agree at the top, say so, and
// carry the disagreement that does exist (the worst gap) instead of manufacturing one.
function soWhatLine(naiveTop, realTop, ranked) {
  if (!naiveTop || !realTop) return 'No measurable live pools in this sample.';
  const worst = [...ranked].sort((a, b) => b.gapPts - a.gapPts)[0];
  const liars = ranked.filter((r) => r.misleading).length;
  if (naiveTop.pair !== realTop.pair) {
    return `Sorting by advertised APR puts ${naiveTop.pair} first (${naiveTop.advertisedAprPct}% advertised, `
      + `but ${naiveTop.realizedAprPct}% realized). Sorting by what LPs actually took home puts `
      + `${realTop.pair} first (${realTop.realizedAprPct}% realized). Rank on realized, screen on trustLabel.`;
  }
  return `Both rankings agree at the top here (${realTop.pair}, ${realTop.realizedAprPct}% realized) — `
    + `advertised APR is not wrong about every pool, and this tool does not pretend otherwise. `
    + `The damage is below the top: ${liars} of ${ranked.length} live pools advertise a positive APR `
    + `while LPs went backwards`
    + (worst ? `, worst gap ${worst.pair} at ${worst.gapPts}pts (${worst.advertisedAprPct}% advertised vs ${worst.realizedAprPct}% realized)` : '')
    + '. Rank on realized, screen on trustLabel.';
}

// The correction, not just the diagnosis. Every other tool here tells you a number is wrong;
// this one tells you what to use instead. A dashboard or allocating agent calls this in place
// of "sort pools by APR descending", which is the exact behaviour that loses people money.
async function rankPools({ limit = 250, top = 10, days = 30, rangeWidthX = 2, excludeMisleading = false }) {
  const pools = await fetchTopPools(URL(), { first: limit, days });
  const scored = pools.map(scorePool);
  const s = summarize(scored);
  // Same discipline as the site: if stable/stable pairs don't show ~0 IL the instrument is
  // broken, and a ranking built on a broken instrument is worse than no ranking at all.
  if (!s.canary.passed) {
    return { error: 'CANARY FAILED — the IL instrument is not trustworthy right now, so no ranking is returned.', canary: s.canary };
  }

  const ranked = [];
  for (const p of scored) {
    if (!p.measurable || !isLive(p)) continue;
    const il = concentratedIlPct(p.priceRatio, rangeWidthX);
    if (il === null) continue;
    const realizedPct = p.feeReturnPct + il;
    const realizedAprPct = (realizedPct / p.windowDays) * 365;
    const gapPts = p.advertisedAprPct - realizedAprPct;
    const misleading = p.advertisedAprPct > 0 && realizedAprPct < 0;
    // Thresholds stated, not hidden. "unmeasurable" is never silently a zero.
    const trustLabel = misleading ? 'routinely misleading'
      : Math.abs(gapPts) <= 2 ? 'historically honest'
        : 'gap-prone';
    if (excludeMisleading && misleading) continue;
    ranked.push({
      poolId: p.pool,
      pair: p.pair,
      tvlUsd: Math.round(p.currentTvlUsd),
      advertisedAprPct: Number(p.advertisedAprPct.toFixed(2)),
      realizedAprPct: Number(realizedAprPct.toFixed(2)),
      gapPts: Number(gapPts.toFixed(2)),
      impermanentLossPct: Number(il.toFixed(2)),
      outOfRange: outOfRange(p.priceRatio, rangeWidthX),
      misleading,
      trustLabel,
    });
  }

  ranked.sort((a, b) => b.realizedAprPct - a.realizedAprPct);
  const byApr = [...ranked].sort((a, b) => b.advertisedAprPct - a.advertisedAprPct);
  // The whole argument in one comparison: what you'd have picked vs what actually paid.
  const naiveTop = byApr[0];
  const realTop = ranked[0];

  return {
    rangeWidthX,
    windowDays: days,
    considered: ranked.length,
    canary: s.canary,
    ranking: ranked.slice(0, top),
    worstOffenders: [...ranked].sort((a, b) => b.gapPts - a.gapPts).slice(0, Math.min(5, top)),
    counts: {
      historicallyHonest: ranked.filter((r) => r.trustLabel === 'historically honest').length,
      gapProne: ranked.filter((r) => r.trustLabel === 'gap-prone').length,
      routinelyMisleading: ranked.filter((r) => r.trustLabel === 'routinely misleading').length,
    },
    soWhat: soWhatLine(naiveTop, realTop, ranked),
    note: 'Fee uplift for concentrated ranges is not modelled, so tight-range realized figures are LOWER BOUNDS. '
      + 'Ordering is robust; treat magnitudes as bounded.',
  };
}

const server = new Server({ name: 'realized-lp-mcp', version: '0.1.0' }, { capabilities: { tools: {} } });
server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));
server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args = {} } = req.params;
  try {
    if (name === 'find_pool') return ok(await findPool(args));
    if (name === 'realized_return') return ok(await realizedReturn(args));
    if (name === 'position_realized') return ok(await positionRealizedTool(args));
    if (name === 'simulate_exit') return ok(await simulateExitTool(args));
    if (name === 'audit_pools') return ok(await auditPools(args));
    if (name === 'explain_gap') return ok(await explainGap(args));
    if (name === 'rank_pools') return ok(await rankPools(args));
    return ok({ error: `unknown tool ${name}` });
  } catch (e) {
    return ok({ error: safeError(e) });
  }
});

await server.connect(new StdioServerTransport());
