#!/usr/bin/env node
/**
 * `npm run accrual` — writes `docs/data/accrual.json` and prints the same
 * figures, answering the one question the README has been open about not being
 * able to answer: what did a pool actually *earn* between two moments, as
 * opposed to what its already-earned rewards were re-priced at.
 *
 * It needs no RPC. Everything it reports comes out of scans this repository has
 * already committed — which is the point: the number is reproducible by anyone
 * with the history, and it cannot drift away from the file it describes.
 *
 * Like `timing`, this wants the full git history of the snapshot file rather
 * than a shallow clone, and only scans from 2026-08-28 onward carry the raw
 * amounts it reads.
 */
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { pathToFileURL } from "node:url";
import { snapshotsFromDir, snapshotsFromGit } from "./settled.js";
import { buildAccrualReport, scanFromSnapshot, type AccrualScan, type AccrualReport } from "./accrual.js";
import { formatError } from "./util.js";

const pct = (x: number) => (Number.isNaN(x) ? "  n/a" : `${(x * 100).toFixed(0).padStart(4)}%`);
const usd = (x: number) => (Number.isNaN(x) ? "n/a" : `$${x.toFixed(2)}`);

export function formatReport(report: AccrualReport): string {
  const lines: string[] = [];
  lines.push(
    `${report.scans} scans carrying raw reward amounts, ${report.from.slice(0, 10)} to ${report.to.slice(0, 10)}.`,
    "",
    "window   obs   any accrual   negative (naive)   negative (accrual)   median naive   median accrual when it moved",
  );
  for (const w of report.windows) {
    lines.push(
      [
        `${String(w.hours).padStart(4)}h`,
        String(w.observations).padStart(6),
        pct(w.withAccrual).padStart(13),
        pct(w.negativeNaive).padStart(19),
        pct(w.negativeAccrual).padStart(21),
        usd(w.medianNaiveUsd).padStart(15),
        usd(w.medianAccrualWhenMoved).padStart(30),
      ].join(""),
    );
  }

  const flagged = report.windows.filter((w) => w.amountFell > 0 || w.withUnpriced > 0);
  if (flagged.length > 0) {
    lines.push("", "Data notes (these are not economics — they are reasons to read a row with care):");
    for (const w of flagged) {
      const bits: string[] = [];
      if (w.amountFell > 0) bits.push(`${w.amountFell} window(s) where a raw amount fell inside an epoch`);
      if (w.withUnpriced > 0) bits.push(`${w.withUnpriced} carrying a token with no price, counted as $0 on both sides`);
      lines.push(`  ${w.hours}h: ${bits.join("; ")}`);
    }
  }

  if (report.pureRepricing.length > 0) {
    lines.push("", "Biggest dollar moves that were entirely price — the amounts behind them never budged:");
    for (const p of report.pureRepricing) {
      lines.push(`  ${p.symbol.padEnd(24)} ${usd(p.repricingUsd).padStart(12)}`);
    }
  }

  if (report.didAccrue.length > 0) {
    lines.push("", "Pools whose raw amounts actually moved:");
    for (const p of report.didAccrue) {
      lines.push(`  ${p.symbol.padEnd(24)} accrual ${usd(p.accrualUsd).padStart(12)}   repricing ${usd(p.repricingUsd).padStart(12)}`);
    }
  } else {
    lines.push("", "No pool's raw amounts moved inside an epoch over this history.");
  }

  return lines.join("\n");
}

async function main() {
  const dir = process.argv[2];
  const outPath = process.argv[3] ?? "docs/data/accrual.json";
  const snapshots = dir ? snapshotsFromDir(dir) : snapshotsFromGit();
  if (snapshots.length === 0) {
    console.error("No snapshots to measure. This needs the full git history of the snapshot file, not a shallow clone.");
    process.exitCode = 1;
    return;
  }

  const scans: AccrualScan[] = [];
  for (const raw of snapshots) {
    const scan = scanFromSnapshot(raw);
    if (scan) scans.push(scan);
  }

  if (scans.length < 2) {
    console.error(
      `Only ${scans.length} scan(s) carry raw reward amounts, and a window needs two. Scans from before 2026-08-28 do not have them.`,
    );
    process.exitCode = 1;
    return;
  }

  const report = buildAccrualReport(scans);
  console.log(formatReport(report));

  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, `${JSON.stringify(report, null, 2)}\n`);
  console.log(`\nWrote ${outPath}`);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((err) => {
    console.error(formatError(err));
    process.exitCode = 1;
  });
}
