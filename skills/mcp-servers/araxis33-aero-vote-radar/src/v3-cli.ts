#!/usr/bin/env node
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { createPublicClient, http, type Chain } from "viem";
import { arbitrum, base, mainnet, optimism } from "viem/chains";
import { client } from "./chain.js";
import { V3_LOGS_RPC_URL } from "./constants.js";
import { getTokenPrices } from "./prices.js";
import { formatError } from "./util.js";
import { registryFromDeployment, scanV3, type V3ScanFile, type V3ScanGauge, type V3Client } from "./v3.js";
import { appendV3Sample, poolKey, steadiness, type V3HistoryFile } from "./v3History.js";
import { renderV3LlmsTxt } from "./v3Llms.js";
import { scanTopAllocators } from "./topAllocators.js";

/**
 * Entrypoint for the scheduled Aero (v3) scan across Aero's seven networks,
 * written to one file (docs/data/v3.json) with a `chain` on every gauge. Each
 * network's FactoryRegistry comes from Aero's own deployment file
 * (dromos-labs/metadex-public, deployment-addresses/leaf-<chain>.json), with
 * the address Aero published at app.aero.xyz/docs/security as the fallback.
 * A network that fails is reported in `chains` and the rest still publish.
 * `V3_CHAINS=base,arc` limits a manual run.
 */
const RAW = "https://raw.githubusercontent.com/dromos-labs/metadex-public/main/deployment-addresses/";

// Public endpoints measured 2026-10-22: `rpc` answers batched eth_call (the
// Optimism and Ink endpoints used for logs refuse batches), `logs` serves
// eth_getLogs back to launch (publicnode refuses history on Base, Optimism,
// Arbitrum and Robinhood). `step` is the block span tried first; refused calls
// are split further in readFeesCollected.
const CHAINS: Record<string, { registry: string; rpc: string; logs: string; step: bigint }> = {
  base: { registry: "0x7b2A2c12dC5Ea2a31455952a05031C3E4BB28F3E", rpc: "", logs: V3_LOGS_RPC_URL, step: 1_000n },
  ethereum: { registry: "0xdd1705e23762F4D6e44D8C31BD8Ea80c54612239", rpc: "https://ethereum-rpc.publicnode.com", logs: "https://mainnet.gateway.tenderly.co", step: 1_000n },
  optimism: { registry: "0xb6F9705A631CC1C0E8570FFde48882C95E2Df408", rpc: "https://optimism-rpc.publicnode.com", logs: "https://mainnet.optimism.io", step: 10_000n },
  arbitrum: { registry: "0x9E635b2c689fC52201DF7eF1C9FA607c2F58f666", rpc: "https://arb1.arbitrum.io/rpc", logs: "https://arb1.arbitrum.io/rpc", step: 100_000n },
  ink: { registry: "0xdd1705e23762F4D6e44D8C31BD8Ea80c54612239", rpc: "https://rpc-gel.inkonchain.com", logs: "https://rpc-qnd.inkonchain.com", step: 10_000n },
  robinhood: { registry: "0xdd1705e23762F4D6e44D8C31BD8Ea80c54612239", rpc: "https://rpc.mainnet.chain.robinhood.com", logs: "https://rpc.mainnet.chain.robinhood.com", step: 100_000n },
  arc: { registry: "0xCe44907DC45D3BFa3f5f6035B0e6E8B22D780A42", rpc: "https://rpc.mainnet.arc.io", logs: "https://rpc.mainnet.arc.io", step: 5_000n },
};
const VIEM_CHAINS: Record<string, Chain> = { base, ethereum: mainnet, optimism, arbitrum };

// The new AERO (app.aero.xyz/docs/security) has no DefiLlama price yet on launch
// day; it upgrades 1:1 from the old AERO, so on Base it is priced as the old one.
const NEW_AERO = "0x3f5bf3edac59d650d8fdf9657a71f2f904a3a4ee";
const OLD_AERO = "0x940181a94a35a4569e4529a3cdfb74e38fd98631";

async function registryAddress(chain: string): Promise<string> {
  try {
    const res = await fetch(`${RAW}leaf-${chain}.json`, { signal: AbortSignal.timeout(10_000) });
    if (res.ok) return registryFromDeployment((await res.json()) as Record<string, unknown>) ?? CHAINS[chain].registry;
  } catch {
    // fall back to the published address below
  }
  return CHAINS[chain].registry;
}

const transport = (url: string) => http(url, { retryCount: 6, retryDelay: 1500, batch: true, fetchOptions: { headers: { "user-agent": "aero-vote-radar" } } });

