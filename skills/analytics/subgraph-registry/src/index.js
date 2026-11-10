#!/usr/bin/env node

/**
 * Subgraph Registry MCP Server
 *
 * Exposes the classified subgraph registry as MCP tools that agents can call
 * to discover and select the right subgraph before querying The Graph.
 *
 * Tools:
 *   - search_subgraphs / recommend_subgraph / semantic_search_subgraphs: DISCOVERY only
 *   - get_subgraph_detail / list_registry_stats / get_schema_changes: local index
 *   - execute_query: opt-in POST of GraphQL to The Graph gateway
 *   - get_schema: opt-in schema (registry cache + live __schema when keyed)
 *   - get_top_subgraph_deployments: contract-first lookup from crawled manifests
 *   - get_deployment_30day_query_counts: real registry query_volume_30d (not official 0s)
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import Database from "better-sqlite3";
import { boundedStarter, findContractDeployments, freshness, healthObservation, HEALTH_QUERY, HEALTH_STALE_SECONDS } from "./agent-discovery.js";
import { parseGoal, rankEntities, planKeyless, planWithSchema, schemaProbeQuery, probeHealth, STALE_INDEXING_SECONDS } from "./goal-query.js";
import { applyTokenQuality, normalizeTrusted, SPAM_HANDLING } from "./token-quality.js";
import express from "express";
import { fileURLToPath, pathToFileURL } from "url";
import { basename, dirname, join } from "path";
import { existsSync, mkdirSync, readFileSync, realpathSync, unlinkSync, writeFileSync } from "fs";
import { get as httpsGet } from "https";
import { createHash, timingSafeEqual } from "crypto";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Read from package.json rather than a literal. The hardcoded string had
// drifted to "0.8.20" while the package shipped 0.8.31 — eleven releases of
// every MCP client being told the wrong server version, which is the kind of
// thing that only surfaces when someone is debugging something else.
// Literal, exact-version npx spec used in generated config examples. Bumped
// with package.json at release time; test/scanner-hygiene.test.mjs asserts the
// two agree, so a stale pin fails CI instead of shipping.
export const PINNED_NPX_PACKAGE = "subgraph-registry-mcp@0.13.2";

const PKG_VERSION = (() => {
  try {
    return JSON.parse(
      readFileSync(join(__dirname, "..", "package.json"), "utf8"),
    ).version;
  } catch {
    return "0.0.0";
  }
})();

const DATA_DIR = join(__dirname, "..", "data");
const DB_PATH = join(DATA_DIR, "registry.db");
const OPENAPI_JSON_PATH = join(DATA_DIR, "openapi.json");
// Bundled with the npm package so runtime semantic search has zero
// network dependency. Same model fastembed uses at crawl time
// (Xenova/all-MiniLM-L6-v2) — vectors are bitwise-comparable.
let EMBEDDING_MODEL_ROOT = join(DATA_DIR, "models");
let EMBEDDING_MODEL_DIR = join(EMBEDDING_MODEL_ROOT, "Xenova", "all-MiniLM-L6-v2");
// Test hook: point the embedder at another model root (e.g. an empty dir to
// exercise the fail-closed path). Not read from the environment.
export function setEmbeddingModelRootForTests(root) {
  EMBEDDING_MODEL_ROOT = root || join(DATA_DIR, "models");
  EMBEDDING_MODEL_DIR = join(EMBEDDING_MODEL_ROOT, "Xenova", "all-MiniLM-L6-v2");
  _embedderPromise = null;
}
const GITHUB_DB_URL =
  "https://github.com/PaulieB14/subgraph-registry/raw/main/python/data/registry.db";

// SHA-256 of the registry.db shipped with this npm version. Any download or
// pre-bundled copy that doesn't match this hash is rejected — protects users
// against a compromised GitHub repo or man-in-the-middle on the download.
//
// HOW TO UPDATE WHEN REBUILDING THE REGISTRY:
//   1. Run the crawler to rebuild python/data/registry.db
//   2. shasum -a 256 python/data/registry.db
//   3. Paste the new hash here and bump package.json version
//   4. Update SKILL.md "Verifying the registry" section
const EXPECTED_DB_SHA256 =
  "672afa2f0d405483af5fb4c403e515fb0f1342c7eeb31968e78a53d5f6ebdd6b";
// Skip-verification escape hatch (set to "1" only if you're rebuilding the DB
// locally and know what you're doing — never set in agent-runtime defaults).
const SKIP_VERIFY = process.env.SUBGRAPH_REGISTRY_SKIP_VERIFY === "1";

// ── x402 gateway constants ─────────────────────────────────
// The Graph's public x402 gateway (live since 2026-05-08) lets agents pay
// per-query in USDC on Base without any API key. POST GraphQL to query_url_x402
// and the gateway returns HTTP 402 with a payment manifest; an x402 client
// (e.g. @graphprotocol/client-x402, x402-fetch) signs the EIP-3009 USDC
// transfer and retries automatically.
const X402_GATEWAY_BASE = "https://gateway.thegraph.com/api/x402";
const X402_PRICING = {
  amount_usd: 0.01,
  asset: "USDC",
  asset_contract: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC on Base
  chain: "base",
  network: "eip155:8453",
  pay_to: "0x79DC34E41B2b591078d3dE222C43EcaaBD52FcCB", // Graph x402 gateway
  scheme: "exact",
  asset_transfer_method: "eip3009",
};

function buildQueryEndpoints(subgraphId) {
  return {
    // The keyed gateway URL. This used to carry `[api-key]` as a path segment,
    // a form the gateway no longer uses — an agent that string-replaced the
    // placeholder was building a URL that has not been correct for a while.
    // The current form takes the key in a header:
    //   POST https://gateway.thegraph.com/api/subgraphs/id/<ID>
    //   Authorization: Bearer <STUDIO_KEY>
    // Verified: without the header this returns HTTP 200 carrying a GraphQL
    // error body, `auth error: missing authorization header` — GraphQL signals
    // auth in the body, so do not treat 200 as success without reading it.
    query_url: `https://gateway.thegraph.com/api/subgraphs/id/${subgraphId}`,
    query_url_x402: `${X402_GATEWAY_BASE}/subgraphs/id/${subgraphId}`,

    // Both routes, stated side by side, because which one is right depends
    // entirely on what the caller already has. An agent embedded in a product
    // with a Studio key should use its key; a headless agent with a funded
    // wallet and no way to mint a key should use x402. Neither is "the
    // recommended one" — the previous wording put x402 first and labelled it
    // RECOMMENDED, which sent key-holding agents down a payment path they had
    // no reason to take, and which some hosts forbid outright.
    payment_options: {
      api_key: {
        url: `https://gateway.thegraph.com/api/subgraphs/id/${subgraphId}`,
        method: "POST",
        auth_header: "Authorization: Bearer <STUDIO_API_KEY>",
        get_a_key: "https://thegraph.com/studio/apikeys/",
        cost: "included in your Studio plan (100K free queries/month)",
        use_when: "you already have, or can obtain, a Graph Studio API key",
      },
      x402: {
        url: `${X402_GATEWAY_BASE}/subgraphs/id/${subgraphId}`,
        method: "POST",
        cost: "$0.01 USDC on Base per query",
        flow: "gateway returns HTTP 402 with a payment manifest; an x402 client (@graphprotocol/client-x402, x402-fetch) signs and retries automatically",
        use_when: "you have a funded wallet and no API key, and no human to mint one",
      },
    },
    pricing: X402_PRICING,
  };
}

// ── Download DB from GitHub if missing ─────────────────────

function sha256OfFile(path) {
  const h = createHash("sha256");
  h.update(readFileSync(path));
  return h.digest("hex");
}

function verifyDbOrThrow(path) {
  if (SKIP_VERIFY) {
    console.error(
      "SUBGRAPH_REGISTRY_SKIP_VERIFY=1 — skipping registry.db hash check."
    );
    return;
  }
  const actual = sha256OfFile(path);
  if (actual !== EXPECTED_DB_SHA256) {
    // Refuse to load a registry that doesn't match the known-good hash.
    // Delete the file so the next run gets a fresh download attempt instead
    // of caching a poisoned copy.
    try { unlinkSync(path); } catch (_) {}
    throw new Error(
      `registry.db SHA-256 mismatch.\n` +
        `  expected: ${EXPECTED_DB_SHA256}\n` +
        `  actual:   ${actual}\n` +
        `The downloaded registry does not match the version pinned to this ` +
        `npm package. Refusing to load. If you intentionally rebuilt the DB ` +
        `locally, set SUBGRAPH_REGISTRY_SKIP_VERIFY=1 to bypass.`
    );
  }
}

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const follow = (u) => {
      httpsGet(u, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          follow(res.headers.location);
          return;
        }
        if (res.statusCode !== 200) {
          reject(new Error(`Download failed: HTTP ${res.statusCode}`));
          return;
        }
        const chunks = [];
        res.on("data", (chunk) => chunks.push(chunk));
        res.on("end", () => {
          writeFileSync(dest, Buffer.concat(chunks));
          resolve();
        });
        res.on("error", reject);
      }).on("error", reject);
    };
    follow(url);
  });
}

async function ensureDb() {
  if (existsSync(DB_PATH)) {
    verifyDbOrThrow(DB_PATH);
    return;
  }
  // The npm package and the git repo both ship data/registry.db, so this path
  // only runs on a damaged install. Fail closed unless explicitly opted in.
  if (process.env.SUBGRAPH_REGISTRY_ALLOW_DB_DOWNLOAD !== "1") {
    throw new Error(
      `registry.db not found at ${DB_PATH}. Reinstall ${PINNED_NPX_PACKAGE} (it bundles the database). ` +
      "To fetch it from GitHub instead (hash-verified), set SUBGRAPH_REGISTRY_ALLOW_DB_DOWNLOAD=1.",
    );
  }
  mkdirSync(DATA_DIR, { recursive: true });
  console.error("Registry not found locally. Downloading from GitHub (SUBGRAPH_REGISTRY_ALLOW_DB_DOWNLOAD=1)...");
  await downloadFile(GITHUB_DB_URL, DB_PATH);
  console.error("Downloaded registry.db — verifying SHA-256...");
  verifyDbOrThrow(DB_PATH);
  console.error("Registry verified OK.");
}

// ── Database ───────────────────────────────────────────────

let db;

function getDb() {
  if (!db) {
    db = new Database(DB_PATH, { readonly: true });
  }
  return db;
}

// ── Network aliases ────────────────────────────────────────
// The corpus stores graph-node's chain IDs (`mainnet`, `arbitrum-one`,
// `matic`), but every human and every model says "ethereum", "arbitrum",
// "polygon" — and so does our own auto_description, which prints the pretty
// name from classifier.py NETWORK_NAMES. So an agent reads "Ethereum" in a
// description, passes network:"ethereum" back, and gets zero results with no
// error. SKILL.md made it worse by documenting `ethereum, arbitrum, base` as
// the example values; two of those three matched nothing.
// mainnet/bsc/arbitrum-one/matic alone are ~45% of the corpus.
const NETWORK_ALIASES = {
  "arc-mainnet": "arc",
  "arc mainnet": "arc",
  "arc testnet": "arc-testnet",
  ethereum: "mainnet",
  eth: "mainnet",
  "ethereum-mainnet": "mainnet",
  arbitrum: "arbitrum-one",
  "arbitrum one": "arbitrum-one",
  arb: "arbitrum-one",
  polygon: "matic",
  "polygon-pos": "matic",
  bnb: "bsc",
  "bnb-chain": "bsc",
  "binance-smart-chain": "bsc",
  binance: "bsc",
  op: "optimism",
  "optimism-mainnet": "optimism",
  avax: "avalanche",
  "avalanche-c-chain": "avalanche",
  xdai: "gnosis",
  zksync: "zksync-era",
  "zksync era": "zksync-era",
  blast: "blast-mainnet",
  "polygon-zk": "polygon-zkevm",
  near: "near-mainnet",
  mode: "mode-mainnet",
  sei: "sei-mainnet",
  ftm: "fantom",
};

// Normalize a caller-supplied chain name to the value stored in the corpus.
// Unknown values pass through untouched so a legitimate new chain still works.
function normalizeNetwork(name) {
  if (!name || typeof name !== "string") return name;
  const k = name.trim().toLowerCase();
  return NETWORK_ALIASES[k] || k;
}

// Networks the corpus actually contains, so a chain word in a goal can be told
// apart from a protocol that happens to share a chain's name. Built once from
// the DB rather than hardcoded, so a new chain in a re-crawl works immediately.
let _knownNetworks = null;
const KNOWN_NETWORKS = {
  has(name) {
    if (!name) return false;
    if (_knownNetworks === null) {
      try {
        _knownNetworks = new Set(
          getDb().prepare("SELECT DISTINCT network FROM subgraphs WHERE network IS NOT NULL")
            .all().map((r) => r.network),
        );
      } catch {
        _knownNetworks = new Set();
      }
    }
    return _knownNetworks.has(name);
  },
};

// ── Testnets ───────────────────────────────────────────────
// 723 of the 5,425 served, non-denied subgraphs (13.3%) are on testnets, and
// they compete directly with production because a testnet deployment's text is
// near-identical to its mainnet twin's — that is exactly how ENS Sepolia (58
// queries/30d) came to outrank ENS mainnet (34.8M queries/30d).
//
// Detected from the network name rather than a new column, so it works on the
// corpus already shipped. All 57 matching networks were checked by hand; the
// six without an explicit -testnet/-sepolia/-goerli suffix (chapel, fuji,
// holesky, holesky-beacon, mumbai, polygon-amoy) are the well-known BSC,
// Avalanche, Ethereum and Polygon testnets.
const TESTNET_MARKERS = [
  "sepolia", "goerli", "testnet", "devnet", "chapel", "fuji",
  "holesky", "mumbai", "amoy", "baobab", "rinkeby", "kovan",
];

function isTestnetNetwork(name) {
  if (!name) return false;
  const n = String(name).toLowerCase();
  return TESTNET_MARKERS.some((m) => n.includes(m));
}

// SQL fragment excluding testnets. Static string — the markers are a constant
// allowlist, never caller input, so there is nothing to bind or escape.
const NOT_TESTNET_SQL = TESTNET_MARKERS.map(
  (m) => `network NOT LIKE '%${m}%'`,
).join(" AND ");

// Whether to hide testnets for this call.
//
// The trap: a caller who explicitly asks for network:"sepolia" must not get an
// empty result because a default filter silently contradicts their request.
// An explicit testnet network always wins over the default exclusion.
function shouldExcludeTestnets({ include_testnets, network }) {
  if (include_testnets) return false;
  if (network && isTestnetNetwork(normalizeNetwork(network))) return false;
  return true;
}

// Tokenize a free-text query into searchable terms.
//
// The old inline version was `.filter((w) => w.length > 2)`, which silently
// dropped every protocol version token — "v2", "v3", "v4" are all two chars.
// That made "uniswap v3" byte-identical to "uniswap", so the single most
// natural way to disambiguate the largest protocol family in the corpus did
// nothing at all. Keep the length floor for noise words, but let version
// tokens through.
const VERSION_TOKEN_RE = /^v\d+$/;

// Function words carry no signal about WHICH subgraph is wanted, and because
// matching is substring-based they actively mislead: "reputation scores for
// onchain agents" scored forsage-x2-prod above agent0, because "for" is inside
// "forsage" and a display-name hit is worth 4 while agent0's two real matches
// ("reputation", "agents", in the description) were worth 1 each. Dropping them
// costs nothing — no one distinguishes two subgraphs by the word "the".
const STOPWORDS = new Set([
  "the", "and", "for", "with", "from", "that", "this", "are", "was", "were",
  "get", "all", "any", "how", "what", "which", "who", "into", "onto", "over",
  "per", "via", "out", "its", "their", "your", "our", "his", "her",
  "show", "give", "find", "list", "want", "need", "using", "use", "used",
  "data", "info", "about", "some", "more", "most", "have", "has", "had",
]);

// Tokens that describe a CATEGORY rather than a protocol. They are real words a
// caller means, so they cannot be dropped like stopwords — but on their own they
// select the wrong thing, because the corpus is full of subgraphs whose names
// happen to contain them.
//
// Measured on the live corpus: "rocket pool" put Venus Core Pool, Thena BSC
// Weighted Pool, "pool factory" and Linked Pool BSC above Rocket Pool itself, on
// the strength of "pool" alone plus reliability. "Blur NFT marketplace" returned
// Heroes Nft Marketplace at #1 and never surfaced Blur. "Safe / Gnosis Safe"
// returned HOPR Nodes, which merely has "Safe" in its description.
//
// So a noise token may CONTRIBUTE to a score, but it may never be the only
// reason a row is in the candidate set.
const NOISE_TOKENS = new Set([
  "pool", "pools", "volume", "volumes", "floor", "safe", "bridge", "token",
  "tokens", "market", "markets", "marketplace", "price", "prices", "history",
  "protocol", "protocols", "network", "chain", "dex", "nft", "nfts", "swap",
  "swaps", "stake", "staking", "staked", "lending", "lend", "borrow",
  "liquidity", "yield", "vault", "vaults", "tvl", "stats", "analytics",
  "activity", "subgraph", "subgraphs", "top", "highest", "largest", "biggest",
  "best", "total", "current", "latest", "recent",
]);

// "highest volume", "most queried", "top TVL" — the caller is asking for scale,
// so 30d query volume becomes a ranking signal rather than a tie-break.
const VOLUME_INTENT_RE =
  /\b(volume|tvl|highest|most|largest|biggest|top|busiest|popular|liquidity)\b/;

// A chain word is routing information when it follows a preposition ("on base",
// "in ethereum"). Without one it may simply be part of a protocol's name —
// "Gnosis Safe" is a product, not a request for the Gnosis chain, and treating
// it as a filter returned HOPR Nodes on gnosis instead of Safe.
const CHAIN_PREP_RE = /\b(on|in|at|for|across)\s+$/;

function queryTerms(query, limit = 5) {
  return query
    .trim()
    .toLowerCase()
    .split(/\s+/)
    .filter((w) => (w.length > 2 || VERSION_TOKEN_RE.test(w)) && !STOPWORDS.has(w))
    .slice(0, limit);
}

// Re-rank candidates on WORD boundaries, which SQL LIKE cannot express.
//
// The SQL score treats any substring of a display name as a name hit, so
// "scores" scored scoresquare-base at full name weight and "for" scored
// forsage-x2-prod, both beating genuine description matches. A term that
// appears as a whole word is a real signal; a term that is merely a prefix of
// a longer word is not.
//
// Shared by search_subgraphs and recommend_subgraph. It lived only in
// recommend, which is why `search_subgraphs("reputation scores for onchain
// agents")` still returned scoresquare-base at #1 while recommend did not —
// two tools disagreeing because a fix was applied to one of them.
function boundaryRerank(rows, words, tieBreak = null, phrases = []) {
  if (!words.length) return rows;
  const res = words.map(
    (w) => new RegExp("(^|[^a-z0-9])" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "([^a-z0-9]|$)", "i"),
  );
  const score = (r) => {
    const name = r.display_name || "";
    const text = `${r.description || ""} ${r.auto_description || ""}`;
    // An exact protocol name should beat a longer, similarly named fork.
    let out = (name.trim().toLowerCase() === words.join(" ") ||
      words.some(w => !NOISE_TOKENS.has(w) && name.trim().toLowerCase() === w)) ? 20 : 0;
    // A whole-phrase name hit outranks any accumulation of single tokens.
    // Without this the SQL phrase boost was silently undone here: "compound v3"
    // re-ranked on the token "compound" alone, every Compound tied, and
    // reliability promoted Compound V2 over the V3 the caller asked for.
    const flatName = name.toLowerCase().replace(/[-_.]+/g, " ").replace(/\s+/g, " ");
    const tightName = flatName.replace(/ /g, "");
    for (const ph of phrases) {
      if (flatName.includes(ph) || tightName.includes(ph.replace(/ /g, ""))) out += 15;
    }
    res.forEach((re, i) => {
      if (re.test(name)) out += 6;
      else if (name.toLowerCase().includes(words[i])) out += 1;
      if (re.test(text)) out += 2;
    });
    return out;
  };
  return rows
    .map((r) => ({ r, s: score(r) }))
    .sort(
      (a, b) =>
        b.s - a.s ||
        // On a "highest volume" goal, scale is the answer the caller asked for,
        // so it outranks accrued reliability inside an equal-relevance band.
        (tieBreak ? tieBreak(a.r, b.r) : 0) ||
        (b.r.reliability_score || 0) - (a.r.reliability_score || 0),
    )
    .map((x) => x.r);
}

// ── Maturity / cold-start handling ─────────────────────────
// reliability_score combines snapshot/traction inputs (curation signal,
// indexer stake, lifetime query fees, 30d volume — see _reliability_score in
// python/classifier.py); its observed age bias is not a health measurement.
// Measured on the 2026-08-25 corpus, served and non-denied:
//
//   age      n      avg reliability
//   <30d     64     0.107
//   30-90d   227    0.143
//   90-365d  1100   0.225
//   >1y      4034   0.313
//
// The newest entry in the global top 25 is 280 days old. A good subgraph
// deployed last month cannot rank, no matter how good it is — 59 of those 64
// sub-30-day subgraphs are already serving real query volume.
//
// Rather than reweight the score (which would silently change every existing
// caller's results and trade a measurable signal for a guess), surface the
// young matches SEPARATELY and label them honestly, so the agent makes the
// call. A label alone would not be enough: at 0.107 average, young subgraphs
// are not in the ranked page to be labelled, so this needs its own lookup.
const EMERGING_MAX_AGE_DAYS = 90;
const NEW_MAX_AGE_DAYS = 30;
const EMERGING_LIMIT = 3;

// Shared so the main search and its emerging companion query select exactly
// the same columns — they feed the same row mapper.
const SEARCH_COLS = `id, display_name, description, auto_description, domain, protocol_type, network,
           reliability_score, ipfs_hash, entity_count, canonical_entities,
           powered_by_substreams, active_allocation_count, example_query, denied_at, created_at,
           query_volume_30d, updated_at`;

function ageDays(created_at) {
  if (!created_at) return null;
  return Math.max(0, Math.floor(Date.now() / 1000 - created_at) / 86400) | 0;
}

function maturityOf(created_at) {
  const d = ageDays(created_at);
  if (d === null) return "unknown";
  if (d < NEW_MAX_AGE_DAYS) return "new";
  if (d < EMERGING_MAX_AGE_DAYS) return "emerging";
  return "established";
}

const EMERGING_CAVEAT =
  "Recent matching deployments outside the primary returned page. " +
  "Ranking combines snapshot curation/stake, lifetime query fees and rolling " +
  "30-day volume; this traction-weighted score can favor established entries. " +
  "A low score is not proof of poor health, missing rewards or unavailable " +
  "queries. Inspect relevance, age and measured health separately; neither " +
  "this companion list nor the primary ranking validates live queryability.";


// Young matches for the same filter, fetched separately because they cannot
// compete on the main ORDER BY. Returns [] on any failure — this is an
// enrichment, and it must never take down the search that already succeeded.
function findEmerging(where, params, excludeIds, selectCols) {
  try {
    const cutoff = Math.floor(Date.now() / 1000) - EMERGING_MAX_AGE_DAYS * 86400;
    const notIn = excludeIds.length
      ? ` AND id NOT IN (${excludeIds.map(() => "?").join(",")})`
      : "";
    const sql = `
      SELECT ${selectCols}
      FROM subgraphs
      ${where ? `${where} AND` : "WHERE"} created_at > ?${notIn}
      ORDER BY reliability_score DESC
      LIMIT ?
    `;
    return getDb()
      .prepare(sql)
      .all(...params, cutoff, ...excludeIds, EMERGING_LIMIT);
  } catch {
    return [];
  }
}

// ── Tool Implementations ───────────────────────────────────

// Discovery input schemas are documentation unless checked at runtime. In
// particular SQLite LIMIT -1 is unbounded, and string "false" is truthy.
function validateDiscoveryInput(args, kind = "search") {
  if (!args || typeof args !== "object" || Array.isArray(args)) return "arguments must be an object";
  const strings = kind === "recommend" ? ["goal", "chain"] :
    ["query", "domain", "network", "protocol_type", ...(kind === "semantic" ? [] : ["entity"])];
  const booleans = kind === "recommend" ? [] : ["include_unserved", "include_denied", "include_testnets"];
  const allowed = new Set([...strings, ...booleans, ...(kind === "recommend" ? [] : ["limit", "min_reliability"]), ...(kind === "semantic" ? ["min_score"] : [])]);
  for (const key of Object.keys(args)) {
    if (!allowed.has(key)) return `Unsupported argument: ${key}${["offset", "cursor", "page"].includes(key) ? "; pagination is not supported" : ""}`;
  }
  for (const key of strings) {
    if (args[key] !== undefined && (typeof args[key] !== "string" || args[key].length > 1000)) {
      return `${key} must be a string of at most 1000 characters`;
    }
  }
  if (kind === "recommend" && !args.goal?.trim()) return "goal must be a non-empty string";
  if (kind === "semantic" && !args.query?.trim()) return "query must be a non-empty string";
  if (kind === "semantic" && args.min_score !== undefined && (!Number.isFinite(args.min_score) || args.min_score < 0 || args.min_score > 1)) return "min_score must be a number from 0 to 1";
  for (const key of booleans) {
    if (args[key] !== undefined && typeof args[key] !== "boolean") return `${key} must be boolean`;
  }
  if (args.limit !== undefined && (!Number.isInteger(args.limit) || args.limit < 1 || args.limit > (kind === "semantic" ? 50 : 100))) {
    return `limit must be an integer from 1 to ${kind === "semantic" ? 50 : 100}`;
  }
  if (args.min_reliability !== undefined && (!Number.isFinite(args.min_reliability) ||
      args.min_reliability < 0 || args.min_reliability > 1)) return "min_reliability must be a number from 0 to 1";
  return null;
}

const ALLOCATION_CAVEAT = "Allocation counts, curation signal, denied rewards and reliability are snapshot discovery signals, NOT a live queryability test. Zero allocations or no indexing rewards does not prove a deployment cannot be queried; positive allocations do not prove it is healthy. Discovery never probes a gateway.";

const STUDIO_KEYS_URL = "https://thegraph.com/studio/apikeys/";
const KEY_RELAY_MESSAGE =
  "To let me run live queries on The Graph with your own quota: sign in to Subgraph Studio " +
  `(${STUDIO_KEYS_URL}) with a Studio account you manage, create an API key, and add it to this ` +
  "MCP server's environment or secret manager as THE_GRAPH_STUDIO_API_KEY, then restart the server. " +
  "Please don't paste the key into this chat. Studio pricing currently lists 100,000 free queries per " +
  "month; check your plan and remaining allowance.";

function executionNextAction(hasCandidates = true) {
  const configured = Boolean(studioApiKey());
  return {
    action: !hasCandidates ? "broaden_discovery_before_execution" : configured ? "prepare_then_explicitly_execute" : "configure_api_key_before_execution",
    credentials: configured ? "configured_not_validated" : "not_configured",
    prepare_tool: "query_for_goal",
    api_key: {
      create_url: STUDIO_KEYS_URL,
      who: "human_operator",
      setup: "Requires a Studio account managed by a person: the human operator creates/manages the key in Studio and stores it in the MCP host's secret manager as THE_GRAPH_STUDIO_API_KEY, then restarts the server. Agents should not create accounts or keys; never paste it in chat, tool arguments, source or logs.",
      ...(configured ? {} : { relay_to_human: KEY_RELAY_MESSAGE }),
      header: "Authorization: Bearer <STUDIO_API_KEY>",
      free_plan: "Official Studio pricing currently advertises 100,000 free queries per month; check your account's remaining allowance and plan. This is not a per-key guarantee or a quota check.",
      pricing_url: "https://thegraph.com/studio-pricing/",
    },
    execution: "Inspect query relevance and schema before opting in. HTTP 200 can contain GraphQL errors; check errors and data. No query has been executed by discovery.",
    paid_alternative: "x402 is a separate explicitly paid route; this server never signs or auto-pays it.",
  };
}

// Copy-paste setup for a human operator. Placeholders only: the server never
// reads, echoes or stores a key in tool output.
function keyOnboarding(request) {
  return {
    who: "human_operator",
    relay_to_human: KEY_RELAY_MESSAGE,
    steps: [
      `Sign in to Subgraph Studio with an account you manage and create an API key at ${STUDIO_KEYS_URL}`,
      "Store it in the MCP host's secret manager / environment as THE_GRAPH_STUDIO_API_KEY (not in chat, source or logs)",
      "Restart this MCP server; execute-capable tools then appear in tools/list",
      "Call query_for_goal again with validate_schema:true and execute:true",
    ],
    mcp_config_example: { mcpServers: { "subgraph-registry": { command: "npx", args: ["-y", PINNED_NPX_PACKAGE],
      env: { THE_GRAPH_STUDIO_API_KEY: "<set from your host's secret manager>" } } } },
    ...(request ? { curl_example: `curl -sS -X POST '${request.query_url}' -H 'Content-Type: application/json' -H "Authorization: Bearer $THE_GRAPH_STUDIO_API_KEY" --data '${JSON.stringify(request.body).replace(/'/g, "'\\''")}'` } : {}),
    alternatives: "Without a key, discovery and query preparation still work. x402 is a separate, explicitly paid route; this server never signs or auto-pays it.",
  };
}

function searchSubgraphs(args = {}) {
  const invalid = validateDiscoveryInput(args);
  if (invalid) return { error: invalid };
  let {
    query = "", domain = "", network = "", protocol_type = "", entity = "",
    min_reliability = 0, include_unserved = false, include_denied = false,
    include_testnets = false, limit = 20,
  } = args;
  const requestedNetwork = network;
  let inferredNetwork = null;
  // Only a standalone known chain/alias is routing intent. An explicit
  // network always wins: query:"arc", network:"mainnet" can mean Aave ARC.
  if (!network && query.trim() && KNOWN_NETWORKS.has(normalizeNetwork(query))) {
    inferredNetwork = normalizeNetwork(query);
    network = inferredNetwork;
    query = "";
  }
  const conditions = [];
  const params = [];

  // Compatibility discovery filter, NOT proof of query failure. Studio or
  // other serving routes can exist without on-chain active allocations.
  if (!include_unserved) {
    conditions.push("active_allocation_count > 0");
  }

  // Default: hide curation-denied deployments (deniedAt > 0 on the network
  // subgraph — denied indexing rewards, not a live serving or safety verdict). classifier.py has persisted this since the denied_at
  // column landed, explicitly "so agents can filter denied subgraphs", but
  // nothing in this file ever read it, so the filter the crawler was feeding
  // did not exist. The 0.5 reliability penalty already keeps denied entries
  // out of the top of a ranked page — measured: 0 of the global top 20, and
  // none in any domain's top 10 — so this changes few results today. It
  // matters for the narrow queries where a denied fork IS the best textual
  // match, and it makes the signal visible either way via `denied` below.
  if (!include_denied) {
    conditions.push("denied_at = 0");
  }
  if (shouldExcludeTestnets({ include_testnets, network })) {
    conditions.push(`(${NOT_TESTNET_SQL})`);
  }

  const visibilityConditionCount = conditions.length;
  if (domain) {
    conditions.push("domain = ?");
    params.push(domain);
  }
  if (network) {
    conditions.push("network = ?");
    params.push(normalizeNetwork(network));
  }
  if (protocol_type) {
    conditions.push("protocol_type = ?");
    params.push(protocol_type);
  }
  if (entity) {
    conditions.push('canonical_entities LIKE ?');
    params.push(`%"${entity}"%`);
  }
  if (min_reliability > 0) {
    conditions.push("reliability_score >= ?");
    params.push(min_reliability);
  }
  // Terms are OR'd for recall, then RANKED by how many of them matched.
  //
  // Before this, a multi-word query OR'd its terms and ordered the result by
  // reliability alone, so a high-reliability subgraph matching ONE incidental
  // word beat a lower-reliability one matching all three. The effect was that
  // being more specific made the answer worse: "aave lending arbitrum"
  // returned uniswap-v3-arbitrum, Arbitrum Minimal, camelot-amm-v3 and Graph
  // TAP — not one Aave subgraph — while the bare query "aave" was correct.
  //
  // Keep the OR (dropping to AND would kill recall on descriptions that
  // phrase things differently) and let matched_terms break the tie first.
  //
  // A hit in display_name is worth 3, a hit in the description 1. Counting
  // them equally is not enough on short terms, where LIKE '%term%' matches
  // half the corpus incidentally: searching "ens" scored ENS and four Uniswap
  // subgraphs at 1 apiece — "tokens" contains "ens" — and reliability then
  // handed the top slots to Uniswap. Weighting the name restores ENS to #1
  // without narrowing what still gets found.
  const matchParams = [];
  let matchExpr = "0";
  if (query) {
    const words = queryTerms(query);
    if (words.length) {
      matchExpr = words
        .map(() => "((CASE WHEN display_name LIKE ? THEN 3 ELSE 0 END) + (CASE WHEN (description LIKE ? OR auto_description LIKE ?) THEN 1 ELSE 0 END))")
        .join(" + ");
      words.forEach((w) => matchParams.push(`%${w}%`, `%${w}%`, `%${w}%`));

      const wordConds = words.map(() => "(display_name LIKE ? OR description LIKE ? OR auto_description LIKE ?)");
      words.forEach((w) => params.push(`%${w}%`, `%${w}%`, `%${w}%`));
      conditions.push(`(${wordConds.join(" OR ")})`);
    } else {
      conditions.push("(display_name LIKE ? OR description LIKE ? OR auto_description LIKE ?)");
      params.push(`%${query}%`, `%${query}%`, `%${query}%`);
    }
  }

  const scopeConditions = conditions.slice(visibilityConditionCount);
  const scopeWhere = scopeConditions.length ? `WHERE ${scopeConditions.join(" AND ")}` : "";
  const where = conditions.length ? `WHERE ${conditions.join(" AND ")}` : "";
  // Over-fetch to allow dedup by IPFS hash (same deployment, different subgraph IDs)
  const fetchLimit = limit * 3;
  const sql = `
    SELECT ${SEARCH_COLS}, (${matchExpr}) AS matched_terms
    FROM subgraphs
    ${where}
    ORDER BY matched_terms DESC, reliability_score DESC
    LIMIT ?
  `;
  // Snapshot the filter params BEFORE the LIMIT is appended — the emerging
  // companion query reuses the same WHERE and must not inherit this LIMIT.
  const filterParams = [...params];

  // Positional binding order: the SELECT-clause scoring expression is bound
  // before the WHERE clause, so matchParams must lead. filterParams stays
  // WHERE-only, which is what the emerging companion query needs.
  const rows = boundaryRerank(
    getDb().prepare(sql).all(...matchParams, ...filterParams, fetchLimit),
    query ? queryTerms(query) : [],
  );
  // Dedup by IPFS hash — keep highest reliability per deployment
  const seenIpfs = new Set();
  const results = [];
  for (const r of rows) {
    if (r.ipfs_hash && seenIpfs.has(r.ipfs_hash)) continue;
    if (r.ipfs_hash) seenIpfs.add(r.ipfs_hash);
    results.push({
      id: r.id,
      display_name: r.display_name,
      description: (r.description || r.auto_description || "").slice(0, 300),
      domain: r.domain,
      protocol_type: r.protocol_type,
      network: r.network,
      reliability_score: r.reliability_score,
    // The registry has this number and the official Graph MCP's
    // get_deployment_30day_query_counts was observed returning 0 for
    // deployments that plainly serve traffic, so it could not break ties
    // between a real protocol and its forks. Surfacing it here is what lets a
    // caller tell Lido (4.7M queries/30d) from lido-copy.
    query_volume_30d: r.query_volume_30d ?? null,
      ipfs_hash: r.ipfs_hash,
      entity_count: r.entity_count,
      canonical_entities: JSON.parse(r.canonical_entities),
      powered_by_substreams: Boolean(r.powered_by_substreams),
      active_allocation_count: r.active_allocation_count || 0,
      // Curation-denied on the network subgraph. Only ever true when the
      // caller passed include_denied — surfaced so that choice stays visible
      // in the result rather than being silently carried.
      denied: Boolean(r.denied_at),
      testnet: isTestnetNetwork(r.network),
      // Ready-to-run GraphQL generated from this subgraph's actual schema — so an
      // agent can POST it to query_url_x402 immediately, no get_subgraph_detail round-trip.
      example_query: r.example_query || null,
      age_days: ageDays(r.created_at),
      maturity: maturityOf(r.created_at),
      freshness: freshnessFor(r),
      ...buildQueryEndpoints(r.id),
    });
    if (results.length >= limit) break;
  }

  // Young matches that could not compete on the cumulative score. Same filter,
  // separate lookup, clearly labelled — never blended into `subgraphs`, so a
  // caller that ignores this field sees exactly what it saw before.
  const emerging = findEmerging(
    where,
    filterParams,
    results.map((x) => x.id),
    SEARCH_COLS,
  ).map((r) => ({
    id: r.id,
    display_name: r.display_name,
    description: (r.description || r.auto_description || "").slice(0, 300),
    domain: r.domain,
    protocol_type: r.protocol_type,
    network: r.network,
    reliability_score: r.reliability_score,
    // The registry has this number and the official Graph MCP's
    // get_deployment_30day_query_counts was observed returning 0 for
    // deployments that plainly serve traffic, so it could not break ties
    // between a real protocol and its forks. Surfacing it here is what lets a
    // caller tell Lido (4.7M queries/30d) from lido-copy.
    query_volume_30d: r.query_volume_30d ?? null,
    ipfs_hash: r.ipfs_hash,
    entity_count: r.entity_count,
    canonical_entities: JSON.parse(r.canonical_entities),
    powered_by_substreams: Boolean(r.powered_by_substreams),
    active_allocation_count: r.active_allocation_count || 0,
    denied: Boolean(r.denied_at),
    testnet: isTestnetNetwork(r.network),
    example_query: r.example_query || null,
    age_days: ageDays(r.created_at),
    maturity: maturityOf(r.created_at),
    freshness: freshnessFor(r),
    ...buildQueryEndpoints(r.id),
  }));

  let diagnostics;
  if (!results.length) {
    const counts = getDb().prepare(`SELECT COUNT(*) AS matching_records,
      SUM(CASE WHEN active_allocation_count <= 0 THEN 1 ELSE 0 END) AS no_active_allocation,
      SUM(CASE WHEN denied_at != 0 THEN 1 ELSE 0 END) AS curation_denied,
      SUM(CASE WHEN network IS NULL THEN 1 ELSE 0 END) AS unknown_network,
      SUM(CASE WHEN NOT (${NOT_TESTNET_SQL}) THEN 1 ELSE 0 END) AS testnet
      FROM subgraphs ${scopeWhere}`).get(...filterParams);
    diagnostics = {
      matching_records_before_visibility_filters: counts.matching_records,
      excluded_by: {
        no_active_allocation: include_unserved ? 0 : counts.no_active_allocation || 0,
        curation_denied: include_denied ? 0 : counts.curation_denied || 0,
        testnet: shouldExcludeTestnets({ include_testnets, network }) ? counts.testnet || 0 : 0,
        unknown_network: shouldExcludeTestnets({ include_testnets, network }) ? counts.unknown_network || 0 : 0,
      },
      counts_overlap: true,
      ...(!include_unserved && counts.no_active_allocation > 0 ? {
        suggested_retry: {
          tool: "search_subgraphs",
          arguments: { ...args, query, network, include_unserved: true },
          effect: "Discovery only: include zero-allocation snapshot records, not verified live endpoints. Other filters remain unchanged.",
        },
      } : {}),
      network_known_in_snapshot: network ? KNOWN_NETWORKS.has(normalizeNetwork(network)) : null,
      ...(network && !KNOWN_NETWORKS.has(normalizeNetwork(network)) ? {
        available_networks: getDb().prepare("SELECT DISTINCT network FROM subgraphs WHERE network IS NOT NULL ORDER BY network").all().map(r => r.network),
      } : {}),
      next_step: counts.matching_records ? "Inspect excluded_by and opt in to the relevant include_* flag for discovery; availability is still unverified." :
        "No matching record in this snapshot. Check network spelling or broaden text filters; absence is not proof no deployment exists. Studio-only deployments may be outside this corpus.",
    };
  }
  return {
    total: results.length,
    // total remains returned-count for compatibility; no pagination is implied.
    total_is_returned_count: true,
    network_filter: network ? normalizeNetwork(network) : null,
    inferred_network: inferredNetwork,
    requested_network: requestedNetwork || null,
    discovery_filters: {
      require_positive_allocation: !include_unserved, exclude_denied: !include_denied,
      exclude_testnets: shouldExcludeTestnets({ include_testnets, network }),
      caveat: ALLOCATION_CAVEAT,
    },
    ...(diagnostics ? { diagnostics } : {}),
    next_action: executionNextAction(results.length > 0),
    subgraphs: results,
    ...(emerging.length
      ? { emerging, emerging_caveat: EMERGING_CAVEAT }
      : {}),
    query_instructions: "This registry does DISCOVERY, not execution — search never POSTs GraphQL. It hands you the subgraph id and a ready-to-run `example_query`. Optional next step: call `execute_query` with that id and query (opt-in; requires THE_GRAPH_STUDIO_API_KEY or you POST yourself). For the schema, call `get_schema` (local entities always; live __schema only with a key). Two equally valid routes if you run it yourself: (a) API KEY — POST to `query_url` with header `Authorization: Bearer <STUDIO_API_KEY>` (get one at https://thegraph.com/studio/apikeys/, 100K free queries/month). Note the gateway returns HTTP 200 with a GraphQL error body when the header is missing, so read the body. (b) x402 — POST to `query_url_x402` and pay $0.01 USDC on Base per query, no key and no signup; the gateway answers 402 with a payment manifest and an x402 client signs and retries. Use (a) if you hold a key, (b) if you are headless with a funded wallet. If your client already has an official Graph MCP or gateway connector, just pass it the `id` from this result and ignore both URLs. See `payment_options` for the full shape of each.",
  };
}

function recommendSubgraph(args = {}) {
  const invalid = validateDiscoveryInput(args, "recommend");
  if (invalid) return { error: invalid };
  const { goal, chain = "" } = args;
  const goalLower = goal.toLowerCase();

  const domainMap = {
    defi: ["defi", "swap", "trade", "lend", "borrow", "yield", "stake", "liquidity", "pool", "token"],
    nfts: ["nft", "collectible", "art", "marketplace"],
    dao: ["governance", "vote", "proposal", "dao"],
    identity: ["ens", "domain", "name", "identity"],
    infrastructure: ["indexer", "graph", "oracle"],
    social: ["social", "profile", "post", "lens"],
    gaming: ["game", "player", "quest"],
  };
  const typeMap = {
    dex: ["dex", "swap", "trade", "exchange", "amm", "uniswap", "sushi"],
    lending: ["lend", "borrow", "loan", "collateral", "aave", "compound"],
    bridge: ["bridge", "cross-chain"],
    staking: ["stake", "validator", "delegation"],
    // "call", "put" and "strike" are gone. They are ordinary English words —
    // "reputation" contains "put", so the goal "reputation scores for onchain
    // agents" inferred protocol_type ["options"] and returned the Polygon
    // Optimistic Oracle. "option" alone is specific enough to keep.
    options: ["option", "derivatives contract"],
    perpetuals: ["perp", "perpetual", "leverage", "margin"],
    governance: ["governance", "vote", "proposal"],
    "name-service": ["ens", "name service", "domain name"],
    "nft-marketplace": ["nft market", "opensea", "blur"],
  };

  // Match on word boundaries, not bare substrings. Boundaries alone would not
  // have saved "reputation"/"put" if "put" had stayed in the list — hence the
  // removals above and the demotion from filter to bonus below — but they do
  // stop "smart contract" inferring nfts via "art", and "start"/"chart"/
  // "party" doing the same.
  const hitsGoal = (kws) =>
    kws.some((k) =>
      new RegExp(`\\b${k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`).test(goalLower),
    );
  const domains = Object.entries(domainMap)
    .filter(([, kws]) => hitsGoal(kws))
    .map(([d]) => d);
  const ptypes = Object.entries(typeMap)
    .filter(([, kws]) => hitsGoal(kws))
    .map(([t]) => t);

  // recommend_subgraph exposes no include_* escape hatches — it answers "which
  // one should I use" under conservative snapshot filters. Reward denial
  // does not prove query failure; search exposes the opt-in discovery path.
  const conditions = ["active_allocation_count > 0", "denied_at = 0"];
  if (shouldExcludeTestnets({ include_testnets: false, network: chain })) {
    conditions.push(`(${NOT_TESTNET_SQL})`);
  }
  const params = [];

  if (chain) {
    conditions.push("network = ?");
    params.push(normalizeNetwork(chain));
  }
  // The inferred domain/protocol_type used to go into the WHERE clause, so a
  // single bad substring collapsed the candidate pool instead of merely
  // mis-ordering it: "tokens" contains "ens" and cut 5,479 candidates to 78
  // with ENS on top, and chain:"arbitrum" returned total_matches 0 with no
  // error at all. Inference is a guess about intent; a guess belongs in the
  // ORDER BY, where being wrong costs a few positions, not every result.
  //
  // The text terms now ALWAYS constrain (they used to be skipped entirely
  // whenever anything was inferred), so the pool stays tied to what was
  // actually asked.
  const scoreParts = [];
  const scoreParams = [];
  let inferredChain = null;

  // A chain named in the goal is a chain, not part of a protocol's name.
  //
  // "lido staking on ethereum" scored Lido Ethereum (2,644 queries/30d) above
  // Lido (4,692,414) because "ethereum" matched Lido Ethereum's DISPLAY NAME
  // for +4, and the ordering is lexicographic — goal_score first, reliability
  // only as a tie-break — so a 0.88-vs-0.63 reliability gap and a 1,775x volume
  // gap never got a vote. The subgraph won for having the chain in its title.
  //
  // The chain already has its own column and its own normalizer. Pull chain
  // words out of the scoring terms and use them the way the `chain` parameter
  // is used, so "on ethereum" narrows the network instead of flattering any
  // subgraph that happens to be called something-Ethereum.
  // Scan EVERY term for chain words before truncating search terms to five:
  // "top Uniswap v3 tokens by volume on Base" has five terms before "base",
  // so the chain used to be cut off and the answer came from Ethereum.
  const allWords = queryTerms(goalLower, 50);
  // A scale question ("highest volume", "most TVL") is inherently a question
  // ABOUT a category on a chain, so any chain word in it is routing.
  const volumeIntent = VOLUME_INTENT_RE.test(goalLower);
  const isChainish = (w) => {
    const c = normalizeNetwork(w);
    return c !== w || KNOWN_NETWORKS.has(c);
  };
  const chainWords = [];
  const words = [];
  for (const w of allWords) {
    // Only treat it as a chain if it resolves to a network the corpus has —
    // otherwise a protocol genuinely called "Base" or "Mode" would vanish.
    if (isChainish(w)) {
      // ...and only if it is actually ROUTING. A chain name routes when the prose
      // marks it ("...on base") or when the goal names something else to search
      // for. "Safe / Gnosis Safe" has neither: consuming `gnosis` as a filter left
      // only the noise token "safe", and the answer was HOPR Nodes on the gnosis
      // chain rather than the Safe multisig.
      const idx = goalLower.indexOf(w);
      const prepositioned = idx > 0 && CHAIN_PREP_RE.test(goalLower.slice(0, idx));
      const otherSubjectRemains = allWords.some(
        (o) => o !== w && !NOISE_TOKENS.has(o) && !VERSION_TOKEN_RE.test(o) && !isChainish(o),
      );
      // "Base DEX with highest volume" names no protocol and has no preposition,
      // but it is unambiguously a question about the Base chain — without this
      // clause `base` stayed a search term and base-dexstarter (0 queries) beat
      // uniswap-v4-base-3 (347M) on the accidental phrase "base dex".
      if (prepositioned || otherSubjectRemains || volumeIntent) {
        chainWords.push(normalizeNetwork(w));
        continue;
      }
    }
    words.push(w);
  }
  words.splice(5);

  // Which tokens actually identify a protocol? Version tokens (v2/v3/v4) and
  // category nouns (pool, dex, marketplace…) MODIFY a request; on their own they
  // just select whichever popular subgraph happens to contain them.
  const strongWords = words.filter(
    (w) => !NOISE_TOKENS.has(w) && !VERSION_TOKEN_RE.test(w),
  );
  const weakWords = words.filter((w) => !strongWords.includes(w));

  // Adjacent word pairs, matched whole against the display name. "compound v3"
  // as a phrase beats Uniswap-V3 on the bare token "v3"; "rocket pool" as a
  // phrase beats Venus Core Pool on the bare token "pool".
  const meaningful = (parts) =>
    parts.some((w) => !NOISE_TOKENS.has(w) && !VERSION_TOKEN_RE.test(w));
  const phrases = [];
  for (let i = 0; i + 1 < words.length; i++) {
    const pair = [words[i], words[i + 1]];
    if (meaningful(pair)) phrases.push(pair.join(" "));
  }
  if (words.length > 2 && meaningful(words)) phrases.push(words.join(" "));
  // A chain word NEVER becomes a scoring term. The first version of this fell
  // back to `words.push(...chainWords)` whenever it could not use them as a
  // filter — and because chainWords hold the CANONICAL form, "on ethereum"
  // re-entered scoring as the token "mainnet" and scored +6 against any
  // display name containing it. Passing chain:"ethereum" with a goal ending
  // "on ethereum" therefore ranked Clearpool staking mainnet (vol 2) over Lido
  // (4,692,414), Mainnet Voting V2 over Snapshot, seer-outcome-tokens-mainnet
  // (vol 1) over ENS (34,835,842), and dropped EigenLayer out of the top 5
  // entirely. It made the explicit chain argument actively worse than omitting
  // it, which is the opposite of what an argument is for.
  //
  // Chain words are routing information. They filter, or they are discarded.
  const explicitChain = chain ? normalizeNetwork(chain) : null;
  if (!explicitChain && chainWords.length === 1) {
    conditions.push("network = ?");
    params.push(chainWords[0]);
  }
  // Report the chain actually in effect, whether it came from the argument or
  // the prose — a caller passing chain used to get inferred_chain: null, which
  // read as "your chain was ignored".
  inferredChain = explicitChain || (chainWords.length === 1 ? chainWords[0] : null);

  // Whole-phrase name matches, scored far above any single token. This is what
  // separates "compound v3" from Uniswap-V3 and "rocket pool" from Venus Core
  // Pool: both lost on a shared modifier token that the phrase disambiguates.
  const phrasePatterns = phrases.flatMap((ph) => [
    `%${ph}%`,
    `%${ph.replace(/ /g, "-")}%`,
    `%${ph.replace(/ /g, "")}%`,
  ]);
  if (phrasePatterns.length) {
    scoreParts.push(
      phrases
        .map(
          () =>
            "(CASE WHEN (display_name LIKE ? OR display_name LIKE ? OR display_name LIKE ?)" +
            " THEN 12 ELSE 0 END)",
        )
        .join(" + "),
    );
    phrasePatterns.forEach((pat) => scoreParams.push(pat));
  }

  // The candidate SET is constrained by strong tokens only. Weak tokens still
  // score — "pool" ought to help Rocket Pool rank — but a row whose ONLY match is
  // "pool" never enters the candidate set, so reliability can no longer promote
  // it. When the goal has no strong token at all ("DEX volume on Base") the text
  // constraint is dropped and the inferred domain/type plus volume do the work,
  // which is the paraphrase path.
  if (strongWords.length) {
    const textConds = strongWords.map(
      () => "(display_name LIKE ? OR description LIKE ? OR auto_description LIKE ?)",
    );
    strongWords.forEach((w) => params.push(`%${w}%`, `%${w}%`, `%${w}%`));
    conditions.push(`(${textConds.join(" OR ")})`);
  }
  if (strongWords.length && words.length) {
    scoreParts.push(
      words
        .map(
          (w) =>
            `((CASE WHEN display_name LIKE ? THEN ${strongWords.includes(w) ? 6 : 1} ELSE 0 END)` +
            ` + (CASE WHEN (description LIKE ? OR auto_description LIKE ?) THEN 1 ELSE 0 END))`,
        )
        .join(" + "),
    );
    words.forEach((w) => scoreParams.push(`%${w}%`, `%${w}%`, `%${w}%`));
  }
  if (domains.length) {
    scoreParts.push(`(CASE WHEN domain IN (${domains.map(() => "?").join(",")}) THEN 1 ELSE 0 END)`);
    scoreParams.push(...domains);
  }
  if (ptypes.length) {
    scoreParts.push(`(CASE WHEN protocol_type IN (${ptypes.map(() => "?").join(",")}) THEN 1 ELSE 0 END)`);
    scoreParams.push(...ptypes);
  }

  const goalScore = scoreParts.length ? scoreParts.join(" + ") : "0";
  const where = `WHERE ${conditions.join(" AND ")}`;
  const sql = `
    SELECT id, display_name, description, auto_description, domain, protocol_type, network,
           reliability_score, ipfs_hash, canonical_entities, active_allocation_count, example_query,
           query_volume_30d, updated_at,
           (${goalScore}) AS goal_score
    FROM subgraphs
    ${where}
    ORDER BY goal_score DESC, ${volumeIntent ? "query_volume_30d DESC, " : ""}reliability_score DESC
    LIMIT 60
  `;

  // SELECT-clause params bind before WHERE-clause params.
  let rows = getDb().prepare(sql).all(...scoreParams, ...params);

  rows = boundaryRerank(
    rows,
    // Re-rank on the tokens that identify the protocol. Including noise tokens
    // here would re-import the pollution the WHERE clause just removed.
    strongWords,
    volumeIntent
      ? (a, b) => (b.query_volume_30d || 0) - (a.query_volume_30d || 0)
      : null,
    phrases,
  );

  // De-dup first so we batch the stability lookup over the trimmed set.
  const seenIpfs = new Set();
  const keep = [];
  const skippedUnhealthy = [];
  for (const r of rows) {
    if (r.ipfs_hash && seenIpfs.has(r.ipfs_hash)) continue;
    if (r.ipfs_hash) seenIpfs.add(r.ipfs_hash);
    // A deployment this process recently saw fail to serve (or fall far
    // behind) yields its slot to the next healthy match, and is reported.
    const bad = knownBadHealth(r);
    if (bad) { skippedUnhealthy.push({ id: r.id, display_name: r.display_name, network: r.network, ...bad }); continue; }
    keep.push(r);
    if (keep.length >= 5) break;
  }
  // Batch the schema-stability lookup into ONE SELECT instead of N+1.
  // Falls back to {} if the schema_history table doesn't exist (pre-
  // feature DB snapshot).
  const stabMap = getSchemaStabilityBatch(keep.map((r) => r.id));
  const recommendations = keep.map((r) => {
    const stab = stabMap[r.id] || {
      schema_changed_at: null,
      schema_stable_days: null,
    };
    return {
      id: r.id,
      display_name: r.display_name,
      description: (r.description || r.auto_description || "").slice(0, 300),
      domain: r.domain,
      protocol_type: r.protocol_type,
      network: r.network,
      reliability_score: r.reliability_score,
    // The registry has this number and the official Graph MCP's
    // get_deployment_30day_query_counts was observed returning 0 for
    // deployments that plainly serve traffic, so it could not break ties
    // between a real protocol and its forks. Surfacing it here is what lets a
    // caller tell Lido (4.7M queries/30d) from lido-copy.
    query_volume_30d: r.query_volume_30d ?? null,
      ipfs_hash: r.ipfs_hash,
      canonical_entities: JSON.parse(r.canonical_entities),
      active_allocation_count: r.active_allocation_count || 0,
      example_query: r.example_query || null,
      schema_changed_at: stab.schema_changed_at,
      schema_stable_days: stab.schema_stable_days,
      freshness: freshnessFor(r),
      health: healthSummary(r),
      ...buildQueryEndpoints(r.id),
    };
  });

  return {
    goal,
    chain_filter: chain || null,
    inferred_domain: domains.length ? domains : null,
    // Surfaced so a caller can see that "on ethereum" in their goal became a
    // network filter, and correct it if that was not what they meant.
    inferred_chain: inferredChain,
    inferred_protocol_type: ptypes.length ? ptypes : null,
    total_matches: recommendations.length,
    next_action: executionNextAction(recommendations.length > 0),
    allocation_caveat: ALLOCATION_CAVEAT,
    ...(skippedUnhealthy.length ? { skipped_unhealthy: skippedUnhealthy, health_note: "Skipped deployments recently failed to serve or were far behind in this process (process-local, expires after 300 seconds). Indexing-reward or curation status is not used for this." } : {}),
    ...(!recommendations.length ? { discovery_hint: "No recommendation survived snapshot filters; use search_subgraphs with an explicit network and inspect diagnostics. Zero allocations or rewards is not proof of unavailable queries." } : {}),
    recommendations,
  };
}

function getSubgraphDetail({ subgraph_id }) {
  const row = getDb()
    .prepare("SELECT * FROM subgraphs WHERE id = ? OR ipfs_hash = ?")
    .get(subgraph_id, subgraph_id);

  if (!row) return { error: `Subgraph '${subgraph_id}' not found` };

  const result = { ...row };
  result.freshness = freshnessFor(row);
  result.canonical_entities = JSON.parse(result.canonical_entities);
  result.categories = JSON.parse(result.categories);
  if (result.all_entities) result.all_entities = JSON.parse(result.all_entities);
  // Contract addresses extracted from the manifest — list of
  // {kind, name, address, network, startBlock}. Null on subgraphs we
  // haven't crawled with manifest support yet, or substreams-powered ones.
  if (result.contract_addresses) {
    try { result.contract_addresses = JSON.parse(result.contract_addresses); }
    catch { /* leave as string if not valid JSON */ }
  }
  if (!result.description && result.auto_description) {
    result.description = result.auto_description;
  }
  const endpoints = buildQueryEndpoints(result.id);
  result.query_url = endpoints.query_url;
  result.query_url_x402 = endpoints.query_url_x402;
  result.pricing = endpoints.pricing;

  // Schema-evolution fields. Surfaces how long the schema has been
  // stable (schema_stable_days) and the unix timestamp of the last
  // detected fingerprint change. Helps agents prefer mature subgraphs.
  const stab = getSchemaStabilityFor(result.id);
  result.schema_changed_at = stab.schema_changed_at;
  result.schema_stable_days = stab.schema_stable_days;
  // Don't leak the embedding blob to MCP callers — it's 1.5 KB of
  // float32 bytes that's only useful for cosine math inside the server.
  delete result.embedding;

  // Per-subgraph starter query generated by the crawler from this subgraph's
  // parsed schema. Falls back to the legacy generic example when the column
  // is empty (pre-feature DBs).
  const FALLBACK_EXAMPLE =
    "{ pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) { id token0 { symbol } token1 { symbol } totalValueLockedUSD } }";
  const exampleQuery = result.example_query || FALLBACK_EXAMPLE;

  result.query_instructions = {
    // No single recommendation: see payment_options on each result. Callers
    // hold either a Studio key or a wallet, rarely both, and the registry has
    // no way to know which — so it states both and lets the caller choose.
    recommended: null,
    routes: ["api_key", "x402"],
    x402: {
      url: endpoints.query_url_x402,
      payment: endpoints.pricing,
      flow: "POST GraphQL to url. Gateway returns HTTP 402 with a base64 payment-required header containing the payment manifest. Sign $0.01 USDC on Base with an x402 client and retry. No API key, no signup.",
      client_libraries: ["@graphprotocol/client-x402", "x402-fetch"],
      example_query: exampleQuery,
    },
    // Not "legacy" — this is the route most callers should take, and the one
    // some MCP hosts allow exclusively. The old text also told you to replace
    // an `[api-key]` placeholder that no longer exists in the URL.
    api_key: {
      url: endpoints.query_url,
      flow: "Get a key at https://thegraph.com/studio/apikeys/ (100K free queries/month), then POST GraphQL to url with header `Authorization: Bearer <STUDIO_API_KEY>`. The key goes in the header, not the path. A missing header returns HTTP 200 with a GraphQL error body, so read the body rather than trusting the status.",
      example_query: exampleQuery,
    },
    schema_hint: result.example_query
      ? "example_query above was generated from this subgraph's actual schema. Adapt the entity name + field selection as needed."
      : "Use the all_entities field above to see what entities and fields are available to query.",
  };
  return result;
}


