# Vault vs OUR engine — the follow-up pass (worked 20 Sep 2026)

Trigger: after a vault DD the user asks *"kondisi engine kita skrng gmn, kalau di compare ama punya dia
gmn, kan bisa di cek confignya dia"*. Deliverable = our live numbers (authoritative, local) against the
vault's, plus an honest statement of which system is failing how. Worked case: Krystal `paman vault`
(Robinhood Chain 4663) vs FlowMetrix (Meteora DLMM, Solana).

## 1. "Cek confignya dia" — there is no config endpoint

Guessing endpoints wastes calls. All three answered **404** through the render/extract proxy:

```
/vaults/{chainId}/{addr}/config   → 404 page not found
/vaults/{chainId}/{addr}/agent    → 404 page not found
/vaults/{chainId}/{addr}/settings → 404 page not found
```

(The raw `curl` variants answer 403 Cloudflare, which looks like "blocked" but is really "does not
exist behind the WAF" — the proxy disambiguates them. If `curl` says 403 and the proxy says 404, the
route is absent, not forbidden.)

**The public config surface IS the vault-detail JSON.** Fields that are genuinely configuration:

| Field | Worked case | Meaning |
|---|---|---|
| `maxTotalCost` | $42.93 | cost ceiling the agent may spend on a position |
| `minPnl` | $26.01 | the only profit floor exposed — **no cost-coverage / IL gate visible** |
| `vaultOwnerFeeBasisPoint` | 0 | owner's own performance cut (0 here; the platform's 10% is separate) |
| `riskScore` + `vaultSecurities[]` | HIGH; `IL_EXTRA 0`, `PRICE_IMPACT_HIGH 1`, `POOL_LIST_CUSTOM 2`, `TRUSTED_OWNER_ANON 1`, `TOKEN_SECURITY_NEUTRAL 2`, `OWNER_SHARE_HIGH 3` | the platform's own risk flags *with scores* — quote them as-is |
| `isAgentActivated`, `vaultType`, `isAutoFarmVault` | true / autofarm / true | whether an agent is actually driving it |

**Everything else must be inferred from positions.** That inference IS the config read-out, and it is
more honest than any settings dump:

- **Rotation rate** = median `strategies[].ageInSecond` (worked: 0.64 d → ~2.5 positions/day). That
  number is the fee-drag driver: every rotation pays gas + slippage.
- **Fee-tier aggression** = distribution of `strategies[].feeTierPercentage` (worked: 1% on 72/110,
  then 0.3%, 0.01%, 5%, 0%…). High-tier concentration = the agent is farming volatility, not depth.
- **Position sizing** = `initialDepositValue` per strategy (worked: $24–$129 on a $542 vault).
- **Pool risk appetite** = for each open position's `pool`: `apr30d` **beside** `drawdown24h`
  (worked: 596–1,641% fee APR with −10% to −20% daily drawdown).
- **What is absent is the finding**: no visible cost-coverage / breakeven gate, no IL guard — which is
  exactly why a lifetime `feeGenerated` of $254.88 coexisted with **−$162.03 net cash flow**.

## 2. Our side — local, authoritative, and it must be reconciled

Get it from `flowmetrix-ops` (`references/book-vs-chain-drift.md` for the full procedure): pm2 state,
`/api/health`, `/api/overview`, `/api/wallet`, engine logs (`[sizing]`, `[friction]`, `[drift]`), the
SQLite DB read-only via python, and the manual-LP registry at `~/.hermes/data/fm_manual_positions.json`.

Same discipline as the vault side: **never quote the panel/book number alone.** In the worked case the
book claimed +$43.12 (+15%) while the chain held **0.768332 SOL less** than the book (−23.2%), and the
engine's own drift line said *"Nothing has been corrected."*

## 3. Head-to-head axes (the table that answered it)

| Axis | Our engine (worked) | Their vault (worked) |
|---|---|---|
| Venue / chain | Meteora DLMM, Solana | Uniswap V3/V4 via Krystal, Robinhood Chain 4663 |
| Capital | 2.5436 SOL (~$276) + 0.29 SOL manual LP | TVL $542; $4,515 lifetime deposits |
| Cut of the yield | **0% performance fee** (LP keeps 90% of swap fee); cost = gas/priority + slippage | **10% of all rewards** |
| Entry gate | 600 pools scanned → 17 candidates → **0 cleared** (needs 24h fee ≥ 2.5× round-trip cost; best 1.36×) + antirug fail-closed (top-10 ≤25%, mint/freeze revoked) + vol guard | none visible; `maxTotalCost`/`minPnl` only, rest delegated to the LLM agent |
| Risk controls | TP +5%, SL −8%, max age 24 h, max 3 positions, 1.8 SOL/position cap, 168 h pool bench, denylist, 0.15 SOL breaker | `riskScore: HIGH`, 6 flags, **no IL guard** |
| Cadence | 20-min scans; **0 entries in 6 days** | ~2.5 positions/day, 110 lifetime |
| Track record | 7 trades, 6W/1L; book +$43 but chain 0.77 SOL below book | fee $254.88 lifetime, **net −$162.03 (−23%)** |
| Characteristic failure | guard + capital: no trades, dangling book | over-rotation: fees eaten by token-price decay |
| Transparency | logs + DB + chain, drift detector volunteers bad news | position-level API matches chain exactly; copy-fee totals unverifiable |

## 4. The framing that landed

- Name the **opposite failure modes** rather than ranking the products: ours is frozen by its own
  discipline (and by an operator manual LP colliding with the sizing guard), theirs moves 2.5×/day and
  gives the fees back as IL. "Masalah kita kebalikan dia" is the useful sentence.
- Steal the right thing: Krystal's **position-level transparency + per-position cost accounting**
  (initDep / pnl / age / pool / fee per position) is the analogue of our drift detector and is what
  would have surfaced the book-vs-chain gap earlier. Do **not** steal the 10% performance fee or the
  copy-vault mechanic (`copyCount: 406`, claimed copy fees $16,796 — backend accounting, unverifiable).
- End on the concrete lever for our side (e.g. `LIVE_CAPITAL_SOL ≤ wallet − 0.15` via the deploy path),
  stated as the next action — not as a question.
