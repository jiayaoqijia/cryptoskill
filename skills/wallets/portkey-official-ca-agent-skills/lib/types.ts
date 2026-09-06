// ============================================================================
// Network & Config
// ============================================================================

export type NetworkType = 'mainnet';

export type ChainId = 'AELF' | 'tDVV';

export interface PortkeyConfig {
  /** Portkey backend API base URL */
  apiUrl: string;
  /** Portkey EOA backend API base URL (for asset fallback) */
  eoaApiUrl: string;
  /** GraphQL / Indexer URL */
  graphqlUrl: string;
  /** Network type */
  network: NetworkType;
  /** Enable or disable AA->EOA fallback in token-list auto mode */
  eoaFallbackEnabled: boolean;
  /** Maximum EOA fallback attempts (including the first attempt) */
  eoaFallbackRetryCount: number;
  /** Delay between EOA fallback retries in milliseconds */
  eoaFallbackRetryDelayMs: number;
}

export interface NetworkDefaults {
  apiUrl: string;
  eoaApiUrl: string;
  graphqlUrl: string;
  eoaFallbackEnabled: boolean;
  eoaFallbackRetryCount: number;
  eoaFallbackRetryDelayMs: number;
}

// ============================================================================
// Chain Info (fetched dynamically from API)
// ============================================================================

export interface DefaultToken {
  name: string;
  address: string;
  imageUrl: string;
  symbol: string;
  decimals: number;
}

export interface ChainInfo {
  chainId: ChainId;
  chainName: string;
  endPoint: string;
  explorerUrl: string;
  caContractAddress: string;
  defaultToken: DefaultToken;
}

// ============================================================================
// Guardian & Verifier
// ============================================================================

export enum LoginType {
  Email = 0,
  Phone = 1,
  Google = 2,
  Apple = 3,
  Telegram = 4,
  Twitter = 5,
  Facebook = 6,
}

export const LoginTypeLabel: Record<LoginType, string> = {
  [LoginType.Email]: 'Email',
  [LoginType.Phone]: 'Phone',
  [LoginType.Google]: 'Google',
  [LoginType.Apple]: 'Apple',
  [LoginType.Telegram]: 'Telegram',
  [LoginType.Twitter]: 'Twitter',
  [LoginType.Facebook]: 'Facebook',
};

export interface GuardianItem {
  guardianIdentifier: string;
  identifierHash: string;
  isLoginGuardian: boolean;
  salt: string;
  type: LoginType;
  verifierId: string;
  thirdPartyEmail?: string;
  isPrivate?: boolean;
  firstName?: string;
  lastName?: string;
}

export interface VerifierItem {
  id: string;
  name: string;
  imageUrl: string;
}

// ============================================================================
// Operation Types
// ============================================================================

/**
 * Operation types matching the on-chain CA contract's `caimpl.OperationType` enum.
 *
 * IMPORTANT: These values were updated to match the mainnet chain contract.
 * The backend API rejects operationType 0 (Unknown).
 *
 * Chain protobuf: caimpl.OperationType
 */
export enum OperationType {
  Unknown = 0,
  /** Used for registration (sendVerificationCode + verifyCode for register flow) */
  CreateCAHolder = 1,
  /** Used for login / social recovery (sendVerificationCode + verifyCode for recovery flow) */
  SocialRecovery = 2,
  AddGuardian = 3,
  RemoveGuardian = 4,
  UpdateGuardian = 5,
  RemoveOtherManagerInfo = 6,
  SetLoginAccount = 7,
  Approve = 8,
  ModifyTransferLimit = 9,
  GuardianApproveTransfer = 10,
  UnsetLoginAccount = 11,
}

// ============================================================================
// Verification
// ============================================================================

export interface SendVerificationCodeParams {
  /** Guardian identifier (email address) */
  email: string;
  /** Verifier service ID */
  verifierId: string;
  /** Target chain ID */
  chainId: ChainId;
  /** Operation type */
  operationType: OperationType;
}

export interface SendVerificationCodeResult {
  verifierSessionId: string;
}

