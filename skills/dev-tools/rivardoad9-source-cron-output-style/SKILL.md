---
name: cron-output-style
description: Use when writing any cron or alert message to the user.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [telegram, formatting, cron, alerts, notifikasi]
---

# Gaya output seragam (cron → Telegram)

## Kapan dipakai

Setiap pesan yang user terima dari cron atau script alert — briefing berita, Trade Radar,
Deep Dive, scorecard, alert zona entry, alert berita HIGH, kartu sinyal LP. Tujuannya:
semua kanal (@HermsNews_Bot, DM user, @zemiztradebot) punya grammar visual yang sama,
ringkas, dan langsung kebaca.

## Aturan (keputusan user 5 Okt 2026)

1. **Baris 1 selalu** `<emoji> JUDUL` — satu baris, maks ~50 char, boleh KAPITAL.
2. **Isi**: bullet `• `; beberapa field dalam satu baris dipisah ` · `; antar blok maksimal
   **1 baris kosong**. Tanpa tabel/box ASCII (`===`, `---`), tanpa `**bold**` bertumpuk.
3. **Angka**: persen 1 desimal (`+2,1%`), harga `$1.234`, waktu **selalu WIB**
   (`05 Okt 20:00 WIB`) — jangan campur UTC dan WIB dalam satu pesan.
4. **Kaki pesan** (2 baris, urutan ini):
   `🕒 <dd Mon HH:MM> WIB` lalu `📊 <regime makro>` dari `~/.hermes/data/market_regime.json`
   (pakai `verdict` + `btc_d` + `breadth7`). Regime **wajib** di tiap pesan setup/alert.
   **Regime cuma untuk pesan market.** Alert non-market — harga NFT/holdings di wallet, saldo akun,
   status proyek, hasil tugas — panggil `finish(..., add_regime=False)` atau CLI `--no-regime`.
   Nempelin `📊 BTC.D …` di alert NFT bikin pesannya kebaca template dan nggak nyambung sama isinya.
5. **Panjang**: alert/setup 3–8 baris; laporan & kartu sinyal boleh lebih panjang tapi
   formatnya sama. Buang basa-basi ("semoga membantu", "berikut laporannya"), tanpa hashtag,
   tanpa emoji beruntun.
6. **Jujur**: data kosong/gagal ditulis apa adanya (`data GMGN 429, konfirmasi tipis`) —
   jangan diisi angka karangan. Khusus metrik: field yang gagal diambil **jangan pernah dibiarkan
   jatuh jadi `0`** — `0` kebaca sebagai angka asli dan ikut ngitung di verdict, jadi kesimpulannya
   bisa kebalik (kasus nyata: dominasi gagal diambil → `BTC.D 0.0%` → verdict berubah dari headwind
   jadi tailwind, padahal aslinya headwind). Hilangkan fieldnya atau tulis `n/a`; perbaikan akarnya
   di script penghasil cache (`market_regime.py`: hitung dari sumber kedua dengan basis yang sama, atau
   `None` + verdict "data nggak lengkap").
7. **Bahasa**: Indonesia santai (gw/lu) untuk DM user; istilah teknis dibiarkan apa adanya.

## Helper yang sudah terpasang

```python
# Python
from msgstyle import finish           # ~/.hermes/scripts/msgstyle.py
teks = finish(teks, kind="alert")     # kind: alert | card | report | news | info | warn
```

```bash
# Bash / stdout cron (no_agent)
printf '%s\n' "$MSG" | python3 ~/.hermes/scripts/msgstyle.py --kind alert
# opsi: --kind report --no-time --no-regime --title "FLOWMETRIX" --emoji 🎯
```

Script yang sudah lewat msgstyle otomatis: `news_send.py`, `fm_engine_bot.py`
(kartu sinyal + caption chart), `fm_bot_bridge.py`, `gaming_entry_alert.py`, `pump_alert.py`,
`fm_manual_lp_monitor.py`, `news_pause_nudge.sh`, `narr_rotation_cron.sh`,
`winner_study_cron.sh`, `sty_ds_balance.sh`, `sty_news_tick.sh`.

## Contoh pesan jadi

```
🟢 ILV — masuk ZONA ENTRY ($12.40–12.90)
   Target: $15.20 · Invalidation: < $11.80
   Vol 24j naik 2,1x, shelf valid. Eksekusi CEX, SL manual.

🕒 05 Okt 08:24 WIB
📊 BTC.D 59,3% · breadth 18% · HEADWIND buat setup alt
```

## Gaya reminder pribadi (koreksi user 9 Okt 2026)

Reminder ke user BUKAN pengumuman instansi — user minta "jangan kayak robot, lebih natural".
Aturan praktis:

- Buka dengan nyebut nama + barangnya: `📌 Do, Rakamin ... masih keinget kan?`
- Fakta (tanggal, biaya, benefit) ditulis sebagai kalimat biasa, bukan tumpukan label
  (`Deadline:`, `Output:`, `Biaya:`). Heading KAPITAL diganti kalimat ("Jadwalnya 24–25 Okt").
- Sebut risikonya kalau kelewat + opsi lain yang masih kebuka.
- Tutup dengan tawaran nemenin: `bilang "gas <kata kunci>" gue temenin ...`
- Tetap tanpa bullet `-`, tanpa tabel, tanpa baris `===`/`---`.
- **Jangan** tempel baris `🕒`/`📊 regime makro` di reminder pribadi — itu buat alert market.
- Reminder script-only (`course_remind_*.sh`, `dawn_reminder.py`): edit isi heredoc/teksnya
  langsung, jangan bikin wrapper baru. Contoh yang sudah benar: `dawn_reminder.py`.

## Pitfall

- **Baris 📊 regime TIDAK otomatis ditambahkan untuk `kind=report`** — `finish()`/CLI hanya menempelnya untuk `alert|card|signal|news` (cek `msgstyle.py` ~line 158). Untuk laporan, tulis sendiri baris `📊 …` di body (kalau body sudah punya 📊, `finish()` tidak menduplikasi). Pola aman: script data-collector ikut mencetak "FOOTER SIAP TEMPEL" dari `market_regime.json` (`verdict` + `btc_d` + `breadth7`), agent tinggal menempel.
- Jangan menambah baris kosong di awal pesan (Telegram bikin spasi jelek).
- Teks > 18 baris dianggap laporan → tidak dipotong (jangan paksa jadi 8 baris, isinya hilang).
- Caption foto dibatasi 1024 char; caption kartu sinyal sudah dipotong otomatis.
- Kalau menambah lane baru: panggil `finish()` **atau** pipe lewat CLI, jangan bikin format sendiri.
