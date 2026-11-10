// Goal-to-GraphQL planning for query_for_goal.
//
// The bundled registry stores entity NAMES (plus a field count and canonical
// type) for every deployment, and the field names of ONE stored starter
// entity. It does not store field types. So:
//   * keyless planning can pick the entity that matches the goal, derive its
//     collection the way graph-node does, and select `id` (always present) plus
//     stored-starter fields when the starter already targets that entity;
//   * ordering, typed filters and other fields need the live schema, which is
//     an explicit opt-in (validate_schema) using the caller's own Studio key.
// Every plan reports what it could not satisfy instead of guessing.
import { parse, print, Kind } from "graphql";

const NAME_RE = /^[_A-Za-z][_0-9A-Za-z]*$/;
const ADDRESS_RE = /0x[0-9a-fA-F]{40}(?![0-9a-fA-F])/g;
export const MAX_GOAL_FIELDS = 8;

// Mirrors python/classifier.py graphql_collection_name (graph-node inflection).
export function collectionName(entity) {
  if (!entity) return entity;
  const head = entity[0].toLowerCase() + entity.slice(1);
  const lower = head.toLowerCase();
  if (lower.endsWith("y") && head.length > 1 && !"aeiou".includes(head.at(-2).toLowerCase())) {
    return head.slice(0, -1) + "ies";
  }
  if (lower.endsWith("s") && !/(ss|us|is)$/.test(lower)) return head;
  if (/(s|x|z|ch|sh)$/.test(lower)) return head + "es";
  return head + "s";
}

const TIME_FIELDS = ["timestamp", "blockTimestamp", "createdAtTimestamp", "periodStartUnix", "date", "createdAt", "startTimestamp", "time"];
const METRIC_FIELDS = {
  volume: ["volumeUSD", "totalVolumeUSD", "amountUSD", "dailyVolumeUSD", "cumulativeVolumeUSD", "volume"],
  tvl: ["totalValueLockedUSD", "tvlUSD", "totalLiquidityUSD", "totalValueLockedETH", "liquidity"],
  generic: ["totalValueLockedUSD", "volumeUSD", "totalVolumeUSD", "amountUSD", "txCount", "liquidity", "balance", "amount"],
};

