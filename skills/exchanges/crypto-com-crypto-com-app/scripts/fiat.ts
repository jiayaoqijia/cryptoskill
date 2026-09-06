import readline from "node:readline";
import { apiGet, apiPost, assertOk } from "./lib/api.js";
import { ErrorCode, fail, run, success } from "./lib/output.js";

// ---------------------------------------------------------------------------
// Helper: TOTP prompt
// ---------------------------------------------------------------------------

async function promptTotp(): Promise<string> {
    const rl = readline.createInterface({ input: process.stdin, output: process.stderr });
    return new Promise((resolve) => {
        rl.question("TOTP code required. Enter your 6-digit authenticator code: ", (answer) => {
            rl.close();
            resolve(answer.trim());
        });
    });
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function discover() {
    const accountRes = await apiGet("/v1/fiat-account");
    assertOk(accountRes, "Fiat account fetch");

    const balances: any[] = accountRes.data.account?.balances ?? [];
    if (balances.length === 0) {
        success({ currencies: [] });
        return;
    }

    const currencies = [];
    for (const bal of balances) {
        const ccy = bal.currency;
        const balance = bal.amount?.amount ?? "0";

        const netRes = await apiGet(`/v1/fiat/payment-networks?currency=${encodeURIComponent(ccy)}`);
        if (netRes.status !== 200 || netRes.data.ok !== true) {
            currencies.push({ currency: ccy, balance, deposit: [], withdrawal: [] });
            continue;
        }

        const networks: any[] = netRes.data.available_payment_networks ?? [];
        const net = networks.find((n: any) => n.currency === ccy);
        if (!net) {
            currencies.push({ currency: ccy, balance, deposit: [], withdrawal: [] });
            continue;
        }

        currencies.push({
            currency: ccy,
            balance,
            deposit: net.deposit_push_payment_networks ?? [],
            withdrawal: net.withdrawal_payment_networks ?? [],
        });
    }

    success({ currencies });
}

async function paymentNetworks(currency: string) {
    if (!currency) {
        fail(ErrorCode.INVALID_ARGS, "Currency required. Example: npx tsx scripts/fiat.ts payment-networks USD");
    }

    const res = await apiGet(`/v1/fiat/payment-networks?currency=${encodeURIComponent(currency)}`);
    assertOk(res, `Payment networks fetch for ${currency}`);

    success(res.data.available_payment_networks);
}

async function depositMethods(currency: string, depositMethod: string) {
    if (!currency) {
        fail(ErrorCode.INVALID_ARGS, "Currency required. Example: npx tsx scripts/fiat.ts deposit-methods USD sepa");
    }
    if (!depositMethod) {
        fail(ErrorCode.INVALID_ARGS, "Deposit method required. Example: npx tsx scripts/fiat.ts deposit-methods USD sepa");
    }

    const res = await apiGet(
        `/v1/fiat/deposit-methods?currency=${encodeURIComponent(currency)}&deposit_method=${encodeURIComponent(depositMethod)}`,
    );
    assertOk(res, `Deposit methods fetch for ${currency} ${depositMethod}`);

    success(res.data.deposit_methods);
}

async function emailDepositInfo(currency: string, vibanType: string) {
    if (!currency) {
        fail(ErrorCode.INVALID_ARGS, "Currency required. Example: npx tsx scripts/fiat.ts email-deposit-info USD iban");
    }
    if (!vibanType) {
        fail(ErrorCode.INVALID_ARGS, "VIBAN type required. Example: npx tsx scripts/fiat.ts email-deposit-info USD iban");
    }

    const res = await apiPost("/v1/fiat/deposit-info/email", {
        currency,
        viban_type: vibanType,
    });
    assertOk(res, `Email deposit info for ${currency} ${vibanType}`);

    success(res.data.bank_info_email);
}

async function withdrawalDetails(currency: string, vibanType: string) {
    if (!currency) {
        fail(ErrorCode.INVALID_ARGS, "Currency required. Example: npx tsx scripts/fiat.ts withdrawal-details USD iban");
    }
    if (!vibanType) {
        fail(ErrorCode.INVALID_ARGS, "VIBAN type required. Example: npx tsx scripts/fiat.ts withdrawal-details USD iban");
    }

    const res = await apiGet(
        `/v1/fiat/withdrawal-details?currency=${encodeURIComponent(currency)}&viban_type=${encodeURIComponent(vibanType)}`,
    );
    assertOk(res, `Withdrawal details fetch for ${currency} ${vibanType}`);

    success(res.data.details);
}

async function createWithdrawalOrder(paramsJson: string) {
    if (!paramsJson) {
        fail(
            ErrorCode.INVALID_ARGS,
            `JSON params required. Example: npx tsx scripts/fiat.ts create-withdrawal-order '{"currency":"USD","amount":"100","viban_type":"iban"}'`,
        );
    }

    let params: any;
    try {
        params = JSON.parse(paramsJson);
    } catch {
        fail(ErrorCode.INVALID_ARGS, `Invalid JSON: ${paramsJson}`);
    }

    if (!params.currency || !params.amount || !params.viban_type) {
        fail(ErrorCode.INVALID_ARGS, "Required fields: currency, amount, viban_type");
    }

    const res = await apiPost("/v1/fiat/withdrawal-orders", params);
    assertOk(res, "Withdrawal order creation");

    success(res.data.viban_withdrawal_order);
}

async function createWithdrawal(orderId: string) {
    if (!orderId) {
        fail(ErrorCode.INVALID_ARGS, "Order ID required. Example: npx tsx scripts/fiat.ts create-withdrawal <order-id>");
    }

    let res = await apiPost("/v1/fiat/withdrawals", { order_id: orderId });

    // Check for TOTP requirement
    if (res.data?.error === "totp_required") {
        const otp = await promptTotp();
        res = await apiPost("/v1/fiat/withdrawals", { order_id: orderId, otp });
    }

    assertOk(res, "Withdrawal creation");

    success(res.data.viban_withdrawal);
}

async function bankAccounts(currency?: string) {
    const path = currency ? `/v1/fiat/bank-accounts?currency=${encodeURIComponent(currency)}` : "/v1/fiat/bank-accounts";
    const res = await apiGet(path);
    assertOk(res, currency ? `Bank accounts fetch for ${currency}` : "Bank accounts fetch");

    success(res.data.bank_accounts);
}

// ---------------------------------------------------------------------------
// CLI router
// ---------------------------------------------------------------------------

const USAGE = `Usage: npx tsx scripts/fiat.ts <command> [args]

Commands:
  discover                                       Cash overview (balances + payment networks)
  payment-networks <currency>                    Available deposit/withdrawal networks
  deposit-methods <currency> <deposit_method>    Bank details for a deposit method
  email-deposit-info <currency> <viban_type>     Email deposit instructions to user
  withdrawal-details <currency> <viban_type>     Withdrawal quotas, fees, minimums
  create-withdrawal-order '<json>'               Create withdrawal order
  create-withdrawal <order_id>                   Execute withdrawal (may prompt for TOTP)
  bank-accounts [currency]                       List linked bank accounts`;

run(async () => {
    const [command, arg1, arg2] = process.argv.slice(2);

    switch (command) {
        case "discover":
            return discover();
        case "payment-networks":
            return paymentNetworks(arg1);
        case "deposit-methods":
            return depositMethods(arg1, arg2);
        case "email-deposit-info":
            return emailDepositInfo(arg1, arg2);
        case "withdrawal-details":
            return withdrawalDetails(arg1, arg2);
        case "create-withdrawal-order":
            return createWithdrawalOrder(arg1);
        case "create-withdrawal":
            return createWithdrawal(arg1);
        case "bank-accounts":
            return bankAccounts(arg1);
        default:
            fail(ErrorCode.INVALID_ARGS, command ? `Unknown command "${command}".\n\n${USAGE}` : USAGE);
    }
});