// ── JSON-LD per-subgraph well-known shape ─────────────────────────────────
// Stable, machine-readable manifest other crawlers and agents can index
// without going through MCP. Served at /.well-known/subgraph/{id}.jsonld and
// /subgraphs/{id}.jsonld (alias, same payload).
// Every JSON-LD document used to carry @context and @id under
// subgraph-registry.paulieb14.dev, a hostname that has never resolved
// (NXDOMAIN). A JSON-LD processor that dereferences the context gets nothing,
// and the @id identified each subgraph by a URL that 404s — so the documents
// the README calls "auto-discoverable" were undiscoverable by construction.
//
// Two changes. The context is inlined, because a context that must be fetched
// is a dependency on a host we do not run. And @id now defaults to The Graph's
// explorer, which is the canonical, resolving identifier for a subgraph and is
// where we want an agent following the link to end up anyway.
//
// Set SUBGRAPH_REGISTRY_BASE_URL to serve these under your own origin (the
// --http-only transport does exactly that).
const PUBLIC_BASE_URL = (process.env.SUBGRAPH_REGISTRY_BASE_URL || "").replace(/\/+$/, "");
const EXPLORER_BASE = "https://thegraph.com/explorer/subgraphs";

function subgraphIri(id) {
  return PUBLIC_BASE_URL ? `${PUBLIC_BASE_URL}/subgraphs/${id}` : `${EXPLORER_BASE}/${id}`;
}

