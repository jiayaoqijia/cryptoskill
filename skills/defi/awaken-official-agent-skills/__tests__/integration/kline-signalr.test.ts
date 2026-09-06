// ============================================================
// Integration Test: K-line SignalR (mainnet, read-only)
// ============================================================

import { describe, test, expect, beforeAll } from 'bun:test';
import axios from 'axios';
import * as signalR from '@microsoft/signalr';
import { getNetworkConfig } from '../../lib/config';
import type { KLineBar } from '../../lib/types';

const config = getNetworkConfig('mainnet');

let tradePairId: string | null = null;

// First, get a valid trade pair ID
beforeAll(async () => {
  const resp = await axios.get(`${config.apiBaseUrl}/api/app/trade-pairs`, {
    params: {
      ChainId: config.chainId,
      Token0Symbol: 'ELF',
      Token1Symbol: 'USDT',
      FeeRate: 0.003,
    },
  });
  const items = resp.data?.data?.items || resp.data?.items || [];
  if (items.length > 0) {
    tradePairId = items[0].id;
  }
}, 15000);

describe('SignalR K-line fetch (mainnet)', () => {
  test('connects to SignalR and fetches 1D K-line data', async () => {
    if (!tradePairId) {
      console.warn('Skipping: no trade pair ID found');
      return;
    }

    const connection = new signalR.HubConnectionBuilder()
      .withUrl(config.socketUrl, { withCredentials: false } as any)
      .withAutomaticReconnect()
      .build();

    const bars = await new Promise<KLineBar[]>(async (resolve, reject) => {
      const timer = setTimeout(() => {
        connection.stop().catch(() => {});
        reject(new Error('SignalR K-line fetch timed out'));
      }, 20000);

      connection.on('ReceiveKlines', (data: any) => {
        clearTimeout(timer);
        const rawBars: any[] = data?.data || data || [];
        const result: KLineBar[] = rawBars.map((bar: any) => ({
          time: bar.timestamp || bar.time,
          open: bar.openWithoutFee ?? bar.open,
          high: bar.highWithoutFee ?? bar.high,
          low: bar.lowWithoutFee ?? bar.low,
          close: bar.closeWithoutFee ?? bar.close,
          volume: bar.volume,
        }));
        connection.stop().catch(() => {});
        resolve(result);
      });

      try {
        await connection.start();
        const now = Date.now();
        const sevenDaysAgo = now - 7 * 24 * 60 * 60 * 1000;
        // Server expects: chainId(string), tradePairId(string), type(number), from(number), to(number)
        await connection.invoke(
          'RequestKline',
          config.chainId,
          tradePairId,
          86400, // 1D period in seconds (number)
          sevenDaysAgo,
          now,
        );
      } catch (err: any) {
        clearTimeout(timer);
        connection.stop().catch(() => {});
        reject(err);
      }
    });

    expect(bars.length).toBeGreaterThanOrEqual(1);

    const firstBar = bars[0];
    expect(firstBar.time).toBeDefined();
    expect(typeof firstBar.open).toBe('number');
    expect(typeof firstBar.high).toBe('number');
    expect(typeof firstBar.low).toBe('number');
    expect(typeof firstBar.close).toBe('number');
    expect(typeof firstBar.volume).toBe('number');
    expect(firstBar.high).toBeGreaterThanOrEqual(firstBar.low);
  }, 30000);
});
