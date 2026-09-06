import { strict as assert } from 'node:assert';
import { mock } from 'bun:test';

type CapturedWallet = {
  address: string;
  keyPair: unknown;
};

type CapturedPayload = {
  symbol: string;
};

let capturedWallet: CapturedWallet | null = null;
let capturedPayload: CapturedPayload | null = null;
let restoredPrivateKey: string | null = null;
let emptyCallArgCount: number | null = null;

class MockAElf {
  chain = {
    contractAt: async (_contractAddress: string, wallet: CapturedWallet) => {
      capturedWallet = wallet;
      return {
        GetBalance: {
          call: async (params: CapturedPayload) => {
            capturedPayload = params;
            return { result: { balance: '123' } };
          },
        },
        GetConfig: {
          call: async (...args: unknown[]) => {
            emptyCallArgCount = args.length;
            return { result: { value: 'config-ok' } };
          },
        },
      };
    },
    getTxResult: async () => ({ Status: 'MINED' }),
    getContractFileDescriptorSet: async () => ({ mocked: true }),
  };

  currentProvider = { host: 'https://rpc.example' };

  static providers = {
    HttpProvider: class {
      constructor(_host: string, _timeout?: number) {}
    },
  };

  static wallet = {
    createNewWallet: () => ({
      address: 'ELF_trimmed_wallet',
      privateKey: 'b'.repeat(64),
      mnemonic: 'm1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12',
      BIP44Path: "m/44'/1616'/0'/0/0",
      childWallet: { id: 'child' },
      keyPair: { getPrivate: () => 'mock-private' },
    }),
    getWalletByPrivateKey: (privateKey: string) => {
      restoredPrivateKey = privateKey;
      return {
        address: 'ELF_rehydrated_wallet',
        privateKey,
        mnemonic: 'm1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12',
        BIP44Path: "m/44'/1616'/0'/0/0",
        childWallet: { id: 'child' },
        keyPair: { getPrivate: () => 'mock-private' },
      };
    },
  };

  static pbjs = {
    Root: {
      fromDescriptor: () => ({ nestedArray: [] }),
    },
  };

  static utils = {};

  constructor(_provider: unknown) {}
}

mock.module('aelf-sdk', () => ({
  default: MockAElf,
}));

const { callViewMethod } = await import('../../../lib/aelf-client.js');

const result = await callViewMethod<{ balance: string }>(
  'https://rpc.example',
  'ELF_contract',
  'GetBalance',
  { symbol: 'ELF' },
);
const configResult = await callViewMethod<{ value: string }>(
  'https://rpc.example',
  'ELF_contract',
  'GetConfig',
);

assert.equal(
  restoredPrivateKey,
  'b'.repeat(64),
  'callViewMethod should rehydrate the ephemeral private key via getWalletByPrivateKey',
);
const wallet = capturedWallet as unknown as CapturedWallet;
const payload = capturedPayload as unknown as CapturedPayload;

assert.ok(wallet, 'contractAt should capture the rehydrated wallet');
assert.ok(payload, 'method.call should capture the input params');

assert.equal(
  wallet.address,
  'ELF_rehydrated_wallet',
  'contractAt should receive the rehydrated wallet',
);
assert.ok(
  wallet.keyPair,
  'contractAt should receive a wallet that still carries keyPair',
);
assert.equal(payload.symbol, 'ELF', 'method.call should receive the input params');
assert.equal(result.balance, '123', 'method.call result should be unwrapped');
assert.equal(emptyCallArgCount, 0, 'Empty-input view calls should omit the synthetic {} payload');
assert.equal(configResult.value, 'config-ok', 'Empty-input view result should still be unwrapped');

console.log(
  JSON.stringify({
    walletAddress: wallet.address,
    walletHasKeyPair: Boolean(wallet.keyPair),
    paramsEcho: payload.symbol,
    balance: result.balance,
    emptyCallArgCount,
    configValue: configResult.value,
  }),
);
