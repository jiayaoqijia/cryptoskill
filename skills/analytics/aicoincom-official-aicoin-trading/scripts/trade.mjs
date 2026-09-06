#!/usr/bin/env node
// Alias: trade.mjs → exchange.mjs (models often guess "trade" instead of "exchange")
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';

const __dir = dirname(fileURLToPath(import.meta.url));
try {
  execFileSync(process.execPath, [resolve(__dir, 'exchange.mjs'), ...process.argv.slice(2)], { stdio: 'inherit' });
} catch (e) {
  process.exit(e.status || 1);
}