const JSONLD_CONTEXT = {
  "@vocab": "https://schema.org/",
  id: "@id",
  name: "https://schema.org/name",
  description: "https://schema.org/description",
  network: "https://schema.org/provider",
  SubgraphDeployment: "https://schema.org/Dataset",
};

function buildJsonLdManifest(row) {
  if (!row) return null;
  const detail = getSubgraphDetail({ subgraph_id: row.id });
  if (detail?.error) return null;
  return {
    "@context": JSONLD_CONTEXT,
    "@type": "SubgraphDeployment",
    "@id": subgraphIri(row.id),
    id: row.id,
    ipfsHash: row.ipfs_hash,
    name: row.display_name,
    description: row.description || row.auto_description,
    network: row.network,
    classification: {
      domain: row.domain,
      protocolType: row.protocol_type,
      confidence: row.classification_confidence,
    },
    entities: detail.all_entities || [],
    canonicalEntities: detail.canonical_entities || [],
    contracts: detail.contract_addresses || null,
    freshness: detail.freshness,
    reliabilityScore: row.reliability_score,
    activeIndexers: row.active_allocation_count,
    queryVolume30d: row.query_volume_30d,
    endpoints: {
      x402: detail.query_url_x402,
      apiKey: detail.query_url,
    },
    exampleQuery: detail.query_instructions?.x402?.example_query || null,
    poweredBySubstreams: !!row.powered_by_substreams,
    pricing: detail.pricing,
  };
}