// Ordered from most to least specific. `entities` are tested against entity
// names: strings are exact (case-insensitive), regexes are partial matches.
// `type` is the classifier's canonical type for the same concept.
export const CONCEPTS = [
  { key: "candle", words: /\b(candles?|candlesticks?|ohlcv?|klines?|price bars?)\b/, entities: ["Candle", "Ohlc", "Ohlcv", "Kline", /candle/i, /ohlc/i, /kline/i], fields: ["open", "high", "low", "close", "volume", "volumeUSD", "timestamp", "periodStartUnix", "period", "interval"], order: "time" },
  { key: "hourly", words: /\b(hourly|per hour|hour data|hourly snapshots?)\b/, entities: [/HourData$/i, /Hourly/i, /HourSnapshot/i], type: "hourly_snapshot", fields: ["periodStartUnix", "date", "timestamp", "volumeUSD", "totalValueLockedUSD", "txCount", "open", "high", "low", "close"], order: "time", modifier: true },
  { key: "daily", words: /\b(daily|per day|day data|daily snapshots?)\b/, entities: [/DayData$/i, /Daily/i, /DaySnapshot/i], type: "daily_snapshot", fields: ["date", "timestamp", "volumeUSD", "totalValueLockedUSD", "txCount", "feesUSD", "open", "high", "low", "close"], order: "time", modifier: true },
  { key: "liquidation", words: /\bliquidat\w*/, entities: ["Liquidation", "Liquidate", "LiquidationCall", /liquidat/i], type: "liquidation", fields: ["timestamp", "amountUSD", "profitUSD", "liquidator", "liquidatee", "amount", "blockNumber", "hash"], order: "time", event: true },
  { key: "swap", words: /\b(swaps?|trades?|fills?)\b/, entities: ["Swap", "Trade", "Fill", /swap/i, /trade/i], type: "trade", fields: ["timestamp", "amountUSD", "amount0", "amount1", "amountIn", "amountOut", "sender", "recipient", "origin", "sqrtPriceX96", "tick"], order: "time", event: true },
  { key: "mint", words: /\b(mints?|liquidity adds?|add liquidity)\b/, entities: ["Mint", "ModifyLiquidity", /^mint/i], fields: ["timestamp", "amountUSD", "amount", "amount0", "amount1", "owner", "sender", "origin"], order: "time", event: true },
  { key: "burn", words: /\b(burns?|liquidity removals?|remove liquidity)\b/, entities: ["Burn", "ModifyLiquidity", /^burn/i], fields: ["timestamp", "amountUSD", "amount", "amount0", "amount1", "owner", "origin"], order: "time", event: true },
  { key: "borrow", words: /\bborrows?\b/, entities: ["Borrow", /^borrow/i], fields: ["timestamp", "amountUSD", "amount", "blockNumber", "hash"], order: "time", event: true },
  { key: "repay", words: /\brepay(s|ments?)?\b/, entities: ["Repay", /^repay/i], fields: ["timestamp", "amountUSD", "amount", "blockNumber", "hash"], order: "time", event: true },
  { key: "deposit", words: /\bdeposits?\b/, entities: ["Deposit", /^deposit/i], fields: ["timestamp", "amountUSD", "amount", "blockNumber", "hash"], order: "time", event: true },
  { key: "withdraw", words: /\bwithdraw(als?|s)?\b/, entities: ["Withdraw", "Withdrawal", /^withdraw/i], fields: ["timestamp", "amountUSD", "amount", "blockNumber", "hash"], order: "time", event: true },
  { key: "transfer", words: /\btransfers?\b/, entities: ["Transfer", /transfer/i], fields: ["timestamp", "blockTimestamp", "from", "to", "value", "amount", "blockNumber", "transactionHash"], order: "time", event: true },
  { key: "proposal", words: /\bproposals?\b/, entities: ["Proposal", /proposal/i], type: "proposal", fields: ["description", "state", "status", "startBlock", "endBlock", "createdAt", "forVotes", "againstVotes"], order: "time" },
  { key: "vote", words: /\bvotes?\b/, entities: ["Vote", /vote$/i], fields: ["support", "votes", "weight", "reason", "timestamp", "blockNumber"], order: "time", event: true },
  { key: "delegate", words: /\bdelegates?\b/, entities: ["Delegate", /delegate/i], type: "delegate", fields: ["delegatedVotes", "tokenHoldersRepresentedAmount", "numberVotes"], order: "metric" },
  { key: "domain", words: /\b(domains?|domain names?|ens names?)\b/, entities: ["Domain", /domain/i], type: "domain_name", fields: ["name", "labelName", "createdAt", "expiryDate"], order: "time" },
  { key: "position", words: /\bpositions?\b/, entities: ["Position", /position$/i], type: "position", fields: ["liquidity", "depositedToken0", "depositedToken1", "withdrawnToken0", "withdrawnToken1", "balance", "isCollateral", "timestampOpened"], order: "metric" },
  { key: "vault", words: /\bvaults?\b/, entities: ["Vault", /vault$/i], type: "vault", fields: ["name", "symbol", "totalValueLockedUSD", "pricePerShare", "createdTimestamp"], order: "metric" },
  { key: "market", words: /\b(lending )?markets?\b/, entities: ["Market", /market$/i], fields: ["name", "totalValueLockedUSD", "totalDepositBalanceUSD", "totalBorrowBalanceUSD", "inputTokenPriceUSD", "createdTimestamp"], order: "metric" },
  { key: "pool_manager", words: /\bpool ?managers?\b/, entities: ["PoolManager", /poolmanager/i], fields: ["poolCount", "txCount", "totalVolumeUSD", "totalFeesUSD", "totalValueLockedUSD"], order: "metric" },
  { key: "pool", words: /\b(pools?|pairs?|liquidity pools?|amm pools?)\b/, entities: ["Pool", "Pair", "LiquidityPool", /^pool$/i, /liquiditypool$/i], type: "liquidity_pool", fields: ["totalValueLockedUSD", "volumeUSD", "txCount", "feeTier", "liquidity", "createdAtTimestamp", "token0Price", "token1Price"], relations: ["token0", "token1"], order: "metric" },
  { key: "token", words: /\b(tokens?|erc-?20s?|token symbols?)\b/, entities: ["Token", /^token$/i], type: "token", fields: ["symbol", "name", "volumeUSD", "totalValueLockedUSD", "txCount", "decimals", "totalSupply"], order: "metric" },
  { key: "account", words: /\b(accounts?|users?|holders?|wallets?)\b/, entities: ["Account", "User", "Holder", /account$/i, /^user$/i], type: "account", fields: ["balance", "createdAt", "txCount"], order: "metric" },
];

