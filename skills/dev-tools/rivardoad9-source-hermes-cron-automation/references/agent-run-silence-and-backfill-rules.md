# Agent-run cron: konvensi sunyi `[SILENT]` + aturan backfill id

Dua koreksi yang cuma kelihatan setelah job-nya beneran jalan (run pertama `63e55c0b5cfd`,
1 Okt 2026). **Baca ini bareng `references/social-account-watchlist-delta-only.md` — file itu masih
menulis "balas dengan teks KOSONG" di langkah 3; instruksi itu SALAH dan digantikan di sini.**

## 1. Job agent-run selalu mengirim final response-nya

Kalau prompt bilang *"kalau nggak ada apa-apa, balas teks kosong"*, itu **nggak menyunyiin apa pun** —
output-nya tetap dikirim ke user. Yang jalan: Hermes sudah menyuntik konvensi sendiri di preamble
cron:

> SILENT: If there is genuinely nothing new to report, respond with exactly "[SILENT]" (nothing
> else) to suppress delivery.

Jadi:
- tulis di prompt: **balas PERSIS `[SILENT]`** (tanpa teks lain);
- **jangan** taruh instruksi tandingan ("balas kosong", "balas satu kata SKIP") — itu bikin run
  pertama ngirim placeholder;
- `[SILENT]` bukan `no_agent`-style empty stdout; beda mekanisme: `no_agent=true` + script sunyi
  lewat stdout kosong, job agent-run sunyi lewat final response `[SILENT]`.

## 2. Id X (snowflake) — backfill bukan post baru

Run pertama ngelaporin 4 post lama (Jul–Sep) yang telat keindeks search engine, padahal user cuma
mau post BARU. Aturan yang harus ada eksplisit di prompt:

> id yang belum ada di `seen` **DAN** nilainya LEBIH BESAR dari id tertinggi di `seen` = post BARU.
> id yang lebih kecil = BACKFILL → masukkan ke `seen`, jangan dilaporkan, jangan bikin laporan.

Bandingkan sebagai `int`. Berlaku umum buat sumber lain yang id-nya monotonik (tweet, msg Telegram).
Kalau user nge-drop link di chat, itu jalur paling fresh — perlakukan id-nya sebagai post baru.

## 3. Pola diagnosis: run pertama bocor ≠ job-nya salah

Kalau run pertama ngelaporin backfill atau placeholder: itu **bug prompt**, bukan bug job. Patch
prompt-nya (`balas [SILENT]` + aturan snowflake), lalu jalankan sekali lagi buat verifikasi —
jangan bikin job baru (langganan state `seen`-nya beda → spam dobel).
