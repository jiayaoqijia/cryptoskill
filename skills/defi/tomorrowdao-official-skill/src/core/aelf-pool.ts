import AElf from 'aelf-sdk';
import { getConfig } from './config.js';

const aelfPool = new Map<string, any>();

export function getAelfByRpc(rpcUrl: string): any {
  const cacheMax = Math.max(1, getConfig().aelfCacheMax || 1);
  if (!aelfPool.has(rpcUrl)) {
    if (aelfPool.size >= cacheMax) {
      const oldestKey = aelfPool.keys().next().value;
      if (oldestKey) {
        aelfPool.delete(oldestKey);
      }
    }
    aelfPool.set(rpcUrl, new AElf(new AElf.providers.HttpProvider(rpcUrl, 20_000)));
  }
  return aelfPool.get(rpcUrl);
}

export function clearAelfPool(): void {
  aelfPool.clear();
}
