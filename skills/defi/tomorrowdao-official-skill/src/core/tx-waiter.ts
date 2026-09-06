import { SkillError } from './errors.js';
import * as aelfPool from './aelf-pool.js';

export interface WaitTxOptions {
  pollMs?: number;
  maxAttempts?: number;
}

export async function waitForTxResult(
  rpcUrl: string,
  txId: string,
  options?: WaitTxOptions,
): Promise<{ status: string; raw: any }> {
  const pollMs = options?.pollMs ?? 1000;
  const maxAttempts = options?.maxAttempts ?? 30;
  const instance = aelfPool.getAelfByRpc(rpcUrl);

  for (let i = 0; i < maxAttempts; i += 1) {
    const result = await instance.chain.getTxResult(txId);
    const normalized = (result?.result || result) as any;
    const status = String(normalized?.Status || '').toUpperCase();
    if (status && status !== 'PENDING' && status !== 'PENDING_VALIDATION' && status !== 'NOTEXISTED') {
      return {
        status,
        raw: normalized,
      };
    }
    await new Promise((resolve) => setTimeout(resolve, pollMs));
  }

  throw new SkillError('TX_TIMEOUT', `transaction polling timeout: ${txId}`);
}