export interface VerifyCodeParams {
  /** Guardian identifier (email address) */
  email: string;
  /** 6-digit verification code */
  verificationCode: string;
  /** Verifier service ID */
  verifierId: string;
  /** Session ID from sendVerificationCode */
  verifierSessionId: string;
  /** Target chain ID */
  chainId: ChainId;
  /** Operation type */
  operationType: OperationType;
}

export interface VerifyCodeResult {
  signature: string;
  verificationDoc: string;
}

// ============================================================================
// Registration & Recovery
// ============================================================================

export interface RegisterParams {
  /** Email address */
  email: string;
  /** Manager wallet address */
  manager: string;
  /** Verifier service ID */
  verifierId: string;
  /** Verification document from verifier */
  verificationDoc: string;
  /** Signature from verifier */
  signature: string;
  /** Origin chain ID */
  chainId: ChainId;
  /** Encoded device/extra data */
  extraData?: string;
  /** Context for tracking */
  context?: { clientId: string; requestId: string };
}

export interface RecoverParams {
  /** Email address */
  email: string;
  /** Manager wallet address */
  manager: string;
  /** Array of approved guardians with their verification proofs */
  guardiansApproved: RecoveryApprovedGuardian[];
  /** Origin chain ID */
  chainId: ChainId;
  /** Encoded device/extra data */
  extraData?: string;
  /** Context for tracking */
  context?: { clientId: string; requestId: string };
}

export interface ApprovedGuardian {
  /** Guardian identifier (email, phone, social ID) */
  identifier?: string;
  /** Hash of the identifier */
  identifierHash?: string;
  /** Guardian type */
  type: LoginType | number | string;
  /** Verifier service ID */
  verifierId: string;
  /** Verification document */
  verificationDoc: string;
  /** Signature from verifier */
  signature: string;
}

/**
 * Recovery requires full guardian proofs with plain identifier.
 */
export interface RecoveryApprovedGuardian extends ApprovedGuardian {
  /** Guardian identifier (email, phone, social ID) */
  identifier: string;
}

export interface RegisterOrRecoverResult {
  sessionId: string;
}

export type StatusCheckType = 'register' | 'recovery';

export interface StatusCheckResult {
  /** Current status: pass, pending, fail */
  status: 'pass' | 'pending' | 'fail';
  /** CA address (available when status is 'pass') */
  caAddress?: string;
  /** CA hash (available when status is 'pass') */
  caHash?: string;
  /** Error message (available when status is 'fail') */
  failMessage?: string;
}

// ============================================================================
// CA Holder Info
// ============================================================================

export interface ManagerInfo {
  address: string;
  extraData: string;
}

export interface HolderInfo {
  caHash: string;
  caAddress: string;
  guardianList: {
    guardians: GuardianItem[];
  };
  managerInfos: ManagerInfo[];
}

// ============================================================================
// Assets
// ============================================================================

export interface CaAddressInfo {
  chainId: ChainId;
  caAddress: string;
}

export interface TokenBalanceParams {
  /** CA address on the specific chain */
  caAddress: string;
  /** Chain ID */
  chainId: ChainId;
  /** Token symbol (e.g., 'ELF') */
  symbol: string;
}

export interface TokenBalanceResult {
  symbol: string;
  balance: string;
  decimals: number;
  tokenContractAddress: string;
}

export interface TokenListParams {
  /** Array of CA address info across chains */
  caAddressInfos: CaAddressInfo[];
  /** Query strategy: aa only, eoa only, or auto(aa then eoa fallback on 401) */
  strategy?: TokenListStrategy;
  /** Skip count for pagination */
  skipCount?: number;
  /** Max result count */
  maxResultCount?: number;
}

export type TokenListStrategy = 'aa' | 'auto' | 'eoa';
export type TokenListDataSource = 'aa' | 'eoa-fallback' | 'eoa-direct';

export interface TokenItem {
  chainId: ChainId;
  symbol: string;
  decimals: number;
  tokenContractAddress: string;
  balance: string;
  balanceInUsd: string;
  imageUrl: string;
  price: number;
  tokenName: string;
}

