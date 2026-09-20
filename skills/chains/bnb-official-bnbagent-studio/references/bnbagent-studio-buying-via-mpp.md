---
name: bnbagent-studio-buying-via-mpp
description: When the user wants an agent to buy from a native MPP+B402 endpoint. Covers trust, quote, buy, recipe wiring, wallet limits, and unknown payment outcomes.
---

> **Reference file** of the `bnbagent-studio` router skill, installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill).

# Buy via native MPP+B402

MPP and x402 are parallel alternatives. Use this flow only when the server returns a native `WWW-Authenticate: Payment` challenge with method `b402` and intent `charge`. Never route an x402 402 body into this buyer and never add automatic protocol fallback.

## Trust, inspect, then buy

```bash
bag mpp trust https://seller.example/mpp --yes
bag mpp quote https://seller.example/mpp --asset U
bag mpp buy https://seller.example/mpp --asset U --max-usd 0.10
```

`trust` is an unpaid probe. Review the live domain, realm, recipient, CAIP-2 network, token address, EIP-3009 method, price, and cap. For an unreviewed endpoint, verify the realm and recipient out-of-band. The resulting `[payments.mpp.merchants.*]` entry pins all of them before any typed data is signed.

The current buyer supports only:

- `wallet.kind = "evm-local"` or an equivalent wallet exposing `sign.typed_data`;
- native MPP `b402.charge`;
- B402's pinned BSC EIP-3009 facts: U, plus Mainnet USD1 at `0x8d0D000Ee44948FC98c9B98A4FA4921476f08B0d` (18 decimals, `World Liberty Financial USD / 1` domain); `TEST_U` is `0x330949Aed7d00FCe0558C64ED6FeC9792616cC39` with 6 decimals and EIP-3009-only. Testnet does not support USD1;
- EIP-3009;
- one paid dispatch per call.

TWAK's delegated `x402.pay` permission is not generic EIP-712 signing, and Altana's current session interface does not expose the required signing surface. Both must fail before payment.

`--asset` is explicit and network-aware; omission means U. Mainnet USD1 is EIP-3009-only and
implemented on the MPP Buyer path, subject to the same live Commerce/facilitator release gates.
USDC/USDT catalog routes are Permit2-only, so MPP Buyer returns a typed unsupported-wallet-route
error and never falls back to x402 or another token. Testnet USD1 is rejected as unsupported
before signing or dispatch. Insufficient balance only produces verified retry hints.

## Wire the agent tools

```bash
bag recipe code mpp-buyer
```

This emits `mppBuyer.ts` with `quote_mpp` and `buy_with_mpp`. Spread `MPP_BUYER_TOOLS` into the generated AgentCore or Azure Foundry AI SDK tool map. Runtime enforcement remains in `@bnbagent/studio-runtime/mpp`; the LLM can tighten `max_usd` but cannot widen configured merchant or daily caps or choose another recipient.

## Unknown means stop

After `Authorization: Payment` crosses the fetch boundary, a timeout, connection loss, or paid response without a successful `Payment-Receipt` is an `unknown` outcome. Studio records `mpp_buy` with status `unknown`. Do not retry automatically or tell the user to rerun blindly. Reconcile the wallet/facilitator/seller state first; another request can create another payment.

Use `--local-dev` only for an operator-owned loopback endpoint. It permits plain HTTP and pins recipient plus realm from the live challenge for that invocation; it is not a production trust mechanism.
