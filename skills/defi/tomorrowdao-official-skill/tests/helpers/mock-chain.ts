export interface TxResultSequenceItem {
  Status?: string;
  status?: string;
  Logs?: unknown[];
  logs?: unknown[];
  [k: string]: unknown;
}

export function startMockAelfRpcServer(sequence: TxResultSequenceItem[]) {
  let cursor = 0;
  let hits = 0;

  const server = Bun.serve({
    port: 0,
    fetch(req) {
      const url = new URL(req.url);
      if (url.pathname === '/api/blockChain/transactionResult') {
        hits += 1;
        const item = sequence[Math.min(cursor, sequence.length - 1)] || { Status: 'NOTEXISTED' };
        cursor += 1;
        return Response.json(item);
      }
      return new Response('not found', { status: 404 });
    },
  });

  return {
    rpcUrl: `http://127.0.0.1:${server.port}`,
    getHits: () => hits,
    stop: () => server.stop(true),
  };
}