async function scanChain(name: string, now: Date): Promise<V3ScanFile> {
  const cfg = CHAINS[name];
  const reads = (cfg.rpc ? createPublicClient({ chain: VIEM_CHAINS[name], transport: transport(cfg.rpc) }) : client) as unknown as V3Client & {
    getBlockNumber(): Promise<bigint>;
    getBlock(a: { blockNumber: bigint }): Promise<{ timestamp: bigint }>;
  };
  const logs = createPublicClient({ chain: VIEM_CHAINS[name], transport: http(cfg.logs, { retryCount: 3, retryDelay: 1000 }) });
  // Block time measured over the last 100,000 blocks (or what the chain has), so the
  // 96 h fee window maps to the right block range on 0.1 s and 12 s chains alike.
  const latest = await reads.getBlockNumber();
  const back = latest > 100_000n ? 100_000n : latest - 1n;
  const [a, b] = await Promise.all([reads.getBlock({ blockNumber: latest }), reads.getBlock({ blockNumber: latest - back })]);
  const blockTimeSec = Number(a.timestamp - b.timestamp) / Number(back);
  return scanV3(
    { readContract: reads.readContract, getBlockNumber: async () => latest, getLogs: logs.getLogs as unknown as V3Client["getLogs"] },
    (await registryAddress(name)) as `0x${string}`,
    {
      chain: name,
      now,
      blockTimeSec,
      logStep: cfg.step,
      priceOf: async (tokens) => {
        const extra = name === "base" ? [OLD_AERO] : [];
        const prices = await getTokenPrices([...tokens, ...extra], name);
        return (t) => {
          const k = t.toLowerCase();
          const p = prices.get(name === "base" && k === NEW_AERO ? OLD_AERO : k);
          return p && p.price > 0 ? { decimals: p.decimals, priceUsd: p.price } : undefined;
        };
      },
    },
  );
}

async function main() {
  const outPath = process.argv[2] ?? "docs/data/v3.json";
  const now = new Date();
  const names = process.env.V3_CHAINS ? process.env.V3_CHAINS.split(",") : Object.keys(CHAINS);
  const results = await Promise.all(
    names.map(async (name) => {
      const t0 = Date.now();
      try {
        const r = await scanChain(name, now);
        console.error(`v3 ${name}: ${r.status}, ${r.gauges.length} gauges, ${r.windowHours.toFixed(1)} h, ${((Date.now() - t0) / 1000).toFixed(0)} s`);
        return { name, r };
      } catch (err) {
        console.error(`v3 ${name}: error ${formatError(err)}`);
        return { name, error: formatError(err) };
      }
    }),
  );
  const gauges: V3ScanGauge[] = results.flatMap((x) => x.r?.gauges ?? []);
  if (gauges.length === 0 && results.every((x) => x.error)) throw new Error("every network failed");
  gauges.sort((a, b) => (b.usdPerDayPer10k ?? -1) - (a.usdPerDayPer10k ?? -1));
  // Hourly history next to the scan; each gauge gets its steadiness from it.
  const historyPath = outPath.replace(/v3\.json$/, "v3-history.json");
  const history = appendV3Sample(existsSync(historyPath) ? (JSON.parse(readFileSync(historyPath, "utf8")) as V3HistoryFile) : null, gauges, now);
  writeFileSync(historyPath, JSON.stringify(history) + "\n");
  for (const g of gauges) {
    const s = steadiness(history.pools[poolKey(g)] ?? []);
    if (s) g.steady = s;
  }
  const out: V3ScanFile = {
    checkedAt: now.toISOString(),
    chain: "all",
    status: results.some((x) => x.r?.status === "live") ? "live" : "not-live",
    windowHours: Math.max(0, ...results.map((x) => x.r?.windowHours ?? 0)),
    gauges,
    chains: Object.fromEntries(
      results.map((x) => [
        x.name,
        x.r
          ? { status: x.r.status, windowHours: x.r.windowHours, gauges: x.r.gauges.length }
          : { status: "error" as const, windowHours: 0, gauges: 0, error: x.error },
      ]),
    ),
  };
  writeFileSync(outPath, JSON.stringify(out, null, 1) + "\n");
  console.error(`v3: ${out.status}, ${gauges.length} gauges -> ${outPath}`);
  // The same scan as plain text for AI assistants, next to the page (docs/llms.txt).
  if (/data[\\/]v3\.json$/.test(outPath) && out.status === "live") {
    const llmsPath = outPath.replace(/data[\\/]v3\.json$/, "llms.txt");
    writeFileSync(llmsPath, renderV3LlmsTxt(out));
    console.error(`v3: llms.txt -> ${llmsPath}`);
  }
  // Where the best allocators are pointed now. Optional: if dromos.kitchen or a
  // network doesn't answer, the last file stays and the page hides it once stale.
  if (out.status === "live") {
    const topPath = outPath.replace(/v3\.json$/, "top-allocators.json");
    try {
      const top = await scanTopAllocators(now);
      writeFileSync(topPath, JSON.stringify(top, null, 1) + "\n");
      console.error(`v3: top allocators, ${top.positions.length} positions -> ${topPath}`);
    } catch (err) {
      console.error(`v3: top allocators skipped: ${formatError(err)}`);
    }
  }
}

main().catch((err) => {
  console.error(`Error: ${formatError(err)}`);
  process.exitCode = 1;
});
