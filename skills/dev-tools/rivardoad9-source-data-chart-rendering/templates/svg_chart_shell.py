#!/usr/bin/env python3
"""Template: data JSON -> dark-theme SVG-in-HTML -> screenshot to PNG with headless Chromium.

Copy this file, replace `DATA_PATH` + the chart functions' bodies with your own series, run it,
then screenshot each generated HTML at the EXACT height this script prints.

    python3 chart_shell.py            # prints "chart1: WxH ..."
    CH=$(ls -d ~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome | head -1)
    "$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars \
          --force-device-scale-factor=2 --window-size=1360,<H> \
          --screenshot=/tmp/chart1.png file:///tmp/chart1.html

Rules baked in (each one came from a broken chart):
  * head() returns the document height -- feed it to --window-size, or the bottom rows get clipped.
  * real "\n" (never "\\n") in sub text; head() counts lines from it.
  * value labels live OUTSIDE the plot (right column), never on top of the lines.
  * clouds/outliers are clipped with <clipPath> and the y-range is capped by a percentile.
  * tick step is adaptive so labels never collide.
  * ALWAYS look at the PNG with vision before sending it to the user.
"""
import json, math

DATA_PATH = '/tmp/chart_data.json'
OUT_HTML = '/tmp/chart1.html'
W = 1360                     # canvas width; plot area should end ~1150 to leave a label column
BG, FG, MUT, GRID = '#0b1020', '#e6edf7', '#93a1b8', '#1e2740'
BLUE, GREEN, RED, AMBER, PURPLE = '#3b7dff', '#2ee6a8', '#ff5c7a', '#ffb020', '#c9a4ff'
F = "font-family:'DejaVu Sans',Arial,Helvetica,sans-serif"

D = json.load(open(DATA_PATH))


def head(title: str, sub: str, svg_h: int, foot_h: int = 0):
    """Returns (html_prefix, document_height_px). Height assumes ~1.5 line-height at 15.5px."""
    lines = 1 + sub.count('\n')
    total = int(74 + lines * 21 + svg_h + foot_h + 26)
    prefix = f"""<!doctype html><html><head><meta charset="utf-8"><style>
    html,body{{margin:0;padding:0;background:{BG};color:{FG};{F}}}
    body{{width:{W}px}}
    .title{{font-size:29px;font-weight:700;padding:20px 30px 0}}
    .sub{{font-size:15.5px;color:{MUT};padding:9px 30px 0;line-height:1.5}}
    text{{ {F} }}
    </style></head><body><div class="title">{title}</div><div class="sub">{sub}</div>"""
    return prefix, total


def nice_step(lo: float, hi: float, max_ticks: int = 12) -> float:
    """Adaptive gridline step so tick labels never collide."""
    step = 1.0
    span = max(hi - lo, 1e-9)
    while span / step > max_ticks:
        step *= 2
    return step


def usd(v: float) -> str:
    return f"${v:,.0f}"


