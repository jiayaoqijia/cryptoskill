# X / Twitter: membaca satu post tanpa login (verified 2026-09-14)

Dipakai kalau user nempel link `x.com/<user>/status/<id>` dan isinya harus dibaca. Urutan percobaan,
paling murah dulu — percobaan 1 yang biasanya langsung berhasil.

## 1. Syndication JSON — satu-satunya route yang benar-benar mengembalikan isi

```bash
curl -sL "https://cdn.syndication.twimg.com/tweet-result?id=<STATUS_ID>&lang=en&token=a" \
  -H "User-Agent: Mozilla/5.0" -o /tmp/tw.json
```

Field yang berguna: `.text`, `.created_at`, `.favorite_count`, `.conversation_count`,
`.display_text_range`, `.user.{name,screen_name,is_blue_verified}`,
`.entities.user_mentions[]`, `.mediaDetails[].media_url_https`, dan
`.quoted_tweet.{text,user,mediaDetails}` — **post yang di-quote ikut terbawa**, dan itu sering
bagian yang paling penting (keluhan/kerugian orang yang dibalas).

Tanpa `token` pun jalan (`token=a` cukup). Post reply biasa dan quote-post dua-duanya lengkap.

## 2. oEmbed — fallback HTML (butuh `-L`, endpoint-nya 301)

```bash
curl -sL "https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2F<user>%2Fstatus%2F<id>&omit_script=1"
```

Balikannya `{"author_name":..., "html":"<blockquote>…"}` dengan teks yang sama (juga terpotong).
Pakai kalau route 1 diblokir.

## 3. Media: unduh, jangan cuma dibaca URL-nya

`pbs.twimg.com/media/<file>` itu CDN publik (tanpa auth) → unduh, lalu **transkrip pakai vision**.
Screenshot di post promo hampir selalu membawa angka yang tidak ada di teksnya (dashboard, kartu PnL,
tabel pool, tombol, URL di address bar). Transkrip dulu "apa adanya", baru simpulkan.

Menarik juga: URL di address bar screenshot sering membocorkan hal yang tidak diomongkan penulisnya
(contoh nyata: post memuji sebuah bot, tapi screenshot-nya dari hostname **`*-dev.`**).

## 4. Yang tidak jalan untuk X (jangan buang waktu)

- `r.jina.ai/https://x.com/<handle>` (halaman PROFIL) **jalan**: balikannya seluruh timeline berisi
  teks post + semua `x.com/<handle>/status/<id>`. Route termurah buat "dia udah posting apa belum".
  Halaman satu post (`/status/<id>`) tidak konsisten — kadang login wall, kadang 403
  `AbuseAlleviationError`. Jangan simpulkan "post tidak ada" dari situ; pindah ke route 1.
- Render pakai browser butuh Chrome hidup; tiap kali browser gagal, `nitter.*` juga mati/000.
- `cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=<handle>` → balikannya kosong;
  `.user.followers_count` = null. **Jangan sebut jumlah follower** kalau tidak ada sumbernya.
- `https://x.com/<user>/status/<id>` sendiri balas 200 dengan shell JS (login wall client-side) —
  **jangan pernah simpulkan "post tidak ada" dari situ**.

## 5. Batas yang harus disebut, bukan ditutup-tutupi

- **Post long-form (X Premium)**: payload cuma bawa `.note_tweet.{id}`; **isi penuhnya tidak ada**, dan
  `.text` adalah preview terpotong (lihat `.display_text_range`, mis. `[0,271]` sementara kalimatnya
  menggantung). Bilang terus terang "teks utuhnya kepotong" + kutip yang kebaca, atau minta user buka di app.
- Rate/engagement yang aneh (fav 30, reply 4) itu fakta yang boleh dikutip — jangan ditafsirkan jadi
  "post ini tidak penting".

## 7. X Article / long-form `x.com/i/article/<id>` — TIDAK terbaca anonim (dicek 2026-09-29)

Kalau tweet-nya isinya cuma satu link (`text` = `https://t.co/...`), itu X Article. Yang bisa diambil:
`.article.title`, `.article.preview_text` (~200 char, sering menggantung), `.article.rest_id`, `.article.cover_media`.
Itu **satu-satunya** isi yang tersedia tanpa login — jangan mengarang sisanya.

| Jalur | Hasil (Sep 2026) |
|---|---|
| `curl https://x.com/i/article/<id>` | **404 shell** (halaman SPA error) |
| camoufox / Chromium headless (render JS) | "Hmm...this page doesn't exist" — X sengaja menyembunyikan artikel dari anonim, **bukan** artikelnya hilang |
| `api.fxtwitter.com/<user>/status/<id>` | ✅ **route terbaik**: metadata + replies/retweets/likes/**bookmarks**/quotes/**views** + `.article.*` |
| `api.fxtwitter.com/i/article/<id>` | 404 |
| `r.jina.ai/https://x.com/...` | 403 `AbuseAlleviationError` di halaman post (profil tetap jalan) |
| nitter | xcancel.com = 451 "service suspended" (legal); lightbrd.com = 403 Cloudflare; tiekoetter = Anubis PoW; poast/privacydev = mati/timeout. **Jangan buang waktu di nitter.** |

Browser headless yang siap di server (untuk halaman publik, login wall X tetap tidak tembus):
`~/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome`; venv dengan playwright+camoufox:
`~/.hermes/venvs/camoufox_venv/bin/python` (pola: scroll 20x lalu `page.inner_text("body")`).

Untuk artikel: minta user tempel teksnya / baca di app, lalu bedah klaimnya satu-satu terhadap data publik.
Metrik post sendiri tetap bisa dilaporkan (`bookmarks` > `likes` = pola "disimpen buat riset", bukan viral).

## 6. Yang dilaporkan ke user

Penulis + handle + flag verified, `created_at`, jumlah fav/reply, lalu teksnya. Untuk post promo:
**kalau tidak ada satu pun angka hasil di dalamnya, itu temuan** — sebut eksplisit ("pujiannya UI dan
harga fee; tidak ada PnL/APR/durasi/wallet"). Itu yang membedakan membaca dari ikut terpromosi.

## 8. Timeline satu handle + timestamp pasti (dicek 2026-10-29)

Pertanyaan "dia udah posting X apa belum" dijawab dari timeline, bukan dari ingatan atau dari label
relatif di render.

```bash
curl -s -H 'x-no-cache: true' "https://r.jina.ai/https://x.com/<handle>" | grep -o 'status/[0-9]\+'
curl -s "https://api.vxtwitter.com/<handle>/status/<id>"     # .date_epoch, .text
```

- Ambil id terbaru (Jina urut baru → lama), lalu `date_epoch` untuk jam pastinya. Konversi ke WIB
  (`+07:00`) sebelum menyebut jam ke user.
- Header `x-no-cache: true` penting: tanpa itu render bisa balik versi cache dan post yang baru masuk
  kelihatan belum ada.
- Label relatif ("5h") di render bisa meleset satu-dua jam. Kalau keputusannya bergantung pada batas
  waktu (window harian, cutoff), pakai epoch dan sebut jam absolutnya.
- Kalau id terbaru bukan post yang dicari (mis. reply tanpa hashtag), sebut itu apa adanya: "post
  terakhir jam X, tapi bukan yang diundikan" — jangan diam-diam menganggapnya sudah memenuhi syarat.
