/**
 * React hook for x402 USDC payments via browser wallet.
 *
 * Manages the full payment flow:
 * 1. Call paywalled endpoint → get 402
 * 2. Parse x402 payment requirements
 * 3. Sign EIP-3009 authorization via connected wallet
 * 4. Retry with X-PAYMENT header → get response
 *
 * Prerequisites:
 *   npm install @x402/fetch @x402/evm viem wagmi @tanstack/react-query
 *
 * Usage:
 *   const { pay, status, error } = useX402Payment();
 *   const result = await pay("https://taraquinn.ai/api/products/x402-paywall-kit/download");
 */

import { useState, useCallback } from "react";
import { useWalletClient, usePublicClient } from "wagmi";
import { wrapFetchWithPayment } from "@x402/fetch";
import { toClientEvmSigner, ExactEvmScheme } from "@x402/evm";
import type { x402ClientConfig } from "@x402/fetch";

export type PaymentStatus = "idle" | "connecting" | "signing" | "processing" | "success" | "error";

export interface X402PaymentResult {
  response: Response;
  data: unknown;
}

export interface UseX402PaymentOptions {
  /** CAIP-2 network ID (default: "eip155:8453" for Base mainnet) */
  network?: string;
  /** Called when payment starts */
  onStart?: () => void;
  /** Called on successful payment */
  onSuccess?: (result: X402PaymentResult) => void;
  /** Called on payment error */
  onError?: (error: Error) => void;
}

export function useX402Payment(options: UseX402PaymentOptions = {}) {
  const { network = "eip155:8453", onStart, onSuccess, onError } = options;
  const { data: walletClient } = useWalletClient();
  const publicClient = usePublicClient();
  const [status, setStatus] = useState<PaymentStatus>("idle");
  const [error, setError] = useState<Error | null>(null);

  const pay = useCallback(
    async (url: string, init?: RequestInit): Promise<X402PaymentResult | null> => {
      setError(null);

      if (!walletClient) {
        const err = new Error("Wallet not connected. Please connect your wallet first.");
        setError(err);
        setStatus("error");
        onError?.(err);
        return null;
      }

      if (!publicClient) {
        const err = new Error("Public client not available.");
        setError(err);
        setStatus("error");
        onError?.(err);
        return null;
      }

      try {
        onStart?.();
        setStatus("connecting");

        // Create x402 signer from connected wallet
        const signer = toClientEvmSigner(
          {
            address: walletClient.account.address,
            signTypedData: (message) => walletClient.signTypedData(message as Parameters<typeof walletClient.signTypedData>[0]),
          },
          publicClient,
        );

        setStatus("signing");

        // Configure x402 client with EVM scheme
        const config: x402ClientConfig = {
          schemes: [new ExactEvmScheme(signer)],
        };

        // Wrap fetch with x402 payment handling
        const x402Fetch = wrapFetchWithPayment(fetch, config);

        setStatus("processing");

        // Make the request — x402 handles the 402 → sign → retry flow
        const response = await x402Fetch(url, init);

        if (response.ok) {
          const data = await response.json();
          const result: X402PaymentResult = { response, data };
          setStatus("success");
          onSuccess?.(result);
          return result;
        }

        // Payment failed or was rejected
        const errorText = await response.text().catch(() => "");
        throw new Error(
          `Payment failed with status ${response.status}${errorText ? `: ${errorText}` : ""}`,
        );
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        setError(error);
        setStatus("error");
        onError?.(error);
        return null;
      }
    },
    [walletClient, publicClient, network, onStart, onSuccess, onError],
  );

  const reset = useCallback(() => {
    setStatus("idle");
    setError(null);
  }, []);

  return {
    /** Trigger a payment for the given URL */
    pay,
    /** Current payment status */
    status,
    /** Error from the last payment attempt */
    error,
    /** Whether a wallet is connected */
    isWalletConnected: !!walletClient,
    /** Reset status back to idle */
    reset,
  };
}
