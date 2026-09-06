import { clearCaches, getAelfInstance, getTxResult } from '../../../lib/aelf-client.js';

type TxResultCheck = {
  terminalError: string;
  pendingError: string;
  longTailMinedStatus: string;
  notExistedError: string;
};

async function main(): Promise<void> {
  const originalSetTimeout = globalThis.setTimeout;
  globalThis.setTimeout = ((callback: (...args: any[]) => void, _delay?: number, ...args: any[]) => {
    callback(...args);
    return 0 as unknown as ReturnType<typeof setTimeout>;
  }) as typeof globalThis.setTimeout;

  try {
    clearCaches();
    let instance = getAelfInstance('https://rpc.test') as any;
    instance.chain = {
      getTxResult: async () => ({
        TransactionId: 'tx-validation',
        Status: 'NODEVALIDATIONFAILED',
        Error: 'Low transfer security level.',
      }),
    };

    let terminalError = '';
    try {
      await getTxResult('https://rpc.test', 'tx-validation', 1);
    } catch (error) {
      terminalError = error instanceof Error ? error.message : String(error);
    }

    clearCaches();
    instance = getAelfInstance('https://rpc.test') as any;
    instance.chain = {
      getTxResult: async () => ({
        TransactionId: 'tx-pending',
        Status: 'PENDING_VALIDATION',
        Error: '',
      }),
    };

    let pendingError = '';
    try {
      await getTxResult('https://rpc.test', 'tx-pending', 0);
    } catch (error) {
      pendingError = error instanceof Error ? error.message : String(error);
    }

    clearCaches();
    instance = getAelfInstance('https://rpc.test') as any;
    let longTailPollCount = 0;
    instance.chain = {
      getTxResult: async () => {
        longTailPollCount += 1;
        if (longTailPollCount <= 2) {
          return {
            TransactionId: 'tx-long-tail',
            Status: 'NOTEXISTED',
            Error: '',
          };
        }
        if (longTailPollCount === 3) {
          return {
            TransactionId: 'tx-long-tail',
            Status: 'PENDING',
            Error: '',
          };
        }
        return {
          TransactionId: 'tx-long-tail',
          Status: 'MINED',
          Error: '',
        };
      },
    };

    const longTailMined = await getTxResult('https://rpc.test', 'tx-long-tail', 4);

    clearCaches();
    instance = getAelfInstance('https://rpc.test') as any;
    instance.chain = {
      getTxResult: async () => ({
        TransactionId: 'tx-not-existed',
        Status: 'NOTEXISTED',
        Error: '',
      }),
    };

    let notExistedError = '';
    try {
      await getTxResult('https://rpc.test', 'tx-not-existed', 1);
    } catch (error) {
      notExistedError = error instanceof Error ? error.message : String(error);
    }

    const payload: TxResultCheck = {
      terminalError,
      pendingError,
      longTailMinedStatus: String(longTailMined?.Status || ''),
      notExistedError,
    };

    console.log(JSON.stringify(payload));
  } finally {
    globalThis.setTimeout = originalSetTimeout;
    clearCaches();
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : String(error));
  process.exitCode = 1;
});
