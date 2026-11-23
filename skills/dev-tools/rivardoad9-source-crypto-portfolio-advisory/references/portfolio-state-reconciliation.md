# Rekonsiliasi state portofolio sebelum ngasih advis

Companion to `holdings-thesis-verification.md` dan `theme-concentration-and-unlock-timing.md`.

**Trigger:** user nyebut holdings mereka ("gw skrng A, B, C, D"), atau balas review dengan daftar posisi
yang beda. Kejadian 3 Okt 2026: gw jalanin full thesis-check buat ONDO/GRAM/ALICE/TAO/BOME/STONK/HBAR,
user koreksi — *"gw skrng wld, tao, ondo sama aster"*. Seluruh analisisnya salah sasaran.

## Aturan

**State portofolio user tersebar di ≥4 tempat dan semuanya basi sendiri-sendiri.** Jangan pernah ngasih
advis posisi tanpa reconcile dulu. Nanya "sekarang pegang apa aja" lebih murah daripada salah analisa.

## Checklist konsumen state (update bareng, bukan sebagian)

| Konsumen | Lokasi | Yang harus diganti |
|---|---|---|
| Memory porto | MEMORY.md line `Modal $1,4k; PORTO: …` | daftar aset (+ level entry/SL/TP kalau ada) |
| Watchdog script | `~/.hermes/scripts/holdings_watch.py` → dict `CONFIG` | key per aset: `sym`, `binance`, `cg`, `move`, `hi`/`lo`, `entry`/`sl`/`tp` |
| Cron digest prompt | job "Holdings digest harian …" di `~/.hermes/cron/jobs.json` | prompt nge-list "aset yang dipantau" eksplisit → **wajib** diganti, plus field `name` |
| Vault | `~/obsidian-vault/*.md` | note baru + tandai note lama `> ⚠️ SUPERSEDED (tgl): … lihat <note baru>` |
| Posisi manual | `~/.hermes/data/fm_manual_positions.json` | kalau ada LP manual |

## Langkah

1. **Jangan langsung analisa.** Tarik harga live buat aset yang baru disebut dulu.
2. `python3 ~/.hermes/scripts/holdings_watch.py --debug` → baris tabelnya = aset yang *benar-benar*
   dipantau. Beda dari yang user sebut ⇒ state basi, itu akar masalahnya.
3. Patch `CONFIG`: tambah aset baru, copot yang lama, **tulis komentar bertanggal** apa yang dicopot
   (biar reconcile berikutnya tahu ini bukan kelalaian). Test ulang `--debug` (exit 0 + tabel benar).
4. Cari cron yang nge-list holdings di prompt:
   `python3 -c "import json;j=json.load(open('/home/ubuntu/.hermes/cron/jobs.json'));…grep holdings_watch…"`
   → update `prompt` **dan** `name` (nama job lama masih nyebut aset lama = jejak basi yang bikin bingung).
5. Update memory line porto (batch `replace`).
6. Vault: note baru + tandai note lama superseded.
7. Baru jawab.

## Pitfalls

- **`replace` memory bisa ngehapus fakta tetangga.** Kejadian nyata: niatnya *nambah* line ASTER, tapi
  `old_text`-nya justru line ONDO-unlock → fakta unlock 18 Jan 2027 ilang, harus di-`add` ulang. Sebelum
  batch op, pastikan `old_text` itu benar-benar line yang mau dibuang.
- **Versi ≠ kebenaran.** Note bernama "Rencana Portofolio Upside v4" tetap bisa basi; yang menentukan
  adalah data live + aset yang user sebut.
- **Aset kecil hidup di tempat lain.** Wallet pribadi / LP punya catatan sendiri (`stonk_watch.py`,
  `fm_manual_positions.json`). Tanya apakah ikut ditutup — jangan asumsi dihapus atau dipertahankan.

## Teknik analitik yang dipakai sesudah reconcile

**Inferensi timing entry dari jarak harga ke high 30 hari.** Kalau user bilang "average minus 3–6%" tapi
harga 3 dari 4 asetnya **15–21% di bawah high 30 hari** (ONDO −21%, ASTER −19%, TAO −15%), artinya entry
mereka di dekat top lokal — beli di kekuatan. Kesimpulannya: yang perlu dibenerin **timing entry**, bukan
nungguin dip. Ini nunjukin masalahnya pakai angka, tanpa nuduh.

**Hitung bet, bukan ticker.** WLD (identity/PoH buat AI) + TAO (AI compute) = **1 taruhan AI** walau 2
ticker; ONDO (RWA) dan ASTER (DEX) beda. Sebut eksplisit: *"kalau narasi AI mendingin, dua-duanya turun
bareng"*. Detail di `theme-concentration-and-unlock-timing.md`.

**Cek mesin vs narasi per aset.** Token fee-bearing: `https://api.llama.fi/summary/fees/<slug>?dataType=dailyFees`
(ASTER 3 Okt 2026: 24j $223k / 7d $0,97M / 30d $5,83M; ONDO $255k / $1,30M / $6,46M). Kalau nggak ada
fee/buyback/burn, tesis "kejemput" nggak punya mesin penarik — itu murni narasi, dan bilang begitu.

**Unlock/cliff: bedakan cliff bertanggal vs drip struktural.** Cliff (ONDO 18 Jan 2027, 1,71B ≈ 35% MC)
= tanggal keluar yang bisa ditulis. Drip dari float rendah (ASTER float 35%, insider cliff buka 18 Sep
2026 → ±+27% circ/tahun) = menjelaskan kenapa harganya **flat 30d saat yang lain +33–52%**: pasar lagi
nyerna unlock. Dua-duanya bukan alasan otomatis jual/hold — yang penting ada di laporan.

## Deliverable

Balas dengan: **koreksi state dulu** ("catatan gw basi, udah gw benerin: memory, watchdog 15m, digest
08:00") → regime line → tabel aset → temuan yang ngubah keputusan → apa yang udah dikerjain → konfirmasi
faktual yang benar-benar nggak bisa dijawab dari data (mis. "STONK di wallet Solana masih ada?").
Jangan tutup dengan "mau gw buatkan?" — level SL/USD yang diusulkan langsung, minta koreksi.
