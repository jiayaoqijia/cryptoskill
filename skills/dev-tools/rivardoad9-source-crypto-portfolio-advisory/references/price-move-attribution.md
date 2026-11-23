# "Kenapa X barusan dump/naik?" — atribusi gerakan harga (verified 28 Sep 2026)

Trigger: user lapor gerakan harga ("kenapa ondo barusan dump", "kenapa X naik") dan minta sebabnya.
**Jangan langsung cari berita — ukur dulu.** Urutannya: bandingkan → cari katalis → checklist struktur.

## Langkah 1 — idiosinkratik atau beta? (satu call yang menentukan segalanya)

Klines 1 jam untuk token **dan** peer-nya di jendela waktu yang sama:

```python
https://api.binance.com/api/v3/klines?symbol=ONDOUSDT&interval=1h&limit=48
```

Print: harga terakhir, %1j, %4j, %24j, "% dari high 24j", plus **bar horizontal per jam** (label jam WIB)
supaya jam jatuhnya kelihatan persis — jawaban "jam berapa" sering lebih berguna dari "kenapa".

Keputusan:
- Token turun **≈2x atau lebih dari peer** (BTC/ETH/SOL + peer sektor) → **idiosinkratik**, lanjut ke
  Langkah 2–3.
- Token turun setara market → **beta/makro**. Jawabannya bukan "kenapa token ini" tapi kondisi market
  (BTC kehilangan level kunci, likuidasi long, yield/geopolitik). Jangan paksa nyari berita token.

Contoh nyata (ONDO, 28 Sep 2026): puncak **$0,5947 jam 11:00 WIB** → **$0,5197 jam 14:00 WIB** =
**−12,6% dalam 3 jam** (dalam satu jam 13:00→14:00: **−8,7%**). Peer di jendela 4 jam yang sama:
BTC −0,6% · ETH −0,4% · SOL −1,3% · TAO −1,7% · ZEC −0,7% → **ONDO ~2x market = flush idiosinkratik**,
bukan beta. Nggak butuh asumsi apa pun, cuma dua fetch.

## Langkah 2 — cari katalis spesifik; "nggak ada headline" itu jawaban yang sah

Cari headline proyek-spesifik (agregator cuma buat tanggal; sumber primer tetap rujukan utama).
Kalau hasilnya "no clear X-only negative headline", **tulis itu apa adanya** — bukan kegagalan riset.
Justru itu yang membedakan flush posisi dari kerusakan fundamental.

## Langkah 3 — checklist 5 penyebab, semuanya terukur

1. **Profit-taking setelah run.** Hitung %7h/%30h + posisi di rentang 30h. Naik +28–36% seminggu
   (dari low $0,30-an) lalu turun 12% = normal, bukan kejadian.
2. **Long crowded di-flush.** Cari data likuidasi + level teknikal yang "semua orang lihat"
   (18 Sep 2026: ~$425 juta long likuidasi/24 jam, ≈$237 juta dalam satu jam saat BTC kehilangan $84K;
   ONDO kebagian ~$110K long likuidasi/jam — kecil, tapi arahnya benar).
3. **Overhang struktural.** Unlock terdekat sebagai **% float + tanggal**, DAN **preseden unlock
   sebelumnya**. Template baca (ONDO): unlock 18 Jan 2025 melepas 134% float →
   **−38% seminggu sebelum unlock, lalu +460% dalam 12 bulan**; unlock berikutnya 18 Jan 2027 =
   1,71–1,94 miliar ONDO (**35–36% float**). → De-risk pra-unlock itu **pola**, bukan vonis mati:
   tulis dua-duanya, jangan cuma yang serem.
4. **Team/whale-linked.** Deposit multisig terkait tim ke exchange / penjualan 30 hari. Kalau sumbernya
   analitik pihak ketiga, labeli "kecurigaan" dan sebut analisnya (gate.com: ~$4,42 juta deposit,
   kecurigaan ~$29,94 juta terjual 30 hari; aixbt: 7 whale geser 69 juta ONDO lebih awal).
5. **Governance.** Sengketa kendali stake besar, fee-switch belum diputus, sengketa yurisdiksi.

## Langkah 4 — output

Tulis berurutan: (a) angka gerakan + jamnya, (b) perbandingan peer → verdict idiosinkratik/beta,
(c) daftar penyebab dengan angka, (d) **implikasi posisi**. Di bagian (d):
- Kalau user masih pegang → sebut level yang penting (support/MA, level unlock, trigger review).
- Kalau user sudah keluar/TP → **konfirmasi pakai angka**, bukan pujian: "kalau lu tahan dari $0,5753
  (harga pas laporan gw) ke $0,5284 = −8,1%". Pujian tanpa angka nggak ada gunanya buat trader.
Simpan sebagai section di note portofolio berjalan (mis. `## 8b. ONDO flush 28 Sep + aturan re-entry`),
lengkap dengan link ke note alokasi.
