# BNB Chain Contract Notes

Store or update verified contract addresses and API endpoints here.

## Suggested fields to maintain
- Comptroller / Pool lens / Oracle contracts
- vToken addresses by market
- Subgraph / API endpoints (with date verified)
- RPC endpoints used for reads

## Verified API endpoints
- Base URL (mainnet): `https://api.venus.io` (verified: 2026-02-22)
- Markets list: `GET /markets?chainId=56` (verified: 2026-02-22)
- Pools list: `GET /pools?chainId=56` (verified: 2026-02-22)

## Verification practice
- Prefer official Venus docs + verified explorers.
- Record `verified_at` date for each endpoint/address.
- If uncertain, mark as unverified and avoid hard claims.
