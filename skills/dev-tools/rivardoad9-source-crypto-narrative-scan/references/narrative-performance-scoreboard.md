# Performance narasi = scoreboard PER TEMA (bukan audit screener)

Trigger: "performance narativе gimana", "L1 hari ini gimana, seminggu terakhir", "breakdown narasi
lain", "yang ga perform alasannya kenapa", atau user komplain "mana laporannya?" setelah kamu
mengirim laporan akurasi/signifikansi.

**Bedakan dua permintaan yang mirip** (salah baca di sini bikin user bilang "lu gagal paham"):
- *"performance narasi"* / *"breakdown narasi"* → tabel performa **tiap tema** (dokumen ini).
- *"audit akurasi"* / *"works atau ga"* / *"akurasi tebakan"* → audit screener-nya
  (`strategy-backtest-validation` → `references/signal-audit-loop.md`). Jangan balas yang ini
  kalau yang diminta per-tema.

## Script (jangan tulis ulang definisi tema)

`~/.hermes/scripts/diag/narr_perf.py` — impor modul detektor supaya bucket tema satu sumber:

```python
spec = importlib.util.spec_from_file_location(
    "nre", os.path.expanduser("~/.hermes/scripts/narrative_rotation_early.py"))
nre = importlib.util.module_from_spec(spec); spec.loader.exec_module(nre)
hist = json.load(open(os.path.join(nre.DATA, "narr_hist_cache.json")))
ts, M, out = nre.build(hist, 90)      # out[theme] = {members, ret[], vol[]}, equal weight
i = len(ts) - 1                        # r1 di indeks terakhir = candle HARI INI (masih jalan)
t7 = nre.cum(out[th]["ret"], i, 7)     # pakai cum() modul itu, jangan hitung sendiri
```

Metrik per tema:
- `r1 / r3 / r7 / r14 / r30` + `alpha_w = r_w − BTC_r_w`.
- **beta 60 hari** (`cov(ret_tema, ret_BTC)/var(ret_BTC)`) → `exp7 = beta*BTC_r7`,
  `resid7 = r7 − exp7`. Ini pembeda **"ikut market" vs "struktural"** — |resid| kecil = cuma kebawa BTC.
- `breadth1d / breadth7d` = % anggota hijau; `volratio7 = mean(vol,7)/mean(vol,30)` = proxy uang masuk/keluar.
- Per anggota: top-3 & bottom-3 r7, favorit/terburuk 24 jam.

## Taksonomi alasan (ini yang bikin "kenapa"-nya bukan tebakan)

| Pola angka | Arti |
|---|---|
| beta tinggi · alpha/resid ≈ 0..negatif kecil · volratio ≈ 1 | **ikut market** (BTC-led) → bakal ikut balik kalau BTC naik |
| volratio < 0,9 · breadth 0–15% | **duit keluar = struktural** → bounce lemah walau market naik |
| volratio > 1,2 · harga turun · breadth 0% | **distribusi** (volume naik tapi harga turun), bukan akumulasi |
| alpha ≫ 0 · breadth > 70% · volratio > 1,5 | narasi sehat → cari katalis spesifiknya di berita |
| beta rendah (<0,6) tapi merah | ditinggal, bukan korban market |

Katalis **wajib dari luar**: 1 `web_search` per gerakan ekstrem (pemimpin + pembebani). Contoh yang
kepakai 4 Okt 2026: SAND +72,8% = Upbit/Bithumb cabut "trading caution"; GRT −20,7% = rally berita
migrasi Subgraph Studio→Network udah pudar + supply inflasi; IOTA +12% hari itu = breakout teknikal
"tanpa katalis berita" (analis sendiri bilang begitu) — jadi tulis apa adanya bahwa itu teknikal.

## Angka contoh (4 Okt 2026, 10 tema, candle tutup 3 Okt; BTC 7d +0,95% / 24j +0,62%)

Gaming +10,03% (α +9,07%, breadth 84%, vol 2,24x) · L2/Scale +1,20% (30d +48,5% tapi breadth 44% →
rotasi sempit) · AI/Compute −0,61% (GRT −20,7%) · L1 −0,77% (IOTA +19,4% teknikal) · Infra −1,09% ·
DeFi −1,17% (breadth 33%) · Fan −2,43% (breadth 9%, beta 0,48) · Meme −3,71% (β 1,46, vol 0,84x,
breadth 11%) · RWA −5,58% (breadth **0%**, vol 1,26x = distribusi, ONDO −15,5%) · Privacy −10,87%
(vol 0,66x, breadth 0%). Ringkasan: 6/10 kalah dari BTC, 4 di antaranya struktural (bukan sekadar market).

Chart: `~/.hermes/scripts/diag/make_narr_perf_chart.py` → bar horizontal r7 + garis BTC putus-putus
+ kolom angka kanan (r7 · α · 24j). 1360px, `--force-device-scale-factor=2`, verifikasi pakai
`vision_analyze` sebelum kirim; simpan ke `~/obsidian-vault/attachments/narrative-perf-7d-<tgl>.png`.

## Pitfalls

- **Skor detektor ≠ kekuatan 7 hari.** Skor mencampur momentum 3 hari + volume: 4 Okt skor menaruh
  AI/Compute (7,2) di atas Gaming (6,7) padahal 7 hari Gaming menang jauh. Sebut ketidakcocokan ini
  di laporan sebagai "skor kita ini momentum 3 hari, bukan kekuatan 7 hari".
- `narr_calls.jsonl` (ledger call, 44 hari) vs `narr_hist_cache.json` (histori tema, basis 90/240 hari)
  = **dua sumber beda**; jangan campur nilai `n` dari keduanya dalam satu baris tanpa keterangan.
- Cache klines TTL 12 jam; `r1` di indeks terakhir = candle **hari ini yang masih jalan** → tulis
  "candle jalan", jangan sajikan sebagai hari yang sudah tutup.
- **Jangan generalisasi** "semua lemah karena market" — memisahkan market-driven dari struktural
  adalah inti jawabannya (dan penentu: mana yang layak dibeli saat BTC balik naik).
- Tutup dengan kaitan ke posisi user kalau ada (4 Okt: RWA breadth 0% + ONDO −15,5% → data pendukung
  trim ONDO yang memang over cap).
