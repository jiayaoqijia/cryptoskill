import { getConfig } from './config.js';
import { SkillError, HttpStatusError } from './errors.js';
import { serializeQuery } from './serializer.js';
import type { AelfscanEnvelope, HttpClientResult } from './types.js';

export interface HttpRequestOptions {
  method?: 'GET' | 'POST';
  path: string;
  query?: Record<string, unknown>;
  body?: unknown;
  headers?: Record<string, string>;
  traceId?: string;
  cacheTtlMs?: number;
  disableCache?: boolean;
}

const responseCache = new Map<string, { expiresAt: number; value: HttpClientResult<unknown> }>();
const pendingResolvers: Array<() => void> = [];
let activeRequests = 0;

function shouldRetry(error: unknown): boolean {
  if (!(error instanceof SkillError)) {
    return true;
  }

  if (!error.httpStatus) {
    return true;
  }

  return error.httpStatus >= 500;
}

function getRetryDelayMs(attempt: number, retryBaseMs: number, retryMaxMs: number): number {
  const exponential = Math.min(retryBaseMs * 2 ** attempt, retryMaxMs);
  const jitter = Math.floor(Math.random() * Math.max(1, Math.floor(exponential * 0.25)));
  return exponential + jitter;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function parseResponseBody(response: Response): Promise<unknown> {
  const text = await response.text();
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function ensurePath(path: string): string {
  if (path.startsWith('/')) {
    return path;
  }

  return `/${path}`;
}

async function acquireSlot(limit: number): Promise<() => void> {
  if (limit <= 0) {
    return () => {};
  }

  if (activeRequests < limit) {
    activeRequests += 1;
    return releaseSlot;
  }

  await new Promise<void>((resolve) => pendingResolvers.push(resolve));
  activeRequests += 1;
  return releaseSlot;
}

function releaseSlot(): void {
  activeRequests = Math.max(0, activeRequests - 1);
  const next = pendingResolvers.shift();
  if (next) {
    next();
  }
}

function getCacheTtlMs(method: 'GET' | 'POST', path: string, options: HttpRequestOptions): number {
  const config = getConfig();

  if (options.disableCache) {
    return 0;
  }

  if (options.cacheTtlMs !== undefined) {
    return Math.max(0, options.cacheTtlMs);
  }

  if (method === 'GET' && path.startsWith('/api/app/statistics/')) {
    return Math.max(0, config.cacheTtlMs);
  }

  return 0;
}

function getCacheKey(method: 'GET' | 'POST', url: string): string {
  return `${method}:${url}`;
}

function getCachedValue<T>(cacheKey: string): HttpClientResult<T> | null {
  const cached = responseCache.get(cacheKey);
  if (!cached) {
    return null;
  }

  if (cached.expiresAt <= Date.now()) {
    responseCache.delete(cacheKey);
    return null;
  }

  // Keep most recently used cache item at the tail.
  responseCache.delete(cacheKey);
  responseCache.set(cacheKey, cached);
  return cached.value as HttpClientResult<T>;
}

function setCachedValue(cacheKey: string, value: HttpClientResult<unknown>, expiresAt: number, maxEntries: number): void {
  if (maxEntries <= 0) {
    return;
  }

  if (responseCache.has(cacheKey)) {
    responseCache.delete(cacheKey);
  }

  responseCache.set(cacheKey, { expiresAt, value });

  while (responseCache.size > maxEntries) {
    const oldest = responseCache.keys().next().value;
    if (oldest === undefined) {
      break;
    }
    responseCache.delete(oldest);
  }
}

export function resetHttpClientState(): void {
  responseCache.clear();
  activeRequests = 0;
  while (pendingResolvers.length > 0) {
    const next = pendingResolvers.shift();
    if (next) {
      next();
    }
  }
}

export async function request<T>(options: HttpRequestOptions): Promise<HttpClientResult<T>> {
  const config = getConfig();
  const method = options.method || 'GET';
  const path = ensurePath(options.path);
  const queryString = serializeQuery(options.query);
  const url = `${config.apiBaseUrl}${path}${queryString ? `?${queryString}` : ''}`;
  const traceId = options.traceId;
  const cacheTtlMs = getCacheTtlMs(method, path, options);
  const cacheMaxEntries = Math.max(0, config.cacheMaxEntries);
  const cacheKey = getCacheKey(method, url);

  if (cacheTtlMs > 0 && cacheMaxEntries > 0 && method === 'GET') {
    const cached = getCachedValue<T>(cacheKey);
    if (cached) {
      return cached;
    }
  }

  let lastError: unknown;

  for (let attempt = 0; attempt <= config.retry; attempt += 1) {
    const releaseSlotHandle = await acquireSlot(config.maxConcurrentRequests);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), config.timeoutMs);

    try {
      const response = await fetch(url, {
        method,
        signal: controller.signal,
        headers: {
          Accept: 'application/json, text/plain; q=0.9',
          'Content-Type': 'application/json',
          ...(traceId ? { 'X-Trace-Id': traceId } : {}),
          ...(options.headers || {}),
        },
        body: options.body === undefined ? undefined : JSON.stringify(options.body),
      });

      const rawBody = await parseResponseBody(response);

      if (!response.ok) {
        throw new HttpStatusError(response.status, rawBody);
      }

      const envelope = rawBody as AelfscanEnvelope<T>;
      if (envelope && typeof envelope === 'object' && 'code' in envelope) {
        if (envelope.code && envelope.code !== '20000') {
          throw new SkillError('API_BUSINESS_ERROR', envelope.message || 'Aelfscan business error', envelope);
        }

        const successResult = {
          data: (envelope.data as T) ?? ({} as T),
          raw: envelope,
        };

        if (cacheTtlMs > 0 && cacheMaxEntries > 0 && method === 'GET') {
          setCachedValue(cacheKey, successResult as HttpClientResult<unknown>, Date.now() + cacheTtlMs, cacheMaxEntries);
        }

        return successResult;
      }

      const successResult = {
        data: rawBody as T,
        raw: rawBody,
      };

      if (cacheTtlMs > 0 && cacheMaxEntries > 0 && method === 'GET') {
        setCachedValue(cacheKey, successResult as HttpClientResult<unknown>, Date.now() + cacheTtlMs, cacheMaxEntries);
      }

      return successResult;
    } catch (error) {
      lastError = error;
      if (attempt < config.retry && shouldRetry(error)) {
        const delayMs = getRetryDelayMs(attempt, config.retryBaseMs, config.retryMaxMs);
        await sleep(delayMs);
        continue;
      }
      break;
    } finally {
      clearTimeout(timeout);
      releaseSlotHandle();
    }
  }

  throw lastError;
}
