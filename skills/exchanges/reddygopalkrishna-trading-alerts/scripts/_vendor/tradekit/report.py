"""Self-contained HTML reports with inline SVG charts (no JS, no CDN)."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

CSS = """
:root{--bg:#0f1115;--card:#171a21;--ink:#e6e8ee;--muted:#9aa3b2;--line:#2a2f3a;--pos:#2fbf71;--neg:#e5484d;--acc:#4c8dff}
@media (prefers-color-scheme: light){:root{--bg:#f7f8fa;--card:#fff;--ink:#14161b;--muted:#5b6475;--line:#e3e6ec}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:1080px;margin:0 auto;padding:28px 20px 60px}h1{font-size:22px;margin:0 0 4px}h2{font-size:15px;margin:28px 0 10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.sub{color:var(--muted);margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}.kpi .l{color:var(--muted);font-size:12px}.kpi .v{font-size:20px;font-weight:600;font-variant-numeric:tabular-nums}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}th:first-child,td:first-child{text-align:left}th{color:var(--muted);font-weight:500}
.pos{color:var(--pos)}.neg{color:var(--neg)}.warn{border-left:3px solid #f5a524;padding:8px 12px;background:var(--card);margin:6px 0;border-radius:6px}
footer{color:var(--muted);font-size:12px;margin-top:30px}svg text{fill:var(--muted);font-size:11px}
"""


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def fmt(v, digits: int = 2, pct: bool = False) -> str:
    if v is None:
        return "-"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, int) or (isinstance(v, float) and v.is_integer() and abs(v) >= 1 and not pct):
        return f"{int(v):,}" + ("%" if pct else "")
    if isinstance(v, (int, float)):
        s = f"{v:,.{digits}f}"
        return s + ("%" if pct else "")
    return esc(v)


def kpis(items: Sequence[Tuple[str, object, str]]) -> str:
    """items: (label, value, kind) kind in '', 'pct', 'signed', 'signedpct'"""
    out = ['<div class="grid">']
    for label, val, kind in items:
        cls = ""
        if kind.startswith("signed") and isinstance(val, (int, float)):
            cls = "pos" if val > 0 else "neg" if val < 0 else ""
        out.append(f'<div class="kpi"><div class="l">{esc(label)}</div>'
                   f'<div class="v {cls}">{fmt(val, 2, pct=kind.endswith("pct"))}</div></div>')
    out.append("</div>")
    return "".join(out)


def line_chart(series: List[Tuple[str, List[Tuple[str, float]], str]], width: int = 1000, height: int = 280,
               log: bool = False) -> str:
    """series: [(name, [(date, value)...], css color)]"""
    import math
    pts = [v for _, s, _ in series for _, v in s if v is not None]
    if not pts:
        return ""
    tf = (lambda x: math.log(x)) if log and min(pts) > 0 else (lambda x: x)
    lo, hi = tf(min(pts)), tf(max(pts))
    if hi == lo:
        hi = lo + 1
    pad_l, pad_r, pad_t, pad_b = 60, 10, 10, 24
    W, H = width - pad_l - pad_r, height - pad_t - pad_b
    n = max(len(s) for _, s, _ in series)
    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img">']
    for k in range(5):
        y = pad_t + H * k / 4
        val = hi - (hi - lo) * k / 4
        label = math.exp(val) if log and min(pts) > 0 else val
        parts.append(f'<line x1="{pad_l}" x2="{width - pad_r}" y1="{y:.1f}" y2="{y:.1f}" stroke="var(--line)"/>'
                     f'<text x="{pad_l - 6}" y="{y + 4:.1f}" text-anchor="end">{label:,.0f}</text>')
    first = series[0][1]
    for k in range(0, 5):
        idx = int((len(first) - 1) * k / 4) if first else 0
        if first:
            x = pad_l + W * idx / max(1, n - 1)
            anchor = "start" if k == 0 else "end" if k == 4 else "middle"
            parts.append(f'<text x="{x:.1f}" y="{height - 6}" text-anchor="{anchor}">{esc(first[idx][0][:10])}</text>')
    for name, s, color in series:
        if not s:
            continue
        coords = []
        for i, (_, v) in enumerate(s):
            if v is None:
                continue
            x = pad_l + W * i / max(1, len(s) - 1)
            y = pad_t + H * (1 - (tf(v) - lo) / (hi - lo))
            coords.append(f"{x:.1f},{y:.1f}")
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="1.8" points="{" ".join(coords)}">'
                     f'<title>{esc(name)}</title></polyline>')
    legend_x = pad_l + 8
    for name, _, color in series:
        parts.append(f'<rect x="{legend_x}" y="{pad_t + 4}" width="10" height="3" fill="{color}"/>'
                     f'<text x="{legend_x + 14}" y="{pad_t + 9}">{esc(name)}</text>')
        legend_x += 14 + 8 * len(name) + 16
    parts.append("</svg>")
    return "".join(parts)


def area_chart(values: List[Tuple[str, float]], width: int = 1000, height: int = 140, color: str = "var(--neg)") -> str:
    if not values:
        return ""
    lo = min(v for _, v in values)
    lo = lo if lo < 0 else -1
    pad_l, pad_t, pad_b = 60, 8, 18
    W, H = width - pad_l - 10, height - pad_t - pad_b
    coords = [f"{pad_l},{pad_t}"]
    for i, (_, v) in enumerate(values):
        x = pad_l + W * i / max(1, len(values) - 1)
        y = pad_t + H * (v / lo)
        coords.append(f"{x:.1f},{y:.1f}")
    coords.append(f"{pad_l + W},{pad_t}")
    return (f'<svg viewBox="0 0 {width} {height}" width="100%" role="img">'
            f'<text x="{pad_l - 6}" y="{pad_t + 4}" text-anchor="end">0%</text>'
            f'<text x="{pad_l - 6}" y="{pad_t + H}" text-anchor="end">{lo:.0f}%</text>'
            f'<polygon fill="{color}" fill-opacity=".35" stroke="{color}" points="{" ".join(coords)}"/></svg>')


def histogram_chart(bins: List[Dict], width: int = 1000, height: int = 200) -> str:
    if not bins:
        return ""
    mx = max(b["count"] for b in bins) or 1
    pad_l, pad_b, pad_t = 40, 24, 8
    W, H = width - pad_l - 10, height - pad_b - pad_t
    bw = W / len(bins)
    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img">']
    for i, b in enumerate(bins):
        h = H * b["count"] / mx
        x = pad_l + i * bw
        color = "var(--pos)" if b["lo"] >= 0 else "var(--neg)" if b["hi"] <= 0 else "var(--acc)"
        parts.append(f'<rect x="{x + 1:.1f}" y="{pad_t + H - h:.1f}" width="{bw - 2:.1f}" height="{h:.1f}" fill="{color}">'
                     f'<title>{b["lo"]:.2f} to {b["hi"]:.2f}: {b["count"]}</title></rect>')
        if i % max(1, len(bins) // 6) == 0:
            parts.append(f'<text x="{x + bw / 2:.1f}" y="{height - 6}" text-anchor="middle">{b["lo"]:.1f}</text>')
    parts.append("</svg>")
    return "".join(parts)


def table(rows: List[Dict], columns: Sequence[Tuple[str, str]], limit: Optional[int] = None,
          signed: Sequence[str] = ()) -> str:
    rows = rows[:limit] if limit else rows
    head = "".join(f"<th>{esc(label)}</th>" for _, label in columns)
    body = []
    for r in rows:
        cells = []
        for key, _ in columns:
            v = r.get(key)
            cls = ""
            if key in signed and isinstance(v, (int, float)):
                cls = ' class="pos"' if v > 0 else ' class="neg"' if v < 0 else ""
            cells.append(f"<td{cls}>{fmt(v) if isinstance(v, (int, float)) else esc(v)}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="card"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def page(title: str, subtitle: str, sections: Sequence[Tuple[str, str]], disclaimer: str) -> str:
    body = "".join(f"<h2>{esc(h)}</h2>{content}" if h else content for h, content in sections)
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{CSS}</style></head>'
            f'<body><main><h1>{esc(title)}</h1><div class="sub">{esc(subtitle)}</div>{body}'
            f'<footer>Generated by trading-skills. {esc(disclaimer)}</footer></main></body></html>')


def write(path: str, content: str) -> str:
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return str(p.resolve())
