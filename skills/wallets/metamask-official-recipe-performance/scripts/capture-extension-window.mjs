#!/usr/bin/env node

import { readFileSync } from 'node:fs';
import { mkdir, writeFile } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

function usage(message) {
  if (message) console.error(`capture-extension-window: ${message}`);
  console.error('Usage: capture-extension-window.mjs [--cdp-port <port>] --boundary <selector> --out-dir <dir> [--timeout-ms <ms>] -- <command> [args...]');
  process.exit(message ? 2 : 0);
}

function parseArgs(argv) {
  if (argv.includes('-h') || argv.includes('--help')) usage();
  const split = argv.indexOf('--');
  if (split < 0 || split === argv.length - 1) usage('pass the measured command after --');
  const options = argv.slice(0, split);
  const command = argv.slice(split + 1);
  const parsed = { timeoutMs: 15_000, command };
  for (let index = 0; index < options.length; index += 1) {
    const key = options[index];
    const value = options[index + 1];
    if (!value) usage(`missing value for ${key}`);
    if (key === '--cdp-port') parsed.cdpPort = Number(value);
    else if (key === '--boundary') parsed.boundary = value;
    else if (key === '--out-dir') parsed.outDir = value;
    else if (key === '--timeout-ms') parsed.timeoutMs = Number(value);
    else usage(`unknown option ${key}`);
    index += 1;
  }
  if (parsed.cdpPort !== undefined && (!Number.isInteger(parsed.cdpPort) || parsed.cdpPort < 1)) usage('--cdp-port must be a positive integer');
  if (!parsed.boundary) usage('--boundary is required');
  if (!parsed.outDir) usage('--out-dir is required');
  if (!Number.isFinite(parsed.timeoutMs) || parsed.timeoutMs < 1) usage('--timeout-ms must be positive');
  return parsed;
}

function resolveCdpPort(explicitPort) {
  const overrides = [
    ['--cdp-port', explicitPort],
    ['RECIPE_CDP_PORT', process.env.RECIPE_CDP_PORT],
    ['CDP_PORT', process.env.CDP_PORT],
  ];
  const override = overrides.find(([, value]) => value !== undefined && value !== '');
  if (override) {
    const [source, rawPort] = override;
    const cdpPort = Number(rawPort);
    if (!Number.isInteger(cdpPort) || cdpPort < 1) {
      throw new Error(`${source} must be a positive integer`);
    }
    return { cdpPort, source };
  }

  const runtimePath = path.resolve('temp/recipe/runtime/agentic-runtime.json');
  try {
    const runtime = JSON.parse(readFileSync(runtimePath, 'utf8'));
    const cdpPort = Number(runtime.cdpPort);
    if (Number.isInteger(cdpPort) && cdpPort > 0) return { cdpPort, source: runtimePath };
  } catch (error) {
    if (error?.code !== 'ENOENT') throw new Error(`could not read ${runtimePath}: ${error.message}`);
  }
  throw new Error('no authoritative Extension CDP port found; run mm-harness doctor --fix or pass --cdp-port <port>');
}

class CdpClient {
  constructor(socket) {
    this.socket = socket;
    this.nextId = 0;
    this.pending = new Map();
    this.listeners = new Map();
    socket.onmessage = ({ data }) => this.receive(JSON.parse(String(data)));
  }

  static async connect(url) {
    if (typeof WebSocket !== 'function') throw new Error('Node WebSocket support is required');
    const socket = new WebSocket(url);
    await new Promise((resolve, reject) => {
      socket.onopen = resolve;
      socket.onerror = () => reject(new Error(`could not connect to ${url}`));
    });
    return new CdpClient(socket);
  }

  receive(message) {
    if (message.id && this.pending.has(message.id)) {
      const pending = this.pending.get(message.id);
      this.pending.delete(message.id);
      if (message.error) pending.reject(new Error(`${pending.method}: ${message.error.message}`));
      else pending.resolve(message.result ?? {});
      return;
    }
    if (!message.method) return;
    for (const listener of this.listeners.get(message.method) ?? []) listener(message.params ?? {});
  }

  send(method, params = {}) {
    const id = ++this.nextId;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { method, resolve, reject });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  on(method, listener) {
    const listeners = this.listeners.get(method) ?? [];
    listeners.push(listener);
    this.listeners.set(method, listeners);
  }

