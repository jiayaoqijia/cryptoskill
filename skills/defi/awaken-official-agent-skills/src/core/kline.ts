// ============================================================
// Core: K-line data functions (no I/O, pure logic)
// ============================================================

import * as signalR from '@microsoft/signalr';
import type { NetworkConfig, KLineBar, FetchKlineParams, KlineResult } from '../../lib/types';
import { KLINE_INTERVALS } from '../../lib/types';

// ---- fetchKline ----

export async function fetchKline(
  config: NetworkConfig,
  params: FetchKlineParams,
): Promise<KlineResult> {
  const interval = params.interval || '1D';
  const periodSeconds = KLINE_INTERVALS[interval];
  if (!periodSeconds) {
    throw new Error(`Invalid interval: ${interval}. Use: ${Object.keys(KLINE_INTERVALS).join(', ')}`);
  }

  const from = parseTimestamp(params.from ?? defaultFrom());
  const to = parseTimestamp(params.to ?? Date.now());
  const timeout = params.timeout ?? 15000;

  const bars = await fetchKlineViaSignalR({
    socketUrl: config.socketUrl,
    chainId: config.chainId,
    tradePairId: params.tradePairId,
    type: String(periodSeconds),
    from,
    to,
    timeout,
  });

  return {
    pairId: params.tradePairId,
    interval,
    periodSeconds,
    from: new Date(from).toISOString(),
    to: new Date(to).toISOString(),
    count: bars.length,
    bars,
  };
}

// ---- getKlineIntervals ----

export function getKlineIntervals(): Record<string, number> {
  return { ...KLINE_INTERVALS };
}

// ---- Internal: SignalR fetcher ----

interface FetchKlineViaSignalROptions {
  socketUrl: string;
  chainId: string;
  tradePairId: string;
  type: string;
  from: number;
  to: number;
  timeout: number;
}

async function fetchKlineViaSignalR(options: FetchKlineViaSignalROptions): Promise<KLineBar[]> {
  const { socketUrl, chainId, tradePairId, type, from, to, timeout } = options;

  const connection = new signalR.HubConnectionBuilder()
    .withUrl(socketUrl, { withCredentials: false } as any)
    .withAutomaticReconnect()
    .build();

  return new Promise<KLineBar[]>(async (resolve, reject) => {
    const timer = setTimeout(() => {
      connection.stop().catch(() => {});
      reject(new Error(`K-line fetch timed out after ${timeout}ms. The pair-id may be invalid.`));
    }, timeout);

    connection.on('ReceiveKlines', (data: any) => {
      clearTimeout(timer);
      try {
        const rawBars: any[] = data?.data || data || [];
        const bars: KLineBar[] = rawBars.map((bar: any) => ({
          time: bar.timestamp || bar.time,
          open: bar.openWithoutFee ?? bar.open,
          high: bar.highWithoutFee ?? bar.high,
          low: bar.lowWithoutFee ?? bar.low,
          close: bar.closeWithoutFee ?? bar.close,
          volume: bar.volume,
        }));

        bars.sort((a, b) => a.time - b.time);
        connection.stop().catch(() => {});
        resolve(bars);
      } catch (parseErr: any) {
        connection.stop().catch(() => {});
        reject(new Error(`Failed to parse K-line data: ${parseErr.message}`));
      }
    });

    try {
      await connection.start();
      // Server expects type as number (period in seconds)
      await connection.invoke('RequestKline', chainId, tradePairId, Number(type), from, to);
    } catch (connErr: any) {
      clearTimeout(timer);
      connection.stop().catch(() => {});
      reject(new Error(`SignalR connection failed: ${connErr.message}`));
    }
  });
}

// ---- Utility ----

function parseTimestamp(value: string | number): number {
  if (typeof value === 'number') return value > 1e12 ? value : value * 1000;
  const num = Number(value);
  if (!isNaN(num) && num > 1e12) return num;
  if (!isNaN(num) && num > 1e9) return num * 1000;
  const date = new Date(value);
  if (isNaN(date.getTime())) {
    throw new Error(`Invalid date: ${value}`);
  }
  return date.getTime();
}

function defaultFrom(): number {
  return Date.now() - 7 * 24 * 60 * 60 * 1000;
}
