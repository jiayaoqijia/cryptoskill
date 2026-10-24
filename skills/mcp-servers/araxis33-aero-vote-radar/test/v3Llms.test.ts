import { test } from "node:test";
import assert from "node:assert/strict";
import { renderV3LlmsTxt } from "../src/v3Llms.js";
import type { V3ScanFile, V3ScanGauge } from "../src/v3.js";

const g = (sym: string, weight: number, fees: number, extra: Partial<V3ScanGauge> = {}): V3ScanGauge =>
  ({
    chain: "base", gauge: "0x1", pool: "0x2", weight, feesUsdPerDay: fees, fees24hUsdPerDay: fees,
    incentivesUsdPerDay: 0, usdPerDayPer10k: null, symbol0: sym, symbol1: "USDC", kind: "CL100", ...extra,
  }) as V3ScanGauge;

const scan = (gauges: V3ScanGauge[]): V3ScanFile => ({
  checkedAt: "2026-10-24T18:47:00.000Z", chain: "all", status: "live", windowHours: 66.4, gauges,
  chains: { base: { status: "live", windowHours: 66.4, gauges: gauges.length }, arc: { status: "live", windowHours: 66.4, gauges: 0 } },
});

test("llms.txt ranks pools of 100k+ sAERO by what 10,000 sAERO earns after dilution", () => {
  const txt = renderV3LlmsTxt(scan([g("SMALL", 50_000, 1000), g("LOW", 990_000, 100), g("HIGH", 190_000, 100)]));
  assert.doesNotMatch(txt, /SMALL\/USDC/);
  assert.ok(txt.indexOf("HIGH/USDC") < txt.indexOf("LOW/USDC"));
  assert.match(txt, /- HIGH\/USDC \(CL, Base\): about \$5\.00 a day for 10,000 sAERO/);
  assert.match(txt, /on 2 networks: 2026-10-24T18:47:00\.000Z/);
  assert.match(txt, /over the last 66 h/);
});

test("llms.txt lists steady pools only once there is history, and says so before", () => {
  assert.match(renderV3LlmsTxt(scan([g("HIGH", 190_000, 100)])), /Not enough hourly history yet/);
  const steady = g("CALM", 190_000, 100, { steady: { held: 30, of: 30, avgPer10k: 5.2, minPer10k: 4.1 } });
  const spiky = g("JUMPY", 190_000, 100, { steady: { held: 10, of: 30, avgPer10k: 9, minPer10k: 0.1 } });
  const txt = renderV3LlmsTxt(scan([steady, spiky]));
  assert.match(txt, /- CALM\/USDC \(CL, Base\): \$5\.00 a day now, average \$5\.20, lowest hour \$4\.10, held up 30 of 30 hours/);
  assert.doesNotMatch(txt.split("## Steadiest pools")[1], /JUMPY/);
});
