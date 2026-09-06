export type ChainId = 'AELF' | 'tDVV' | 'tDVW';

export type ExecutionMode = 'simulate' | 'send';
export type SignerMode = 'auto' | 'explicit' | 'context' | 'env' | 'daemon';
export type SignerProvider = 'explicit' | 'context' | 'env' | 'daemon';

export type SignerContextInput = {
  signerMode?: SignerMode;
  walletType?: 'EOA' | 'CA';
  address?: string;
  password?: string;
  privateKey?: string;
  caHash?: string;
  caAddress?: string;
  network?: 'mainnet' | 'testnet';
};

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonObject | JsonValue[];
export interface JsonObject {
  [key: string]: JsonValue | unknown;
}

export interface PagedResponse<T = JsonObject> extends JsonObject {
  items?: T[];
  totalCount?: number;
  skipCount?: number;
  maxResultCount?: number;
}

export interface ChainSimulatePayload extends JsonObject {
  chainId: ChainId;
  contractAddress: string;
  methodName: string;
  args?: unknown;
}

export interface EnvConfig {
  apiBase: string;
  authBase: string;
  defaultDaoChain: ChainId;
  defaultNetworkChain: ChainId;
  authChainId: ChainId;
  source: string;
  caHash?: string;
  privateKey?: string;
  httpTimeoutMs: number;
  httpRetryMax: number;
  httpRetryBaseMs: number;
  httpRetryPost: boolean;
  aelfCacheMax: number;
  rpc: Record<ChainId, string>;
}

export interface TxReceipt {
  txId: string;
  status: string;
  logs?: unknown[];
  explorerUrl?: string;
}

export interface ToolError {
  code: string;
  message: string;
  details?: unknown;
}

export interface ToolResult<T> {
  success: boolean;
  data?: T;
  error?: ToolError;
  traceId?: string;
  tx?: TxReceipt;
}

export interface SendOptions {
  mode?: ExecutionMode;
  waitForMined?: boolean;
  traceId?: string;
  signer?: SignerContextInput;
  signerContext?: SignerContextInput;
  privateKey?: string;
}

export interface ChainCallInput {
  chainId: ChainId;
  contractAddress: string;
  methodName: string;
  args?: unknown;
}

export interface AuthToken {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
  expiresAt: number;
}

export interface ApiResponse<T> {
  code: string;
  message?: string;
  data: T;
}

export interface SignaturePayload {
  timestamp: number;
  address: string;
  publicKey: string;
  signature: string;
}

export interface WithAuth {
  auth?: boolean;
}
