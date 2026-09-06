#!/usr/bin/env bun
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import packageJson from '../../package.json';
import { getConfig } from '../../lib/config.js';
import { createWallet } from '../../lib/aelf-client.js';
import { validateRpcUrl } from '../../lib/http.js';
import { LoginType, OperationType } from '../../lib/types.js';
import { fail } from './error.js';
import { requireWallet } from './require-wallet.js';

// Core functions
import {
  checkAccount,
  getGuardianList,
  getHolderInfo,
  getChainInfo,
  prepareAuthFlow,
} from '../core/account.js';
import { getTokenBalance, getTokenList, getNftCollections, getNftItems, getTokenPrice } from '../core/assets.js';
import { getVerifierServer, sendVerificationCode, verifyCode, registerWallet, recoverWallet, checkRegisterOrRecoveryStatus } from '../core/auth.js';
import { recoverAndSaveWallet } from '../core/auth-session.js';
import { sameChainTransfer, crossChainTransfer, recoverStuckTransfer, getTransactionResult } from '../core/transfer.js';
import { checkManagerSyncState } from '../core/manager-sync.js';
import { addGuardian, removeGuardian } from '../core/guardian.js';
import { callContractViewMethod, managerForwardCallWithKey } from '../core/contract.js';
import { transferPreflight } from '../core/security.js';
import {
  saveKeystore,
  unlockWallet,
  lockWallet,
  getWalletStatus,
  getActiveWallet,
  setActiveWallet,
  listWalletProfiles,
} from '../core/keystore.js';
import { SkillError } from '../core/errors.js';

// ---------------------------------------------------------------------------
// Server setup
// ---------------------------------------------------------------------------

const server = new McpServer({
  name: 'ca-agent-skills',
  version: packageJson.version,
});

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const CHAIN_ID = z.enum(['AELF', 'tDVV']).describe('aelf chain ID');
const NETWORK = z.literal('mainnet').default('mainnet').describe('Portkey network (mainnet only)');
const LOGIN_EMAIL = z.string().email().describe('Login email associated with the CA account');
const PASSWORD = z.string().min(1).describe('Keystore password for this operation');
const KEYSTORE_FILE = z.string().describe('Absolute path to a CA keystore file');
const JSON_PREVIEW_MAX_CHARS = 200;

function ok(data: unknown) {
  return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
}

/** Parse a JSON string and validate against a zod schema. */
function parseJson<S extends z.ZodTypeAny>(raw: string, schema: S, label: string): z.infer<S> {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new SkillError('INVALID_PARAMS', `Invalid JSON for ${label}: ${raw.slice(0, JSON_PREVIEW_MAX_CHARS)}`);
  }
  return schema.parse(parsed);
}

const READ_ONLY_ANNOTATIONS = {
  readOnlyHint: true,
  read_only_hint: true,
} as const;

const LOCAL_WRITE_ANNOTATIONS = {
  destructiveHint: true,
  destructive_hint: true,
} as const;

const NETWORK_WRITE_ANNOTATIONS = {
  destructiveHint: true,
  destructive_hint: true,
  openWorldHint: true,
  side_effects_hint: true,
} as const;

const READ_ONLY_TOOLS = new Set([
  'portkey_check_account',
  'portkey_get_guardian_list',
  'portkey_get_holder_info',
  'portkey_manager_sync_status',
  'portkey_get_chain_info',
  'portkey_prepare_auth_flow',
  'portkey_get_verifier',
  'portkey_check_status',
  'portkey_balance',
  'portkey_token_list',
  'portkey_nft_collections',
  'portkey_nft_items',
  'portkey_token_price',
  'portkey_tx_result',
  'portkey_transfer_preflight',
  'portkey_view_call',
  'portkey_wallet_status',
  'portkey_list_wallet_profiles',
  'portkey_get_active_wallet',
]);

const LOCAL_WRITE_TOOLS = new Set([
  'portkey_create_wallet',
  'portkey_save_keystore',
  'portkey_unlock',
  'portkey_lock',
  'portkey_set_active_wallet',
]);

const NETWORK_WRITE_TOOLS = new Set([
  'portkey_send_code',
  'portkey_verify_code',
  'portkey_register',
  'portkey_recover',
  'portkey_recover_and_save',
  'portkey_transfer',
  'portkey_cross_chain_transfer',
  'portkey_recover_stuck_transfer',
  'portkey_add_guardian',
  'portkey_remove_guardian',
  'portkey_forward_call',
]);

