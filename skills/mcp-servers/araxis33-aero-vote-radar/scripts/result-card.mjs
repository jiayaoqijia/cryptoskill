// The link-preview card: the last settled week's forecast against what the
// pools paid, the same figures as the page's "How wrong this page usually is"
// panel. X shows docs/card.png when a post links the page, so a post about the
// radar carries its latest result instead of a screenshot of the form.
//
// Writes the card as HTML to the path given (the workflow photographs it with
// the runner's Chrome) and prints the week it shows, e.g. 2026-10-08, which the
// workflow puts on og:image so X fetches the new picture instead of its cache.
// Run: node scripts/result-card.mjs card.html

import { readFileSync, writeFileSync } from "node:fs";

const promise = JSON.parse(readFileSync(new URL("../docs/data/promise.json", import.meta.url), "utf8"));
const epochs = (promise.epochs || []).filter((e) => e.rows && e.rows.length);
if (!epochs.length) {
  console.error("promise.json has no settled week");
  process.exit(1);
}
const week = epochs[epochs.length - 1];
const forecast = week.rows.reduce((a, r) => a + r.forecastUsd, 0) / week.rows.length;
const paid = week.rows.reduce((a, r) => a + (r.paidUsd || 0), 0) / week.rows.length;
const pct = Math.round((paid / forecast) * 100);
const usd = (n) => "$" + n.toFixed(2);
const day = new Date(week.epochStart + "T00:00:00Z").toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" });
const votes = (promise.perVeAero || 10000).toLocaleString("en-US");

writeFileSync(process.argv[2], `<!doctype html><html><head><meta charset="utf-8"><style>
body { margin: 0; font-family: Inter, "Segoe UI", "DejaVu Sans", system-ui, sans-serif; font-feature-settings: "calt" 0; }
.card { width: 1200px; height: 630px; box-sizing: border-box; padding: 56px 64px; display: flex; flex-direction: column;
  justify-content: space-between; color: #e8ecf3; background: radial-gradient(circle at 85% 0%, #3a1220 0%, #0b0f19 55%); }
.top { display: flex; justify-content: space-between; font-size: 26px; color: #9aa4b6; } .top b { color: #e8ecf3; }
h1 { font-size: 54px; line-height: 1.1; margin: 0; font-weight: 800; }
.nums { display: flex; gap: 28px; }
.n { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; padding: 24px 28px; }
.v { font-size: 64px; font-weight: 800; } .l { font-size: 22px; color: #9aa4b6; margin-top: 4px; }
.blue { color: #5aa2ff; } .good { color: #35d07f; } .mid { color: #ffb648; } .bad { color: #ff6b6b; }
.foot { display: flex; justify-content: space-between; font-size: 24px; color: #9aa4b6; } .foot b { color: #e8ecf3; }
</style></head><body><div class="card">
<div class="top"><span><b>Aero Vote Radar</b> · forecast vs paid</span><span>Week of ${day}</span></div>
<h1>The radar forecast ${usd(forecast)}.<br>Pools actually paid ${usd(paid)}.</h1>
<div class="nums">
<div class="n"><div class="v blue">${usd(forecast)}</div><div class="l">forecast per ${votes} votes</div></div>
<div class="n"><div class="v ${pct >= 90 ? "good" : pct >= 60 ? "mid" : "bad"}">${usd(paid)}</div><div class="l">actually paid</div></div>
<div class="n"><div class="v">${pct}%</div><div class="l">paid of the forecast</div></div>
</div>
<div class="foot"><span>Average per pool of the radar's top ${week.rows.length}, settled on-chain</span><b>aero.deftools.xyz</b></div>
</div></body></html>`);
console.log(week.epochStart);
