/**
 * Stripe checkout session API route for taraquinn.ai.
 *
 * Creates a Stripe Checkout session for the x402 Paywall Kit ($29).
 * After payment, sends download link via email (same as Business Starter flow).
 *
 * Add to: /api/checkout/x402-paywall-kit (Next.js API route or Express endpoint)
 *
 * Environment variables:
 *   STRIPE_SECRET_KEY     — Stripe secret key
 *   STRIPE_PRICE_ID       — Price ID for the x402 Paywall Kit ($29)
 *   SITE_URL              — Base URL (e.g., https://taraquinn.ai)
 */

// For Next.js App Router:
// import { NextRequest, NextResponse } from "next/server";
// import Stripe from "stripe";

// For Express:
// import { Request, Response } from "express";
// import Stripe from "stripe";

/*
 * Example implementation (Next.js App Router):
 *
 * const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
 *
 * export async function POST(req: NextRequest) {
 *   const session = await stripe.checkout.sessions.create({
 *     mode: "payment",
 *     payment_method_types: ["card"],
 *     line_items: [
 *       {
 *         price: process.env.STRIPE_PRICE_ID!,
 *         quantity: 1,
 *       },
 *     ],
 *     success_url: `${process.env.SITE_URL}/products/x402-paywall-kit/success?session_id={CHECKOUT_SESSION_ID}`,
 *     cancel_url: `${process.env.SITE_URL}/products/x402-paywall-kit`,
 *     customer_email: undefined, // Stripe will collect email
 *     metadata: {
 *       product: "x402-paywall-kit",
 *       version: "1.0.0",
 *     },
 *   });
 *
 *   return NextResponse.json({ url: session.url });
 * }
 */

/*
 * Example implementation (Express):
 *
 * import Stripe from "stripe";
 * import { Router } from "express";
 *
 * const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
 * const router = Router();
 *
 * router.post("/api/checkout/x402-paywall-kit", async (req, res) => {
 *   const session = await stripe.checkout.sessions.create({
 *     mode: "payment",
 *     payment_method_types: ["card"],
 *     line_items: [
 *       {
 *         price: process.env.STRIPE_PRICE_ID!,
 *         quantity: 1,
 *       },
 *     ],
 *     success_url: `${process.env.SITE_URL}/products/x402-paywall-kit/success?session_id={CHECKOUT_SESSION_ID}`,
 *     cancel_url: `${process.env.SITE_URL}/products/x402-paywall-kit`,
 *     metadata: {
 *       product: "x402-paywall-kit",
 *       version: "1.0.0",
 *     },
 *   });
 *
 *   res.json({ url: session.url });
 * });
 */

/*
 * Stripe Webhook (for email delivery):
 *
 * Handle `checkout.session.completed` event:
 * 1. Verify webhook signature
 * 2. Extract customer email from session
 * 3. Send download link email with the package tarball or GitHub access
 *
 * Same flow as the Business Starter product delivery.
 */

export const STRIPE_CONFIG = {
  productName: "x402 Paywall Kit",
  priceAmount: 2900, // cents
  currency: "usd",
  successPath: "/products/x402-paywall-kit/success",
  cancelPath: "/products/x402-paywall-kit",
  metadata: {
    product: "x402-paywall-kit",
    version: "1.0.0",
  },
};
