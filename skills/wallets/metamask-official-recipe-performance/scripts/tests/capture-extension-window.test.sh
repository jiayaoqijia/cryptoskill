#!/usr/bin/env bash
set -euo pipefail

skill="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
script="$skill/scripts/capture-extension-window.mjs"

node --check "$script"
"$script" --help 2>&1 | grep -q '^Usage: capture-extension-window\.mjs \[--cdp-port <port>\]'
SCRIPT="$script" node --input-type=module <<'NODE'
const { normalizeUrl, sanitize } = await import(`file://${process.env.SCRIPT}`);
const canaries = [
  'url-user-canary', 'url-pass-canary', 'query-canary', 'fragment-canary',
  '0x1234567890abcdef1234567890abcdef', 'bearer-canary', 'password-canary',
  'token-canary', 'access-token-canary', 'api-key-canary', 'authorization-canary',
  'cookie-canary', 'session-canary', 'credential-canary',
];
const url = normalizeUrl(`https://url-user-canary:url-pass-canary@example.com/accounts/0x1234567890abcdef1234567890abcdef?token=query-canary#fragment-canary`);
const evidence = JSON.stringify(sanitize({
  error: `request failed at ${url}; Authorization: Bearer bearer-canary; password=password-canary`,
  requestUrl: `https://example.com/session/0x1234567890abcdef1234567890abcdef?key=query-canary#fragment-canary`,
  token: 'token-canary',
  accessToken: 'access-token-canary',
  apiKey: 'api-key-canary',
  authorization: 'authorization-canary',
  cookie: 'cookie-canary',
  session: { id: 'session-canary' },
  credential: 'credential-canary',
}));
for (const canary of canaries) {
  if (url.includes(canary) || evidence.includes(canary)) throw new Error(`secret canary leaked: ${canary}`);
}
if (!url.includes('example.com') || !evidence.includes('[REDACTED')) throw new Error('sanitized evidence lost safe context or its redaction marker');
NODE
SCRIPT="$script" node --input-type=module <<'NODE'
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import path from 'node:path';
const { run, terminateWithSignal } = await import(`file://${process.env.SCRIPT}`);
const root = mkdtempSync(path.join(tmpdir(), 'capture-extension-window-'));
const commandWithDescendant = (pidPath, resistSigterm = false) => [
  process.execPath,
  '-e',
  `const fs = require('node:fs');
   const { spawn } = require('node:child_process');
   const child = spawn(process.execPath, ['-e', ${JSON.stringify(
     resistSigterm ? "process.on('SIGTERM', () => {}); setInterval(() => {}, 1000)" : 'setInterval(() => {}, 1000)',
   )}], { stdio: 'ignore' });
   fs.writeFileSync(process.argv[1], String(child.pid));
   setInterval(() => {}, 1000);`,
  pidPath,
];
const assertStopped = async (pidPath) => {
  const descendantPid = Number(readFileSync(pidPath, 'utf8'));
  try {
    process.kill(descendantPid, 0);
    throw new Error('measured command left a descendant running');
  } catch (error) {
    if (error?.code !== 'ESRCH') throw error;
  }
};
try {
  const timeoutPidPath = path.join(root, 'timeout-descendant.pid');
  const startedAt = Date.now();
  try {
    await run(commandWithDescendant(timeoutPidPath), 500);
    throw new Error('hanging measured command unexpectedly passed');
  } catch (error) {
    if (!error.message.includes('measured command timed out after 500ms')) throw error;
    if (Date.now() - startedAt > 2_000) throw new Error('timed-out measured command was not terminated');
    await assertStopped(timeoutPidPath);
  }

  for (const signal of ['SIGHUP', 'SIGTERM']) {
    const signalPidPath = path.join(root, `${signal}-descendant.pid`);
    try {
      setTimeout(() => process.kill(process.pid, signal), 500);
      await run(commandWithDescendant(signalPidPath, signal === 'SIGTERM'), 5_000);
      throw new Error('interrupted measured command unexpectedly passed');
    } catch (error) {
      if (!error.message.includes(`measured command interrupted by ${signal}`)) throw error;
      await assertStopped(signalPidPath);
    }
  }
} finally {
  rmSync(root, { recursive: true, force: true });
}

const statusProbe = spawnSync(process.execPath, [
  '--input-type=module',
  '-e',
  `const { run, terminateWithSignal } = await import(${JSON.stringify(`file://${process.env.SCRIPT}`)});
   setTimeout(() => process.kill(process.pid, 'SIGTERM'), 100);
   try {
     await run([process.execPath, '-e', 'setInterval(() => {}, 1000)'], 5000);
   } catch (error) {
     terminateWithSignal(error.signal);
   }`,
]);
if (statusProbe.signal !== 'SIGTERM') {
  throw new Error(`interrupted wrapper lost SIGTERM status: ${statusProbe.status}/${statusProbe.signal}`);
}
if (typeof terminateWithSignal !== 'function') throw new Error('signal termination helper is unavailable');
NODE
! grep -q 'command: options.command' "$script"

set +e
output="$("$script" --cdp-port 9500 --boundary body --out-dir /tmp 2>&1)"
status=$?
set -e
test "$status" -eq 2
grep -q '^capture-extension-window: pass the measured command after --$' <<<"$output"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/temp/recipe/runtime"
printf '{"cdpPort":1}\n' > "$tmp/temp/recipe/runtime/agentic-runtime.json"
set +e
output="$(cd "$tmp" && "$script" --boundary body --out-dir artifacts -- true 2>&1)"
status=$?
set -e
test "$status" -eq 1
grep -q 'fetch failed' <<<"$output"

printf '{"cdpPort":0}\n' > "$tmp/temp/recipe/runtime/agentic-runtime.json"
set +e
output="$(cd "$tmp" && "$script" --boundary body --out-dir artifacts -- true 2>&1)"
status=$?
set -e
test "$status" -eq 1
grep -q 'no authoritative Extension CDP port found' <<<"$output"

printf '{broken json\n' > "$tmp/temp/recipe/runtime/agentic-runtime.json"
set +e
output="$(cd "$tmp" && "$script" --cdp-port 1 --boundary body --out-dir artifacts -- true 2>&1)"
status=$?
set -e
test "$status" -eq 1
grep -q 'fetch failed' <<<"$output"
! grep -q 'could not read .*agentic-runtime.json' <<<"$output"

echo 'capture-extension-window: CLI contract passed'
