import { test } from "node:test";
import assert from "node:assert/strict";
import { formatReport } from "../src/accrual-cli.js";
import type { AccrualReport, WindowSummary } from "../src/accrual.js";

const window = (overrides: Partial<WindowSummary> = {}): WindowSummary => ({
  hours: 48,
  observations: 10,
  negativeNaive: 0.2,
  negativeAccrual: 0,
  withAccrual: 0.1,
  medianNaiveUsd: 12.5,
  medianAccrualUsd: 4,
  medianAccrualWhenMoved: 30,
  medianRepricingShare: 0.6,
  amountFell: 0,
  withUnpriced: 0,
  ...overrides,
});

const report = (overrides: Partial<AccrualReport> = {}): AccrualReport => ({
  generatedAt: "2026-09-01T00:00:00.000Z",
  scans: 5,
  from: "2026-08-28T00:00:00.000Z",
  to: "2026-09-01T00:00:00.000Z",
  windows: [window()],
  pureRepricing: [],
  didAccrue: [],
  ...overrides,
});

test("formatReport prints the scan count and date range from the report", () => {
  const out = formatReport(report());
  assert.ok(out.includes("5 scans carrying raw reward amounts, 2026-08-28 to 2026-09-01."));
});

test("formatReport renders a window's percentages and dollar figures", () => {
  const out = formatReport(report({ windows: [window({ hours: 72, observations: 4, negativeNaive: 0.5 })] }));
  assert.ok(out.includes("72h"));
  assert.ok(out.includes("50%"), "negativeNaive should render as a whole-number percent");
  assert.ok(out.includes("$12.50"), "medianNaiveUsd should render as a dollar figure");
});

test("formatReport renders n/a for NaN figures instead of a literal 'NaN'", () => {
  const out = formatReport(
    report({
      windows: [
        window({
          observations: 0,
          negativeNaive: NaN,
          negativeAccrual: NaN,
          withAccrual: NaN,
          medianNaiveUsd: NaN,
          medianAccrualUsd: NaN,
          medianAccrualWhenMoved: NaN,
        }),
      ],
    }),
  );
  assert.ok(!out.includes("NaN"), `expected no literal NaN in output, got:\n${out}`);
  assert.ok(out.includes("n/a"));
});

test("formatReport calls out windows with a fallen amount or an unpriced token as data notes", () => {
  const out = formatReport(
    report({ windows: [window({ hours: 96, amountFell: 2, withUnpriced: 3 })] }),
  );
  assert.ok(out.includes("Data notes"));
  assert.ok(out.includes("2 window(s) where a raw amount fell inside an epoch"));
  assert.ok(out.includes("3 carrying a token with no price, counted as $0 on both sides"));
});

test("formatReport omits the data notes section when nothing was flagged", () => {
  const out = formatReport(report({ windows: [window({ amountFell: 0, withUnpriced: 0 })] }));
  assert.ok(!out.includes("Data notes"));
});

test("formatReport lists pure-repricing and accrued pools when present", () => {
  const out = formatReport(
    report({
      pureRepricing: [{ symbol: "AERO/USDC", pool: "0xpool1", repricingUsd: 99.5 }],
      didAccrue: [{ symbol: "WETH/AERO", pool: "0xpool2", accrualUsd: 10, repricingUsd: -2 }],
    }),
  );
  assert.ok(out.includes("Biggest dollar moves that were entirely price"));
  assert.ok(out.includes("AERO/USDC"));
  assert.ok(out.includes("$99.50"));
  assert.ok(out.includes("Pools whose raw amounts actually moved"));
  assert.ok(out.includes("WETH/AERO"));
});

test("formatReport says nothing accrued when didAccrue is empty", () => {
  const out = formatReport(report({ didAccrue: [] }));
  assert.ok(out.includes("No pool's raw amounts moved inside an epoch over this history."));
});
