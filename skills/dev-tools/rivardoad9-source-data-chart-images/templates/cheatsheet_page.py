#!/usr/bin/env python3
"""Threshold cheat-sheet -> PNG: HTML+CSS -> headless Chromium -> PIL auto-crop.

Copy, replace CARD content, run. No matplotlib, no image API, offline, real fonts.
Deliver with MEDIA:<abs path>. See data-chart-images SKILL.md for when to use this
vs the SVG chart pipeline.
"""
import glob, os, subprocess
from PIL import Image

BG, FG, MUT, GRID = "#0b1020", "#e6edf7", "#93a1b8", "#1e2740"
G, A, R, BL = "#35d07f", "#f5a623", "#ff5c5c", "#5aa9ff"
W, TALL = 1200, 3600          # CSS px; x2 device scale -> 2400 px wide PNG, auto-cropped

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:{BG};color:{FG};font-family:'DejaVu Sans',Verdana,sans-serif;
     padding:54px 54px 40px;width:{W}px}}
h1{{font-size:52px;line-height:1.1}} h1 .accent{{color:{BL}}}
.sub{{color:{MUT};font-size:22px;margin-top:12px;line-height:1.5}}
.sec{{margin-top:38px}}
.sec h2{{font-size:29px;padding-bottom:12px;border-bottom:2px solid {GRID};margin-bottom:20px}}
table{{width:100%;border-collapse:collapse;font-size:23px}}
th{{text-align:left;color:{MUT};font-size:19px;text-transform:uppercase;letter-spacing:1px;
    padding:10px 12px;border-bottom:2px solid {GRID}}}
td{{padding:11px 12px;border-bottom:1px solid {GRID}}}
tr:last-child td{{border-bottom:none}}
.g{{color:{G}}} .a{{color:{A}}} .r{{color:{R}}} .mu{{color:{MUT}}}
.big{{font-size:27px}}
.note{{margin-top:26px;background:#121a33;border-left:5px solid {A};padding:16px 20px;
       font-size:21px;line-height:1.55;border-radius:6px}}
.verdict{{margin-top:22px;background:#1a1220;border-left:5px solid {R};padding:18px 20px;
          font-size:23px;line-height:1.5;border-radius:6px}}
.foot{{margin-top:34px;padding-top:18px;border-top:2px solid {GRID};color:{MUT};font-size:18px;
       line-height:1.6}}
"""


def table(rows, head):
    h = "<tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr>"
    bodies = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table>{h}{bodies}</table>"


def render(html, png):
    """Write the page, screenshot it tall, crop the trailing background."""
    hp = png.replace(".png", ".html")
    open(hp, "w").write(
        f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html}</body></html>")
    ch = glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome"))[0]
    # stderr dbus noise is harmless; the PNG is written anyway
    subprocess.run([ch, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={W},{TALL}",
                    f"--screenshot={png}", "file://" + hp], capture_output=True)
    im = Image.open(png).convert("RGB")
    bb = im.convert("L").point(lambda v: 255 if v > 26 else 0).getbbox()  # >26 = not background
    if bb:
        im = im.crop((0, 0, im.width, min(im.height, bb[3] + 30)))
    im.save(png)
    size = im.size
    flag = "!! MUNGKIN KEPOTONG" if size[1] >= TALL * 2 - 40 else "ok"
    return size, flag


if __name__ == "__main__":
    rows = [
        ("Metrik contoh", f'<span class="g">&lt;20%</span>',
         '<span class="a">20&ndash;50%</span>', '<span class="r">&gt;50%</span>'),
    ]
    html = f"""<h1>JUDUL <span class="accent">KARTU</span></h1>
<div class="sub">Sumber + window data + tanggal. Sebut apa yang angka ini bukan.</div>
<div class="sec"><h2>Ambang batas per metrik</h2>
{table(rows, ["Metrik", "\U0001f7e2 Bagus", "\U0001f7e1 Hati-hati", "\U0001f534 Jangan"])}
<div class="note">Satu takeaway per section, di kotak callout.</div></div>
<div class="foot">Bacaan rule-based, bukan saran investasi.</div>"""
    out = os.path.expanduser("~/obsidian-vault/attachments/contoh-cheatsheet.png")
    print(out, *render(html, out))
