#!/usr/bin/env node
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

const DEFAULT_API_BASE_URL = "https://api.coinpilot.bot";
const ALLOWED_API_BASE_URLS = new Set(
  ["coinpilot.bot", "coinpilot.com"].flatMap((domain) =>
    ["", "dev-", "staging-"].map((prefix) => `https://${prefix}api.${domain}`),
  ),
);
const HYPERLIQUID_API_ENDPOINT = "https://api.hyperliquid.xyz";
const RATE_LIMIT_MS = 1000;

const getDefaultWalletsPath = () => {
  const homeDir = os.homedir();
  if (!homeDir) {
    throw new Error("Unable to resolve the user home directory");
  }
  return path.join(homeDir, ".coinpilot", "coinpilot.json");
};
const normalizeApiBaseUrl = (value) => {
  let url;
  try {
    url = new URL(value);
  } catch {
    throw new Error("coinpilot.json apiBaseUrl must be a valid URL");
  }
  if (url.protocol !== "https:") {
    throw new Error("coinpilot.json apiBaseUrl must use https");
  }
  if (url.username || url.password || url.search || url.hash) {
    throw new Error(
      "coinpilot.json apiBaseUrl must not include auth, query params, or fragments",
    );
  }
  if (url.pathname !== "/" && url.pathname !== "") {
    throw new Error("coinpilot.json apiBaseUrl must not include a path");
  }
  return url.origin;
};
const validateApiBaseUrl = (value) => {
  if (value === undefined) return DEFAULT_API_BASE_URL;
  const normalized = normalizeApiBaseUrl(value);
  if (!ALLOWED_API_BASE_URLS.has(normalized)) {
    throw new Error(
      `coinpilot.json apiBaseUrl must be one of: ${[...ALLOWED_API_BASE_URLS].join(", ")}`,
    );
  }
  return normalized;
};
const getApiBaseUrl = (wallets) => validateApiBaseUrl(wallets.apiBaseUrl);
const DEFAULT_WALLETS_PATH = getDefaultWalletsPath();

let lastRequestAt = 0;
let coinpilotQueue = Promise.resolve();
let loadedSecrets = [];

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const throttle = async () => {
  const now = Date.now();
  const wait = RATE_LIMIT_MS - (now - lastRequestAt);
  if (wait > 0) await sleep(wait);
  lastRequestAt = Date.now();
};

const withCoinpilotLock = async (fn) => {
  const start = coinpilotQueue;
  let release;
  coinpilotQueue = new Promise((resolve) => {
    release = resolve;
  });
  return start.then(fn).finally(release);
};

const readJson = async (filePath) => {
  const raw = await fs.readFile(filePath, "utf8");
  return JSON.parse(raw);
};

const validateWallets = (data) => {
  if (!data || typeof data !== "object")
    throw new Error("coinpilot.json must be an object");
  if (!data.apiKey || typeof data.apiKey !== "string")
    throw new Error("Missing apiKey");
  if (!data.userId || typeof data.userId !== "string")
    throw new Error("Missing userId");
  data.apiBaseUrl = validateApiBaseUrl(data.apiBaseUrl);
  if (!Array.isArray(data.wallets) || data.wallets.length !== 10) {
    throw new Error(
      "wallets must be an array with exactly 10 entries (1 primary + 9 subwallets)",
    );
  }

  const primaryWallets = data.wallets.filter((wallet) => wallet.isPrimary);
  if (primaryWallets.length !== 1) {
    throw new Error("Exactly one wallet must have isPrimary: true");
  }

  const primary = primaryWallets[0];
  if (primary.index !== 0) {
    throw new Error("Primary wallet must have index 0");
  }

  const seenIndexes = new Set();
  for (const wallet of data.wallets) {
    if (typeof wallet.index !== "number")
      throw new Error("wallet.index must be a number");
    if (!wallet.address || typeof wallet.address !== "string") {
      throw new Error("wallet.address must be a string");
    }
    if (!wallet.privateKey || typeof wallet.privateKey !== "string") {
      throw new Error("wallet.privateKey must be a string");
    }
    if (typeof wallet.isPrimary !== "boolean") {
      throw new Error("wallet.isPrimary must be a boolean");
    }
    if (seenIndexes.has(wallet.index)) {
      throw new Error(
        `wallet.index values must be unique (duplicate: ${wallet.index})`,
      );
    }
    seenIndexes.add(wallet.index);
    if (wallet.isPrimary) {
      if (wallet.index !== 0) {
        throw new Error("Primary wallet must have index 0");
      }
      continue;
    }
    if (wallet.index < 1 || wallet.index > 9) {
      throw new Error("Subwallet indexes must be between 1 and 9");
    }
  }
  return data;
};

