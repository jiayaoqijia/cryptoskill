# Recon app SPA + docs tanpa connect wallet (kasus: Liquidity Ladder, 29 Sep 2026)

Dipakai saat user nempel post promo tool DeFi dan situsnya **SPA kosong** (HTML cuma `<div id="root">`),
nggak ada halaman docs/fee/security yang bisa dibaca, dan nggak ada di DefiLlama. Semua fakta biaya,
chain, referral, dan permukaan approval biasanya ada di **bundle JS-nya** — tanpa connect wallet,
tanpa bayar, tanpa login.

## 1. Homepage kosong → langsung ke bundle

```bash
curl -sL -m 30 -A "Mozilla/5.0" "https://<site>/" -o site.html   # cek: body cuma #root + <script src=/assets/index-*.js>
curl -sL -m 60 -A "Mozilla/5.0" "https://<site>/assets/index-XXXX.js" -o app.js   # biasanya 1–3 MB
```

Catatan harness: one-liner grep raksasa (banyak `for` + `grep -oE` inline) **ditolak** dengan
"command parser limit or malformed executable payload". Jangan ulang inline — `write_file` dulu
script Python ke `/tmp/grep_app.py`, lalu jalankan `python3 /tmp/grep_app.py`. Pola ini jauh lebih
enak buat bundle 2 MB dan hasilnya bisa di-print terstruktur.

## 2. Urutan grep yang paling menghasilkan (dari bundle)

1. **Host docs** — regex `https?://[a-z0-9.-]*(docs|gitbook)[a-z0-9.-]*`. Di kasus ini ketemu
   `<project>-docs.vercel.app` **di dalam bundle**, padahal situs utamanya nggak nge-link docs sama
   sekali. Habis itu tetap coba `<docs-host>/llms.txt` (404 di kasus ini — coba dulu, kalau 404 lanjut
   crawl halaman `/`, `/faq`, `/networks`, `/wallet`, `/free`, `/create`, `/manage`, `/dashboard`).
2. **Peta API** — `["'`]/(?:api|v1|v2)/[a-zA-Z0-9_/-]+` → daftar endpoint nyata
   (`/api/zap/prepare-v4-uni`, `/api/zap/quote`, `/api/migrate/health`, `/api/flip/*`).
   Endpoint **`*/health` biasanya keyless**: `GET /api/zap/health` →
   `{"enabled":true,"supported_chains":[1,56,4663,8453]}`; `GET /api/migrate/health` →
   `{"enabled":false}`. Ini cara paling murah dapat (a) daftar chain yang aktif, (b) fitur yang
   dijual di post tapi sedang **mati** — di kasus ini "Migrate" yang dipuji postnya.
   Endpoint config lain balas `{"detail":"Not authenticated"}` → jangan dipaksa.
3. **Fee** — cari `fee_bips`, `ladder_fee_bips`, `platformFee`, `serviceFee`, dan string i18n
   ber-placeholder: `"zap.ladderFee.label": "Ladder fee ({rate})"`,
   `"Charged by the Zap contract on what the…"`. Nilai rate-nya datang dari API
   (`chains[].ladder_fee_bips`), tapi **keberadaan** fee + siapa pemungutnya (kontrak Zap mereka)
   kebaca dari sini. Bundle biasanya bawa **seluruh JSON i18n (EN+RU)** → teks UI/disclaimer paling
   jujur yang bisa kita dapat tanpa akun.
4. **Referral / monetisasi** — hitung `referr` (kasus ini **111 hit**) dan baca string-nya:
   `"your share of ladder fees from the people you invite"`, panel admin `owed/paid → "Owed to
   referrers"`. Artinya: **app bayar referrer dari fee user**. Ini bukti monetisasi promotor
   walau post-nya nggak punya link `?r=` — cukup dengan invite code (versi berbayar sering
   invite-gated). Angkanya masuk laporan.
