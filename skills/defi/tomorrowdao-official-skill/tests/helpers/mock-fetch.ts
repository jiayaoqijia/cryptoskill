export interface FetchCall {
  url: string;
  init?: RequestInit;
}

export type FetchHandler = (
  url: string,
  init: RequestInit | undefined,
  calls: FetchCall[],
) => Response | Promise<Response>;

export function installFetchMock(handler: FetchHandler): {
  calls: FetchCall[];
  restore: () => void;
} {
  const calls: FetchCall[] = [];
  const original = globalThis.fetch;

  globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
    const url =
      typeof input === 'string'
        ? input
        : input instanceof URL
          ? input.toString()
          : input.url;
    calls.push({ url, init });
    return handler(url, init, calls);
  }) as typeof fetch;

  return {
    calls,
    restore: () => {
      globalThis.fetch = original;
    },
  };
}

export function jsonResponse(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}

export function textResponse(payload: string, status = 200): Response {
  return new Response(payload, { status });
}