const getPrimaryWallet = (wallets) =>
  wallets.wallets.find((wallet) => wallet.isPrimary);

const findWalletByAddress = (wallets, address) =>
  wallets.wallets.find(
    (wallet) => wallet.address.toLowerCase() === address.toLowerCase(),
  );

const findWalletByIndex = (wallets, index) =>
  wallets.wallets.find((wallet) => wallet.index === index);

const ensureFollowerWallet = (wallet) => {
  if (wallet.isPrimary) {
    throw new Error(
      "Follower wallet must be a subwallet, not the primary wallet",
    );
  }
  return wallet;
};

const GLOBAL_OPTION_KEYS = new Set(["help", "h"]);
const COMMAND_OPTION_KEYS = {
  validate: new Set(["online"]),
  "lead-metrics": new Set(["wallet"]),
  "lead-periods": new Set(["wallet"]),
  "lead-data": new Set([
    "period",
    "sort-by",
    "sort-order",
    "type",
    "search",
    "watchlist",
    "page",
    "limit",
  ]),
  "lead-categories": new Set(["limit"]),
  "lead-category": new Set([
    "category",
    "period",
    "sort-by",
    "sort-order",
    "search",
    "page",
    "limit",
  ]),
  "prepare-wallet": new Set(),
  start: new Set([
    "lead-wallet",
    "lead-wallet-name",
    "allocation",
    "stop-loss-percent",
    "take-profit-percent",
    "inverse-copy",
    "force-copy-existing",
    "max-leverage",
    "max-margin-percentage",
    "follower-index",
    "follower-wallet",
    "use-prepare-wallet",
  ]),
  stop: new Set([
    "subscription-id",
    "follower-index",
    "follower-wallet",
    "use-prepare-wallet",
  ]),
  "renew-api-wallet": new Set([
    "subscription-id",
    "follower-index",
    "follower-wallet",
    "use-prepare-wallet",
  ]),
  "list-subscriptions": new Set(),
  "update-config": new Set(["subscription-id", "payload"]),
  "close-all": new Set(["subscription-id"]),
  close: new Set(["subscription-id", "coin", "percentage"]),
  activities: new Set(["subscription-id", "cursor", "size"]),
  history: new Set(),
  "hl-account": new Set(["wallet"]),
  "hl-portfolio": new Set(["wallet"]),
};

const parseArgs = (argv) => {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }
    const key = token.replace(/^--/, "");
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
};

const validateArgs = (command, args) => {
  const allowedKeys = COMMAND_OPTION_KEYS[command];
  if (!allowedKeys) {
    throw new Error(`Unknown command: ${command}`);
  }

  const optionKeys = Object.keys(args).filter((key) => key !== "_");
  const unknownKeys = optionKeys.filter(
    (key) => !GLOBAL_OPTION_KEYS.has(key) && !allowedKeys.has(key),
  );
  if (unknownKeys.length > 0) {
    throw new Error(`Unknown option: --${unknownKeys[0]}`);
  }

  if (args._.length > 1) {
    throw new Error(`Unexpected positional argument: ${args._[1]}`);
  }
};

const toNumber = (value, field) => {
  if (value === undefined) return undefined;
  const parsed = Number(value);
  if (Number.isNaN(parsed)) throw new Error(`${field} must be a number`);
  return parsed;
};

const toBoolean = (value) => {
  if (value === undefined) return undefined;
  if (value === true) return true;
  if (value === "true") return true;
  if (value === "false") return false;
  return undefined;
};

const getLoadedSecrets = (wallets) => {
  const values = [
    wallets.apiKey,
    ...wallets.wallets.map((wallet) => wallet.privateKey),
  ];
  return values.filter(
    (value) => typeof value === "string" && value.length > 0,
  );
};