function listRegistryStats() {
  const d = getDb();
  const domains = d
    .prepare("SELECT domain, COUNT(*) as count FROM subgraphs GROUP BY domain ORDER BY count DESC")
    .all();
  const networks = d
    .prepare("SELECT network, COUNT(*) as count FROM subgraphs WHERE network IS NOT NULL GROUP BY network ORDER BY count DESC")
    .all();
  const ptypes = d
    .prepare("SELECT protocol_type, COUNT(*) as count FROM subgraphs GROUP BY protocol_type ORDER BY count DESC")
    .all();
  const total = d.prepare("SELECT COUNT(*) as c FROM subgraphs").get().c;

  return {
    total_subgraphs: total,
    domains: Object.fromEntries(domains.map((r) => [r.domain, r.count])),
    networks: Object.fromEntries(networks.map((r) => [r.network, r.count])),
    protocol_types: Object.fromEntries(ptypes.map((r) => [r.protocol_type, r.count])),
  };
}

// ── Semantic search (vector embeddings) ───────────────────
// At crawl time the Python pipeline computes a 384-dim
// sentence-transformers/all-MiniLM-L6-v2 embedding per subgraph and
// stores it as a little-endian float32 BLOB in the `embedding` column.
// At query time the Node MCP server loads the SAME model architecture
// via @xenova/transformers (quantized INT8 ONNX bundled under
// data/models/) and embeds the query string once, then ranks rows by
// cosine similarity. No PyTorch, no Python sidecar — runtime is pure
// JS + sqlite.
//
// IMPORTANT: vectors are NOT bitwise-identical across runtimes. The JS
// side is INT8-quantized; the Python side is float32. Top-K rankings
// are stable but absolute scores can drift by ~0.01-0.03. The default
// `min_score: 0.3` is calibrated for the quantized JS side. If you
// run cross-runtime cosine comparisons, expect approximate not exact
// agreement.

let _embedderPromise = null;

export const BUNDLED_MODEL_FILES = ["config.json", "tokenizer.json", "tokenizer_config.json", "onnx/model_quantized.onnx"];

export function missingBundledModelFiles(dir = EMBEDDING_MODEL_DIR) {
  return BUNDLED_MODEL_FILES.filter((f) => !existsSync(join(dir, f)));
}

async function getEmbedder() {
  // Lazy single-load; ~23 MB ONNX. First call latency ~1-2s on cold
  // start, subsequent calls are ~5-20ms per query embed.
  if (!_embedderPromise) {
    _embedderPromise = (async () => {
      // Dynamic import keeps the cold-start cost off the critical
      // path of tools that don't need embeddings (search_subgraphs,
      // get_subgraph_detail, list_registry_stats).
      // Bundled model only (0.13.2+). Remote model downloads are disabled
      // unconditionally; if the bundled files are missing we fail closed and
      // semantic_search_subgraphs falls back to keyword search.
      const missing = missingBundledModelFiles();
      if (missing.length) {
        const err = new Error(`Bundled embedding model missing (${missing.join(", ")}); remote model downloads are disabled.`);
        err.code = "BUNDLED_MODEL_MISSING";
        throw err;
      }
      const { pipeline, env } = await import("@xenova/transformers");
      env.localModelPath = EMBEDDING_MODEL_ROOT;
      env.allowLocalModels = true;
      env.allowRemoteModels = false;
      env.useBrowserCache = false;
      const extractor = await pipeline(
        "feature-extraction",
        "Xenova/all-MiniLM-L6-v2",
        { quantized: true },
      );
      return extractor;
    })();
  }
  return _embedderPromise;
}

async function embedQuery(text) {
  const extractor = await getEmbedder();
  // pooling: "mean" + normalize: true matches sentence-transformers
  // default — identical to what fastembed produces server-side.
  const output = await extractor(text, { pooling: "mean", normalize: true });
  // output.data is a Float32Array of length 384
  return output.data;
}

function blobToFloat32(buf) {
  // SQLite returns the BLOB as a Node Buffer. better-sqlite3's Buffers
  // are views into a pooled slab with NO byteOffset alignment guarantee
  // — and Float32Array requires byteOffset to be a multiple of 4. Wrap-
  // without-copy used to throw `RangeError: start offset of Float32Array
  // should be a multiple of 4` on any row whose blob landed at an odd
  // offset (~7/8 of the time in production). Copy the bytes into a
  // fresh aligned ArrayBuffer instead — the 1.5 KB/row alloc dwarfs the
  // cosine compute that follows anyway.
  const ab = buf.buffer.slice(
    buf.byteOffset,
    buf.byteOffset + buf.byteLength,
  );
  return new Float32Array(ab);
}

function cosineSim(a, b) {
  // Assumes vectors are already L2-normalized (they are: the embedder
  // is called with normalize:true and fastembed normalizes by default).
  // For normalized vectors, cosine sim == dot product.
  let dot = 0;
  const n = Math.min(a.length, b.length);
  for (let i = 0; i < n; i++) dot += a[i] * b[i];
  return dot;
}

async function semanticSearchSubgraphs(args = {}) {
  const invalid = validateDiscoveryInput(args, "semantic");
  if (invalid) return { error: invalid };
  const {
    query, limit = 10, min_score = 0.3, include_unserved = false,
    include_denied = false, include_testnets = false, domain = "", network = "",
    protocol_type = "", min_reliability = 0,
  } = args;

  let qvec;
  try {
    qvec = await embedQuery(query);
  } catch (err) {
    _embedderPromise = null;
    if (err?.code !== "BUNDLED_MODEL_MISSING") throw err;
    // Fail closed: never download a model. Answer with keyword search and say so.
    const kw = searchSubgraphs({
      query, limit, include_unserved, include_denied, include_testnets, domain, network,
      protocol_type, min_reliability,
    });
    return {
      ...kw,
      search_mode: "keyword_fallback",
      semantic_unavailable: {
        reason: "bundled_model_missing",
        detail: err.message,
        fix: "Reinstall the exact published package (npx -y " + PINNED_NPX_PACKAGE + "), which bundles the model. No download is attempted.",
      },
    };
  }

  // SQL pre-filter shaves ~14k → <1k rows for narrow queries (e.g.
  // "lending positions on Arbitrum"). Cosine math runs only on the
  // post-filter set.
  // Exclude the handful of null-ipfs "shell" rows — they carry embeddings but
  // are unqueryable (no deployment) so they must not surface as recommendations.
  const conditions = ["embedding IS NOT NULL", "ipfs_hash != ''", "ipfs_hash IS NOT NULL"];
  const params = [];
  if (!include_unserved) {
    conditions.push("active_allocation_count > 0");
  }
  if (!include_denied) {
    conditions.push("denied_at = 0");
  }
  if (shouldExcludeTestnets({ include_testnets, network })) {
    conditions.push(`(${NOT_TESTNET_SQL})`);
  }
  if (domain) {
    conditions.push("domain = ?");
    params.push(domain);
  }
  if (network) {
    conditions.push("network = ?");
    params.push(normalizeNetwork(network));
  }
  if (protocol_type) {
    conditions.push("protocol_type = ?");
    params.push(protocol_type);
  }
  if (typeof min_reliability === "number" && min_reliability > 0) {
    conditions.push("reliability_score >= ?");
    params.push(min_reliability);
  }
  const where = `WHERE ${conditions.join(" AND ")}`;
  const rows = getDb()
    .prepare(
      `SELECT id, display_name, description, auto_description, domain,
              protocol_type, network, reliability_score, ipfs_hash,
              entity_count, canonical_entities, powered_by_substreams,
              active_allocation_count, example_query, denied_at, created_at,
              query_volume_30d, updated_at, embedding
       FROM subgraphs
       ${where}`,
    )
    .all(...params);

  // Score every row. With ~14k subgraphs × 384 floats this is ~5ms on
  // a modern x64 box — cheap enough to do linearly per request.
  const scored = [];
  const seenIpfs = new Set();
  for (const r of rows) {
    const vec = blobToFloat32(r.embedding);
    const score = cosineSim(qvec, vec);
    if (score < min_score) continue;
    scored.push({ row: r, score });
  }
  // Rank on similarity WEIGHTED by reliability, not similarity alone.
  //
  // Pure cosine made this the only tool in the package that ignored the
  // registry's own quality signal, and testnets win on pure cosine because
  // their text is near-identical to mainnet's. Observed: "ENS domain name
  // registrations" put ENS Sepolia (58 queries/30d, reliability 0.2463) above
  // ENS mainnet (34.8M queries/30d, reliability 0.9775) on a cosine margin of
  // 0.0105 — a rounding error deciding between a toy and the real thing.
  //
  // The 0.5 floor is deliberate: reliability is itself age-biased (see the
  // maturity block above), so a multiplier that ran to 0 would re-bury every
  // new subgraph and undo the emerging work. At 0.5 + 0.5*r a brand-new
  // subgraph keeps half its similarity and can still outrank an established
  // one it genuinely beats on meaning, while a 0.01 cosine tie resolves
  // toward the subgraph that is actually serving traffic.
  const effective = (s) => s.score * (0.5 + 0.5 * (s.row.reliability_score || 0));
  scored.sort((a, b) => effective(b) - effective(a));

  const results = [];
  for (const { row: r, score } of scored) {
    if (r.ipfs_hash && seenIpfs.has(r.ipfs_hash)) continue;
    if (r.ipfs_hash) seenIpfs.add(r.ipfs_hash);
    results.push({
      id: r.id,
      display_name: r.display_name,
      description: (r.description || r.auto_description || "").slice(0, 300),
      domain: r.domain,
      protocol_type: r.protocol_type,
      network: r.network,
      reliability_score: r.reliability_score,
    // The registry has this number and the official Graph MCP's
    // get_deployment_30day_query_counts was observed returning 0 for
    // deployments that plainly serve traffic, so it could not break ties
    // between a real protocol and its forks. Surfacing it here is what lets a
    // caller tell Lido (4.7M queries/30d) from lido-copy.
    query_volume_30d: r.query_volume_30d ?? null,
      ipfs_hash: r.ipfs_hash,
      entity_count: r.entity_count,
      canonical_entities: JSON.parse(r.canonical_entities),
      powered_by_substreams: Boolean(r.powered_by_substreams),
      active_allocation_count: r.active_allocation_count || 0,
      denied: Boolean(r.denied_at),
      testnet: isTestnetNetwork(r.network),
      example_query: r.example_query || null,
      // No `emerging` companion list here: this tool ranks by cosine score,
      // not reliability_score, so a three-week-old subgraph can and does take
      // the top slot on merit. The cold-start bias is a property of the ranked
      // search, not of semantic search — what this tool needs is the label, so
      // a caller knows a strong match is also unproven.
      age_days: ageDays(r.created_at),
      maturity: maturityOf(r.created_at),
      semantic_score: Number(score.toFixed(4)),
      freshness: freshnessFor(r),
      ...buildQueryEndpoints(r.id),
    });
    if (results.length >= limit) break;
  }

  return {
    allocation_caveat: ALLOCATION_CAVEAT,
    next_action: executionNextAction(results.length > 0),
    query,
    total: results.length,
    model: "sentence-transformers/all-MiniLM-L6-v2",
    subgraphs: results,
    query_instructions:
      "Discovery only — this tool does not execute GraphQL and never introspects a schema. To run a query, call execute_query (opt-in). To inspect a schema, call get_schema (opt-in). Optional next step: `execute_query` (opt-in) or `get_schema`. Each result includes both query routes in `payment_options` — a keyed gateway URL (Authorization: Bearer <STUDIO_API_KEY>) and an x402 URL ($0.01 USDC on Base, no key). Use whichever your client already has. semantic_score is cosine similarity in [0,1]; values >0.5 are typically strong matches.",
  };
}

// ── Schema evolution ──────────────────────────────────────
// schema_history is append-only: one row per fingerprint change for a
// given subgraph_id. Read at query time to surface "how long has this
// schema been stable?" so agents can prefer subgraphs whose contract
// of data is mature.

function getSchemaChanges({ subgraph_id, since_timestamp = 0 }) {
  if (!subgraph_id || typeof subgraph_id !== "string") {
    return { error: "subgraph_id is required and must be a string" };
  }
  // Coerce since_timestamp to a non-negative integer. SQLite has loose
  // typing so passing a string like "2024-01-01" used to silently match
  // nothing; passing NaN matched everything. Validate at the boundary.
  let since = Number(since_timestamp);
  if (!Number.isFinite(since) || since < 0) since = 0;
  since = Math.floor(since);

  // Always return the same key set so agents can pattern-match against
  // a stable shape even when the schema_history table is missing.
  const now = Math.floor(Date.now() / 1000);
  const baseShape = {
    subgraph_id,
    total_changes: 0,
    last_changed_at: null,
    stable_days: null,
    changed_within_24h: false,
    changed_within_7d: false,
    changes: [],
  };

  let rows;
  try {
    rows = getDb()
      .prepare(
        `SELECT fingerprint, prev_fingerprint, detected_at, ipfs_hash
         FROM schema_history
         WHERE subgraph_id = ? AND detected_at >= ?
           AND prev_fingerprint IS NOT NULL
         ORDER BY detected_at DESC`,
      )
      .all(subgraph_id, since);
  } catch (err) {
    // schema_history table doesn't exist yet (pre-feature DB snapshot).
    return {
      ...baseShape,
      note: "schema_history table not present in this registry.db — feature ships in v0.7+.",
    };
  }

  // Baselines are excluded from `rows`, so "no rows" now means "never changed
  // since we first saw it" rather than "no history". Those are very different
  // claims to an agent deciding whether a schema is safe to depend on, and
  // collapsing them to stable_days: null loses the distinction. Report the
  // first sighting separately and measure stability from it, so a subgraph
  // that has genuinely never changed reads as stable — which is the honest
  // answer, and the one the old code accidentally gave everybody.
  let first_seen_at = null;
  try {
    const fs = getDb()
      .prepare(
        "SELECT MIN(detected_at) AS t FROM schema_history WHERE subgraph_id = ?",
      )
      .get(subgraph_id);
    first_seen_at = fs && fs.t != null ? fs.t : null;
  } catch {
    first_seen_at = null;
  }

  const never_changed = rows.length === 0;
  const last_changed_at = rows.length > 0 ? rows[0].detected_at : null;
  const stable_since = last_changed_at !== null ? last_changed_at : first_seen_at;
  const stable_days =
    stable_since !== null
      ? Math.round(((now - stable_since) / 86400) * 10) / 10
      : null;

  return {
    subgraph_id,
    total_changes: rows.length,
    never_changed,
    first_seen_at,
    last_changed_at,
    stable_days,
    stable_days_basis: never_changed ? "first_seen" : "last_change",
    changed_within_24h:
      last_changed_at !== null && now - last_changed_at < 86400,
    changed_within_7d:
      last_changed_at !== null && now - last_changed_at < 86400 * 7,
    changes: rows.map((r) => ({
      fingerprint: r.fingerprint,
      prev_fingerprint: r.prev_fingerprint,
      detected_at: r.detected_at,
      ipfs_hash: r.ipfs_hash,
    })),
  };
}

function getSchemaStabilityFor(id) {
  // Light-weight helper used by get_subgraph_detail to enrich a single
  // row with schema-stability fields. Falls back to nulls if the
  // schema_history table doesn't exist (older DB snapshots). For
  // recommend_subgraph, use getSchemaStabilityBatch instead — it
  // collapses N queries into one.
  try {
    const r = getDb()
      .prepare(
        "SELECT MAX(detected_at) AS schema_changed_at " +
          "FROM schema_history WHERE subgraph_id = ? " +
          "AND prev_fingerprint IS NOT NULL",
      )
      .get(id);
    if (!r || r.schema_changed_at == null) {
      return { schema_changed_at: null, schema_stable_days: null };
    }
    const now = Math.floor(Date.now() / 1000);
    const days = Math.round(((now - r.schema_changed_at) / 86400) * 10) / 10;
    return { schema_changed_at: r.schema_changed_at, schema_stable_days: days };
  } catch (_) {
    return { schema_changed_at: null, schema_stable_days: null };
  }
}

function getSchemaStabilityBatch(ids) {
  // Single GROUP BY query for up to ~5-50 subgraph IDs. Returns a map
  // { [id]: { schema_changed_at, schema_stable_days } }. Empty map on
  // missing table or empty input.
  if (!Array.isArray(ids) || ids.length === 0) return {};
  try {
    const placeholders = ids.map(() => "?").join(",");
    const rows = getDb()
      .prepare(
        `SELECT subgraph_id, MAX(detected_at) AS schema_changed_at
         FROM schema_history
         WHERE subgraph_id IN (${placeholders})
           AND prev_fingerprint IS NOT NULL
         GROUP BY subgraph_id`,
      )
      .all(...ids);
    const now = Math.floor(Date.now() / 1000);
    const out = {};
    for (const r of rows) {
      if (r.schema_changed_at == null) {
        out[r.subgraph_id] = {
          schema_changed_at: null,
          schema_stable_days: null,
        };
        continue;
      }
      out[r.subgraph_id] = {
        schema_changed_at: r.schema_changed_at,
        schema_stable_days:
          Math.round(((now - r.schema_changed_at) / 86400) * 10) / 10,
      };
    }
    return out;
  } catch (_) {
    return {};
  }
}

