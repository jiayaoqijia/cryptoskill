---
name: hermes-trade-desk
description: Run/debug the Hermes Trade paper desk.
---

# Hermes Trade desk

Paper-trading desk yang dijalankan agent: scan market sendiri, bikin plan RR 1:2, gambar posisi di OpenMarket,
catat entry/exit jadi track record, tampilkan di dashboard web + kirim update Telegram.
Semua ada di `~/.hermes/trade/`.

## Komponen

Venue: OpenMarket MCP (`om.py`, token OAuth `~/.hermes/mcp-tokens/openmarket.json`, auto refresh).
venv terpisah `~/.hermes/trade/venv` (mcp + httpx + httpx2).

- `om.py` — `om.call(tool, args)`, `om.candles(symbol, interval=..., lookback=...)`.
- `ta.py` — EMA/RSI/ATR + `features(bars)` (tanpa numpy/pandas; system python cuma stdlib).
- `core.py` — SQLite `data/hermes_trade.db` (tabel `trades`, `equity`, `events`, `meta`): aturan main,
  ukuran posisi, PnL, statistik. Satu-satunya sumber kebenaran.
- `scan.py` — planner: `market_screen` → candle 15m → setup → plan → gambar di OpenMarket. `--dry` = tanpa tulis DB/gambar.
- `monitor.py` — trigger entry, stop/target, expiry 8 jam, time exit 24 jam. Cetak HANYA kalau ada kejadian; cek kapasitas (maks 3 posisi) + kas sebelum fill, kalau tidak lolos batalkan plan dengan alasannya.
- `seed_manual_plans.py` — masukin plan yang sudah dipublikasi ke user sebelum DB ada, level persis seperti yang dilaporkan, `created_at`/`expire_at` asli.
- `server.py` + `page.html` — dashboard :8793 (`/`, `/api/state`, `/healthz`), cache harga 60s pakai tool `markets`.
- `up.sh` — watchdog idempotent server + cloudflared, kirim URL kalau berubah. URL publik terkini selalu
  ada di `data/ht_url.txt` (`data/ht_url_seen.txt` = yang sudah dikabarkan ke user) — baca file itu,
  jangan grep log tunnel atau nyari ulang di cron output.
- `run_scan.sh` / `run_monitor.sh` — pembungkus cron (pipe ke `~/.hermes/scripts/msgstyle.py` + dedupe error).

Cron (`~/.hermes/scripts/hermes_trade_{scan,monitor,up}.sh` → exec script di atas):
scan `0 */2 * * *` (tiap 2 jam, 12 sesi/hari), monitor `*/15 * * * *`, keeper `*/10 * * * *`, semua `no_agent` + deliver origin.

## Aturan main desk (jangan diubah tanpa bilang ke user)

- Modal $1000 cash, tanpa leverage, notional per posisi maks 30% equity (3 posisi = 90% kas, sisa buffer, bukan 35% — 3×35% bikin posisi ketiga kehabisan kas), risiko 1% equity, maks 3 posisi, 1 per simbol.
- Plan valid 8 jam (kalau entry ga kesentuh → batal), exit di stop/target atau maks 24 jam. Karena scan jalan tiap 2 jam sementara plan hidup 8 jam, sering kali slot (`MAX_PLAN` 3) masih penuh dan scan-nya nggak ngasih plan baru — itu normal, tanda slot lagi kepakai, bukan error. Scan tetap membatalkan plan kadaluarsa dulu sebelum hitung slot, jadi slot balik sendiri.
- Entry breakout butuh CLOSE 15m lewat level; entry retest cukup harga sentuh level (limit).
- Candle yang sama dengan fill tidak dihitung untuk stop/target (konservatif, hindari exit mustahil).
- Fee 0,05% per sisi dihitung di PnL.
- Stop breakout/breakdown: di bawah/atas base 3 jam, jarak dikunci 1–2,5 ATR; tolak plan kalau jarak > 4% harga.

## Kesalahan OpenMarket yang mahal (semua sudah pernah kejadian)

- `om.call` TIDAK melempar exception kalau argumen salah — dia balikin dict `{"error":"invalid_arguments",...}`.
  Selalu cek `if isinstance(r, dict) and r.get("error")` sebelum lanjut, kalau tidak, langkah berikutnya jalan
  dengan asumsi yang salah (drawing numpuk / chart kosong).
- `chart_drawing_remove` parameternya `ids` (array), BUKAN `drawingIds`.
- Sebelum menggambar: pastikan pane-nya simbol & interval yang benar (`chart_symbol`, `chart_interval` 15m).
  Server menolak box 12 jam di pane 1d: "spans 12h of chart time but the pane's bars are 1d".
