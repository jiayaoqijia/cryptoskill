import { CHAIN_NAMES, chainOf, perDay } from "./radar.js";
import type { V3ScanFile } from "./v3.js";

/**
 * A wallet's sAERO on Aero, read the way the web page reads it
 * (app.aero.xyz/docs/security): stakes from the VotingEscrow on Base, and per
 * network the 47 h timer and current split from that network's LeafVoter
 * (tokenStates.lastAllocated + allocationCooldown − accumulatedCooldownReduction,
 * as ILeafVoter documents). Every network has its LeafVoter at the same address,
 * keyed by the Base stake id.
 */
export const VOTING_ESCROW = "0xbf7977e1521e9a3032bf7243ee4712f311f13915";
export const LEAF_VOTER = "0x382409fad8503fbcdbb27a4211551fa03e884078";

const SEL_BALANCE_OF = "0x70a08231"; // balanceOf(address)
const SEL_POWER_OF = "0xe7e242d4"; // balanceOfNFT(uint256)
const SEL_TOKEN_OF_OWNER = "0x2f745c59"; // tokenOfOwnerByIndex(address,uint256)
const SEL_TOKEN_STATES = "0xaa9f3eca"; // tokenStates(uint256) -> (operator, lastAllocated, canVoteForZeroCapGauges, chainAllocation)
const SEL_COOLDOWN = "0x6f5aa6ab"; // allocationCooldown()
const SEL_REDUCTION = "0xbe8cfed2"; // accumulatedCooldownReduction(uint256)
const SEL_GAUGES = "0xd596efe1"; // allocatedGauges(uint256) -> address[]
const SEL_ALLOCATION = "0x1c3a964f"; // allocations(uint256,address) -> uint128

export const MAX_STAKES = 20;
export const RPC_TIMEOUT_MS = 8000;

/** Tried in order; the first that answers wins. BASE_RPC_URL, when set, goes first. */
export const CHAIN_RPCS: Record<string, string[]> = {
  base: [...(process.env.BASE_RPC_URL ? [process.env.BASE_RPC_URL] : []), "https://base-rpc.publicnode.com", "https://mainnet.base.org"],
  ethereum: ["https://ethereum-rpc.publicnode.com", "https://eth.llamarpc.com"],
  optimism: ["https://optimism-rpc.publicnode.com", "https://mainnet.optimism.io"],
  arbitrum: ["https://arbitrum-one-rpc.publicnode.com", "https://arb1.arbitrum.io/rpc"],
  ink: ["https://rpc-gel.inkonchain.com", "https://rpc-qnd.inkonchain.com", "https://ink-rpc.publicnode.com"],
  robinhood: ["https://rpc.mainnet.chain.robinhood.com"],
  arc: ["https://rpc.mainnet.arc.io"],
};

const word = (hex: string) => hex.replace(/^0x/, "").toLowerCase().padStart(64, "0");
const hexOf = (n: bigint | number) => word(BigInt(n).toString(16));
const big = (hex: string) => BigInt(hex === "0x" ? 0 : hex);

async function ethCall(chain: string, to: string, data: string): Promise<string> {
  let lastErr: unknown;
  for (const url of CHAIN_RPCS[chain]) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "eth_call", params: [{ to, data }, "latest"] }),
        signal: AbortSignal.timeout(RPC_TIMEOUT_MS),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = (await res.json()) as { result?: string; error?: { message?: string } };
      if (json.error) throw new Error(json.error.message || "rpc error");
      return json.result ?? "0x";
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr ?? new Error(`no RPC answered on ${chain}`);
}

export interface StakeOnChain {
  /** Unix seconds of the last allocation on this network, 0 if never. */
  lastAllocated: number;
  /** Unix seconds when the stake may move again here; 0 when it has never allocated (no wait). */
  readyAt: number;
  allocations: { gauge: string; amount: number }[];
}

export interface Stake {
  id: bigint;
  sAero: number;
  chains: Record<string, StakeOnChain>;
}

export interface WalletStakes {
  address: string;
  /** Stakes the wallet owns, of which at most MAX_STAKES are read. */
  count: number;
  stakes: Stake[];
  totalSAero: number;
  /** Networks that did not answer; their timers and splits are missing. */
  failed: string[];
}

/** The network's cooldown between moves of one stake, in seconds. */
export async function readCooldown(chain: string): Promise<number> {
  return Number(big(await ethCall(chain, LEAF_VOTER, SEL_COOLDOWN)));
}

