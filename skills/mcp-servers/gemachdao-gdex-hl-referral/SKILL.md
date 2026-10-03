---
name: gdex-hl-referral
description: HyperLiquid referral info and reward claims — distinct from the HL copy-trading referral flows
---

# GDEX: HyperLiquid Referral

Inspect a wallet's HyperLiquid referral status and submit claims for accrued
rewards. This is the user-side HL referral flow exposed under
`/v1/hl_ref/*` — **distinct** from the copy-trading top-traders referral
flow under `/v1/hl/top_traders_by_pnl` and from the builder referral under
`/v1/hl/builder_referral`.

## When to Use

- Checking how much HL referral reward a wallet has accrued
- Submitting a claim transaction for accrued rewards

## Prerequisites

- `@gemachdao/gdex-skill` installed
- Authenticated via managed custody — see **gdex-authentication**
- For claim: a pre-built `computedData` payload built by the caller using
  the standard managed-custody encrypted-payload contract (claim ABI lives
  in `src/api/services/ServiceHlReferral.ts` of the backend)

## Backend Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/v1/hl_ref/info` | Referral info (earned, eligibility, code) |
| `POST` | `/v1/hl_ref/request_claim` | Submit a reward claim |

## SDK Usage

```typescript
import { GdexSkill } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();
skill.loginWithApiKey(process.env.GDEX_API_KEY!);

const info = await skill.getHlReferralInfo({ userAddress: '0xWallet' });

// Claim rewards (caller pre-builds computedData)
const result = await skill.requestHlReferralClaim({ computedData });
```

## Notes

- Eligibility is enforced server-side based on referral state and minimum
  thresholds.
- The claim response typically contains a `requestId` to poll via
  `/v1/trade-status/:requestId` when the claim is processed asynchronously.
