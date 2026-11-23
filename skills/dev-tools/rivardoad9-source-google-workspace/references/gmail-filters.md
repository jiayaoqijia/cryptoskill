# Gmail: filter asli + sapu backlog

## Scope
`gmail.settings.basic` **tidak ada** di daftar SCOPES setup.py default. Tanpa itu
`users.settings.filters().*` balas 403. Cara nambah: sisipkan scope-nya ke SCOPES,
lalu `--auth-url` / `--auth-code`. Minta SEMUA scope lama sekalian, kalau tidak
token baru bakal mencabut izin calendar/drive/documents yang sudah jalan.

## Bikin filter
```python
svc.users().settings().filters().create(userId="me", body={
    "criteria": {"from": "alamat@domain.com"},          # satu alamat = paling andal
    "action": {"addLabelIds": [label_id],
               "removeLabelIds": ["INBOX", "UNREAD"]}})   # UNREAD = mark as read
```
- Kriteria `query` boleh, mis. `"from:bitget.com"`, tapi **hanya untuk domain yang
  isinya marketing dari ujung ke ujung**. Domain campuran (marketplace, bank,
  maskapai) jangan: notifikasi pesanan/pengiriman satu domain bisa kesapu juga.
- **Filter tidak berlaku mundur.** Pesan lama harus disapu terpisah:
  `messages().list(q="from:X")` lalu `messages().batchModify(removeLabelIds=["INBOX"])`.
- Rerun harus idempoten: Gmail **tidak** menolak filter duplikat. Baca dulu
  `filters().list()` dan bandingkan (criteria, label, removeLabelIds) sebelum create.
- Ada `--rebuild` (hapus semua filter lalu bikin ulang) buat kasus logika aksi berubah.
- Aksi harus ditentukan dari **asal daftar pengirim**, bukan dari nama labelnya:
  label yang sama bisa dipakai dua-duanya (mis. "Kripto" punya yang diarsipkan dan
  yang harus tetap di inbox). Bug ini sempat kejadian: alert keamanan exchange
  kena "skip inbox" gara-gara cek-nya `if lab in RULE`.

## Kuota (yang bikin kerjaan gagal)
- `403 Quota exceeded for quota metric 'Total Query Cost' ... Units per minute per user`
  muncul setelah kira-kira 1.000 `messages().get` cepat, atau beberapa ratus
  `messages().list`. Jeda 1-2 menit sudah cukup pulih. Sapu 100+ pengirim beri
  `time.sleep(0.25)` per pengirim.
- Jangan census seluruh mailbox pakai `messages().get` per pesan untuk inbox
  puluhan ribu: kena limit dan lama. Kalau butuh daftar pengirim, trik yang jalan:
  `list` per domain kandidat (`from:domain`) lalu `get` metadata cuma subset itu.

## Jebakan teknis lain
- Batch endpoint lama `https://www.googleapis.com/batch` sudah 404. Yang hidup:
  `https://gmail.googleapis.com/batch/gmail/v1` (set `batch_uri=`).
- `ThreadPoolExecutor` dengan satu objek service googleapiclient = **SIGSEGV**
  (klien HTTP-nya tidak thread-safe). Pakai batch atau sekuensial.
- `messages().list(maxResults=500)` + `pageToken` buat hitung inbox; jangan pakai
  `resultSizeEstimate`, angkanya ngawur (sempat balas 23.876 padahal 19.5 ribu).

## Sapu unread massal ("bikin semua read")
Pola yang jalan untuk puluhan ribu pesan:
```python
ids = semua `messages().list(q="is:unread", maxResults=500, pageToken=tok)`
for chunk in 500-an: svc.users().messages().batchModify(userId="me", body={
    "ids": chunk, "addLabelIds": [], "removeLabelIds": ["UNREAD"]}).execute()
```
- **Jangan** `messages().get` per pesan, dan **jangan** hapus/pindah apa pun: yang
  dilepas cuma bendera UNREAD, isi dan lokasi pesan tetap. Bilang itu ke user
  sebelum jalan — di situ izinnya datang.
- 23,5 ribu pesan selesai dalam ~2 menit (48 halaman list + 47 batchModify) dan
  masih jauh di bawah kuota. Aman dijalankan sekali per sesi pembersihan.
- Jalankan **setelah** filter terpasang, bukan sebelumnya: filter cuma nandain yang
  baru masuk, jadi urutan yang benar itu bersihin dulu, pasang filter, baru sapu unread.
- Alasan yang bikin ini layak dikerjakan, sebutkan ke user: selama backlog unread
  numpuk, badge unread nggak punya arti. Setelah nol, unread balik jadi sinyal
  (cuma nambah kalau ada email baru di luar daftar yang difilter).

## Verifikasi (jangan cuma bilang sukses)
1. `filters().list()` -> hitung ulang; cek **tidak ada** pengirim di daftar
   "tetap di inbox" yang punya `INBOX` di removeLabelIds.
2. `labels().get()` per label -> `messagesTotal` / `messagesUnread`.
3. `count("in:inbox")` sebelum vs sesudah, plus `count("is:unread")` kalau abis sapu
   unread (target 0). Indeks Gmail bisa telat beberapa menit, jadi angka sesisir
   boleh beda sedikit dari jumlah pesan yang dipindah.
4. Simpan aturan sebagai satu file data (`gmail_rules.py`) dan impor dari script
   filter + script sapu, biar tidak ada dua daftar yang bisa berbeda.
