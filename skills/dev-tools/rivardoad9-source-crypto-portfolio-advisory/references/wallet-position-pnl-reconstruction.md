# Reconstructing a wallet's position + PnL in one token (keyless)

Companion to `solana-keyless-rpc-forensics.md` (endpoint ladder, single-tx decoding, fill-price/friction).
This file covers the **multi-leg** case: the user says "gw udah beli, profit nih — analisa" and you must
state their real entry, exit and PnL. Built + verified 1 Oct 2026 on a live wallet.

## Why this path exists

`gmgn-cli portfolio holdings` is a **critical-auth** command (needs `GMGN_PRIVATE_KEY`). When that key is not
configured, do **not** answer "the position can't be checked" — reconstruct it from public RPC. It answers
the same question with no key, and this user treats chain-verified numbers as the stronger evidence anyway
("selalu verifikasi wallet di chain, jangan cuma percaya buku engine / buku engine bisa drift").

## Run it

```bash
python3 ~/.hermes/skills/research/crypto-portfolio-advisory/scripts/solana_wallet_token_pnl.py \
  <WALLET> <MINT> --sol-usd 117.67 --price-usd 0.00045792 --limit 40
```

Self-contained (urllib only). Detects the wallet's ATA in both token programs, prints every leg, then the
averages and the PnL table. Get `--price-usd` from `gmgn-cli token info` and `--sol-usd` from the pool
(`quote_reserve_value / quote_reserve`) or CoinGecko — never from memory.

## Method

1. `getTokenAccountsByOwner` (both token programs, mint-filtered) → the wallet's ATA pubkey(s). **Do this
   first**; attribution depends on it.
2. `getSignaturesForAddress` (limit ~40) → `getTransaction` per signature.
3. Per tx, per **accountIndex** in `pre/postTokenBalances` for that mint:
   `delta = post.get(i, 0) − pre.get(i, 0)`; keep the row only when the account owner is the wallet or its
   ATA. Positive delta = buy, negative = sell; the wallet's own SOL delta is that leg's cash side.
4. Aggregate: `avg_entry = ΣSOL_out / Σtokens_in` · `realized = ΣSOL_in − tokens_out × avg_entry` ·
   `open = Σtokens_in − Σtokens_out` · `unrealized = open × (market − avg_entry)`.

**Compute in SOL, convert to USD exactly ONCE** with a dated SOL/USD quote. Converting each leg with a
remembered rate is how a correct SOL figure gets printed as a wrong USD one — that shipped once in this
session: avg entry 3,2915e-06 SOL printed as "$0,00000329" while the real value was $0,00038731, which
inflated the "gain vs entry" line by 100×. Print sub-$0,001 values in scientific notation.

## Pitfalls

- **Never diff `sum(post.values()) − sum(pre.values())`.** When the venue vault and the wallet trade
  accountIndex slots between pre and post, the two dicts have different key sets and the difference comes out
  `+0.00` for EVERY transaction — a wallet that obviously traded looks untouched. Pair per index, then
  filter by owner. (This is the bug the script exists to prevent.)
- **The huge balance beside the user's is the venue vault, not the user.** Tens of millions of tokens (curve
  reserve / DLMM pool / vault) sit in the same tx as the wallet's own thousands. Attribute by owner/ATA,
  never by size.
- **Public RPC 429s in bursts** on 20+ back-to-back `getTransaction` calls. Rotate the endpoint ladder with
  2s×attempt backoff and `sleep ~1s` between successful calls. A 429 is not "no history".
- **`blockTime` is UTC** — report UTC *and* WIB for this user.
- **Skip failed txs** (`err` set, often `meta = null`) instead of crashing.
- **State the sample window.** `limit: 40` is minutes-to-hours for an active wallet: say "in the last N
  signatures", never "all his trades". Widen or page with `before` if the mint is older.
- **Confirm the wallet identity.** If the address came from memory rather than from the user, name the
  address you actually read and invite correction — analysing the wrong wallet produces a confident report
  about someone else's position.

## Worked example (HOURS, 1 Oct 2026, wallet A8XDKU…XeYo)

Four legs inside a 40-signature window, all within 8 minutes:

| leg | tokens | SOL | balance after |
|---|---|---|---|
| 19:00 BUY | +36.742,06 | −0,103739 | 36.742,06 |
| 19:01 BUY | +56.510,50 | −0,203199 | 93.252,57 |
| 19:05 SELL | −9.325,25 | +0,045064 | 83.927,32 |
| 19:07 SELL | −8.392,73 | +0,035353 | 75.534,59 |

→ avg entry **3,2915e-06 SOL = $0,00038731**; avg exit 4,5387e-06 SOL (the partial sells were *above* the
then-market — worth saying out loud); open 75.534,59 tokens; position $34,59 on $36,12 cost plus $9,46
realized = **PnL +$7,93 (+22,0%)** at $0,00045792 with SOL $117,67.

Report shape that landed: leg list → avg entry / avg exit → position size in $ → then a table of
price → mcap → position value → total PnL for **entry**, a **partial-sell level**, the **ATH**, a **stretch
target**, and the **stop**. Every level row carries the PnL it implies; the stop row sits at the wallet's own
average entry when the goal is "cannot become a loss". Scale the advice to the position — a $36 ticket gets a
ladder plus one line of rationale, not a thesis essay.
