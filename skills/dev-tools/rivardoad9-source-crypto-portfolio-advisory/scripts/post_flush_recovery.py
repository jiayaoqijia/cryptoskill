"""Uji klaim '<ticker> paling sering balik setelah flush' pakai base rate, bukan feeling.

Usage:
    python3 post_flush_recovery.py [SYM ...]        # default UNI AAVE INJ SUI
    python3 post_flush_recovery.py --days 730 LINK

Sumber: Binance klines harian, keyless. Semua angka yang dicetak dihitung dari
close, jadi aman dikutip apa adanya (sebut n-nya).

Yang dicetak:
  1. base rate: setelah hari BTC <= -4%, return alt pada +5/+10/+20 hari
  2. rezim koreksi: saat BTC 30d <= -10%, return alt 20 hari ke depan
  3. beta / korelasi / vol tahunan vs BTC (1 tahun)
  4. posisi harga di rentang 1 tahun + drawdown dari puncak 3 tahun

Baca hasilnya begini: win-rate ~50% dengan median ~0% berarti tidak ada edge
pemulihan, sekadar ikut market. Nama dengan 20d win < 40% dan median negatif
adalah yang paling salah untuk dijadikan 'pemulihan cepat' — biasanya itu
berlawanan dengan keyakinan user, dan justru situasi di mana tabel ini berguna.
"""
import json
import statistics
import sys
import time
import urllib.request

HDR = {"User-Agent": "Mozilla/5.0"}
BENCH = "BTCUSDT"


def get(url):
    req = urllib.request.Request(url, headers=HDR)
    return json.loads(urllib.request.urlopen(req, timeout=45).read().decode())


def klines(sym, days=1095):
    """Close series, paginated backwards; Binance caps 1000 candles per call."""
    out, end = [], None
    while len(out) < days:
        url = f"https://api.binance.com/api/v3/klines?symbol={sym}&interval=1d&limit=1000"
        if end:
            url += f"&endTime={end}"
        try:
            k = get(url)
        except Exception as exc:  # noqa: BLE001 - a delisted symbol should not kill the run
            print(f"  ! {sym}: {exc}")
            return []
        if not k:
            break
        out = k + out
        end = k[0][0] - 1
        if len(k) < 1000:
            break
        time.sleep(0.2)
    return [(int(x[0]), float(x[2]), float(x[3]), float(x[4])) for x in out[-days:]]


def main(argv):
    days = 1095
    if "--days" in argv:
        i = argv.index("--days")
        days = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    syms = [a.upper() if a.upper().endswith("USDT") else a.upper() + "USDT" for a in argv] or [
        "UNIUSDT", "AAVEUSDT", "INJUSDT", "SUIUSDT"
    ]

    data = {BENCH: klines(BENCH, days)}
    for s in syms:
        data[s] = klines(s, days)
    n = min(len(v) for v in data.values() if v)
    if n < 120:
        print("data terlalu pendek buat base rate yang layak (butuh >=120 hari)")
        return
    closes = {s: [x[3] for x in v][-n:] for s, v in data.items()}
    btc = closes[BENCH]
    brets = [(btc[i] / btc[i - 1] - 1) * 100 for i in range(1, n)]

    print(f"bars={n}  simbol={', '.join(s for s in syms)}")

    flush = [i + 1 for i, r in enumerate(brets) if r <= -4]
    print(f"\n=== setelah hari BTC <= -4% (n={len(flush)}) ===")
    for s in syms:
        if not closes.get(s):
            continue
        p = closes[s]
        cells = []
        for h in (5, 10, 20):
            vals = [(p[i + h] / p[i] - 1) * 100 for i in flush if i + h < n]
            if vals:
                win = 100 * sum(1 for v in vals if v > 0) / len(vals)
                cells.append(f"{h:2d}d win {win:4.0f}% med {statistics.median(vals):+5.1f}%")
        print(f"  {s:9s} " + " | ".join(cells))

    print("\n=== rezim koreksi: BTC 30d <= -10% -> 20d forward ===")
    for s in syms:
        if not closes.get(s):
            continue
        p = closes[s]
        vals = [(p[i + 20] / p[i] - 1) * 100 for i in range(30, n - 20) if (btc[i] / btc[i - 30] - 1) * 100 <= -10]
        if vals:
            win = 100 * sum(1 for v in vals if v > 0) / len(vals)
            print(f"  {s:9s} n={len(vals):3d} win {win:4.0f}% med {statistics.median(vals):+6.1f}% mean {statistics.mean(vals):+6.1f}%")

    print("\n=== beta / korelasi / vol vs BTC (1 tahun) ===")
    b = btc[-365:]
    br = [(b[i] / b[i - 1] - 1) for i in range(1, len(b))]
    mb = statistics.mean(br)
    vb = sum((x - mb) ** 2 for x in br) / len(br)
    for s in syms:
        if not closes.get(s):
            continue
        c = closes[s][-365:]
        r = [(c[i] / c[i - 1] - 1) for i in range(1, len(c))]
        mr = statistics.mean(r)
        cov = sum((x - mb) * (y - mr) for x, y in zip(br, r)) / len(r)
        beta = cov / vb
        corr = cov / (vb ** 0.5 * statistics.pstdev(r))
        vol = statistics.pstdev(r) * (365 ** 0.5) * 100
        print(f"  {s:9s} beta {beta:.2f} corr {corr:.2f} vol {vol:.0f}%/thn")

    print("\n=== posisi harga ===")
    for s in syms + [BENCH]:
        if not closes.get(s):
            continue
        p = closes[s]
        last = p[-1]
        y = data[s][-365:]
        hi1 = max(x[1] for x in y)
        lo1 = min(x[2] for x in y)
        hi3 = max(x[1] for x in data[s])
        ch30 = (last / p[-31] - 1) * 100 if len(p) > 31 else float("nan")
        print(
            f"  {s:9s} {last:<10.6g} rentang1y {lo1:.6g}-{hi1:.6g} pos {100*(last-lo1)/(hi1-lo1):5.1f}% "
            f"dd-ATH3y {100*(last/hi3-1):6.1f}% 30d {ch30:+6.1f}%"
        )


if __name__ == "__main__":
    main(sys.argv[1:])
