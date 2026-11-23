#!/usr/bin/env python3
"""Reusable builder for long-form info-graphic pages (roadmap / plan / one-pager).

Copy to ~/.hermes/scripts/diag/make_<topic>_page.py and replace the panel bodies.
Everything is stdlib + SVG strings; rasterise with headless Chromium:

    CH=$(ls -d ~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome | head -1)
    "$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars \
          --force-device-scale-factor=2 --window-size=1360,$H \
          --screenshot=$OUT.png "file://$OUT.html"

Then verify with vision_analyze: one full-page pass AND one zoomed pass on the
header (region=[0,0,W*2,H*2]) — a word clipped by the page edge looks like a typo.
"""
import html
import os

W = 1360
PAD = 48
BG = "#0b1020"      # page background
PANEL = "#111a30"   # panel fill
INNER = "#0e1830"   # inner card fill
BORDER = "#1e2740"
TXT = "#e6edf7"
MUTED = "#93a1b8"
BODY = "#d5deef"
GREEN = "#34d399"
AMBER = "#fbbf24"
CYAN = "#22d3ee"
VIOLET = "#a78bfa"
RED = "#fb7185"
FONT = "'DejaVu Sans','Liberation Sans',sans-serif"

# Conservative on purpose: the estimator runs ~7% optimistic otherwise, the last
# word of a line crosses the panel/page edge and the viewport clips it silently.
SAFETY = 0.93


def cw(ch, size, bold):
    if ch == " ":
        return size * 0.30
    if ch.isdigit():
        return size * 0.62
    if ch.isupper():
        return size * (0.74 if bold else 0.72)
    if ch in "iljt.,:;!|'`[]()":
        return size * 0.28
    if ch in "mwMW":
        return size * 0.88
    if ch in "frt/\\-":
        return size * 0.38
    return size * (0.62 if bold else 0.58)


def tw(s, size, bold=False):
    return sum(cw(c, size, bold) for c in s)


def wrap(text, maxpx, size, bold=False):
    limit = maxpx * SAFETY
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if tw(trial, size, bold) <= limit or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Doc:
    """Collects SVG fragments; caller tracks y and passes the final height to render()."""

    def __init__(self, title):
        self.title, self.parts = title, []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=18, color=TXT, bold=False, anchor="start"):
        wt = "700" if bold else "400"
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{wt}" fill="{color}" text-anchor="{anchor}">{html.escape(s, quote=False)}</text>'
        )

    def block(self, x, y, text, size, color=TXT, bold=False, maxpx=1000, lh=None):
        """Paragraph. Returns the LAST baseline so the caller can keep stacking."""
        lh = lh or size * 1.45
        lines = wrap(text, maxpx, size, bold)
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size, color, bold)
        return y + (len(lines) - 1) * lh

    def rect(self, x, y, w, h, fill=PANEL, stroke=BORDER, rx=14, sw=1.2):
        self.add(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def dot(self, cx, cy, r, fill):
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"/>')

    def line(self, x1, y1, x2, y2, color=BORDER, sw=1, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{sw}"{da}/>'
        )

    def render(self, height, path):
        body = "\n".join(self.parts)
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                f'<!doctype html><html><head><meta charset="utf-8"><title>'
                f'{html.escape(self.title)}</title><style>html,body{{margin:0;padding:0;'
                f'background:{BG};}}svg{{display:block}}</style></head><body>\n'
                f'<svg width="{W}" height="{height}" viewBox="0 0 {W} {height}" '
                f'xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg></body></html>'
            )
        return height


def header(d, y, kicker, title, sub, note):
    """Title block. Baseline of each following block derives from the WRAPPED LINE COUNT,
    never a fixed offset — a two-line title otherwise sits on top of the subtitle."""
    d.text(PAD, y + 26, kicker, 19, CYAN, True)
    tl = wrap(title, W - 2 * PAD, 46, True)
    ty = y + 92
    for i, ln in enumerate(tl):
        d.text(PAD, ty + i * 56, ln, 46, TXT, True)
    yy = ty + (len(tl) - 1) * 56 + 58
    sl = wrap(sub, W - 2 * PAD, 21)
    for i, ln in enumerate(sl):
        d.text(PAD, yy + i * 31, ln, 21, MUTED)
    yy += (len(sl) - 1) * 31 + 30
    nl = wrap(note, W - 2 * PAD, 18)
    for i, ln in enumerate(nl):
        d.text(PAD, yy + i * 26, ln, 18, MUTED)
    return yy + (len(nl) - 1) * 26 + 48


def panel(d, px, y, pw, h, title, subtitle=None, inner=False):
    d.rect(px, y, pw, h, fill=INNER if inner else PANEL)
    bx = px + 28
    d.text(bx, y + 44, title, 22, TXT, True)
    if subtitle:
        d.text(px + pw - 28, y + 44, subtitle, 17, MUTED, False, "end")
    return bx  # content x


def main():
    outdir = os.path.expanduser("~/obsidian-vault/attachments")
    os.makedirs(outdir, exist_ok=True)

    # --- figure 1 ---------------------------------------------------------
    d = Doc("contoh halaman")
    d.rect(0, 0, W, 6000, fill=BG, stroke=BG, rx=0)   # backdrop taller than the page
    y = header(
        d, 42,
        "KICKER · JUDUL KECIL",
        "Judul besar yang boleh panjang dan membungkus dua baris",
        "Satu baris konteks: rentang waktu, modal, dan satuan angka yang dipakai.",
        "Catatan kejujuran: angka di halaman ini target, bukan hasil.",
    )
    px, pw = PAD, W - 2 * PAD
    bx = panel(d, px, y, pw, 240, "JUDUL PANEL", "subjudul kanan rata")
    d.block(bx, y + 84, "Isi panel ditulis lewat block() supaya tinggi baris terhitung sendiri.",
            17, BODY, maxpx=pw - 56, lh=28)
    y += 240 + 34

    # timeline: measure every card FIRST, then emit rail -> cards -> dots
    cards = [("FASE 1", "judul fase", ["aksi satu", "aksi dua"], "Rp0"), ("FASE 2", "fase dua", ["aksi"], "Rp750 rb")]
    card_x, card_w = bx + 76, px + pw - 28 - (bx + 76)
    heights = []
    for no, title, acts, money in cards:
        hb = sum(len(wrap(a, card_w - 86, 18)) for a in acts) * 30
        heights.append(138 + hb + 30)
    d.line(bx + 30, y + 10, bx + 30, y + sum(heights) + 22 * (len(cards) - 1) - 90, color=BORDER, sw=3)
    for (no, title, acts, money), ch in zip(cards, heights):
        d.rect(px, y, pw, ch)
        d.dot(bx + 30, y + 52, 15, CYAN)
        d.text(card_x, y + 84, title, 27, TXT, True)
        d.text(px + pw - 28, y + 44, money, 20, TXT, True, "end")
        yy = y + 120
        for a in acts:
            d.dot(card_x + 6, yy - 6, 4.5, CYAN)
            yy = d.block(card_x + 22, yy, a, 18, BODY, maxpx=card_w - 86, lh=30) + 30
        y += ch + 22

    h = d.render(y + 44, os.path.join(outdir, "contoh-halaman.html"))
    print(f"contoh-halaman\tH={int(h)}\t{os.path.join(outdir, 'contoh-halaman.html')}")


if __name__ == "__main__":
    main()
