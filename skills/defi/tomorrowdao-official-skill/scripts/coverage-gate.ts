#!/usr/bin/env bun
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

type SectionTotals = {
  linesFound: number;
  linesHit: number;
  funcsFound: number;
  funcsHit: number;
};

function isSrcFile(sfPath: string): boolean {
  const normalized = sfPath.replace(/\\/g, '/');
  return normalized.startsWith('src/') || normalized.includes('/src/');
}

function parseLcov(lcovText: string): SectionTotals {
  const totals: SectionTotals = {
    linesFound: 0,
    linesHit: 0,
    funcsFound: 0,
    funcsHit: 0,
  };

  let currentFile = '';

  for (const rawLine of lcovText.split('\n')) {
    const line = rawLine.trim();
    if (!line) continue;

    if (line.startsWith('SF:')) {
      currentFile = line.slice(3);
      continue;
    }

    if (!currentFile || !isSrcFile(currentFile)) {
      continue;
    }

    if (line.startsWith('LF:')) {
      totals.linesFound += Number(line.slice(3)) || 0;
      continue;
    }

    if (line.startsWith('LH:')) {
      totals.linesHit += Number(line.slice(3)) || 0;
      continue;
    }

    if (line.startsWith('FNF:')) {
      totals.funcsFound += Number(line.slice(4)) || 0;
      continue;
    }

    if (line.startsWith('FNH:')) {
      totals.funcsHit += Number(line.slice(4)) || 0;
      continue;
    }
  }

  return totals;
}

function percent(hit: number, found: number): number {
  if (found <= 0) return 0;
  return (hit / found) * 100;
}

function main() {
  const minLines = Number(process.env.COVERAGE_MIN_LINES || '85');
  const minFuncs = Number(process.env.COVERAGE_MIN_FUNCS || '80');
  const lcovFile = process.env.COVERAGE_LCOV_FILE || 'coverage/lcov.info';
  const lcovPath = resolve(process.cwd(), lcovFile);

  if (!existsSync(lcovPath)) {
    console.error(`[coverage-gate] lcov file not found: ${lcovPath}`);
    process.exit(1);
  }

  const lcov = readFileSync(lcovPath, 'utf8');
  const totals = parseLcov(lcov);

  if (totals.linesFound === 0 || totals.funcsFound === 0) {
    console.error('[coverage-gate] no src/** lines/functions coverage data found');
    process.exit(1);
  }

  const linePct = percent(totals.linesHit, totals.linesFound);
  const funcPct = percent(totals.funcsHit, totals.funcsFound);

  const failures: string[] = [];
  if (linePct < minLines) {
    failures.push(`lines ${linePct.toFixed(2)}% < ${minLines}%`);
  }
  if (funcPct < minFuncs) {
    failures.push(`funcs ${funcPct.toFixed(2)}% < ${minFuncs}%`);
  }

  if (failures.length) {
    console.error(`[coverage-gate] failed: ${failures.join(', ')}`);
    process.exit(1);
  }

  console.log(
    `[coverage-gate] passed: lines=${linePct.toFixed(2)}% funcs=${funcPct.toFixed(2)}% (threshold lines>=${minLines} funcs>=${minFuncs})`,
  );
}

main();
