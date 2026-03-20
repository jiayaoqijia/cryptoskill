/**
 * RPC provider helpers.
 *
 * Why this exists:
 * - ethers' JsonRpcProvider will auto-detect the network when not given one.
 *   When RPCs are flaky or rate-limited, this can emit noisy
 *   "failed to detect network; retry" logs.
 * - For write ops, we want to avoid accidentally signing for the wrong chain.
 *
 * We therefore construct providers with a *static* expected chainId.
 * Optionally, callers can still validate the RPC chainId explicitly.
 */

import { JsonRpcProvider } from "ethers";
import { getChainConfig, type SupportedChain } from "./addresses.js";

/**
 * Create a JsonRpcProvider pinned to the expected network.
 * This skips ethers' network auto-detection (less flake/noise).
 */
export function makeProvider(chain: SupportedChain, rpcUrl: string): JsonRpcProvider {
  const cfg = getChainConfig(chain);
  // ethers v6 only commits to the provided `network` when `staticNetwork` is enabled.
  // This avoids noisy "failed to detect network; retry" logs on flaky RPCs.
  return new JsonRpcProvider(
    rpcUrl,
    { chainId: cfg.chainId, name: chain },
    { staticNetwork: true }
  );
}

/** Read the chainId from the RPC itself (not from provider's static network). */
export async function fetchRpcChainId(provider: JsonRpcProvider): Promise<number> {
  const res = await provider.send("eth_chainId", []);
  if (typeof res !== "string") {
    throw new Error(`Unexpected eth_chainId response: ${String(res)}`);
  }
  return Number(BigInt(res));
}

/**
 * Assert the RPC returns the expected chainId.
 * Useful for friendly errors when a user points --rpc at the wrong chain.
 */
export async function assertRpcChain(
  provider: JsonRpcProvider,
  chain: SupportedChain
): Promise<void> {
  const cfg = getChainConfig(chain);
  let actual: number;
  try {
    actual = await fetchRpcChainId(provider);
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    throw new Error(`RPC unreachable or invalid response: ${msg}`);
  }
  if (actual !== cfg.chainId) {
    throw new Error(
      `RPC chainId mismatch: expected ${cfg.chainId} (${chain}), got ${actual}`
    );
  }
}

/**
 * Ensure an address has contract bytecode on-chain.
 *
 * This prevents foot-guns like:
 * - wrong address on the right chain
 * - wrong chain RPC (where that address is an EOA)
 *
 * In those cases, a "contract call" can devolve into an ETH transfer.
 */
export async function assertHasBytecode(
  provider: JsonRpcProvider,
  address: string,
  label: string
): Promise<void> {
  const code = await provider.getCode(address);
  if (!code || code === "0x") {
    throw new Error(`${label} has no contract bytecode at ${address}. Refusing to continue.`);
  }
}
