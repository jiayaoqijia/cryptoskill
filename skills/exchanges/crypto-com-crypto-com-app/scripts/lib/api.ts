import crypto from "node:crypto";
import os from "node:os";
import { ErrorCode, fail } from "./output.js";

export const BASE_URL = "https://wapi.crypto.com";

function getCredentials(): { apiKey: string; apiSecret: string } {
    const apiKey = process.env.CDC_API_KEY;
    const apiSecret = process.env.CDC_API_SECRET;
    if (!apiKey || !apiSecret) {
        fail(
            ErrorCode.MISSING_ENV,
            `CDC_API_KEY and/or CDC_API_SECRET not set. Run:\n  export CDC_API_KEY="your-key"\n  export CDC_API_SECRET="your-secret"`,
        );
    }
    return { apiKey, apiSecret };
}

function getSignedHeaders(method: string, path: string, body?: unknown): Record<string, string> {
    const { apiKey, apiSecret } = getCredentials();
    const timestamp = Date.now().toString();
    const bodyStr = body ? JSON.stringify(body) : "";
    const signPayload = timestamp + method.toUpperCase() + path + bodyStr;
    const signature = crypto
        .createHmac("sha256", apiSecret)
        .update(signPayload)
        .digest("base64");
    const userAgent = `Node/${process.version} ${os.platform()}/${os.release()}-cdc-clawbot/1.0`;

    const headers: Record<string, string> = {
        "User-Agent": userAgent,
        "Cdc-Api-Key": apiKey,
        "Cdc-Api-Timestamp": timestamp,
        "Cdc-Api-Signature": signature,
    };
    if (body) {
        headers["Content-Type"] = "application/json";
    }
    return headers;
}

interface ApiResponse {
    status: number;
    data: any;
}

async function request(method: string, path: string, body?: unknown): Promise<ApiResponse> {
    const signPath = path.split("?")[0];
    const headers = getSignedHeaders(method, signPath, body);
    const url = `${BASE_URL}${path}`;

    const res = await fetch(url, {
        method,
        headers,
        body: body ? JSON.stringify(body) : undefined,
    });

    let data: any;
    try {
        data = await res.json();
    } catch {
        fail(ErrorCode.API_ERROR, `Non-JSON response from ${method} ${path} (HTTP ${res.status})`);
    }

    return { status: res.status, data };
}

export async function apiGet(path: string): Promise<ApiResponse> {
    return request("GET", path);
}

export async function apiPost(path: string, body?: unknown): Promise<ApiResponse> {
    return request("POST", path, body);
}

export function assertOk(res: ApiResponse, context: string): void {
    if (res.status === 429) {
        fail(
            ErrorCode.RATE_LIMITED,
            `${context}: Rate limit exceeded. Wait 60 seconds before retrying.`,
        );
    }
    if (res.status !== 200 || res.data?.ok !== true) {
        const apiError = res.data?.error || res.data?.code;
        const apiMsg = res.data?.error_message || res.data?.message;
        const detail = apiMsg && apiError ? `${apiError}: ${apiMsg}` : apiError || apiMsg || `HTTP ${res.status}`;
        fail(ErrorCode.API_ERROR, `${context}: ${detail}`);
    }
}