function getToolAnnotations(name: string) {
  if (READ_ONLY_TOOLS.has(name)) return READ_ONLY_ANNOTATIONS;
  if (LOCAL_WRITE_TOOLS.has(name)) return LOCAL_WRITE_ANNOTATIONS;
  if (NETWORK_WRITE_TOOLS.has(name)) return NETWORK_WRITE_ANNOTATIONS;
  return undefined;
}

const baseRegisterTool = (server.registerTool as any).bind(server);
(server as any).registerTool = (name: string, definition: any, handler: any) =>
  baseRegisterTool(
    name,
    {
      ...definition,
      annotations: getToolAnnotations(name),
    },
    handler,
  );

// ---------------------------------------------------------------------------
// Shared zod schemas for JSON string inputs
// ---------------------------------------------------------------------------

const CaAddressInfoSchema = z.array(z.object({
  chainId: CHAIN_ID,
  caAddress: z.string(),
}));

const TokenListStrategySchema = z.enum(['aa', 'auto', 'eoa']).default('auto');

const GuardianApprovedSchema = z.array(z.object({
  identifier: z.string().optional(),
  identifierHash: z.string().optional(),
  type: z.union([z.string(), z.number()]).default(0),
  verifierId: z.string(),
  verificationDoc: z.string(),
  signature: z.string(),
}));

const RecoveryGuardianApprovedSchema = z.array(z.object({
  identifier: z.string().min(1),
  type: z.union([z.string(), z.number()]),
  verifierId: z.string().min(1),
  verificationDoc: z.string().min(1),
  signature: z.string().min(1),
}));

const GuardianToAddSchema = z.object({
  identifierHash: z.string(),
  type: z.number(),
  verificationInfo: z.object({
    id: z.string(),
    signature: z.string(),
    verificationDoc: z.string(),
  }),
});

const GuardianToRemoveSchema = z.object({
  identifierHash: z.string(),
  type: z.number(),
  verificationInfo: z.object({
    id: z.string(),
  }),
});

const OPERATION_TYPE_MAP = {
  register: OperationType.CreateCAHolder,
  recovery: OperationType.SocialRecovery,
  transferApprove: OperationType.GuardianApproveTransfer,
  guardianApproveTransfer: OperationType.GuardianApproveTransfer,
  addGuardian: OperationType.AddGuardian,
  deleteGuardian: OperationType.RemoveGuardian,
} as const;

