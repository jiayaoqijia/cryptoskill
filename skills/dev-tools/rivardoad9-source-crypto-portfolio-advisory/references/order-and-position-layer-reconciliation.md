# Rekonsiliasi lapisan ORDER & posisi (bukan cuma daftar holdings)

Companion to `portfolio-state-reconciliation.md` (which reconciles the *holdings list* across memory /
watchdog / cron / vault) and `cash-target-and-book-wide-execution-verify.md`. This file covers the layer
that file misses: **posisi futures, open order, realized PnL, dan kas yang benar-benar bebas** — the
state that changes the moment the user acts between sessions.

**Trigger:** "trigger gw dah mulai bisa buy apa ya skrng", "skrng gw harus ngapain", "posisi gw masih
aman ga", or *any* question that assumes a plan written earlier is still the live plan.

## Kenapa ini wajib: 3 dari 4 asumsi salah (8 Okt 2026)

User tanya apa yang bisa dia beli sekarang berdasarkan trigger-nya. Yang ketemu setelah cek akun:

1. **Short ETH 150x sudah ditutup jam 16:43 WIB** (`REALIZED_PNL −2,549` + `COMMISSION −0,401` ≈
   **−$3,1**), dompet futures kosong. Rencana *hedge-accumulation* 0,31 ETH yang "belum dieksekusi"
   jadi **batal sendiri**. Tanpa cek ini, jawabannya akan menyuruh dia mengeksekusi rencana mati.
2. **Sudah ada limit order jalan**: `SOLUSDT BUY LIMIT 0,457 @ 109,25` — ini penjelasan dari
   "$49,93 ke-lock" yang muncul di output porto spot. Tanpa cek open order, saran "pasang limit di X"
   berisiko jadi order ganda, dan kehilangan fakta bahwa dia **sudah lebih sabar dari rencana aslinya**
   (order di 109,25 = di bawah zona T1 110–111 yang dia tulis sendiri).
3. **Tangga beli lebih besar dari kas.** Rencana tertulis $220 + $300 + $200 = **$720**; kas riil
   **$467,68** dan $49,93 di antaranya sudah ke-lock. Trigger pertama kena = cuma 2 dari 3 anak tangga
   yang bisa jalan. Resize (mis. $150/$150/$120 = $420, sisa sebagai buffer) harus diusulkan **sebelum**
   trigger kena, bukan sesudah.

## Perintah cek (read-only, sebelum menulis satu baris advis entry)

```python
fapi("/fapi/v3/positionRisk")            # abs(positionAmt) > 0 → amt, entryPrice, markPrice, leverage, marginType
fapi("/fapi/v2/balance")                 # balance / availableBalance per aset (kosong = dompet futures nol)
fapi("/fapi/v1/openOrders")              # order futures yang masih NEW
fapi("/fapi/v1/income", {"limit": 50})   # REALIZED_PNL · FUNDING_FEE · COMMISSION + timestamp
api("/api/v3/openOrders")                # order SPOT — limit buy yang duduk di bawah harga nongkrong di sini
```

Signing: HMAC-SHA256 atas query string yang **sudah** memuat `timestamp` + `recvWindow`, header
`X-MBX-APIKEY`. Helper yang sudah jalan ada di `scripts/position_plan_card.py`; kunci dibaca lewat
`binance_porto.py::load_keys()` — jangan hardcode, jangan cetak.

## Aturan

1. **`positionRisk` kosong = user sudah menutup semuanya.** Jangan menyimpulkan "posisi lu masih ada"
   dari catatan sesi sebelumnya. Sebutkan perubahannya sebagai kabar pertama, bukan sebagai catatan kaki.
2. **Cek open order sebelum mengusulkan level.** Laporkan bahwa order itu sudah ada dan di harga berapa.
3. **Rekonsiliasi ukuran tangga vs `availableBalance`.** Trigger yang totalnya melebihi kas bukan
   rencana, itu daftar keinginan — tunjukkan angkanya, usulkan ukuran baru.
4. **`/fapi/v1/income` adalah kebenaran biaya keputusan.** Pakai untuk menutup episode dengan angka.
   Di sini ±−$3,1 untuk menutup short yang liq-nya cuma 5,8% di atas harga = **keputusan bagus**, dan
   itu harus dikatakan sebagai penilaian, bukan cuma dilaporkan sebagai kerugian.
5. **Jawab pertanyaannya dalam bentuk tabel trigger**: `trigger | level | status | jarak %`, diurut dari
   yang paling dekat. Kalau tidak ada yang kena, **bilang "belum ada yang kena"** secara eksplisit —
   termasuk menolak permintaan implisit untuk beli di harga sekarang kalau harga masih di atas zona yang
   dia tetapkan sendiri ("beli SOL di 112,53 = di atas zona T1 lu sendiri 110–111").
6. **Sebut konsekuensi beta dari posisi yang sudah berubah.** Setelah short ditutup, buku jadi full long
   (β porto 1,51 → BTC −15% = porto −22,6%): nambah beli = nambah beta, bukan sekadar "beli murah".
7. **Tutup dengan satu aksi sabar yang konkret** ("biarkan order 109,25 duduk, jangan tambah limit baru,
   jangan ubah tangga sebelum BTC masuk 81,5k"), bukan daftar panjang.

8. **Order yang masih duduk itu leverage yang belum kena, bukan "posisi kosong".** `/fapi/v2/account`
   memberi tell satu baris: `totalOpenOrderInitialMargin > 0` padahal `totalPositionInitialMargin == 0`
   = tidak ada posisi, tapi ada order nangkring yang menarik margin. Cek `openOrders` sebelum bilang
   "dompet futures lu bersih". Lalu hitung konsekuensinya: tiap limit buy membawa notional — dua bid yang
   belum kelihatan di daftar posisi (total $249,62) lawan dompet $69,91 = **3,57x begitu kena**. User
   membaca "nggak ada posisi" sebagai "leverage gw udah nol", dan itu keliru selama order-nya hidup.

## Pitfalls

- **Rencana di disk tidak punya tanggal kedaluwarsa.** File `hedge_accum_plan.py` / `rebalance_plan.py`
  tetap terbaca rapi berhari-hari setelah isinya tidak relevan. Yang menentukan selalu state akun live.
- **Jangan campur angka porto spot dengan posisi futures** dalam satu tabel tanpa label — total spot
  ($1.274,45) dan dompet futures adalah dua kolom berbeda.
- **Verifikasi bila ada order berstatus parsial** (`origQty` vs `executedQty`): "sudah keisi sebagian"
  berbeda artinya dari "belum keisi" untuk rekomendasi berikutnya.
