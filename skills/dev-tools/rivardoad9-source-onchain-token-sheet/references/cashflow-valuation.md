# Valuasi cash-flow (revenue) buat token protokol

Dipakai kalau user tanya "fair value berapa / undervalued atau overvalued" buat token yang punya revenue nyata (DEX, perp DEX, launchpad, aggregator, lending).

## Rumus

fair_price = harga_sekarang x (revenue_setahun x fair_multiple) / market_cap

fair_multiple = median_multiple_kategori x faktor_tren_revenue

Sumber revenue: DeFiLlama `/overview/fees?dataType=dailyRevenue&excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true`.
**Jumlahkan SEMUA entri satu keluarga protokol**, jangan ambil satu baris. Contoh: Hyperliquid Perps + Spot Orderbook + L1; Aerodrome Slipstream + V1; Meteora DLMM + DAMM V2 + DBC; Raydium AMM + LaunchLab; Jupiter Aggregator + Perp + Lend + DCA. Kalau cuma ambil satu baris, revenue-nya kelewat jauh.

## Median multiple pasar (diukur 12 Okt 2026, 61 protokol DeFi dengan mcap >= $80 juta)

- keseluruhan: median 23,4x, p25 12,2x, p75 45,8x
- Dexs 20,7x | Derivatives 23,3x | Launchpad 9,4x | DEX Aggregator 18,7x | Lending 28,0x

Hitung ulang dari dataset sendiri kalau lebih dari ~2 bulan, karena median pasar bergerak.

## Faktor tren revenue

Ambil `change_7dover7d` tiap entri, bobot pakai `total30d`, baru dirata-ratakan:

| tren revenue mingguan | faktor |
|---|---|
| >= +5% | 1,1 |
| -5% sampai +5% | 1,0 |
| -15% sampai -5% | 0,9 |
| -25% sampai -15% | 0,8 |
| <= -25% | 0,65 |

## Empat jebakan yang wajib dihindari

1. **Jangan pakai `total24h / (total30d/30)` sebagai momentum.** Hari libur dan akhir pekan bikin angkanya kelihatan menyusut padahal enggak, dan efeknya sistematis ke SEMUA protokol sekaligus. Gunakan `change_7dover7d`. Buat gambaran panjang, bandingkan laju harian sekarang dengan `average1y` (rata-rata harian setahun, bukan bulanan: `average1y x 365` kira-kira sama dengan `total1y`).
2. **Selalu tampilkan dua lensa: supply beredar dan supply penuh (FDV).** Ini bisa membalik kesimpulan. Contoh nyata: HYPE cuma 23,3% beredar, jadi 22,8x revenue di hitungan beredar tapi 97,8x di hitungan penuh, sementara median kategori Derivatives cuma 23,3x.
3. **Revenue kotor bukan uang yang bisa masuk ke token.** Yang bisa dipakai buyback itu surplus protokol. Sky Q1 2026: revenue kotor $123,79 juta, surplus protokol cuma $46 juta. Sebut angka surplusnya, jangan cuma revenue.
4. **Cek mekanisme payout sebelum menyebut sesuatu buyback atau burn.** Token hasil buyback bisa dibakar ATAU dibagi ke staker (Sky dua-duanya, tergantung parameter governance). Cek juga sumber dananya dan seberapa otomatis, karena buyback diskresioner bisa berhenti tanpa laporan.

## Circulating bukan float

Market cap dari CoinGecko menghitung token yang di-stake sebagai "beredar". Float yang beneran diperdagangkan bisa jauh lebih kecil, dan itu menjelaskan volume yang kelihatan sepi. Cek breakdown resmi protokol sebelum menyimpulkan likuiditas. Contoh Sky (info.skyeco.com/buyback): 74,67% supply beredar distake, 8,84% belum dimigrasi dari MKR, jadi float nyatanya cuma 16,21%.

## Yang harus dinyatakan jujur di output

- Fair value bukan target harga. Dia cuma artinya "pasar sekarang ngasih diskon segini ke cash flow hari ini kalau sisanya setuju".
- Model ini mengukur cash flow HARI INI, bukan masa depan. Kalau revenue-nya sedang turun, fair value-nya ikut turun.
- Kalau mayoritas universe kelihatan "murah" sekaligus, biasanya yang lagi dihukum itu sektornya, bukan semuanya diskon.
- Unlock tidak masuk hitungan model. Sebut terpisah.
