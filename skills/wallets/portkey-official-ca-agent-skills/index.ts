// ============================================================================
// @portkey/ca-agent-skills — SDK Entry
//
// Pure re-exports. Zero logic.
// ============================================================================

// --- Config ---
export { getConfig, NETWORK_DEFAULTS } from './lib/config.js';

// --- Types ---
export type {
  NetworkType,
  PortkeyConfig,
  ChainId,
  ChainInfo,
  DefaultToken,
  LoginType,
  GuardianItem,
  VerifierItem,
  OperationType,
  WalletInfo,
  HolderInfo,
  ManagerInfo,
  // Verification
  SendVerificationCodeParams,
  SendVerificationCodeResult,
  VerifyCodeParams,
  VerifyCodeResult,
  // Registration & Recovery
  RegisterParams,
  RecoverParams,
  ApprovedGuardian,
  RecoveryApprovedGuardian,
  RegisterOrRecoverResult,
  StatusCheckType,
  StatusCheckResult,
  // Assets
  CaAddressInfo,
  TokenBalanceParams,
  TokenBalanceResult,
  TokenListParams,
  TokenListStrategy,
  TokenListDataSource,
  TokenListResult,
  TokenItem,
  NftCollectionParams,
  NftCollectionResult,
  NftCollectionItem,
  NftItemParams,
  NftItemResult,
  NftItem,
  TokenPriceParams,
  TokenPriceItem,
  AccelerateGuardian,
  TransferSecurityCheckParams,
  TransferSecurityCheckResult,
  TransferLimitCheckParams,
  TransferLimitCheckResult,
  TransferPreflightParams,
  TransferPreflightDecision,
  TransferPreflightResult,
  ManagerSyncCheckParams,
  ManagerSyncCheckResult,
  TransactionFeePreview,
  // Transfer
  TransferParams,
  CrossChainTransferParams,
  TransferResult,
  // Guardian management
  GuardianToAdd,
  GuardianToRemove,
  AddGuardianParams,
  RemoveGuardianParams,
  GuardianVerificationInfo,
  // Contract
  ManagerForwardCallParams,
  RecoverAndSaveWalletParams,
  RecoverAndSaveWalletResult,
  ViewMethodParams,
  TransactionResultParams,
  TransactionResult,
} from './lib/types.js';

export { getApprovalCount } from './lib/types.js';

// --- Wallet helpers ---
export { createWallet, getWalletByPrivateKey } from './lib/aelf-client.js';

// --- HTTP utilities ---
export { HttpError, validateRpcUrl } from './lib/http.js';

// --- Core: Account ---
export {
  checkAccount,
  getGuardianList,
  getHolderInfo,
  getChainInfo,
  getChainInfoByChainId,
  prepareAuthFlow,
  clearChainInfoCache,
} from './src/core/account.js';

// --- Core: Assets ---
export {
  getTokenBalance,
  getTokenList,
  getNftCollections,
  getNftItems,
  getTokenPrice,
} from './src/core/assets.js';

// --- Core: Security / Preflight ---
export {
  checkTransferSecurity,
  checkTransferLimit,
  transferPreflight,
} from './src/core/security.js';

// --- Core: Contract ---
export {
  callContractViewMethod,
  callCaViewMethod,
  managerForwardCall,
  managerForwardCallWithKey,
} from './src/core/contract.js';

// --- Core: Auth (Phase 2) ---
export {
  getVerifierServer,
  sendVerificationCode,
  verifyCode,
  registerWallet,
  recoverWallet,
  checkRegisterOrRecoveryStatus,
} from './src/core/auth.js';
export { recoverAndSaveWallet } from './src/core/auth-session.js';

// --- Core: Transfer (Phase 3) ---
export {
  sameChainTransfer,
  crossChainTransfer,
  recoverStuckTransfer,
  getTransactionResult,
} from './src/core/transfer.js';
export { checkManagerSyncState } from './src/core/manager-sync.js';

// --- Core: Guardian (Phase 3) ---
export {
  addGuardian,
  removeGuardian,
} from './src/core/guardian.js';

// --- Core: Keystore (wallet persistence) ---
export {
  saveKeystore,
  unlockWallet,
  lockWallet,
  getWalletStatus,
  getUnlockedWallet,
  getKeystorePath,
  listWalletProfiles,
  getWalletProfileByLoginEmail,
  clearKeystoreState,
  resolveManagerWallet,
  createSignerFromCaWallet,
  resolveSignerContext,
  getActiveWallet,
  setActiveWallet,
} from './src/core/keystore.js';

// --- AelfSigner integration (for use with awaken/eforest DApp skills) ---
export type { AelfSigner } from '@portkey/aelf-signer';
export {
  createCaSigner,
  createSignerFromEnv,
  CaSigner,
} from '@portkey/aelf-signer';

export type {
  SignerMode,
  SignerProvider,
  SignerContextInput,
  WalletType,
  WalletSource,
  ActiveWalletProfile,
  WalletContextFile,
} from './lib/wallet-context.js';
export {
  readWalletContext,
  writeWalletContext,
  getActiveWalletProfile,
  setActiveWalletProfile,
} from './lib/wallet-context.js';
