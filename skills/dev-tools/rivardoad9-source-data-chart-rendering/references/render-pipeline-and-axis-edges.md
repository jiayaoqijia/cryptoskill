# Pipeline render & edge layout sumbu (dari sesi 4 Okt 2026, chart PROVE vs SOMI)

Dua hal yang berulang tiap kali bikin chart harga multi-panel, dan dua-duanya pernah lolos ke
gambar jadi. Treat as part of `rendered-chart-qa.md`, bukan lampiran opsional — file itu tidak bisa
di-patch langsung (guard read-before-write vs dedup `skill_view`), jadi tambahannya ditaruh di sini.

## 1. Ujung KANAN sumbu-X = tempat label tanggal bertumpuk

Tik bulanan + label "sekarang" di `x(n-1)` saling menimpa. Kejadian nyata: chart dua panel skala log
(PROVE vs SOMI) → hasil verifikasi vision: label terbaca "*Sep* 4 Okt Okt" berdesakan.

Fix dua baris, dua-duanya dipakai:

```python
# tik bulanan: lewati tik yang jaraknya < ~16 bar dari ujung
if d.month != prev_m and d.day <= 5 and i < n - 16: ...
# label "sekarang" ditaruh di KANAN titik terakhir, bukan di tengahnya
s += f'<text x="{x(n-1)+8:.1f}" y="{bot+24}" text-anchor="start">4 Okt 26</text>'
```

Setelah fix, prompt vision yang sama konfirmasi tidak ada overlap. **Tanya spesifik soal strip
sumbu-X** ("apakah label tanggal masih bertumpuk di ujung kanan?") — pertanyaan umum
"ada yang tumpang tindih?" pernah melaporkan aman padahal tidak.

## 2. Render lewat `render.sh`, jangan baris shell ketik-tangan

Generator + chromium itu gampang benar sekali lalu salah ketik selamanya. Taruh di file:
generator mencetak `W x H` di baris terakhir → skrip parsing → `--window-size=W,H` → `ls -la` PNG.

```bash
#!/bin/bash
set -e
python3 -u ~/.hermes/scripts/diag/make_<nama>_chart.py > /tmp/gc/gen.log 2>&1
cat /tmp/gc/gen.log
H=$(tail -1 /tmp/gc/gen.log | cut -dx -f2)
CH=$(ls -d /home/ubuntu/.cache/ms-playwright/chromium-*/chrome-linux64/chrome | head -1)
"$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
      --window-size=1360,"$H" --screenshot=/tmp/chart_<nama>.png file:///tmp/chart_<nama>.html 2>/dev/null
```

Tulis skripnya dengan `write_file`, jalankan dengan `bash /tmp/gc/render.sh`. Itu sekaligus
menjauhkan URL API ber-`&` (query string) dari baris perintah shell, di mana `&` dibaca sebagai
backgrounding. Di dalam generator sendiri pakai `AMP = chr(38)` lalu rakit URL dengan `%s`.

## 3. Template dasar yang sudah ada — jangan bikin dari nol

`~/.hermes/scripts/diag/make_ilv_imx_chart.py` (16 KB) adalah kerangka matang: `num()` untuk koma
desimal gaya Indonesia, `resolve()` anti-tumpuk label, `head()` yang menghitung tinggi dokumen,
`nice_step()` untuk tick, `panel_price()` dua panel + legenda + klip. Cara tercepat bikin chart baru:
salin kerangka ini, ganti `DATA`/`SYMS`/`COL`, tambah `texts()` untuk catatan bukti di bawah.
Generator baru disimpan di `~/.hermes/scripts/diag/make_<nama>_chart.py` supaya rerun murah.

## 4. Skala log untuk dua koin yang beda orde

Bandingkan bentuk dua kandidat: pakai `y = bot - (log v - log ymin)/(log ymax - log ymin) * (bot-top)`
dengan **ymin/ymax sama** untuk kedua panel (mis. 0,05–2,4) → bentuk kurvanya bisa dia du langsung
dengan screenshot user. Tick log di 0,05 / 0,1 / 0,2 / 0,5 / 1 / 2 — jangan `nice_step()`, itu untuk
skala linear.
