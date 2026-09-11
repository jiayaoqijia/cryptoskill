// Does trustLabel PERSIST as a CLASSIFICATION? Uses the REAL labeller from build-pools.js:
//   misleading (adv>0 && realized<0) -> 'routinely misleading'
//   |adv - realizedApr| <= 2         -> 'historically honest'
//   else                             -> 'gap-prone'
// All on ANNUALIZED values, which is what the real one compares. My first attempt compared
// window percentages and returned null for everything -- a broken instrument, not a finding.
import { gatewayUrl, fetchTopPools, impermanentLossPct } from '/home/ubuntu/.openclaw/workspace/projects/ethonline2026-graph-agent/lib/realized.js';
import { venueList, subgraphId } from '/home/ubuntu/.openclaw/workspace/projects/ethonline2026-graph-agent/lib/venues.js';
import { readFileSync as _rf } from "fs";
const KEY = JSON.parse(_rf("/home/ubuntu/.config/cadence-secure/thegraph.json","utf8")).api_key;
const SPAN = 21, HISTORY = 210, STEP = 21;

function label(days) {
  if (days.length < 2) return null;
  const feesPct = days.reduce((s, d) => s + d.feeYield * 100, 0);
  const p0 = days[0].price, pN = days[days.length-1].price;
  if (!(p0>0)||!(pN>0)||!Number.isFinite(feesPct)) return null;
  const realizedPct = feesPct + impermanentLossPct(pN/p0);
  const adv = (feesPct / days.length) * 365;              // annualized, fees-only
  const realizedApr = (realizedPct / days.length) * 365;  // annualized, fees+IL
  if (!Number.isFinite(adv)||!Number.isFinite(realizedApr)) return null;
  if (adv > 0 && realizedApr < 0) return 'routinely misleading';
  if (Math.abs(adv - realizedApr) <= 2) return 'historically honest';
  return 'gap-prone';
}

const rows = [];
for (const v of venueList()) {
  const sid = subgraphId(v.dex, v.chain); if (!sid) continue;
  let pools; try { pools = await fetchTopPools(gatewayUrl(KEY, sid), { first: 150, days: HISTORY }); } catch { continue; }
  for (const p of pools||[]) {
    const d = [...(p.poolDayData||[])].reverse().map(x=>({feeYield:Number(x.feesUSD)/Math.max(Number(x.tvlUSD),1), price:Number(x.token0Price)}));
    const seq = [];
    for (let s=0; s+SPAN<=HISTORY && s+SPAN<=d.length; s+=STEP) seq.push(label(d.slice(s,s+SPAN)));
    if (seq.filter(Boolean).length >= 3) rows.push({ id:p.id, seq:seq.filter(Boolean) });
  }
}

let tot=0, stay=0; const byLabel={};
for (const r of rows) for (let i=0;i+1<r.seq.length;i++) {
  const a=r.seq[i], b=r.seq[i+1];
  tot++; if(a===b) stay++;
  (byLabel[a] ||= {n:0,same:0}); byLabel[a].n++; if(a===b) byLabel[a].same++;
}
const flat = rows.flatMap(r=>r.seq);
const dist = flat.reduce((m,l)=>{m[l]=(m[l]||0)+1;return m;},{});
const base = Math.max(...Object.values(dist))/flat.length;

console.log('pools with >=3 labelled windows:', rows.length, '| transitions:', tot);
console.log('LABEL DISTRIBUTION:', JSON.stringify(dist));
console.log('base rate (always guess majority):', (base*100).toFixed(1)+'%');
console.log('');
console.log('PERSISTENCE P(label stays same):', ((stay/tot)*100).toFixed(1)+'%');
for (const [l,v] of Object.entries(byLabel)) console.log('  from '+l.padEnd(22)+': '+((v.same/v.n)*100).toFixed(1)+'% stay (n='+v.n+')');
console.log('');
console.log('LIFT over base rate:', ((stay/tot)/base).toFixed(3)+'x');

// DECOY: shuffle each pool's sequence. Destroys time order, keeps distribution.
let ds=0, dt=0, seed=42; const rnd=()=>{seed=(seed*1103515245+12345)&0x7fffffff;return seed/0x7fffffff;};
for (const r of rows) {
  const s=[...r.seq]; for(let i=s.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[s[i],s[j]]=[s[j],s[i]];}
  for(let i=0;i+1<s.length;i++){dt++; if(s[i]===s[i+1]) ds++;}
}
console.log('DECOY (shuffled order):', ((ds/dt)*100).toFixed(1)+'%  -> real must beat this');
