export const ErrorCode = {
    MISSING_ENV: "MISSING_ENV",
    API_ERROR: "API_ERROR",
    INVALID_ARGS: "INVALID_ARGS",
    QUOTATION_FAILED: "QUOTATION_FAILED",
    EXECUTION_FAILED: "EXECUTION_FAILED",
    API_KEY_NOT_FOUND: "API_KEY_NOT_FOUND",
    RATE_LIMITED: "RATE_LIMITED",
    UNKNOWN: "UNKNOWN",
} as const;

export type ErrorCode = (typeof ErrorCode)[keyof typeof ErrorCode];

interface SuccessOutput {
    ok: true;
    data: unknown;
}

interface ErrorOutput {
    ok: false;
    error: string;
    error_message: string;
}

export function success(data: unknown): never {
    const out: SuccessOutput = { ok: true, data };
    console.log(JSON.stringify(out, null, 2));
    process.exit(0);
}

export function fail(code: ErrorCode, message: string): never {
    const out: ErrorOutput = { ok: false, error: code, error_message: message };
    console.log(JSON.stringify(out, null, 2));
    process.exit(1);
}

export function run(fn: () => Promise<void>): void {
    fn().catch((err: unknown) => {
        const message = err instanceof Error ? err.message : String(err);
        fail(ErrorCode.UNKNOWN, message);
    });
}