// ── Opt-in gateway (schema + execute) ──────────────────────
// Discovery tools never call these. Explicit execution/schema/health tools are the
// only paths that POST GraphQL at The Graph gateway, and only when the
// caller invokes them. No private key is bundled; a Studio key is read
// from the environment if the host set one.

const KEYED_GATEWAY_BASE = "https://gateway.thegraph.com/api";
const GATEWAY_TIMEOUT_MS = 20_000;
// Ceiling on a single gateway response handed back through a tool result.
// Override with GATEWAY_MAX_BODY_BYTES if you genuinely want more.
const MAX_GATEWAY_BODY = Number(process.env.GATEWAY_MAX_BODY_BYTES ?? 1_000_000);
const DEPLOYMENT_ID_RE = /^0x[0-9a-fA-F]{64}$/;
const IPFS_HASH_RE = /^(Qm[1-9A-HJ-NP-Za-km-z]{44,}|bafy[a-z0-9]{20,})$/i;
// Subgraph ids are base58 (no 0, O, I or l). Without this the classifier
// treated ANY leftover string as a subgraph id and interpolated it straight
// into the gateway URL, so an id could walk the path while carrying the
// caller's Studio key:
//   "../../evil"       -> https://gateway.thegraph.com/api/evil
//   "x/../../../admin" -> https://gateway.thegraph.com/api/admin
//   "a?b=c#d"          -> query string injected into the path
// The host could never be changed — the base is a literal — so this was never
// arbitrary-host SSRF. But sending a user's bearer token to a path they chose
// is a degree of freedom with no upside, and it costs one regex to remove.
const SUBGRAPH_ID_RE = /^[1-9A-HJ-NP-Za-km-z]{20,60}$/;
const CONTRACT_ADDR_RE = /^0x[0-9a-fA-F]{40}$/;

function studioApiKey() {
  const raw =
    process.env.THE_GRAPH_STUDIO_API_KEY ||
    process.env.GRAPH_STUDIO_API_KEY ||
    process.env.GATEWAY_API_KEY ||
    "";
  const key = String(raw).trim();
  return key || null;
}

function classifyIdentifier(value) {
  const v = String(value || "").trim();
  if (!v) return null;
  if (DEPLOYMENT_ID_RE.test(v)) return { kind: "deployment_id", id: v };
  if (IPFS_HASH_RE.test(v)) return { kind: "ipfs_hash", id: v };
  if (SUBGRAPH_ID_RE.test(v)) return { kind: "subgraph_id", id: v };
  return null;   // not an identifier we know how to address
}

// Official subgraph-MCP uses subgraphs/id for a subgraph id and
// deployments/id for both a 0x deployment id and an IPFS hash.
function endpointTypeFor(kind) {
  return kind === "subgraph_id" ? "subgraphs/id" : "deployments/id";
}

function resolveQueryTarget(args = {}) {
  const deployment_id = args.deployment_id ? String(args.deployment_id).trim() : "";
  const ipfs_hash = args.ipfs_hash ? String(args.ipfs_hash).trim() : "";
  const subgraph_id = args.subgraph_id
    ? String(args.subgraph_id).trim()
    : args.id
      ? String(args.id).trim()
      : "";

  // Every branch validates. The explicit deployment_id / ipfs_hash arguments
  // used to be trusted as given and skipped classifyIdentifier altogether, so
  // the format check that existed for `id` could be sidestepped by naming a
  // different parameter.
  let kind;
  let id;
  if (deployment_id) {
    if (!DEPLOYMENT_ID_RE.test(deployment_id)) {
      return { error: "deployment_id must be 0x followed by 64 hex characters", got: deployment_id.slice(0, 80) };
    }
    kind = "deployment_id";
    id = deployment_id;
  } else if (ipfs_hash) {
    if (!IPFS_HASH_RE.test(ipfs_hash)) {
      return { error: "ipfs_hash must be a Qm… or bafy… CID", got: ipfs_hash.slice(0, 80) };
    }
    kind = "ipfs_hash";
    id = ipfs_hash;
  } else if (subgraph_id) {
    const classified = classifyIdentifier(subgraph_id);
    if (!classified) {
      return {
        error: "not a valid identifier: expected a base58 subgraph id, a 0x… deployment id, or a Qm…/bafy… IPFS hash",
        got: subgraph_id.slice(0, 80),
      };
    }
    kind = classified.kind;
    id = classified.id;
  } else {
    return { error: "id, subgraph_id, deployment_id or ipfs_hash is required" };
  }
  if (!id) return { error: "identifier is empty" };

  const endpointType = endpointTypeFor(kind);
  const query_url = `${KEYED_GATEWAY_BASE}/${endpointType}/${id}`;
  const query_url_x402 = `${X402_GATEWAY_BASE}/${endpointType}/${id}`;

  let row = null;
  if (kind !== "deployment_id") {
    try {
      row = getDb()
        .prepare("SELECT * FROM subgraphs WHERE id = ? OR ipfs_hash = ?")
        .get(id, id);
    } catch {
      row = null;
    }
  }

  return { kind, id, endpointType, query_url, query_url_x402, row };
}

function credentialsRequired(target, extra = {}) {
  return {
    error: "credentials_required",
    query_url: target.query_url,
    query_url_x402: target.query_url_x402,
    hint:
      "Set THE_GRAPH_STUDIO_API_KEY (a Graph Studio API key) to run this through the registry. " +
      "This tool does not sign x402 payments and does not bundle a private key. POST the GraphQL " +
      "yourself to query_url with header `Authorization: Bearer <key>`, or to query_url_x402 with " +
      "an x402 client. The keyed gateway often returns HTTP 200 with a GraphQL error body when the " +
      "header is missing — read the body rather than trusting the status.",
    get_a_key: "https://thegraph.com/studio/apikeys/",
    next_action: executionNextAction(),
    ...extra,
  };
}

const INTROSPECTION_QUERY = `{
  __schema {
    queryType { name }
    types {
      name
      kind
      fields {
        name
        type { name kind ofType { name kind ofType { name kind } } }
      }
    }
  }
}`;

async function postGateway({ url, key, query, variables, timeoutMs = GATEWAY_TIMEOUT_MS }) {
  if (process.env.SUBGRAPH_REGISTRY_MOCK_GATEWAY === "1") {
    return {
      http_status: 200,
      body: {
        data: {
          _mock: true,
          url,
          query,
          variables: variables && typeof variables === "object" ? variables : null,
        },
      },
      network_error: null,
    };
  }
  const headers = { "content-type": "application/json" };
  if (key) headers.Authorization = `Bearer ${key}`;
  const payload = { query };
  if (variables && typeof variables === "object" && !Array.isArray(variables)) {
    payload.variables = variables;
  }
  try {
    const res = await fetch(url, {
      method: "POST",
      redirect: "error",
      headers,
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(timeoutMs),
    });
    const text = await res.text();
    // Cap what a single tool call can return. The body was read and spread
    // into the result unbounded, so one broad query ("give me every entity")
    // could bury the caller's whole context window in one response — the
    // caller pays for that in tokens and cannot undo it.
    if (text.length > MAX_GATEWAY_BODY) {
      return {
        http_status: res.status,
        body: {
          error: "response_too_large",
          bytes: text.length,
          limit: MAX_GATEWAY_BODY,
          hint: "Narrow the query — add `first:`, select fewer fields, or paginate. The gateway returned more than this tool will hand back in one piece.",
          preview: text.slice(0, 1000),
        },
        network_error: null,
      };
    }
    let body;
    try {
      body = JSON.parse(text);
    } catch {
      body = { parse_error: true, raw: text.slice(0, 2000) };
    }
    return { http_status: res.status, body, network_error: null };
  } catch (err) {
    const timedOut = err && (err.name === "TimeoutError" || err.name === "AbortError");
    return {
      http_status: null,
      body: null,
      network_error: timedOut
        ? `gateway timed out after ${timeoutMs}ms`
        : String(err?.message || err),
    };
  }
}

function gatewayResultShape(posted, target) {
  const body = posted.body;
  const errors = body && Array.isArray(body.errors) ? body.errors : null;
  const authError = Boolean(
    errors &&
      errors.some((e) =>
        // Anchored on whole words. The first alternative used to be a bare
        // `auth`, which matches "author", "authority" and "authored" — so a
        // subgraph with an `author` field returning a normal field error was
        // reported to the caller as an authentication failure, sending them
        // to go fix a key that was never the problem.
        /\b(unauthorized|unauthenticated|authorization|authentication|api[- ]?key|missing authorization)\b/i
          .test(String(e?.message || e)),
      ),
  );
  const out = {
    http_status: posted.http_status,
    data: body && Object.prototype.hasOwnProperty.call(body, "data") ? body.data : null,
    errors,
    auth_error: authError,
    query_url: target.query_url,
    query_url_x402: target.query_url_x402,
  };
  if (body?.error) out.error = body.error;
  else if (body?.parse_error) out.error = "invalid_gateway_response";
  else if (posted.http_status !== null && (posted.http_status < 200 || posted.http_status >= 300)) out.error = "gateway_http_error";
  else if (!errors?.length && out.data == null) out.error = "invalid_gateway_response";
  if (posted.network_error) {
    out.error = "gateway_error";
    out.message = posted.network_error;
  }
  return out;
}

async function executeQuery(args = {}) {
  const query = typeof args.query === "string" ? args.query.trim() : "";
  if (!query) {
    return { error: "query is required and must be a GraphQL string" };
  }
  const target = resolveQueryTarget(args);
  if (target.error) return target;
  const key = studioApiKey();
  if (!key) {
    return credentialsRequired(target, { id: target.id, kind: target.kind });
  }
  const posted = await postGateway({
    url: target.query_url,
    key,
    query,
    variables: args.variables,
  });
  return {
    id: target.id,
    kind: target.kind,
    ...gatewayResultShape(posted, target),
  };
}

function compactIntrospection(data) {
  const types = data?.__schema?.types;
  if (!Array.isArray(types)) return data;
  return {
    queryType: data.__schema.queryType || null,
    types: types
      .filter((t) => t && !String(t.name || "").startsWith("__"))
      .filter((t) => t.kind === "OBJECT" || t.kind === "INTERFACE" || t.kind === "UNION")
      .map((t) => ({
        name: t.name,
        kind: t.kind,
        fields: Array.isArray(t.fields) ? t.fields.map((f) => f.name) : [],
      })),
  };
}

function registrySchemaFields(row) {
  if (!row) return null;
  let all_entities = row.all_entities;
  if (typeof all_entities === "string") {
    try {
      all_entities = JSON.parse(all_entities);
    } catch {
      /* leave as string */
    }
  }
  const stab = getSchemaStabilityFor(row.id);
  return {
    id: row.id,
    ipfs_hash: row.ipfs_hash,
    display_name: row.display_name,
    network: row.network,
    entity_count: row.entity_count,
    all_entities,
    example_query: row.example_query || null,
    schema_fingerprint: row.schema_fingerprint || null,
    schema_changed_at: stab.schema_changed_at,
    schema_stable_days: stab.schema_stable_days,
    query_volume_30d: row.query_volume_30d ?? null,
  };
}

async function getSchema(args = {}) {
  const target = resolveQueryTarget(args);
  if (target.error) return target;
  const cached = registrySchemaFields(target.row);
  const key = studioApiKey();
  const base = {
    id: target.id,
    kind: target.kind,
    query_url: target.query_url,
    query_url_x402: target.query_url_x402,
    registry_schema: cached,
  };
  if (!key) {
    if (cached) {
      return {
        ...base,
        live_introspection: null,
        live_introspection_error: credentialsRequired(target),
        hint:
          "registry_schema is from the local index (entities, example_query, fingerprint) — no network call. " +
          "Live GraphQL introspection against the gateway needs THE_GRAPH_STUDIO_API_KEY.",
      };
    }
    return {
      ...base,
      live_introspection: null,
      ...credentialsRequired(target, {
        hint:
          "Not in the local registry and no Studio key is set. Set THE_GRAPH_STUDIO_API_KEY to introspect " +
          "via the gateway, or POST an introspection query to query_url / query_url_x402 yourself.",
      }),
    };
  }
  const posted = await postGateway({
    url: target.query_url,
    key,
    query: INTROSPECTION_QUERY,
  });
  const shape = gatewayResultShape(posted, target);
  const out = {
    ...base,
    live_introspection: shape.data ? compactIntrospection(shape.data) : null,
    http_status: shape.http_status,
    errors: shape.errors,
    auth_error: shape.auth_error,
  };
  if (shape.error) {
    out.live_introspection_error = { error: shape.error, message: shape.message };
  }
  return out;
}

// Read-only cached observations, keyed by immutable deployment where possible.
// Bounded memory; no database writes or background/billable health checks.
const healthObservations = new Map();
function healthKey(row) { return row?.ipfs_hash || row?.id; }
function freshnessFor(row) {
  return freshness(row, healthObservations.get(healthKey(row)));
}
function rememberHealth(row, result, extra = {}) {
  const key = healthKey(row);
  healthObservations.delete(key);
  healthObservations.set(key, { ...healthObservation(result), ...extra });
  if (healthObservations.size > 500) {
    healthObservations.delete(healthObservations.keys().next().value);
  }
}

// Classify a failed gateway response. Only "serving" failures justify moving to
// another deployment: auth/quota/payment problems would fail everywhere, and
// query errors are about the query, not the deployment.
function classifyGatewayFailure(shape) {
  const text = [shape?.error, shape?.message, ...(shape?.errors || []).map((e) => e?.message || e)].filter(Boolean).join(" | ");
  if (shape?.auth_error || [401, 402, 403, 429].includes(shape?.http_status) ||
      /\b(quota|billing|payment|insufficient funds|rate limit|too many requests|api key)\b/i.test(text)) return "auth_or_quota";
  if (shape?.error === "gateway_error" || shape?.error === "invalid_gateway_response" ||
      (shape?.error === "gateway_http_error" && (shape?.http_status ?? 500) >= 500) ||
      /bad indexers|indexing_error|no indexers|not (yet )?available|unavailable|no allocations?|subgraph not found|deployment not found|not synced|timed out|timeout|store error|indexer.*error/i.test(text)) return "serving";
  return "query_error";
}

function failureEvidence(shape) {
  const msg = shape?.message || shape?.errors?.[0]?.message || shape?.error || "unknown";
  return String(msg).slice(0, 240);
}

// Process-local health memory: skip a deployment that recently failed to serve
// or was far behind. Never derived from rewards/curation (denied_at) or from a
// chain lacking indexing rewards; those say nothing about query availability.
function knownBadHealth(row, now = Math.floor(Date.now() / 1000)) {
  const obs = healthObservations.get(healthKey(row));
  if (!obs || now - obs.observed_at > HEALTH_STALE_SECONDS) return null;
  if (obs.status === "query_failed" && obs.failure_class === "serving") return { reason: "not_serving", evidence: obs.evidence || "recent gateway failure", observed_at: obs.observed_at };
  if (obs.status === "query_failed" && obs.failure_class === "stale") return { reason: "stale_indexing", evidence: obs.evidence, observed_at: obs.observed_at };
  if (obs.indexed_block_timestamp && obs.observed_at - obs.indexed_block_timestamp > STALE_INDEXING_SECONDS) {
    return { reason: "stale_indexing", evidence: `indexed block ${obs.observed_at - obs.indexed_block_timestamp}s behind observation`, observed_at: obs.observed_at };
  }
  return null;
}

function healthSummary(row) {
  const obs = healthObservations.get(healthKey(row));
  if (!obs) return { status: "not_observed" };
  const age = Math.max(0, Math.floor(Date.now() / 1000) - obs.observed_at);
  return { status: obs.failure_class && obs.status === "query_failed" ? `query_failed_${obs.failure_class}` : obs.status, observed_seconds_ago: age, stale_observation: age > HEALTH_STALE_SECONDS,
    ...(obs.indexed_block_timestamp ? { indexed_block_timestamp: obs.indexed_block_timestamp } : {}) };
}

function findByContract({ address, chain, limit = 3 } = {}) {
  const found = findContractDeployments(getDb(), { address, chain, limit }, normalizeNetwork);
  if (found.error) return found;
  return {
    contract_address: found.address,
    chain: found.chain,
    source: "registry",
    ranking: "reliability_score DESC, query_volume_30d DESC, id ASC; only allocated, non-denied deployments in the snapshot",
    allocation_caveat: ALLOCATION_CAVEAT,
    total: found.deployments.length,
    deployments: found.deployments.map(({ row: r, matched }) => ({
      id: r.id, display_name: r.display_name, domain: r.domain,
      protocol_type: r.protocol_type, network: r.network,
      reliability_score: r.reliability_score, query_volume_30d: r.query_volume_30d,
      ipfs_hash: r.ipfs_hash, matched_contracts: matched,
      schema_entities: registrySchemaFields(r)?.all_entities || [],
      coverage: {
        source: "crawled_manifest",
        contract_to_entity_mapping: null,
        caveat: "schema_entities describe the whole deployment, not verified entities/fields for this contract. Dynamic template instances and substreams may be absent; no match does not prove no coverage.",
      },
      example_query: r.example_query || null,
      freshness: freshnessFor(r),
      ...buildQueryEndpoints(r.id),
    })),
    caveat: "Exact case-insensitive EVM address matches from crawled manifests, not live chain discovery. Omit chain to search all networks; use matched_contracts.network for manifest-level chain evidence. Allocation and reliability are snapshot signals, not live health.",
  };
}

function getTopSubgraphDeployments({ contract_address, chain, limit = 3 } = {}) {
  if (!CONTRACT_ADDR_RE.test(String(contract_address || "").trim())) {
    return { error: "contract_address is required (0x-prefixed 40-hex EVM address)" };
  }
  if (typeof chain !== "string" || !chain.trim()) {
    return { error: "chain is required (e.g. mainnet, ethereum, base, arbitrum)" };
  }
  return findByContract({ address: contract_address, chain, limit });
}

async function checkSubgraphHealth(args = {}) {
  let target = resolveQueryTarget(args);
  if (target.error) return target;
  if (!studioApiKey()) return credentialsRequired(target);
  // Pin a discovered subgraph to the snapshot deployment: a mutable subgraph
  // id may have moved since the crawl and must not poison that snapshot's health.
  if (target.kind === "subgraph_id" && target.row?.ipfs_hash) {
    target = resolveQueryTarget({ ipfs_hash: target.row.ipfs_hash });
    if (target.error) return target;
  }
  // A fixed _meta query: caller cannot add fields, change host, or auto-pay.
  const identifier = target.kind === "subgraph_id" ? { subgraph_id: target.id }
    : target.kind === "ipfs_hash" ? { ipfs_hash: target.id } : { deployment_id: target.id };
  const result = await executeQuery({ ...identifier, query: HEALTH_QUERY });
  const row = target.row || { id: target.id, ipfs_hash: target.kind === "ipfs_hash" ? target.id : null };
  rememberHealth(row, result);
  return { id: target.id, kind: target.kind, ...result, freshness: freshnessFor(row) };
}

function isChainWord(w) {
  const c = normalizeNetwork(w);
  return c !== w || KNOWN_NETWORKS.has(c);
}

// Extra candidates for entity-specific goals: recommend_subgraph ranks by
// protocol text and traction, so a deployment that actually has the requested
// entity (e.g. an OHLCV subgraph) can be missing from its top five.
function goalCandidateRows(intent, network, { include_denied = false, include_unserved = false } = {}) {
  const terms = intent.protocol_terms.filter((w) => w.length > 1 && !/^v\d+$/.test(w));
  if (!terms.length && !network) return [];
  const conditions = [];
  if (!include_unserved) conditions.push("active_allocation_count > 0");
  if (!include_denied) conditions.push("denied_at = 0");
  const params = [];
  if (network) { conditions.push("network = ?"); params.push(network); }
  if (shouldExcludeTestnets({ include_testnets: false, network })) conditions.push(`(${NOT_TESTNET_SQL})`);
  if (terms.length) {
    conditions.push(`(${terms.map(() => "display_name LIKE ?").join(" OR ")})`);
    params.push(...terms.map((t) => `%${t}%`));
  }
  return getDb().prepare(`SELECT id, display_name, domain, protocol_type, network, reliability_score, query_volume_30d, ipfs_hash, example_query, all_entities, updated_at, active_allocation_count, denied_at
    FROM subgraphs WHERE ${conditions.join(" AND ")} ORDER BY reliability_score DESC LIMIT 40`).all(...params);
}

