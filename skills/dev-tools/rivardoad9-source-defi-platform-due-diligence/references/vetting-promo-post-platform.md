# Vet platform DeFi dari post promo — tanpa connect wallet

Dipakai kalau user drop link X/post yang isinya promosi tool/pool/platform LP ("part 3 strategi gw",
"tool ini satu-satunya yang bisa…"). Tujuannya: keluarkan rating, fee asli, dan sinyal monetisasi
promotornya — **tanpa** connect wallet apa pun.

## 1. Ambil post + media

```bash
curl -s "https://api.fxtwitter.com/<user>/status/<id>" -o post.json   # .tweet.text/.author/.media
curl -sL "https://pbs.twimg.com/media/<file>.jpg?name=orig" -o ss.jpg # nama file ada di post.json
```

Lalu `vision_analyze` tiap gambar (angka, label dashboard, dan — kalau ada — URL di address bar).
Screenshot sering memuat angka yang tidak ada di teks post (fee, liq, mcap, PnL).

## 2. Bongkar bundle app-nya (langkah paling produktif)

SPA biasanya menyimpan fakta yang tidak ada di halaman mana pun:

```bash
curl -sL https://<domain>/ -o page.html       # cari <script src=".../assets/index-*.js">
curl -sL https://<domain>/assets/index-*.js -o app.js
```

Yang dicari di `app.js`:

| pola | artinya |
|---|---|
| `*-docs.<host>` / `docs.` | host dokumentasi resmi (sering hardcoded, tidak ada di navigasi) |
| `t.me/<name>` | grup Telegram komunitas → cek `https://t.me/s/<name>` (kosong = red flag) |
| `referr` | sistem referral/afiliasi → indikasi promotor punya insentif |
| `ladderFee` / `"Charged by the <X> contract"` | fee yang dipotong kontrak mereka |
| `"no fee"` / path non-Zap | jalur yang BEBAS fee (biasanya create manual dua-sisi) |
| `setApprovalForAll` + warning text | mereka peduli approval berbahaya (sinyal plus) |
| `permit2`, `wagmi`, `rainbowkit` | non-custodial standar |
| `0x6131b5fae19ea4f9d964eac0408e4408b66337b5` | KyberSwap MetaAggregationRouterV2 (routing swap) |
| `/api/...` paths | probe `<domain>/api/<x>/health` dan `/config` — sering tanpa auth |

Probe endpoint terbuka (contoh nyata: `/api/zap/health` → `enabled:true`, `supported_chains:[1,56,4663,8453]`;
`/api/migrate/health` → `enabled:false` = fitur yang diiklankan justru mati).

## 3. Fee diambil dari docs, bukan dari caption

Docs biasanya memisahkan tier **gratis** (fee per operasi) vs **berbayar** (subscription + invite code).
Cek khusus: apakah *create* biasa (dua token dari wallet) bebas fee sementara *Zap In* kena fee —
itu angka yang menentukan untung/rugi, dan promotor biasanya cuma menyebut yang kecil.

## 4. Traction & verifikasi independen

- Profil X: followers, **tanggal join** (`api.fxtwitter.com/<handle>`) — tool umur 5 bulan dengan 318
  follower ≠ "sudah terbukti".
- DefiLlama: tidak ada halaman protokol = **nol data TVL independen**.
- Audit: cari kata `audit` di docs; tidak ada = tidak ada.
- Komunitas: Telegram/Discord kosong = distribusi masih 100% dari KOL berbayar.

## 5. Yang wajib masuk laporan

1. **Sinyal monetisasi promotor** — referral share / invite-gated tier / akun platform yang meng-amplify.
   Sebut sebagai inferensi + buktinya, jangan tuduh tanpa bukti.
2. **Provenance bukti PnL** — kalau screenshot PnL datang dari dashboard tool yang dipromosikan, itu
   klaim pihak yang berkepentingan, bukan data on-chain. Cari konsistensi internal angkanya.
3. **Tabel fee per operasi** + biaya round trip dibanding target harian promotor.
4. **Rating per use case** (strategi / tool / traction), bukan satu skor gabungan.
5. **Test plan terbatas** kalau user mau coba: wallet eksternal baru, chain likuid, jalur bebas fee,
   ukuran kecil, dan metrik pembanding vs incumbent yang sudah dipakai user.

## Contoh nyata (Liquidity Ladder, 29 Sep 2026)

Post @DankoWeb3 (4.938 follower) → punchline @liquidityladder. Bundle mengungkap referral
(`"your share of ladder fees from the people you invite"`, panel admin `Owed to referrers`) +
paid tier invite-gated → promosi ini punya insentif. Docs: free-tier `0,1%` (Zap In) + `0,5%`
(swap via aggregator), **create dua-sisi biasa 0% fee**. Tidak ada di DefiLlama, tidak ada audit
publik, Telegram kosong, `migrate` API mati. Screenshot "PnL" promotor konsisten-tidak-konsisten
(1.622 trades vs 913W+159L = 1.072) dan `Open Invested $2.185` > modal yang diklaim $1.000.

## Pitfall

- Jangan pakai klaim "satu-satunya tool yang bisa X" sebagai fakta; bandingkan dengan incumbent user
  (Meteora DLMM sudah punya preset bid-ask, Arrakis/Gamma/Alchemii ada, bahkan PancakeSwap manual).
- Jangan simpulkan tool jelek hanya karena kecil — pisahkan *utility* (nyata: ladder 1 tx, dashboard)
  dari *traction* dan *verifiabilitas*.
- Kalau user sudah punya vault note DD untuk chain yang sama (mis. Robinhood Chain), sambungkan
  dengan link "Lihat juga" supaya konteksnya nyambung.
