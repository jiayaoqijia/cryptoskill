#!/usr/bin/env bun
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.resolve(import.meta.dir, '..');
const lcovPath = path.join(root, 'coverage', 'lcov.info');
const outputDir = path.join(root, 'badge');
const outputPath = path.join(outputDir, 'coverage.json');

if (!fs.existsSync(lcovPath)) {
  process.stderr.write(`[ERROR] lcov not found: ${lcovPath}\n`);
  process.exit(1);
}

const lcov = fs.readFileSync(lcovPath, 'utf-8');
let linesFound = 0;
let linesHit = 0;

for (const line of lcov.split('\n')) {
  if (line.startsWith('LF:')) linesFound += Number(line.slice(3)) || 0;
  if (line.startsWith('LH:')) linesHit += Number(line.slice(3)) || 0;
}

const coverage = linesFound > 0 ? (linesHit / linesFound) * 100 : 0;
const rounded = Math.round(coverage * 100) / 100;

let color = 'red';
if (rounded >= 90) color = 'brightgreen';
else if (rounded >= 80) color = 'green';
else if (rounded >= 70) color = 'yellowgreen';
else if (rounded >= 60) color = 'yellow';
else if (rounded >= 50) color = 'orange';

const badge = {
  schemaVersion: 1,
  label: 'coverage',
  message: `${rounded}%`,
  color,
};

fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(badge, null, 2)}\n`, 'utf-8');
process.stdout.write(`[OK] Coverage badge generated: ${outputPath} (${badge.message})\n`);
