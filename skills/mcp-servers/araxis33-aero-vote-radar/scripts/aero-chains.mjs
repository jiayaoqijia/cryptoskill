// Which of Aero's seven chains have published contracts, for the chips under "Where to point sAERO on Oct 22".
// Read from Aero's own deployment files (dromos-labs/metadex-public, deployment-addresses/<chain>.json) and
// written to docs/data/aero-chains.json, so the page asks GitHub nothing itself. A chain counts as having
// "pools" when its file names a pool factory or the factory registry, and "allocation" when it names a voter
// (the contract sAERO is allocated through). Run by the snapshot workflow; on any error the old file stays.
import { writeFileSync } from "node:fs";

const API = "https://api.github.com/repos/dromos-labs/metadex-public/contents/deployment-addresses";
const headers = { accept: "application/vnd.github+json", "user-agent": "aero-vote-radar" };
if (process.env.GITHUB_TOKEN) headers.authorization = "Bearer " + process.env.GITHUB_TOKEN;

// File names are not announced yet (only arc.json exists on 12.10.2026), so match loosely.
const CHAINS = {
  base: /^base/, ethereum: /^(ethereum|eth|mainnet)\b/, optimism: /^(optimism|op)\b/, arc: /^arc/,
  ink: /^ink/, robinhood: /^robinhood/, arbitrum: /^(arbitrum|arb)/,
};

const list = await fetch(API, { headers }).then((r) => { if (!r.ok) throw new Error("list " + r.status); return r.json(); });
const chains = {};
for (const f of list.filter((x) => x.name.endsWith(".json"))) {
  const key = Object.keys(CHAINS).find((k) => CHAINS[k].test(f.name.toLowerCase()));
  if (!key) continue;
  const body = await fetch(f.download_url, { headers }).then((r) => { if (!r.ok) throw new Error(f.name + " " + r.status); return r.json(); });
  const names = Object.keys(body).map((k) => k.toLowerCase());
  chains[key] = {
    file: f.name,
    pools: names.some((k) => k.includes("poolfactory") || k === "factoryregistry"),
    allocation: names.some((k) => k.includes("voter")),
  };
}
writeFileSync("docs/data/aero-chains.json", JSON.stringify({ checkedAt: new Date().toISOString(), chains }, null, 1) + "\n");
console.log("aero-chains:", JSON.stringify(chains));
