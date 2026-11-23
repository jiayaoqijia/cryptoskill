# Entry location & trigger playbook (liquid majors under the DD threshold)

Companion to `prospective-entry-vetting.md` (which gates small-cap *candidates*) and
`theme-concentration-and-unlock-timing.md` (unlocks as entry timing). This file answers the question that
comes *after* a screener verdict: **"set up entrynya sekarang kurang ya?"** — i.e. the asset is fine, is the
*price* fine?

Worked 04 Okt 2026 on ZRO (LayerZero). The daily deep-dive had just printed "7/10, di bawah ambang 8/10 —
katalis tanpa tanggal keras + cliff unlock 25,71jt ZRO", and the user replied with exactly that question.

## The verdict shape: a good chart is not a good entry

A liquid major can have a real narrative and strong structure and still be a **bad entry at the ask**.
ZRO: narrative real (Citadel Securities / ARK / Tether / DTCC / ICE around the "Zero" L1; fee switch →
protocol fees routed to ZRO buyback+burn), structure strong (pos90 90%, vol 7d÷30d 1,79x) — correct answer
was still **watchlist, bukan buy**.

Say that in line one, then show why.

## 1. Compute the location from daily candles

`Binance klines` direct (`https://api.binance.com/api/v3/klines?symbol=<SYM>USDT&interval=1d&limit=250` via
urllib) is a clean path when CoinGecko 429s or the symbol bucket recorded the pair as missing — both happen
in this environment's daily script. Print, do not eyeball:

| measure | ZRO @ 04 Okt 2026 | how |
|---|---|---|
| last / 7d / 30d / 90d | $2,00 / +21,8% / +93% / +97% | closes |
| position in 90d range | 90% (low $0,92 → high $2,146 set 3 Okt) | last vs min/max |
| MA20 / MA50 / MA200 | $1,4665 / $1,2072 / $1,2431 → price **36% above MA20** | mean of closes |
| vol 7d ÷ 30d | 1,79x | mean quote volume |
| drawdown from range high | −22,7% | max high vs last |

**Read volume direction together with price.** Here the last three sessions added volume (24,8M → 28,5M →
36,4M) while price stalled under $2,146: rising volume into a ceiling after +93%/30d is a distribution
candidate, not confirmation. Volume expansion only confirms when price is making progress.

## 2. The three questions that actually decide it

1. **R:R at the ask.** The SL must sit below *structure* (the breakout base), never at a round number. ZRO:
   nearest resistance $2,146 = **+7%** from the ask, while the logical SL under the 2 Okt base is **−14%**.
   A trade whose stop is twice as far as its first target is a chase regardless of the story — print both
   percentages next to each other and the answer is self-evident.
2. **A dated trigger.** "Zero/ATLAS mainnet fall–late 2026" is hope: with no date there is no way to be wrong
   on time, so there is no entry trigger. No date ⇒ no trigger ⇒ no entry today, however real the narrative.
3. **A dated supply event inside the plan window.** ZRO: 25,71M cliff on **20 Okt** (≈$40,6M ≈ 7,3% of mcap;
   13,42M to strategic partners, 10,63M to core contributors) — 16 days out. An upcoming unlock is not a
   reason to stay flat forever: it is the *dated chance to buy cheaper*, and often the only dated fact in the
   whole thesis. Verify the date/size against an unlock calendar (Tokenomist-style lists, gate.com/coingabbar
   roundups) rather than repeating the screener's number.

## 3. Always close with a numbered trigger playbook, never a bare "tunggu"

| | Trigger | Execution |
|---|---|---|
| **A** | Pullback-retest of the structural base ($1,72–1,78) on drying volume, entry on the reclaim ($1,85) | SL <$1,62, T1 $2,14, T2 $2,40–2,59 → R:R ≈2,5–3x. Primary path |
| **B** | Daily close above the range high on volume above the prior sessions' average | SL under the breakout, **half size** — the unlock sits inside the window |
| **C** | Post-unlock absorption (unlock date +3–5 days): price holds above pre-unlock support on normal volume | Real demand absorbed the supply ⇒ re-rate leg; loses it ⇒ fall back to MA20 |
| **D** | Hard-catalyst date (mainnet/listing/fee event with a calendar date) | Only a dated event converts narrative into trigger |

## 4. "Dulu skornya rendah, sekarang katanya momentum — beli nggak?"

Pertanyaan ini punya dua jawaban yang berbeda dan harus dipisah eksplisit, karena skor screener lama
mengukur **nilai tesis**, bukan **nilai entry**, dan momentum bukan sumbu yang sama.

1. **Ulangi dasar skornya dulu.** Skor rendah biasanya berasal dari satu gate keras: revenue yang tidak
   sampai ke token, atau overhang supply. Sebut gate itu dengan angkanya, lalu cek apakah faktanya berubah
   — dan kalau berubah, katakan skornya perlu di-update. Contoh perbaikan struktural yang sah: supply
   beredar sudah ~83% dari total dan FDV/mcap cuma ~1,2x berarti fase unlock besar sudah lewat; itu
   alasan nyata untuk menaikkan skor, bukan karena harganya naik.
2. **Jangan hitung P/S untuk chain yang fee-nya tidak jatuh ke holder.** Kalau fee jaringan masuk ke
   validator/burn dan holder token hanya dapat nilai dari inflasi staking, rasio fee÷mcap tidak berlaku —
   tulis "tidak aplikabel" dan ganti dengan pertanyaan yang benar: apa yang menahan harga kalau narasi
   berhenti? Angka fee harian yang kecil (ratusan dolar) adalah jawabannya: tidak ada.
3. **Ukur kualitas momentum, bukan cuma besarnya.** Ekspansi volume 7d vs 30d vs 90d memisahkan rally
   luas dari spike tipis. Funding datar/negatif saat harga naik = dipimpin spot (sehat, long belum padat);
   OI melonjak dalam sehari di harga tinggi = leverage baru masuk, yang memperpendek umur trade.
4. **Sizing diambil dari kas, bukan dari menambah beta.** Kalau kas 0% dan koin yang ditanya sekorelasi
   dengan sleeve terbesar, jawabannya bukan "beli 3–5% sekarang" tapi "bentuk kas dulu, baru trade ini".
   Sebut juga kalau trade momentum yang setara sudah ada di porto — menambah nama keempat yang bergerak
   searah bukan diversifikasi.
5. **Tutup dengan invalidasi yang bisa dieksekusi**: close harian di bawah MA/time frame yang dipakai
   untuk stop, volume turun di bawah rata 30 hari, atau dominasi BTC menembus level yang membalik regime.

## 5. Sizing context closes the answer

The user was already 41% in ONDO against a 12% cap, so any add here is capped small and split into tranches.
An entry inside an already-concentrated narrative is not a fresh bet — say the concentration number in the
same breath as the entry plan, and end with the mandatory one-line regime (BTC.D / ETH.D / USDT.D / breadth /
median alt vs BTC), never with "mau gw buatkan?".
