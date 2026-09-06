import type { ChainId, EnvConfig } from './types.js';
import { SkillError } from './errors.js';

export interface ContractsConfig {
  dao: {
    daoAddress: string;
    proposalAddress: string;
    voteAddress: string;
  };
  network: {
    AELF: {
      parliament: string;
      association: string;
      referendum: string;
      election: string;
      tokenConverter: string;
      profit: string;
      token: string;
      genesis: string;
    };
    tDVV: {
      token: string;
    };
    tDVW: {
      token: string;
    };
  };
  explorer: Record<ChainId, string>;
}

const DEFAULTS = {
  apiBase: 'https://api.tmrwdao.com',
  authBase: 'https://api.tmrwdao.com',
  daoChain: 'tDVV' as ChainId,
  networkChain: 'AELF' as ChainId,
  authChain: 'AELF' as ChainId,
  source: 'nightElf',
  rpcAELF: 'https://aelf-public-node.aelf.io',
  rpcTDVV: 'https://tdvv-public-node.aelf.io',
  rpcTDVW: 'https://tdvw-test-node.aelf.io',
  httpTimeoutMs: 30_000,
  httpRetryMax: 1,
  httpRetryBaseMs: 200,
  httpRetryPost: false,
  aelfCacheMax: 8,
};

const DEFAULT_CONTRACTS: ContractsConfig = {
  dao: {
    daoAddress: '2izSidAeMiZ6tmD7FKmnoWbygjFSmH5nko3cGJ9EtbfC44BycC',
    proposalAddress: '2tCM3oV6dTCmwFxSiFGPEVhGngdMwBV741wi156vj8kmqfp6da',
    voteAddress: '2A8h4hLynLt86RxqvpNY43x6Js8CYhgyuAzj7sDGQ2ecP77Zgp',
  },
  network: {
    AELF: {
      parliament: '2JT8xzjR5zJ8xnBvdgBZdSjfbokFSbF5hDdpUCbXeWaJfPDmsK',
      association: 'XyRN9VNabpBiVUFeX2t7ZUR2b3tWV7U31exufJ2AUepVb5t56',
      referendum: 'NxSBGHE3zs85tpnX1Ns4awQUtFL8Dnr6Hux4C4E18WZsW4zzJ',
      election: 'NrVf8B7XUduXn1oGHZeF1YANFXEXAhvCymz2WPyKZt4DE2zSg',
      tokenConverter: 'SietKh9cArYub9ox6E4rU94LrzPad6TB72rCwe3X1jQ5m1C34',
      profit: '2ZUgaDqWSh4aJ5s5Ker2tRczhJSNep4bVVfrRBRJTRQdMTbA5W',
      token: 'JRmBduh4nXWi1aXgdUsj5gJrzeZb2LxmrAbf7W99faZSvoAaE',
      genesis: 'pykr77ft9UUKJZLVq15wCH8PinBSjVRQ12sD1Ayq92mKFsJ1i',
    },
    tDVV: {
      token: '7RzVGiuVWkvL4VfVHdZfQF2Tri3sgLe9U991bohHFfSRZXuGX',
    },
    tDVW: {
      token: '',
    },
  },
  explorer: {
    AELF: 'https://aelfscan.io/AELF',
    tDVV: 'https://aelfscan.io/tDVV',
    tDVW: 'https://aelfscan.io/tDVW',
  },
};

let cached: EnvConfig | null = null;
let contractsInitialized = false;

export const CONTRACTS: ContractsConfig = cloneContracts(DEFAULT_CONTRACTS);

function mustChain(value: string, field: string): ChainId {
  if (value === 'AELF' || value === 'tDVV' || value === 'tDVW') {
    return value;
  }
  throw new SkillError('INVALID_CONFIG', `${field} must be one of AELF/tDVV/tDVW`);
}

function trimSlash(url: string): string {
  return url.replace(/\/$/, '');
}

function readInt(value: string | undefined, fallback: number): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) return fallback;
  return Math.floor(parsed);
}

function readBool(value: string | undefined, fallback: boolean): boolean {
  if (!value) return fallback;
  return value === '1' || value.toLowerCase() === 'true';
}

function cloneContracts(input: ContractsConfig): ContractsConfig {
  return JSON.parse(JSON.stringify(input)) as ContractsConfig;
}

function setContracts(next: ContractsConfig): void {
  CONTRACTS.dao = { ...next.dao };
  CONTRACTS.network.AELF = { ...next.network.AELF };
  CONTRACTS.network.tDVV = { ...next.network.tDVV };
  CONTRACTS.network.tDVW = { ...next.network.tDVW };
  CONTRACTS.explorer = { ...next.explorer };
}

function parseJsonObjectEnv(name: string): Record<string, unknown> | undefined {
  const raw = process.env[name];
  if (!raw) return undefined;

  try {
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      throw new Error(`${name} must be a JSON object`);
    }
    return parsed as Record<string, unknown>;
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    throw new SkillError('INVALID_CONFIG', `${name} is invalid JSON object`, message);
  }
}

