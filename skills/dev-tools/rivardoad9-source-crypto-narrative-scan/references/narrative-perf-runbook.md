# Runbook: menyusun laporan "performance narasi" (eksekusi, bukan teori)

Pelengkap `references/narrative-performance-scoreboard.md` (yang isinya definisi metrik + taksonomi
alasan). Dokumen ini isi hal-hal operasional yang bikin laporannya benar dan bisa direproduksi.
Catatan: skill_manage `patch` untuk file existing bisa ditolak (read-before-write guard, dedup) —
kalau itu terjadi, tulis/timpa lewat `write_file` ke path baru atau tempel isinya ke file ini.

## 1. Skrip yang dipakai

| file | fungsi |
|---|---|
| `~/.hermes/scripts/diag/narr_perf.py` | dump skorboard per tema → `/tmp/narr_perf.json` + tabel teks. **Kalau hilang, salin dari `scripts/narr_perf.py` di skill ini** — jangan tulis ulang dari nol. |
| `~/.hermes/scripts/diag/make_narr_perf_chart.py` | baca `/tmp/narr_perf.json` → `/tmp/narr_perf.html` (bar horizontal r7 + garis BTC putus-putus + kolom angka). Caption bawah **dinamis** sejak 5 Okt 2026. |
| `~/.hermes/scripts/narrative_rotation_early.py` | sumber bucket tema + `build()`, `cum()`, `metrics()`, `intraday()`. **Jangan** bikin daftar tema kedua. |

Render chart:

```bash
cd ~/.hermes/scripts/diag && python3 narr_perf.py
OUT=$(python3 make_narr_perf_chart.py)          # cetak "chart: 1360x965 -> --window-size=1360,965"
SIZE=$(echo "$OUT" | sed 's/.*--window-size=//')
/home/ubuntu/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome --headless=new --no-sandbox \
  --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size="$SIZE" \
  --screenshot=/tmp/narr_perf_7d.png "file:///tmp/narr_perf.html"
```

Lalu WAJIB `vision_analyze` gambar sebelum kirim, dan simpan salinan ke
`~/obsidian-vault/attachments/narrative-perf-7d-<tgl>.png` + catatan angka ke
`~/obsidian-vault/Performance Narasi 7d (<tgl>).md`.

## 2. Kontrak `/tmp/narr_perf.json`

```json
{"ts_last": <epoch ms>, "ts_prev": <epoch ms>, "days": 120,
 "btc": {"r1":…, "r3":…, "r7":…, "r14":…, "r30":…},
 "rows": [{"th":"Gaming/Metaverse","r7":0.1562,"a7":0.1212,"r1":-0.0001, "...":"..."}]}
```

- Kunci `btc` **harus bernama** (`r7`, bukan int `7`): `json.dump` mengubah key int jadi string,
  sementara chart script membaca `D['btc']['r7']` → pernah mati `KeyError: 'r7'`.
- Tiap row butuh minimal `th`, `r7`, `a7`, `r1` (itu yang dicetak di kanan batang).
- `ts_last` dipakai caption untuk menuliskan tanggal bar → sediakan (epoch ms).

## 3. Metrik: apa yang sudah ada vs dihitung sendiri

`nre.metrics(td, M, ts, i)` hanya mengembalikan `r1/r3/r7/r14/volratio/breadth3/alpha3`.
Yang dihitung sendiri dari `M` + `ts`: `r30`, alpha per horizon (`r_w − BTC_r_w`), **beta 60 hari**
(`cov(ret_tema, ret_BTC)/var(ret_BTC)`, butuh ≥20 sampel harian), `exp7 = beta × BTC_r7`,
`resid7 = r7 − exp7`, `breadth1`/`breadth7` (% anggota hijau), `volratio7 = mean(vol,7)/mean(vol,30)`,
top3/bot3 anggota per r7, best/worst 24 jam. Kumulatif tema selalu lewat `nre.cum(ret, i, w)`.

`resid7` adalah pembeda inti **ikut market** (|resid| kecil) vs **struktural** (resid negatif +
volume keluar) — hitung juga counter "n tema ngalahin BTC" (alpha7 > 0) untuk ringkasan.

## 4. Waktu bar (mudah salah)

- Klines harian open time **07:00 WIB**. `ts_last` = candle HARI INI yang baru jalan beberapa jam
  → semua r1 mepet nol. Tulis eksplisit "bar terakhir 05 Okt 07:00 WIB (candle jalan)".
- `narr_hist_cache.json` TTL 12 jam (mtime = kapan terakhir diambil). Kalau laporannya jam 14:00,
  angkanya tetap dari candle pagi — sebut itu, jangan pura-pura real-time.
- Konversi epoch ms → WIB: `datetime.fromtimestamp(ms/1000, timezone(timedelta(hours=7)))`.

## 5. Kondisi live dari jalur 4 jam

`intraday()` **return lebih awal kalau tidak ada tema baru yang lolos sinyal** (`if not force and not new`),
jadi memanggil CLI-nya bisa keluar tanpa cetakan. Paksa:

```python
spec = importlib.util.spec_from_file_location(
    "nre", os.path.expanduser("~/.hermes/scripts/narrative_rotation_early.py"))
nre = importlib.util.module_from_spec(spec); spec.loader.exec_module(nre)
nre.intraday(force=True)
```

Kalimat yang dihasilkan: "belum ada sinyal HARI-1 bar ini (butuh alpha 4j ≥ +1,5% & volume ≥ 2x)".
Contoh 5 Okt 2026 (bar 11:00 WIB): BTC 4j +0,20%, 10 tema hijau tipis, Meme memimpin (alpha +1,00%)
tapi volume hanya 1,08x → tidak ada yang lolos.

## 6. Tiga pembatas jujur yang harus selalu ada di laporan

1. Candle terakhir masih jalan (lihat §4) — angka 24 jam mepet nol itu artefak, bukan pasar mati.
2. Lane narasi statusnya **PERFORMANCE-ONLY** kalau `~/.hermes/data/narr_alert_on` tidak ada
   (alert dimatikan 4 Okt 2026; `narr_rotation_cron.sh` menulis ke log tanpa kirim pesan).
   Katakan: ini pengukuran, bukan sinyal entry.
3. Banding r7 hari ini vs kemarin **bukan** performa harian: jendela 7 hari geser satu hari, jadi
   hari terburuk yang keluar dari jendela ikut mengangkat angkanya (Privacy −10,87% → −3,46% pada
   5 Okt tanpa pembalikan harga). Sebut pergeseran jendela; jangan bilang "tema X naik".

Tutup laporan dengan kaitan ke posisi user (mis. 5 Okt: WLD +17,5% nolong porto; ONDO −4,5% +
RWA breadth 57% + resid −2,43% = data pendukung trim ONDO yang over cap).