function parseEntities(raw) {
  try { const v = JSON.parse(raw || "[]"); return Array.isArray(v) ? v : []; } catch { return []; }
}

function chooseGoalTarget(intent, discovery, opts = {}) {
  const network = discovery.inferred_chain || null;
  const byId = new Map();
  if (!opts.only_extra) discovery.recommendations.forEach((r, idx) => byId.set(r.id, { rec: r, idx }));
  for (const row of goalCandidateRows(intent, network, opts)) if (!byId.has(row.id)) byId.set(row.id, { rec: row, idx: null });
  const terms = intent.protocol_terms;
  const scored = [];
  for (const { rec, idx } of byId.values()) {
    if (network && rec.network !== network) continue;
    const row = rec.all_entities !== undefined ? rec : getDb().prepare("SELECT all_entities, example_query FROM subgraphs WHERE id = ?").get(rec.id) || {};
    const entities = parseEntities(row.all_entities);
    const ranked = rankEntities(entities, intent);
    if (!ranked.length) continue;
    const name = String(rec.display_name || "").toLowerCase().replace(/[-_]/g, " ");
    const text = terms.length ? terms.filter((t) => name.includes(t)).length / terms.length : 0;
    const score = ranked[0].score + 0.3 * text + (idx === null ? 0 : 0.1 * (5 - idx) / 5) + 0.05 * (rec.reliability_score || 0);
    scored.push({ rec, entities, ranked, example_query: row.example_query ?? rec.example_query, score: Number(score.toFixed(4)), text_match: Number(text.toFixed(2)), from_recommendation: idx !== null });
  }
  return scored.sort((a, b) => b.score - a.score);
}

function selectedSummary(r) {
  return { id: r.id, display_name: r.display_name, network: r.network, ipfs_hash: r.ipfs_hash, domain: r.domain,
    protocol_type: r.protocol_type, reliability_score: r.reliability_score, query_volume_30d: r.query_volume_30d };
}

const MAX_GOAL_GATEWAY_REQUESTS = 6;
const MAX_GOAL_DEPLOYMENT_ATTEMPTS = 3;
const GOAL_PROBE_TIMEOUT_MS = 12_000;

async function queryForGoal({ goal, chain, first, execute = false, validate_schema = false, include_denied = false, include_unserved = false,
  spam_handling = "flag_and_push_down", trusted_tokens } = {}) {
  if (typeof goal !== "string" || !goal.trim() || goal.length > 1000) {
    return { error: "goal must be a non-empty string of at most 1000 characters" };
  }
  if (chain !== undefined && (typeof chain !== "string" || !chain.trim())) {
    return { error: "chain must be a non-empty network name" };
  }
  if (typeof execute !== "boolean" || typeof validate_schema !== "boolean" || typeof include_denied !== "boolean" || typeof include_unserved !== "boolean" ||
      (first !== undefined && (!Number.isInteger(first) || first < 1 || first > 10))) {
    return { error: "execute, validate_schema, include_denied and include_unserved must be boolean; first must be an integer from 1 to 10" };
  }
  if (!SPAM_HANDLING.includes(spam_handling)) return { error: `spam_handling must be one of ${SPAM_HANDLING.join(", ")}` };
  const trusted = normalizeTrusted(trusted_tokens);
  if (!trusted.ok) return { error: trusted.error };
  const discovery = recommendSubgraph({ goal: goal.trim(), chain: chain || "" });
  if (discovery.error) return { error: discovery.error, execution_attempted: false, executed: false };
  const intent = parseGoal(goal.trim(), { isChain: isChainWord });
  const rows = first ?? Math.min(intent.first_from_goal || 5, 10);
  const skipped = [];
  const key = studioApiKey();

  let selected, query = null, target, mapping, schemaValidation = "not_checked", liveErrors;
  let gatewayRequests = 0;
  let chosen = null; // { cand, plan, health, result? }
  const skippedDeployments = [];
  let stopReason = null;
  const tokenKind = intent.primary === "token" ? "token" : intent.primary === "pool" ? "pool" : null;
  // Rankings by TVL/volume are where spam/manipulated rows surface; fetch a
  // little more so pushing flagged rows down still leaves `first` usable rows.
  // Only when the caller did not set `first` explicitly.
  const overFetch = first === undefined && tokenKind && !intent.ids_only && spam_handling === "flag_and_push_down" && (intent.ordering === "top" || !intent.ordering) ? Math.min(10, rows * 2) : rows;

  if (!intent.primary) {
    // No entity intent recognised: keep the stored starter, labelled generic.
    for (const candidate of discovery.recommendations) {
      try { query = boundedStarter(candidate.example_query, rows); selected = candidate; break; }
      catch (err) { skipped.push({ id: candidate.id, reason: err.message }); }
    }
    if (!selected) return { error: "no_suitable_starter", goal, skipped, execution_attempted: false, executed: false, next_action: executionNextAction(false), discovery_hint: "Use search_subgraphs with an explicit network and inspect diagnostics; no suitable example is not proof that no queryable deployment exists." };
    mapping = { intent, confidence: "generic_starter", goal_specific: false,
      rationale: ["No entity intent (e.g. pools, swaps, candles, positions, liquidations) was recognised, so the deployment's stored starter is returned as a generic example."],
      unmet: [], alternatives: [], schema_source: "crawled_starter" };
  } else {
    const scored = chooseGoalTarget(intent, discovery, { include_denied, include_unserved });
    const best = scored[0];
    const alternatives = scored.slice(0, 5).flatMap((c, i) => c.ranked.slice(0, i === 0 ? 4 : 1).map((e) => ({
      id: c.rec.id, display_name: c.rec.display_name, network: c.rec.network, entity: e.name, entity_score: Number(e.score.toFixed(2)), reason: e.reason, deployment_score: c.score,
    }))).slice(0, 8);
    const minScore = validate_schema && key ? 0.6 : 0.75;
    const eligible = scored.filter((c) => c.ranked[0].score >= minScore);
    selected = best ? best.rec : discovery.recommendations[0];
    if (!eligible.length) {
      mapping = { intent, confidence: best ? "low" : "none", goal_specific: false,
        rationale: [best ? `Best entity ${best.ranked[0].name} only matched by ${best.ranked[0].reason}` : `No candidate deployment has an entity matching "${intent.primary}"`],
        unmet: ["No confident entity mapping; inspect alternatives or use get_subgraph_detail / get_schema before writing a query."],
        alternatives, schema_source: "registry_entity_names" };
      if (!include_denied || !include_unserved) {
        const hidden = chooseGoalTarget(intent, discovery, { include_denied: true, include_unserved: true, only_extra: true })
          .filter((c) => c.ranked[0].score >= 0.75 && (c.rec.denied_at || !c.rec.active_allocation_count)).slice(0, 3);
        if (hidden.length) {
          mapping.hidden_candidates = hidden.map((c) => ({ id: c.rec.id, display_name: c.rec.display_name, network: c.rec.network, entity: c.ranked[0].name,
            denied_indexing_rewards: Boolean(c.rec.denied_at), active_allocation_count: c.rec.active_allocation_count || 0 }));
          mapping.unmet.push("Deployments with a matching entity exist but are excluded by default snapshot filters (denied rewards or zero allocations are NOT proof they cannot be queried); retry with include_denied:true and/or include_unserved:true to consider them.");
        }
      }
    } else {
      const skip = (cand, reason, evidence, extra = {}) => {
        if (!skippedDeployments.some((d) => d.id === cand.rec.id)) skippedDeployments.push({ id: cand.rec.id, display_name: cand.rec.display_name, network: cand.rec.network, reason, evidence, ...extra });
      };
      // recommend_subgraph already dropped recently-unhealthy deployments; keep them visible.
      for (const u of discovery.skipped_unhealthy || []) skippedDeployments.push({ id: u.id, display_name: u.display_name, network: u.network, reason: u.reason, evidence: u.evidence, source: "process_local_observation", observed_at: u.observed_at });
      let attempts = 0, staleFallback = null, lastFailure = null;
      for (const cand of eligible) {
        if (attempts >= MAX_GOAL_DEPLOYMENT_ATTEMPTS) break;
        const bad = knownBadHealth(cand.rec);
        if (bad) { skip(cand, bad.reason, bad.evidence, { source: "process_local_observation", observed_at: bad.observed_at }); continue; }
        const entity = cand.ranked[0];
        const candTarget = resolveQueryTarget(cand.rec.ipfs_hash ? { ipfs_hash: cand.rec.ipfs_hash } : { subgraph_id: cand.rec.id });
        if (candTarget.error) { skip(cand, "no_query_target", candTarget.error); continue; }
        let plan = planKeyless({ intent, entity, starter: cand.example_query, first: overFetch, allEntityNames: cand.entities.map((e) => e.name) });
        let health = null, candValidation = validate_schema ? (key ? "not_checked" : "not_checked_no_key") : "not_checked";
        attempts++;
        if (validate_schema && key) {
          if (gatewayRequests >= MAX_GOAL_GATEWAY_REQUESTS) { stopReason = "request_budget_exhausted"; break; }
          gatewayRequests++;
          const posted = await postGateway({ url: candTarget.query_url, key, query: schemaProbeQuery(entity.name), timeoutMs: GOAL_PROBE_TIMEOUT_MS });
          const shape = gatewayResultShape(posted, candTarget);
          if (shape.error || shape.errors?.length || !shape.data) {
            const cls = classifyGatewayFailure(shape);
            const errs = [{ http_status: shape.http_status, error: shape.error ?? null, message: shape.message ?? null, errors: shape.errors, auth_error: shape.auth_error, failure_class: cls }];
            if (cls === "auth_or_quota") { lastFailure = { cand, target: candTarget, errs }; stopReason = "auth_or_quota"; break; }
            rememberHealth(cand.rec, { http_status: shape.http_status, error: shape.error || "query_failed", errors: shape.errors }, { failure_class: cls === "serving" ? "serving" : "query", evidence: failureEvidence(shape) });
            skip(cand, cls === "serving" ? "not_serving" : "schema_probe_failed", failureEvidence(shape), { source: "live_probe" });
            lastFailure = { cand, target: candTarget, errs };
            continue;
          }
          health = probeHealth(shape.data.m);
          if (shape.data.m) rememberHealth(cand.rec, { http_status: 200, data: { _meta: shape.data.m } });
          const live = planWithSchema({ intent, entity, probe: shape.data, first: overFetch });
          if (live.errors?.length) {
            skip(cand, "schema_does_not_fit_goal", live.errors.join("; ").slice(0, 240), { source: "live_probe" });
            lastFailure = { cand, target: candTarget, errs: live.errors };
            continue;
          }
          plan = live; candValidation = "validated_fields_and_arguments";
          if (health.status === "stale") {
            skip(cand, "stale_indexing", `indexed block is ${health.lag_seconds}s behind now`, { source: "live_probe", health });
            staleFallback ||= { cand, plan, health, target: candTarget, validation: candValidation };
            continue;
          }
        }
        const attempt = { cand, plan, health, target: candTarget, validation: candValidation };
        const willExecute = execute && key && plan?.query && !(plan.blocking_unmet?.length);
        if (!willExecute) { chosen = attempt; break; }
        if (gatewayRequests >= MAX_GOAL_GATEWAY_REQUESTS) { chosen = attempt; stopReason = "request_budget_exhausted"; break; }
        gatewayRequests++;
        const result = await executeQuery({ ipfs_hash: cand.rec.ipfs_hash, subgraph_id: cand.rec.id, query: plan.query });
        const ok = result.http_status >= 200 && result.http_status < 300 && !result.error && !result.errors?.length && result.data != null;
        if (!ok) {
          const cls = classifyGatewayFailure(result);
          rememberHealth(cand.rec, result, { failure_class: cls === "serving" ? "serving" : "query", evidence: failureEvidence(result) });
          if (cls === "serving" && eligible.indexOf(cand) < eligible.length - 1 && gatewayRequests < MAX_GOAL_GATEWAY_REQUESTS) {
            skip(cand, "not_serving", failureEvidence(result), { source: "execution" });
            continue;
          }
        } else if (result.data?._meta) {
          rememberHealth(cand.rec, result);
          const h = probeHealth(result.data._meta);
          attempt.health = attempt.health || h;
        }
        attempt.result = result;
        chosen = attempt;
        break;
      }
      if (!chosen && staleFallback && stopReason !== "auth_or_quota") {
        chosen = staleFallback;
        chosen.stale_fallback = true;
        // Execute the stale-but-serving deployment only if nothing healthier exists.
        if (execute && key && chosen.plan?.query && !chosen.plan.blocking_unmet?.length && gatewayRequests < MAX_GOAL_GATEWAY_REQUESTS) {
          gatewayRequests++;
          chosen.result = await executeQuery({ ipfs_hash: chosen.cand.rec.ipfs_hash, subgraph_id: chosen.cand.rec.id, query: chosen.plan.query });
        }
      }
      const pick = chosen || lastFailure || { cand: eligible[0] };
      const entity = pick.cand.ranked[0];
      selected = pick.cand.rec;
      target = pick.target || resolveQueryTarget(selected.ipfs_hash ? { ipfs_hash: selected.ipfs_hash } : { subgraph_id: selected.id });
      if (target.error) return { ...target, executed: false };
      const plan = chosen?.plan || null;
      if (chosen) schemaValidation = chosen.validation;
      else if (validate_schema && key) { schemaValidation = "failed"; liveErrors = lastFailure?.errs || [{ error: stopReason || "no_deployment_attempted" }]; }
      else if (validate_schema) schemaValidation = "not_checked_no_key";
      query = plan?.query ?? null;
      let confidence = "medium";
      if (chosen && schemaValidation === "validated_fields_and_arguments") confidence = entity.score >= 0.75 && !plan.blocking_unmet?.length ? "high" : "medium";
      if (chosen?.stale_fallback) confidence = "medium";
      const firstSkip = skippedDeployments[0];
      mapping = { intent, confidence: plan ? confidence : "low", goal_specific: Boolean(plan),
        entity: entity.name, entity_score: Number(entity.score.toFixed(2)), collection: plan?.collection ?? null,
        fields: plan?.fields ?? null, order: plan?.order ?? null, where: plan?.where ?? null, field_source: plan?.field_source ?? null,
        rationale: [`Selected ${selected.display_name} (${selected.network}) because entity ${entity.name}: ${entity.reason}; protocol text match ${pick.cand.text_match}${pick.cand.from_recommendation ? "" : "; found by entity-aware candidate search"}`,
          ...(chosen && firstSkip ? [`Fell back from ${firstSkip.display_name} (${firstSkip.id}): ${firstSkip.reason}`] : []),
          ...(plan?.rationale || [])],
        unmet: [...(plan?.unmet || []), ...(chosen?.stale_fallback ? ["All fitting deployments that answered were stale; returned the stale one with a warning"] : [])],
        filters_not_applied: plan?.blocking_unmet || [], alternatives, schema_source: plan?.field_source === "live_introspection" ? "live_introspection" : "registry_entity_names",
        skipped_deployments: skippedDeployments, fallback_used: Boolean(chosen && skippedDeployments.length),
        health_policy: "Fallback uses serving signals only (gateway failures, timeouts, indexer errors, stale _meta). Indexing-reward denial, curation and chains without rewards are not treated as unhealthy." };
      if (stopReason) mapping.stop_reason = stopReason;
      if (liveErrors) mapping.live_schema_errors = liveErrors;
      if (overFetch !== rows && plan) mapping.first_fetched = overFetch;
      if (chosen?.health) mapping.deployment_health = chosen.health;
    }
  }
  if (selected && !target) {
    target = resolveQueryTarget(selected.ipfs_hash ? { ipfs_hash: selected.ipfs_hash } : { subgraph_id: selected.id });
    if (target.error) return { ...target, executed: false };
  }
  const row = target?.row || (selected ? { id: selected.id, ipfs_hash: selected.ipfs_hash } : null);
  const request = query && target ? { method: "POST", query_url: target.query_url, query_url_x402: target.query_url_x402, body: { query, variables: {} } } : null;
  const out = {
    goal,
    next_action: executionNextAction(Boolean(query)),
    selected: selected ? { ...selectedSummary(selected), ...(selected.denied_at ? { denied_indexing_rewards: true } : {}), ...(selected.active_allocation_count === 0 ? { active_allocation_count: 0 } : {}) } : null,
    query, variables: {}, first: rows, skipped,
    goal_mapping: mapping,
    selection: mapping.goal_specific
      ? "Goal-specific query generated from the requested entity. Keyless plans are checked only against stored entity names and starter fields; validate_schema:true with your own Studio key checks fields and arguments live."
      : mapping.confidence === "generic_starter" ? "Stored starter returned as a generic example; it may not answer the goal."
        : "No query returned: the goal could not be mapped confidently. Use goal_mapping.alternatives to choose an entity.",
    validation: { syntax: query ? "passed" : "not_applicable", bounded_structure: query ? "passed" : "not_applicable", live_schema: schemaValidation, gateway_execution: "not_attempted" },
    execution_attempted: false, executed: false,
    gateway_requests: gatewayRequests,
    request,
    freshness: row ? freshnessFor(row) : null,
  };
  if (tokenKind && query) {
    out.token_quality_plan = { applies: true, handling: spam_handling, kind: tokenKind,
      note: spam_handling === "off" ? "Spam heuristics disabled by spam_handling:\"off\"." : "Returned rows are checked for likely spam/scam tokens and flagged in token_quality; with flag_and_push_down, flagged rows are moved after the others. Nothing is removed." };
  }
  if (!key) out.onboarding = keyOnboarding(request);
  else if (query && !execute && !(schemaValidation === "validated_fields_and_arguments" && mapping.filters_not_applied?.length)) {
    out.next_action.execute_call = { name: "query_for_goal", arguments: { goal, ...(chain ? { chain } : {}), first: rows, validate_schema: true, execute: true },
      cost: "Uses up to two gateway queries from your own Studio allowance (schema check + execution), more only if a deployment fails and a healthy alternative is tried (hard cap 6); never x402." };
  }
  if (!execute) return out;
  // Explicit execution opt-in is necessary even when the process has a key.
  if (!key) return { ...out, ...credentialsRequired(target || resolveQueryTarget({ subgraph_id: selected.id })), onboarding: keyOnboarding(request) };
  if (!query) return { ...out, execution_skipped: mapping.stop_reason === "auth_or_quota" ? "auth_or_quota_error" : schemaValidation === "failed" ? "live_schema_validation_failed" : "no_confident_goal_query" };
  if (schemaValidation === "failed") return { ...out, execution_skipped: "live_schema_validation_failed" };
  // Never run a query that silently drops a filter the goal asked for (address
  // or time range): the rows would look relevant but not answer the goal.
  if (mapping.filters_not_applied?.length) return { ...out, execution_skipped: "requested_filter_not_applied" };
  let result = chosen?.result;
  if (!result) {
    if (!intent.primary) {
      if (gatewayRequests >= MAX_GOAL_GATEWAY_REQUESTS) return { ...out, execution_skipped: "request_budget_exhausted" };
      result = await executeQuery({ ipfs_hash: selected.ipfs_hash, subgraph_id: selected.id, query });
      out.gateway_requests = ++gatewayRequests;
      if (result.data?._meta) rememberHealth(row, result);
      else if (result.error || result.errors?.length) { const cls = classifyGatewayFailure(result); rememberHealth(row, result, { failure_class: cls === "serving" ? "serving" : "query", evidence: failureEvidence(result) }); }
    } else {
      return { ...out, execution_skipped: mapping.stop_reason || "not_executed" };
    }
  }
  out.execution_attempted = true;
  out.validation.gateway_execution = result.http_status >= 200 && result.http_status < 300 &&
    !result.error && !result.errors?.length && result.data != null ? "succeeded" : "failed";
  out.executed = out.validation.gateway_execution === "succeeded";
  if (out.executed && tokenKind && mapping.collection && Array.isArray(result.data?.[mapping.collection])) {
    const tq = applyTokenQuality(result.data[mapping.collection], { network: selected.network, trusted: trusted.set, handling: spam_handling, kind: tokenKind, collection: mapping.collection });
    if (tq.report) {
      result = { ...result, data: { ...result.data, [mapping.collection]: tq.rows } };
      out.token_quality = tq.report;
    }
  }
  out.result = result;
  out.freshness = freshnessFor(row);
  return out;
}

