/**
 * "Pay with USDC" button component for taraquinn.ai.
 *
 * Full payment flow: connect wallet → sign EIP-3009 → get download link.
 * Uses wagmi for wallet connection and @x402/fetch for the x402 protocol.
 *
 * Prerequisites:
 *   - WagmiProvider configured at app root (see wagmi-config.ts)
 *   - @x402/fetch, @x402/evm, wagmi, viem installed
 *
 * Usage:
 *   <PayWithUsdcButton
 *     productUrl="/api/products/x402-paywall-kit/download"
 *     price="$29"
 *     onSuccess={(data) => window.location.href = data.downloadUrl}
 *   />
 */

import React from "react";
import { useConnect, useAccount, useDisconnect } from "wagmi";
import { useX402Payment, type PaymentStatus } from "./use-x402-payment";

interface PayWithUsdcButtonProps {
  /** The paywalled API endpoint URL */
  productUrl: string;
  /** Display price (e.g., "$29") */
  price: string;
  /** Called with response data after successful payment */
  onSuccess?: (data: { downloadUrl: string; [key: string]: unknown }) => void;
  /** Called on payment error */
  onError?: (error: Error) => void;
  /** Additional CSS class */
  className?: string;
}

const STATUS_LABELS: Record<PaymentStatus, string> = {
  idle: "",
  connecting: "Connecting wallet...",
  signing: "Sign the payment in your wallet...",
  processing: "Processing payment...",
  success: "Payment successful!",
  error: "Payment failed",
};

export function PayWithUsdcButton({
  productUrl,
  price,
  onSuccess,
  onError,
  className = "",
}: PayWithUsdcButtonProps) {
  const { address, isConnected } = useAccount();
  const { connectors, connect } = useConnect();
  const { disconnect } = useDisconnect();
  const { pay, status, error, reset } = useX402Payment({
    onSuccess: (result) => {
      onSuccess?.(result.data as { downloadUrl: string });
    },
    onError,
  });

  const isProcessing = ["connecting", "signing", "processing"].includes(status);

  async function handleClick() {
    if (!isConnected) {
      // Connect with first available connector (MetaMask, WalletConnect, etc.)
      const connector = connectors[0];
      if (connector) {
        connect({ connector });
      }
      return;
    }

    reset();
    await pay(productUrl);
  }

  function getButtonText(): string {
    if (!isConnected) return `Pay with USDC — ${price}`;
    if (isProcessing) return STATUS_LABELS[status];
    if (status === "success") return "Download Ready";
    if (status === "error") return `Retry Payment — ${price}`;
    return `Pay with USDC — ${price}`;
  }

  return (
    <div className={`pay-with-usdc ${className}`}>
      <button
        onClick={handleClick}
        disabled={isProcessing}
        className={`pay-with-usdc-btn pay-with-usdc-btn--${status}`}
      >
        {getButtonText()}
      </button>

      {isConnected && status === "idle" && (
        <div className="pay-with-usdc-wallet">
          <span className="pay-with-usdc-address">
            {address?.slice(0, 6)}...{address?.slice(-4)}
          </span>
          <button
            onClick={() => disconnect()}
            className="pay-with-usdc-disconnect"
          >
            Disconnect
          </button>
        </div>
      )}

      {status === "signing" && (
        <p className="pay-with-usdc-hint">
          Check your wallet for a signature request. This authorizes a USDC
          transfer — no gas fees required.
        </p>
      )}

      {error && (
        <p className="pay-with-usdc-error">
          {error.message}
        </p>
      )}

      {status === "success" && (
        <p className="pay-with-usdc-success">
          Payment confirmed on Base. Your download is ready.
        </p>
      )}
    </div>
  );
}
