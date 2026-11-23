# Keyless Solana wallet/token state + tx forensics (public RPC)

Use when the user says "cek wallet gw", "isi dompet ini apa", "kemana duitnya pergi", or when you must
verify a fill / a position on-chain but have no Helius key, or when the DAS path in
`onchain-analytics` is unavailable. Built + tested 30 Sep 2026 against a real user wallet:
reconstructed a buy of 171,62 STONK for 0,4033 SOL (effective $0,2803 vs market $0,2750–0,2765,
friction ~1,5–2%) **and** the batch funding transfer behind it.

## Endpoint ladder (keyless)

```
https://api.mainnet-beta.solana.com
https://solana-rpc.publicnode.com
https://rpc.ankr.com/solana
https://solana.api.onfinality.io/public
```

Wrap every call: POST the JSON-RPC body to each URL in turn, `sleep ~0.4s` between attempts, return the
first response containing `result`. One public endpoint flaking or 429-ing must not fail the script.
Fine for one or a few wallets — **not** for whale enumeration (use DAS/Helius there).

## The four calls that answer almost everything

1. `getBalance [WALLET]` → lamports / 1e9 = SOL.
2. `getTokenAccountsByOwner`, **twice**:
   - `{programId: "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"}` — classic SPL
   - `{programId: "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"}` — **Token-2022**

   **Query both.** Reward/dividend memecoins (StonkFun `reward` mode) and xStocks (NVDAx, GLDX, SPYx)
   are Token-2022 with a transfer-fee extension and live outside the classic program — skipping the
   second call produces the false conclusion "the wallet is empty".
   For one known mint, filter instead: `[WALLET, {mint}, {encoding: "jsonParsed"}]` — far cheaper.
   Amounts live at `account.data.parsed.info.tokenAmount.uiAmountString` (+ `decimals`).
3. `getSignaturesForAddress [WALLET, {limit: N}]` → `signature`, `slot`, `blockTime` (epoch, UTC),
   `err`. Report blockTime in UTC **and** the user's timezone (this user: WIB = UTC+7).
4. `getTransaction [sig, {encoding: "jsonParsed", maxSupportedTransactionVersion: 0}]`.

## Decoding one transaction

- **SOL delta for the wallet**: its index in `transaction.message.accountKeys`, then
  `(meta.postBalances[i] - meta.preBalances[i]) / 1e9`. Index 0 is the fee payer.
- **Token deltas**: walk `meta.preTokenBalances` / `meta.postTokenBalances`, keep `owner == WALLET`,
  diff `uiTokenAmount.uiAmountString` per mint. A mint only in POST = received; only in PRE = sent
  away. Works for Token-2022 too. This is how you separate a buy from a sell.
- **Fee**: `meta.fee` in lamports — subtract it before calling the remainder "spent on the token".
- **Which program ran**: `message.instructions[].programId` + `meta.logMessages` (`Instruction: Swap…`).
  Do **not** name the trading venue from a log line alone; report the swap and let the fee math imply
  the venue, or say it is undetermined.
- **Batch fan-out**: one tx can pay several wallets. Loop **all** accountKeys and print every delta over
  a threshold. A sender at `−1,318 SOL` with `+0,416 / +0,799 / +0,104` to three recipients is a
  dispersal/batch payout — describe it as such, and never infer the sender's identity from one address.

## Effective fill price + friction (post-purchase check)

```
effective_price = (SOL_spent × SOL_usd) / tokens_received     # exclude meta.fee from SOL_spent
friction_%      = effective_price / market_price_at_that_minute − 1
```

Report: paid X SOL → received Y tokens → effective $Z vs market $M, friction ~1–2% (platform fee +
slippage). Friction above ~3% on a small ticket means a thin pool or a sandwich. Then state the
consequence in the user's terms: if the fill is above the planned entry zone, keep the cut level where
the plan put it and quote the risk in $ from *their* entry.

## Print discipline

Print lamport-accurate numbers and full-precision token quantities (`decimals`-aware) — never round a
token amount you are about to derive a risk level from. Identify unknown dust mints with
`gmgn-cli token info --chain sol --address <mint> --raw` (then `sleep 5`) instead of guessing a symbol.