function mergeRecord<T extends Record<string, string>>(target: T, patch: Record<string, unknown>): void {
  const mutable = target as Record<string, string>;
  for (const [key, value] of Object.entries(patch)) {
    if (typeof value !== 'string') continue;
    if (key in target) {
      mutable[key] = value;
    }
  }
}

export function getContracts(): ContractsConfig {
  if (contractsInitialized) {
    return CONTRACTS;
  }

  const next = cloneContracts(DEFAULT_CONTRACTS);
  const contractsOverride = parseJsonObjectEnv('TMRW_CONTRACTS_JSON');
  const explorerOverride = parseJsonObjectEnv('TMRW_EXPLORER_JSON');

  if (contractsOverride) {
    const daoOverride = contractsOverride.dao;
    if (daoOverride && typeof daoOverride === 'object' && !Array.isArray(daoOverride)) {
      mergeRecord(next.dao, daoOverride as Record<string, unknown>);
    }

    const networkOverride = contractsOverride.network;
    if (networkOverride && typeof networkOverride === 'object' && !Array.isArray(networkOverride)) {
      for (const chain of ['AELF', 'tDVV', 'tDVW'] as const) {
        const chainOverride = (networkOverride as Record<string, unknown>)[chain];
        if (chainOverride && typeof chainOverride === 'object' && !Array.isArray(chainOverride)) {
          mergeRecord(next.network[chain], chainOverride as Record<string, unknown>);
        }
      }
    }

    const explorerFromContracts = contractsOverride.explorer;
    if (
      explorerFromContracts &&
      typeof explorerFromContracts === 'object' &&
      !Array.isArray(explorerFromContracts)
    ) {
      mergeRecord(next.explorer, explorerFromContracts as Record<string, unknown>);
    }
  }

  if (explorerOverride) {
    mergeRecord(next.explorer, explorerOverride);
  }

  setContracts(next);
  contractsInitialized = true;
  return CONTRACTS;
}

export function getConfig(): EnvConfig {
  if (cached) return cached;

  const apiBase = trimSlash(process.env.TMRW_API_BASE ?? DEFAULTS.apiBase);
  const authBase = trimSlash(process.env.TMRW_AUTH_BASE ?? DEFAULTS.authBase);
  getContracts();

  const config: EnvConfig = {
    apiBase,
    authBase,
    defaultDaoChain: mustChain(process.env.TMRW_CHAIN_DEFAULT_DAO ?? DEFAULTS.daoChain, 'TMRW_CHAIN_DEFAULT_DAO'),
    defaultNetworkChain: mustChain(
      process.env.TMRW_CHAIN_DEFAULT_NETWORK ?? DEFAULTS.networkChain,
      'TMRW_CHAIN_DEFAULT_NETWORK',
    ),
    authChainId: mustChain(process.env.TMRW_AUTH_CHAIN_ID ?? DEFAULTS.authChain, 'TMRW_AUTH_CHAIN_ID'),
    source: process.env.TMRW_SOURCE ?? DEFAULTS.source,
    caHash: process.env.TMRW_CA_HASH,
    privateKey: process.env.TMRW_PRIVATE_KEY,
    httpTimeoutMs: readInt(process.env.TMRW_HTTP_TIMEOUT_MS, DEFAULTS.httpTimeoutMs),
    httpRetryMax: readInt(process.env.TMRW_HTTP_RETRY_MAX, DEFAULTS.httpRetryMax),
    httpRetryBaseMs: readInt(process.env.TMRW_HTTP_RETRY_BASE_MS, DEFAULTS.httpRetryBaseMs),
    httpRetryPost: readBool(process.env.TMRW_HTTP_RETRY_POST, DEFAULTS.httpRetryPost),
    aelfCacheMax: readInt(process.env.TMRW_AELF_CACHE_MAX, DEFAULTS.aelfCacheMax),
    rpc: {
      AELF: process.env.TMRW_RPC_AELF ?? DEFAULTS.rpcAELF,
      tDVV: process.env.TMRW_RPC_TDVV ?? DEFAULTS.rpcTDVV,
      tDVW: process.env.TMRW_RPC_TDVW ?? DEFAULTS.rpcTDVW,
    },
  };

  cached = config;
  return config;
}

export function resetConfigCache(): void {
  cached = null;
  contractsInitialized = false;
  setContracts(DEFAULT_CONTRACTS);
}

export type ProposalContractType = 'Parliament' | 'Association' | 'Referendum';

export function getProposalContractAddress(chainId: ChainId, proposalType: ProposalContractType): string {
  const chainContracts = getContracts().network.AELF;
  if (chainId !== 'AELF') {
    throw new SkillError('UNSUPPORTED_CHAIN', `network governance currently supports AELF only, got ${chainId}`);
  }
  if (proposalType === 'Parliament') return chainContracts.parliament;
  if (proposalType === 'Association') return chainContracts.association;
  return chainContracts.referendum;
}

export function getTokenContractAddress(chainId: ChainId): string {
  const contracts = getContracts();
  if (chainId === 'AELF') return contracts.network.AELF.token;
  if (chainId === 'tDVV') return contracts.network.tDVV.token;
  if (chainId === 'tDVW') return contracts.network.tDVW.token;
  throw new SkillError('UNSUPPORTED_CHAIN', `token contract not configured for ${chainId}`);
}
