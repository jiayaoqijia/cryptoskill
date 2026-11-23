# "Cariin gw CA dari <link>" — resolving a token's identifier

Companion to the platform-DD ladder, step 1–4. Use when the user drops a **project's own website** (not a
promo post) and asks for the contract address, usually because they intend to buy or to add it to a
tracker. Same treatment applies when a tipster hands over an "official CA".

## The answer is sometimes "there is no CA" — say it plainly

A project running its **own chain** (native L1 / PoW coin, Substrate-based, Bitcoin-like) has *native
accounts*, not an ERC-20/SPL contract. There is no contract address to find; anyone handing one over is
confused or lying. State that first, then hand over the identifiers that do exist — do not go hunting for
an address to satisfy the question.

**Fast test** (`api.coingecko.com/api/v3/coins/<id>?localization=false&tickers=true&market_data=true`):

- `platforms` = `{}` or `{"": ""}` ⇒ **no contract on any chain**. Native coin.
- `market_data` gives price / ATH / supply (`market_cap: 0` = supply unreported — say that, don't quote 0
  as a valuation).
- `tickers` = the complete venue list — usually the real constraint on what the user can even do.

## Worked case — Quantus / QTC (29 Sep 2026, user: "cariin gw CA dri ini https://www.quantus.com/")

| check | result |
|---|---|
| CoinGecko `platforms` | **empty** → no contract anywhere |
| categories | Layer 1 (L1), Proof of Work, Quantum-Resistant |
| supply | `market_cap: 0` (unreported), `max_supply` 21.000.000 |
| native address format | Substrate-style: **SS58 prefix 189** (e.g. the vesting pool `qzmviwoPJR19XovVwUYUoUKb2MoBygYgwYAevj5Br8JeunxW7`) or a bare 32-byte `0x…` AccountId; 12 decimals |
| explorers | `explorer.quantus.com` (official), `qtcscan.com` (third party; also explains the supply formula) |
| venues | **one**: SafeTrade `QUANTUS/USDT`, ~$1,1M/24h; price at/near ATH the same day; chain 20 days old, ~238 active accounts |
| ticker inconsistency | `qtc` (CoinGecko) / `QUAN` (explorer) / `QUANTUS/USDT` (exchange) — three names for one asset |
| DexScreener `search?q=QTC` and `q=quantus` | only **impostors**: a pump.fun token (~$4,4k 24h volume) and a "QUANTUS" on an EVM chain ($34k liquidity, $231 volume) |

## Checklist

1. Pull the CoinGecko record (above). `platforms` empty ⇒ native coin: report the **address format** for
   that chain family, the official explorer, and that the venue list is the only place to buy.
2. Run `api.dexscreener.com/latest/dex/search?q=<ticker>` **anyway**, and name the impostors you find —
   explicit addresses and volumes, so the user can never be talked into them. (Filter returned pairs by
   baseToken name/symbol; most hits are unrelated coins that merely match the ticker.)
3. Flag **ticker/name inconsistency across tools**. Resolving a token by ticker or by name instead of by
   chain + address is exactly how someone buys the fake.
4. If the docs mention a bridge or a wrapped version ("via NEAR intents", "coming soon"), say that the
   **bridged artifact** is what will eventually have a contract address — that is the thing to verify later,
   before any execution. Present it as a pending check, not a green light.
5. Read the liquidity reality out loud: one venue, thin book, price at/near ATH shortly after launch, small
   active-account count — and what that implies for size. Evidence that mattered here: the project's docs
   describe an open PoW distribution with a large premine, while the CEX book is thin enough that small
   sells move the price.
6. Deliverable shape: "no CA exists, and here is why" → the real identifier format → where to verify →
   the only venue → the impostor list → the size/liquidity caveat. Never hand over an address you did not
   tie to the project's own chain.
