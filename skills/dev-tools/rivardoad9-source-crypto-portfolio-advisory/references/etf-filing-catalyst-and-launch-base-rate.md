# "Coin X punya filing ETF — masuk sekarang?"

Trigger: user (atau mentornya) bilang sebuah koin bakal big move karena **ada filing ETF**. Jangan
jawab dari ingatan dan jangan cuma mengamin — verifikasi filingnya, lalu pisahkan **filing** dari
**event**, lalu ukur berapa yang sudah kepakai di harga.

## 1. Verifikasi filingnya dulu (jangan percaya ringkasan orang)

EDGAR full-text search `https://efts.sec.gov/LATEST/search-index?q=%22<token>%22&hits=12` → ambil
`display_names` + CIK → poll `https://data.sec.gov/submissions/CIK#########.json`. UA wajib real.
Cek: berapa issuer (dua issuer = sinyal kuat), form terakhir (S-1/A = proses; `8-A12B`/`485BPOS` =
menjelang jalan), dan apakah ETF-nya **staked** (versions seperti Canary Staked INJ) — staked ETF
menyedot float likuid dan bayar yield, jauh lebih material daripada wrapper biasa.
Detail endpoint + form-type artinya: skill `hermes-cron-automation` →
`references/regulatory-filing-watch-edgar.md`.

## 2. Pisahkan "filing" dari "approval", dan cari tanggal keputusannya

Tanpa tanggal keputusan, ini bukan katalis, cuma harapan (lihat aturan "catalyst with a date" di
`holdings-thesis-verification.md`). Yang bisa dikutip: jam 19b-4 (keputusan awal ~75 hari, bisa
diperpanjang hingga 240 hari) dan pernyataan issuer/CEO ("launch sebelum 2027" = belum pasti).
Sebutkan fase yang sedang berjalan dan label langkah filenya, jangan bilang "approval" untuk S-1/A.

## 3. Ukur berapa yang sudah kepakai — dan lihat reaksi koin itu sendiri pada berita serupa

Hitung: kenaikan 30 hari, jarak dari ATH, posisi di range 1 tahun, volatilitas harian, beta. Lalu cari
**preseden internal koin itu**: reaksi pas filing/upgrade sebelumnya. Contoh nyata (INJ, 2026):
spike 24 Sep ke $8,687 (upgrade Meridian + amendemen S-1) → turun ke $6,417 pada 8 Okt = **-26,1%
dalam 2 minggu**, baru breakout lagi setelahnya. Koin mid-cap biasanya kasih kesempatan retest setelah
spike berita; membeli di hari kenaikan +25% adalah timing terburuk yang tersedia.

## 4. Base rate peluncuran ETF alt: launch ≠ pump (ini yang paling sering salah)

Diukur 16 Okt 2026 dari Binance daily closes, gelombang ETF spot alt yang launch akhir Okt 2025:
30 hari setelah launch SOL **-27,5%**, HBAR **-24,4%**, XRP **-15,5%**, LTC **-10,4%**; 60 hari
-36%/-41%/-28%/-17%; nol dari empat nama itu bikin high baru setelah launch. Artinya: re-rating
transfer terjadi di fase **antisipasi**, dan approval/launch justru tempatnya dijual. Wajib disebut
caveat-nya: jendela itu barengan koreksi pasar luas → ini pola, bukan kausalitas bersih. Contoh lain
(BTC Jan 2024, ETH Mei 2024): dua-duanya koreksi ~20% setelah approval.

## 5. Cek juga cerita "mirip koin Z": cari di mana filingnya mendarat relatif ke puncak

Kalau user membandingkan dengan koin lain yang sudah meledak, ukur kapan filing/pengumumannya datang
vs kapan puncaknya. ZEC 2026: puncak **26 Sep** $1.698, filing spot Zcash ETF Winklevoss baru **6 Okt**
(setelah puncak) → sejak itu -30%. Filingnya datang di puncak, bukan sebelum lonjakan — jadi ZEC bukan
bukti "filing → pump". NEAR: filing Bitwise Mei 2025 tanpa gerakan berarti saat itu, lonjakan besar baru
Agustus-September 2026 di sekitar S-1/A amendemen + ETP Eropa.

## 6. Klaim "arus/AUM ETF melonjak" — bedakan tiga hal yang sering dicampur

Kalau user bilang "AUM ETF <koin> lagi melonjak", jangan amin dulu. Tiga angka berbeda:

1. **AUM** bergerak karena harga underlying, bukan cuma arus. AUM naik saat harga koin naik meski investor
   keluar. AUM juga bisa turun dari puncaknya sementara arus tahunan tetap positif.
2. **Arus YTD** adalah akumulasi setahun; headline "ETH outpace BTC" biasanya soal ini, bukan kondisi minggu ini.
3. **Arus harian** adalah satu-satunya yang menjawab "lagi". Jumlahkan 6–10 sesi terakhir sebelum menjawab.

Sumber harian keyless: `https://farside.co.uk/{btc,eth,sol,hype,zec}/`. HTML statis; tiap `<tr>` berisi tanggal,
kolom per issuer, dan kolom total dalam **juta dolar**, negatif ditulis dalam tanda kurung `(116.1)`. Parse dengan
regex `<tr>` → `<td>` (jangan asumsikan pandas terpasang):

```python
rows = re.findall(r"<tr.*?</tr>", html, re.S)
# cell[0] = tanggal, cell[-1] = total harian $M; buang baris Fee/Seed/Total/Average/Maximum/Minimum
```

Jebakan yang sudah kena:

- **Baris `Total` di tabel Farside tidak selalu sama dengan jumlah arus harian** (seed/konversi ikut terhitung di
  beberapa halaman). Jangan kutip baris Total sebagai "net flow" — jumlahkan sendiri baris harian yang mau dikutip.
- **Produk yang baru listing**: pisahkan **seed** dari arus. Seed besar (ratusan juta) bukan demand; yang penting
  arus harian setelah hari pertama. ETF yang baru beberapa minggu biasanya arusnya kecil dan bolak-balik.
- **AUM satu kelas aset bukan pendukung tesis koin lain.** ETF ETH menguat cuma sinyal beta/sentimen untuk porto yang
  isinya SOL/SUI/TAO/INJ; yang benar-benar mendukung tesis adalah arus ETF koin itu sendiri plus TVL/stablecoin chain-nya.
- **Jangan campur horizon**: 30 hari bisa positif sementara 7 hari negatif. Sebutkan dua-duanya, lalu bilang horizon
  mana yang dipakai untuk klaim.

Ganti "headline" dengan ambang konfirmasi yang bisa dicek: arus positif 3 sesi berturut-turut, arus harian koin
terkait di atas ambang nominal, TVL chain reclaim level sebelumnya, supply stablecoin naik. Kalau ambang itu belum
kena, sebut ini koreksi di dalam tren, bukan konfirmasi tesis.

## 7. Bentuk jawaban yang bekerja

1. Verifikasi filingnya (angka + tanggal + nama issuer + fase).
2. Akui eksplisit kalau tesis user benar **sebagian** — jangan nge-amin, jangan matiin.
3. Tabel: apa yang sudah kepakai di harga vs apa yang masih di depan (tanggal event).
4. Rencana tranche (masuk sebagian sekarang, sisanya tunggu retest — sebutkan level), plus **aturan
   keluar yang ditulis SEBELUM event**, karena base rate launch itu negatif.
5. Invalidation level yang bisa diukur (MA50 close, rasio harga vs BTC), bukan feeling.
