# Roadmap / plan pages as an image (recipe that worked, 10 Okt 2026)

Trigger: "bikin roadmap gw", "kayak plan kita gimana, output gambar", any ask for a visual plan.
Rendered with the `data-chart-images` pipeline (SVG in HTML → headless Chromium), builder in
`templates/infographic_page.py`. Live example: `~/rapel-usaha/ROADMAP.md` + the two PNGs
`~/obsidian-vault/attachments/rapel-roadmap-1-fase.png` and `rapel-roadmap-2-uang-pagar.png`,
generator `~/.hermes/scripts/diag/make_rapel_roadmap.py`.

Do NOT route this through a text-to-image model: infographic prompts produce garbled Indonesian text.
SVG gives exact wording, and it is verifiable.

## Split into 2 pages, not one

One tall page buries the message. Worked shape:

1. **Page 1 — status + phases.** Header, "POSISI SEKARANG" (two columns: what EXISTS vs what is
   MISSING), then the phased timeline, then a closing rule.
2. **Page 2 — money, time, risk.** Milestone bars per phase, weekly time allocation, then a
   risk → guardrail table.

## Panel set

- **Status block**: two columns, green "udah ada" vs amber "belum ada", each item a short line with a
  dot instead of a dash. This is the honest baseline and it shows the user their own progress.
- **Timeline**: one card per phase. Header row = `FASE n · <duration>` on the left, the revenue target
  right-aligned. Body = 3–4 concrete actions. Then a rule line and an amber **"Ukuran lulus:"** line.
  Every phase must have a pass condition — it stops "still preparing, not selling yet" from looking
  like progress. Make the pass condition include a number the user can only hit by talking to people.
- **Milestone bars**: one bar per phase, y = Rp juta/month. Label each bar with the range
  ("Rp1,25 sampai Rp2,5 jt") and say in the subtitle that the bar is the midpoint of the range.
- **Time allocation**: a single 100% stacked bar of the weekly hours. Deliberately give the biggest
  slice to the activity the user admits they are weak at (here: 5 of 8 hours talking to prospects).
  This is the panel that lands the message; make its colour the loud one.
- **Risk → guardrail table**: one row per risk, the guardrail underneath in muted text. Source the
  rows from problems that already appeared in the project, never generic startup advice.
- **Closing rule strip**: one bold sentence with the honesty rule ("nggak ada angka penjualan yang
  ditulis kalau belum ada bukti bayar") + a muted source line.

## Content rules for this user

- Indonesian casual, second person, no dash bullets anywhere — use dots, `·`, or numbers.
- Numbers are TARGETS. Say it twice: once in the subtitle of the page and once in the chat caption.
- Include the honest horizon ("Rp100 juta ≈ 24 bulan di jalur ini") so a 6-month plan cannot be read as
  a 6-month promise.
- End with what is still blocking phase 1 and the one action that unblocks it (here: the BotFather token).
- Also write the plan as markdown next to the product (`ROADMAP.md`) — the PNG is for reading on the
  phone, the markdown is what future sessions and the user's own notes link to.

## Layout pitfalls (all three hit in the first render)

1. **Text-width estimator clipped the title.** "kejawab" was rendered as "keja" and the vision check
   reported it as a typo — it was the last word crossing the page edge and being cut by the viewport.
   Fix: wrap against `maxpx * 0.93`. Treat a truncated word in a vision report as a CLIPPING symptom.
2. **Fixed offset under the title.** The title wrapped to two lines and the subtitle landed on top of
   line 2. Fix: derive the next baseline from `(len(wrapped_title) - 1) * line_height + gap` and return it.
3. **Rail drawn after the cards.** The timeline spine crossed every card. Fix: measure all card heights
   first, emit rail → cards → dots, and keep the backdrop rect taller than the page (it gets clipped).

## Verification before sending

1. Full-page `vision_analyze` for global collisions, then a **zoomed** pass on the header
   (`region=[0, 0, 2*W, 0.25*H]` in 2× PNG pixels) to prove no word is clipped — the header is where
   clipping hides.
2. Ask the vision pass explicitly: "label uang di kanan nabrak label fase di kiri?", "baris Ukuran
   lulus kepotong di dasar kartu?", "catatan bawah nabrak label bar?".
3. Vision prose is unreliable on details (it "read" `Tetap` as `Tetapi` and invented a typo). Use it to
   find collision/clipping hot spots, then trust the generator's own arithmetic for wording.
4. Send with `MEDIA:<absolute path>` in the same message as a caption that explains how to READ each
   picture (which panel carries which decision), and keep the caveat in the prose too.
