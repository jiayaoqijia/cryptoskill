import { apiGet, apiPost, assertOk } from "./lib/api.js";
import { ErrorCode, fail, run, success } from "./lib/output.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function filterFiat(balances: any[]): any[] {
    return balances.filter((b: any) => parseFloat(b.amount?.amount ?? "0") > 0);
}

function filterCrypto(wallets: any[]): any[] {
    return wallets.filter((w: any) => {
        const amt = w.available?.amount ?? w.balance?.amount ?? "0";
        return parseFloat(amt) > 0;
    });
}

function parsePortfolioProducts(res: any): any[] | null {
    if (res.data?.ok !== true) return null;
    return (res.data.products as any[] ?? []).filter(
        (p: any) => parseFloat(p.price_native?.amount ?? "0") > 0,
    );
}

function parseCurrencyAllocation(res: any): Record<string, string> | null {
    if (res.data?.ok !== true) return null;
    const allocation: Record<string, string> = {};
    for (const [key, val] of Object.entries(res.data)) {
        if (key === "ok") continue;
        const entry = val as any;
        if (entry?.amount && parseFloat(entry.amount) > 0) {
            allocation[key] = entry.amount;
        }
    }
    return Object.keys(allocation).length > 0 ? allocation : null;
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function balances(scope: string) {
    const validScopes = ["fiat", "crypto", "all"];
    if (!validScopes.includes(scope)) {
        fail(ErrorCode.INVALID_ARGS, `Invalid scope "${scope}". Use: fiat | crypto | all`);
    }

    const includeFiat = scope !== "crypto";
    const includeCrypto = scope !== "fiat";
    const result: Record<string, any> = {};

    if (includeFiat) {
        const res = await apiGet("/v1/fiat-account");
        assertOk(res, "Fiat balance fetch");
        result.fiat = filterFiat(res.data.account.balances);
    }

    if (includeCrypto) {
        const [cryptoRes, portfolioRes] = await Promise.all([
            apiGet("/v1/crypto-account"),
            apiGet("/v1/portfolio"),
        ]);
        assertOk(cryptoRes, "Crypto balance fetch");
        result.crypto = {
            note: "available for trading",
            wallets: filterCrypto(cryptoRes.data.account.wallets),
        };
        const products = parsePortfolioProducts(portfolioRes);
        if (products) {
            result.portfolio_allocation = products;
        }
    }

    success(result);
}

async function balance(symbol: string) {
    if (!symbol) {
        fail(ErrorCode.INVALID_ARGS, "Token symbol required. Example: npx tsx scripts/account.ts balance BTC");
    }

    const upper = symbol.toUpperCase();
    const [cryptoRes, allocationRes] = await Promise.all([
        apiGet("/v1/crypto-account"),
        apiGet(`/v1/currency_allocation?currency=${encodeURIComponent(upper)}`),
    ]);
    assertOk(cryptoRes, "Crypto balance fetch");

    const wallet = (cryptoRes.data.account.wallets as any[]).find(
        (w: any) => w.currency.toUpperCase() === upper,
    );

    const result: Record<string, any> = {
        currency: upper,
        available: wallet?.available?.amount ?? "0",
        available_note: "available for trading",
        balance: wallet?.balance?.amount ?? "0",
    };

    const allocation = parseCurrencyAllocation(allocationRes);
    if (allocation) {
        result.product_allocation = allocation;
    }

    success(result);
}

async function tradingLimit() {
    const res = await apiGet("/v1/api-keys/current");
    assertOk(res, "Trading limit fetch");

    const k = res.data.api_key;
    const limit = parseFloat(k.weekly_trading_limit_in_usd);
    const remaining = parseFloat(k.remaining_weekly_trading_limit_in_usd);

    success({ used: limit - remaining, limit, remaining, currency: "USD" });
}

async function resolveSource(tradeType: string) {
    const validTypes = ["purchase", "sale", "exchange"];
    if (!validTypes.includes(tradeType)) {
        fail(ErrorCode.INVALID_ARGS, `Invalid trade type "${tradeType}". Use: purchase | sale | exchange`);
    }

    const walletType = tradeType === "purchase" ? "fiat" : "crypto";

    if (walletType === "fiat") {
        const res = await apiGet("/v1/fiat-account");
        assertOk(res, "Fiat balance fetch");
        emitResolveResult(filterFiat(res.data.account.balances), walletType);
    } else {
        const res = await apiGet("/v1/crypto-account");
        assertOk(res, "Crypto balance fetch");
        emitResolveResult(filterCrypto(res.data.account.wallets), walletType);
    }
}

function emitResolveResult(funded: any[], walletType: string): never {
    if (funded.length === 1) {
        success({ status: "SELECTED", currency: funded[0].currency, walletType });
    } else if (funded.length > 1) {
        success({ status: "AMBIGUOUS", options: funded.map((w: any) => w.currency), walletType });
    } else {
        success({ status: "EMPTY", walletType });
    }
}

async function revokeKey() {
    const res = await apiPost("/v1/api-keys/self-revoke", {});

    const errorCode = res.data?.error || res.data?.code;

    if (errorCode === "api_key_not_found") {
        fail(ErrorCode.API_KEY_NOT_FOUND, "API key not found — it may have already been revoked or does not exist.");
    }

    if (errorCode === "key_not_active") {
        fail(ErrorCode.API_KEY_NOT_FOUND, "API key is not active — it has been revoked or expired.");
    }

    if (res.status !== 200 || res.data?.ok === false) {
        const apiMsg = res.data?.error_message || res.data?.message;
        const detail = apiMsg && errorCode ? `${errorCode}: ${apiMsg}` : errorCode || apiMsg || `HTTP ${res.status}`;
        fail(ErrorCode.API_ERROR, `Kill switch request failed: ${detail}`);
    }

    success({ revoked: true });
}

// ---------------------------------------------------------------------------
// CLI router
// ---------------------------------------------------------------------------

const USAGE = `Usage: npx tsx scripts/account.ts <command> [args]

Commands:
  balances [fiat|crypto|all]       Filtered non-zero balances (default: all)
  balance <SYMBOL>                 Single token balance lookup
  trading-limit                    Weekly trading limit info
  resolve-source <type>            Find funded wallets (purchase|sale|exchange)
  revoke-key                       Revoke API key (kill switch)`;

run(async () => {
    const [command, arg] = process.argv.slice(2);

    switch (command) {
        case "balances":
            return balances(arg || "all");
        case "balance":
            return balance(arg);
        case "trading-limit":
            return tradingLimit();
        case "resolve-source":
            return resolveSource(arg);
        case "revoke-key":
            return revokeKey();
        default:
            fail(ErrorCode.INVALID_ARGS, command ? `Unknown command "${command}".\n\n${USAGE}` : USAGE);
    }
});
