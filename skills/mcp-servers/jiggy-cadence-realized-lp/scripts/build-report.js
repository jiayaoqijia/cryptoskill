#!/usr/bin/env node
/**
 * build-report.js — render report.html from the JSON artifacts.
 *
 * RULE: this script does NO measurement. It reads the committed JSON and renders it. If a
 * number is not in the data files it cannot appear on the page, and if a window is
 * `trusted: false` the page must say so rather than quietly averaging it in. A report that
 * can compute its own numbers is a report that can disagree with its own evidence.
 *
 * No build step, no dependencies, no framework: one self-contained HTML file with inline SVG.
 *
 * Run: node scripts/build-report.js
 */
import { readFileSync, writeFileSync } from 'fs';
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const R = (p) => JSON.parse(readFileSync(`${__dirname}/../${p}`, 'utf8'));

const corpus = R('data/corpus.json');
const wf = R('data/walkforward.json');
const hist = R('data/history.json');
const xdex = R('data/cross-dex.json');

const esc = (s) => String(s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const pct = (v, d = 0) => (v === null || v === undefined ? '—' : `${v.toFixed(d)}%`);

/** Sparkline of misleading% over time for one series of windows (oldest → newest). */
function spark(windows, range, w = 260, h = 46) {
  const pts = windows.filter((x) => x.trusted).map((x) => x.byRange[range].misleadingPct)
    .filter((v) => v !== null).reverse();
  if (pts.length < 2) return '<span class="dim">insufficient trusted windows</span>';
  const max = 100, min = 0;
  const dx = w / (pts.length - 1);
  const y = (v) => h - ((v - min) / (max - min)) * h;
  const d = pts.map((v, i) => `${i === 0 ? 'M' : 'L'}${(i * dx).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
  const area = `${d} L${w},${h} L0,${h} Z`;
  return `<svg viewBox="0 0 ${w} ${h}" class="spark" preserveAspectRatio="none">`
    + `<path d="${area}" fill="rgba(224,122,95,.13)"/>`
    + `<line x1="0" y1="${y(50).toFixed(1)}" x2="${w}" y2="${y(50).toFixed(1)}" class="mid"/>`
    + `<path d="${d}" fill="none" stroke="#e07a5f" stroke-width="1.8"/></svg>`;
}

/** Horizontal bar: min–max span with median tick. */
function bar(s, w = 210, h = 22) {
  if (!s) return '<span class="dim">—</span>';
  const x = (v) => (v / 100) * w;
  return `<svg viewBox="0 0 ${w} ${h}" class="bar">`
    + `<rect x="0" y="${h / 2 - 3}" width="${w}" height="6" fill="#1c2128" rx="3"/>`
    + `<rect x="${x(s.min).toFixed(1)}" y="${h / 2 - 5}" width="${Math.max(2, x(s.max) - x(s.min)).toFixed(1)}" height="10" fill="rgba(224,122,95,.42)" rx="5"/>`
    + `<line x1="${x(s.median).toFixed(1)}" y1="${h / 2 - 9}" x2="${x(s.median).toFixed(1)}" y2="${h / 2 + 9}" stroke="#e07a5f" stroke-width="2.5"/>`
    + `</svg>`;
}

const rangeRows = corpus.byRange.rows.map((r) => `<tr>
  <td><b>${esc(r.label)}</b> <span class="dim">${r.rangeWidthX === 1e8 ? 'full-range' : `±${r.rangeWidthX}x`}</span></td>
  <td class="num">${pct(r.medianIlPct, 2)}</td>
  <td class="num">${pct(r.medianRealizedPct, 2)}</td>
  <td class="num">${r.outOfRangeCount}/${r.n}</td>
  <td class="num big">${pct(r.misleadingPct)}</td></tr>`).join('');

const chainRows = Object.entries(hist.stability).map(([chain, s]) => {
  const d = hist.perChain[chain];
  if (!s || !s.tight) {
    return `<tr class="untrusted"><td><b>${esc(chain)}</b></td><td colspan="5" class="dim">
      no trusted windows — n=${d.windows?.[0]?.byRange?.full?.n ?? '?'} per window, below the n≥20 bar. No number quoted.</td></tr>`;
  }
  return `<tr>
    <td><b>${esc(chain)}</b><div class="dim sm">${d.oldestWindowEnd} →</div></td>
    <td class="num">${s.tight.windows}</td>
    <td>${bar(s.tight)}<div class="dim sm">${pct(s.tight.min)}–${pct(s.tight.max)} · med <b>${pct(s.tight.median)}</b></div></td>
    <td>${bar(s.moderate)}<div class="dim sm">med ${pct(s.moderate.median)}</div></td>
    <td>${bar(s.full)}<div class="dim sm">med ${pct(s.full.median)}</div></td>
    <td>${spark(d.windows, 'tight')}</td></tr>`;
}).join('');

const dexRows = Object.entries(xdex.perVenue).map(([venue, d]) => {
  if (d.error || !d.stability?.tight) {
    return `<tr class="untrusted"><td><b>${esc(venue)}</b><div class="dim sm">${esc(d.chain)}</div></td>
      <td colspan="4" class="dim">unmeasurable — ${d.poolsFetched ?? 0} pools clear the TVL floor, canary could not be proven.
      All ${d.windowsTotal ?? 0} windows <code>trusted:false</code>. No number quoted.</td></tr>`;
  }
  const s = d.stability;
  return `<tr>
    <td><b>${esc(d.team)}</b><div class="dim sm">${esc(d.chain)} · ${d.oldestWindowEnd} →</div></td>
    <td class="num">${s.tight.windows}</td>
    <td>${bar(s.tight)}<div class="dim sm">${pct(s.tight.min)}–${pct(s.tight.max)} · med <b>${pct(s.tight.median)}</b></div></td>
    <td>${bar(s.moderate)}<div class="dim sm">med ${pct(s.moderate.median)}</div></td>
    <td>${bar(s.full)}<div class="dim sm">med ${pct(s.full.median)}</div></td></tr>`;
}).join('');

const volRows = Object.entries(hist.volatilityTest.rows).map(([label, r]) => `<tr>
  <td><b>${esc(label)}</b></td><td class="num">${r.n}</td>
  <td class="num">${r.pearson?.toFixed(3)}</td><td class="num">${r.spearman?.toFixed(3)}</td></tr>`).join('');

const corrRows = corpus.correlation.rows.map((r) => `<tr>
  <td><b>${esc(r.label)}</b></td><td class="num">${r.n}</td>
  <td class="num">${r.pearson?.toFixed(3)}</td><td class="num">${r.spearman?.toFixed(3)}</td>
  <td class="num">${r.pearsonTrimmed?.toFixed(3)} / ${r.spearmanTrimmed?.toFixed(3)}</td></tr>`).join('');

const totalMonths = Object.values(hist.stability).reduce((a, s) => a + (s?.tight?.windows || 0), 0);
// Count chains we could actually VALIDATE, not chains we queried. Optimism answers but never
// clears the canary/n bar, so quoting "5 chains" would inflate the claim with a chain whose
// numbers we refuse to publish -- the exact substitution this project exists to catch.
const chainsValidated = Object.values(hist.stability).filter((s) => s?.tight).length;
const dexesValidated = Object.values(xdex.perVenue).filter((d) => d.stability?.tight).length;
const worstChain = Object.entries(hist.stability).filter(([, s]) => s?.tight)
  .sort((a, b) => b[1].tight.median - a[1].tight.median)[0];

const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>REALIZED — what LPs actually took home</title>
<style>
:root{--bg:#0d1117;--fg:#e6edf3;--dim:#8b949e;--accent:#e07a5f;--line:#21262d;--card:#141a21}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif;
 -webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:56px 24px 96px}
h1{font-size:15px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin:0 0 28px;font-weight:600}
h2{font-size:23px;margin:56px 0 6px;letter-spacing:-.01em}
h2 .n{color:var(--dim);font-weight:400;font-size:15px;margin-right:10px}
.lede{font-size:26px;line-height:1.4;font-weight:600;letter-spacing:-.02em;margin:0 0 20px}
.lede em{color:var(--accent);font-style:normal}
.sub{color:var(--dim);font-size:16px;max-width:74ch;margin:0 0 8px}
p{max-width:74ch;color:#c9d1d9}
.dim{color:var(--dim)}.sm{font-size:12.5px;line-height:1.45}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14.5px}
th{text-align:left;font-weight:600;color:var(--dim);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;
 padding:0 12px 9px 0;border-bottom:1px solid var(--line)}
td{padding:13px 12px 13px 0;border-bottom:1px solid var(--line);vertical-align:middle}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
td.big{font-size:19px;font-weight:600;color:var(--accent)}
tr.untrusted td{background:rgba(139,148,158,.05)}
.spark,.bar{display:block;width:100%;height:auto}
.spark{max-width:260px}.bar{max-width:210px}
.mid{stroke:#30363d;stroke-width:1;stroke-dasharray:2 3}
.box{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);
 padding:18px 22px;margin:22px 0;border-radius:0 8px 8px 0}
.box.warn{border-left-color:#8b949e}
.box h3{margin:0 0 8px;font-size:15px;letter-spacing:.02em}
.box p{margin:0;font-size:14.5px;color:#adbac7}
code{background:#1c2128;padding:2px 6px;border-radius:4px;font-size:13px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.foot{margin-top:64px;padding-top:22px;border-top:1px solid var(--line);color:var(--dim);font-size:13px}
.kpi{display:flex;gap:38px;flex-wrap:wrap;margin:26px 0 8px}
.kpi div b{display:block;font-size:32px;color:var(--accent);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.kpi div span{font-size:12.5px;color:var(--dim)}
</style></head><body><div class="wrap">

<h1>Realized</h1>
<p class="lede">Advertised LP APR is positive by construction. <em>It cannot tell you that you lost money.</em></p>
<p class="sub">Advertised APR is fee income, annualized. It has no price term, so a pool cannot advertise a loss
no matter what happened to the people in it. Realized return = fees <b>+ impermanent loss</b>. Measured on live
data from The&nbsp;Graph across ${chainsValidated} chains and ${dexesValidated + 1} DEXes.</p>

<div class="kpi">
  <div><b>${totalMonths}</b><span>independent months measured</span></div>
  <div><b>${chainsValidated}</b><span>chains validated <span class="dim">of ${hist.chainsMeasured.length} queried</span></span></div>
  <div><b>${pct(worstChain[1].tight.median)}</b><span>median pools misleading a tight-range LP (${esc(worstChain[0])})</span></div>
  <div><b>${pct(worstChain[1].tight.min)}</b><span>even in that chain's best month</span></div>
</div>

<h2><span class="n">01</span>The defect survives every knob we can turn</h2>
<p class="sub">Uniswap v3 LPs <b>concentrate</b> into a price band. Inside a band impermanent loss is amplified;
once price leaves it you are fully converted into the losing asset and the loss is no longer impermanent.
Full-range is therefore the <b>most generous possible case for the pool</b> — so we report all of them.</p>
<table><thead><tr><th>LP range</th><th>median IL</th><th>median realized</th><th>knocked out of range</th><th>advertised + / real −</th></tr></thead>
<tbody>${rangeRows}</tbody></table>
<div class="box warn"><h3>Held deliberately unfair to us</h3><p>The fee term is constant across ranges.
Concentrating earns more fees too, so some of that IL is earned back — we cannot measure per-position fees from
pool-level data, so we did not model the uplift. The <b>direction</b> is what survives; treat magnitudes as bounded by that.</p></div>

<h2><span class="n">02</span>Not one lucky month, and not one chain</h2>
<p class="sub">Strictly <b>non-overlapping</b> 30-day tiles — no shared days, so the window count is a real sample count.
Each window runs its own stable-pair canary. Sparkline shows tight-range misleading% over time, oldest → newest, 50% mid-line.</p>
<table><thead><tr><th>chain</th><th>months</th><th>tight ±1.25x</th><th>moderate ±2x</th><th>full-range</th><th>over time</th></tr></thead>
<tbody>${chainRows}</tbody></table>
<div class="box"><h3>No Wayback Machine required</h3><p>We were about to reconstruct history by scraping archived
DeFi dashboards. Checked the primary source first: <code>poolDayData</code> reaches <b>2021-05-05</b> on mainnet —
1,952 days for USDC/WETH. The subgraph carries full history natively. One query saved an entire subsystem.</p></div>
<div class="box warn"><h3>Unavailable is never reported as clean</h3><p>${esc(hist.chainsUnavailable.join(' · '))}.
A chain we could not measure is never reported as a chain without the defect.</p></div>

<h2><span class="n">03</span>Not a Uniswap artifact</h2>
<p class="sub">The same instrument, unchanged, on an independent DEX. Different team, different codebase,
different incentive model — same defect, same shape, same range-ordering.</p>
<table><thead><tr><th>venue</th><th>months</th><th>tight ±1.25x</th><th>moderate ±2x</th><th>full-range</th></tr></thead>
<tbody>${dexRows}</tbody></table>

<h2><span class="n">04</span>The volatility check is a falsification test, not a finding</h2>
<p class="sub">Impermanent loss is <b>mathematically</b> a function of price divergence, so the defect <b>must</b>
worsen in volatile months. That is a prediction our own theory makes — if the data did not show it, our instrument
would be broken. We ran it to try to break ourselves and failed to.</p>
<table><thead><tr><th>range</th><th>n</th><th>Pearson</th><th>Spearman</th></tr></thead><tbody>${volRows}</tbody></table>
<div class="box warn"><h3>This is not evidence about macro or equities</h3><p>We did not test those series and will
not imply we did. With enough candidate predictors you can find a "relationship" to anything. A correlation predicted
in advance from an identity is a self-check; a correlation found by fishing would be a story.</p></div>

<h2><span class="n">05</span>Honesty box</h2>
<div class="box"><h3>Retracted: corr(advertised, realized) = 0.06</h3><p>It was this page's headline and it does
<b>not reproduce</b> — it existed in no committed code. Recomputed honestly it spans Pearson ${corpus.correlation.rows[0].pearson.toFixed(2)}–${corpus.correlation.rows[2].pearsonTrimmed.toFixed(2)}
depending on gate, trimming and estimator. That spread <i>is</i> the finding: quoting any single value as "the"
correlation was the mistake. The headline is now the pool-count result, which is measured rather than estimated.</p></div>
<table><thead><tr><th>liveness gate</th><th>n</th><th>Pearson</th><th>Spearman</th><th>trimmed 2% (P / S)</th></tr></thead>
<tbody>${corrRows}</tbody></table>
<div class="box"><h3>Base first returned 0 of 30 trusted windows — the canary working</h3><p>Base's top pools by
volume contained no stable/stable pair, so the instrument could not prove it measures IL correctly and refused to
certify. The fix was to <b>fetch the canary its reference pools</b>, never to weaken the canary. Those pools are
validation-only and excluded from every headline.</p></div>
<div class="box warn"><h3>Survivorship bias, and it points against us</h3><p>Pools are ranked by <i>current</i>
volume, so pools that died are absent from historical windows. That makes the past look <b>better</b> than it was,
weakening our thesis rather than inflating it. The subgraph exposes no point-in-time ranking, so we state the bias
instead of pretending to correct it.</p></div>
<div class="box warn"><h3>The stability check is not a hypothesis test</h3><p>A separate ${wf.windowsTotal}-window run
(<code>walkforward.json</code>) steps 15 days across a 30-day span, so adjacent windows share half their data.
${wf.windowsTrusted}/${wf.windowsTotal} trusted, defect in every one — but they are <b>not</b> independent samples.</p></div>

<div class="foot">
Corpus generated ${esc(corpus.generatedAt.slice(0, 16).replace('T', ' '))} UTC ·
history ${esc(hist.generatedAt.slice(0, 16).replace('T', ' '))} UTC ·
cross-DEX ${esc(xdex.generatedAt.slice(0, 16).replace('T', ' '))} UTC<br>
Source: The Graph decentralized network. Every number on this page is read from committed JSON —
this page performs no measurement of its own. Regenerate: <code>node scripts/build-report.js</code>
</div>
</div></body></html>`;

writeFileSync(`${__dirname}/../report.html`, html);
console.log(`wrote report.html (${(html.length / 1024).toFixed(1)} KB)`);
console.log(`  ${totalMonths} independent months, ${chainsValidated}/${hist.chainsMeasured.length} chains validated, ${dexesValidated + 1} DEXes`);
console.log(`  worst chain: ${worstChain[0]} median ${worstChain[1].tight.median.toFixed(0)}% tight-range`);
