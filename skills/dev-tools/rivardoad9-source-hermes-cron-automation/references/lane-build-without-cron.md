# Bangun lane baru: script dulu, cron DITAWARKAN (bukan dipasang) — 6 Okt 2026

Kasus: user menyetujui pembangunan lane baru ("Gas #1 (magang hunter) dulu"), lane dibangun lengkap
**termasuk cron `no_agent` harian**, laporan dikirim — lalu user bilang singkat: **"ga ush jadi cron job"**.

Bacaannya: user mau **hasilnya**, bukan jadwalnya. Lane/laporan yang dia minta sekali bukan otomatis
langganan harian; keputusan "jadi cron atau nggak" milik user. Memasang cron tanpa diminta = langganan
senyap yang user harus repot mematikan.

## Pola yang benar

1. **Bangun artefaknya** (scanner/script + laporan + file datanya) dan kirim hasilnya. Itu permintaannya.
2. **Tunjukkan perintah manual** di laporan: `~/.hermes/scripts/<lane>.sh` (jalankan langsung) dan
   `python3 ~/.hermes/scripts/<lane>_scan.py` (tarik penuh + tampilkan per tier).
3. **Tawarkan** cron sebagai satu baris opsi ("mau gw jadwalin harian jam X? bilang aja") — jangan install.
   Sampai user bilang "jadikan cron"/"otomatis tiap hari", lane tetap manual.
4. Kalau user bilang jangan: **`cronjob action=remove`** (bukan `pause` — pause menyisakan job zombie yang
   nanti masuk audit), **sisakan script + data-nya** supaya masih bisa dipanggil kapan pun, dan balas
   dengan perintah manual + path file hasil terakhir.
5. **Verifikasi penghapusan**: `grep -i <nama-job> ~/.hermes/cron/jobs.json` harus kosong. Pesan
   `{"success": true, "message": "Cron job 'x' removed."}` itu laporan tool, bukan bukti — cek file.

## Pengecualian: keeper proses nol-risk tetap layak jalan

Bukan semua job harus menunggu diminta. Keeper yang **hanya menyalakan ulang proses read-only** dan
tidak menyentuh uang/engine (mis. `fm_api_up.sh` — API dashboard) tetap boleh aktif, dengan syarat:
idempoten, **senyap kalau sehat**, cetak pesan hanya saat benar-benar restart, dan nol token (`no_agent`).
Bedakan tajam: *lane baru berisi pekerjaan/konten* → tunggu diminta; *keeper yang cuma menjaga sesuatu
yang sudah ada tetap hidup* → pasang, dan sebutkan di laporan.

## Sisi memory

Preferensi ini juga layak jadi memory singkat (bukan cuma reference) karena berlaku lintas lane:
"User menentukan apa yang jadi cron: bangun script + perintah manual, cron ditawarkan." Jangan tulis
detail job ID ke memory — itu cepat basi; job ID cukup di reference seperti ini.
