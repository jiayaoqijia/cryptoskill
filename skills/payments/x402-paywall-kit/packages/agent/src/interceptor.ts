import {
  createWalletClient,
  createPublicClient,
  http,
  type Hex,
  type Chain,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { baseSepolia, base } from "viem/chains";
import { ExactEvmScheme, toClientEvmSigner } from "@x402/evm";
import { x402Client, x402HTTPClient } from "@x402/core/client";
import type { Network } from "@x402/core/types";
import {
  createPolicyEngine,
  createPaymentLogger,
  type X402Policy,
} from "x402-kit-shared";

/**
 * Configuration for creating a policy-aware x402 fetch wrapper.
 */
export interface AgentFetchConfig {
  /** Hex private key for the payer wallet. */
  walletPrivateKey: Hex;
  /** Policy rules for controlling spending. */
  policy: X402Policy;
  /** Blockchain network in CAIP-2 format (e.g., "eip155:84532"). */
  network: Network;
  /** Path to the daily spend persistence file. */
  spendFilePath?: string;
  /** Path to the payment log file. */
  logFilePath?: string;
  /** Custom JSON-RPC URL. */
  rpcUrl?: string;
  /** Token decimals for the payment asset (default: 6 for USDC). */
  tokenDecimals?: number;
}

const CHAIN_MAP: Record<number, Chain> = {
  8453: base,
  84532: baseSepolia,
};

/**
 * Convert a raw token amount (smallest unit) to a human-readable string.
 * E.g., "1000000" with 6 decimals → "1".
 */
function rawToHuman(rawAmount: string, decimals: number): string {
  const raw = Number(rawAmount);
  return (raw / 10 ** decimals).toString();
}

/**
 * Create a fetch wrapper that auto-detects x402 paywalls, checks
 * the spending policy, signs a payment if approved, and retries.
 *
 * If the policy denies the payment, the original 402 response is
 * returned without attempting payment.
 */
export function createAgentFetch(config: AgentFetchConfig): typeof fetch {
  const account = privateKeyToAccount(config.walletPrivateKey);
  const chainId = parseInt(config.network.split(":")[1]);
  const chain = CHAIN_MAP[chainId];
  const decimals = config.tokenDecimals ?? 6;

  const walletClient = createWalletClient({
    account,
    chain,
    transport: http(config.rpcUrl),
  });
  const publicClient = createPublicClient({
    chain,
    transport: http(config.rpcUrl),
  });

  const signer = toClientEvmSigner(
    {
      address: account.address,
      signTypedData: (message) => walletClient.signTypedData(message),
    },
    publicClient,
  );

  const x402client = new x402Client().register(
    config.network,
    new ExactEvmScheme(signer),
  );
  const httpClient = new x402HTTPClient(x402client);

  const policyEngine = createPolicyEngine(config.policy, {
    spendFilePath: config.spendFilePath ?? ".x402/daily-spend.json",
  });

  const logger = createPaymentLogger(config.logFilePath);

  const agentFetch = async (
    input: RequestInfo | URL,
    init?: RequestInit,
  ): Promise<Response> => {
    const url =
      typeof input === "string"
        ? input
        : input instanceof URL
          ? input.toString()
          : input.url;

    // 1. Make the initial request
    const request = new Request(input, init);
    const requestClone = request.clone();
    const response = await fetch(request);

    if (response.status !== 402) {
      return response;
    }

    // 2. Parse x402 payment requirements from 402 response
    let paymentRequired;
    try {
      const responseClone = response.clone();
      let body: unknown;
      try {
        const text = await responseClone.text();
        if (text) body = JSON.parse(text);
      } catch {
        /* body may not be JSON */
      }
      paymentRequired = httpClient.getPaymentRequiredResponse(
        (name) => response.headers.get(name) ?? undefined,
        body,
      );
    } catch {
      return response; // Not a valid x402 response
    }

    // 3. Find a matching payment requirement for our network
    const matchingReq = paymentRequired.accepts.find(
      (r) => r.network === config.network,
    );
    if (!matchingReq) {
      return response; // No matching payment option
    }

    // 4. Convert raw amount to human-readable for policy checks
    const humanAmount = rawToHuman(matchingReq.amount, decimals);

    // 5. Check policy
    const domain = new URL(url).hostname;
    const policyResult = policyEngine.evaluate(
      humanAmount,
      matchingReq.network,
      matchingReq.asset,
      domain,
    );

    if (policyResult.decision !== "approved") {
      logger.log({
        timestamp: new Date().toISOString(),
        url,
        amount: humanAmount,
        asset: matchingReq.asset,
        network: matchingReq.network,
        facilitator: "",
        success: false,
        error: policyResult.reason,
        policyDecision: policyResult.decision,
      });
      return response; // Return the 402 — policy denied
    }

    // 6. Create and sign the payment payload
    let paymentPayload;
    try {
      paymentPayload = await httpClient.createPaymentPayload(paymentRequired);
    } catch (error) {
      logger.log({
        timestamp: new Date().toISOString(),
        url,
        amount: humanAmount,
        asset: matchingReq.asset,
        network: matchingReq.network,
        facilitator: "",
        success: false,
        error: error instanceof Error ? error.message : String(error),
        policyDecision: "approved",
      });
      return response;
    }

    // 7. Retry with payment header
    const paymentHeaders =
      httpClient.encodePaymentSignatureHeader(paymentPayload);
    for (const [key, value] of Object.entries(paymentHeaders)) {
      requestClone.headers.set(key, value);
    }
    const retryResponse = await fetch(requestClone);

    // 8. Record spend and log
    policyEngine.recordSpend(humanAmount);
    logger.log({
      timestamp: new Date().toISOString(),
      url,
      amount: humanAmount,
      asset: matchingReq.asset,
      network: matchingReq.network,
      facilitator: "",
      success: retryResponse.ok,
      error: retryResponse.ok ? undefined : `HTTP ${retryResponse.status}`,
      policyDecision: "approved",
    });

    return retryResponse;
  };

  return agentFetch as typeof fetch;
}
