import { describe, expect, spyOn, test } from 'bun:test';
import * as aelfPool from '../../src/core/aelf-pool.js';
import { waitForTxResult } from '../../src/core/tx-waiter.js';
import { startMockAelfRpcServer } from '../helpers/mock-chain.js';

describe('tx waiter', () => {
  test('polls until transaction is mined', async () => {
    const rpc = startMockAelfRpcServer([
      { Status: 'PENDING' },
      { Status: 'MINED', Logs: [{ Name: 'Transferred' }] },
    ]);

    try {
      const result = await waitForTxResult(rpc.rpcUrl, '0xtx-1', {
        pollMs: 1,
        maxAttempts: 3,
      });

      expect(result.status).toBe('MINED');
      expect(rpc.getHits()).toBe(2);
      expect((result.raw?.Logs || []).length).toBe(1);
    } finally {
      rpc.stop();
    }
  });

  test('returns FAILED status without extra polling', async () => {
    const rpc = startMockAelfRpcServer([{ Status: 'FAILED', Error: 'execution failed' }]);

    try {
      const result = await waitForTxResult(rpc.rpcUrl, '0xtx-2', {
        pollMs: 1,
        maxAttempts: 3,
      });

      expect(result.status).toBe('FAILED');
      expect(rpc.getHits()).toBe(1);
    } finally {
      rpc.stop();
    }
  });

  test('throws TX_TIMEOUT when tx keeps pending', async () => {
    const rpc = startMockAelfRpcServer([{ Status: 'PENDING' }]);

    try {
      await expect(
        waitForTxResult(rpc.rpcUrl, '0xtx-timeout', {
          pollMs: 1,
          maxAttempts: 2,
        }),
      ).rejects.toMatchObject({
        code: 'TX_TIMEOUT',
      });
      expect(rpc.getHits()).toBe(2);
    } finally {
      rpc.stop();
    }
  });

  test('supports maxAttempts=0 fast timeout path', async () => {
    await expect(
      waitForTxResult('http://127.0.0.1:1', '0xtx-fast-timeout', {
        maxAttempts: 0,
      }),
    ).rejects.toMatchObject({
      code: 'TX_TIMEOUT',
    });
  });

  test('uses shared AElf factory from aelf pool', async () => {
    const rpc = startMockAelfRpcServer([{ Status: 'MINED' }]);
    const getAelfSpy = spyOn(aelfPool, 'getAelfByRpc');

    try {
      const result = await waitForTxResult(rpc.rpcUrl, '0xtx-shared-factory', {
        pollMs: 1,
        maxAttempts: 1,
      });

      expect(result.status).toBe('MINED');
      expect(getAelfSpy).toHaveBeenCalledTimes(1);
      expect(getAelfSpy.mock.calls[0]?.[0]).toBe(rpc.rpcUrl);
    } finally {
      getAelfSpy.mockRestore();
      rpc.stop();
    }
  });
});