const isWalletAddress = (value) =>
  typeof value === "string" && /^0x[a-fA-F0-9]{40}$/.test(value);

const extractLeadWallet = (value) => {
  if (isWalletAddress(value)) return value.toLowerCase();
  if (Array.isArray(value)) {
    for (const entry of value) {
      const wallet = extractLeadWallet(entry);
      if (wallet) return wallet;
    }
    return undefined;
  }
  if (!value || typeof value !== "object") return undefined;

  for (const key of ["wallet", "address", "leadWallet"]) {
    const candidate = value[key];
    if (isWalletAddress(candidate)) return candidate.toLowerCase();
  }

  for (const entry of Object.values(value)) {
    const wallet = extractLeadWallet(entry);
    if (wallet) return wallet;
  }
  return undefined;
};

const redactSecretsInString = (value) => {
  let redacted = value;
  for (const secret of [...loadedSecrets].sort((a, b) => b.length - a.length)) {
    redacted = redacted.split(secret).join("[REDACTED]");
  }
  return redacted;
};

const sanitizeOutput = (value) => {
  if (typeof value === "string") return redactSecretsInString(value);
  if (Array.isArray(value)) return value.map(sanitizeOutput);
  if (!value || typeof value !== "object") return value;

  const sanitized = {};
  for (const [key, entry] of Object.entries(value)) {
    if (
      key === "privateKey" ||
      key === "primaryWalletPrivateKey" ||
      key === "followerWalletPrivateKey" ||
      key === "apiKey" ||
      key === "x-api-key" ||
      key === "x-wallet-private-key"
    ) {
      sanitized[key] = "[REDACTED]";
      continue;
    }
    sanitized[key] = sanitizeOutput(entry);
  }
  return sanitized;
};

const formatOutput = (data) => {
  console.log(JSON.stringify(sanitizeOutput(data), null, 2));
};

