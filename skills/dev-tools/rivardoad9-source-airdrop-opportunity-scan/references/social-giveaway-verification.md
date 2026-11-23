# Undian sosial / post-to-earn harian — verifikasi menang & pengingat

Dipakai kalau kampanye bukan "farm lalu tunggu TGE", tapi **draw harian**: syaratnya posting tiap hari,
pemenang diundi, hadiah dikirim langsung ke wallet. Contoh kelas ini: Proof of Agent (Ptah), dan
program sejenis dari agent wallet / NFT card.

## 1. Identitas peserta diambil dari kontrak, bukan dari situs

Situs sering nampilin contoh/nomor demo di preview post. Jangan pernah percaya angka itu.
Baca langsung dari kontrak kampanye:

```python
# selector tokenOf(address); ganti sesuai kontrak
w.rpc("eth_call", [{"to": CAMPAIGN, "data": "0x<selector>" + wallet[2:].lower().rjust(64, "0")}, "latest"])
```

Nomor yang balik dari `tokenOf` / `agentOf` / `balanceOf` itulah yang harus ada di teks post.
Kalau nomor di post beda dengan on-chain, wallet-nya nggak dihitung walau postingnya rapi.

## 2. Jendela waktu: hitung dari perilaku situs, bukan dari teks FAQ

FAQ resmi bisa meleset satu hari dari jadwal yang benar-benar jalan. Cara memastikan:

1. Buka kartu hari yang sedang jalan. Kalau tertulis **"output complete · awaiting draw"** padahal
   jam tutup nominal belum lewat, berarti snapshot ditutup **sehari sebelum** draw — bukan 24 jam
   sebelum draw seperti yang biasa ditulis di FAQ.
2. Cocokkan dengan label rentang tanggal di kartu hari sebelumnya (`Day N · <tgl A>–<tgl B> output`)
   dan jam draw yang tertulis. Dua data itu yang dipakai, bukan prosa FAQ.
3. Simpan hasilnya sebagai fungsi waktu (window start = boundary UTC terakhir, draw = boundary + 2 hari)
   supaya pengingat otomatis nggak salah label.

Kalau pernah bilang ke user "post lu hangus" lalu ternyata masuk: akui salahnya di kalimat pertama,
sebut alasan koreksinya (jendela tutup jam berapa vs jam post), baru lanjut. User membaca koreksi
eksplisit sebagai reliability.

## 3. Menang atau tidak: cek transfer masuk, bukan daftar pemenang

Hadiah dikirim langsung, tanpa claim. Jadi bukti menang = ada transfer token hadiah ke wallet.

```python
pad = "0x" + "0" * 24 + wallet[2:].lower()          # topic2 = penerima
logs = logrpc("eth_getLogs", [{"address": PRIZE_TOKEN,
        "fromBlock": hex(start), "toBlock": hex(end),
        "topics": [TRANSFER, None, pad]}])
```

- Chunk 20.000 blok per panggilan; window 300–400 ribu blok cukup buat kampanye beberapa hari.
- Nol log = belum menang. Saldo token juga 0 = konfirmasi kedua.
- **Jangan** mengandalkan daftar pemenang di halaman: list-nya virtualized, cuma belasan dari
  ratusan yang ter-render, jadi "nggak ketemu nama gw" bukan bukti apa-apa.

## 4. Pengingat harian yang senyap kalau sudah posting

Cron 2x sehari (mis. 12:30 dan 20:30 WIB) yang **memeriksa dulu** sebelum bicara:

1. Ambil timeline akun: `https://r.jina.ai/https://x.com/<handle>` dengan header `x-no-cache: true`.
2. Ambil status id terbaru, lalu waktu pastinya: `https://api.vxtwitter.com/<handle>/status/<id>` →
   `date_epoch`. Jangan pakai label relatif ("5h") — itu bisa meleset beberapa jam.
3. Kalau ada post ber-hashtag wajib setelah window start: keluar tanpa output (senyap).
4. Kalau belum: kirim reminder berisi nomor hari, jam tutup dalam WIB, sisa jam, satu draf siap
   copy, dan pengingat "post baru, bukan reply".
5. Rotasi 3–4 varian draf biar timeline nggak kelihatan copy-paste; teks wajib: hashtag kampanye,
   handle resmi, nomor peserta dari kontrak.
6. Matikan sendiri setelah hari terakhir (`n > total_hari` → return 0), jangan minta user mematikan.

## 5. Angka yang wajib disebut saat melapor

Peserta hari itu, hadiah per pemenang dalam token + USD, peluang = pemenang/peserta, jam tutup
persis dalam WIB, dan hari ke berapa dari total. Peluang 2–5% itu normal — bilang apa adanya,
jangan bikin kelihatan lebih besar dari kenyataannya. Hadiah receh ($20-an) disebut nominalnya,
bukan cuma "bonus".

## 6. Kalau menang, jangan langsung senang

Token hadiah biasanya tipis likuiditas dan baru listing. Sebelum nyaranin jual, cek pool dan
kedalaman bid; kalau nggak ada venue, sebut itu sebagai kendala, bukan "profit".