5. **Custody / approval** — `permit2|Permit2` (hitung), `approval`, `wagmi|viem`, `walletconnect`,
   `rainbowkit` → non-custodial standar. Plus cari string peringatan mereka sendiri
   (`"do not approve this in your wallet"`) — itu tanda tim paham attack surface, layak dikutip.
   Alamat kontrak `0x[a-fA-F0-9]{40}`: cocokkan yang familiar — kasus ini `0x6131b5fa…337b5` =
   **KyberSwap MetaAggregationRouterV2**, jadi swap dirouting ke aggregator pihak ketiga
   (dua fee bertumpuk: fee aggregator + fee platform).
6. **Chain & RPC** — `chainId`, nama network, dan host RPC (`*-mainnet.g.alchemy.com`,
   `rpc.<x>.com`) → cross-check ke halaman docs "Networks". Berguna buat nulis tabel chain/DEX
   dan nandain chain yang **poolnya tipis** (biasanya justru itu yang paling dipromosikan).
7. **Default user settings** — `defaultSlippage`, `addliqSlippagePct`, `maxPriceImpact`,
   `swapRetryImpactMode` → dipakai buat menilai seberapa agresif default-nya.

## 3. Docs-nya sering bukan bahasa Inggris

Kasus ini docs-nya default **Rusia** (`Введение — BNB Liquidity Ladder`; halaman `/ru/*`: create,
manage, zap, networks, wallet, free, faq, dashboard). Ambil semua halaman, buang tag, lalu filter
kalimat yang mengandung `fee|комисс|audit|approv|network|free|сеть`. **Tabel fee-nya justru ada di
halaman "Free version"**, bukan di FAQ — dan di situ ketemu biaya yang nggak disebut promotor
(swap 0,5%; Zap In 0,1%; Create dua-sisi biasa 0% fee platform) plus disclaimer wallet built-in
(password nggak bisa di-reset, "as is, no liability").

## 4. Yang dilaporkan dari hasil recon ini

- Tabel fee **per aksi** + layer-multiply (fee platform + fee aggregator + gas + fee pool),
  dibandingkan ke target harian yang promotor sebut sendiri (kasus: 0,274%/hari → satu round trip
  0,6% = >2 hari target).
- Tabel chain/DEX per chain, dan catatan chain mana yang poolnya tipis.
- Sumber bukti PnL promotor: kalau kartu di screenshot **cocok dengan UI produk** yang sedang
  diulas (kasus: `Cumulative PnL` + `Open Positions … in 3 ladders` = kartu dashboard Ladder),
  tulis eksplisit "buktinya dari UI tool yang dipromosikan, bukan explorer" → statusnya
  **belum terverifikasi** (nggak ada wallet address), bukan "terbukti bohong".
- Cek aritmetika internal screenshot: jumlah W+L vs jumlah trade (kasus: 913+159 = 1.072 vs
  klaim 1.622 trade) dan eksposur terbuka vs modal yang diklaim (kasus: `Open Invested $2.185`
  vs "starting with $1.000") — inkonsistensi itu temuan, bukan detail teknis.
- Status fitur per tanggal cek dari `/health` (fitur yang dijual bisa sedang `enabled:false`).

## 5. Batas yang harus disebut

- Alamat kontrak pemungut fee (Zap) sering **tidak ada di bundle** — di backend. Catat sebagai
  lubang ("perlu ambil dari tx approve kalau nanti benar-benar nyoba"), jangan ditebak.
- Bundle ≠ perilaku on-chain: semua yang kebaca dari sini tetap **klaim vendor** sampai ada tx.
- Screenshot post yang isinya chart platform lain (mis. GMGN) tetap harus ditranskrip apa adanya:
  di kasus ini 4 panel chart menunjukkan 4 token meme persis di **−90,50%±0,2%** dari ATH, yang
  justru membuktikan rung bawah strategi = nyemplung ke koin yang sudah jatuh 90%.