# ---------------------------------------------------------------- example: equity + band chart
def chart_equity():
    oos = D['oosCurve']                     # list[float], index 0 = starting capital
    bands = D.get('mcBands', {})            # {'p5': [...], 'p50': [...], 'p95': [...]} optional
    samples = D.get('mcSampleCurves', [])   # list of thin background curves, optional
    capital = oos[0]
    n = len(oos) - 1

    L, R, TOP, BOT = 130, 1150, 200, 690    # plot box; R+label column must fit inside W
    ymin = capital * 0.9
    # cap the y-range on a percentile so a few runaway simulations cannot flatten the chart
    ymax = max(bands.get('p95', [max(oos)])[-1], max(oos)) * 1.25
    step = nice_step(ymin, ymax)
    x = lambda i: L + i / max(n, 1) * (R - L)
    y = lambda v: BOT - (min(v, ymax) - ymin) / (ymax - ymin) * (BOT - TOP)

    svg_h = BOT + 108
    s, total = head(
        "1 · Equity + ketidakpastian",
        "Garis tebal = hasil yang benar-benar terjadi. Awan = resample dari trade yang sama: "
        "tiap garis = \"bagaimana kalau urutannya beda\".\nYang penting batas bawahnya, bukan garis "
        "yang paling atas.", svg_h, foot_h=64)

    s += (f'<svg width="{W}" height="{svg_h}"><defs><clipPath id="plot">'
          f'<rect x="{L}" y="{TOP}" width="{R-L}" height="{BOT-TOP}"/></clipPath></defs>')
    v = ymin + step
    while v < ymax:
        s += f'<line x1="{L}" y1="{y(v):.1f}" x2="{R}" y2="{y(v):.1f}" stroke="{GRID}"/>'
        s += f'<text x="{L-14}" y="{y(v)+5:.1f}" font-size="13" fill="{MUT}" text-anchor="end">{usd(v)}</text>'
        v += step
    for i in range(0, n + 1, max(1, n // 6 or 1)):
        s += f'<line x1="{x(i):.1f}" y1="{TOP-10}" x2="{x(i):.1f}" y2="{BOT}" stroke="{GRID}" stroke-dasharray="2 6"/>'
        s += f'<text x="{x(i):.1f}" y="{BOT+26}" font-size="13" fill="{MUT}" text-anchor="middle">{i}</text>'
    s += (f'<line x1="{L}" y1="{y(capital):.1f}" x2="{R}" y2="{y(capital):.1f}" stroke="{MUT}" stroke-dasharray="7 5"/>'
          f'<text x="{L+10}" y="{y(capital)-9:.1f}" font-size="13" fill="{MUT}">modal awal (impas)</text>')
    s += '<g clip-path="url(#plot)">'
    for c in samples[:120]:                                   # thin background cloud
        pts = " ".join(f"{x(i):.1f},{y(vv):.1f}" for i, vv in enumerate(c))
        s += f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="0.7" opacity="0.20"/>'
    if bands:
        up = " ".join(f"{x(i):.1f},{y(bands['p95'][i]):.1f}" for i in range(len(bands['p95'])))
        dn = " ".join(f"{x(i):.1f},{y(bands['p5'][i]):.1f}" for i in range(len(bands['p5']) - 1, -1, -1))
        s += f'<polygon points="{up} {dn}" fill="{BLUE}" opacity="0.18"/>'
        for k in ('p5', 'p95'):
            pts = " ".join(f"{x(i):.1f},{y(bands[k][i]):.1f}" for i in range(len(bands[k])))
            s += f'<polyline points="{pts}" fill="none" stroke="#a8c9ff" stroke-width="1.7" stroke-dasharray="6 4"/>'
        med = " ".join(f"{x(i):.1f},{y(bands['p50'][i]):.1f}" for i in range(len(bands['p50'])))
        s += f'<polyline points="{med}" fill="none" stroke="{PURPLE}" stroke-width="2.2" stroke-dasharray="8 5"/>'
    real = " ".join(f"{x(i):.1f},{y(vv):.1f}" for i, vv in enumerate(oos))
    s += f'<polyline points="{real}" fill="none" stroke="{GREEN}" stroke-width="3.6"/></g>'
    # value labels OUTSIDE the plot, so they never sit on top of a line
    if bands:
        for txt, vv, col in ((f"p95 {usd(bands['p95'][-1])}", bands['p95'][-1], '#a8c9ff'),
                             (f"median {usd(bands['p50'][-1])}", bands['p50'][-1], PURPLE),
                             (f"nyata {usd(oos[-1])}", oos[-1], GREEN),
                             (f"p5 {usd(bands['p5'][-1])}", bands['p5'][-1], '#a8c9ff')):
            s += f'<text x="{R+12}" y="{y(vv)+5:.1f}" font-size="14" fill="{col}">{txt}</text>'
    s += '</svg></body></html>'
    open(OUT_HTML, 'w').write(s)
    return total


# ---------------------------------------------------------------- example: two-panel bar chart
def chart_bars(labels, values, colors, title, sub, left=(0, 1)):
    """Simple vertical bars. left=(i,j) indexes into labels/values to draw a '−x%' gap marker."""
    svg_h, base, W_plot = 600, 520, 300
    s, total = head(title, sub, svg_h, foot_h=40)
    s += f'<svg width="{W}" height="{svg_h}">'
    mx = max(values) or 1
    for i, (lab, v, col) in enumerate(zip(labels, values, colors)):
        bx = 150 + i * 210
        bh = max(v / mx * W_plot, 8)
        s += f'<rect x="{bx}" y="{base-bh:.1f}" width="140" height="{bh:.1f}" rx="6" fill="{col}" opacity="0.85"/>'
        s += f'<text x="{bx+70}" y="{base-bh-18:.1f}" font-size="24" fill="{col}" text-anchor="middle">{v:,.2f}</text>'
        s += f'<text x="{bx+70}" y="{base+30}" font-size="15" fill="{MUT}" text-anchor="middle">{lab}</text>'
    s += f'<line x1="110" y1="{base}" x2="600" y2="{base}" stroke="{GRID}"/>'
    if left and len(values) > 1:
        i, j = left
        delta = (values[j] / values[i] - 1) * 100 if values[i] else 0
        s += (f'<text x="640" y="250" font-size="44" fill="{RED}" text-anchor="middle">{delta:+.0f}%</text>'
              f'<text x="640" y="282" font-size="13" fill="{MUT}" text-anchor="middle">selisih dua angka ini</text>')
    s += '</svg></body></html>'
    open('/tmp/chart_bars.html', 'w').write(s)
    return total


if __name__ == '__main__':
    h = chart_equity()
    print(f"chart1: {W}x{h}  ->  --window-size={W},{h}")
