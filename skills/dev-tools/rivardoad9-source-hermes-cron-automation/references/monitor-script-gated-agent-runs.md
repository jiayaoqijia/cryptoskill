# Monitor-script gating: agent hanya jalan kalau ada yang berubah

Pola termurah untuk cron agent yang "nonton feed" (X akun, blog, halaman harga):
taruh SEMUA kerja deterministik di `monitor_script`, biarkan agent cuma dipanggil
kalau output monitor berubah. Di tick yang tidak ada perubahan, **agent tidak jalan
sama sekali** (0 token) — bukan "agent jalan lalu balas [SILENT]".

## Kenapa penting (kasus nyata 3 Okt 2026)

Job "X watch @Proxonchain" (63e55c0b5cfd) = agent murni yang tiap run
`web_search("site:x.com/...")` + buka halaman. Hasil ukur:
- 737 rb token/run rata-rata, **puncak 3,6 jt dalam satu run**, 8 run/hari
  → ~5,9 jt token/hari = 69–85% dari SELURUH konsumsi token profil.
- 38% run gagal `HTTP 400: Content Exists Risk` (moderasi provider, kemungkinan
  dipicu snippet web_search — bukan oleh teks post-nya sendiri; diuji langsung ke
  API: teks post 200 OK).
Setelah dirombak (monitor + script pre-compute + cadence 3j→6j): **16 rb token/run
(-98,6%)**, dan tick tanpa post baru = 0 token.

## Aturan output monitor: WAJIB byte-stabil

Scheduler membandingkan hash output tiap tick. Output yang berubah-ubah = agent
jalan terus = pemborosan total. Yang bikin output goyang:
- **timestamp "sekarang"** → jangan pernah cetak `now()` di jalur sukses.
  Kalau perlu waktu, cetak waktu POST terbaru (stabil), bukan waktu fetch.
- **counter/jumlah item** yang bisa naik-turun (feed balikin 19 vs 20 item).
- **whitespace/HTML entity** yang beda antar-fetch → normalisasi keras
  (`re.sub(r"\s+"," ", html.unescape(strip_tags(s))).strip()`).

## Verifikasi wajib sebelum percaya gating bekerja

```bash
# output harus byte-identik antar run
python3 monitor.py | md5sum; python3 monitor.py | md5sum
```
Lalu bandingkan hash yang DISIMPAN scheduler:
```python
j = [x for x in json.load(open("~/.hermes/cron/jobs.json"))["jobs"] if x["id"]==JOB_ID][0]
j["monitor_state"]["last_output_hash"]   # + output/<job>/monitor_last_output.txt
```
⚠️ **GOTCHA**: scheduler menyimpan hash dari output **tanpa trailing newline**.
`sha256(output)` mentah akan kelihatan beda walau isinya sama. Bandingkan dengan
`output.rstrip(b"\n")` — kalau cocok, gating OK.

## Desain yang dipakai (proxonchain_watch.py)

1. Discovery + detail via **nitter RSS** (`status.d420.de/api/v1/instances` untuk
   daftar instance sehat + RSS, seed `https://shitter.thepixora.com`). RSS sudah
   bawa teks asli + waktu + id.
   - DDG html/lite: **rusak/rate-limited dari IP server ini** ("discovery kosong").
   - `syndication.twitter.com`: 429 terus. `r.jina.ai` → 403 abuse block.
   - API X official: butuh kredensial + kuota baca. fxtwitter: bagus untuk detail
     SATU id, tidak memberi timeline.
2. Tulis 8 post terbaru (teks penuh) ke `~/.hermes/data/<src>_latest.json`.
3. Cetak digest KECIL & stabil: `latest=<id>` + `time=<waktu post terbaru>` +
   `head=<140 char post terbaru>` + `detail_file=<path>`. Berubah HANYA saat ada
   post baru.
4. Jalur gagal: cetak `fail` + `last_ok=<ts>` (stabil selama gagal) + satu baris
   `[ALERT ...]` teks TETAP saat streak ≥ 3. Karena teksnya tetap, alert cuma
   memicu satu agent-run, tidak spam tiap tick.
5. Prompt agent: **larang web_search**, baca `detail_file` + state seen, hanya
   laporkan id > max(seen), verifikasi angka via CoinGecko `curl`, update seen.
6. `enabled_toolsets: ["terminal","file"]` — buang `web` (tool-schema overhead +
   sumber moderasi).

## Cek biaya sesudahnya

`~/.hermes/cron/usage_audit.jsonl` — satu baris JSON per agent-run:
`{ts, id, prompt_tokens, completion_tokens, total_tokens, duration_ms, error}`.
Agregat per job untuk lihat mana yang paling boros. Job `no_agent=true` TIDAK
muncul di sini (memang 0 token).
