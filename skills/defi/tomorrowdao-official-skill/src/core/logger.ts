import { randomUUID } from 'node:crypto';

export type LogLevel = 'error' | 'warn' | 'info' | 'debug';

const LEVEL_WEIGHT: Record<LogLevel, number> = {
  error: 0,
  warn: 1,
  info: 2,
  debug: 3,
};

function parseLevel(raw?: string): LogLevel {
  const value = (raw || '').toLowerCase();
  if (value === 'debug' || value === 'info' || value === 'warn' || value === 'error') {
    return value;
  }
  return 'error';
}

let level = parseLevel(process.env.TMRW_LOG_LEVEL || 'error');

function activeLevel(): LogLevel {
  return level;
}

export function setLogLevel(nextLevel: LogLevel | string): LogLevel {
  level = parseLevel(String(nextLevel || ''));
  return level;
}

export function resetLogLevelFromEnv(): LogLevel {
  level = parseLevel(process.env.TMRW_LOG_LEVEL || 'error');
  return level;
}

function sanitize(payload: Record<string, unknown>): Record<string, unknown> {
  const banned = ['privateKey', 'accessToken', 'authorization', 'token'];
  const out: Record<string, unknown> = {};
  Object.entries(payload).forEach(([k, v]) => {
    if (banned.some((x) => k.toLowerCase().includes(x.toLowerCase()))) {
      out[k] = '[REDACTED]';
    } else {
      out[k] = v;
    }
  });
  return out;
}

function shouldLog(levelName: LogLevel): boolean {
  return LEVEL_WEIGHT[levelName] <= LEVEL_WEIGHT[activeLevel()];
}

export function log(levelName: LogLevel, event: string, payload: Record<string, unknown> = {}): void {
  if (!shouldLog(levelName)) return;
  const entry = {
    ts: new Date().toISOString(),
    level: levelName,
    event,
    ...sanitize(payload),
  };
  process.stderr.write(`${JSON.stringify(entry)}\n`);
}

export function logError(event: string, payload: Record<string, unknown> = {}): void {
  log('error', event, payload);
}

export function newTraceId(): string {
  return randomUUID();
}
