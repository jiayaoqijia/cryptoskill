# Multi-Step Workflows

## Idle fund analysis — check and subscribe

"我有多少闲置资金可以赚币？"

1. `okx --profile live account asset-balance <ccy>` → idle funds in funding account
2. `okx --profile live account balance <ccy>` → idle funds in trading account
3. `okx --profile live earn savings balance <ccy>` → already in earn
4. `okx --profile live earn savings rate-history --ccy <ccy> --limit 1 --json` → current `rate` (threshold) and `lendingRate` (actual yield)
→ summarize idle funds and suggest subscribing if lendingRate is acceptable

---

## Subscribe earn then verify

"帮我把资金账户里的 1000 USDT 申购赚币"

1. Run in parallel:
   - `okx --profile live account asset-balance USDT` → verify balance ≥ 1000
   - `okx --profile live earn savings rate-history --ccy USDT --limit 1 --json` → current APY
2. Show confirmation summary (see savings-commands.md), wait for user confirmation
3. `okx --profile live earn savings purchase --ccy USDT --amt 1000`
4. Run in parallel to verify:
   - `okx --profile live earn savings balance USDT --json` → confirm position updated
   - `okx --profile live earn savings rate-history --ccy USDT --limit 1 --json` → show current lendingRate in position summary

---

## Redeem earn and transfer to trading account

"赎回我的 USDT 赚币，划转到交易账户"

1. `okx --profile live earn savings balance USDT` → check redeemable amount; show summary, wait for confirmation
2. `okx --profile live earn savings redeem --ccy USDT --amt <amt>`
3. _(Optional — requires **Withdraw** permission on the API key)_
   `okx --profile live account transfer --ccy USDT --amt <amt> --from 18 --to 6` (CLI account type IDs: 18=funding, 6=trading)

   If step 3 fails with a permission error, inform the user that their API key does not have Withdraw permission and they should complete the transfer manually in the OKX app.

---

## On-chain earn — subscribe with balance check

"帮我申购 ETH 链上赚币"

1. `okx --profile live account asset-balance ETH` → verify available balance
2. `okx --profile live earn onchain offers --ccy ETH` → show products, compare APY; show summary with risk disclaimer, wait for confirmation
3. `okx --profile live earn onchain purchase --productId <id> --ccy ETH --amt <amt>`
4. `okx --profile live earn onchain orders` → confirm order created

---

## DCD — Browse products with live spot price

"看看双币赢产品" / "看看BTC双币赢"

When user does **not** specify a currency pair, run in parallel:

```bash
okx --profile live earn dcd pairs                                              # supported pairs
okx --profile live market ticker BTC-USDT                                     # spot price
okx --profile live earn dcd products --baseCcy BTC --quoteCcy USDT --optType <C|P>  # default BTC-USDT
```

- Show BTC-USDT as default result
- After table, briefly mention up to 3 other available pairs (e.g. ETH-USDT, XRP-USDT) and ask if the user wants to view them. Respond in the user's language.

When user **specifies** a currency (e.g. "BTC高卖"), run ALL three in parallel **before rendering the table**:

```bash
okx --profile live market ticker {baseCcy}-USDT               # 1. Spot price (MUST)
okx --profile live account asset-balance {ccy}                # 2. Balance (MUST): CALL→baseCcy, PUT→quoteCcy
okx --profile live earn dcd products --baseCcy {baseCcy} --quoteCcy {quoteCcy} --optType {C|P} --json  # 3. Products
```

> ⚠️ Do NOT render the product table until all three are complete. Show spot price and balance above the table.
>
> If balance query fails (e.g. 401 / no credentials): show the product table anyway with spot price, omit the balance line, and note that balance check requires API credentials. Respond in the user's language.

Cross-skill: `okx-cex-market` for spot price, `okx-cex-portfolio` for balance if needed.

---

## DCD — Subscribe (quote-and-buy)

"我想申购高卖BTC，5%的价差，7天以内" / "帮我买这个双币产品"

1. Run parallel pre-display fetch (spot price + balance + products) as above
2. Show product table with ↑X.XX% / ↓X.XX% (2 decimal places) relative to spot, reference APR, term
3. Explain settlement scenarios **before** user selects — fill in ALL placeholders with real values. Respond in the user's language. Example structure (CALL / 高卖):

   ```
   You invest {sz} {notionalCcy} at target price ${strike}:

   ✅ Expiry price < ${strike} (not triggered — not sold):
      Receive {sz} × (1 + yield rate) {baseCcy}

   ⚠️ Expiry price ≥ ${strike} (triggered — sold at target price):
      Receive {sz} × {strike} × (1 + yield rate) {quoteCcy}
      Both principal and yield convert to {quoteCcy}

   The above APR is indicative; actual yield is locked at quote execution.
   ```

4. After user selects product and confirms amount, ask **once** whether they want to confirm the quote before placing, or place immediately. Quotes expire in 30 seconds, so place-immediately is recommended. Respond in the user's language.

   **Path A — Place immediately (default/recommended):**
   - Execute `earn dcd quote-and-buy` immediately, no extra confirmation step.

   **Path B — Preview quote first:**
   1. `earn dcd quote --productId ... --sz ... --notionalCcy ...`
   2. Show `annualizedYield`, `absYield`, `idxPx`, `validUntil` (quote expires in 30s)
   3. Explicitly warn the user the quote expires at `{validUntil}` and execution will be immediate upon confirmation.
   4. User confirms → `earn dcd buy --quoteId <quoteId>`
   5. If quote expired (HTTP 500): re-fetch quote, show new details, wait for confirmation again.

   > This confirmation flow applies to the **first order only**. If user has already said "just buy", skip to Path A for subsequent orders.

5. After `quote-and-buy`: wait 3–5 seconds, then query `earn dcd orders` to confirm. Show locked-in APR and order state.

---

## DCD — Early redemption (two-phase)

"提前赎回第1个订单"

This is the **only DCD WRITE operation requiring explicit user confirmation**.

**Phase 1 — Preview (indicative):**

1. `okx --profile live earn dcd redeem-quote --ordId <id>`
2. Show `redeemSz`, `redeemCcy`, `termRate` (positive = gain, negative = loss)
3. Explicitly state (in user's language) that the above figures are indicative — actual redemption amount is based on the live quote at confirmation time.
4. Wait for user confirmation

**Phase 2 — Execute (after confirmation):**

5. Immediately run `okx --profile live earn dcd redeem-execute --ordId <id>`
   - Internally re-fetches a fresh quote and executes — do NOT reuse Phase 1 quoteId
6. Wait 3–5 seconds, then query `earn dcd orders --ordId <id> --json` to confirm. Show the estimated settlement time from the order response (field: `estSettlementTime` or equivalent) as the expected arrival time. Respond in the user's language.

---

## DCD — Cross-skill: target-price sell workflow

"我想在72000卖出BTC"

1. `okx-cex-market` `okx --profile live market ticker BTC-USDT`
2. `okx --profile live earn dcd products --baseCcy BTC --quoteCcy USDT --optType C --strikeNear 72000`
   → explain CALL mechanics, show table, guide user to select term
3. `okx --profile live earn dcd quote-and-buy --productId <id> --sz <sz> --notionalCcy BTC`
