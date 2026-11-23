#!/usr/bin/env python3
"""Template: dark-theme SVG chart page rendered to PNG by headless Chromium.

Copy, then replace DATA + the panel bodies. Verify with vision_analyze() after rendering.

    python3 chart_page.py                 # writes /tmp/chart.html, prints "H=<doc height>"
    CH=~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome
    H=$(python3 chart_page.py | sed 's/H=//')
    "$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars \
          --force-device-scale-factor=2 --window-size=1360,$H \
          --screenshot=/tmp/chart.png file:///tmp/chart.html
"""
import json

# ---------------------------------------------------------------- palette / page
BG, FG, MUT, GRID = '#0b1020', '#e6edf7', '#93a1b8', '#1e2740'
GREEN, RED, AMBER, BLUE, PURPLE = '#2ee6a8', '#ff5c7a', '#ffb020', '#3b7dff', '#c9a4ff'
FONT = "font-family:'DejaVu Sans',Arial,Helvetica,sans-serif"
W = 1360

DATA = json.load(open('/tmp/chart_data.json'))          # <- numbers come from here, never typed


def head(title, sub):
    """Page header. `sub` may contain real newlines; its line count feeds the height budget."""
    lines = 1 + sub.count('\n')
    top = 74 + lines * 21
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
    html,body{{margin:0;padding:0;background:{BG};color:{FG};{FONT}}}
    body{{width:{W}px}}
    .title{{font-size:29px;font-weight:700;padding:20px 30px 0}}
    .sub{{font-size:15.5px;color:{MUT};padding:9px 30px 0;line-height:1.5}}
    text{{ {FONT} }}
    table{{border-collapse:collapse;margin:16px 30px 0;font-size:15px}}
    td,th{{padding:7px 14px;border-bottom:1px solid {GRID};text-align:right}}
    th{{color:{MUT};font-weight:600;font-size:14px}}
    td.l,th.l{{text-align:left}}
    </style></head><body><div class="title">{title}</div><div class="sub">{sub}</div>"""
    return html, top


def line_panel(series, ymin=None, ymax=None, xlabel='index', caption='', h=500):
    """series = [{'values': [...], 'color': GREEN, 'label': '$752', 'sub': '121 trade'},
                 {'values': [...], 'band': {'p5': [...], 'p95': [...]}}]

    Axis top is capped at a percentile of the final values by the CALLER (see pitfall: an outlier
    curve will otherwise flatten everything and pile the tick labels up).
    """
    L, R, BOT, TOP = 130, 1000, h - 80, 60
    allv = [v for s in series for v in s['values']]
    lo = ymin if ymin is not None else min(0, min(allv))
    hi = ymax if ymax is not None else max(allv) * 1.08
    n = max(len(s['values']) for s in series) - 1
    x = lambda i: L + i / n * (R - L)
    y = lambda v: BOT - (v - lo) / (hi - lo) * (BOT - TOP)
    step = 100.0
    while (hi - lo) / step > 12:
        step *= 2
    out = [f'<svg width="{W}" height="{h}">',
           f'<text x="{L}" y="{TOP-22}" font-size="18" fill="{FG}">{caption}</text>',
           f'<clipPath id="plot"><rect x="{L}" y="{TOP}" width="{R-L}" height="{BOT-TOP}"/></clipPath>']
    v = lo
    while v <= hi:
        out.append(f'<line x1="{L}" y1="{y(v):.1f}" x2="{R}" y2="{y(v):.1f}" stroke="{GRID}"/>')
        out.append(f'<text x="{L-14}" y="{y(v)+5:.1f}" font-size="13" fill="{MUT}" text-anchor="end">{v:,.0f}</text>')
        v += step
    for i in range(0, n + 1, max(1, n // 6)):
        out.append(f'<text x="{x(i):.1f}" y="{BOT+26}" font-size="13" fill="{MUT}" text-anchor="middle">{i}</text>')
    out.append(f'<text x="{(L+R)/2}" y="{BOT+52}" font-size="14" fill="{MUT}" text-anchor="middle">{xlabel}</text>')
    for s in series:
        if 'band' in s:                                  # shaded confidence band
            b, t = s['band']['p5'], s['band']['p95']
            pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(b)) + " " + \
                  " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in reversed(list(enumerate(t))))
            out.append(f'<polygon points="{pts}" fill="{s["color"]}" opacity="0.16" clip-path="url(#plot)"/>')
        pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(s['values']))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{s["color"]}" stroke-width="3.2" clip-path="url(#plot)"/>')
        last = s['values'][-1]
        out.append(f'<text x="{R+16}" y="{y(last)+5:.1f}" font-size="15" fill="{s["color"]}">{s["label"]}</text>')
        if s.get('sub'):
            out.append(f'<text x="{R+16}" y="{y(last)+26:.1f}" font-size="13.5" fill="{MUT}">{s["sub"]}</text>')
    out.append('</svg>')
    return "\n".join(out)


def bar_panel(bars, caption, h=330, base=None, maxv=None):
    """bars = [(label, value, colour), ...] — one idea per panel; heading sits 60px above tallest bar."""
    base = base or h - 70
    maxv = maxv or max(v for _, v, _ in bars) * 1.15
    out = [f'<svg width="{W}" height="{h}">',
           f'<text x="130" y="38" font-size="18" fill="{FG}">{caption}</text>']
    for i, (lab, val, col) in enumerate(bars):
        bx, bw = 160 + i * 210, 140
        bh = val / maxv * (base - 90)
        out.append(f'<rect x="{bx}" y="{base-bh:.1f}" width="{bw}" height="{bh:.1f}" rx="6" fill="{col}" opacity="0.85"/>')
        out.append(f'<text x="{bx+bw/2}" y="{base-bh-12:.1f}" font-size="19" fill="{col}" text-anchor="middle">{val:,.2f}</text>')
        out.append(f'<text x="{bx+bw/2}" y="{base+26}" font-size="14" fill="{MUT}" text-anchor="middle">{lab}</text>')
    out.append(f'<line x1="140" y1="{base}" x2="{min(W-40, 160+len(bars)*210)}" y2="{base}" stroke="{GRID}"/>')
    out.append('</svg>')
    return "\n".join(out)


def table(rows, headers):
    cells = "".join(f'<th class="l">{h}</th>' for h in headers)
    body = "".join("<tr>" + "".join(f'<td class="l">{c}</td>' for c in r) + "</tr>" for r in rows)
    return f'<table><tr>{cells}</tr>{body}</table>'


def note(text):
    return f'<div style="padding:16px 30px 24px;font-size:14.5px;color:{MUT};line-height:1.65">{text}</div>'


def main():
    sub = ("Satu baris penjelasan: data dari mana, window berapa, dan apa yang angka ini BUKAN.\n"
           "Baris kedua kalau perlu. Gambar ini harus bisa dibaca tanpa chat-nya.")
    html, top = head("Judul panel", sub)
    body = line_panel(
        [{'values': DATA['a'], 'color': GREEN, 'label': f"${DATA['a'][-1]:,.0f}", 'sub': '121 trade · 15 pool'},
         {'values': DATA['b'], 'color': RED, 'label': f"${DATA['b'][-1]:,.0f}", 'sub': '43 trade · 3 pool'}],
        caption='equity (compounded)')
    body += bar_panel([('gate 1,0x', 2.34, GREEN), ('gate 2,5x (live)', 5.85, RED)],
                      'lantai fee/TVL yang dituntut gate')
    body += table([["baris 1", "+$333,79", "93,9%"], ["baris 2", "-$51,79", "3,6%"]],
                  ["konfigurasi", "net", "P(profit)"])
    body += note("Teks bawah: caveat + kesimpulan satu kalimat. Kalau baris ini kepotong, "
                 "naikin H ±120px dan render ulang.")
    open('/tmp/chart.html', 'w').write(html + body + "</body></html>")
    # height budget: top (title+sub) + panels + table + note. Verify visually, then trust it.
    print(f"H={top + 500 + 330 + 210 + 120}")


if __name__ == '__main__':
    main()