function getDeployment30dayQueryCounts(args = {}) {
  let hashes = args.ipfs_hashes;
  if (typeof hashes === "string") hashes = [hashes];
  if (!Array.isArray(hashes)) hashes = [];
  hashes = hashes.map((h) => String(h || "").trim()).filter(Boolean);

  let ids = args.ids;
  if (typeof ids === "string") ids = [ids];
  if (!Array.isArray(ids)) ids = [];
  if (args.id) ids.push(String(args.id).trim());
  if (args.ipfs_hash) hashes.push(String(args.ipfs_hash).trim());
  ids = ids.filter(Boolean);

  const keys = [...hashes, ...ids];
  if (!keys.length) {
    return { error: "ipfs_hashes (array of Qm...) or ids is required" };
  }

  const deployments = keys.map((key) => {
    const row = getDb()
      .prepare(
        `SELECT id, display_name, network, ipfs_hash, query_volume_30d, reliability_score
         FROM subgraphs WHERE id = ? OR ipfs_hash = ?`,
      )
      .get(key, key);
    if (!row) {
      return {
        requested: key,
        ipfs_hash: null,
        id: null,
        query_volume_30d: null,
        error: "not_in_registry",
      };
    }
    return {
      requested: key,
      id: row.id,
      ipfs_hash: row.ipfs_hash,
      display_name: row.display_name,
      network: row.network,
      reliability_score: row.reliability_score,
      query_volume_30d: row.query_volume_30d ?? 0,
      source: "registry",
    };
  });

  return {
    source: "registry",
    note:
      "These are the crawler's query_volume_30d figures — the same numbers search/recommend already return. " +
      "The official subgraph MCP's get_deployment_30day_query_counts was observed returning 0 for deployments that plainly serve traffic (ENS ~34M, Lido ~4.7M). We do not copy that oracle.",
    deployments,
    total_deployments_processed: deployments.length,
  };
}

const EXECUTE_QUERY_DESCRIPTION =
  "Opt-in: POST a GraphQL query to The Graph gateway for a discovered subgraph. Discovery tools (search_subgraphs, recommend_subgraph, semantic_search_subgraphs, get_subgraph_detail) NEVER execute queries — call this tool only when the user/caller wants data fetched. Accepts id (subgraph id), subgraph_id, deployment_id (0x… 32-byte), or ipfs_hash (Qm…), plus query and optional variables. Replaces official execute_query_by_subgraph_id / execute_query_by_deployment_id / execute_query_by_ipfs_hash. When THE_GRAPH_STUDIO_API_KEY is set, POSTs to gateway.thegraph.com with Authorization: Bearer. If no key, returns {error: credentials_required, query_url, query_url_x402, hint} immediately — does not hang, does not auto-pay x402. Gateway often returns HTTP 200 with a GraphQL error body when auth is missing; http_status and errors are surfaced honestly.";

const GET_SCHEMA_DESCRIPTION =
  "Opt-in: return the GraphQL schema for a subgraph. Discovery tools never introspect. Accepts id / subgraph_id / deployment_id / ipfs_hash. Always returns registry_schema from the local index when the subgraph is in the corpus (entities, example_query, fingerprint, stability) with no network call. When THE_GRAPH_STUDIO_API_KEY is set, also POSTs a __schema introspection to the gateway. If no key, live introspection is omitted and a credentials_required block includes query_url and query_url_x402 so the caller can introspect themselves. Replaces official get_schema_by_subgraph_id / get_schema_by_deployment_id / get_schema_by_ipfs_hash.";

const IDENTIFIER_PROPS = {
  id: {
    type: "string",
    description: "Subgraph id (e.g. 5zvR82…). Also accepts an IPFS hash or 0x deployment id — it is classified by shape.",
  },
  subgraph_id: {
    type: "string",
    description: "Official-MCP alias of id. Subgraph id for the current deployment.",
  },
  deployment_id: {
    type: "string",
    description: "32-byte deployment id (0x + 64 hex). Queries gateway deployments/id/…",
  },
  ipfs_hash: {
    type: "string",
    description: "Manifest IPFS hash (Qm…). Queries gateway deployments/id/…, matching official subgraph-MCP.",
  },
};


// ── MCP Server ─────────────────────────────────────────────

// Tools that cannot work without a Studio API key. Every one of them returns
// credentials_required when none is set.
const KEYED_TOOLS = new Set([
  "check_subgraph_health",
  "execute_query", "execute_query_by_subgraph_id", "execute_query_by_deployment_id",
  "execute_query_by_ipfs_hash", "get_schema", "get_schema_by_subgraph_id",
  "get_schema_by_deployment_id", "get_schema_by_ipfs_hash",
]);

// Advertise only what this process can actually do.
//
// A tool list is injected into every model context. Omit credential-only
// capabilities from keyless servers instead of inviting fruitless calls.
// query_for_goal stays visible because its default preparation path is local.
//
// This matters most for the deployment where it is least visible: a public
// discovery endpoint runs keyless by design, precisely so there is no
// credential for an unauthenticated caller to spend.
//
// The discovery tools still return query_url and query_url_x402 on every hit,
// so a caller loses no ability to run its own query — only the pretence that
// this server would run it for them. Set SUBGRAPH_REGISTRY_LIST_ALL_TOOLS=1 to
// advertise everything regardless.
function listableTools() {
  if (process.env.SUBGRAPH_REGISTRY_LIST_ALL_TOOLS === "1") return TOOLS;
  if (studioApiKey()) return TOOLS;
  return TOOLS.filter((t) => !KEYED_TOOLS.has(t.name));
}

const TOOLS = [
  {
    name: "find_by_contract",
    description: "Discovery only: exact case-insensitive EVM contract lookup from crawled manifests. Optional chain (aliases supported); omitted chain searches all networks. Ranks allocated, non-denied snapshot deployments by reliability then volume. Returns matched manifest records, deployment-level schema entities (NOT verified contract-to-entity mappings), starter and cached freshness. No live calls or payments.",
    inputSchema: { type: "object", additionalProperties: false, required: ["address"], properties: {
      address: { type: "string", description: "0x-prefixed 40-hex EVM address" },
      chain: { type: "string", description: "Optional network, e.g. ethereum, base, arbitrum" },
      limit: { type: "integer", minimum: 1, maximum: 20, default: 3 },
    } },
  },
  {
    name: "check_subgraph_health",
    description: "Opt-in: one fixed _meta query against The Graph gateway using your Studio API key, pinning known subgraphs to their crawled deployment. Reports observed timestamp, indexed block/timestamp, indexing errors or honest failure/unknown states. Does NOT establish sync to chain head or trigger x402 payments. Observations are process-local, stale after five minutes and lost on restart; discovery never probes automatically.",
    inputSchema: { type: "object", additionalProperties: false, properties: IDENTIFIER_PROPS },
  },
  {
    name: "query_for_goal",
    description: "Turn a goal into a bounded, goal-specific GraphQL query: maps intent (pool ids, swaps, candles/OHLCV, daily/hourly data, positions, liquidations, tokens, addresses, time ranges, latest/top) to a deployment entity from the registry's crawled entity names, with rationale, confidence, unmet parts and ranked alternatives. Returns query:null instead of a misleading query when no entity maps confidently; goals without entity intent get the stored starter labelled generic. Keyless default makes NO network call. validate_schema=true (your own Studio key) adds ONE scoped introspection request per deployment to confirm fields/arguments, typed ordering/filters and serving freshness; execute=true adds ONE gateway POST. If the chosen deployment times out, has failing indexers or is stale, it is skipped (reported in goal_mapping.skipped_deployments) and the next deployment that fits the goal is tried: at most 3 deployments and 6 gateway requests, never x402. Reward/curation status is not treated as unhealthy. Token/pool results are checked for likely spam (URL/lure names, implausible TVL, TVL without volume, low activity): flagged rows are reported in token_quality and, by default, moved after the others; nothing is removed. Without a key, onboarding explains the human-operator key setup.",
    inputSchema: { type: "object", additionalProperties: false, required: ["goal"], properties: {
      goal: { type: "string", minLength: 1, maxLength: 1000 },
      chain: { type: "string" },
      first: { type: "integer", minimum: 1, maximum: 10, description: "Rows to request; defaults to a number in the goal (e.g. top 3) or 5" },
      execute: { type: "boolean", default: false, description: "Explicit opt-in to spend a Studio gateway query; never auto-pays x402" },
      validate_schema: { type: "boolean", default: false, description: "Opt-in: with your own Studio key, one scoped live introspection request validates the generated fields/arguments before any execution" },
      include_denied: { type: "boolean", default: false, description: "Also consider deployments with denied indexing rewards (not proof of unavailability) for entity matching" },
      include_unserved: { type: "boolean", default: false, description: "Also consider deployments with zero active allocations in the snapshot (not a queryability test)" },
      spam_handling: { type: "string", enum: ["flag_and_push_down", "flag_only", "off"], default: "flag_and_push_down", description: "Token/pool rows: flag likely spam and move flagged rows last (default), only flag, or disable. Rows are never removed." },
      trusted_tokens: { type: "array", maxItems: 50, items: { type: "string", pattern: "^0x[0-9a-fA-F]{40}$" }, description: "Extra known-good token addresses never flagged as spam (adds to a small built-in per-chain allowlist)" },
    } },
  },
  {
    name: "search_subgraphs",
    description:
      "Search and filter the classified subgraph registry (15,000+ subgraphs). Filter by domain (defi, nfts, dao, gaming, identity, infrastructure, social, analytics), network (mainnet, arbitrum-one, base, matic, bsc, optimism, avalanche), protocol_type (dex, lending, bridge, staking, options, perpetuals, nft-marketplace, yield-aggregator, governance, name-service), canonical entity type (liquidity_pool, trade, token, position, vault, loan, collateral, liquidation, nft_collection, nft_item, nft_sale, proposal, delegate, domain_name, account, transaction, daily_snapshot, hourly_snapshot), or free-text keyword. Returns subgraphs ranked by reliability score. Discovery only — this tool does not execute GraphQL and never introspects a schema. To run a query, call execute_query (opt-in). To inspect a schema, call get_schema (opt-in). Each result carries the subgraph id, a ready-to-run example_query, and both query routes in `payment_options`: a keyed gateway URL (Authorization: Bearer) or an x402 URL ($0.01 USDC on Base, no key). Pass the id to your own Graph client if you have one. Plus age_days and maturity (new | emerging | established). Because reliability_score is traction-weighted it can favour older deployments, so a separate `emerging` list carries recent matches that ranked below the main cut for age rather than quality — read `emerging_caveat` before offering one to a user.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        query: { type: "string", maxLength: 1000, description: "Free-text search across names and descriptions. A standalone known chain or alias (e.g. arc, ethereum) becomes an explicit network filter unless network is supplied; inferred_network makes this visible" },
        domain: { type: "string", maxLength: 1000, description: "Filter by domain: defi, nfts, dao, gaming, identity, infrastructure, social, analytics" },
        network: { type: "string", maxLength: 1000, description: "Filter by chain: mainnet, arbitrum-one, base, matic, bsc, optimism, avalanche, etc." },
        protocol_type: { type: "string", maxLength: 1000, description: "Filter by protocol type: dex, lending, bridge, staking, options, perpetuals, etc." },
        entity: { type: "string", maxLength: 1000, description: "Filter by canonical entity: liquidity_pool, trade, token, position, vault, loan, etc." },
        min_reliability: { type: "number", minimum: 0, maximum: 1, description: "Minimum reliability score (0-1). Higher = more query fees, volume, curation signal, and indexer allocation. NOTE: this traction-weighted score can favor older deployments; 30-day volume is a rolling window — setting a floor here filters out good recent subgraphs along with bad ones." },
        limit: { type: "integer", description: "Max results to return, 1–100 (default: 20); total is returned count, not corpus match count. No offset/cursor pagination.", minimum: 1, maximum: 100, default: 20 },
        include_unserved: {
          type: "boolean",
          description: "Include records with zero active allocations in the registry snapshot. Default false is a discovery heuristic, NOT a queryability test; Studio or other serving routes may work without allocations.",
          default: false,
        },
        include_denied: {
          type: "boolean",
          description: "Include curation-denied deployments (deniedAt > 0 — denied indexing rewards; not proof of spam or query failure). Default false. When true, each result carries denied: true so the choice stays visible.",
          default: false,
        },
        include_testnets: {
          type: "boolean",
          description: "Include testnet deployments (sepolia, goerli, holesky, chapel, fuji, mumbai, amoy, *-testnet). Default false — a testnet twin's text is near-identical to its mainnet original, so it competes for the top slot without being the thing anyone wanted. Ignored when you explicitly request a testnet network, so network:\"sepolia\" still works. Each result carries testnet: true|false.",
          default: false,
        },
      },
    },
  },
  {
    name: "recommend_subgraph",
    description:
      "Given a natural-language goal like 'find DEX trades on Arbitrum' or 'get lending liquidation data', returns the best matching subgraphs with reliability scores. Automatically infers domain and protocol type from the goal. Discovery only — it returns ids and starter queries, it does not execute GraphQL. Each result carries both query routes in `payment_options`: a keyed gateway URL (Authorization: Bearer <STUDIO_API_KEY>) or an x402 URL ($0.01 USDC on Base, no key).",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        goal: { type: "string", maxLength: 1000, description: "What you want to do, e.g. 'query Uniswap pool data on Base'" },
        chain: { type: "string", maxLength: 1000, description: "Optional chain filter: mainnet, arbitrum-one, base, matic, etc." },
      },
      required: ["goal"],
    },
  },
  {
    name: "get_subgraph_detail",
    description:
      "Get full classification detail for a specific subgraph by its subgraph ID or IPFS hash. Returns domain, protocol type, canonical entities, all entity names with field counts, reliability score, signal data, both query URLs (x402 and legacy), the x402 pricing manifest ($0.01 USDC on Base), and step-by-step instructions for both query paths.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        subgraph_id: { type: "string", description: "Subgraph ID or IPFS hash (Qm...)" },
      },
      required: ["subgraph_id"],
    },
  },
  {
    name: "list_registry_stats",
    description:
      "Get an overview of the subgraph registry: total count, available domains, networks, and protocol types with counts. Use this to understand what data is available before searching.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {},
    },
  },
  {
    name: "semantic_search_subgraphs",
    description:
      "Discovery only — this tool does not execute GraphQL and never introspects a schema. To run a query, call execute_query (opt-in). To inspect a schema, call get_schema (opt-in). Semantic vector search over the subgraph registry. Embeds the query string with sentence-transformers/all-MiniLM-L6-v2 (the same model architecture used at crawl time; the runtime uses an INT8-quantized ONNX build so absolute scores can drift ~0.01-0.03 from the float32 reference but top-K rankings are stable) and ranks subgraphs by cosine similarity against the precomputed 384-dim embedding of each subgraph's description + entities + protocol metadata. Prefer this over search_subgraphs when the goal is fuzzy, paraphrased, or describes a use-case rather than a literal protocol/entity name. Supports the same domain/network/protocol_type/min_reliability pre-filters as search_subgraphs (applied as SQL WHERE before cosine scoring for performance). Returns the same shape as search_subgraphs plus a `semantic_score` in [0,1] (>0.5 is typically a strong match).",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        query: {
          type: "string",
          description: "Natural-language description of the data the agent wants to query, e.g. 'on-chain options market activity' or 'lending positions near liquidation'",
        },
        limit: {
          type: "integer",
          description: "Max results to return (default 10, max 50)",
          default: 10,
          minimum: 1,
          maximum: 50,
        },
        min_score: {
          type: "number", minimum: 0, maximum: 1,
          description: "Minimum cosine similarity to include (0-1). Default 0.3.",
          default: 0.3,
        },
        include_unserved: {
          type: "boolean",
          description: "Include records with zero active allocations in the registry snapshot. Default false is a discovery heuristic, NOT a queryability test; Studio or other serving routes may work without allocations.",
          default: false,
        },
        include_denied: {
          type: "boolean",
          description: "Include curation-denied deployments (deniedAt > 0 — denied indexing rewards; not proof of spam or query failure). Default false. When true, each result carries denied: true so the choice stays visible.",
          default: false,
        },
        include_testnets: {
          type: "boolean",
          description: "Include testnet deployments (sepolia, goerli, holesky, chapel, fuji, mumbai, amoy, *-testnet). Default false — a testnet twin's text is near-identical to its mainnet original, so it competes for the top slot without being the thing anyone wanted. Ignored when you explicitly request a testnet network, so network:\"sepolia\" still works. Each result carries testnet: true|false.",
          default: false,
        },
        domain: {
          type: "string",
          description: "Pre-filter by domain (defi, nfts, dao, gaming, identity, infrastructure, social, analytics)",
        },
        network: {
          type: "string",
          description: "Pre-filter by chain (mainnet, arbitrum-one, base, matic, bsc, optimism, avalanche, etc.)",
        },
        protocol_type: {
          type: "string",
          description: "Pre-filter by protocol type (dex, lending, bridge, staking, options, perpetuals, etc.)",
        },
        min_reliability: {
          type: "number", minimum: 0, maximum: 1,
          description: "Pre-filter: minimum reliability score (0-1).",
        },
      },
      required: ["query"],
    },
  },
  {
    name: "get_schema_changes",
    description:
      "Return chronological schema-fingerprint changes for a subgraph. Each row is one detected fingerprint change with prev_fingerprint, fingerprint, and detected_at (unix seconds). Use to assess schema stability before depending on a subgraph: a long stable_days value means the schema contract is mature; a recent changed_within_24h means the upstream protocol just shipped a schema update and queries may need to be revisited.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        subgraph_id: {
          type: "string",
          description: "Subgraph ID (the same id used by other tools)",
        },
        since_timestamp: {
          type: "integer",
          description: "Only return changes detected at or after this unix timestamp (seconds). Default 0 (full history).",
          default: 0,
        },
      },
      required: ["subgraph_id"],
    },
  },
  {
    name: "execute_query",
    description: EXECUTE_QUERY_DESCRIPTION,
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        ...IDENTIFIER_PROPS,
        query: {
          type: "string",
          description: "GraphQL query document to POST to the gateway",
        },
        variables: {
          type: "object",
          description: "Optional GraphQL variables object",
          additionalProperties: true,
        },
      },
      required: ["query"],
    },
  },
  {
    name: "execute_query_by_subgraph_id",
    description:
      "Alias of execute_query for the official subgraph-MCP name. Pass subgraph_id + query. Prefer execute_query, which also accepts deployment_id and ipfs_hash. Opt-in; discovery tools never execute.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        subgraph_id: { type: "string", description: "Subgraph ID (e.g. 5zvR82…)" },
        query: { type: "string", description: "GraphQL query document" },
        variables: { type: "object", additionalProperties: true, description: "Optional GraphQL variables" },
      },
      required: ["subgraph_id", "query"],
    },
  },
  {
    name: "execute_query_by_deployment_id",
    description:
      "Alias of execute_query for the official subgraph-MCP name. Pass deployment_id (0x + 64 hex) + query. Opt-in; discovery tools never execute.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        deployment_id: { type: "string", description: "32-byte deployment id (0x…)" },
        query: { type: "string", description: "GraphQL query document" },
        variables: { type: "object", additionalProperties: true, description: "Optional GraphQL variables" },
      },
      required: ["deployment_id", "query"],
    },
  },
  {
    name: "execute_query_by_ipfs_hash",
    description:
      "Alias of execute_query for the official subgraph-MCP name. Pass ipfs_hash (Qm…) + query. Opt-in; discovery tools never execute.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        ipfs_hash: { type: "string", description: "Manifest IPFS hash (Qm…)" },
        query: { type: "string", description: "GraphQL query document" },
        variables: { type: "object", additionalProperties: true, description: "Optional GraphQL variables" },
      },
      required: ["ipfs_hash", "query"],
    },
  },
  {
    name: "get_schema",
    description: GET_SCHEMA_DESCRIPTION,
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: { ...IDENTIFIER_PROPS },
    },
  },
  {
    name: "get_schema_by_subgraph_id",
    description:
      "Alias of get_schema for the official subgraph-MCP name. Pass subgraph_id. Returns local registry_schema without a network call; live __schema introspection only if THE_GRAPH_STUDIO_API_KEY is set. Opt-in; discovery tools never introspect.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        subgraph_id: { type: "string", description: "Subgraph ID (e.g. 5zvR82…)" },
      },
      required: ["subgraph_id"],
    },
  },
  {
    name: "get_schema_by_deployment_id",
    description:
      "Alias of get_schema for the official subgraph-MCP name. Pass deployment_id (0x + 64 hex). Live introspection needs THE_GRAPH_STUDIO_API_KEY — deployment ids are not stored in the local corpus. Opt-in.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        deployment_id: { type: "string", description: "32-byte deployment id (0x…)" },
      },
      required: ["deployment_id"],
    },
  },
  {
    name: "get_schema_by_ipfs_hash",
    description:
      "Alias of get_schema for the official subgraph-MCP name. Pass ipfs_hash (Qm…). Local registry_schema when the hash is in the corpus. Opt-in; discovery tools never introspect.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        ipfs_hash: { type: "string", description: "Manifest IPFS hash (Qm…)" },
      },
      required: ["ipfs_hash"],
    },
  },
  {
    name: "get_top_subgraph_deployments",
    description:
      "Find subgraphs whose crawled manifest indexes a given contract on a given chain. Official subgraph-MCP name, better ranking: reliability_score then real query_volume_30d, not query fees and not the official 0-count oracle. contract_addresses come from subgraph.yaml dataSources/templates at crawl time — coverage is high for EVM subgraphs, empty for most substreams-powered ones. Does not query the gateway. Default 3 results, matching official.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        contract_address: {
          type: "string",
          description: "EVM contract address (0x-prefixed 40 hex)",
        },
        chain: {
          type: "string",
          description: "Official subgraph-MCP uses graph-node ids here (`mainnet`, not `ethereum`). We accept both; aliases resolve (ethereum→mainnet, arbitrum→arbitrum-one, polygon→matic).",
        },
        limit: {
          type: "integer",
          description: "Max results (default 3, max 20)",
          default: 3,
        },
      },
      required: ["contract_address", "chain"],
    },
  },
  {
    name: "get_deployment_30day_query_counts",
    description:
      "Return 30-day query volume for one or more deployments from the local registry. Official subgraph-MCP name; unlike official, these numbers are real (the official tool has been observed returning 0 for ENS, Lido, Uniswap). Pass ipfs_hashes (Qm…) and/or ids. Does not query the gateway. Unknown hashes return query_volume_30d: null with error not_in_registry rather than a fake 0.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        ipfs_hashes: {
          type: "array",
          items: { type: "string" },
          description: "Manifest IPFS hashes (Qm…), the official subgraph-MCP input",
        },
        ids: {
          type: "array",
          items: { type: "string" },
          description: "Subgraph ids to look up",
        },
        ipfs_hash: { type: "string", description: "Single IPFS hash convenience field" },
        id: { type: "string", description: "Single subgraph id convenience field" },
      },
    },
  },
];

