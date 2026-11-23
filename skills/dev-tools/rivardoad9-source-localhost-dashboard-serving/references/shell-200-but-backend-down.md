# Shell 200 tapi tiap `/api/*` 500 → backend proxy-nya mati (6 Okt 2026)

Keluhan user: *"aplikasi kita benerin, lg eror ga muncul"*. Halaman kebuka, angkanya kosong.
Ini pola paling sering untuk dashboard yang agent sendiri yang pasang: **UI dan backend itu dua proses**,
dan yang mati biasanya backend-nya. Jangan mulai dari membaca kode; mulai dari memisahkan dua lapis ini.

## 1. Pisahkan shell vs data (2 perintah)

```bash
curl -s -o /dev/null -w "%{http_code} %{size_download}b\n" -m 10 http://127.0.0.1:<port>/
# → 200 + ukuran HTML penuh = shell sehat, route & template hidup
for p in /api/health /api/status /api/logs; do printf "%-14s " "$p"
  curl -s -o /dev/null -w "%{http_code} %{size_download}b\n" -m 10 "http://127.0.0.1:<port>$p"; done
# → semuanya 500 = upstream proxy mati   |   404 JSON = route memang tidak ada (itu BUKAN bug)
```

Bedakan 404 vs 500: balasan `{"error":"no route for GET /api/positions"}` dari Fastify = server sehat,
endpoint-nya saja yang salah tebak. 500 seragam di semua `/api/*` = proxy gagal nyambung.

## 2. Baca log proses UI-nya, di situ alamat upstream-nya tertulis

```bash
pm2 logs <app> --lines 60 --nostream
# → Failed to proxy http://127.0.0.1:4000/api/status Error: connect ECONNREFUSED 127.0.0.1:4000
grep -rn "127.0.0.1:4000\|destination\|rewrites" next.config.*     # sumber alamat upstream
grep -rn "BASE_URL\|NEXT_PUBLIC" src/lib/api.ts                    # ← fetch client-side, penting
```

Catat dua hal: (a) **port upstream**, (b) apakah client memanggil `localhost:<port>` **dari browser**
(bukan lewat rewrite). Kalau ya, server sehat pun user bisa lihat kosong kalau jalur aksesnya tidak
mem-forward port itu — cek bind address (`ss -ltnp`: `127.0.0.1` bukan `0.0.0.0`) sebelum menyalahkan data.

## 3. Cari siapa yang seharusnya mendengarkan port itu

Standarnya: **proses itu di-start in-process oleh aplikasi lain** (mis. engine trading yang di-pause),
jadi matinya bukan crash — mati karena induknya memang stop. Cek `package.json` scripts (`"api": "node
--import tsx src/api/server.ts"`) dan `grep -rn "import .*api/server\|listen(" src/index.ts`.

Konsekuensi yang sering terlewat: **proses lain ikut mati** karena ikut menembak port itu (bot Telegram
`/status`, cron delta, keeper). Sebutkan ini di laporan, jangan cuma bilang "dashboard sudah normal".

## 4. Fix: nyalakan yang mati saja, jangan yang lain

- Kalau port itu milik proses berisiko (engine/trading), jalankan **backend-nya standalone** — jangan
  menyalakan induknya. Untuk FlowMetrix: `node --import tsx src/api/server.ts`, engine tetap stop.
- **Jangan `npm start` dari shell agent**: proses mewarisi env Hermes (insiden 10 Sep: bot poll 409).
  Pola aman = keeper script yang men-spawn dengan `setsid nohup … >>log 2>&1 </dev/null &` dari dalam
  file script, bukan inline panjang dari terminal agent. Jalankan dengan node yang sama seperti pm2
  (`pm2 describe <app> | grep interpreter`), dan `cd` ke root repo supaya loader `.env` (yang membaca
  `process.cwd()/.env`) ketemu.
- Pasang keeper `*/5` `no_agent` + `deliver=origin`, senyap kalau sehat, cetak hanya saat restart —
  ini kategori "keeper nol-risk" yang boleh aktif tanpa menunggu diminta
  (`hermes-cron-automation` → `references/lane-build-without-cron.md`).
- **Jangan** pakai ini sebagai alasan menghidupkan kembali lane yang user sengaja pause.

## 5. Verifikasi dua lapis

1. API langsung: `curl -s http://127.0.0.1:4000/api/health` → JSON nyata (`{"status":"ok"...}`), plus satu
   endpoint berisi data besar (`/api/funnel` ~108 KB) supaya yakin bukan cuma health-check kosong.
2. **Render di browser nyata** (chromium dari cache playwright + venv, viewport HP) → screenshot →
   `vision_analyze`. Yang dicari: angka/metric nyata, bukan spinner. Screenshot ini juga yang dikirim ke
   user sebagai bukti (Telegram `MEDIA:`), sekaligus jaring pengaman kalau laporan "sudah normal" salah.

## 6. Kalau user ternyata maksud aplikasi lain

Aplikasi yang mirip-mirip (beberapa dashboard/tunnel/job dalam satu mesin) membuat "aplikasi kita"
ambigu. Sebelum menjawab, scan cepat semua yang hidup (`ss -ltnp`, `pm2 list`, `ps aux | grep -E
"cloudflared|server"`) dan tutup laporan dengan penunjuk: "kalau yang lu maksud bukan ini, bilang".
Yang jangan dilakukan: mengklaim sudah diperbaiki tanpa menyebut aplikasi mana yang diperiksa.
