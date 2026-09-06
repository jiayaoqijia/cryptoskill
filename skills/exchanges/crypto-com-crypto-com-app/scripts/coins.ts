import { apiGet, assertOk } from "./lib/api.js";
import { ErrorCode, fail, run, success } from "./lib/output.js";

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function search(paramsJson: string) {
    if (!paramsJson) {
        fail(
            ErrorCode.INVALID_ARGS,
            `JSON params required. Example: npx tsx scripts/coins.ts search '{"keyword":"BTC","sort_by":"rank","sort_direction":"asc","native_currency":"USD","page_size":10}'`,
        );
    }

    let params: any;
    try {
        params = JSON.parse(paramsJson);
    } catch {
        fail(ErrorCode.INVALID_ARGS, `Invalid JSON: ${paramsJson}`);
    }

    const qs = new URLSearchParams();
    for (const [key, val] of Object.entries(params)) {
        if (val !== undefined && val !== null) qs.set(key, String(val));
    }

    const path = `/v1/crypto/coins?${qs.toString()}`;
    const res = await apiGet(path);
    assertOk(res, "Coin search");

    success({
        coins: res.data.coins,
        pagination: res.data.pagination,
    });
}

// ---------------------------------------------------------------------------
// CLI router
// ---------------------------------------------------------------------------

const USAGE = `Usage: npx tsx scripts/coins.ts <command> [args]

Commands:
  search '<json>'    Search coins by keyword, sort, pagination`;

run(async () => {
    const [command, arg] = process.argv.slice(2);

    switch (command) {
        case "search":
            return search(arg);
        default:
            fail(ErrorCode.INVALID_ARGS, command ? `Unknown command "${command}".\n\n${USAGE}` : USAGE);
    }
});
