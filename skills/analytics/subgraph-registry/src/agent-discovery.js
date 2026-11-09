// Small, testable safety/provenance helpers for the opt-in agent workflow.
import { parse, print, Kind } from "graphql";

export function boundedStarter(source, first = 5) {
  if (!Number.isInteger(first) || first < 1 || first > 10) {
    throw new Error("first must be an integer from 1 to 10");
  }
  if (typeof source !== "string" || !source.trim() || source.length > 8000) {
    throw new Error("No bounded registry starter query is available");
  }
  const doc = parse(source, { noLocation: true, maxTokens: 500 });
  const [op] = doc.definitions;
  if (doc.definitions.length !== 1 || op.kind !== Kind.OPERATION_DEFINITION ||
      op.operation !== "query" || op.variableDefinitions?.length || op.directives?.length) {
    throw new Error("Starter must contain one query without variables or directives");
  }
  const roots = op.selectionSet.selections;
  const collections = roots.filter((f) => f.name?.value !== "_meta");
  if (collections.length !== 1 || roots.length > 2) {
    throw new Error("Starter must select one collection and optional _meta");
  }
  function fieldOnly(f) {
    if (f.kind !== Kind.FIELD || f.alias || f.directives?.length) {
      throw new Error("Starter aliases, fragments and directives are not supported");
    }
  }
  for (const root of roots) {
    fieldOnly(root);
    if (root.name.value === "_meta") {
      // Do not allow stored metadata selections to hide expensive nested lists.
      const meta = print({ kind: Kind.DOCUMENT, definitions: [{ ...op,
        selectionSet: { kind: Kind.SELECTION_SET, selections: [root] } }] });
      if (root.arguments?.length || !/^\{\s*_meta\s*\{\s*block\s*\{\s*number(?:\s+timestamp)?\s*\}\s*\}\s*\}$/.test(meta)) {
        throw new Error("Unsupported starter metadata selection");
      }
      continue;
    }
    if (root.name.value.startsWith("_") || !root.selectionSet ||
        root.selectionSet.selections.length > 10) {
      throw new Error("Starter must select at most ten scalar fields");
    }
    for (const f of root.selectionSet.selections) {
      fieldOnly(f);
      if (f.selectionSet || f.arguments?.length) {
        throw new Error("Nested starter collections are not supported");
      }
    }
    const args = root.arguments || [];
    const names = args.map((a) => a.name.value);
    if (new Set(names).size !== names.length || args.some((a) =>
      !["first", "orderBy", "orderDirection"].includes(a.name.value) ||
      (a.name.value === "first" ? a.value.kind !== Kind.INT : a.value.kind !== Kind.ENUM))) {
      throw new Error("Unsupported starter arguments");
    }
    root.arguments = [
      ...args.filter((a) => a.name.value !== "first"),
      { kind: Kind.ARGUMENT, name: { kind: Kind.NAME, value: "first" },
        value: { kind: Kind.INT, value: String(first) } },
    ];
  }
  return print(doc);
}

export const HEALTH_STALE_SECONDS = 300;
export const HEALTH_QUERY = "{ _meta { deployment hasIndexingErrors block { number timestamp } } }";

export function healthObservation(result, observedAt = Math.floor(Date.now() / 1000)) {
  const meta = result.data?._meta;
  const transportOk = result.http_status >= 200 && result.http_status < 300 &&
    !result.error && !result.errors?.length;
  const validBlock = Number.isSafeInteger(meta?.block?.number) && meta.block.number >= 0;
  const usable = transportOk && validBlock;
  return {
    observed_at: observedAt,
    status: !transportOk ? "query_failed" : !usable ? "metadata_unavailable" :
      meta.hasIndexingErrors === true ? "indexing_errors" : "serving",
    indexed_block_number: usable ? meta.block.number : null,
    indexed_block_timestamp: usable && Number.isSafeInteger(meta.block.timestamp) &&
      meta.block.timestamp > 0 ? meta.block.timestamp : null,
    has_indexing_errors: usable && typeof meta.hasIndexingErrors === "boolean"
      ? meta.hasIndexingErrors : null,
    deployment: usable && typeof meta.deployment === "string" ? meta.deployment : null,
    // A successful gateway query cannot establish distance to the chain head.
    synced_to_chain_head: null,
    http_status: result.http_status ?? null,
  };
}

export function freshness(row, observation, now = Math.floor(Date.now() / 1000)) {
  return {
    source: "process_local_gateway_observation",
    registry_updated_at: row?.updated_at || null,
    registry_updated_at_meaning: "upstream subgraph metadata update, NOT a crawl or health timestamp",
    live: observation ? {
      ...observation,
      age_seconds: Math.max(0, now - observation.observed_at),
      stale: now - observation.observed_at > HEALTH_STALE_SECONDS,
    } : null,
    caveat: "No background probes. Observations are process-local, stale after 300 seconds, and lost on restart. Serving does not mean synced or current with the chain head.",
  };
}

export function findContractDeployments(db, { address, chain, limit = 3 }, normalizeNetwork) {
  if (typeof address !== "string" || !/^0x[0-9a-fA-F]{40}$/.test(address.trim())) {
    return { error: "address must be a 0x-prefixed 40-hex EVM address" };
  }
  if (chain !== undefined && (typeof chain !== "string" || !chain.trim())) {
    return { error: "chain must be a non-empty network name" };
  }
  if (!Number.isInteger(limit) || limit < 1 || limit > 20) {
    return { error: "limit must be an integer from 1 to 20" };
  }
  const needle = address.trim().toLowerCase();
  const network = chain === undefined ? null : normalizeNetwork(chain);
  // SQL does exact address matching before LIMIT, not a substring prefilter
  // whose false positives could crowd a real match out of the candidate set.
  const rows = db.prepare(`
    SELECT s.* FROM subgraphs s
    WHERE active_allocation_count > 0 AND denied_at = 0
      AND EXISTS (
        SELECT 1 FROM json_each(CASE WHEN json_valid(contract_addresses)
          THEN contract_addresses ELSE '[]' END) c
        WHERE c.type = 'object' AND lower(json_extract(CASE WHEN c.type = 'object' THEN c.value ELSE '{}' END, '$.address')) = ?
      )
    ORDER BY reliability_score DESC, query_volume_30d DESC, id ASC
  `).iterate(needle);
  const deployments = [];
  const seen = new Set();
  for (const row of rows) {
    const contracts = JSON.parse(row.contract_addresses);
    if (!Array.isArray(contracts)) continue;
    const matched = contracts.filter((c) => c &&
      String(c.address || "").toLowerCase() === needle &&
      (!network || normalizeNetwork(c.network || row.network) === network));
    if (!matched.length) continue;
    // Do not collapse identical deployments across different chains.
    const key = `${row.ipfs_hash || row.id}:${row.network}`;
    if (seen.has(key)) continue;
    seen.add(key);
    deployments.push({ row, matched });
    if (deployments.length >= limit) break;
  }
  return { address: needle, chain: network, deployments };
}
