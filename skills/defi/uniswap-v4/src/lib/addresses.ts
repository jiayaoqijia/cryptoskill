/**
 * Contract addresses per chain — sourced from official Uniswap V4 deployment docs.
 * https://docs.uniswap.org/contracts/v4/deployments
 *
 * All addresses verified 2026-02-08 against on-chain bytecode.
 */

export type SupportedChain = "base" | "ethereum" | "base-sepolia";

export interface ChainConfig {
  chainId: number;
  poolManager: string;
  universalRouter: string;
  permit2: string;
  stateView: string;
  quoter: string;
  weth: string;
  defaultRpcEnv: string;
  explorerBase: string;
}

/**
 * Canonical Uniswap V4 addresses from official docs.
 * Permit2 is universal: 0x000000000022D473030F116dDEE9F6B43aC78BA3 on all chains.
 */
const CHAINS: Record<SupportedChain, ChainConfig> = {
  base: {
    chainId: 8453,
    poolManager: "0x498581fF718922c3f8e6A244956aF099B2652b2b",
    universalRouter: "0x6ff5693b99212da76ad316178a184ab56d299b43",
    permit2: "0x000000000022D473030F116dDEE9F6B43aC78BA3",
    stateView: "0xa3c0c9b65bad0b08107aa264b0f3db444b867a71",
    quoter: "0x0d5e0f971ed27fbff6c2837bf31316121532048d",
    weth: "0x4200000000000000000000000000000000000006",
    defaultRpcEnv: "BASE_RPC_URL",
    explorerBase: "https://basescan.org",
  },
  ethereum: {
    chainId: 1,
    poolManager: "0x000000000004444c5dc75cB358380D2e3dE08A90",
    universalRouter: "0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af",
    permit2: "0x000000000022D473030F116dDEE9F6B43aC78BA3",
    stateView: "0x7ffe42c4a5deea5b0fec41c94c136cf115597227",
    quoter: "0x52f0e24d1c21c8a0cb1e5a5dd6198556bd9e1203",
    weth: "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    defaultRpcEnv: "ETH_RPC_URL",
    explorerBase: "https://etherscan.io",
  },
  "base-sepolia": {
    chainId: 84532,
    poolManager: "0x05E73354cFDd6745C338b50BcFDfA3Aa6fA03408",
    universalRouter: "0x492e6456d9528771018deb9e87ef7750ef184104",
    permit2: "0x000000000022D473030F116dDEE9F6B43aC78BA3",
    stateView: "0x571291b572ed32ce6751a2cb2486ebee8defb9b4",
    quoter: "0x4a6513c898fe1b2d0e78d3b0e0a4a151589b1cba",
    weth: "0x4200000000000000000000000000000000000006",
    defaultRpcEnv: "BASE_SEPOLIA_RPC_URL",
    explorerBase: "https://sepolia.basescan.org",
  },
};

/** Well-known tokens on Base mainnet. */
export const BASE_TOKENS: Record<string, { address: string; decimals: number }> = {
  USDC: { address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", decimals: 6 },
  DAI:  { address: "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb", decimals: 18 },
  cbBTC:{ address: "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf", decimals: 8 },
  WETH: { address: "0x4200000000000000000000000000000000000006", decimals: 18 },
};

/** Common V4 fee tiers: [fee, tickSpacing] */
export const FEE_TIERS: ReadonlyArray<[number, number]> = [
  [500, 10],
  [3000, 60],
  [10000, 200],
  [100, 1],
  [8388608, 60],   // dynamic fee, tickSpacing 60 (Clanker-style)
  [8388608, 200],  // dynamic fee, tickSpacing 200
  [8388608, 10],   // dynamic fee, tickSpacing 10
];

export function getChainConfig(chain: SupportedChain): ChainConfig {
  return CHAINS[chain];
}

export function isSupportedChain(chain: string): chain is SupportedChain {
  return chain in CHAINS;
}

/**
 * Resolve RPC URL from: explicit flag > env var > error.
 * Never hardcodes a default — forces explicit configuration.
 */
export function resolveRpcUrl(chain: SupportedChain, explicitRpc?: string): string {
  if (explicitRpc) return explicitRpc;
  const cfg = CHAINS[chain];
  const fromEnv = process.env[cfg.defaultRpcEnv];
  if (fromEnv) return fromEnv;
  throw new Error(
    `No RPC URL. Pass --rpc <url> or set ${cfg.defaultRpcEnv} env var.`
  );
}

/** ETH address(0) in V4 = native ether. */
export const ADDRESS_ZERO = "0x0000000000000000000000000000000000000000";
