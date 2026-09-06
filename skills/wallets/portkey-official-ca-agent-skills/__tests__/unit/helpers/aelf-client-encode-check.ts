import { strict as assert } from 'node:assert';
import { mock } from 'bun:test';

type MockResolvedType = {
  fromObject: (obj: unknown) => unknown;
  encode: (msg: unknown) => { finish: () => Uint8Array };
};

const resolvedType: MockResolvedType = {
  fromObject: (obj: unknown) => obj,
  encode: () => ({ finish: () => new Uint8Array([1, 2, 3]) }),
};

const methodRecord: { requestType: string; resolvedRequestType?: MockResolvedType } = {
  requestType: '.aelf.Hash',
};

const root = {
  nestedArray: [
    {
      name: 'RewardClaimContract',
      methods: {
        ClaimByPortkeyToCa: methodRecord,
      },
    },
  ],
  resolveAll() {
    methodRecord.resolvedRequestType = resolvedType;
    return this;
  },
};

class MockAElf {
  chain = {
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
      address: 'ELF_mock_wallet',
      privateKey: 'a'.repeat(64),
      mnemonic: 'm1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12',
    }),
    getWalletByPrivateKey: (privateKey: string) => ({
      address: 'ELF_mock_wallet',
      privateKey,
    }),
  };

  static pbjs = {
    Root: {
      fromDescriptor: () => root,
    },
  };

  static utils = {};

  constructor(_provider: unknown) {}
}

mock.module('aelf-sdk', () => ({
  default: MockAElf,
}));

const { encodeManagerForwardCallParams } = await import('../../../lib/aelf-client.js');

const result = await encodeManagerForwardCallParams('https://rpc.example', {
  caHash: 'hash',
  contractAddress: 'reward',
  methodName: 'ClaimByPortkeyToCa',
  args: { value: Buffer.from('11'.repeat(32), 'hex') },
});

assert.equal(
  methodRecord.resolvedRequestType,
  resolvedType,
  'resolveAll should populate resolvedRequestType before encoding',
);
assert.deepEqual(
  Array.from(result.args as Uint8Array),
  [1, 2, 3],
  'encoded args should come from the resolved protobuf type',
);

console.log(
  JSON.stringify({
    resolvedRequestTypeSet: methodRecord.resolvedRequestType === resolvedType,
    encodedArgs: Array.from(result.args as Uint8Array),
  }),
);
