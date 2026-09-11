// Recon only: which non-Uniswap concentrated-liquidity subgraphs actually answer,
// and do they carry the two fields the instrument needs (poolDayData + token0Price)?
import { readFileSync } from 'fs';

const KEY = process.env.GRAPH_API_KEY || readFileSync('/tmp/gk.txt', 'utf8').trim();

async function q(id, query) {
  try {
    const r = await fetch(`https://gateway.thegraph.com/api/${KEY}/subgraphs/id/${id}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    if (!r.ok) return { err: `HTTP ${r.status}` };
    const j = await r.json();
    if (j.errors) return { err: JSON.stringify(j.errors).slice(0, 90) };
    return j.data;
  } catch (e) {
    return { err: String(e.message).slice(0, 90) };
  }
}

const CANDIDATES = {
  'pancake-v3-bsc': 'A1fvJWQLBeUAggX2WQTMm3FKjXTekNXo77ZySun4YN2m',
  'pancake-v3-eth': 'CJYGNhb7RvnhfBBjTgQ8LzXAeSKzWNsSJ3QuwXsLrEeq',
  'aerodrome-slipstream': 'GENunSHWLBXm59mBSgPzQ8metBEp9YDfdqwFr91Av1UM',
  'sushi-v3-eth': '5nnoU1nUFeWqtXgbpC54L9PWdpgo7Y9HYinR3uTMsfzs',
  'quickswap-v3-poly': 'FqsRcH1XqSjqVx9GRTvEJe959aCbKrcyGgDWBrUkG24g',
  'camelot-v3-arb': '3utanEBA9nqMjPnuQP1vMCCys6enSM3EfhXTWUUFcRi6',
};

const GQL = `{pools(first:3,orderBy:volumeUSD,orderDirection:desc,where:{totalValueLockedUSD_gt:"250000"}){
  id token0{symbol} token1{symbol} totalValueLockedUSD
  poolDayData(first:2,orderBy:date,orderDirection:desc){date feesUSD tvlUSD token0Price}}}`;

for (const [name, id] of Object.entries(CANDIDATES)) {
  const d = await q(id, GQL);
  if (d.err) { console.log(`${name.padEnd(22)} DEAD  ${d.err}`); continue; }
  const p = d.pools || [];
  const day = p[0]?.poolDayData?.[0];
  const hasDay = (p[0]?.poolDayData || []).length > 0;
  const hasPrice = Number(day?.token0Price || 0) > 0;
  const hasFees = day?.feesUSD !== undefined;
  const hasTvl = day?.tvlUSD !== undefined;
  console.log(
    `${name.padEnd(22)} LIVE  ${String(p.length).padStart(2)} pools  `
    + `top=${(p[0]?.token0.symbol + '/' + p[0]?.token1.symbol).padEnd(14)} `
    + `dayData=${hasDay ? 'y' : 'N'} price=${hasPrice ? 'y' : 'N'} fees=${hasFees ? 'y' : 'N'} tvl=${hasTvl ? 'y' : 'N'}`,
  );
}
