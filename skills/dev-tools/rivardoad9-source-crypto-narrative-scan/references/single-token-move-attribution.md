# Atribusi pergerakan SATU token ("kenapa X naik tinggi?") — worked 4 Okt 2026 (STRK)

Trigger: user tanya **kenapa satu token naik/turun tajam** — tanpa minta DD kontrak, tanpa minta tema.
Bukan pertanyaan tema (→ `crypto-narrative-scan`), bukan DD token (→ `gmgn-token`), bukan audit wallet.

Tujuannya: jawab **apa penyebabnya, seberapa nyata, dan apa yang membatalkan tesis itu** — bukan
mengarang narasi yang enak dibaca.

## Prosedur 6 langkah

**1. Ukur & pin JAM-nya (data venue, bukan berita).**

```python
get("https://api.binance.com/api/v3/ticker/24hr?symbol=STRKUSDT")   # lastPrice, priceChangePercent, volume, count
get(".../klines?symbol=STRKUSDT&interval=1d&limit=90")              # % 1/7/14/30/60/90 hari + high/low 90h
get(".../klines?symbol=STRKUSDT&interval=1h&limit=72")              # cari jam dengan volume 10–30x
```

Yang dicari: **jam** dengan volume ekstrem. STRK: **3 Okt 15:00 UTC**, volume 54,7 juta vs 1,5–4,3
juta/jam sebelumnya (±13–30x) dan +11,7% dalam 1 jam. Jam itu = waktu katalis; semua verifikasi
berikutnya diikat ke jam tersebut.

**2. Tes idiosinkratik vs sektor — langkah yang paling sering kelewat.**

Ambil peers di jam yang sama (`ticker/24hr` + `klines 1h&startTime=<jam katalis>`):

| | STRK | ARB | OP | ZK | IMX | BTC | ETH |
|---|---|---|---|---|---|---|---|
| 24 jam | **+21,2%** | +0,9% | +2,6% | +3,6% | −0,6% | +0,2% | +0,5% |

Peers flat → **katalis spesifik token**, lanjut cari beritanya. Kalau peers ikut naik → jawabannya
"sektor/market", jangan paksa cari berita token.

**3. Derivatif: leverage atau beli spot?**

```python
get("https://fapi.binance.com/fapi/v1/openInterest?symbol=STRKUSDT")
get("https://fapi.binance.com/fapi/v1/premiumIndex?symbol=STRKUSDT")   # lastFundingRate
get("https://fapi.binance.com/fapi/v1/fundingRate?symbol=STRKUSDT&limit=8")
get("https://fapi.binance.com/fapi/v1/klines?symbol=STRKUSDT&interval=1h&limit=24")
```

Funding ≈ +0,005%/8 jam + OI naik tipis = **bukan short squeeze**; lebih beli spot yang ditumpuk
posisi. Funding ekstrem (>0,1%/8 jam) atau OI meledak = gerakan leverage → sebut risikonya
(funding positif besar = long sudah bayar mahal). Catat juga futures volume (Coinglass di berita
bilang +212% ke $187,68 juta, OI +20,46% ke $74,19 juta) sebagai penguat, bukan sebab.

**4. Fundamental vs harga — uji paling jujur.**

```python
get("https://api.llama.fi/charts/Starknet")   # seri TVL harian
# QUIRK: r['date'] = STRING epoch → int(str(dv)[:10]) ; int(dv) langsung melempar ValueError
```

STRK: TVL $182,6M (30 Sep) → $189,5M (4 Okt) = **+2%**, harga +21% → **posisi/sentimen, bukan inflow
modal nyata.** Ini bagian yang wajib dikatakan. Angka TVL beda antar sumber (CoinGecko $272M vs
DefiLlama $189M — beda definisi kategori); sebut sumbernya, jangan campur. `/v2/chains` memberi TVL
sekarang per chain tapi inklusi kategorinya beda dari seri `charts/<Chain>`.

**5. Katalis bertanggal (berita + kalender).**

`web_search "<token> surge reason"` → `web_extract` artikelnya; lalu cek **event bertanggal di depan**:
CoinMarketCal memberi tanggal + skor impact (STRK: **v0.14.4 mainnet 5 Okt, impact 5,5/10 medium** —
1,1 miliar L2 gas per proof, SNIP-36) → pola **beli sebelum event**. Katalis tanpa tanggal bukan
katalis; aturannya di `catalyst-and-flow-verification.md`.

**6. Overhang: unlock + kabar jelek yang masih beredar.**

Unlock terjadwal adalah risiko tepat setelah pump (STRK: **127 juta token ≈ 1,3% supply, 15 Okt**,
lanjut bulanan s/d Mar 2027). Sebut juga insiden yang belum hilang (Nostra oracle exploit 24 Sep,
$3,5 juta bad debt).

## Bentuk laporan (dipakai 4 Okt 2026, user diem — artinya bukan komplain)

1. Angka dulu: harga, % multi-timeframe, **jam lompatan + rasio volume**, sumber data venue.
2. 3 sebab **diurut dari yang paling nyata**, tiap sebab ada tanggal + sumber bernama.
3. Satu bagian "yang bikin gw hati-hati": mismatch fundamental (TVL vs harga), overbought (RSI,
   resistance berikutnya), unlock.
4. Satu kalimat bacaan: "katalis beneran, tapi reaksi >> fundamental → ini posisi trader menjelang
   event, bukan perubahan nilai."
5. Kutip sumber lewat ledger (`grounded-citations`: register saat retrieval, `render --cited-in`,
   `verify --min-coverage 0.5`), jangan URL hafalan.

## Pitfall

- **Artikel berbentuk sama dari event LAIN.** Coinpedia "STRK jumps 50% … $0,040 → $0,061" itu **Mei
  2026** (governance SNIP-38/39; strkBTC live 12 Mei) — rentang harganya identik dengan pergerakan
  3 Okt, jadi gampang dipakai sebagai "penyebab sekarang". Cek tanggal + isi sebelum mengutip.
- **"Volume naik" bukan sebab**, itu gejala. Sebab = katalis bertanggal / posisi / inflow.
- Kalau berita tidak ketemu: katakan apa adanya — "tidak ada pengumuman resmi di jendela 30 Sep–2 Okt,
  jadi ini momentum + posisi" (persis temuan CoinStats 2 Okt 2026 untuk STRK). Jangan karang katalis.
- Jangan mulai dari narasi Twitter/KOL; mulai dari jam & volume, narasi dipakai untuk **menjelaskan**
  setelah angkanya cocok.
