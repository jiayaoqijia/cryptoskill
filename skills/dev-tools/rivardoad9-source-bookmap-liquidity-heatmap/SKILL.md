---
name: bookmap-liquidity-heatmap
description: Render Bookmap-style order-book liquidity heatmaps.
---

# Liquidity heatmap gaya Bookmap (dari data OpenMarket)

## Kapan dipakai

User minta visual "kayak Bookmap" — heatmap likuiditas (warna = size limit order yang nangkring per
level harga sepanjang waktu), volume dots, DOM/depth. Pertanyaan khas "tambahin kek gini dong".

## Langkah 0 — cek dulu apakah OpenMarket bisa langsung (jawab jujur sebelum ngoding)

`chart_indicator_list` (65 indikator) punya yang persis gaya Bookmap —
`ORDERBOOK_HEATMAP` (alias `orderbook`/`heatmap`), `HYPERLIQUID_LIQUIDATION_HEATMAP` (alias
`liquidation_heatmap`), `HYPERLIQUID_TPSL_HEATMAP` (alias `tpsl`), `VOLUME_FOOTPRINT` (alias
`footprint`), `ORDERBOOK_PROFILE`, `ORDERBOOK_DEPTH`, `CUMULATIVE_VOLUME_DELTA`.

**Kepagari plan.** Dua heatmap itu nolak dengan
`INTERNAL, heatmap4K requires plus tier (indicator type 'ORDERBOOK_HEATMAP')`.
Pricing resmi (openmarket.xyz/chart/plus) — Free $0 (3 indikator/pane, multichart 1, workspaces 10)
vs Plus $29/bln atau $348/thn (10 indikator/pane, heatmap depth maximum, multichart 16).
Jadi kalau user mau heatmap resmi, jawabannya **Plus**, bukan akal-akalan setting.

Yang **masih bisa** di Free (sudah terpasang di workspace BTC `co3r70cd`, 5m) — `footprint`,
`VISIBLE_RANGE_VOLUME_PROFILE`, `CUMULATIVE_VOLUME_DELTA`, `ORDERBOOK_DEPTH`. Batas Free 3
indikator/pane (pesan errornya `plan_limit ... holds 4 indicators, the most the Free plan allows (3)`) —
kalau mau nambah, hapus dulu lewat `chart_indicator_remove`.

## Langkah 1 — render sendiri dari snapshot book mentah (gratis)

Data mentahnya ada di tool `points` — `type=BLOCK_BOOK_SNAPSHOT_AGG` ("separate bids and asks arrays,\n`blockSize` REQUIRED"). Ini satu-satunya jalan gratis untuk heatmap penuh.
Proyek `~/.hermes/bookmap/` (venv dipinjam dari `~/.hermes/trade/venv`, `om.py` di-symlink).

```bash
cd ~/.hermes/bookmap
~/.hermes/trade/venv/bin/python fetch.py 120      # book 120 menit + candle 1m
~/.hermes/trade/venv/bin/python render.py data/heatmap_btc.png
~/.hermes/trade/venv/bin/python walls.py          # ringkas dinding likuiditas (murni teks)
```

- `fetch.py` — `BLOCK_BOOK_SNAPSHOT_AGG` + `blockSize` (mis. 25 USDT) + `interval: MINUTE`; candle 1m
  lewat `om.candles(...)` dengan **interval `MINUTE`** (bukan `ONE_MINUTE` — itu balikin 0 bar).
- Titik book **nggak punya timestamp** (cuma `{"Point": {bids, asks}}`), jadi sumbu waktu = jumlah
  snapshot ke belakang dari sekarang (asumsi 1 menit/snapshot; 90m → 89 baris).
- Format bids/asks = **list rata** `[harga, size, harga, size, ...]`, bukan pasangan bersarang.
- `render.py` — PNG ditulis tangan (zlib + struct + CRC), tanpa PIL/numpy. Parameter penting
  `BLOCK=25.0`, `SPAN_PCT=1.2` (buang level jauh, ladder Binance nggak jarang ngebalikin level $52k/$98k
  yang bikin skala ancur), normalisasi warna pakai persentil p95, ramp bid (biru→cyan→putih-biru) vs ask
  (merah→oranye→krem), plus profil likuiditas per level di kanan.
- Font 5x7 ditulis sendiri di `render.py`. Huruf yang belum ada di tabel tampil kosong, bukan error —
  kalau judul muncul bolong, tambahin glyph-nya.

## Jebakan yang mahal waktu

- **Rate limit Free 10 weight / 60 s.** Satu tarikan book 120 menit berat; habis itu `points` balikin
  `{"error": "rate_limited"}` (bukan exception) — tunggu window reset (~30-60 s), jangan retry loop.
  Candle 1m murah, tarik terpisah dari book.
- Guard lifecycle Hermes nolak heredoc yang nyebut file data >1 MiB — taruh analisis di `.py` biasa,
  jangan `python - <<'PY'` yang membaca `book_*.json` 12 MB.
- `series[0]` candle pakai key `rows`, sedangkan book pakai `points` — beda, jangan diasumsikan sama.
- Screenshot chart OpenMarket — `chart_screenshot` balikin image di `content[].data` (base64), pakai
  `~/.hermes/cache/scratch/om_shot_ws.py <workspaceId> <out.png>`.
- Verifikasi visual wajib — `vision_analyze` PNG-nya sebelum dikirim (judul kepotong atau tulisan
  tenggelam gampang lolos kalau nggak dilihat).
