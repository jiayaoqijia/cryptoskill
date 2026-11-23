# Watchlist akun sosial (X) — delta-only, tanpa API key

Use when user bilang *"tambahin CT ini ke watch list lu"*, *"mantau akun ini"*, *"gw mau dikabarin
kalau dia posting"*. Aturan user: **notif HANYA kalau ada post baru** — tick tanpa perubahan harus
sunyi total.

## Langkah 0 — pilih bentuk job-nya: script bisa nembak sumbernya sendiri?

| Sumber bisa difetch deterministik oleh script biasa? | Bentuk | Kenapa |
|---|---|---|
| Ya (`t.me/s/<ch>`, RSS, API keyless) | `no_agent=true` + script, atau `monitor_script` | 0 token; tick tanpa perubahan = sunyi |
| Tidak — cuma bisa lewat tool agent (`web_search`) | cron **agent-run** + state file `seen` | script nggak punya `web_search`; `monitor_script` nggak kepakai |

Kasus 1 Okt 2026 (@Proxonchain): discovery X **cuma** jalan lewat `web_search("site:x.com/<screen>")`
(rute scraping lain tidak stabil dari server ini) → agent-run. Kalau nanti ketemu endpoint keyless
(RSS/JSON) untuk sumber yang sama, pindah ke `no_agent`/`monitor_script`: lebih murah dan tetap sunyi.

## Bentuk agent-run yang dipakai (proven)

- `schedule="0 */3 * * *"`, `deliver=origin`, `enabled_toolsets=["web","terminal","file"]`.
- State: `~/.hermes/data/<name>_seen.json` = `{"seen": [<post_id>...], "capped": 300}`.
- Prompt self-contained berisi 5 langkah:
  1. `web_search("site:x.com/<screen>", limit=10)` → kumpulin semua URL `status/<id>` + judulnya.
  2. Baca state; id yang belum ada di `seen` = post BARU.
  3. Kalau tidak ada id baru: tulis semua id ke `seen`, balas dengan **teks KOSONG** (jangan kirim
     pesan apa pun, jangan mengarang).
  4. Kalau ada (maks 5/run): `curl -s https://api.fxtwitter.com/<screen>/status/<id>` → teks +
     media, **verifikasi klaimnya** (pakai `analyst-claim-verification` →
     `references/onchain-flow-alarm-claims.md`), lapor ≤900 char/post + link aslinya.
  5. Update `seen` (cap 300 id terbaru).
- Aturan keras di prompt: jangan eksekusi trade apa pun; jangan ngarang angka/tx hash/alamat —
  kalau data nggak ketemu tulis "nggak bisa diverifikasi"; kalau post barunya cuma retweet/reply
  kosong, masukkan id ke `seen` dan balas kosong.

## Baseline seeding (jangan dilewat)

Sebelum bikin job, isi `seen` dengan ~10 id terakhir (dari hasil `web_search` + link yang user
kirim di chat). Tanpa ini, run pertama = laporan 10 post lama sekaligus — persis spam yang user
minta dihindari. Tulis juga catatan kecil di file state biar sesi berikutnya tahu itu baseline.

## Freshness — sebut apa adanya, jangan janji realtime

`site:x.com/<screen>` index-nya lag jam–hari: 1 Okt 2026 dua post terbaru (yang justru dikirim
user) belum keindeks, sementara 8 post lama muncul lengkap. Bilang "ketauan telat beberapa jam",
dan minta user tetap drop link kalau nemu duluan. Sisi bagusnya: **judul hasil search sudah berisi
potongan teks post** → cukup buat screening, fetch fxtwitter buat teks utuh.

## Job yang sudah ada

- `63e55c0b5cfd` — "X watch: @Proxonchain (on-chain flows)", `0 */3 * * *`, agent-run,
  state `~/.hermes/data/proxonchain_seen.json` (proven 1 Okt 2026).
