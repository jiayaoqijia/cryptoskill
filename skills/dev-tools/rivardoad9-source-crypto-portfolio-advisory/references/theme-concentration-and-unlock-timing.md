# Theme concentration, unlock timing, fee-on-transfer sizing

Companion to `holdings-thesis-verification.md` (which covers supply structure per asset). Load when a
portfolio review adds **new picks inside a narrative that already has sleeves**, or when an unlock date
is being used to justify a hold. Worked 30 Sep 2026 (asked: "totally portofolio yg upside potensial,
kita ambil apa untuk skrg").

## 1. Theme concentration cap — count the bet, not the tickers

When several picks come out of one narrative scan (institutional leg + degen leg + momentum leg of the
same meta), they are **one bet placed three times**. Sum them, cap the sum, and print the cap next to the
allocation table so the user sees the real exposure.

Worked example — all four rows below were "different" recommendations in one narrative
(tokenized equities / stock-paired coins):

| Name | Role in the meta | Weight |
|---|---|---|
| ONDO | institutional leg (RWA issuer) | 12% |
| STONK | platform/equity leg (revenue → buyback+burn) | 8% |
| GP | degen leg (paired to a tokenized-gold xStock) | 4% |
| SI | momentum trade leg | 2% |
| **Cap** | **one meta ⇒ 26% ceiling** | 26% |

Say plainly: *"kalau meta-nya pecah, bocor bareng"* — and that the cap holds no matter how good the
story sounds. Distinct roles inside a meta do **not** diversify it; correlation is ~1 on unwind.

### Measure it, don't just assert it (the "diversifikasi atau konsentrasi?" question)

Pull daily venue klines for the held coins plus `BTCUSDT` (`/api/v3/klines?symbol=<SYM>USDT&interval=1d&limit=91`;
a token listed for less than the window has no full-window number — say which window you used), then compute:

```
betaᵢ      = cov(rᵢ, r_BTC) / var(r_BTC)
beta_porto = Σ wᵢ · betaᵢ
vol_porto  = √(Σᵢ Σⱼ wᵢ wⱼ ρᵢⱼ σᵢ σⱼ)        # pakai korelasi NYATA, bukan asumsi
rasio_div  = Σ wᵢ σᵢ ÷ vol_porto            # makin dekat 1, makin nggak ada gunanya nyebar
```

These three numbers are what answer the question. Reference run: three alts with betas 1,23–1,57 and
pairwise correlations 0,72–0,78 gave **rasio_div 1,12** (spreading across four assets cut the swing by
11%) and **beta_porto 1,44** (BTC −30% ⇒ book −43%). So the HHI that looks like "3,1 names" is one bet:
say that, and give the beta as the consequence, not the HHI. A fourth name whose correlation to BTC is
~±0,05 is the only real diversifier in the list — but price the escape too: a fat FDV/rev premium paid to
dodge beta can cancel the benefit.

### Kalau user yang nyusun bobotnya sendiri ("full power 30/30/40")

Proposal bobot dari user diperlakukan sebagai hipotesis yang harus diuji, bukan order. Tiga cek, urut:

1. **Cek kas dulu.** Tanpa USDT bebas, "bid" artinya **jual** sesuatu — dan itu pertanyaan yang beda dari
   "beli apa". Kalau cash ≈ 0, jawabannya trim nama paling lemah, bukan tambah nama baru.
2. **ρ pairwise, bukan label.** Hitung korelasi return harian antar kandidat (20–30 hari cukup). 0,88–0,91
   = satu posisi berkepala tiga: bilang "ini bukan diversifikasi, ini satu taruhan", lalu kasih β/ρ angkanya.
3. **Bobotnya dibalik nggak?** Bandingkan bobot usulan dengan kekuatan relatif terukur (7d/30d vs BTC,
   jarak ke EMA20/50 4h). Skema 30/30/40 yang menaruh 70% di dua nama terlemah adalah inverse of the signal:
   koreksi bobotnya, jangan cuma bilang "ok tapi hati-hati".

Kalau "full power" muncul beberapa menit setelah user setuju pegang cash, sebut kontradiksinya langsung
("tadi lu setuju bantalan cash, rencana ini ngabisin 100% dan semuanya korelasi 0,9") — jangan diam-diam
ikuti rencana barunya. Yang ditawarkan sebagai ganti: cash maks 50%, bobot urut kekuatan terukur,
masuk 3 tranche, stop per nama di bawah 30d low.

## 2. Unlock dates are entry timing, not only risk

Read the **next** unlock (Tokenomist/DefiLlama unlocks/CoinGecko tokenomics), not the last one, and split
the conclusion in two:

- Next cliff far away (months) ⇒ **structurally clean window to accumulate now**.
- Same date ⇒ **dated exit** ahead of the cliff.

ONDO worked example: last unlock 18 Jan 2026 was the remembered fact; the *next* is **18 Jan 2027
releasing 1,71B ≈ 35% of market cap**. Correct call: hold/add through Q4 (clean supply), trim before the
date — instead of treating ONDO as permanently overhung. A stale note holding the previous unlock
reads as present danger and produces the wrong verdict.

Cross-check the cliff against current float: "% of market cap" is the number that matters for price
impact, not the token count.

## 3. Fee-on-transfer / reward-tax coins inside a sleeve

Before an entry level is published for a pair-paired or reward-mode coin, pull its tax from the
**launchpad's own token record** (GMGN `token info` does not expose it):

```
round-trip tax = 2 × transferFee.bps / 10000        # charged in AND out
break-even     ≈ 2× the rate for small rates        # 300 bps → >+6,4% before slippage
```

300 bps + thin liquidity ($319–517k) ⇒ shrink the size, label it **swing, not scalp**, and never chase
green candles inside the BEP band. The same discipline applies to LP sleeves (exit cost floor) — see
`sizing-arithmetic.md` and `meteora-dlmm-lp-screening.md`.

## 4. Report shape for a full-portfolio upside review

1. Regime first, one line: is money rotating (majors flat/bleeding while themed alts run +30–50%/30d)
   or is it risk-off? Sizing follows from this, not from conviction.
2. Current sleeve-by-sleeve vs live data, with explicit **keep / trim / add** and the number that decided it.
3. New picks, each with role, weight, pair/reward config, entry zone, invalidation.
4. Explicit rejections with the disqualifying number (late-stage mcap, bridge friction, tax controversy,
   lottery % moves).
5. Guardrails: theme cap, cash floor, dated exits (unlock cliffs).
6. Vault note `… (DD Mon YYYY).md` + `bacaan rule-based, bukan saran investasi`.

A portfolio review here is a **plan with dates and levels**, not a list of tickers.
