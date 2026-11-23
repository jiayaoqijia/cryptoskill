# Verifikasi event token/protokol dari sumber primer (studi kasus PAID / UsePaid, 29 Sep 2026)

Konteks: user kirim **link post X** (di sini thread @StarPlatinum_ soal $PAID & X Money pause). Yang diminta:
benar/nggak, dan **apa artinya buat posisi dia**. Urutan kerja yang terbukti:

## 1. Ambil isi post + lampirannya, jangan cuma teks

- `https://api.fxtwitter.com/<user>/status/<id>` → teks penuh, entities, URL media.
- Unduh media `pbs.twimg.com/media/...?name=orig` → **transkrip pakai vision apa adanya** (angka, dashboard,
  screenshot chart resmi). Screenshot sering memuat data yang tidak ada di teks: tabel fee harian, PnL dashboard,
  live feed payout.
- Kalau screenshot memuat dashboard tool yang sedang dipromosikan, catat itu: **bukti berasal dari UI pihak
  yang diuntungkan**, bukan data on-chain.

## 2. Cek angka internal si pemosting LEBIH DULU

Bandingkan angka di teks vs angka di screenshot-nya sendiri. Contoh nyata: "1622 trades" vs "913W/159L" (=1072),
dan "starting with $1,000" vs "Open Invested $2,185". Selisih seperti ini tidak membuktikan bohong, tapi wajib
dilaporkan sebagai tidak konsisten. Lakukan hal sama pada akun resmi proyek: klaim "26x hari sebelumnya" tidak
cocok dengan grafik harian mereka sendiri ($1,54M vs $623rb; 26x vs 5,4x).

## 3. Halaman resmi proyek = sumber primer paling produktif

Untuk token/protokol kecil, `curl` halaman-halamannya dan baca teksnya (server-rendered React aman dibaca):
`/` (banner status) · `/docs` · `/analytics` · `/capital-flow` · `/claim` · `/payments`.
Yang biasanya cuma ada di situ: **perubahan split fee yang berlaku jam-jam terakhir**, jendela klaim + apa yang
terjadi pada saldo yang tidak diklaim, definisi eligibility (timestamp), dan disclaimer afiliasi
("not affiliated with X Corp"). Ini yang paling sering jadi temuan terpenting dan TIDAK disebut di thread.

## 4. Data pasar & posisi user

- Harga/mcap/likuiditas: GeckoTerminal (`/networks/<net>/tokens/<mint>`, OHLCV `.../pools/<pool>/ohlcv/day`) +
  DexScreener (`/latest/dex/tokens/<mint>` → priceChange h1/h6/h24, liq, vol).
- Watchdog lokal (`holdings_watch.py --debug`) untuk angka yang dipakai alert + cek trigger mana yang sudah bunyi.
- Barang on-chain kalau perlu: di Solana, burn biasanya lewat **instruksi SPL burn**, jadi cek saldo alamat
  incinerator BUKAN cara verifikasi yang benar (bisa kosong padahal burn jalan) — verifikasi via `getTokenSupply`
  dari waktu ke waktu.
- Selalu konversi ke dampak posisi user (mis. "5% alokasi → sekarang ~2%") + level invalidation eksplisit.

## 5. Jangan berhenti di "benar/salah"

Struktur laporan yang diterima user: (a) thread-nya akurat atau tidak, klaim per klaim ✓/✗; (b) temuan yang
**tidak** disebut pemosting (bagian paling bernilai); (c) posisi user sekarang dalam angka; (d) apa yang masih
hidup vs yang rusak; (e) aksi + level invalidation. Simpan ke vault + lampirkan screenshot ke
`attachments/` supaya bisa dirujuk lagi.