// ---------------------------------------------------------------------------
// 1. portkey_check_account
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_check_account',
  {
    description: 'Check if an email address is registered in Portkey. Use when you need to determine whether a user has an existing Portkey CA wallet. Returns isRegistered boolean and originChainId.',
    inputSchema: {
      email: z.string().email().describe('Email address to check'),
      network: NETWORK,
    },
  },
  async ({ email, network }) => {
    try {
      return ok(await checkAccount(getConfig({ network }), { email }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 2. portkey_prepare_auth_flow
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_prepare_auth_flow',
  {
    description: 'Prepare the recommended auth flow for an email account. Use this before register/recovery to discover recommendedFlow and resolvedChainId. Existing accounts stay on originChainId; new accounts default to tDVV unless an explicit override is provided.',
    inputSchema: {
      email: z.string().email().describe('Email address to prepare auth flow for'),
      chainId: CHAIN_ID.optional(),
      network: NETWORK,
    },
  },
  async ({ email, chainId, network }) => {
    try {
      const config = getConfig({ network });
      return ok(await prepareAuthFlow(config, {
        email,
        chainId,
        network: config.network,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 3. portkey_get_guardian_list
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_get_guardian_list',
  {
    description: 'Get all guardians associated with an account on an explicit chain. Prefer portkey_prepare_auth_flow when the chain is not already known.',
    inputSchema: {
      identifier: z.string().describe('Guardian identifier (email, phone, or social user ID)'),
      chainId: CHAIN_ID.describe('Explicit chain ID for the guardian query'),
      network: NETWORK,
    },
  },
  async ({ identifier, chainId, network }) => {
    try {
      return ok(await getGuardianList(getConfig({ network }), { identifier, chainId }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 4. portkey_get_holder_info
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_get_holder_info',
  {
    description: 'Get CA holder info directly from the blockchain. Use when you need authoritative on-chain data about a wallet including guardian list, manager list, and CA address. Returns HolderInfo with caHash, caAddress, guardians, and managers.',
    inputSchema: {
      caHash: z.string().describe('CA hash identifier'),
      chainId: CHAIN_ID,
      network: NETWORK,
    },
  },
  async ({ caHash, chainId, network }) => {
    try {
      return ok(await getHolderInfo(getConfig({ network }), { caHash, chainId }));
    } catch (err) { return fail(err); }
  },
);

server.registerTool(
  'portkey_manager_sync_status',
  {
    description: 'Check whether the current manager address has synced to the CA holder on the target chain. Use this before forward-call or claim flows on a different write chain such as tDVV.',
    inputSchema: {
      caHash: z.string().describe('CA hash'),
      chainId: CHAIN_ID.describe('Target chain ID where the write will be sent'),
      managerAddress: z.string().describe('Manager wallet address to check'),
      network: NETWORK,
    },
  },
  async ({ caHash, chainId, managerAddress, network }) => {
    try {
      return ok(await checkManagerSyncState(getConfig({ network }), {
        caHash,
        chainId,
        managerAddress,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 5. portkey_get_chain_info
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_get_chain_info',
  {
    description: 'Get chain configuration info including RPC endpoints, CA contract addresses, and default tokens. Use when you need chain-specific configuration to make contract calls or transfers. Returns array of ChainInfo objects.',
    inputSchema: {
      network: NETWORK,
    },
  },
  async ({ network }) => {
    try {
      return ok(await getChainInfo(getConfig({ network })));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 5. portkey_send_code
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_send_code',
  {
    description: 'Send a verification code to an email address. Requires an explicit resolved chainId. Call portkey_prepare_auth_flow first, then pass resolvedChainId here.',
    inputSchema: {
      email: z.string().email().describe('Email address to send code to'),
      verifierId: z.string().describe('Verifier service ID from portkey_get_verifier'),
      chainId: CHAIN_ID.describe('Resolved chain ID from portkey_prepare_auth_flow'),
      operationType: z.enum(['register', 'recovery', 'transferApprove', 'guardianApproveTransfer', 'addGuardian', 'deleteGuardian']).describe('Operation requiring verification'),
      network: NETWORK,
    },
  },
  async ({ email, verifierId, chainId, operationType, network }) => {
    try {
      return ok(await sendVerificationCode(getConfig({ network }), {
        email, verifierId, chainId, operationType: OPERATION_TYPE_MAP[operationType],
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 6. portkey_verify_code
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_verify_code',
  {
    description: 'Verify a 6-digit code sent to an email. Requires an explicit resolved chainId from portkey_prepare_auth_flow. Returns signature and verificationDoc needed for registration or recovery.',
    inputSchema: {
      email: z.string().email().describe('Email address the code was sent to'),
      verificationCode: z.string().length(6).describe('6-digit verification code'),
      verifierId: z.string().describe('Verifier service ID'),
      verifierSessionId: z.string().describe('Session ID from portkey_send_code'),
      chainId: CHAIN_ID.describe('Resolved chain ID from portkey_prepare_auth_flow'),
      operationType: z.enum(['register', 'recovery', 'transferApprove', 'guardianApproveTransfer', 'addGuardian', 'deleteGuardian']).describe('Operation type'),
      network: NETWORK,
    },
  },
  async ({ email, verificationCode, verifierId, verifierSessionId, chainId, operationType, network }) => {
    try {
      return ok(await verifyCode(getConfig({ network }), {
        email,
        verificationCode,
        verifierId,
        verifierSessionId,
        chainId,
        operationType: OPERATION_TYPE_MAP[operationType],
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 7. portkey_get_verifier
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_get_verifier',
  {
    description: 'Get an assigned verifier server for verification operations on an explicit chain. Call portkey_prepare_auth_flow first and pass resolvedChainId here.',
    inputSchema: {
      chainId: CHAIN_ID.describe('Resolved chain ID from portkey_prepare_auth_flow'),
      network: NETWORK,
    },
  },
  async ({ chainId, network }) => {
    try {
      return ok(await getVerifierServer(getConfig({ network }), { chainId }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 8. portkey_register
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_register',
  {
    description: 'Register a new Portkey CA wallet with email. Requires an explicit resolved chainId. Call portkey_prepare_auth_flow first, then pass resolvedChainId here.',
    inputSchema: {
      email: z.string().email().describe('Email address'),
      manager: z.string().describe('Manager wallet address (from createWallet)'),
      verifierId: z.string().describe('Verifier service ID'),
      verificationDoc: z.string().describe('Verification document from portkey_verify_code'),
      signature: z.string().describe('Signature from portkey_verify_code'),
      chainId: CHAIN_ID.describe('Resolved chain ID from portkey_prepare_auth_flow'),
      network: NETWORK,
    },
  },
  async ({ email, manager, verifierId, verificationDoc, signature, chainId, network }) => {
    try {
      return ok(await registerWallet(getConfig({ network }), {
        email, manager, verifierId, verificationDoc, signature, chainId,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 9. portkey_recover
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_recover',
  {
    description: 'Recover (login to) an existing Portkey CA wallet. Requires an explicit resolved chainId. Call portkey_prepare_auth_flow first, then pass resolvedChainId here.',
    inputSchema: {
      email: z.string().email().describe('Email address'),
      manager: z.string().describe('New manager wallet address'),
      guardiansApproved: z.string().describe('JSON string of approved guardians array: [{ identifier, type, verifierId, verificationDoc, signature }]'),
      chainId: CHAIN_ID.describe('Resolved chain ID from portkey_prepare_auth_flow'),
      network: NETWORK,
    },
  },
  async ({ email, manager, guardiansApproved, chainId, network }) => {
    try {
      const parsed = parseJson(guardiansApproved, RecoveryGuardianApprovedSchema, 'guardiansApproved');
      return ok(await recoverWallet(getConfig({ network }), {
        email, manager, guardiansApproved: parsed, chainId,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 10. portkey_check_status
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_check_status',
  {
    description: 'Check the status of a registration or recovery request. Use after portkey_register or portkey_recover to poll for completion. Returns status (pass/pending/fail), and caAddress + caHash when status is pass.',
    inputSchema: {
      sessionId: z.string().describe('Session ID from register or recover'),
      type: z.enum(['register', 'recovery']).describe('Request type'),
      network: NETWORK,
    },
  },
  async ({ sessionId, type, network }) => {
    try {
      return ok(await checkRegisterOrRecoveryStatus(getConfig({ network }), { sessionId, type }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 11. portkey_balance
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_balance',
  {
    description: 'Query the token balance of a CA address on a specific chain. Use when you need to check how many tokens a wallet holds. Returns symbol, balance (in smallest unit), decimals, and tokenContractAddress.',
    inputSchema: {
      caAddress: z.string().describe('CA address on the chain'),
      chainId: CHAIN_ID,
      symbol: z.string().describe('Token symbol, e.g. ELF'),
      network: NETWORK,
    },
  },
  async ({ caAddress, chainId, symbol, network }) => {
    try {
      return ok(await getTokenBalance(getConfig({ network }), { caAddress, chainId, symbol }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 12. portkey_token_list
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_token_list',
  {
    description: 'Get all tokens with balances for CA addresses across chains. Default strategy is "auto": query AA first, then fallback to EOA endpoint on 401. Returns tokens plus dataSource for traceability.',
    inputSchema: {
      caAddressInfos: z.string().describe('JSON array of { chainId, caAddress } objects'),
      strategy: TokenListStrategySchema.describe('aa | auto | eoa'),
      network: NETWORK,
    },
  },
  async ({ caAddressInfos, strategy, network }) => {
    try {
      const parsed = parseJson(caAddressInfos, CaAddressInfoSchema, 'caAddressInfos');
      return ok(await getTokenList(getConfig({ network }), { caAddressInfos: parsed, strategy }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 13. portkey_nft_collections
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_nft_collections',
  {
    description: 'Get NFT collections owned by CA addresses. Use to browse NFT holdings. Returns collection names, images, and item counts.',
    inputSchema: {
      caAddressInfos: z.string().describe('JSON array of { chainId, caAddress } objects'),
      network: NETWORK,
    },
  },
  async ({ caAddressInfos, network }) => {
    try {
      const parsed = parseJson(caAddressInfos, CaAddressInfoSchema, 'caAddressInfos');
      return ok(await getNftCollections(getConfig({ network }), { caAddressInfos: parsed }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 14. portkey_nft_items
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_nft_items',
  {
    description: 'Get NFT items within a specific collection. Use to see individual NFTs in a collection. Returns token IDs, images, balances, and metadata.',
    inputSchema: {
      caAddressInfos: z.string().describe('JSON array of { chainId, caAddress } objects'),
      symbol: z.string().describe('Collection symbol'),
      network: NETWORK,
    },
  },
  async ({ caAddressInfos, symbol, network }) => {
    try {
      const parsed = parseJson(caAddressInfos, CaAddressInfoSchema, 'caAddressInfos');
      return ok(await getNftItems(getConfig({ network }), { caAddressInfos: parsed, symbol }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 15. portkey_token_price
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_token_price',
  {
    description: 'Get current token prices in USD. Use to check market prices. Returns array of { symbol, priceInUsd }.',
    inputSchema: {
      symbols: z.string().describe('Comma-separated token symbols, e.g. "ELF,USDT"'),
      network: NETWORK,
    },
  },
  async ({ symbols, network }) => {
    try {
      return ok(await getTokenPrice(getConfig({ network }), { symbols: symbols.split(',').map(s => s.trim()) }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 16. portkey_transfer
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_transfer',
  {
    description: 'Transfer tokens on the same chain. Use when sender and receiver are on the same aelf sidechain. Requires manager private key. Returns transactionId and status.',
    inputSchema: {
      caHash: z.string().describe('CA hash of the sender wallet'),
      tokenContractAddress: z.string().describe('Token contract address on the chain'),
      symbol: z.string().describe('Token symbol, e.g. ELF'),
      to: z.string().describe('Recipient address'),
      amount: z.string().describe('Amount in smallest unit (e.g. 100000000 = 1 ELF)'),
      memo: z.string().optional().describe('Optional transfer memo'),
      guardiansApproved: z.string().optional().describe('Optional JSON array of approved guardians for one-time transfer approval'),
      chainId: CHAIN_ID,
      loginEmail: LOGIN_EMAIL.optional(),
      password: PASSWORD.optional(),
      keystoreFile: KEYSTORE_FILE.optional(),
      network: NETWORK,
    },
  },
  async ({ caHash, tokenContractAddress, symbol, to, amount, memo, guardiansApproved, chainId, loginEmail, password, keystoreFile, network }) => {
    try {
      const wallet = requireWallet({ network, loginEmail, password, keystoreFile });
      return ok(await sameChainTransfer(getConfig({ network }), wallet, {
        caHash, tokenContractAddress, symbol, to, amount, memo, chainId,
        guardiansApproved: guardiansApproved
          ? parseJson(guardiansApproved, GuardianApprovedSchema, 'guardiansApproved')
          : undefined,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 17. portkey_cross_chain_transfer
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_cross_chain_transfer',
  {
    description: 'Transfer tokens across chains (e.g., tDVV to AELF). Two-step process handled automatically. Requires manager private key. Returns transactionId and status.',
    inputSchema: {
      caHash: z.string().describe('CA hash of the sender wallet'),
      tokenContractAddress: z.string().describe('Token contract address on source chain'),
      symbol: z.string().describe('Token symbol'),
      to: z.string().describe('Recipient address on target chain'),
      amount: z.string().describe('Amount in smallest unit'),
      guardiansApproved: z.string().optional().describe('Optional JSON array of approved guardians for one-time transfer approval'),
      toChainId: CHAIN_ID.describe('Target chain ID'),
      chainId: CHAIN_ID.describe('Source chain ID'),
      loginEmail: LOGIN_EMAIL.optional(),
      password: PASSWORD.optional(),
      keystoreFile: KEYSTORE_FILE.optional(),
      network: NETWORK,
    },
  },
  async ({ caHash, tokenContractAddress, symbol, to, amount, guardiansApproved, toChainId, chainId, loginEmail, password, keystoreFile, network }) => {
    try {
      const wallet = requireWallet({ network, loginEmail, password, keystoreFile });
      return ok(await crossChainTransfer(getConfig({ network }), wallet, {
        caHash, tokenContractAddress, symbol, to, amount, toChainId, chainId,
        guardiansApproved: guardiansApproved
          ? parseJson(guardiansApproved, GuardianApprovedSchema, 'guardiansApproved')
          : undefined,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 18. portkey_tx_result
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_tx_result',
  {
    description: 'Get the result of a blockchain transaction. Use to check if a transaction was mined successfully. Returns full transaction result including status, logs, and block info.',
    inputSchema: {
      txId: z.string().describe('Transaction ID'),
      chainId: CHAIN_ID,
      network: NETWORK,
    },
  },
  async ({ txId, chainId, network }) => {
    try {
      return ok(await getTransactionResult(getConfig({ network }), { txId, chainId }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 19. portkey_transfer_preflight
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_transfer_preflight',
  {
    description: 'Run the CA app transfer preflight checks. Returns whether the transfer can proceed directly, needs one-time approval, needs transfer-limit modification, or is blocked by wallet security.',
    inputSchema: {
      caHash: z.string().describe('CA hash'),
      caAddress: z.string().describe('CA address on the transfer chain'),
      symbol: z.string().describe('Token symbol'),
      amount: z.string().describe('Amount in smallest unit'),
      chainId: CHAIN_ID.describe('Transfer chain ID'),
      network: NETWORK,
    },
  },
  async ({ caHash, caAddress, symbol, amount, chainId, network }) => {
    try {
      return ok(await transferPreflight(getConfig({ network }), {
        caHash,
        caAddress,
        symbol,
        amount,
        chainId,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 20. portkey_recover_stuck_transfer
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_recover_stuck_transfer',
  {
    description: 'Recover tokens stuck on the Manager address after a failed cross-chain transfer. When crossChainTransfer Step 1 (CA→Manager) succeeds but Step 2 fails, tokens remain on the Manager. This tool transfers them back to the CA address.',
    inputSchema: {
      tokenContractAddress: z.string().describe('Token contract address'),
      symbol: z.string().describe('Token symbol (e.g. ELF)'),
      amount: z.string().describe('Amount in smallest unit'),
      caAddress: z.string().describe('CA address to recover tokens to'),
      chainId: CHAIN_ID,
      memo: z.string().optional().describe('Optional memo'),
      loginEmail: LOGIN_EMAIL.optional(),
      password: PASSWORD.optional(),
      keystoreFile: KEYSTORE_FILE.optional(),
      network: NETWORK,
    },
  },
  async ({ tokenContractAddress, symbol, amount, caAddress, chainId, memo, loginEmail, password, keystoreFile, network }) => {
    try {
      const wallet = requireWallet({ network, loginEmail, password, keystoreFile });
      return ok(await recoverStuckTransfer(getConfig({ network }), wallet, {
        tokenContractAddress, symbol, amount, caAddress, chainId, memo,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 21. portkey_add_guardian
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_add_guardian',
  {
    description: 'Add a new guardian to a CA wallet. Requires existing guardian approvals. Use after verifying the new guardian identity and getting approvals from current guardians.',
    inputSchema: {
      caHash: z.string().describe('CA hash'),
      guardianToAdd: z.string().describe('JSON: { identifierHash, type (0=Email), verificationInfo: { id, signature, verificationDoc } }'),
      guardiansApproved: z.string().describe('JSON array of approved guardians'),
      chainId: CHAIN_ID,
      loginEmail: LOGIN_EMAIL.optional(),
      password: PASSWORD.optional(),
      keystoreFile: KEYSTORE_FILE.optional(),
      network: NETWORK,
    },
  },
  async ({ caHash, guardianToAdd, guardiansApproved, chainId, loginEmail, password, keystoreFile, network }) => {
    try {
      const wallet = requireWallet({ network, loginEmail, password, keystoreFile });
      return ok(await addGuardian(getConfig({ network }), wallet, {
        caHash,
        guardianToAdd: parseJson(guardianToAdd, GuardianToAddSchema, 'guardianToAdd'),
        guardiansApproved: parseJson(
          guardiansApproved,
          GuardianApprovedSchema,
          'guardiansApproved',
        ),
        chainId,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 22. portkey_remove_guardian
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_remove_guardian',
  {
    description: 'Remove a guardian from a CA wallet. Requires existing guardian approvals. The guardian must not be the only login guardian.',
    inputSchema: {
      caHash: z.string().describe('CA hash'),
      guardianToRemove: z.string().describe('JSON: { identifierHash, type (0=Email), verificationInfo: { id } }'),
      guardiansApproved: z.string().describe('JSON array of approved guardians'),
      chainId: CHAIN_ID,
      loginEmail: LOGIN_EMAIL.optional(),
      password: PASSWORD.optional(),
      keystoreFile: KEYSTORE_FILE.optional(),
      network: NETWORK,
    },
  },
  async ({ caHash, guardianToRemove, guardiansApproved, chainId, loginEmail, password, keystoreFile, network }) => {
    try {
      const wallet = requireWallet({ network, loginEmail, password, keystoreFile });
      return ok(await removeGuardian(getConfig({ network }), wallet, {
        caHash,
        guardianToRemove: parseJson(guardianToRemove, GuardianToRemoveSchema, 'guardianToRemove'),
        guardiansApproved: parseJson(
          guardiansApproved,
          GuardianApprovedSchema,
          'guardiansApproved',
        ),
        chainId,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 23. portkey_forward_call
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_forward_call',
  {
    description: 'Execute a generic ManagerForwardCall on any contract through the CA wallet. The current manager must already be synced on the target chain; if not, this tool stops before fee preview or transaction send.',
    inputSchema: {
      caHash: z.string().describe('CA hash'),
      contractAddress: z.string().describe('Target contract address'),
      methodName: z.string().describe('Target method name'),
      args: z.string().describe('JSON object of method arguments'),
      guardiansApproved: z.string().optional().describe('Optional JSON array of approved guardians for transfer-related calls'),
      chainId: CHAIN_ID,
      loginEmail: LOGIN_EMAIL.optional(),
      password: PASSWORD.optional(),
      keystoreFile: KEYSTORE_FILE.optional(),
      network: NETWORK,
    },
  },
  async ({ caHash, contractAddress, methodName, args, guardiansApproved, chainId, loginEmail, password, keystoreFile, network }) => {
    try {
      const wallet = requireWallet({ network, loginEmail, password, keystoreFile });
      let parsedArgs: Record<string, unknown>;
      try { parsedArgs = JSON.parse(args); } catch { throw new SkillError('INVALID_PARAMS', `Invalid JSON for "args": ${args.slice(0, JSON_PREVIEW_MAX_CHARS)}`); }
      return ok(await managerForwardCallWithKey(getConfig({ network }), wallet.privateKey, {
        caHash,
        contractAddress,
        methodName,
        args: parsedArgs,
        chainId,
        guardiansApproved: guardiansApproved
          ? parseJson(guardiansApproved, GuardianApprovedSchema, 'guardiansApproved')
          : undefined,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 24. portkey_view_call
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_view_call',
  {
    description: 'Call a read-only (view) method on any contract. Use for querying contract state without signing. No private key needed.',
    inputSchema: {
      rpcUrl: z.string().describe('RPC endpoint URL'),
      contractAddress: z.string().describe('Contract address'),
      methodName: z.string().describe('Method name'),
      params: z.string().optional().describe('JSON object of method parameters'),
      network: NETWORK,
    },
  },
  async ({ rpcUrl, contractAddress, methodName, params, network }) => {
    try {
      validateRpcUrl(rpcUrl);
      let parsedParams: Record<string, unknown> | undefined;
      if (params) { try { parsedParams = JSON.parse(params); } catch { throw new SkillError('INVALID_PARAMS', `Invalid JSON for "params": ${params.slice(0, JSON_PREVIEW_MAX_CHARS)}`); } }
      return ok(await callContractViewMethod(getConfig({ network }), {
        rpcUrl, contractAddress, methodName, params: parsedParams,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// Bonus: portkey_create_wallet
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_create_wallet',
  {
    description: 'Create a new aelf wallet (manager keypair). Use when you need a fresh manager address for registration or recovery. Returns address, privateKey, and mnemonic. IMPORTANT: after registration/recovery succeeds, use portkey_save_keystore to encrypt and persist the wallet.',
  },
  async () => {
    try {
      return ok(createWallet());
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 25. portkey_save_keystore
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_save_keystore',
  {
    description: 'Encrypt and save the Manager wallet to a keystore file (~/.portkey/ca/). Requires an explicit originChainId from portkey_prepare_auth_flow or a completed auth flow result.',
    inputSchema: {
      password: z.string().min(1).describe('Password to encrypt the keystore'),
      privateKey: z.string().describe('Manager private key (hex, from portkey_create_wallet)'),
      mnemonic: z.string().describe('Manager mnemonic (from portkey_create_wallet)'),
      caHash: z.string().describe('CA hash (from portkey_check_status)'),
      caAddress: z.string().describe('CA address (from portkey_check_status)'),
      loginEmail: LOGIN_EMAIL.optional(),
      originChainId: CHAIN_ID.describe('Resolved origin chain ID from portkey_prepare_auth_flow'),
      network: NETWORK,
    },
  },
  async ({ password, privateKey, mnemonic, caHash, caAddress, loginEmail, originChainId, network }) => {
    try {
      return ok(saveKeystore({
        password,
        privateKey,
        mnemonic,
        caHash,
        caAddress,
        loginEmail,
        originChainId,
        network: network || 'mainnet',
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 26. portkey_unlock
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_unlock',
  {
    description: 'Unlock the encrypted keystore with a password. Loads the Manager wallet into memory for write operations. If the password was forgotten, stop retrying and use portkey_recover_and_save to re-login / recover with fresh guardian verification codes.',
    inputSchema: {
      password: z.string().min(1).describe('Keystore password'),
      loginEmail: LOGIN_EMAIL.optional(),
      keystoreFile: KEYSTORE_FILE.optional(),
      network: NETWORK,
    },
  },
  async ({ password, loginEmail, keystoreFile, network }) => {
    try {
      return ok(unlockWallet(password, network || 'mainnet', loginEmail, keystoreFile));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 26b. portkey_recover_and_save
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_recover_and_save',
  {
    description: 'Recover an existing CA wallet, wait for pass status, and immediately save the new manager to a local encrypted keystore. Use this when you want a reusable signer instead of a one-off recovery session.',
    inputSchema: {
      email: z.string().email().describe('Email address to recover'),
      guardiansApproved: z.string().describe('JSON array of approved guardians'),
      chainId: CHAIN_ID.describe('Resolved chain ID from portkey_prepare_auth_flow'),
      password: PASSWORD,
      loginEmail: LOGIN_EMAIL.optional(),
      maxStatusChecks: z.number().int().positive().optional().describe('Optional max status polling attempts'),
      statusCheckDelayMs: z.number().int().positive().optional().describe('Optional delay between status polling attempts in milliseconds'),
      network: NETWORK,
    },
  },
  async ({ email, guardiansApproved, chainId, password, loginEmail, maxStatusChecks, statusCheckDelayMs, network }) => {
    try {
      return ok(await recoverAndSaveWallet(getConfig({ network }), {
        email,
        guardiansApproved: parseJson(
          guardiansApproved,
          RecoveryGuardianApprovedSchema,
          'guardiansApproved',
        ),
        chainId,
        password,
        loginEmail,
        network,
        maxStatusChecks,
        statusCheckDelayMs,
      }));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 27. portkey_lock
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_lock',
  {
    description: 'Lock the wallet — clear the Manager private key from memory. Use when done with write operations for security.',
  },
  async () => {
    try {
      return ok(lockWallet());
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 28. portkey_wallet_status
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_wallet_status',
  {
    description: 'Check the wallet status for the active or targeted CA keystore: whether a keystore exists, whether it is unlocked, CA address, manager address, the recommended next step (unlock), and fallback guidance for wrong-profile selection or forgotten passwords.',
    inputSchema: {
      loginEmail: LOGIN_EMAIL.optional(),
      network: NETWORK,
    },
  },
  async ({ loginEmail, network }) => {
    try {
      return ok(getWalletStatus(network || 'mainnet', loginEmail));
    } catch (err) { return fail(err); }
  },
);

// ---------------------------------------------------------------------------
// 29. portkey_list_wallet_profiles
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_list_wallet_profiles',
  {
    description:
      'List locally saved CA keystore profiles. Use when you need to discover which login emails already have local keystores and which profile is currently active.',
    inputSchema: {
      network: NETWORK.optional().describe('Optional network filter'),
    },
  },
  async ({ network }) => {
    try {
      return ok({ profiles: listWalletProfiles(network) });
    } catch (err) {
      return fail(err);
    }
  },
);

// ---------------------------------------------------------------------------
// 30. portkey_get_active_wallet
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_get_active_wallet',
  {
    description:
      'Get shared active wallet context used by cross-skill signer resolution.',
    inputSchema: {},
  },
  async () => {
    try {
      return ok({ activeWallet: getActiveWallet() });
    } catch (err) {
      return fail(err);
    }
  },
);

// ---------------------------------------------------------------------------
// 31. portkey_set_active_wallet
// ---------------------------------------------------------------------------
server.registerTool(
  'portkey_set_active_wallet',
  {
    description:
      'Set shared active wallet context manually for cross-skill signer resolution.',
    inputSchema: {
      walletType: z.enum(['EOA', 'CA']).describe('Wallet identity type'),
      source: z
        .enum(['eoa-local', 'ca-keystore', 'env'])
        .describe('Credential source'),
      network: NETWORK.optional().describe('Optional network tag'),
      address: z.string().optional().describe('EOA or manager address'),
      loginEmail: LOGIN_EMAIL.optional(),
      caAddress: z.string().optional().describe('CA address'),
      caHash: z.string().optional().describe('CA hash'),
      walletFile: z.string().optional().describe('EOA wallet file absolute path'),
      keystoreFile: z
        .string()
        .optional()
        .describe('CA keystore file absolute path'),
    },
  },
  async (input) => {
    try {
      const context = setActiveWallet(input);
      return ok({ updated: true, context });
    } catch (err) {
      return fail(err);
    }
  },
);

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Portkey MCP Server running on stdio');
}

main().catch((err) => {
  console.error('Fatal:', err);
  process.exit(1);
});