export async function readStakeOn(chain: string, id: bigint, cooldown: number): Promise<StakeOnChain> {
  const state = (await ethCall(chain, LEAF_VOTER, SEL_TOKEN_STATES + hexOf(id))).slice(2);
  const last = Number(BigInt("0x" + (state.slice(64, 128) || "0")));
  const reduction = Number(big(await ethCall(chain, LEAF_VOTER, SEL_REDUCTION + hexOf(id))));
  const list = (await ethCall(chain, LEAF_VOTER, SEL_GAUGES + hexOf(id))).slice(2);
  const n = list.length >= 128 ? Number(BigInt("0x" + list.slice(64, 128))) : 0;
  const allocations = [];
  for (let k = 0; k < n; k++) {
    const gauge = "0x" + list.slice(128 + k * 64 + 24, 128 + (k + 1) * 64);
    const raw = big(await ethCall(chain, LEAF_VOTER, SEL_ALLOCATION + hexOf(id) + word(gauge)));
    allocations.push({ gauge, amount: Number(raw) / 1e18 });
  }
  return { lastAllocated: last, readyAt: last ? last + Math.max(0, cooldown - reduction) : 0, allocations };
}

export async function readWalletStakes(address: string): Promise<WalletStakes> {
  const count = Number(big(await ethCall("base", VOTING_ESCROW, SEL_BALANCE_OF + word(address))));
  const stakes: Stake[] = [];
  for (let i = 0; i < Math.min(count, MAX_STAKES); i++) {
    const id = big(await ethCall("base", VOTING_ESCROW, SEL_TOKEN_OF_OWNER + word(address) + hexOf(i)));
    const sAero = Number(big(await ethCall("base", VOTING_ESCROW, SEL_POWER_OF + hexOf(id)))) / 1e18;
    stakes.push({ id, sAero, chains: {} });
  }
  // Networks are read in parallel; one that doesn't answer is reported, not fatal.
  const failed: string[] = [];
  if (stakes.length) {
    await Promise.all(
      Object.keys(CHAIN_NAMES).map(async (chain) => {
        try {
          const cooldown = Number(big(await ethCall(chain, LEAF_VOTER, SEL_COOLDOWN)));
          for (const st of stakes) st.chains[chain] = await readStakeOn(chain, st.id, cooldown);
        } catch {
          for (const st of stakes) delete st.chains[chain];
          failed.push(chain);
        }
      }),
    );
  }
  return { address, count, stakes, totalSAero: stakes.reduce((a, s) => a + s.sAero, 0), failed };
}

/** Soonest time each network lets one of the wallet's stakes move, for networks it has allocated on. */
export function timersByChain(w: Pick<WalletStakes, "stakes">): Record<string, number> {
  const soonest: Record<string, number> = {};
  for (const st of w.stakes)
    for (const [chain, c] of Object.entries(st.chains))
      if (c.lastAllocated) soonest[chain] = Math.min(soonest[chain] ?? Infinity, c.readyAt);
  return soonest;
}

/** What the wallet's current split pays a day at the scan's rates, and how much sAERO it has placed. */
export function currentSplitPays(w: Pick<WalletStakes, "stakes">, scan: V3ScanFile): { usdPerDay: number; placedSAero: number } {
  const byGauge = new Map(scan.gauges.map((g) => [`${chainOf(g)}:${g.gauge.toLowerCase()}`, g]));
  let usdPerDay = 0;
  let placedSAero = 0;
  for (const st of w.stakes)
    for (const [chain, c] of Object.entries(st.chains))
      for (const a of c.allocations) {
        const g = byGauge.get(`${chain}:${a.gauge.toLowerCase()}`);
        placedSAero += a.amount;
        if (g && g.weight > 0) usdPerDay += perDay(g) * Math.min(1, a.amount / g.weight);
      }
  return { usdPerDay, placedSAero };
}

/**
 * The scan with the wallet's own sAERO taken out of each pool's weight. A
 * suggested split moves the whole stake, so ranking against the full weight
 * would count the sAERO already in a pool twice: once in the pool, once as
 * the amount joining it.
 */
export function withoutOwnSAero(scan: V3ScanFile, w: Pick<WalletStakes, "stakes">): V3ScanFile {
  const own = new Map<string, number>();
  for (const st of w.stakes)
    for (const [chain, c] of Object.entries(st.chains))
      for (const a of c.allocations) {
        const key = `${chain}:${a.gauge.toLowerCase()}`;
        own.set(key, (own.get(key) ?? 0) + a.amount);
      }
  if (own.size === 0) return scan;
  return {
    ...scan,
    gauges: scan.gauges.map((g) => {
      const mine = own.get(`${chainOf(g)}:${g.gauge.toLowerCase()}`);
      return mine ? { ...g, weight: Math.max(0, g.weight - mine) } : g;
    }),
  };
}

/** "now" or "in N h". */
export const untilText = (readyAt: number, nowSec: number = Date.now() / 1000) =>
  readyAt <= nowSec ? "now" : `in ${Math.ceil((readyAt - nowSec) / 3600)} h`;