  once(method, timeoutMs) {
    return new Promise((resolve, reject) => {
      const remove = (listener) => {
        const listeners = this.listeners.get(method) ?? [];
        this.listeners.set(method, listeners.filter((candidate) => candidate !== listener));
      };
      const listener = (params) => {
        clearTimeout(timer);
        remove(listener);
        resolve(params);
      };
      const timer = setTimeout(() => {
        remove(listener);
        reject(new Error(`timed out waiting for ${method}`));
      }, timeoutMs);
      this.on(method, listener);
    });
  }

  close() {
    this.socket.close();
  }
}

async function extensionTarget(port) {
  const response = await fetch(`http://127.0.0.1:${port}/json/list`);
  if (!response.ok) throw new Error(`CDP target list returned HTTP ${response.status}`);
  const targets = await response.json();
  const matches = targets.filter((target) => target.type === 'page' && /^chrome-extension:\/\/.+\/home\.html/.test(target.url));
  if (matches.length !== 1) throw new Error(`expected one MetaMask home.html page target on CDP :${port}, found ${matches.length}`);
  if (!matches[0].webSocketDebuggerUrl) throw new Error('selected Extension target has no webSocketDebuggerUrl');
  return matches[0];
}

export function run(command, timeoutMs) {
  return new Promise((resolve, reject) => {
    const detached = process.platform !== 'win32';
    const child = spawn(command[0], command.slice(1), {
      cwd: process.cwd(),
      env: process.env,
      stdio: 'inherit',
      detached,
    });
    let timedOut = false;
    let interruptedBy;
    let forceKillTimer;
    let timeout;
    let cleanupPromise = Promise.resolve();
    const kill = (signal) => {
      if (!child.pid) return;
      try {
        if (detached) process.kill(-child.pid, signal);
        else child.kill(signal);
      } catch (error) {
        if (error?.code !== 'ESRCH') throw error;
      }
    };
    const waitForGroupExit = async () => {
      if (!detached || !child.pid) return;
      for (let attempt = 0; attempt < 100; attempt += 1) {
        try {
          process.kill(-child.pid, 0);
        } catch (error) {
          if (error?.code === 'ESRCH') return;
          throw error;
        }
        await new Promise((resolve) => setTimeout(resolve, 10));
      }
      throw new Error('measured command process group did not terminate');
    };
    const scheduleForceKill = (delayMs) => {
      cleanupPromise = new Promise((resolve, rejectCleanup) => {
        forceKillTimer = setTimeout(async () => {
          try {
            kill('SIGKILL');
            await waitForGroupExit();
            resolve();
          } catch (error) {
            rejectCleanup(error);
          }
        }, delayMs);
      });
    };
    const signalHandlers = new Map(['SIGHUP', 'SIGINT', 'SIGQUIT', 'SIGTERM'].map((signal) => [
      signal,
      () => {
        if (interruptedBy) return;
        interruptedBy = signal;
        clearTimeout(timeout);
        kill(signal);
        scheduleForceKill(1_000);
      },
    ]));
    const removeSignalHandlers = () => {
      for (const [signal, handler] of signalHandlers) process.off(signal, handler);
    };
    for (const [signal, handler] of signalHandlers) process.on(signal, handler);
    timeout = setTimeout(() => {
      timedOut = true;
      kill('SIGTERM');
      scheduleForceKill(Math.min(timeoutMs, 1_000));
    }, timeoutMs);
    child.once('error', (error) => {
      clearTimeout(timeout);
      clearTimeout(forceKillTimer);
      removeSignalHandlers();
      reject(error);
    });
    child.once('exit', async (code, signal) => {
      clearTimeout(timeout);
      if (!timedOut && !interruptedBy) clearTimeout(forceKillTimer);
      removeSignalHandlers();
      try {
        if (timedOut || interruptedBy) await cleanupPromise;
      } catch (error) {
        reject(error);
        return;
      }
      if (timedOut) {
        reject(new Error(`measured command timed out after ${timeoutMs}ms`));
        return;
      }
      if (interruptedBy) {
        const error = new Error(`measured command interrupted by ${interruptedBy}`);
        error.signal = interruptedBy;
        reject(error);
        return;
      }
      if (code === 0) resolve();
      else reject(new Error(`measured command failed (${signal ?? `exit ${code ?? 'unknown'}`})`));
    });
  });
}

