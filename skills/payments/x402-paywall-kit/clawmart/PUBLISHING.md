# Publishing x402 Paywall Kit to ClawMart

## Prerequisites

1. **ClawMart seller account** — Create at https://www.shopclawmart.com (Tara Quinn AI)
2. **API key** — Get `CLAWMART_API_KEY` from the seller dashboard
3. **Product image** — Tara-branded, x402 themed (recommended: 1200x630px)

## Step 1: Bundle the Package

```bash
chmod +x clawmart/bundle.sh
./clawmart/bundle.sh
```

This creates `clawmart/x402-paywall-kit-1.0.0.tar.gz` containing all source code, skill files, demo app, and documentation.

## Step 2: Create the Listing

```bash
export CLAWMART_API_KEY="your-api-key-here"

curl -X POST https://www.shopclawmart.com/api/v1/listings \
  -H "Authorization: Bearer $CLAWMART_API_KEY" \
  -H "Content-Type: application/json" \
  -d @clawmart/listing.json
```

Save the returned `listing_id` for the upload step.

## Step 3: Upload the Package

```bash
LISTING_ID="returned-listing-id"

curl -X POST "https://www.shopclawmart.com/api/v1/listings/${LISTING_ID}/upload" \
  -H "Authorization: Bearer $CLAWMART_API_KEY" \
  -F "file=@clawmart/x402-paywall-kit-1.0.0.tar.gz" \
  -F "type=package"
```

## Step 4: Upload Product Image

```bash
curl -X POST "https://www.shopclawmart.com/api/v1/listings/${LISTING_ID}/upload" \
  -H "Authorization: Bearer $CLAWMART_API_KEY" \
  -F "file=@clawmart/product-image.png" \
  -F "type=image"
```

## Step 5: Publish

```bash
curl -X POST "https://www.shopclawmart.com/api/v1/listings/${LISTING_ID}/publish" \
  -H "Authorization: Bearer $CLAWMART_API_KEY"
```

## Verify

1. Visit the listing URL on shopclawmart.com
2. Confirm:
   - Title: "x402 Paywall Kit — Crypto Payments for Agents & Websites"
   - Price: $29
   - Category: Engineering
   - All 8 tags visible
   - Description renders correctly with markdown
3. Test a purchase flow (use a test card if available)

## Listing Details

| Field | Value |
|-------|-------|
| Title | x402 Paywall Kit — Crypto Payments for Agents & Websites |
| Price | $29 |
| Category | Engineering |
| Author | Tara Quinn AI |
| License | MIT |
| Tags | x402, crypto, payments, USDC, Base, paywall, agent-payments, middleware |

## What's Included in the Package

- **Agent skill**: SKILL.md + `@x402-kit/agent` source (HTTP interceptor, policy-aware auto-pay)
- **Express middleware**: `@x402-kit/express` source (enhanced paywall middleware with logging)
- **Shared library**: `@x402-kit/shared` source (policy engine, payment logger, types)
- **Demo app**: Paywalled Express API + agent script (Base Sepolia testnet)
- **Reference files**: Policy config example, agent setup example
- **Documentation**: PRD, per-package READMEs

## Updating

To publish a new version:

1. Update `version` in `clawmart/listing.json`
2. Update `VERSION` in `clawmart/bundle.sh`
3. Re-run `./clawmart/bundle.sh`
4. Upload the new tarball to the existing listing
