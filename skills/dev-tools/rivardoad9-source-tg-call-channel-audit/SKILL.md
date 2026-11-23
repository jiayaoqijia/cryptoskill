---
name: tg-call-channel-audit
description: Audit a Telegram call channel's real track record.
---

# Audit track record channel call Telegram

Dipakai buat jawab "channel/grup ini valid ga, track record-nya gimana" dengan **angka terukur**, bukan klaim channel.

## Langkah

1. **Profil channel** (tanpa login):
   - `curl -s -A 'Mozilla/5.0' https://t.me/<user>` → og:title + og:description (biasanya isi folder/premium link).
   - `curl -s https://t.me/s/<user>` → preview publik: post + **view count** + counter subscriber.
   - Subscriber history & sentimen independen: `https://tgregister.com/channel/<user>` (riwayat subscriber terukur + contoh post lama). Pakai `web_extract`.
   - View/post ÷ subscriber = **rasio engagement**. <2% → subscriber beli/bot. Sinyal terkuat channel abal-abal.
   - Owner: dari deskripsi/bio, cek X via `https://api.fxtwitter.com/<handle>` (followers, umur akun, bio).

2. **Scrape arsip**: `t.me/s/<user>?before=<msg_id>` paginasi 20 post/permintaan, sleep ~1,1s, simpan JSONL. Format call khas:
   - call: `⚡️ <nama> ｜ $SYM` + `🤴 CA: <mint>` + `🧢 MC:` + `👫 Holders:` + `🎮 Total Volume:` + `⏳ Age:`
   - update profit: `#SYM <n>x 💹 $<MC call> 🔜 $<MC sekarang>` → 🔜 SELALU = n × 💹 (konfirmasi format dulu).
   - Pesan iklan/sale: simpan, ini nunjukin model bisnis (mis. `6 Months → 0.5 SOL`, `LIFETIME → 1 SOL`, bot pembayaran, kontak support).

3. **Replay harga tiap call** (GMGN kline punya `--from/--to` Unix detik):
   - `gmgn-cli market kline --chain sol --address <mint> --resolution <res> --from $((t0-3600)) --to <now> --raw`
   - Pilih resolusi supaya (now - t0 + 3600) ≤ 100 candle: ≤8,3j → 5m · ≤25j → 15m · ≤100j → 1h · else 4h.
   - Weight kline = 2, bucket rate 20/capacity 20 → **pace ≥0,5s/req**; burst >10 req memicu `RATE_LIMIT_BANNED` (~5 menit, retry saat ban **memperpanjang** ban).
   - Ban muncul di **stderr** exit 1 → gabung stderr+stdout, parse `resets at <ts lokal>`, tidur sampai lewat. Jangan retry selama ban.
   - Baseline harga call = close candle terakhir dengan `t <= t0`; simpan juga `ppre` (open candle paling awal) buat ukur pump pra-call.

4. **Kondisi terkini semua token** (gratis, 25-30 mint/req): `https://api.geckoterminal.com/api/v2/networks/solana/tokens/multi/<ca,ca,...>` → `price_usd`, `fdv_usd` (= MC), `total_reserve_in_usd` (likuiditas), `volume_usd.h24`, `launchpad_details`, `top_pools[0]`.
   - Simpan pool → verifikasi silang: `/networks/solana/pools/<pool>/ohlcv/hour?limit=100` (rate 30/menit, sleep ≥2,3s).
   - 12/17 sampel cocok ~1% dengan GMGN; sisanya beda karena pindah pool → **laporkan agregat, jangan 1 token**.

5. **Metrik yang dilaporkan** (semua dari harga call, bukan dari klaim):
   - puncak pasca-call (median x, % ≥1,5x/2x/5x/10x), waktu ke puncak
   - harga +5m/+15m/+30m/+1j/+6j + "sekarang" sebagai kelipatan → simulasikan exit tiap horizon (median + win-rate)
   - drawdown terburuk pasca-call
   - pump pra-call 1 jam (median x) = bukti channel ngejar pump, bukan early
   - kondisi sekarang: likuiditas, volume 24j, % di bawah X% harga call
   - klaim vs realita: max klaim per simbol ÷ puncak asli
   - faktor pembeda pemenang (MC/umur/holders/TOP10/volume/jam) — sering **tidak ada** yang diskriminatif; katakan apa adanya.

## Pitfall
- F-string `{x:.1%}` mengalikan rasio dengan 100 → 0,74 tercetak "+74%". Pakai `x{:.2f}`.
- `re.search(...)[0]` = seluruh match, bukan grup → pakai `.group(1)` (bikin lookup metadata kosong).
- Token mati tetap ada di GeckoTerminal; "hilang" ≠ mati — pakai likuiditas <$3k sebagai proxy mati.
- Channel sering re-call simbol sama; dedupe per CA, hitung simbol unik.
- Update profit = cherry-pick puncak. Bandingkan klaim dengan puncak asli DAN harga sekarang.