export interface TokenListResult {
  data: TokenItem[];
  totalRecordCount: number;
  /** Data source used for this response */
  dataSource?: TokenListDataSource;
}

export interface NftCollectionParams {
  caAddressInfos: CaAddressInfo[];
  skipCount?: number;
  maxResultCount?: number;
}

export interface NftCollectionItem {
  chainId: ChainId;
  collectionName: string;
  imageUrl: string;
  itemCount: number;
  symbol: string;
}

export interface NftCollectionResult {
  data: NftCollectionItem[];
  totalRecordCount: number;
}

export interface NftItemParams {
  caAddressInfos: CaAddressInfo[];
  symbol: string;
  skipCount?: number;
  maxResultCount?: number;
}

export interface NftItem {
  chainId: ChainId;
  symbol: string;
  alias: string;
  balance: string;
  tokenContractAddress: string;
  imageLargeUrl: string;
  imageUrl: string;
  tokenId: string;
  totalSupply: string;
  collectionName: string;
  collectionSymbol: string;
  inscriptionName?: string;
}

export interface NftItemResult {
  data: NftItem[];
  totalRecordCount: number;
}

export interface TokenPriceParams {
  /** Array of token symbols */
  symbols: string[];
}

export interface TokenPriceItem {
  symbol: string;
  priceInUsd: number;
}

// ============================================================================
// Transfer Security / Preflight
// ============================================================================

export interface AccelerateGuardian {
  type: LoginType | number | string;
  verifierId: string;
  identifierHash: string;
  salt: string;
  isLoginAccount: boolean;
  transactionId: string;
  chainId: ChainId;
}

export interface TransferSecurityCheckParams {
  caHash: string;
  chainId: ChainId;
}

export interface TransferSecurityCheckResult {
  isTransferSafe: boolean;
  isSynchronizing: boolean;
  isOriginChainSafe: boolean;
  accelerateGuardians: AccelerateGuardian[];
}

export interface TransferLimitCheckParams {
  caHash: string;
  caAddress: string;
  symbol: string;
  amount: string;
  chainId: ChainId;
}

export interface TransferLimitCheckResult {
  symbol: string;
  chainId: ChainId;
  amount: string;
  balance: string;
  decimals: number;
  tokenContractAddress: string;
  feeSymbol: string;
  feeBalance: string;
  feeDecimals: number;
  feeTokenContractAddress: string;
  dailyLimit: string | null;
  dailyBalance: string | null;
  singleLimit: string | null;
  defaultDailyLimit: string | null;
  defaultSingleLimit: string | null;
  isDailyLimited: boolean;
  isSingleLimited: boolean;
  canApprove: boolean;
  feeBuffer: string;
}

export type TransferPreflightDecision =
  | 'direct_transfer'
  | 'needs_add_guardian'
  | 'needs_security_sync'
  | 'needs_one_time_approval'
  | 'needs_limit_modification';

export interface TransferPreflightParams extends TransferLimitCheckParams {}

export interface TransferPreflightResult {
  decision: TransferPreflightDecision;
  reason: string;
  walletSecurity: TransferSecurityCheckResult;
  transferLimit?: TransferLimitCheckResult;
}

// ============================================================================
// Transfer
// ============================================================================

export interface ManagerSyncCheckParams {
  /** CA hash */
  caHash: string;
  /** Chain ID where the CA write operation will be sent */
  chainId: ChainId;
  /** Manager wallet address */
  managerAddress: string;
}

export interface ManagerSyncCheckResult {
  caHash: string;
  chainId: ChainId;
  managerAddress: string;
  caAddress: string;
  isManagerSynced: boolean;
  managerInfos: ManagerInfo[];
}

export interface TransactionFeePreview {
  transactionFee: Record<string, string> | null;
  transactionFees: Record<string, unknown> | null;
  chargingAddress: string | null;
  isCaPayingFee: boolean | null;
  feeSymbol: string | null;
  feeAmount: string | null;
}

