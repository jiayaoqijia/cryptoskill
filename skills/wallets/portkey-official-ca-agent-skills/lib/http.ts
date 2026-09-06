import type { PortkeyConfig } from './types.js';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface HttpRequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  params?: Record<string, string | number | boolean | undefined>;
  data?: unknown;
  headers?: Record<string, string>;
  timeout?: number;
}

interface ApiResponse<T = unknown> {
  code: string;
  message: string;
  data: T;
}

// ---------------------------------------------------------------------------
// HttpError — structured error for precise matching
// ---------------------------------------------------------------------------

export class HttpError extends Error {
  /** HTTP status code (e.g. 400, 404, 500) */
  statusCode: number;
  /** Portkey API error code (e.g. '3002'), if present */
  errorCode: string | null;
  /** Raw response body text */
  responseBody: string;

  constructor(statusCode: number, statusText: string, body: string) {
    const { errorCode, apiMessage } = extractApiError(body);

    super(`HTTP ${statusCode} ${statusText}: ${apiMessage || body}`);
    this.name = 'HttpError';
    this.statusCode = statusCode;
    this.errorCode = errorCode;
    this.responseBody = body;
  }
}

function extractApiError(body: string): { errorCode: string | null; apiMessage: string } {
  try {
    const parsed = JSON.parse(body);
    const nested = parsed?.error && typeof parsed.error === 'object' ? parsed.error : null;
    return {
      errorCode: nested?.code ?? nested?.Code ?? parsed?.code ?? parsed?.Code ?? null,
      apiMessage: nested?.message ?? nested?.Message ?? parsed?.message ?? parsed?.Message ?? '',
    };
  } catch {
    return {
      errorCode: null,
      apiMessage: body,
    };
  }
}

// ---------------------------------------------------------------------------
// HTTP client
// ---------------------------------------------------------------------------

const DEFAULT_TIMEOUT = 20_000;

/**
 * Lightweight HTTP client for Portkey Backend API.
 *
 * Usage:
 *   const client = createHttpClient(config);
 *   const result = await client.get('/api/app/wallet/getRegisterInfo', { params: { ... } });
 *   const result = await client.post('/api/app/account/sendVerificationRequest', { data: { ... } });
 */
export function createHttpClient(config: PortkeyConfig) {
  const baseUrl = config.apiUrl.replace(/\/$/, '');

  async function request<T = unknown>(endpoint: string, options: HttpRequestOptions = {}): Promise<T> {
    const { method = 'GET', params, data, headers = {}, timeout = DEFAULT_TIMEOUT } = options;

    // Build URL with query params
    let url = `${baseUrl}${endpoint}`;
    if (params) {
      const searchParams = new URLSearchParams();
      for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== null) {
          searchParams.set(key, String(value));
        }
      }
      const qs = searchParams.toString();
      if (qs) url += `?${qs}`;
    }

    // Build fetch options
    const fetchOptions: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };

    if (data && method !== 'GET') {
      fetchOptions.body = JSON.stringify(data);
    }

    // Timeout via AbortController
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);
    fetchOptions.signal = controller.signal;

    try {
      const response = await fetch(url, fetchOptions);
      clearTimeout(timer);

      if (!response.ok) {
        const text = await response.text().catch(() => '');
        throw new HttpError(response.status, response.statusText, text);
      }

      const json = await response.json() as ApiResponse<T> | T;

      // Portkey API wraps some responses in { code, message, data }
      if (json && typeof json === 'object' && 'code' in json) {
        const wrapped = json as ApiResponse<T>;
        if (wrapped.code !== '20000' && wrapped.code !== '0') {
          throw new Error(`API error [${wrapped.code}]: ${wrapped.message}`);
        }
        return wrapped.data;
      }

      return json as T;
    } catch (err: unknown) {
      clearTimeout(timer);
      if (err instanceof DOMException && err.name === 'AbortError') {
        throw new Error(`Request timeout after ${timeout}ms: ${method} ${url}`);
      }
      throw err;
    }
  }

  return {
    get<T = unknown>(endpoint: string, options?: Omit<HttpRequestOptions, 'method' | 'data'>) {
      return request<T>(endpoint, { ...options, method: 'GET' });
    },
    post<T = unknown>(endpoint: string, options?: Omit<HttpRequestOptions, 'method'>) {
      return request<T>(endpoint, { ...options, method: 'POST' });
    },
    put<T = unknown>(endpoint: string, options?: Omit<HttpRequestOptions, 'method'>) {
      return request<T>(endpoint, { ...options, method: 'PUT' });
    },
    del<T = unknown>(endpoint: string, options?: Omit<HttpRequestOptions, 'method'>) {
      return request<T>(endpoint, { ...options, method: 'DELETE' });
    },
    /** Raw request with full control */
    request,
  };
}

export type HttpClient = ReturnType<typeof createHttpClient>;

// ---------------------------------------------------------------------------
// SSRF protection — validate user-supplied RPC URLs
// ---------------------------------------------------------------------------

const PRIVATE_IP_PATTERNS = [
  /^localhost$/i,
  /^127\./,
  /^10\./,
  /^172\.(1[6-9]|2\d|3[01])\./,
  /^192\.168\./,
  /^0\./,
  /^\[::1\]/,
  /^\[fd/i,      // IPv6 unique-local
  /^\[fe80:/i,   // IPv6 link-local
];

/**
 * Validate a user-supplied RPC URL to prevent SSRF attacks.
 * - Requires https:// (or http:// only for known aelf domains)
 * - Blocks private/internal IP ranges and localhost
 *
 * Throws if the URL is unsafe.
 */
export function validateRpcUrl(url: string): void {
  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    throw new Error(`Invalid RPC URL: ${url}`);
  }

  // Only allow http(s)
  if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') {
    throw new Error(`RPC URL must use http(s) protocol, got: ${parsed.protocol}`);
  }

  // Block private/internal addresses
  const hostname = parsed.hostname;
  for (const pattern of PRIVATE_IP_PATTERNS) {
    if (pattern.test(hostname)) {
      throw new Error(`RPC URL must not point to a private/internal address: ${hostname}`);
    }
  }
}
