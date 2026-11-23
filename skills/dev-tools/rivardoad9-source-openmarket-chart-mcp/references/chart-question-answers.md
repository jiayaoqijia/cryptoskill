# Menjawab chart yang dikirim user ("solid long, atau nunggu turun ke mana")

User sering kirim screenshot chart dari app lain (TradingView mobile, Bookmap) berisi EMA ribbon,
box resistance/support, dan trendline bikinan dia sendiri, lalu tanya keputusan: masuk sekarang atau
tunggu di harga berapa. Ini kelas pertanyaan yang berulang, jadi perlakuannya tetap.

## Aturan yang tidak boleh dilanggar

1. **Angka di chart dia itu LEVEL TUJUAN, bukan fakta.** Dia menandai level yang dia ingin lihat,
   jadi tugas pertama bukan mengiyakan, tapi mengecek apakah harga/struktur sekarang benar-benar di
   situ. Ambil data live dulu (harga, candle, funding, OI), baru komentar.
2. **Baca screenshot-nya dengan `vision_analyze`** sebelum menafsirkan: sumbu harga, label yang dia
   tulis, angka indikator, posisi harga terhadap ribbon. Deskripsi otomatis sering salah baca satu
   label dan seluruh analisa ikut geser. Minta pembacaan eksplisit ("sebutkan angka yang benar-benar
   terbaca").
3. **Cocokkan garis dia dengan indikator.** Garis "support" yang dia gambar sering sama dengan
   EMA200 atau EMA50, dan level resistance-nya sama dengan swing high sebelumnya. Kalau ketemu,
   bilang ("garis hijau 0.003263 itu EMA200 harian, bukan support acak") - dia jadi tau level itu
   bergerak dan apa yang bikinnya penting.
4. **Indikator dihitung di timeframe chart yang dia kirim**, bukan di timeframe yang enak buat kita.
   Chart 1D berarti EMA/RSI/ATR harian. `scripts/daily_ta.py` buat itu; OpenMarket free plan nggak
   bisa (lihat pitfall `tier_forbidden` di SKILL.md).
5. **`metric_get` interval HOUR buat posisi trader live**, bukan buat tren: `funding_rate`,
   `open_interest`, `open_interest_delta_pct` (`params {"bars":24}`), `taker_buy_ratio`, `cvd`
   (`params {"bars":24}`), `book_imbalance` - semua dalam satu call (maks 8 query per call).

## Bentuk jawaban

Urutannya: **verdict di baris pertama**, lalu bukti dua sisi, lalu level, lalu larangan.

1. **Verdict dulu, dan jangan memihak harga cuma karena dia kelihatan mau beli.** Contoh yang benar:
   "Bukan solid long. Trennya masih naik tapi lu bakal beli tepat setelah breakout mingguannya gagal."
2. **Harga live vs angka di screenshot** - sebut kalau cocok (chart-nya akurat) atau kalau beda.
3. **Yang bilang trennya masih sehat**: susunan EMA, jarak ke EMA200, range position.
4. **Yang bilang jangan buru-buru**: harga vs EMA terdekat, kapan puncaknya, jarak dari puncak,
   RSI/StochRSI, dan yang paling penting **ATR dalam persen** - ini yang menjelaskan kenapa stop 4%
   di aset ATR 11%/hari itu cuma 0,4 ATR dan bakal kesapu. Selalu tulis stop yang diusulkan dalam
   satuan ATR, bukan cuma dalam persen.
5. **Posisi trader live** (funding, OI, taker buy, CVD): bedakan "permukaan beli" dari "CVD negatif".
6. **Pendorong fundamentalnya, dengan tanggal.** Kalau reli punya sebab nyata (buyback/burn dari
   revenue, unlock, listing), tulis angka + tanggalnya, plus batasnya: tanggal program berakhir,
   pemegang token nggak punya klaim cash flow, warning regulator, sektor induknya menyusut. Chart yang
   naik di sektor yang mati itu penting disebut, bukan dipuji.
7. **Zona tunggu, tiga tingkat, dengan RR**: (a) pullback ke swing low terdekat, (b) konfirmasi
   close di atas level yang tadi gagal, (c) zona dalam (EMA50 + swing high lama yang jadi support).
   Tiap opsi: entry, stop, target, RR, dan jujur kalau stop-nya masih di bawah 1 ATR.
8. **Regime makro satu baris** dari `~/.hermes/scripts/market_regime.py` (BTC dominance, breadth,
   stablecoin). Ini permintaan tetap user untuk tiap analisa pasar: alt itu lawan atau dibantu arus.
9. **"Yang jangan dilakuin"** sebagai penutup - jangan long karena takut ketinggalan, jangan pakai
   leverage di aset ATR dua digit. Bukan disclaimer kosong.
10. Kalau ada angka faktual dari web (harga, tanggal program, warning regulator), sertakan sources
    lewat skill `grounded-citations`; data hitungan sendiri (klines) sebutkan sumbernya juga.

## Yang jangan dilakukan

- Jangan menafsirkan StochRSI oversold sebagai sinyal beli. Sebut konteksnya: oversold di tengah
  candle turun itu momentum habis, bukan pembalikan.
- Jangan menyarankan entry market di tengah range konsolidasi; sebut dulu bahwa pasar belum mutusin.
- Jangan menyembunyikan keraguan. Kalau strukturnya "bisa dua arah", bilang begitu - user lebih
  menghargai jawaban yang bisa dia cek daripada keyakinan yang dipaksakan.
- Jangan lupa bilang kalau harga minggu ini tinggal bolak-balik di range sempit: itu artinya sinyal
  titik masuknya belum ada, dan menunggu itu keputusan yang sah.
