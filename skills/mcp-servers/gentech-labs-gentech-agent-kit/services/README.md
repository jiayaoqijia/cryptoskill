# x402 Gateway Backends (6 services)

FastAPI backends behind the x402 gateway. Each is paid via the gateway
(front gate verifies the standard `Authorization: x402 <proof>` header and
forwards `X-Payment-Proof`). Data sources are keyless public APIs.

| Service | Port | Data source | Price |
|---------|------|-------------|-------|
| token_security | 8088 | internal rugcheck | $0.01 |
| market_intelligence | 8082 | internal price API | $0.005 |
| agent_discovery | 8091 | 8004scan.io ERC-8004 registry | $0.01 |
| defi_lp_analytics | 8092 | DexScreener | $0.02 |
| wallet_analysis | 8093 | Solana RPC + DexScreener | $0.02 |
| nft_search | 8094 | Magic Eden | $0.01 |

Deploy: `systemctl enable --now x402-backend@<service>.service`
(unit template at /etc/systemd/system/x402-backend@.service)

Live on: https://api.gentechlabs.net/v1/<friendly>/...

## API Health Audit (`api-audit.py`)

**`api-audit.py`** probes every live API service and flags endpoints that
return hardcoded placeholder data (zeros / empty stubs) instead of real data.
**A placeholder API cannot earn revenue even when a client pays the x402
challenge** — it returns garbage, so it sits on the Bazaar looking live but
never converts.

```bash
python3 services/api-audit.py                 # audit all defined targets
python3 services/api-audit.py --url http://localhost:8080/v1/price/BTC  # single
python3 services/api-audit.py --health-only   # just health checks
```

Classification:
- ✅ **HEALTHY** — real data OR a proper 402 payment challenge
- ❌ **PLACEHOLDER** — hardcoded zeros/empty (fix these FIRST)
- ⚠️ **STUB** — empty array/dict shell
- 🔗 **REDIRECT** — 3xx (re-run with `--follow`)

**Fix pattern:** replace placeholder bodies with a real data source (CoinGecko /
Etherscan / live RPC / a working internal engine), add a pytest, restart the
service, re-run the audit. Always add placeholder-token cases to
`PLACEHOLDER_TOKENS` and verify exact-zero matching (don't flag `:0.xx` as a
zero).

**Real incident (Aug 3, 2026):** deal-tracker `/v1/deals` was a stub returning
`[]`; crypto-price returned `price:0.0 placeholder`; gas-price returned all-zero;
token-security returned `score:0 unknown`. All four now return live data. This
is exactly why the audit exists.
