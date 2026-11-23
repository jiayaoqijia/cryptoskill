# PB5MAT ICA 5 — SPSS: Sampling, Estimation & Confidence Interval (UBM, 22 Sep 2026)

## Modulnya apa
`IN-CLASS ACTIVITY — WEEK 5 / From Population to Sample`. Mode individual, 20 menit, IBM SPSS,
dataset `grocery_1month.sav` (sample bawaan SPSS: `File → Open → Data → Samples → English`).
Peran: Junior Market Research Analyst. Alur: **Population → Sample → Estimate → CI → Business Decision**.
12 part + Final Challenge + submission checklist (11 item).

Part kunci & output yang diminta:
| Part | Yang diminta | Dari mana |
|---|---|---|
| 1 | Setiap pelanggan vs sampel + alasan 1 kalimat | jawaban konsep |
| 3 | Population N + nama spending variable | Descriptives (N) + Variable View (label) |
| 4 | Population Mean | Analyze → Descriptive Statistics → Descriptives |
| 6 | Sample N + "≈10%?" | Data → Select Cases → Random sample of cases → Sample → Approximately 10% |
| 7 | Sample Mean | Descriptives (dengan filter nyala) |
| 8 | Dua mean sama? → No; berarti sampel salah? → No + 1 kalimat (sampling error) | |
| 10 | Mean + Lower + Upper (95% CI) | Analyze → Descriptive Statistics → **Explore** → Statistics → Descriptives + CI 95% |
| 11 | Kalimat estimasi: "around ___, 95% CI from ___ to ___" | |
| 12 | Boleh pakai sampel buat gambaran awal? + alasan pakai sampel DAN CI | |
| Final | "beda dari mean populasi = sampel gagal?" → **Disagree**, pakai konsep sampling + estimation | |

Poin pedagogis yang bikin nilai bocor kalau kelewat:
1. **"Approximately 10%"** = tiap kasus diundi independen p=0,10 → N sampel boleh ±1-2 dari 10% (bukan error).
2. Kasus **tidak dihapus**, hanya ditandai (`filter_$`); salah paham ini bikin Part 6 salah.
3. Beda mean populasi vs sampel itu **sampling error yang diharapkan**, bukan bukti sampel gagal —
   dan CI-lah yang mengukur seberapa jauh bedanya masih wajar. Bukti sampel "berhasil" = mean populasi
   masuk ke dalam CI (Part 10 punya baris cek ini).
4. Sampel cuma ~10% → CI **lebar**; itu justru alasan Part 12 dijawab "ya, tapi sebagai gambaran awal".

## Kenapa angkanya tidak bisa dikasih dari jauh
- `grocery_1month.sav` = `grocery_coupons.sav` yang di-roll-up (1 kasus = 1 customer, "amount spent" =
  jumlah 4 minggu). File-nya **tidak ada di mesin**, tidak ada mirror GitHub, dan ibm.com memblokir extractor.
- N/mean populasi cuma bisa dipastiin kalau usernya kirim `.sav`-nya; N sampel/mean sampel/batas CI
  **memang beda tiap undian** (bahkan dua kali klik di SPSS yang sama hasilnya beda) → mustahil dijawab
  dari jauh, dan memang bukan itu soalnya.

## Deliverable yang dikirim (22 Sep 2026)
1. `PB5MAT_ICA5_Analisis_Data_Jawaban.docx` — lembar jawaban siap-isi: checkbox udah ditandai, jawaban
   naratif Part 1/8/11/12/Final udah jadi (Inggris), slot angka bertanda `______________` + baris italic
   jalur menu SPSS-nya, plus "BEFORE YOU SUBMIT — self-check" dari checklist modul.
2. `PB5MAT_ICA5_syntax_spss.sps` — 3 blok: `DESCRIPTIVES` (populasi) → sampel acak 10%
   (`COMPUTE filter_$=(UNIFORM(1) <= .10). / FILTER BY filter_$.`) → `EXAMINE /CINTERVAL 95`.
   Pakai placeholder SATU nama variabel (`SPEND`) + komentar cara gantinya; **jangan** `VARIABLES=ALL`
   (bisa kena variabel string).
Dibuat dengan `python-docx` di venv uv (`uv pip install python-docx`); tidak ada pandoc/libreoffice di server.

## Kalau user balas bawa `.sav` atau screenshot output
Baca: `/tmp/spssenv/bin/python -c "import pyreadstat; df,md = pyreadstat.read_sav('grocery_1month.sav'); ..."`
→ isi N, nama variabel, mean populasi; lalu (opsional) undi sampel 10% dengan `numpy.random.default_rng(seed)`
buat nunjukin bentuk angka sampel + lebar CI-nya, dan verifikasi angka user: mean populasi harus masuk CI-nya.
