#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import { client } from "./chain.js";
import { getTokenPrices } from "./prices.js";
import { formatError } from "./util.js";
import { registryFromDeployment, scanV3, type V3ScanFile, type V3Client } from "./v3.js";

/**
 * Entrypoint for the scheduled Aero (v3) scan on Base. It waits on Aero's own
 * deployment file: scripts/aero-chains.mjs records which file in
 * dromos-labs/metadex-public belongs to Base, and until there is one this
 * writes `status: "no-addresses"` and stops. Nothing on the page reads the
 * output yet. `V3_REGISTRY` overrides the registry for a manual check.
 */
const RAW = "https://raw.githubusercontent.com/dromos-labs/metadex-public/main/deployment-addresses/";

async function registryAddress(): Promise<string | undefined> {
  if (process.env.V3_REGISTRY) return process.env.V3_REGISTRY;
  let file: string | undefined;
  try {
    file = JSON.parse(readFileSync("docs/data/aero-chains.json", "utf8")).chains?.base?.file;
  } catch {
    return undefined;
  }
  if (!file) return undefined;
  const res = await fetch(RAW + file, { signal: AbortSignal.timeout(10_000) });
  if (!res.ok) throw new Error(`${file} ${res.status}`);
  return registryFromDeployment((await res.json()) as Record<string, unknown>);
}

async function main() {
  const outPath = process.argv[2] ?? "docs/data/v3.json";
  const now = new Date();
  const registry = await registryAddress();
  let out: V3ScanFile;
  if (!registry) {
    out = { checkedAt: now.toISOString(), chain: "base", status: "no-addresses", windowHours: 0, gauges: [] };
  } else {
    out = await scanV3(client as unknown as V3Client & { getBlockNumber(): Promise<bigint> }, registry as `0x${string}`, {
      chain: "base",
      now,
      priceOf: async (tokens) => {
        const prices = await getTokenPrices(tokens);
        return (t) => {
          const p = prices.get(t.toLowerCase());
          return p && p.price > 0 ? { decimals: p.decimals, priceUsd: p.price } : undefined;
        };
      },
    });
  }
  writeFileSync(outPath, JSON.stringify(out, null, 1) + "\n");
  console.error(`v3: ${out.status}, ${out.gauges.length} gauges, ${out.windowHours.toFixed(1)} h of fees -> ${outPath}`);
}

main().catch((err) => {
  console.error(`Error: ${formatError(err)}`);
  process.exitCode = 1;
});
