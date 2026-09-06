declare module 'aelf-sdk' {
  interface HttpProvider {
    new (host: string, timeout?: number): HttpProvider;
  }

  interface WalletModule {
    createNewWallet(): {
      address: string;
      privateKey: string;
      mnemonic: string;
      BIP44Path: string;
      childWallet: unknown;
      keyPair: unknown;
    };
    getWalletByPrivateKey(privateKey: string): {
      address: string;
      privateKey: string;
      keyPair: unknown;
    };
  }

  interface ChainModule {
    contractAt(
      contractAddress: string,
      wallet: { address: string; privateKey?: string },
    ): Promise<Record<string, any>>;
    getTxResult(txId: string): Promise<Record<string, any>>;
    getContractFileDescriptorSet(address: string): Promise<any>;
  }

  interface PbjsModule {
    Root: {
      fromDescriptor(descriptor: any, syntax?: string): any;
    };
  }

  interface UtilsModule {
    chainIdConvertor: {
      base58ToChainId(chainId: string): number;
      chainIdToBase58(chainId: number): string;
    };
    sha256(input: string): string;
    transform?: {
      transformMapToArray(type: any, params: any): any;
      transform(type: any, params: any, transformers: any): any;
      INPUT_TRANSFORMERS: any;
    };
  }

  class AElf {
    constructor(provider: HttpProvider);
    chain: ChainModule;
    currentProvider: { host: string };
    static providers: { HttpProvider: new (host: string, timeout?: number) => HttpProvider };
    static wallet: WalletModule;
    static pbjs: PbjsModule;
    static utils: UtilsModule;
  }

  export default AElf;
}

declare module 'aelf-sdk/src/util/keyStore.js' {
  interface KeystoreWalletInfo {
    privateKey: string;
    mnemonic: string;
    address?: string;
    nickName?: string;
  }

  interface KeystoreObject {
    version: number;
    type: string;
    nickName?: string;
    address: string;
    crypto: {
      cipher: string;
      ciphertext: string;
      cipherparams: { iv: string };
      mnemonicEncrypted: string;
      kdf: string;
      kdfparams: {
        r: number;
        n: number;
        p: number;
        dklen: number;
        salt: string;
      };
      mac: string;
    };
  }

  export function getKeystore(
    walletInfo: KeystoreWalletInfo,
    password: string,
    option?: Record<string, unknown>,
  ): KeystoreObject;

  export function unlockKeystore(
    keyStore: KeystoreObject | Record<string, unknown>,
    password: string,
  ): KeystoreWalletInfo;

  export function checkPassword(
    keyStore: KeystoreObject | Record<string, unknown>,
    password: string,
  ): boolean;
}