const FILLER = new Set(["on", "for", "the", "of", "and", "in", "with", "a", "an", "to", "by", "from", "data", "get", "show", "list", "find", "all", "me", "latest", "recent", "newest", "top", "largest", "biggest", "highest", "most", "oldest", "first", "last", "ids", "id", "per", "over", "past", "since", "between", "names", "name", "symbols", "symbol", "volume", "volumes", "tvl", "counters", "counts", "metadata", "amount", "amounts", "hourly", "daily", "day", "hour", "days", "hours", "weeks", "week", "every", "each", "chain", "network", "mainnet"]);

function words(goal) { return goal.toLowerCase().match(/[a-z0-9]+/g) || []; }

export function parseGoal(goal, { now = Math.floor(Date.now() / 1000), isChain = () => false } = {}) {
  const lower = goal.toLowerCase();
  const concepts = CONCEPTS.filter((c) => c.words.test(lower));
  // A modifier (daily/hourly) narrows another concept: "daily pool volume"
  // wants PoolDayData, not every DayData entity.
  const primary = concepts[0] || null;
  const secondary = concepts.filter((c) => c !== primary).map((c) => c.key);
  let ordering = null;
  if (/\b(latest|recent|newest|most recent|last \d*)\b/.test(lower)) ordering = "latest";
  else if (/\b(oldest|earliest)\b/.test(lower)) ordering = "oldest";
  else if (/\b(top|largest|biggest|highest|most|leading|deepest)\b/.test(lower)) ordering = "top";
  const metricHint = /\b(tvl|liquidity|locked)\b/.test(lower) ? "tvl" : /\bvolumes?\b/.test(lower) ? "volume" : null;
  const idsOnly = /\b(ids?|identifiers?|addresses)\b/.test(lower) && !/\b(and|with|plus)\b.*\b(symbols?|names?|volumes?|tvl|prices?)\b/.test(lower);
  const addresses = [];
  for (const m of goal.matchAll(ADDRESS_RE)) {
    const before = words(goal.slice(0, m.index)).filter((w) => !FILLER.has(w) || w === "from" || w === "to");
    addresses.push({ address: m[0].toLowerCase(), context: before.at(-1) || null });
  }
  let timeRange = null;
  const rel = lower.match(/\b(?:last|past|previous)\s+(\d+)?\s*(hours?|h|days?|d|weeks?|w)\b/);
  if (rel) {
    const n = Number(rel[1] || 1);
    const unit = rel[2][0] === "h" ? 3600 : rel[2][0] === "w" ? 604800 : 86400;
    if (n > 0 && n <= 3650) timeRange = { from: now - n * unit, to: null, label: rel[0] };
  } else if (/\b(today|24h)\b/.test(lower)) {
    timeRange = { from: now - 86400, to: null, label: "last 24 hours" };
  }
  const since = lower.match(/\bsince\s+(\d{4}-\d{2}-\d{2})\b/);
  if (since) {
    const t = Date.parse(`${since[1]}T00:00:00Z`);
    if (Number.isFinite(t)) timeRange = { from: Math.floor(t / 1000), to: null, label: `since ${since[1]} UTC` };
  }
  const topN = lower.match(/\b(?:top|first|latest|largest|biggest)\s+(\d{1,3})\b(?!\s*(?:hours?|h|days?|d|weeks?|w)\b)/);
  const conceptWords = new Set(concepts.flatMap((c) => [...lower.matchAll(new RegExp(c.words.source, "g"))].flatMap((m) => words(m[0]))));
  const protocolTerms = words(goal).filter((w) => !FILLER.has(w) && !conceptWords.has(w) && !/^0x/.test(w) && !/^\d+$/.test(w) && !isChain(w));
  const fieldHints = words(goal).filter((w) => /^(symbols?|names?|decimals|prices?|fees?|volumes?|tvl|liquidity|supply|owners?|timestamps?|amounts?|counts?|holders?)$/.test(w))
    .map((w) => w.replace(/s$/, ""));
  return {
    concepts: concepts.map((c) => c.key), primary: primary?.key || null, secondary,
    ordering, metric_hint: metricHint, ids_only: idsOnly, addresses, time_range: timeRange,
    first_from_goal: topN ? Number(topN[1]) : null, protocol_terms: protocolTerms, field_hints: fieldHints,
  };
}