const HANDLERS = {
  find_by_contract: findByContract,
  check_subgraph_health: checkSubgraphHealth,
  query_for_goal: queryForGoal,
  search_subgraphs: searchSubgraphs,
  recommend_subgraph: recommendSubgraph,
  get_subgraph_detail: getSubgraphDetail,
  list_registry_stats: listRegistryStats,
  semantic_search_subgraphs: semanticSearchSubgraphs,
  get_schema_changes: getSchemaChanges,
  execute_query: executeQuery,
  execute_query_by_subgraph_id: executeQuery,
  execute_query_by_deployment_id: executeQuery,
  execute_query_by_ipfs_hash: executeQuery,
  get_schema: getSchema,
  get_schema_by_subgraph_id: getSchema,
  get_schema_by_deployment_id: getSchema,
  get_schema_by_ipfs_hash: getSchema,
  get_top_subgraph_deployments: getTopSubgraphDeployments,
  get_deployment_30day_query_counts: getDeployment30dayQueryCounts,
};

function createServer() {
  const server = new Server(
    { name: "subgraph-registry", version: PKG_VERSION },
    { capabilities: { tools: {} } }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: listableTools(),
  }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const handler = HANDLERS[name];
    if (!handler) {
      return {
        content: [{ type: "text", text: JSON.stringify({ error: `Unknown tool: ${name}` }) }],
        isError: true,
      };
    }
    try {
      // semantic_search_subgraphs, execute_query and get_schema are async;
      // the rest are sync. `await` is a no-op on plain values.
      const result = await handler(args || {});
      return {
        content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: JSON.stringify({ error: err.message }) }],
        isError: true,
      };
    }
  });

  return server;
}

// ── SSE/HTTP Transport (OpenClaw + remote agents) ──────────
//
// Security model (0.13.1+):
// - Binds 127.0.0.1 unless MCP_HTTP_HOST says otherwise.
// - A non-loopback bind is REFUSED unless SUBGRAPH_REGISTRY_HTTP_TOKEN is set
//   (at least 24 characters). Then every route except /health requires
//   `Authorization: Bearer <token>` (constant-time compare) or gets 401, so no
//   unauthenticated remote caller can reach a tool that spends the operator's
//   Studio key.
// - Without a token, requests are also rejected unless they arrive from a
//   loopback socket with a loopback Host header (blocks DNS rebinding from a
//   browser page).
// The token is never logged or echoed.

export const HTTP_TOKEN_ENV = "SUBGRAPH_REGISTRY_HTTP_TOKEN";
export const MIN_HTTP_TOKEN_LENGTH = 24;

export function isLoopbackHost(host) {
  const h = String(host || "").trim().toLowerCase().replace(/^\[|\]$/g, "");
  return h === "localhost" || h === "::1" || /^127(\.\d{1,3}){3}$/.test(h) || /^::ffff:127(\.\d{1,3}){3}$/.test(h);
}

function hostHeaderName(value) {
  const v = String(value || "").trim().toLowerCase();
  if (v.startsWith("[")) return v.slice(1, v.indexOf("]"));
  return v.replace(/:\d+$/, "");
}

export function resolveHttpSecurity(env = process.env) {
  const host = (env.MCP_HTTP_HOST || "127.0.0.1").trim();
  const rawToken = env[HTTP_TOKEN_ENV];
  const token = typeof rawToken === "string" && rawToken.trim() ? rawToken.trim() : null;
  const loopback = isLoopbackHost(host);
  if (token && token.length < MIN_HTTP_TOKEN_LENGTH) {
    return { ok: false, host, loopback, error: `${HTTP_TOKEN_ENV} must be at least ${MIN_HTTP_TOKEN_LENGTH} characters.` };
  }
  if (!loopback && !token) {
    return {
      ok: false, host, loopback,
      error: `Refusing to bind HTTP transport to non-loopback host ${host} without ${HTTP_TOKEN_ENV}. ` +
        `Set ${HTTP_TOKEN_ENV} to a long random secret (clients send Authorization: Bearer <token>), ` +
        "or unset MCP_HTTP_HOST to bind 127.0.0.1 only.",
    };
  }
  return { ok: true, host, loopback, token, auth: token ? "bearer_token" : "loopback_only" };
}

function tokenMatches(expected, header) {
  const m = /^Bearer\s+(\S+)\s*$/i.exec(String(header || ""));
  if (!m) return false;
  // Hash both sides so lengths match and the compare is constant-time.
  const a = createHash("sha256").update(expected).digest();
  const b = createHash("sha256").update(m[1]).digest();
  return timingSafeEqual(a, b);
}

export function httpAuthMiddleware(security) {
  return (req, res, next) => {
    if (req.path === "/health") return next();
    if (security.token) {
      if (tokenMatches(security.token, req.headers.authorization)) return next();
      res.set("WWW-Authenticate", 'Bearer realm="subgraph-registry"');
      res.status(401).json({ error: "unauthorized", hint: "Send Authorization: Bearer <token>." });
      return;
    }
    // No token configured: loopback callers only, with a loopback Host header.
    if (isLoopbackHost(req.socket?.remoteAddress) && isLoopbackHost(hostHeaderName(req.headers.host))) return next();
    res.set("WWW-Authenticate", 'Bearer realm="subgraph-registry"');
    res.status(401).json({ error: "unauthorized", hint: `Loopback only. Set ${HTTP_TOKEN_ENV} to allow authenticated remote access.` });
  };
}

export function createHttpApp(security = resolveHttpSecurity()) {
  if (!security.ok) throw new Error(security.error);
  const app = express();
  app.disable("x-powered-by");
  app.use(httpAuthMiddleware(security));
  const sessions = new Map();

  app.get("/sse", async (req, res) => {
    const transport = new SSEServerTransport("/messages", res);
    sessions.set(transport.sessionId, transport);

    const server = createServer();

    res.on("close", () => {
      sessions.delete(transport.sessionId);
    });

    await server.connect(transport);
  });

  app.post("/messages", async (req, res) => {
    const sessionId = req.query.sessionId;
    const transport = sessions.get(sessionId);
    if (!transport) {
      res.status(400).json({ error: "Invalid or expired session" });
      return;
    }
    await transport.handlePostMessage(req, res);
  });

  app.get("/health", (_req, res) => {
    res.json({ status: "ok", subgraphs: getDb().prepare("SELECT COUNT(*) as c FROM subgraphs").get().c });
  });

  // ── payql compatibility shim ─────────────────────────────────────
  // payql (npm `payql`, same author) advertises PAYQL_REGISTRY_URL as a "free
  // discovery source (e.g. your own subgraph registry)" — but it POSTs the
  // Graph network subgraph's GraphQL document and reads
  // `data.subgraphMetadataSearch`, a shape this registry has never served. So
  // pointing payql here returned zero hits and, because the response still
  // parsed as JSON, it failed as an empty success rather than an error. The
  // two projects were built to compose and the seam between them was dead.
  //
  // Serve that shape. No GraphQL engine needed: the only input that varies is
  // the `text` variable, and the result set is what search_subgraphs already
  // computes. Answering in the incumbent's vocabulary means payql works
  // against this registry with no change on its side.
  //
  // Token amounts are returned as wei-scale strings because payql divides them
  // by 1e18 (weiToGRT); handing back plain GRT would under-report by 1e18.
  app.post("/graphql", express.json({ limit: "256kb" }), (req, res) => {
    try {
      const text = String(req.body?.variables?.text ?? "");
      const first = Math.max(1, Math.min(Number(req.body?.variables?.first) || 10, 50));
      // payql sends a prefix tsquery ("uniswap:* | v3:*"); strip the fulltext
      // operators back to plain words before handing them to LIKE matching.
      const plain = text.replace(/:\*/g, " ").replace(/[|&()]/g, " ").trim();
      const { subgraphs = [] } = searchSubgraphs({ query: plain, limit: first });
      res.json({
        data: {
          subgraphMetadataSearch: subgraphs.map((s) => ({
            displayName: s.display_name,
            description: s.description,
            categories: s.domain ? [s.domain] : [],
            subgraphs: [
              {
                id: s.id,
                active: true,
                currentSignalledTokens: null,
                currentVersion: {
                  subgraphDeployment: {
                    ipfsHash: s.ipfs_hash,
                    stakedTokens: null,
                    signalledTokens: null,
                    queryFeesAmount: null,
                  },
                },
              },
            ],
          })),
        },
      });
    } catch (err) {
      // Answer in GraphQL's error shape so a client that only knows GraphQL
      // sees a failure instead of an empty success — the exact trap this
      // route exists to close.
      res.status(500).json({ errors: [{ message: String(err?.message || err) }] });
    }
  });

  // ── OpenAPI 3.1 spec (auto-generated at release time) ────────────
  // scripts/gen-openapi.js inventories the TOOLS array + the REST
  // routes below and writes data/openapi.json. We serve the file
  // verbatim so consumers and codegens can hit a stable URL.
  app.get("/.well-known/openapi.json", (_req, res) => {
    if (!existsSync(OPENAPI_JSON_PATH)) {
      res.status(404).json({
        error: "openapi.json not present in this build",
        hint: "Run `node scripts/gen-openapi.js` to generate it.",
      });
      return;
    }
    try {
      const spec = JSON.parse(readFileSync(OPENAPI_JSON_PATH, "utf8"));
      res.type("application/json").json(spec);
    } catch (err) {
      res.status(500).json({ error: "openapi.json parse failed: " + err.message });
    }
  });

  // ── Stable per-subgraph manifest for ecosystem crawlers ───────────────
  // Other tools (E&N tooling, indexer dashboards, agent frameworks) can
  // hit this without needing MCP. JSON-LD so the shape is auto-discoverable.
  const serveManifest = (req, res) => {
    const id = req.params.id;
    const row = getDb()
      .prepare("SELECT * FROM subgraphs WHERE id = ? OR ipfs_hash = ?")
      .get(id, id);
    if (!row) {
      res.status(404).json({ error: `Subgraph '${id}' not found` });
      return;
    }
    const manifest = buildJsonLdManifest(row);
    if (!manifest) {
      res.status(500).json({ error: "Manifest build failed" });
      return;
    }
    res.type("application/ld+json").json(manifest);
  };

  // Canonical .well-known location + a friendlier alias under /subgraphs/
  app.get("/.well-known/subgraph/:id.jsonld", serveManifest);
  app.get("/subgraphs/:id.jsonld", serveManifest);

  // Discovery index so a crawler that doesn't know the ID can find one:
  // returns the top 100 by reliability with their .jsonld URLs.
  app.get("/.well-known/subgraph-index.jsonld", (_req, res) => {
    const rows = getDb()
      .prepare(
        "SELECT id, display_name, network, domain, reliability_score " +
        "FROM subgraphs WHERE active_allocation_count > 0 " +
        "ORDER BY reliability_score DESC LIMIT 100"
      ).all();
    res.type("application/ld+json").json({
      "@context": JSONLD_CONTEXT,
      "@type": "SubgraphIndex",
      generatedAt: new Date().toISOString(),
      count: rows.length,
      subgraphs: rows.map((r) => ({
        "@id": subgraphIri(r.id),
        id: r.id,
        name: r.display_name,
        network: r.network,
        domain: r.domain,
        reliabilityScore: r.reliability_score,
        manifest: `/.well-known/subgraph/${r.id}.jsonld`,
      })),
    });
  });

  return app;
}

function startHttpTransport(port) {
  // History: this once bound all interfaces while logging "localhost", and
  // /sse and /messages had no authentication, so anyone on the LAN could
  // spend the operator's Graph quota. Now loopback is the default and a
  // non-loopback bind requires a bearer token (see resolveHttpSecurity).
  const security = resolveHttpSecurity();
  if (!security.ok) {
    console.error(`Fatal: ${security.error}`);
    process.exit(1);
  }
  const app = createHttpApp(security);
  const host = security.host;
  app.listen(port, host, () => {
    const shown = host === "0.0.0.0" || host === "::" ? `<this-host>:${port}` : `${host}:${port}`;
    console.error(`SSE transport listening on http://${shown}/sse (bound to ${host}; auth: ${security.auth})`);
    console.error(`Well-known manifest at http://${shown}/.well-known/subgraph/{id}.jsonld`);
  });
}

// ── Entry Point ────────────────────────────────────────────

async function main() {
  await ensureDb();

  const subgraphCount = getDb().prepare("SELECT COUNT(*) as c FROM subgraphs").get().c;
  const httpPort = process.env.MCP_HTTP_PORT || (process.argv.includes("--http") ? "3848" : null);
  const httpOnly = process.argv.includes("--http-only");

  // Start SSE/HTTP transport if requested
  if (httpPort || httpOnly) {
    const port = parseInt(httpPort || "3848", 10);
    startHttpTransport(port);
  }

  // Start stdio transport (default, skip if --http-only)
  if (!httpOnly) {
    const server = createServer();
    const transport = new StdioServerTransport();
    await server.connect(transport);
  }

  console.error(`Subgraph Registry MCP server running (${subgraphCount} subgraphs)`);
}

// ── Exports for tooling (OpenAPI generator, tests) ────────
// scripts/gen-openapi.js imports TOOLS + REST_ROUTES at build time.
// Inventory the HTTP routes declaratively here so generator + runtime
// stay in lockstep — drift would silently mis-document the API.
export const REST_ROUTES = [
  {
    method: "get",
    path: "/health",
    summary: "Liveness probe + total subgraph count",
    response: {
      type: "object",
      properties: {
        status: { type: "string", enum: ["ok"] },
        subgraphs: { type: "integer" },
      },
      required: ["status", "subgraphs"],
    },
  },
  {
    method: "post",
    path: "/graphql",
    summary: "payql compatibility — search results in subgraphMetadataSearch shape",
    description:
      "Answers a `subgraphMetadataSearch` query in The Graph network subgraph's shape, so payql (PAYQL_REGISTRY_URL) can use this registry as a free discovery source with no change on its side. Only the `text` and `first` variables are read; results come from the same index search_subgraphs uses.",
    response: { type: "object", description: "{ data: { subgraphMetadataSearch: [...] } }" },
  },
  {
    method: "get",
    path: "/.well-known/subgraph/{id}.jsonld",
    summary: "JSON-LD manifest for a single subgraph (canonical location)",
    parameters: [
      { name: "id", in: "path", required: true, schema: { type: "string" } },
    ],
    response: { type: "object", description: "JSON-LD SubgraphDeployment manifest" },
  },
  {
    method: "get",
    path: "/subgraphs/{id}.jsonld",
    summary: "JSON-LD manifest alias (same payload as /.well-known/...)",
    parameters: [
      { name: "id", in: "path", required: true, schema: { type: "string" } },
    ],
    response: { type: "object", description: "JSON-LD SubgraphDeployment manifest" },
  },
  {
    method: "get",
    path: "/.well-known/subgraph-index.jsonld",
    summary: "Top-100 subgraphs by reliability with their manifest URLs",
    response: { type: "object", description: "JSON-LD SubgraphIndex" },
  },
  {
    method: "get",
    path: "/.well-known/openapi.json",
    summary: "This OpenAPI spec, self-served for discovery",
    response: { type: "object", description: "OpenAPI 3.1 document" },
  },
];

export { TOOLS, HANDLERS };
// Test-only: clear process-local health observations between test cases.
export function resetHealthObservationsForTests() { healthObservations.clear(); }

// Only auto-start when invoked as the entry point — importing the
// module for tooling (scripts/gen-openapi.js, tests) MUST NOT spawn
// the MCP server or open the SQLite file. Use pathToFileURL so the
// comparison works on Windows where process.argv[1] uses backslashes
// while import.meta.url is forward-slashed.
// Whether this file was RUN, as opposed to imported (scripts/gen-openapi.js
// imports it for TOOLS[] and must not spawn a server).
//
// This has to compare real paths. npm installs a bin as a symlink —
// node_modules/.bin/subgraph-registry-mcp -> ../subgraph-registry-mcp/src/index.js
// — and Node sets import.meta.url to the RESOLVED target while argv[1] keeps
// the symlink. So the old comparison was:
//
//   pathToFileURL(argv[1]) = file:///…/node_modules/.bin/subgraph-registry-mcp
//   import.meta.url        = file:///…/subgraph-registry-mcp/src/index.js
//   basename(argv[1])      = "subgraph-registry-mcp"   (not "index.js")
//
// Both branches false, so main() never ran: the process exited 0, instantly,
// silently, and every MCP host reported "Connection closed" with 0 tools. It
// worked in local testing only because `node src/index.js` satisfies the
// basename fallback — which is exactly why no test caught it. The package has
// never once started over npx.
//
// realpathSync collapses the symlink on both sides, so npx, `npm i -g`, a
// direct path and a symlinked directory all agree. Note the URL comparison was
// already unreliable on its own: on macOS a /var path resolves to /private/var,
// so even a direct run failed that branch and survived on the basename check.
const _isMain =
  process.argv[1] !== undefined &&
  (() => {
    try {
      return realpathSync(process.argv[1]) === realpathSync(__filename);
    } catch {
      return false;
    }
  })();

if (_isMain) {
  main().catch((err) => {
    console.error("Fatal:", err);
    process.exit(1);
  });
}