export function terminateWithSignal(signal) {
  process.kill(process.pid, signal);
}

async function waitForBoundary(client, selector, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  const expression = `(() => { const node = document.querySelector(${JSON.stringify(selector)}); if (!node) return false; const style = getComputedStyle(node); const rect = node.getBoundingClientRect(); return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0; })()`;
  while (Date.now() < deadline) {
    const result = await client.send('Runtime.evaluate', { expression, returnByValue: true });
    if (result.result?.value === true) return;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  throw new Error(`boundary did not become visible within ${timeoutMs}ms: ${selector}`);
}

function redactPlainText(value) {
  return String(value)
    .replace(/\bBearer\s+\S+/giu, 'Bearer [REDACTED]')
    .replace(/\b(password|passwd|token|secret|mnemonic|seed|private[_-]?key)\s*[:=]\s*([^\s,;&]+)/giu, '$1=[REDACTED]')
    .replace(/0x[a-fA-F0-9]{16,}/g, '[REDACTED_HEX]');
}

function sensitivePathSegment(segment) {
  let decoded = segment;
  try {
    decoded = decodeURIComponent(segment);
  } catch {}
  return /^0x[a-f0-9]{16,}$/iu.test(decoded)
    || decoded.length >= 24;
}

export function normalizeUrl(value) {
  try {
    const url = new URL(value);
    url.username = '';
    url.password = '';
    for (const key of [...url.searchParams.keys()]) url.searchParams.set(key, '<redacted>');
    url.hash = '';
    url.pathname = url.pathname
      .split('/')
      .map((segment) => (sensitivePathSegment(segment) ? encodeURIComponent('[REDACTED]') : segment))
      .join('/');
    return redactPlainText(url.toString());
  } catch {
    return redactPlainText(value);
  }
}

function sanitizeString(value) {
  const withSafeUrls = String(value).replace(
    /\b(?:https?|wss?):\/\/[^\s"'<>]+/giu,
    (url) => normalizeUrl(url),
  );
  return redactPlainText(withSafeUrls);
}

export function sanitize(value, key = '') {
  if (value === null || value === undefined) return value;
  if (/headers|postData|password|mnemonic|private|secret|seed|vault|token|authorization|cookie|session|credential|api[-_]?key/i.test(key)) return '<redacted>';
  if (typeof value === 'string') return /url/i.test(key) ? normalizeUrl(value) : sanitizeString(value);
  if (Array.isArray(value)) return value.map((item) => sanitize(item));
  if (typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([childKey, childValue]) => [childKey, sanitize(childValue, childKey)]));
  return value;
}

function metricsMap(result) {
  return Object.fromEntries((result.metrics ?? []).map(({ name, value }) => [name, value]));
}

function metricDeltas(before, after) {
  const names = ['TaskDuration', 'ScriptDuration', 'LayoutDuration', 'RecalcStyleDuration', 'LayoutCount', 'RecalcStyleCount'];
  return Object.fromEntries(names.map((name) => [name, Number(((after[name] ?? 0) - (before[name] ?? 0)).toFixed(6))]));
}

function networkSummary(events) {
  const requests = new Map();
  for (const event of events) {
    const id = event.params.requestId;
    const record = requests.get(id) ?? { requestId: id };
    if (event.method === 'Network.requestWillBeSent') {
      record.method = event.params.request?.method;
      record.url = normalizeUrl(event.params.request?.url ?? '');
      record.initiator = sanitize(event.params.initiator ?? null);
      record.startedAt = event.params.timestamp ?? null;
    } else if (event.method === 'Network.responseReceived') {
      record.status = event.params.response?.status ?? null;
      record.protocol = event.params.response?.protocol ?? null;
    } else if (event.method === 'Network.loadingFinished') {
      record.encodedDataLength = event.params.encodedDataLength ?? 0;
      record.finishedAt = event.params.timestamp ?? null;
    } else if (event.method === 'Network.loadingFailed') {
      record.failed = true;
      record.errorText = sanitizeString(event.params.errorText ?? 'unknown');
    }
    requests.set(id, record);
  }
  const rows = [...requests.values()].filter((row) => row.url);
  const groups = new Map();
  for (const row of rows) {
    const key = `${row.method ?? 'GET'} ${row.url}`;
    const group = groups.get(key) ?? [];
    group.push(row.requestId);
    groups.set(key, group);
  }
  return {
    requestCount: rows.length,
    transferredBytes: rows.reduce((sum, row) => sum + (row.encodedDataLength ?? 0), 0),
    duplicateCandidates: [...groups.entries()].filter(([, ids]) => ids.length > 1).map(([key, requestIds]) => ({ key, count: requestIds.length, requestIds })),
    requests: rows,
  };
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const resolvedPort = resolveCdpPort(options.cdpPort);
  options.cdpPort = resolvedPort.cdpPort;
  const outDir = path.resolve(options.outDir);
  await mkdir(outDir, { recursive: true });
  const target = await extensionTarget(options.cdpPort);
  const client = await CdpClient.connect(target.webSocketDebuggerUrl);
  const networkEvents = [];
  const traceEvents = [];
  let before = {};
  let after = {};
  let startedAt = null;
  let finishedAt = null;
  let failure = null;
  let interruptedSignal = null;
  let tracingStarted = false;

  for (const method of ['Network.requestWillBeSent', 'Network.responseReceived', 'Network.loadingFinished', 'Network.loadingFailed']) {
    client.on(method, (params) => networkEvents.push({ method, params }));
  }
  client.on('Tracing.dataCollected', ({ value }) => traceEvents.push(...(value ?? [])));

  try {
    await client.send('Network.enable');
    await client.send('Performance.enable');
    before = metricsMap(await client.send('Performance.getMetrics'));
    await client.send('Tracing.start', {
      categories: 'devtools.timeline,v8.execute,blink.user_timing,loading',
      transferMode: 'ReportEvents',
    });
    tracingStarted = true;
    startedAt = new Date().toISOString();
    await run(options.command, options.timeoutMs);
    await waitForBoundary(client, options.boundary, options.timeoutMs);
    finishedAt = new Date().toISOString();
    after = metricsMap(await client.send('Performance.getMetrics'));
  } catch (error) {
    failure = sanitizeString(error instanceof Error ? error.message : String(error));
    if (typeof error?.signal === 'string') interruptedSignal = error.signal;
  } finally {
    if (tracingStarted) {
      try {
        const complete = client.once('Tracing.tracingComplete', options.timeoutMs);
        await client.send('Tracing.end');
        await complete;
      } catch (error) {
        failure ??= sanitizeString(error instanceof Error ? error.message : String(error));
      }
    }
  }

  const network = networkSummary(networkEvents);
  const summary = {
    schemaVersion: 1,
    status: failure ? 'fail' : 'pass',
    target: { id: target.id, url: normalizeUrl(target.url), cdpPort: options.cdpPort, cdpPortSource: resolvedPort.source },
    boundary: sanitizeString(options.boundary),
    startedAt,
    finishedAt,
    durationMs: startedAt && finishedAt ? Date.parse(finishedAt) - Date.parse(startedAt) : null,
    metrics: failure || Object.keys(before).length === 0 || Object.keys(after).length === 0
      ? null
      : metricDeltas(before, after),
    requestCount: network.requestCount,
    transferredBytes: network.transferredBytes,
    duplicateCandidates: network.duplicateCandidates,
    reactCommits: 'N/A — no verified React Profiler channel',
    ...(failure ? { error: failure } : {}),
  };
  const evidence = {
    ...summary,
    performance: { before, after },
    network: network.requests,
    traceEvents: sanitize(traceEvents),
  };
  const summaryPath = path.join(outDir, 'performance-window.summary.json');
  const evidencePath = path.join(outDir, 'performance-window.events.json');
  await writeFile(summaryPath, `${JSON.stringify(summary, null, 2)}\n`);
  await writeFile(evidencePath, `${JSON.stringify(evidence, null, 2)}\n`);
  client.close();
  console.log(`performance summary: ${summaryPath}`);
  console.log(`performance events: ${evidencePath}`);
  if (interruptedSignal) {
    terminateWithSignal(interruptedSignal);
    return;
  }
  if (failure) throw new Error(failure);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch((error) => {
    console.error(`capture-extension-window: ${sanitizeString(error instanceof Error ? error.message : String(error))}`);
    process.exitCode = 1;
  });
}