function conceptByKey(key) { return CONCEPTS.find((c) => c.key === key) || null; }

// Score one entity for the parsed intent; 1 exact, 0.8 partial, 0.6 type-only.
export function scoreEntity(entity, intent) {
  const concept = conceptByKey(intent.primary);
  if (!concept || !entity?.name || entity.name.startsWith("_") || !NAME_RE.test(entity.name)) return { score: 0, reason: null };
  const name = entity.name;
  let score = 0, reason = null;
  for (const pattern of concept.entities) {
    if (typeof pattern === "string" && pattern.toLowerCase() === name.toLowerCase()) { score = 1; reason = `entity name equals ${pattern}`; break; }
  }
  if (!score && concept.entities.some((p) => p instanceof RegExp && p.test(name))) { score = 0.8; reason = `entity name matches ${concept.key}`; }
  if (!score && concept.type && entity.type === concept.type) { score = 0.6; reason = `classifier type ${concept.type}`; }
  if (!score) return { score: 0, reason: null };
  // Secondary concepts compose: daily + pool -> PoolDayData.
  for (const key of intent.secondary) {
    const sec = conceptByKey(key);
    const stem = typeof sec?.entities[0] === "string" ? sec.entities[0].toLowerCase() : null;
    if (stem && name.toLowerCase().includes(stem)) { score += 0.15; reason += `; includes ${stem}`; }
  }
  // An unrequested snapshot/derived entity should not beat the base entity.
  if (!concept.modifier && /(DayData|HourData|Daily|Hourly|Snapshot|Minute)/i.test(name)) score -= 0.25;
  if (concept.modifier && !intent.secondary.length && /^(Uniswap|Protocol|Financials|UsageMetrics|Factory)/i.test(name)) score += 0.05;
  return { score: Math.max(0, Math.min(1.2, score)), reason };
}

export function rankEntities(entities, intent) {
  return (entities || [])
    .map((e) => ({ name: e.name, type: e.type ?? null, field_count: e.fields ?? null, ...scoreEntity(e, intent) }))
    .filter((e) => e.score > 0)
    .sort((a, b) => b.score - a.score || (a.name.length - b.name.length) || a.name.localeCompare(b.name));
}

