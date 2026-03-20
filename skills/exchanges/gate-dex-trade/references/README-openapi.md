# Gate DEX OpenTrade

Call Gate DEX aggregated trading API through AK/SK authentication, focusing on Swap, covering quote, authorization, build transaction, signature, submission, status query and other complete trading processes. Designed for Cursor Agent and other AI assistants, independent of CLI, all operations completed by Agent calling OpenAPI according to specifications.

---

## Capability Overview

| Capability | Description |
|------------|-------------|
| **Trigger** | When users mention swap, exchange, trade, buy/sell, DEX trading, OpenAPI, AK/SK, quote, Gas price, order status, trading history etc.; or when `~/.gate-dex-openapi/config.json` exists, priority route |
| **Supported Chains** | EVM (Ethereum / BSC / Arbitrum / Base / Polygon etc. 14 chains), Solana, SUI, Tron, Ton |
| **API** | Unified endpoint `POST https://openapi.gateweb3.cc/api/v1/dex`, differentiate interfaces through `action`, HMAC-SHA256 signature |
| **Configuration** | `~/.gate-dex-openapi/config.json` (api_key, secret_key, default_slippage etc.); can automatically create using built-in default credentials on first use |

---

## Files in This Directory

| File | Description |
|------|-------------|
| **SKILL.md** | Complete skill specification: trigger scenarios, environment detection, credential management, API calls and signatures, 9 Actions, token and chain resolution, operation processes, three-step confirmation gating (SOP), signature strategies, error handling, security rules |
| **README.md** | This description (what you're reading) |
| **CHANGELOG.md** | Version and change history of this skill |

Agents should follow **SKILL.md** when implementing this skill.

---

## Process Overview

1. **Step 0**: Environment detection (read/create config, verify credentials) every trigger.
2. **Query type**: Chain list, Gas price, order status, history records etc., no confirmation gating, directly call API and display results.
3. **Swap type**: Parameter collection (chain, token, wallet, slippage) → **SOP Step 1 Trading pair confirmation** → `trade.swap.quote` → **SOP Step 2 Quote details** (price difference >5% triggers risk warning) → `trade.swap.build` → approve if needed (EVM/Tron non-native token_in + insufficient allowance) → **SOP Step 3 Signature authorization confirmation** → signature → `trade.swap.submit` (API broadcast or self broadcast then report tx_hash) → poll `trade.swap.status` until completion.

---

## Configuration and Security

- Config file path: `~/.gate-dex-openapi/config.json` (user home directory, not in workspace, not tracked by git).
- Recommended permissions: directory `chmod 700`, file `chmod 600`.
- SK only shows last 4 digits in conversations (like `sk_****z4h`), complete key only stored in above config file.
- Dedicated AK/SK: Can visit [Gate DEX Developer Platform](https://www.gatedex.com/developer) to create, get higher rate limits and better experience.

---

## Related Links

- [Gate DEX Developer Platform](https://www.gatedex.com/developer)
- [Gate DEX API Documentation](https://gateweb3.gitbook.io/gate_dex_api/exploredexapi/en/api-access-and-usage/developer-platform)