// Which of Aero's seven chains have published contracts, for the chips under "Where to point sAERO on Oct 22".
// Read from Aero's own deployment files (dromos-labs/metadex-public, deployment-addresses/<chain>.json) and
// written to docs/data/aero-chains.json, so the page asks GitHub nothing itself. A chain counts as having
// "pools" when its file names a pool factory or the factory registry, and "allocation" when it names a voter
// (the contract sAERO is allocated through). Run by the snapshot workflow; on any error the old file stays.
import { writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const API = "https://api.github.com/repos/dromos-labs/metadex-public/contents/deployment-addresses";

// Without this, a hung GitHub API response would block the whole step for the
// runner's default job timeout (hours), not just skip this best-effort check
// as `continue-on-error: true` in the workflow implies it should.
const GITHUB_API_TIMEOUT_MS = 10_000;

// File names are not announced yet (only arc.json exists on 12.10.2026), so match loosely.
export const CHAINS = {
  base: /^base/, ethereum: /^(ethereum|eth|mainnet)\b/, optimism: /^(optimism|op)\b/, arc: /^arc/,
  ink: /^ink/, robinhood: /^robinhood/, arbitrum: /^(arbitrum|arb)/,
};

/** Which of `CHAINS` a deployment-addresses file name belongs to, or undefined if none match. */
export function matchChainKey(filename) {
  return Object.keys(CHAINS).find((k) => CHAINS[k].test(filename.toLowerCase()));
}

/**
 * Whether a deployment file's contract names show pools/allocation are live on
 * that chain, given the (lower-cased) keys of its deployment JSON.
 */
export function classifyChainFile(names) {
  return {
    pools: names.some((k) => k.includes("poolfactory") || k === "factoryregistry"),
    allocation: names.some((k) => k.includes("voter")),
  };
}

async function main() {
  const headers = { accept: "application/vnd.github+json", "user-agent": "aero-vote-radar" };
  if (process.env.GITHUB_TOKEN) headers.authorization = "Bearer " + process.env.GITHUB_TOKEN;

  const list = await fetch(API, { headers, signal: AbortSignal.timeout(GITHUB_API_TIMEOUT_MS) }).then((r) => { if (!r.ok) throw new Error("list " + r.status); return r.json(); });
  const chains = {};
  for (const f of list.filter((x) => x.name.endsWith(".json"))) {
    const key = matchChainKey(f.name);
    if (!key) continue;
    const body = await fetch(f.download_url, { headers, signal: AbortSignal.timeout(GITHUB_API_TIMEOUT_MS) }).then((r) => { if (!r.ok) throw new Error(f.name + " " + r.status); return r.json(); });
    const names = Object.keys(body).map((k) => k.toLowerCase());
    chains[key] = { file: f.name, ...classifyChainFile(names) };
  }
  writeFileSync("docs/data/aero-chains.json", JSON.stringify({ checkedAt: new Date().toISOString(), chains }, null, 1) + "\n");
  console.log("aero-chains:", JSON.stringify(chains));
}

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((err) => {
    console.error(err instanceof Error ? err.message : String(err));
    process.exitCode = 1;
  });
}