export function parseStarter(source) {
  try {
    const op = parse(source, { noLocation: true, maxTokens: 500 }).definitions[0];
    const root = op.selectionSet.selections.find((s) => s.name?.value !== "_meta");
    if (!root || root.selectionSet == null) return null;
    const arg = (n) => root.arguments?.find((a) => a.name.value === n)?.value?.value ?? null;
    return {
      collection: root.name.value,
      fields: root.selectionSet.selections.filter((f) => f.kind === Kind.FIELD && !f.selectionSet && !f.arguments?.length).map((f) => f.name.value),
      order_by: arg("orderBy"), order_direction: arg("orderDirection"),
    };
  } catch { return null; }
}

// Field names that are relations in common subgraph schemas. Keyless plans
// cannot type-check fields, and selecting an object without a sub-selection is
// invalid GraphQL, so these are dropped from reused starter fields.
const LIKELY_RELATIONS = new Set(["parent", "subdomains", "owner", "registrant", "resolver", "wrappedOwner", "transaction", "transactions", "pool", "pools", "token", "tokens", "token0", "token1", "factory", "market", "account", "user", "position", "positions", "pair", "vault", "asset", "protocol", "events", "swaps", "mints", "burns", "hook", "collection", "inputToken", "outputToken", "rewardTokens", "manager", "poolManager", "bundle", "userLPTransactions"]);

function literal(value) { return typeof value === "number" ? String(value) : JSON.stringify(String(value)); }

function render({ collection, args, fields }) {
  const argText = args.map(([k, v]) => `${k}: ${v}`).join(", ");
  const sel = fields.map((f) => (typeof f === "string" ? `    ${f}` : `    ${f.name} { ${(f.sub || ["id"]).join(" ")} }`)).join("\n");
  const source = `{\n  _meta { block { number timestamp } }\n  ${collection}(${argText}) {\n${sel}\n  }\n}`;
  return print(parse(source, { noLocation: true, maxTokens: 800 }));
}

function chooseOrder(intent, concept, available) {
  const wanted = intent.ordering || (concept?.order === "time" ? "latest" : concept?.order === "metric" ? "top" : null);
  if (!wanted) return null;
  if (wanted === "latest" || wanted === "oldest") {
    const f = TIME_FIELDS.find((x) => available.has(x));
    return f ? { field: f, direction: wanted === "latest" ? "desc" : "asc", requested: Boolean(intent.ordering) } : { missing: wanted, requested: Boolean(intent.ordering) };
  }
  const list = METRIC_FIELDS[intent.metric_hint || "generic"];
  const f = list.find((x) => available.has(x));
  return f ? { field: f, direction: "desc", requested: Boolean(intent.ordering) } : { missing: wanted, requested: Boolean(intent.ordering) };
}