export interface TransferParams {
  /** CA hash */
  caHash: string;
  /** Token contract address on the chain */
  tokenContractAddress: string;
  /** Token symbol */
  symbol: string;
  /** Recipient address */
  to: string;
  /** Amount (in smallest unit, e.g., 1 ELF = 100000000) */
  amount: string;
  /** Optional memo */
  memo?: string;
  /** Chain ID where the transfer happens */
  chainId: ChainId;
  /** Optional guardian approvals for one-time transfer approval */
  guardiansApproved?: ApprovedGuardian[];
}

export interface CrossChainTransferParams extends TransferParams {
  /** Target chain ID */
  toChainId: ChainId;
  /** Token issue chain ID (numeric) */
  issueChainId?: number;
}

export interface TransferResult {
  transactionId: string;
  status: string;
  feePreview?: TransactionFeePreview;
}

// ============================================================================
// Guardian Management
// ============================================================================

export interface GuardianVerificationInfo {
  id: string;
  signature: string;
  verificationDoc: string;
}

export interface GuardianToAdd {
  identifierHash: string;
  type: LoginType | number;
  verificationInfo: GuardianVerificationInfo;
}

export interface GuardianToRemove {
  identifierHash: string;
  type: LoginType | number;
  verificationInfo: {
    id: string;
  };
}

export interface AddGuardianParams {
  caHash: string;
  guardianToAdd: GuardianToAdd;
  guardiansApproved: ApprovedGuardian[];
  chainId: ChainId;
}

export interface RemoveGuardianParams {
  caHash: string;
  guardianToRemove: GuardianToRemove;
  guardiansApproved: ApprovedGuardian[];
  chainId: ChainId;
}

// ============================================================================
// Generic Contract Call
// ============================================================================

export interface ManagerForwardCallParams {
  caHash: string;
  contractAddress: string;
  methodName: string;
  args: Record<string, unknown>;
  chainId: ChainId;
  /** Optional guardian approvals for transfer-related ManagerForwardCall flows */
  guardiansApproved?: ApprovedGuardian[];
  /** Optional pre-fetched manager sync result to avoid duplicate holder lookups */
  managerSync?: ManagerSyncCheckResult;
}

export interface RecoverAndSaveWalletParams {
  email: string;
  guardiansApproved: RecoveryApprovedGuardian[];
  chainId: ChainId;
  password: string;
  network: NetworkType;
  loginEmail?: string;
  extraData?: string;
  maxStatusChecks?: number;
  statusCheckDelayMs?: number;
}

export interface RecoverAndSaveWalletResult {
  sessionId: string;
  status: 'pass';
  caAddress: string;
  caHash: string;
  keystorePath: string;
  managerAddress: string;
  originChainId: ChainId;
  loginEmail: string | null;
}

export interface ViewMethodParams {
  /** RPC endpoint URL */
  rpcUrl: string;
  /** Contract address */
  contractAddress: string;
  /** Method name */
  methodName: string;
  /** Method parameters */
  params?: Record<string, unknown>;
}

// ============================================================================
// Transaction Result
// ============================================================================

export interface TransactionResultParams {
  /** Transaction ID */
  txId: string;
  /** Chain ID */
  chainId: ChainId;
}

export interface TransactionResult {
  TransactionId: string;
  Status: string;
  Logs: Array<{
    Address: string;
    Name: string;
    Indexed: string[];
    NonIndexed: string;
  }>;
  BlockNumber: number;
  BlockHash: string;
  ReturnValue: string;
  Error: string | null;
}

// ============================================================================
// Wallet
// ============================================================================

export interface WalletInfo {
  address: string;
  privateKey: string;
  mnemonic?: string;
}

// ============================================================================
// Utility: approval count calculation
// ============================================================================

/**
 * Calculate the number of guardian approvals required.
 * - guardianCount <= 3: all guardians required
 * - guardianCount > 3: Math.floor(count * 3/5) + 1
 */
export function getApprovalCount(guardianCount: number): number {
  if (guardianCount <= 3) return guardianCount;
  return Math.floor((guardianCount * 3) / 5) + 1;
}
