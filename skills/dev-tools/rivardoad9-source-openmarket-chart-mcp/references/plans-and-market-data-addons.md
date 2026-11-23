# Plan vs market-data add-on (jawaban buat "bedanya free plan sama ini apa")

Diverifikasi dari halaman live `openmarket.xyz/chart/plus`. Harga bisa berubah — buka halaman itu dan
baca ulang sebelum menyebut angka.

## Dua sumbu yang beda dan sering ketuker

| Sumbu | Isi | Yang diangkat |
|---|---|---|
| **Plan** (charting) | batas platform: indikator per pane, jumlah chart/workspace, alert, kedalaman heatmap, device | batas plan — dan lewat MCP: window candle (`tier_forbidden`) + batas geometri chart |
| **Market-data add-on** | lisensi feed dari bursa (CME Group: CME · CBOT · NYMEX · COMEX), dibeli terpisah dari plan | cuma real-time vs delay untuk 4 bursa itu |

**Add-on tidak mengangkat satu pun batas plan, dan plan tidak membuat data CME jadi real-time.**
Kalau user nanya soal langganan, tentukan dulu sumbu mana yang dia lihat, lalu jawab sumbu itu.

## Angka plan

| | Free $0 | Plus $29/bln ($348/tahun) |
|---|---|---|
| Indikator per chart | 3 | 10 |
| Private scripts | 100 | 500 |
| Heatmap depth | Normal | Maximum |
| Multichart | 1 | 16 |
| Sesi / device | 1 | 5 |
| Price alert | 100 | 500 |
| Indicator alert | 2 | 25 |
| Widget / layout | 3 | 10 |
| Workspace | 10 | 50 |

FAQ halaman itu soal Free: "every chart type on every exchange" — semua bursa keliatan, yang bukan
real-time cuma feed-nya. Kripto tidak butuh lisensi.

## Add-on data

- **Real-time L1** = top of book. **Real-time depth (L2)** = order book penuh. Ini persis pembagian
  produk CME sendiri (trades, top of book, market depth).
- Harga di app (IDR, ~17,9rb/USD saat dicek): L1 Rp 179.000/bln ≈ **$10**, L2 Rp 1.090.000/bln ≈ **$61**.
  Halaman web nulis "from $7/mo" buat CME real-time. Pembanding wajar: TradingView memasang CME Group
  real-time $9,95/bln — bandingkan angkanya, jangan mengarang.
- Langganan bulanan auto-renew dari tanggal pembelian; sebut tanggal itu kalau user niatnya nyoba.
- Tanpa lisensi, data CME Group datang delay (aturan bursa, standar platform lain 10–15 menit).
  Angka delay persis OpenMarket tidak ditulis di halaman mereka — jangan mengarang, bilang "standarnya
  segitu di platform lain".

## Cara membingkai ke user (porto kecil)

- Untuk trading kripto: **nol manfaat** — feed kripto real-time sudah gratis (`api.binance.com`,
  `fapi.binance.com`) dan itu yang dipakai script kita.
- Yang dia kasih: futures CME (ES/NQ), kripto futures CME, WTI NYMEX, emas COMEX, obligasi CBOT — bahan
  baca makro, bukan alat entry alt.
- Kalibrasi biaya ke ukuran portonya: Rp 179.000/bln ≈ 0,8% nilai porto per bulan; Plus Rp 519.000/bln
  ≈ 2,3% per bulan (≈27%/tahun). Langganan yang lebih gede dari hasil trading dijawab dengan angka ini,
  bukan opini.
- Bookmap-style heatmap = jalur Plus, bukan add-on ini; alternatif gratis ada di skill
  `bookmap-liquidity-heatmap`.

## Pitfall

- Halaman plan menulis resolusi heatmap 4K juga di Free, tapi MCP-nya menolak `ORDERBOOK_HEATMAP` dengan
  `INTERNAL: heatmap4K requires plus tier`. Percayai refusal tool-nya untuk klaim kemampuan, dan sebut
  halaman plan sebagai klaim marketing — jangan janjikan fitur ke user berdasarkan tabel harga.
- Jangan jawab pertanyaan "bedanya apa" dengan mengutip harga saja: tanpa pemisahan plan vs add-on,
  user akan beli add-on untuk memecahkan batas plan (atau sebaliknya) dan salah belanja.
