import { apiGet, apiPost, assertOk } from "./lib/api.js";
import { ErrorCode, fail, run, success } from "./lib/output.js";

// ---------------------------------------------------------------------------
// Quotation body builders
// ---------------------------------------------------------------------------

const QUOTE_PATHS: Record<string, string> = {
    purchase: "/v1/crypto-purchase/quotations",
    sale: "/v1/crypto-sales/quotations",
    exchange: "/v1/crypto-exchange/quotations",
};

const ORDER_PATHS: Record<string, string> = {
    purchase: "/v1/crypto-purchase/orders",
    sale: "/v1/crypto-sales/orders",
    exchange: "/v1/crypto-exchange/orders",
};

function buildQuotationBody(type: string, params: any): Record<string, any> {
    switch (type) {
        case "purchase":
            return {
                from_currency: params.from_currency,
                to_currency: params.to_currency,
                ...(params.from_amount
                    ? { from_amount: params.from_amount }
                    : { to_amount: params.to_amount }),
            };
        case "sale":
            return {
                from_currency: params.from_currency,
                from_amount: params.from_amount,
                to_currency: params.to_currency,
                fixed_side: params.fixed_side || "from",
            };
        case "exchange":
            return {
                from: params.from_currency,
                to: params.to_currency,
                from_amount: params.from_amount,
                side: params.side || "buy",
            };
        default:
            fail(ErrorCode.INVALID_ARGS, `Unknown trade type: ${type}`);
    }
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function quote(type: string, paramsJson: string) {
    if (!QUOTE_PATHS[type]) {
        fail(ErrorCode.INVALID_ARGS, `Invalid trade type "${type}". Use: purchase | sale | exchange`);
    }
    if (!paramsJson) {
        fail(ErrorCode.INVALID_ARGS, `JSON params required. Example: npx tsx scripts/trade.ts quote purchase '{"from_currency":"USD","to_currency":"BTC","from_amount":"100"}'`);
    }

    let params: any;
    try {
        params = JSON.parse(paramsJson);
    } catch {
        fail(ErrorCode.INVALID_ARGS, `Invalid JSON: ${paramsJson}`);
    }

    const body = buildQuotationBody(type, params);
    const res = await apiPost(QUOTE_PATHS[type], body);

    if (res.status !== 200 || res.data?.ok !== true) {
        const apiError = res.data?.error;
        const apiMsg = res.data?.error_message;
        const msg = apiMsg && apiError ? `${apiError}: ${apiMsg}` : apiError || apiMsg || "Quotation request rejected.";
        fail(ErrorCode.QUOTATION_FAILED, msg);
    }

    success(res.data.quotation);
}

async function confirm(type: string, quotationId: string) {
    if (!ORDER_PATHS[type]) {
        fail(ErrorCode.INVALID_ARGS, `Invalid trade type "${type}". Use: purchase | sale | exchange`);
    }
    if (!quotationId) {
        fail(ErrorCode.INVALID_ARGS, "Quotation ID required. Example: npx tsx scripts/trade.ts confirm purchase <quotation-id>");
    }

    const body: Record<string, string> =
        type === "exchange"
            ? { quotation_id: quotationId, side: "buy" }
            : { quotation_id: quotationId };

    const res = await apiPost(ORDER_PATHS[type], body);

    if (res.status !== 200 || res.data?.ok !== true) {
        const apiError = res.data?.error;
        const apiMsg = res.data?.error_message;
        const msg = apiMsg && apiError ? `${apiError}: ${apiMsg}` : apiError || apiMsg || "Order confirmation failed.";
        fail(ErrorCode.EXECUTION_FAILED, msg);
    }

    success(res.data.transaction);
}

async function history() {
    const res = await apiGet("/v1/transactions");
    assertOk(res, "Transaction history fetch");

    const txns = (res.data.transactions ?? []).slice(0, 5);
    success(txns);
}

// ---------------------------------------------------------------------------
// CLI router
// ---------------------------------------------------------------------------

const USAGE = `Usage: npx tsx scripts/trade.ts <command> [args]

Commands:
  quote <type> '<json>'            Get quotation (purchase|sale|exchange)
  confirm <type> <quotation-id>    Confirm order
  history                          Last 5 transactions`;

run(async () => {
    const [command, arg1, arg2] = process.argv.slice(2);

    switch (command) {
        case "quote":
            return quote(arg1, arg2);
        case "confirm":
            return confirm(arg1, arg2);
        case "history":
            return history();
        default:
            fail(ErrorCode.INVALID_ARGS, command ? `Unknown command "${command}".\n\n${USAGE}` : USAGE);
    }
});
