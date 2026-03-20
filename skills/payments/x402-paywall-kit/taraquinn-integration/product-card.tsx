/**
 * Product card component for the x402 Paywall Kit on taraquinn.ai.
 *
 * Drop into the Products page. Supports both Stripe (fiat) and USDC (crypto)
 * payment flows.
 *
 * Prerequisites:
 *   - Stripe checkout session endpoint at /api/checkout (see stripe-checkout.ts)
 *   - x402 paywall endpoint at /api/products/x402-paywall-kit (see usdc-paywall.ts)
 *   - Environment variables: STRIPE_PRICE_ID, X402_PAYTO_ADDRESS
 */

import React, { useState } from "react";

interface ProductCardProps {
  /** Stripe checkout URL or API endpoint */
  stripeCheckoutUrl: string;
  /** x402 paywall endpoint for USDC payment */
  usdcPaymentUrl: string;
}

export function X402PaywallKitCard({
  stripeCheckoutUrl,
  usdcPaymentUrl,
}: ProductCardProps) {
  const [usdcLoading, setUsdcLoading] = useState(false);
  const [usdcError, setUsdcError] = useState<string | null>(null);

  async function handleStripeCheckout() {
    window.location.href = stripeCheckoutUrl;
  }

  async function handleUsdcPayment() {
    setUsdcLoading(true);
    setUsdcError(null);

    try {
      // Step 1: Hit the paywalled endpoint — gets 402 with x402 requirements
      const response = await fetch(usdcPaymentUrl);

      if (response.status === 402) {
        // Step 2: Parse x402 payment requirements from response
        const paymentRequired = await response.json();
        const requirements = paymentRequired.accepts?.[0];

        if (!requirements) {
          setUsdcError("No payment options available");
          return;
        }

        // Step 3: Prompt user to connect wallet and sign payment
        // This would integrate with wagmi/viem or WalletConnect
        // For now, show a message directing to wallet-based payment
        setUsdcError(
          "Wallet payment flow coming soon. Use Stripe checkout for now.",
        );
      } else if (response.ok) {
        // Payment already processed or free access
        const data = await response.json();
        window.location.href = data.downloadUrl;
      } else {
        setUsdcError(`Unexpected response: ${response.status}`);
      }
    } catch (err) {
      setUsdcError(err instanceof Error ? err.message : "Payment failed");
    } finally {
      setUsdcLoading(false);
    }
  }

  return (
    <div className="product-card">
      <div className="product-header">
        <h3>x402 Paywall Kit</h3>
        <span className="product-price">$29</span>
      </div>

      <p className="product-tagline">
        Crypto Payments for Agents &amp; Websites
      </p>

      <ul className="product-features">
        <li>Agent skill — auto-detect and pay x402 paywalls</li>
        <li>Express middleware — USDC paywalls in minutes</li>
        <li>Policy engine — spending limits &amp; domain filtering</li>
        <li>Payment logging — JSONL audit trail</li>
        <li>Demo app — working testnet example</li>
      </ul>

      <div className="product-stack">
        <span>TypeScript</span>
        <span>Base</span>
        <span>USDC</span>
        <span>Coinbase x402</span>
      </div>

      <div className="product-actions">
        <button
          className="btn btn-primary"
          onClick={handleStripeCheckout}
        >
          Buy with Card — $29
        </button>

        <button
          className="btn btn-secondary"
          onClick={handleUsdcPayment}
          disabled={usdcLoading}
        >
          {usdcLoading ? "Processing..." : "Pay with USDC — $29"}
        </button>
      </div>

      {usdcError && <p className="product-error">{usdcError}</p>}

      <div className="product-links">
        <a href="https://github.com/tara-quinn-ai/x402-kit">GitHub</a>
        <a href="https://www.npmjs.com/org/x402-kit">NPM</a>
      </div>
    </div>
  );
}
