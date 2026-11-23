# Menindaklanjuti cron job yang GAGAL (atau yang diam-diam bohong)

Dua mode kegagalan cron yang harus dibedakan, dan cara membacanya.

## 1. Job gagal terang-terangan → baca file output-nya

`cronjob action=list` menampilkan `last_status` per job. Sweep cepat: cari semua job dengan
`last_status: error` — jangan tunggu user menanyakan.

Output tiap run disimpan per job:

```
~/.hermes/cron/output/<job_id>/<YYYY-MM-DD_HH-MM-SS>.md
```

Isinya: `**Status:** script failed`, exit code, dan **stderr** yang sebenarnya — ini yang
menjelaskan sebabnya, sedangkan `cronjob list` cuma bilang "error". Baca 2-3 file terbaru untuk
melihat apakah kegagalannya berulang atau sekali.

```bash
ls -t ~/.hermes/cron/output/<job_id>/ | head -3
cat ~/.hermes/cron/output/<job_id>/<file-terbaru>.md
```

⚠️ Kalau `ls`-nya di-pipe ke `tail`/`head`, exit code yang dilaporkan adalah exit code pipe —
jangan simpulkan "job sukses" dari situ.

## 2. Job SUKSES tapi keluarannya bohong (lebih berbahaya)

`no_agent` script yang menelan kegagalan parse/logika dan tetap keluar dengan exit 0 akan
mengirim laporan "tidak ada apa-apa" — dan bagi operator itu tidak bisa dibedakan dari keadaan
normal. Contoh nyata 17 Sep 2026: rekap harian menulis "tidak ada cycle baru" **tiga hari**
karena regex format log-nya basi (75/612 baris terbaca), tanpa error apa pun.

Aturan desain yang lahir dari itu:

- **"Nol" bukan hasil netral.** Setiap langkah yang bisa gagal harus punya jalur alarm eksplisit
  (mis. "format log berubah", "alat ukur gagal"), bukan jalur "diam".
- **Bedakan "alat ukur gagal" dari "objeknya rusak"** — dua-duanya pernah jadi alarm palsu di
  stack ini (RPC 500 dipanggil `chain anomaly`; UTC dibaca sebagai WIB dipanggil "engine mati").
- **Watermark jangan berupa hitungan baris** kalau sumbernya file yang bisa di-rotate — pakai
  pasangan id/tipe data (`{"db_max_id": …, "log_lines": …}`) supaya rotate tidak menggeser window.
- **Prefer sumber data terstruktur (DB) daripada parse teks log** untuk job rekap; teks log
  format-nya milik aplikasi lain dan bisa berubah tanpa pemberitahuan.

## 3. Cron yang menyentuh repo git yang dipakai bersama

Job yang commit/push di worktree LIVE harus **fail fast sebelum efek samping apa pun** kalau
premisnya tidak terpenuhi (mis. bukan di branch `main`) — dieksekusi sebagai guard-dulu, bukan
verifikasi-sesudah. Contoh lengkap + harness uji tanpa menyentuh worktree live:
`flowmetrix-ops → references/nightly-export-branch-guard.md`.

## Checklist singkat saat "kok ga ada kerja?" / "cron-nya jalan ga?"

1. `cronjob action=list` → job apa yang `last_status: error`, mana yang `paused`, mana yang
   `next_run_at`-nya di masa lalu (artinya tidak pernah fire).
2. Untuk setiap error: baca file output-nya, kutip stderr-nya.
3. Untuk job yang "sukses tapi hasilnya kosong": cek apakah sumber datanya benar-benar dibaca
   (jumlah baris/row yang diparse vs yang ada) — jangan percaya output kosong begitu saja.
4. Baru simpulkan, dan sebutkan job id + nama file buktinya.
