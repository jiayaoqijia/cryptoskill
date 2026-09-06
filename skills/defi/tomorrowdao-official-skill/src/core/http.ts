import { getConfig } from './config.js';
import { getAccessToken } from './auth.js';
import { SkillError } from './errors.js';
import type { ApiResponse } from './types.js';

function joinUrl(base: string, path: string): string {
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  if (path.startsWith('/')) return `${base}${path}`;
  return `${base}/${path}`;
}

function encodeQuery(params?: Record<string, unknown>): string {
  if (!params || Object.keys(params).length === 0) return '';
  const q = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v === undefined || v === null) return;
    q.set(k, String(v));
  });
  const query = q.toString();
  return query ? `?${query}` : '';
}

function shouldRetryStatus(status: number): boolean {
  return status === 408 || status === 425 || status === 429 || status >= 500;
}

function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function timeoutError(url: string, timeoutMs: number): SkillError {
  return new SkillError('API_HTTP_ERROR', `request timeout after ${timeoutMs}ms: ${url}`);
}

async function fetchWithTimeout(url: string, init: RequestInit, timeoutMs: number): Promise<Response> {
  if (timeoutMs <= 0) {
    return fetch(url, init);
  }

  const controller = new AbortController();
  let timeoutId: ReturnType<typeof setTimeout> | undefined;

  try {
    const fetchPromise = fetch(url, {
      ...init,
      signal: controller.signal,
    });

    const timeoutPromise = new Promise<Response>((_resolve, reject) => {
      timeoutId = setTimeout(() => {
        controller.abort();
        reject(timeoutError(url, timeoutMs));
      }, timeoutMs);
    });

    return await Promise.race([fetchPromise, timeoutPromise]);
  } catch (err) {
    if ((err as any)?.name === 'AbortError') {
      throw timeoutError(url, timeoutMs);
    }
    throw err;
  } finally {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  }
}

async function fetchWithPolicy(
  url: string,
  init: RequestInit,
  opts: {
    retryMax: number;
    retryBaseMs: number;
    retryEnabled: boolean;
    timeoutMs: number;
  },
): Promise<Response> {
  const maxAttempts = opts.retryEnabled ? Math.max(1, opts.retryMax + 1) : 1;

  let lastError: unknown;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      const resp = await fetchWithTimeout(url, init, opts.timeoutMs);
      if (!resp.ok && shouldRetryStatus(resp.status) && attempt < maxAttempts) {
        await wait(opts.retryBaseMs * 2 ** (attempt - 1));
        continue;
      }
      return resp;
    } catch (err) {
      lastError = err;
      if (attempt < maxAttempts) {
        await wait(opts.retryBaseMs * 2 ** (attempt - 1));
        continue;
      }
      break;
    }
  }

  if (lastError instanceof SkillError) {
    throw lastError;
  }

  throw new SkillError('API_HTTP_ERROR', `request failed: ${url}`, lastError);
}

export async function apiGet<T>(
  path: string,
  query?: Record<string, unknown>,
  options?: { auth?: boolean },
): Promise<T> {
  const config = getConfig();
  const headers: Record<string, string> = {};
  if (options?.auth) {
    const token = await getAccessToken();
    headers.Authorization = `${token.tokenType} ${token.accessToken}`;
  }
  const url = joinUrl(`${config.apiBase}/api/app`, path) + encodeQuery(query);

  const resp = await fetchWithPolicy(
    url,
    { method: 'GET', headers },
    {
      retryMax: config.httpRetryMax,
      retryBaseMs: config.httpRetryBaseMs,
      retryEnabled: config.httpRetryMax > 0,
      timeoutMs: config.httpTimeoutMs,
    },
  );

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    throw new SkillError('API_HTTP_ERROR', `${resp.status} ${path}`, text);
  }

  const json = (await resp.json()) as ApiResponse<T>;
  if (json?.code && json.code !== '20000') {
    throw new SkillError('API_BUSINESS_ERROR', json?.message || `api error ${json.code}`, json);
  }

  return (json?.data ?? (json as unknown as T));
}

export async function apiPost<TReq extends object, TRes>(
  path: string,
  payload: TReq,
  options?: { auth?: boolean },
): Promise<TRes> {
  const config = getConfig();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (options?.auth) {
    const token = await getAccessToken();
    headers.Authorization = `${token.tokenType} ${token.accessToken}`;
  }

  const url = joinUrl(`${config.apiBase}/api/app`, path);
  const resp = await fetchWithPolicy(
    url,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    },
    {
      retryMax: config.httpRetryMax,
      retryBaseMs: config.httpRetryBaseMs,
      retryEnabled: config.httpRetryPost && config.httpRetryMax > 0,
      timeoutMs: config.httpTimeoutMs,
    },
  );

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    throw new SkillError('API_HTTP_ERROR', `${resp.status} ${path}`, text);
  }

  const json = (await resp.json()) as ApiResponse<TRes>;
  if (json?.code && json.code !== '20000') {
    throw new SkillError('API_BUSINESS_ERROR', json?.message || `api error ${json.code}`, json);
  }

  return (json?.data ?? (json as unknown as TRes));
}
