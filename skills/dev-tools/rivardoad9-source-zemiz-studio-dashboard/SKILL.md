---
name: zemiz-studio-dashboard
description: Use when working on the Zemiz Studio dashboard.
---

# Zemiz Studio dashboard

Dashboard content automation TikTok/YouTube milik Do. Stdlib Python + SQLite + SPA statis, port **8801**, tunnel cloudflared. Working dir `~/studio`.

## Aturan desain (dari Do, wajib)

- Palet **putih + biru muda**. Ditolak keras: hitam/ungu/neon, gradient ungu, glow — disebut "terlalu AI".
- Satu aksen saja: `--blue #2563EB`, `--blue-deep #1D4ED8`, `--blue-soft #EFF5FF`, `--blue-line #D7E5FB`, bg `--paper #F6F8FB`, card `#FFFFFF`, border `--line #E4E9F1`.
- Teks: ink `#0E1726`, sekunder `#62718A`, label kecil `#6E7C93` (jangan lebih pucat, gagal kontras).
- Hierarki lewat **ukuran + berat**, bukan warna. Label KPI uppercase 10,5px letterspacing .7px; angka 30px/700 tabular.
- Tanpa dot dekoratif di label, tanpa kartu di dalam kartu, tanpa gradient text, tanpa emoji sebagai ikon.
- Chart: satu keluarga biru, seri kedua dibedakan **garis putus-putus** (bukan cuma warna). Skala Y dibulatkan (1/1,5/2/…×10^n), gridline 5, sumbu X label adaptif (`w < 560` → 3 label).
- Status pakai chip netral + teks; hijau/amber hanya untuk makna (tayang, warning kuota).
- Font Plus Jakarta Sans (satu-satunya font terpasang), fallback system.

## Aturan isi layar

- **Tanpa chrome demo/disclaimer di layar utama.** Banner "Mode demo" dan kartu status "0/2 akun tersambung" di sidebar dua-duanya diminta dihapus. Kejujuran soal keterbatasan taruh di tempat yang dicari orang: tab Akun, kartu metode modul, atau jawaban chat — bukan pita peringatan di atas KPI yang bikin produk kelihatan setengah jadi.
- Jangan menaikkan angka contoh ke halaman yang punya data live; kalau sumber tidak ada (TikTok), kosongkan dan sebut alasannya sekali di kartu metode.
- Copy UI bahasa Indonesia netral, bukan gaya gw/lu — register santai cuma untuk chat.

### Kalau Do minta hapus satu elemen

Hapus node-nya **dan** semua JS yang menulis ke id itu. Contoh: membuang `#acc-summary` / `#acc-note` dari `index.html` tapi meninggalkan `$('#acc-summary').textContent = …` di `route()` bikin seluruh view Ringkasan gagal render (`null.textContent`). Verifikasi habis itu dengan `dump-dom` + grep teks yang dihapus (harus 0) dan screenshot sekali untuk cek jarak atas.

## Jalanin & jaga hidup

```bash
cd ~/studio && python3 app.py            # 127.0.0.1:8801
bash ~/studio/keep.sh                    # server + tunnel, URL di data/url.txt
```

Cron Hermes `zemiz-studio-keeper` (every 10m, no_agent, script `zemiz_studio_keep.sh` di ~/.hermes/scripts) — **hanya cetak URL kalau berubah**; script harus diam kalau sehat.

Kalau `cronjob_manage` menolak path: script wajib file nyata di `~/.hermes/scripts/` (symlink ditolak sebagai traversal).

## Riset pasar (`#/pasar`)

Modul data live, bukan mock:

- `market_scan.py`: 7 tema × 2 query lewat `https://www.youtube.com/results?...&sp=EgIIAw%3D%3D` (filter minggu ini), parse `ytInitialData` → `videoRenderer`. Simpan `market_runs` + `market_videos`.
- `GET /api/market`, `POST /api/market/refresh` (thread background, UI polling 4 detik, ±2 menit).
- Metrik: tayangan, rata-rata, `velocity` = tayangan/jam tayang dibagi rata-rata semua tema, leaderboard 10 akun, temuan kalimat yang dihitung dari angka.
- TikTok **tidak bisa**: `ads.tiktok.com/creative_radar_api` balas `40101 no permission`; tikwm search kena Cloudflare. Jangan isi angka karangan, tulis apa adanya.

### Pitfall angka

- UI `hl=id` bikin angka `67.264 x ditonton` (titik = ribuan) dan `5,5 rb` (koma = desimal). Satu parser `parse_views` harus dua jalur; kalau tidak, 67 ribu kebaca 67.
- Usia video datang sebagai teks (`2 h lalu`, `12 jam lalu`), simpan **jam** (`age_hours`), bukan hari, biar velocity bisa dihitung.
- Jangan `DROP TABLE market_videos` saat scan: halaman jadi kosong di tengah refresh. Biarkan run lama tetap ada, pilih run terakhir yang `EXISTS` videonya.
- Saat scan jalan, `/api/market` bisa balas `empty: true` dengan totals nol. Empty-state harus cek `scanning` dulu dan polling sampai selesai, jangan menampilkan tombol "mulai scan" seolah belum pernah ada run.
- Jangan pakai `pkill -f app.py` (match shell sendiri) — matikan lewat `fuser -k 8801/tcp`.

## Struktur

- `app.py` — ThreadingHTTPServer + sqlite3, `DATA/studio.db`, tabel `content`, `rules`, `events`, `accounts`; seed 32 konten + 3 rules.
- `static/index.html|app.js|styles.css` — SPA hash router (`#/ringkasan|konten|kalender|otomasi|akun`), render per view, event delegation.
- API: `/api/overview?days=`, `/api/content` (GET/POST/PATCH/DELETE), `/api/calendar?start=`, `/api/rules(/<id>/toggle)`, `/api/agent/run`, `/api/accounts`, `/api/accounts/<p>/credentials`, `/oauth/<p>/start`.
- Upload TikTok/YouTube **belum aktif** — butuh app credential punya Do; jangan klaim nyambung.

## Pitfall QA

- `goto_url` ke URL dengan hash yang sama **tidak reload** SPA; pakai `cdp('Page.reload', ignoreCache=True)`.
- `capture_screenshot` di 1440×@2x sering timeout 60 s. Fallback cepat: `chromium --headless=new --window-size=W,H --virtual-time-budget=6000 --screenshot=out.png URL`.
- Cek overflow mobile: `document.documentElement.scrollWidth === innerWidth`.
- Cek render semua tab tanpa screenshot: `chromium --dump-dom URL#/tab` lalu grep judul kartu.