// Keyless plan from stored registry data only.
export function planKeyless({ intent, entity, starter, first, allEntityNames = [] }) {
  const concept = conceptByKey(intent.primary);
  const collection = collectionName(entity.name);
  const unmet = [];
  const rationale = [`collection ${collection} derived from entity ${entity.name} with graph-node pluralisation (not live-checked)`];
  const parsed = starter ? parseStarter(starter) : null;
  const starterMatches = parsed?.collection === collection;
  const relationNames = new Set(allEntityNames.flatMap((n) => [n.toLowerCase(), collectionName(n).toLowerCase()]));
  let fields = ["id"];
  if (!intent.ids_only && starterMatches) {
    const safe = parsed.fields.filter((f) => f !== "id" && !LIKELY_RELATIONS.has(f) && !relationNames.has(f.toLowerCase()) && NAME_RE.test(f));
    fields = ["id", ...safe].slice(0, MAX_GOAL_FIELDS);
    rationale.push("fields reused from the crawled starter for this entity; likely relation fields removed");
  } else if (!intent.ids_only) {
    unmet.push("fields: only id is known keylessly for this entity; validate_schema:true (with your own Studio key) or get_schema adds goal-relevant fields");
  }
  const args = [];
  let order = null;
  if (starterMatches && parsed.order_by && NAME_RE.test(parsed.order_by)) {
    const isTime = TIME_FIELDS.includes(parsed.order_by);
    const wanted = intent.ordering;
    const ok = !wanted || ((wanted === "latest" || wanted === "oldest") ? isTime : !isTime);
    if (ok) {
      const direction = wanted === "oldest" ? "asc" : (parsed.order_direction === "asc" ? "asc" : "desc");
      order = { field: parsed.order_by, direction };
      args.push(["orderBy", parsed.order_by], ["orderDirection", direction]);
      rationale.push(`orderBy ${parsed.order_by} ${direction} reused from the crawled starter`);
    } else unmet.push(`ordering: "${wanted}" needs a field the stored starter does not confirm; use validate_schema:true`);
  } else if (intent.ordering) {
    unmet.push(`ordering: "${intent.ordering}" needs a live-schema field; use validate_schema:true`);
  }
  const where = [], blocking = [];
  for (const a of intent.addresses) {
    if (a.context && concept && concept.words.test(a.context) || (intent.addresses.length === 1 && !a.context)) {
      where.push(["id", literal(a.address)]);
      rationale.push(`where id = ${a.address} (address names the ${concept?.key || "requested"} entity itself)`);
    } else { unmet.push(`address filter for ${a.address}: relation field unknown keylessly; use validate_schema:true`); blocking.push(`address ${a.address}`); }
  }
  if (intent.time_range) { unmet.push(`time range (${intent.time_range.label}): field type unknown keylessly; use validate_schema:true`); blocking.push(`time range ${intent.time_range.label}`); }
  if (concept?.key === "candle") unmet.push("candle/OHLCV entities may be timeseries aggregations that require an interval argument; not detectable without the live schema");
  if (where.length) args.push(["where", `{ ${where.map(([k, v]) => `${k}: ${v}`).join(", ")} }`]);
  args.push(["first", String(first)]);
  return { query: render({ collection, args, fields }), collection, fields, order, where: Object.fromEntries(where.map(([k, v]) => [k, JSON.parse(v)])), unmet, blocking_unmet: blocking, rationale, field_source: starterMatches && !intent.ids_only ? "crawled_starter_fields" : "id_only" };
}

// One aliased, read-only introspection request scoped to the selected entity.
export function schemaProbeQuery(entityName) {
  if (!NAME_RE.test(entityName)) throw new Error("invalid entity name");
  return `{
  q: __type(name: "Query") { fields { name args { name defaultValue type { ...T } } type { ...T } } }
  e: __type(name: "${entityName}") { name fields { name type { ...T } } }
  o: __type(name: "${entityName}_orderBy") { enumValues { name } }
  f: __type(name: "${entityName}_filter") { inputFields { name type { ...T } } }
  i: __type(name: "Aggregation_interval") { enumValues { name } }
  t: __type(name: "Token") { name fields { name type { ...T } } }
  m: _meta { block { number timestamp } hasIndexingErrors deployment }
}
fragment T on __Type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }`;
}

function unwrap(t) {
  let list = false, cur = t;
  while (cur && (cur.kind === "NON_NULL" || cur.kind === "LIST")) { if (cur.kind === "LIST") list = true; cur = cur.ofType; }
  return { kind: cur?.kind ?? null, name: cur?.name ?? null, list };
}

