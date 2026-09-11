#!/usr/bin/env node
/**
 * demo-refresh.js — print the exact numbers that are on screen RIGHT NOW.
 *
 * Every figure in DEMO-SCRIPT.md drifts: the corpus rebuilds, the 30-day window slides, and
 * a pool that was the worst offender on Tuesday is mid-table by Friday. Reading a stale
 * number off a script while a live page shows a different one is the single most avoidable
 * way to lose credibility on camera -- and a judge WILL pause the video on the hero.
 *
 * So: run this immediately before recording, and narrate what it prints. Nothing here is
 * computed by this script; it reads the same live endpoints the page and the MCP server use,
 * so if this disagrees with the page, the page is mid-rebuild and you should wait.
 *
 * Usage:  node scripts/demo-refresh.js
 */
const BASE = process.env.REALIZED_BASE || 'https://realized.drainfun.xyz';
const DEMO_POOL = '0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640'; // USDC/WETH 0.05% mainnet
const DEMO_ENTRY = '2026-07-28';

const pct = (n, d = 2) => (n === null || n === undefined ? 'n/a' : `${n >= 0 ? '+' : ''}${Number(n).toFixed(d)}%`);
const usd = (n) => `$${Math.round(Math.abs(n)).toLocaleString('en-US')}`;

async function getJson(path) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`${path} -> HTTP ${res.status}`);
  return res.json();
}

const line = (k, v) => console.log(`  ${k.padEnd(26)} ${v}`);

async function main() {
  console.log(`\nREALIZED — live demo numbers  (${new Date().toISOString().replace('T', ' ').slice(0, 16)} UTC)`);
  console.log(`source: ${BASE}\n`);

  // ---- 1. the hero / shock card ----------------------------------------------------------
  // Recomputed with the SAME selection rule build-app.js uses: highest-TVL pool that is
  // currently misleading. If that rule picks a different pool than the page shows, the page
  // is stale -- rebuild it before recording rather than narrating a number nobody can see.
  const pools = await getJson('/api/pools');
  const cands = pools.pools
    .filter((p) => p.misleading === true && p.realizedAprPct !== null && p.trustLabel !== 'unmeasurable')
    .sort((a, b) => b.tvl - a.tvl);
  const s = cands[0];

  console.log('[0:00] SHOCK CARD (the hero — read these exactly)');
  if (!s) {
    console.log('  !! No misleading pool in the corpus right now.');
    console.log('  !! The hero has degraded to the honest headline. Re-check the page before recording.\n');
  } else {
    const stake = 100_000;
    const winReal = (s.realizedAprPct / 365) * s.days;
    const winAdv = (s.adv / 365) * s.days;
    const ilPct = winReal - s.fees;
    line('pool', `${s.pair} ${s.fee}% (${s.dex}/${s.chain})`);
    line('TVL', usd(s.tvl));
    line('advertised APR', pct(s.adv));
    line('LOST per $100k', usd(stake * (winReal / 100)));
    line('DEX implied', usd(stake * (1 + winAdv / 100)));
    line('actually have', usd(stake * (1 + winReal / 100)));
    line('fees earned', `+${usd(stake * (s.fees / 100))}  (${pct(s.fees)})`);
    line('impermanent loss', `-${usd(stake * (ilPct / 100))}  (${pct(ilPct)})`);
    line('net over window', `${pct(winReal)} over ${s.days} days  (${pct(s.realizedAprPct, 1)} annualised)`);
  }

  const misleadingPct = (pools.pools.filter((p) => p.misleading === true).length
    / pools.pools.filter((p) => p.misleading !== null).length) * 100;
  line('corpus misleading', `${misleadingPct.toFixed(0)}% of measurable live pools`);
  line('venues', [...new Set(pools.pools.map((p) => `${p.dex}/${p.chain}`))].join(', '));

  // ---- 2. the personal position beat ------------------------------------------------------
  console.log('\n[0:55] YOUR POSITION (typed live on camera)');
  try {
    const p = await getJson(`/api/position/${DEMO_POOL}?entry=${DEMO_ENTRY}&range=2`);
    if (p.error || p.measurable === false) {
      console.log(`  !! ${p.error || p.reason} — pick a different entry date before recording.`);
    } else {
      line('search for', 'WETH/USDC');
      line('entry date', `${p.entryDate}  (${p.daysHeld} days held)`);
      line('fees', pct(p.feeReturnPct));
      line('impermanent loss', pct(p.impermanentLossPct));
      line('realized annualised', pct(p.realizedAprPct, 1));
      line('in range?', p.outOfRange ? 'NO — price left the band (loss is locked in)' : 'yes, whole window');
      console.log(`  say: "${p.verdict}"`);
    }
  } catch (e) {
    console.log(`  !! position endpoint failed: ${e.message}`);
  }

  // ---- 3. the closer ----------------------------------------------------------------------
  // Uses the HTTP audit rather than booting the MCP server: same numbers, ~1s instead of ~90s.
  // The MCP call is what you RUN on camera; this is so you know what it will say first.
  // The closer numbers MUST come from the same gated path rank_pools uses, or the count you
  // narrate won't match the MCP output a judge might run. pools.json has no liveness fields
  // (activeDays, 7d volume), so re-deriving the gate here is impossible -- an earlier version
  // tried and silently counted all 256 dead-and-alive pools, surfacing a +1,494,982% pool as
  // "top realized". We call /api/audit, which applies isLive() server-side, then rank the
  // rank_pools tool directly for the ordered list.
  console.log('\n[1:15] RANK_POOLS CLOSER (gated, matches the MCP tool)');
  try {
    const audit = await getJson('/api/audit?limit=150');
    const c = audit.counts || {};
    line('live volatile pools', `${c.liveVolatile} of ${c.measurable} measurable (${c.fetched} fetched)`);
    line('canary', audit.canary?.passed ? 'passed (stable pairs ~0 IL)' : 'FAILED — do not quote numbers');
    if (audit.interpretation) console.log(`  say: "${audit.interpretation}"`);
    console.log('  For the ordered ranking + soWhat line, run the MCP call in DEMO-SCRIPT.md');
    console.log('  (rank_pools, ~60-90s). It gates identically; these counts will agree.');
  } catch (e) {
    console.log(`  !! ${e.message}`);
  }

  console.log('\nRe-read DEMO-SCRIPT.md with these numbers in hand. Nothing above is cached.\n');
}

main().catch((e) => {
  console.error(`\ndemo-refresh failed: ${e.message}`);
  console.error('Is the site up? Try: curl -sI https://realized.drainfun.xyz\n');
  process.exit(1);
});
