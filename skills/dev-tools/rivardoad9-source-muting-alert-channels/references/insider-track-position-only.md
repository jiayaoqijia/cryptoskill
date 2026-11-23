# Partial mute: Hyperliquid insider tracker (8 Okt → 11 Okt 2026)

Dua kali user minta lane ini dibikin lebih senyap. Aturannya makin ketat, jadi baca bagian
terbaru dulu sebelum mengubah filter.

## Tier aturan (yang berlaku sekarang: 11 Okt 2026)

| Tanggal | Aturan | Yang dikirim |
|---|---|---|
| 8 Okt | position-only | semua event posisi (buka/tutup/flip/ubah ukuran/cepat) |
| **11 Okt** | **cuma buka posisi gede** | `🟢 BUKA POSISI` / `🔁 FLIP` dengan notional **>= `OPEN_MIN` = $1jt** + error `⚠️` (selain 429) |

Pemicu 11 Okt: user (reply ke card `Insider Track HL` isi `🪙 SPOT DIKELUARIN` HYPE $26K/$100K)
*"ini jangan di alert ke gw, lu cukup announced trade dia kalau dia open sized nya gede kayak waktu itu"*.

Yang sekarang **disenyapkan** (tetap diproses, tetap dicatat log + dashboard Zemiz Chain):
`🪙` (semua spot: masuk/ubah/keluar), `🔴 TUTUP POSISI`, `📈 UBAH UKURAN`, `⚡ BUKA+TUTUP CEPAT`,
`🟢 ADA POSISI DI WALLET BARU`, `🚨 POLA KLASTER BARU`, `💸 LEDGER HL`, semua jalur pindah wallet.
Catatan: kalau user mau `🚨 POLA KLASTER BARU` (temuan klaster baru) dikirim lagi, itu flag terpisah
— bilang dulu ke dia, jangan diam-diam dinyalakan.

## Lane

- Script: `~/.hermes/scripts/hl_insider_track.py` (cron `Insider Track HL — klaster short BTC (10m)`,
  `*/10 * * * *`, `no_agent=true`, deliver origin → silence = empty stdout).
- State: `~/.hermes/data/hl_insider_track.json` · log `~/.hermes/data/hl_insider_log.jsonl`.
- Venue pantau: 4 trader + hub pendana + depositor jembatan (>= $100rb) · style `msgstyle.finish(text, kind=)`.

## Implementasi (11 Okt)

- Konstanta `OPEN_MIN = 1_000_000` di blok ambang, komentar tebal di atasnya (jangan hilang saat edit).
- Saat blok `🟢 BUKA POSISI` / `🔁 FLIP` dibangun, kalau `abs(p["value"]) >= OPEN_MIN` teks bloknya
  dimasukkan ke set `big_open`; tail loop mengirim blok itu sebagai **prioritas 0**
  (`events.append((0 if b in big_open else 1, b))`). Prioritas lain tetap 1/2/5/9.
- `position_only(events)` sekarang: `hit = pri == 0 or (t.startswith("⚠️") and "429" not in t)`
  → jangan kembali ke filter berbasis prefix `ALERT_KEEP` (tuple itu sudah dihapus).
- Baseline card + prompt cron job ikut diubah biar orang berikutnya tahu ambangnya.
- Kalau nanti mau naik/turun ambang: ubah `OPEN_MIN` saja (mis. $500rb), jangan bikin daftar prefix baru.

## Cek cepat (jangan skip)

```bash
python3 -c "import ast;ast.parse(open('hl_insider_track.py').read())"
# unit: pastikan cuma prioritas 0 + error yang lolos
python3 - <<'PY'
import importlib.util, os
s = importlib.util.spec_from_file_location('hit', os.path.expanduser('~/.hermes/scripts/hl_insider_track.py'))
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
ev = [(0,'🟢 BUKA POSISI — T1 · BTC SHORT'), (1,'🪙 SPOT DIKELUARIN — HYPE'), (1,'🟢 ADA POSISI DI WALLET BARU'),
      (1,'🚨 POLA KLASTER BARU'), (9,'⚠️ gagal — 429')]
keep, drop = m.position_only(ev)
print([k[1][:20] for k in keep], [d[1][:20] for d in drop])
PY
# live: harus nggak ada baris 'alert' baru, cuma 'muted-moves'
python3 hl_insider_track.py --dry-run
python3 -c "import json;rows=[json.loads(l) for l in open('/home/ubuntu/.hermes/data/hl_insider_log.jsonl')];print([r['kind'] for r in rows[-4:]])"
```

`--dry-run` nggak nyimpan state dan tetap nge-log `muted-moves`, jadi aman dipakai buat bukti
"live lane sekarang senyap untuk event yang dimute".
