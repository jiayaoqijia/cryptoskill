# Provider stall: job cron mati karena LLM provider nggak jawab

## Gejala

Beberapa job LLM mati bareng di jendela jam yang sama (pola khas: pagi 07:00-09:00),
error-nya:
`RuntimeError: Provider has been unresponsive (no response received) for 5-6 consecutive stale attempts — aborting this call to avoid an indefinite stall.`

Artinya endpoint provider-nya yang ngadat, bukan job-nya. Job lain di jendela yang sama
bisa lolos, jadi ini gangguan sesaat, bukan setelan yang salah. Jangan buru-buru ubah jadwal
atau nyalahin script.

## Diagnosa (urutan yang terbukti)

1. Baca `~/.hermes/cron/jobs.json`, filter `last_status == 'error'`, lihat `last_error`,
   `last_run_at`, `failure_streak`, dan `deliver`. Kalau errornya pola stall di atas, ini kasus ini.
2. Cek jadwal pagi: kalau job-jobnya sudah tersebar (07:00, 07:20, 07:45, 08:00), berarti
   BUKAN masalah tabrakan beban barengan — konfirmasi provider yang memang ngadat.
3. Tes providernya langsung sekarang:
   `curl -s -o /dev/null -w '%{http_code} %{time_total}s' -H "Authorization: Bearer $KEY" <base_url>/models`
   lalu satu `POST /chat/completions` kecil (`max_tokens: 10`). Jawab 200 dalam detik = sudah sehat.
4. Cek apa ada provider cadangan yang benar-benar hidup. Jangan percaya bahwa key yang tersimpan
   masih valid — tes satu-satu semua provider custom di `~/.hermes/.env`:
   sumopod (`https://ai.sumopod.com/v1`) pernah 401 "Key is blocked";
   `https://rkwtga3.abc-tunnel.us/v1` pernah 530 (origin mati);
   `http://localhost:20128/v1` nggak ada server-nya. Kalau semua mati, memang nggak ada cadangan —
   katakan apa adanya, jangan ngarang fallback.
5. Bandingkan fingerprint key (sha256 12 char pertama) `HERMES_DEEPSEEK_API_KEY` vs `DEEPSEEK_API_KEY`
   vs key inline di `config.yaml`; kalau sama semua, rotasi kredensial nggak menolong.

## Perbaikan yang bisa dikerjakan tanpa provider baru

Watchdog auto-retry: `~/.hermes/scripts/cron_retry_stalled.py` (job `7f0e643539e3`, tiap 15 menit
jam 06:00-22:00, `no_agent`). Logika: job enabled non-`no_agent` yang `last_status=error`, error cocok
regex `unresponsive|stale attempts|did not respond in time|timed out`, `last_run_at` HARI INI,
maksimal 2 job per tick, tiap job 1x per hari (state `~/.hermes/data/cron_retry_state.json`),
stdout kosong kalau nggak ada yang di-retry. Log: `~/.hermes/logs/cron_retry.log`.

Bedakan: bug script (mis. `whale_sync` payload halaman berubah, `btc_etf_collect.py` traceback)
TIDAK boleh masuk watchdog ini — di-retry tetap gagal dan malah nyepam. Perbaiki scriptnya.

## Jebakan yang bikin repot

- `hermes cron run <id>` BLOCKING sampai job-nya selesai (bukan fire-and-forget). Dari script
  pengawas harus `subprocess.Popen(..., start_new_session=True, close_fds=True)` tanpa `wait()`,
  kalau tidak watchdog-nya ikut gantung. Kalau proses CLI-nya ke-kill di tengah jalan, run-nya
  berstatus `unknown` di riwayat.
- `hermes fallback add` cuma interaktif (nggak ada flag). Edit langsung top-level
  `fallback_providers:` di `~/.hermes/config.yaml`; tiap entri butuh `provider` + `model`, dan
  endpoint custom juga menerima `base_url` + `key_env`.
- Job LLM tanpa `model`/`provider` sendiri itu inherit rantai fallback; job yang di-pin provider sendiri
  TIDAK ikut fallback. Jadi cadangan cuma nolong job yang belum di-pin.
- Job dengan `deliver: local` nulis ke `~/.hermes/cron/output/<run_id>/`, BUKAN ke chat. Jangan bilang
  "hasilnya nyusul ke chat" untuk job local; bilang cek foldernya.
- Backup dulu `config.yaml` + `jobs.json` sebelum ngutak-ngutik cron (`scripts/config_backup.sh`).

## Cadangan beneran

Butuh key provider kedua (yang ada sekarang satu-satunya DeepSeek). Pilihan paling murah yang sudah
ada kuota gratis: Google AI Studio (Gemini) atau OpenRouter model gratis. Kalau user kasih key-nya,
pasang lewat `fallback_providers` dan tes `/models` endpoint-nya sebelum dipakai.
