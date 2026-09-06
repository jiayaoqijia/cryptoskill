import { describe, it, expect } from 'bun:test';

describe('SDK exports (index.ts)', () => {
  it('should export config functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.getConfig).toBe('function');
    expect(mod.NETWORK_DEFAULTS).toBeDefined();
  });

  it('should export wallet helpers', async () => {
    const mod = await import('../../index');
    expect(typeof mod.createWallet).toBe('function');
    expect(typeof mod.getWalletByPrivateKey).toBe('function');
  });

  it('should export account functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.checkAccount).toBe('function');
    expect(typeof mod.prepareAuthFlow).toBe('function');
    expect(typeof mod.getGuardianList).toBe('function');
    expect(typeof mod.getHolderInfo).toBe('function');
    expect(typeof mod.getChainInfo).toBe('function');
    expect(typeof mod.getChainInfoByChainId).toBe('function');
  });

  it('should export asset functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.getTokenBalance).toBe('function');
    expect(typeof mod.getTokenList).toBe('function');
    expect(typeof mod.getNftCollections).toBe('function');
    expect(typeof mod.getNftItems).toBe('function');
    expect(typeof mod.getTokenPrice).toBe('function');
  });

  it('should export transfer security functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.checkTransferSecurity).toBe('function');
    expect(typeof mod.checkTransferLimit).toBe('function');
    expect(typeof mod.transferPreflight).toBe('function');
  });

  it('should export contract functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.callContractViewMethod).toBe('function');
    expect(typeof mod.callCaViewMethod).toBe('function');
    expect(typeof mod.managerForwardCall).toBe('function');
    expect(typeof mod.managerForwardCallWithKey).toBe('function');
  });

  it('should export auth functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.getVerifierServer).toBe('function');
    expect(typeof mod.sendVerificationCode).toBe('function');
    expect(typeof mod.verifyCode).toBe('function');
    expect(typeof mod.registerWallet).toBe('function');
    expect(typeof mod.recoverWallet).toBe('function');
    expect(typeof mod.recoverAndSaveWallet).toBe('function');
    expect(typeof mod.checkRegisterOrRecoveryStatus).toBe('function');
  });

  it('should export transfer functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.sameChainTransfer).toBe('function');
    expect(typeof mod.crossChainTransfer).toBe('function');
    expect(typeof mod.getTransactionResult).toBe('function');
    expect(typeof mod.checkManagerSyncState).toBe('function');
  });

  it('should export guardian functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.addGuardian).toBe('function');
    expect(typeof mod.removeGuardian).toBe('function');
  });

  it('should export utility functions', async () => {
    const mod = await import('../../index');
    expect(typeof mod.getApprovalCount).toBe('function');
    expect(typeof mod.listWalletProfiles).toBe('function');
    expect(typeof mod.getWalletProfileByLoginEmail).toBe('function');
    expect(typeof mod.resolveManagerWallet).toBe('function');
  });
});