const requestCoinpilot = async (
  method,
  route,
  wallets,
  body,
  query,
  extraHeaders,
) => {
  return withCoinpilotLock(async () => {
    await throttle();
    const primary = getPrimaryWallet(wallets);
    const baseUrl = getApiBaseUrl(wallets);
    const url = new URL(route, baseUrl);
    if (query) {
      for (const [key, value] of Object.entries(query)) {
        if (value === undefined || value === "") continue;
        url.searchParams.set(key, String(value));
      }
    }
    console.log(`[coinpilot] ${method} ${url.toString()}`);
    const headers = {
      "Content-Type": "application/json",
      "x-api-key": wallets.apiKey,
      "x-wallet-private-key": primary.privateKey,
      "x-user-id": wallets.userId,
      ...extraHeaders,
    };
    const res = await fetch(url.toString(), {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
    const contentType = res.headers.get("content-type") || "";
    const payload = contentType.includes("application/json")
      ? await res.json()
      : await res.text();
    if (!res.ok) {
      const message =
        typeof payload === "string"
          ? redactSecretsInString(payload)
          : JSON.stringify(sanitizeOutput(payload));
      throw new Error(
        `Coinpilot ${method} ${route} failed (${res.status}): ${message}`,
      );
    }
    if (payload && typeof payload === "object" && "success" in payload) {
      if (payload.success === false) {
        const message = payload.error
          ? redactSecretsInString(String(payload.error))
          : JSON.stringify(sanitizeOutput(payload));
        throw new Error(`Coinpilot ${method} ${route} failed: ${message}`);
      }
      if ("data" in payload) {
        const keys = Object.keys(payload);
        const hasOnlyData =
          keys.length === 2 &&
          keys.includes("success") &&
          keys.includes("data");
        if (hasOnlyData) return payload.data;
      }
    }
    // console.log(`[coinpilot] ${method} ${route} response:`, payload);
    return payload;
  });
};

const requestHyperliquid = async (payload) => {
  const url = new URL("/info", HYPERLIQUID_API_ENDPOINT);
  const res = await fetch(url.toString(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(
      `Hyperliquid request failed (${res.status}): ${JSON.stringify(data)}`,
    );
  }
  return data;
};

const resolveFollowerWallet = async (wallets, args, primaryAddress) => {
  if (args["follower-index"] !== undefined) {
    const index = Number(args["follower-index"]);
    if (Number.isNaN(index))
      throw new Error("--follower-index must be a number");
    const follower = findWalletByIndex(wallets, index);
    if (!follower) throw new Error(`No wallet found at index ${index}`);
    return ensureFollowerWallet(follower);
  }

  if (args["follower-wallet"]) {
    const follower = findWalletByAddress(wallets, args["follower-wallet"]);
    if (!follower)
      throw new Error(`No wallet found for ${args["follower-wallet"]}`);
    return ensureFollowerWallet(follower);
  }

  if (args["use-prepare-wallet"]) {
    const prepared = await requestCoinpilot(
      "GET",
      `/experimental/${primaryAddress}/subscriptions/prepare-wallet`,
      wallets,
    );
    const follower = findWalletByAddress(wallets, prepared.address);
    if (!follower) {
      throw new Error(
        `Prepared wallet ${prepared.address} not found in coinpilot.json`,
      );
    }
    return ensureFollowerWallet(follower);
  }

  throw new Error(
    "Specify --follower-index, --follower-wallet, or --use-prepare-wallet so the private key is loaded from coinpilot.json in memory",
  );
};

const printHelp = () => {
  console.log(`
Usage: node scripts/coinpilot_cli.mjs <command> [options]

Commands:
  validate                     Validate coinpilot.json (use --online for readonly auth checks)
  lead-metrics                 Get metrics for a lead wallet
  lead-periods                 Get period metrics for a lead wallet
  lead-data                    Query lead wallet performance data
  lead-categories              List lead categories
  lead-category                Get category rankings
  prepare-wallet               Get an available follower wallet
  start                        Start copy trading (experimental)
  stop                         Stop copy trading (experimental)
  renew-api-wallet             Renew API wallet for a subscription (experimental)
  list-subscriptions           List subscriptions for the user
  update-config                Update subscription config/leverages
  close-all                    Close all positions for a subscription
  close                        Close a single position for a subscription
  activities                   Get subscription activity feed
  history                      Get subscription history
  hl-account                   Hyperliquid clearinghouseState for a wallet
  hl-portfolio                 Hyperliquid portfolio for a wallet

Common options:
  coinpilot.json location is fixed to: ${DEFAULT_WALLETS_PATH}

Follower wallet selection:
  --follower-index <n>         Load follower wallet by subwallet index from coinpilot.json
  --follower-wallet <address>  Load follower wallet by address from coinpilot.json
  --use-prepare-wallet         Ask Coinpilot for an available follower wallet, then match it in coinpilot.json

Examples:
  node scripts/coinpilot_cli.mjs validate --online
  node scripts/coinpilot_cli.mjs lead-metrics --wallet 0xabc...
  node scripts/coinpilot_cli.mjs start --lead-wallet 0xlead... --allocation 200 --follower-index 1
    (allocation must be >= 5 USDC)
  node scripts/coinpilot_cli.mjs stop --subscription-id 123 --follower-index 1
  node scripts/coinpilot_cli.mjs renew-api-wallet --subscription-id 123 --follower-index 1
`);
};

const main = async () => {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (!command || args.help || args.h) {
    printHelp();
    return;
  }
  validateArgs(command, args);

  const walletsPath = DEFAULT_WALLETS_PATH;
  // console.log(`[coinpilot] wallets path: ${walletsPath}`);
  const wallets = validateWallets(await readJson(walletsPath));
  loadedSecrets = getLoadedSecrets(wallets);

  const primary = getPrimaryWallet(wallets);
  const primaryAddress = primary.address;

  if (command === "validate") {
    if (!args.online) {
      console.log("coinpilot.json format looks valid.");
      return;
    }
    const me = await requestCoinpilot(
      "GET",
      `/experimental/${primaryAddress}/me`,
      wallets,
    );
    const apiUserId = me?.userId ?? me?.data?.userId;
    if (apiUserId !== wallets.userId) {
      throw new Error(
        `UserId mismatch: coinpilot.json has ${wallets.userId}, API returned ${apiUserId}`,
      );
    }

    const subscriptions = await requestCoinpilot(
      "GET",
      `/users/${wallets.userId}/subscriptions`,
      wallets,
    );
    const leadDiscovery = await requestCoinpilot(
      "GET",
      "/lead-wallets/metrics/categories",
      wallets,
      undefined,
      { limit: 1 },
    );
    const discoveredLeadWallet = extractLeadWallet(leadDiscovery);
    if (!discoveredLeadWallet) {
      throw new Error(
        "Unable to extract a lead wallet from the lead discovery response during validation",
      );
    }
    const hlAccount = await requestHyperliquid({
      type: "clearinghouseState",
      user: primaryAddress,
    });

    formatOutput({
      ok: true,
      validation: {
        me: { userId: apiUserId },
        subscriptions: {
          count: Array.isArray(subscriptions)
            ? subscriptions.length
            : undefined,
        },
        leadDiscovery: {
          leadWallet: discoveredLeadWallet,
        },
        hlAccount: {
          wallet: primaryAddress,
          found: Boolean(hlAccount),
        },
      },
    });
    return;
  }

  if (command === "lead-metrics") {
    if (!args.wallet) throw new Error("--wallet is required");
    const data = await requestCoinpilot(
      "GET",
      `/lead-wallets/metrics/wallets/${args.wallet}`,
      wallets,
    );
    formatOutput(data);
    return;
  }

  if (command === "lead-periods") {
    if (!args.wallet) throw new Error("--wallet is required");
    const data = await requestCoinpilot(
      "GET",
      `/lead-wallets/metrics/wallets/${args.wallet}/periods`,
      wallets,
    );
    formatOutput(data);
    return;
  }

  if (command === "lead-data") {
    const data = await requestCoinpilot(
      "GET",
      "/lead-wallets/data",
      wallets,
      undefined,
      {
        period: args.period,
        sortBy: args["sort-by"],
        sortOrder: args["sort-order"],
        type: args.type,
        search: args.search,
        watchlist: args.watchlist,
        page: args.page,
        limit: args.limit,
      },
    );
    formatOutput(data);
    return;
  }

  if (command === "lead-categories") {
    const data = await requestCoinpilot(
      "GET",
      "/lead-wallets/metrics/categories",
      wallets,
      undefined,
      { limit: args.limit },
    );
    formatOutput(data);
    return;
  }

  if (command === "lead-category") {
    if (!args.category) throw new Error("--category is required");
    const data = await requestCoinpilot(
      "GET",
      `/lead-wallets/metrics/categories/${args.category}`,
      wallets,
      undefined,
      {
        period: args.period,
        sortBy: args["sort-by"],
        sortOrder: args["sort-order"],
        search: args.search,
        page: args.page,
        limit: args.limit,
      },
    );
    formatOutput(data);
    return;
  }

  if (command === "prepare-wallet") {
    const data = await requestCoinpilot(
      "GET",
      `/experimental/${primaryAddress}/subscriptions/prepare-wallet`,
      wallets,
    );
    formatOutput(data);
    return;
  }

  if (command === "start") {
    if (!args["lead-wallet"]) throw new Error("--lead-wallet is required");
    const allocation = toNumber(args.allocation, "allocation");
    if (!allocation) throw new Error("--allocation is required");
    if (allocation < 5) throw new Error("--allocation must be >= 5 USDC");

    const follower = await resolveFollowerWallet(wallets, args, primaryAddress);

    const config = {
      allocation,
      stopLossPercent: toNumber(args["stop-loss-percent"], "stop-loss-percent"),
      takeProfitPercent: toNumber(
        args["take-profit-percent"],
        "take-profit-percent",
      ),
      inverseCopy: toBoolean(args["inverse-copy"]),
      forceCopyExisting: toBoolean(args["force-copy-existing"]),
      maxLeverage: toNumber(args["max-leverage"], "max-leverage"),
      maxMarginPercentage: toNumber(
        args["max-margin-percentage"],
        "max-margin-percentage",
      ),
    };

    Object.keys(config).forEach((key) => {
      if (config[key] === undefined) delete config[key];
    });

    const body = {
      primaryWalletPrivateKey: primary.privateKey,
      followerWalletPrivateKey: follower.privateKey,
      subscription: {
        leadWallet: args["lead-wallet"],
        leadWalletName: args["lead-wallet-name"],
        followerWallet: follower.address,
        config,
      },
    };

    const data = await requestCoinpilot(
      "POST",
      `/experimental/${primaryAddress}/subscriptions/start`,
      wallets,
      body,
    );
    formatOutput(data);
    return;
  }

  if (command === "stop") {
    if (!args["subscription-id"])
      throw new Error("--subscription-id is required");
    const follower = await resolveFollowerWallet(wallets, args, primaryAddress);
    const body = {
      followerWalletPrivateKey: follower.privateKey,
      subscriptionId: args["subscription-id"],
    };
    const data = await requestCoinpilot(
      "POST",
      `/experimental/${primaryAddress}/subscriptions/stop`,
      wallets,
      body,
    );
    formatOutput(data);
    return;
  }

  if (command === "renew-api-wallet") {
    if (!args["subscription-id"])
      throw new Error("--subscription-id is required");
    const follower = await resolveFollowerWallet(wallets, args, primaryAddress);
    const body = {
      followerWalletPrivateKey: follower.privateKey,
    };
    const data = await requestCoinpilot(
      "POST",
      `/experimental/${primaryAddress}/subscriptions/${args["subscription-id"]}/renew-api-wallet`,
      wallets,
      body,
    );
    formatOutput(data);
    return;
  }

  if (command === "list-subscriptions") {
    const data = await requestCoinpilot(
      "GET",
      `/users/${wallets.userId}/subscriptions`,
      wallets,
    );
    formatOutput(data);
    return;
  }

  if (command === "update-config") {
    if (!args["subscription-id"])
      throw new Error("--subscription-id is required");
    if (!args.payload) throw new Error("--payload <path> is required");
    const payload = await readJson(args.payload);
    if (!payload.config || !payload.leverages) {
      throw new Error("payload must include config and leverages");
    }
    const data = await requestCoinpilot(
      "PATCH",
      `/users/${wallets.userId}/subscriptions/${args["subscription-id"]}`,
      wallets,
      payload,
    );
    formatOutput(data);
    return;
  }

  if (command === "close-all") {
    if (!args["subscription-id"])
      throw new Error("--subscription-id is required");
    const data = await requestCoinpilot(
      "POST",
      `/users/${wallets.userId}/subscriptions/${args["subscription-id"]}/close-all`,
      wallets,
      {},
    );
    formatOutput(data);
    return;
  }

  if (command === "close") {
    if (!args["subscription-id"])
      throw new Error("--subscription-id is required");
    if (!args.coin) throw new Error("--coin is required");
    const percentage = toNumber(args.percentage, "percentage") ?? 1;
    if (percentage < 0 || percentage > 1) {
      throw new Error("--percentage must be between 0 and 1");
    }
    const body = {
      coin: args.coin,
      percentage,
    };
    const data = await requestCoinpilot(
      "POST",
      `/users/${wallets.userId}/subscriptions/${args["subscription-id"]}/close`,
      wallets,
      body,
    );
    formatOutput(data);
    return;
  }

  if (command === "activities") {
    if (!args["subscription-id"])
      throw new Error("--subscription-id is required");
    const data = await requestCoinpilot(
      "GET",
      `/users/${wallets.userId}/subscriptions/${args["subscription-id"]}/activities`,
      wallets,
      undefined,
      { cursor: args.cursor, size: args.size },
    );
    formatOutput(data);
    return;
  }

  if (command === "history") {
    const data = await requestCoinpilot(
      "GET",
      `/users/${wallets.userId}/subscriptions/history`,
      wallets,
    );
    formatOutput(data);
    return;
  }

  if (command === "hl-account") {
    if (!args.wallet) throw new Error("--wallet is required");
    const data = await requestHyperliquid({
      type: "clearinghouseState",
      user: args.wallet,
    });
    formatOutput(data);
    return;
  }

  if (command === "hl-portfolio") {
    if (!args.wallet) throw new Error("--wallet is required");
    const data = await requestHyperliquid({
      type: "portfolio",
      user: args.wallet,
    });
    formatOutput(data);
    return;
  }

  throw new Error(`Unknown command: ${command}`);
};

main().catch((err) => {
  const message =
    err instanceof Error
      ? err.message
      : typeof err === "string"
        ? err
        : String(err);
  console.error(redactSecretsInString(message));
  process.exitCode = 1;
});
