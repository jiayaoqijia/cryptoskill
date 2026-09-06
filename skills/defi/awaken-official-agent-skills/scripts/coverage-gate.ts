#!/usr/bin/env bun
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

type SectionTotals = {
  linesFound: number;
  linesHit: number;
  funcsFound: number;
  funcsHit: number;
};

type FileCoverage = {
  lines: Map<number, number>;
  funcs: Map<string, number>;
  funcsFoundFallback: number;
  funcsHitFallback: number;
};

function isSrcFile(sfPath: string): boolean {
  const normalized = sfPath.replace(/\\/g, '/');
  return normalized.startsWith('src/') || normalized.includes('/src/');
}

function parseLcov(lcovText: string): SectionTotals {
  const files = new Map<string, FileCoverage>();
  let currentFile = '';
  let currentIsSrc = false;

  for (const rawLine of lcovText.split('\n')) {
    const line = rawLine.trim();
    if (!line) continue;

    if (line.startsWith('SF:')) {
      currentFile = line.slice(3);
      currentIsSrc = isSrcFile(currentFile);
      if (currentIsSrc && !files.has(currentFile)) {
        files.set(currentFile, {
          lines: new Map<number, number>(),
          funcs: new Map<string, number>(),
          funcsFoundFallback: 0,
          funcsHitFallback: 0,
        });
      }
      continue;
    }

    if (!currentFile || !currentIsSrc) {
      continue;
    }

    const coverage = files.get(currentFile);
    if (!coverage) continue;

    if (line.startsWith('DA:')) {
      const payload = line.slice(3);
      const [lineNoStr, hitsStr] = payload.split(',');
      const lineNo = Number(lineNoStr);
      const hits = Number(hitsStr) || 0;
      if (!Number.isNaN(lineNo)) {
        const prevHits = coverage.lines.get(lineNo) ?? 0;
        coverage.lines.set(lineNo, Math.max(prevHits, hits));
      }
      continue;
    }

    if (line.startsWith('FNDA:')) {
      const payload = line.slice(5);
      const firstComma = payload.indexOf(',');
      if (firstComma > 0) {
        const hits = Number(payload.slice(0, firstComma)) || 0;
        const fnName = payload.slice(firstComma + 1);
        const prevHits = coverage.funcs.get(fnName) ?? 0;
        coverage.funcs.set(fnName, Math.max(prevHits, hits));
      }
      continue;
    }

    if (line.startsWith('FN:')) {
      const payload = line.slice(3);
      const firstComma = payload.indexOf(',');
      if (firstComma > 0) {
        const fnName = payload.slice(firstComma + 1);
        if (!coverage.funcs.has(fnName)) {
          coverage.funcs.set(fnName, 0);
        }
      }
      continue;
    }

    if (line.startsWith('FNF:')) {
      const found = Number(line.slice(4)) || 0;
      coverage.funcsFoundFallback = Math.max(coverage.funcsFoundFallback, found);
      continue;
    }

    if (line.startsWith('FNH:')) {
      const hit = Number(line.slice(4)) || 0;
      coverage.funcsHitFallback = Math.max(coverage.funcsHitFallback, hit);
      continue;
    }
  }

  let linesFound = 0;
  let linesHit = 0;
  let funcsFound = 0;
  let funcsHit = 0;

  for (const fileCoverage of files.values()) {
    linesFound += fileCoverage.lines.size;
    for (const hits of fileCoverage.lines.values()) {
      if (hits > 0) linesHit += 1;
    }

    if (fileCoverage.funcs.size > 0) {
      funcsFound += fileCoverage.funcs.size;
      for (const hits of fileCoverage.funcs.values()) {
        if (hits > 0) funcsHit += 1;
      }
    } else {
      funcsFound += fileCoverage.funcsFoundFallback;
      funcsHit += Math.min(fileCoverage.funcsHitFallback, fileCoverage.funcsFoundFallback);
    }
  }

  return { linesFound, linesHit, funcsFound, funcsHit };
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
