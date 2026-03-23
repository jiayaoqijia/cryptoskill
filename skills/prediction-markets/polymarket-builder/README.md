# Polymarket Builder Program Skill

This skill covers advanced integration patterns for the [Polymarket Builder Program](https://polymarket.com/builders) — the production-grade details that aren't in the standard docs.

## What's Covered

- **Builder Program registration** — earn weekly USDC fee rebates on routed volume
- **`py-builder-signing-sdk` usage** — builder-specific credentials separate from trading credentials
- **Gnosis Safe wallet integration** — signature_type=2 for gasless order signing
- **5-minute epoch market discovery** — deterministic slug pattern `{coin}-updown-5m-{epoch}`
- **CTF conditional token balance polling** — fixes the `400 not enough balance/allowance` error
- **Production scalper bot patterns** — gate logic, risk engine, circuit breakers

## Key Fixes Documented

Every item below cost real USDC to learn running live on Polymarket:

1. `update_balance_allowance` is a **GET**, not a transaction — polling fix included
2. Builder rewards work via HTTP headers only — no contract interaction needed
3. 5-min slugs follow `{coin}-updown-5m-{epoch}` where `epoch = (ts // 300) * 300`
4. Gamma API returns 403 without a browser User-Agent header

## Maintained By

[DeepBlue](https://deepbluebase.xyz) — autonomous crypto trading agents running live on Polymarket since 2025.