// Plan using the live probe; every emitted name is checked against it.
export function planWithSchema({ intent, entity, probe, first }) {
  const concept = conceptByKey(intent.primary);
  const errors = [], unmet = [], rationale = [];
  const qFields = probe?.q?.fields, eFields = probe?.e?.fields;
  if (!Array.isArray(qFields) || !Array.isArray(eFields)) return { errors: ["live schema probe did not return the Query and entity types"] };
  const collectionField = qFields.find((f) => { const u = unwrap(f.type); return u.list && u.name === entity.name; });
  if (!collectionField) return { errors: [`no Query collection returns [${entity.name}]`] };
  const collection = collectionField.name;
  rationale.push(`collection ${collection} confirmed by live introspection`);
  const leaf = new Map(), objects = new Map();
  for (const f of eFields) {
    const u = unwrap(f.type);
    if (u.kind === "SCALAR" || u.kind === "ENUM") leaf.set(f.name, u);
    else if ((u.kind === "OBJECT" || u.kind === "INTERFACE") && !u.list) objects.set(f.name, u);
  }
  const fields = ["id"];
  if (!leaf.has("id")) errors.push("entity has no id field");
  if (!intent.ids_only) {
    const want = [...(concept?.fields || []), ...[...leaf.keys()].filter((n) => intent.field_hints.some((h) => n.toLowerCase().includes(h)))];
    // Reserve room for single relations (pool token0/token1) so token symbols
    // can be shown and checked for spam.
    const rels = (concept?.relations || []).filter((r) => objects.has(r));
    for (const n of want) if (leaf.has(n) && !fields.includes(n) && fields.length < MAX_GOAL_FIELDS - rels.length) fields.push(n);
    const tokenLeaves = new Set((probe?.t?.fields || []).filter((f) => ["SCALAR", "ENUM"].includes(unwrap(f.type).kind)).map((f) => f.name));
    for (const r of rels) {
      if (fields.length >= MAX_GOAL_FIELDS) break;
      const sub = objects.get(r)?.name === "Token" ? ["id", ...["symbol", "name"].filter((n) => tokenLeaves.has(n))] : ["id"];
      fields.push({ name: r, sub });
    }
    for (const n of leaf.keys()) if (fields.length < 4 && !fields.includes(n)) fields.push(n);
    rationale.push("fields chosen from live entity fields relevant to the goal (scalars; single relations as { id })");
  }
  const orderEnum = new Set((probe?.o?.enumValues || []).map((v) => v.name));
  const filterFields = new Map((probe?.f?.inputFields || []).map((f) => [f.name, unwrap(f.type)]));
  const args = [];
  const requiredArgs = (collectionField.args || []).filter((a) => a.type?.kind === "NON_NULL" && a.defaultValue == null);
  for (const a of requiredArgs) {
    if (a.name === "interval") {
      const values = (probe?.i?.enumValues || []).map((v) => v.name);
      const pick = intent.concepts.includes("daily") && values.includes("day") ? "day" : values.includes("hour") ? "hour" : values[0];
      if (pick) { args.push(["interval", pick]); rationale.push(`required aggregation interval: ${pick}`); }
      else errors.push("required interval argument has no known values");
    } else errors.push(`required argument ${a.name} cannot be supplied automatically`);
  }
  const order = chooseOrder(intent, concept, orderEnum);
  if (order?.field) { args.push(["orderBy", order.field], ["orderDirection", order.direction]); rationale.push(`orderBy ${order.field} ${order.direction}`); }
  else if (order?.missing && order.requested) unmet.push(`ordering: no ${order.missing === "top" ? "metric" : "time"} field in ${entity.name}_orderBy`);
  const where = [], blocking = [];
  const RELATION_BY_CONTEXT = { pool: ["pool", "pair"], pair: ["pair", "pool"], token: ["token", "token0", "token1", "inputToken", "asset"], wallet: ["owner", "account", "user", "origin", "sender", "from"], user: ["user", "account", "owner", "origin", "sender"], account: ["account", "user", "owner"], owner: ["owner", "registrant", "account", "user"], owned: ["owner", "registrant", "account", "user"], owns: ["owner", "registrant", "account", "user"], held: ["owner", "account", "user"], holder: ["owner", "account", "user"], holding: ["owner", "account", "user"], registrant: ["registrant", "owner"], registered: ["registrant", "owner"], sender: ["sender", "from", "origin"], from: ["from", "sender"], to: ["to", "recipient"], recipient: ["recipient", "to"], market: ["market"], vault: ["vault"] };
  for (const a of intent.addresses) {
    const self = a.context ? concept?.words.test(a.context) : intent.addresses.length === 1;
    const candidates = self ? ["id"] : (RELATION_BY_CONTEXT[a.context] || []);
    const field = candidates.find((c) => filterFields.has(c));
    const pair = /^token[01]$/.test(field || "") && filterFields.has("token0") && filterFields.has("token1");
    if (pair && filterFields.has("or")) {
      where.push(["or", `[{ token0: ${literal(a.address)} }, { token1: ${literal(a.address)} }]`, [{ token0: a.address }, { token1: a.address }]]);
      rationale.push(`where token0 = ${a.address} OR token1 = ${a.address}`);
    } else if (field) {
      where.push([field, literal(a.address)]); rationale.push(`where ${field} = ${a.address}`);
      if (pair) unmet.push(`address ${a.address} filtered on ${field} only; this schema has no "or" filter, so matches on the other token side are not included`);
    } else { unmet.push(`address filter for ${a.address}: no matching filter field for context "${a.context ?? "none"}"`); blocking.push(`address ${a.address}`); }
  }
  if (intent.time_range) {
    const tf = TIME_FIELDS.find((f) => filterFields.has(`${f}_gte`));
    const type = tf ? filterFields.get(`${tf}_gte`)?.name : null;
    if (tf && (type === "Int" || type === "BigInt" || type === "Int8")) {
      where.push([`${tf}_gte`, type === "Int" ? literal(intent.time_range.from) : literal(String(intent.time_range.from))]);
      rationale.push(`where ${tf}_gte = ${intent.time_range.from} (${intent.time_range.label}, unix seconds)`);
    } else { unmet.push(`time range (${intent.time_range.label}): no Int/BigInt seconds filter confirmed`); blocking.push(`time range ${intent.time_range.label}`); }
  }
  for (const [k] of where) if (!filterFields.has(k)) errors.push(`filter ${k} not in ${entity.name}_filter`);
  if (where.length) args.push(["where", `{ ${where.map(([k, v]) => `${k}: ${v}`).join(", ")} }`]);
  args.push(["first", String(first)]);
  for (const f of fields) if (!(typeof f === "string" ? leaf.has(f) : objects.has(f.name))) errors.push(`field ${typeof f === "string" ? f : f.name} not on ${entity.name}`);
  if (order?.field && !orderEnum.has(order.field)) errors.push(`orderBy ${order.field} not in ${entity.name}_orderBy`);
  if (errors.length) return { errors, unmet, rationale };
  return { query: render({ collection, args, fields }), collection, fields: fields.map((f) => (typeof f === "string" ? f : `${f.name} { ${(f.sub || ["id"]).join(" ")} }`)), order: order?.field ? order : null, where: Object.fromEntries(where.map(([k, v, j]) => [k, j ?? JSON.parse(v)])), unmet, blocking_unmet: blocking, rationale, errors: [], field_source: "live_introspection" };
}

// Serving/freshness signal from the probe's `_meta` (no extra request).
export const STALE_INDEXING_SECONDS = 2 * 3600;
export function probeHealth(meta, now = Math.floor(Date.now() / 1000)) {
  const ts = meta?.block?.timestamp;
  if (!Number.isSafeInteger(meta?.block?.number)) return { status: "unknown", indexed_block_number: null, indexed_block_timestamp: null, lag_seconds: null, has_indexing_errors: null };
  const lag = Number.isSafeInteger(ts) && ts > 0 ? Math.max(0, now - ts) : null;
  return {
    status: lag !== null && lag > STALE_INDEXING_SECONDS ? "stale" : meta.hasIndexingErrors === true ? "serving_with_indexing_errors" : "serving",
    indexed_block_number: meta.block.number, indexed_block_timestamp: Number.isSafeInteger(ts) ? ts : null, lag_seconds: lag,
    has_indexing_errors: typeof meta.hasIndexingErrors === "boolean" ? meta.hasIndexingErrors : null,
  };
}
