# Sizing arithmetic: "wise nggak masukin X% ke <token>?"

Referensi ini lahir dari pertanyaan user 28 Sep 2026: *"wise ga gw masukin 5% aster"*.
Pertanyaan seperti ini **bukan** pertanyaan DD token — ini pertanyaan alokasi, dan
jawabannya harus keluar dari aritmatika posisi, bukan dari narasi proyek.

## Dua perkalian yang wajib dihitung dulu

```
$ posisi        = pct × buku            # 5% × $1.400 = $70
mcap sekarang   = price × total_supply  # hitung SENDIRI, jangan percaya label
target mcap     = mcap × multiple       # 10x dari $5,7B = $57B
```

Contoh nyata (ASTER, BSC, 28 Sep 2026): harga ~$0,717 · supply 8B → mcap ≈ **$5,74B** →
5% dari buku $1,4k = **$70**. Verdict jujur: **bukan upside play** — nominalnya nggak ngaruh
ke hasil, dan butuh 10x berarti mcap $57B. Yang benar dilaporkan: "ini bukan 'nggak boleh',
tapi nggak nyambung sama tujuan upside maksimal lu" + sebut sleeve-nya harus dari mana
(bukan bucket LP) dan apa yang tergantikan.

## Jebakan data (semua kelihatan nyata di sesi itu)

- **`gmgn-cli token info` `stat` bisa balik `market_cap`/`holder_count`/`ath_price` kosong
  atau `0`.** Itu **bukan** berarti tokennya nggak punya market cap — `price` +
  `total_supply` ada di payload yang sama, kalikan sendiri. (Hindari juga mencetak field
  yang isinya dict: `price` di payload itu objek dengan `price/price_1h/price_24h/volume_*`,
  jadi `symbol`/`price` harus digali ke dalam.)
- **Angka `liquidity` satu pool ≠ likuiditas token.** ASTER: $1,3M line vs mcap $5,7B
  (0,02%) karena venue-nya perp DEX yang tersebar di banyak pool + CEX. Jangan dipakai
  buat bilang "likuiditasnya tipis" — bilang terus terang bahwa angka itu nggak representatif
  untuk token multi-venue.
- **Istilah "circulating supply" dari aggregator sering = total supply.** Kalau `circulating`
  persis sama dengan `total`, jangan simpulkan "bebas unlock" — artinya cuma "data ini nggak
  ngasih tau jadwal unlock". Kalau unlock/vesting nggak bisa diverifikasi dari data yang ada,
  **bilang nggak bisa diverifikasi**, jangan diam-diam dianggap aman.

## Cara menyampaikan

1. Harga + mcap (sebut cara ngitungnya) + nominal $ dari persen yang ditanya.
2. Satu kalimat verdict yang nyambung ke **tujuan** user (di sini: upside maksimal), bukan
   ke kualitas proyeknya.
3. Sleeve asal + apa yang digantikan + aturan yang tetap berlaku (LP bucket jangan dipakai
   buat spekulasi).
4. Kalau ada yang nggak bisa diverifikasi (unlock, tesis fee-share), sebut eksplisit.