- Baca balik: `chart_drawing_list` → key `marks`; `chart_show` → key `drawings`. Dua-duanya `drawingId` + `tool`.

## Pelajaran teknis (yang pernah bikin gagal)

- Scan yang nggak nemu plan baru mencetak penanda `NO_PLAN` (satu baris), dan `run_scan.sh` nangkep itu → diam total. Jangan bikin scan.py mencetak stdout kosong: wrapper menganggap stdout kosong sebagai scan gagal dan mengirim alert palsu. Kartu "no trade" cuma dicetak dengan `scan.py --verbose`.

- Rate limit OpenMarket free plan: jarak ≥6,5 detik antar panggilan candle (`paced_candles`), retry 3× jeda 20s.
- Kill server: jangan `pkill -f "[s]erver.py"` (kena semua server lain di `~/.hermes/scripts/`), TAPI bracket trick (`[t]rade/server.py`) juga jebol kalau teks pola itu ada di command line yang lu kirim sendiri (heredoc atau `python -c` yang menyebut path-nya) — pkill-nya bunuh shell lu (exit `-15`, output kosong) dan server-nya malah ikut mati. Aman: pkill di dalam file script (`up.sh`) dan dijalankan lewat bash, atau kill by PID dari port yang dicek.
- Cron `script` WAJIB relatif terhadap `~/.hermes/scripts/` → wrapper tipis di sana, jangan path absolut.
- `chart_grid` minta array objek `{symbol,exchange}`, bukan array string.
- Plan Free OpenMarket: grid 1 sel, layout maks 2 pane → satu workspace per simbol (nama `Hermes <SYM>`, id di `meta.ws_<SYM>`).
- Slot plan = `min(MAX_OPEN - posisi terbuka, MAX_PLAN - plan pending)`; monitor menolak fill kalau posisi udah 3
  atau kas kurang (batal dengan alasan).
- `points` = 1 simbol per request; `markets` dengan `coins:[...]` balikin harga banyak simbol dalam 1 request (dipakai dashboard).
- mcp library butuh `httpx2.AsyncClient`; kolom candle `points` = `[t, open, high, low, close, volume]` (akses by index, bukan `o/h/l/c`).
- Kurva equity: monitor nulis snapshot tiap 15 menit, jadi API harus downsample 1 titik per jam (`WHERE ts IN (SELECT MAX(ts) FROM equity GROUP BY substr(ts,1,13))`) biar rentangnya hari, bukan cuma 2 hari terakhir.
- Plan yang sudah dipublikasi ke user sebelum DB ada: seed ke `trades` dengan `created_at`/`expire_at` asli, jangan mulai dari nol — dan kalau level entry-nya sudah berada di harga saat dipublikasi, tulis apa adanya bahwa limitnya kena di situ (jangan dipresentasikan sebagai fill normal di harga plan).
- PIL/numpy tidak ada di system python → kalau perlu cek PNG, pakai parser murni.
- Bentuk `/api/state`: angka akun ada di dict `account` (`equity`, `cash`, `positions_value`, `unrealized`,
  `open_risk`, `n_open`, `max_open`, `ret_pct`, `realized`) dan statistik di `stats` (`closed`, `wins`,
  `losses`, `win_rate`, `avg_r`, `realized`, `total_fees`). Top-level cuma `ts`/`age_s`/`open`/`plans`/
  `history`/`curve`/`events`/`btc`/`rules`/`live` — `d.get("equity")` balikin `None`, jangan simpulin
  equity-nya ilang. Untuk rangkuman ke user: equity + `ret_pct`, `cash` + `n_open`/`max_open`,
  `unrealized`, `open_risk`, lalu `closed`/`wins`/`losses`/`win_rate`/`avg_r` + fee.

## Verifikasi sebelum lapor

1. `./venv/bin/python scan.py --dry` — cek plan masuk akal (stop 1–2,5 ATR, RR ≥2).
2. `./venv/bin/python monitor.py` — harus sunyi kalau tidak ada kejadian.
3. `curl -s localhost:8793/api/state | head -c 400` + URL publik `…/` (title `Hermes Trade`) dan `/api/state` 200.
4. Kalau yang ditanya soal dashboard-nya: buka URL publik di browser dan baca DOM yang sudah dirender (`js("document.getElementById('eq').textContent")`, `#body` innerText), bukan cuma status 200 — lalu kirim screenshot-nya ke user sebagai bukti.
5. Baru lapor: apa yang jalan, link dashboard, aturan main, apa yang belum (posisi masih menunggu entry).
