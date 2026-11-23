#!/usr/bin/env python3
"""Per-cell / per-chip measurement of ONE table row — use when a row is unexpectedly tall.

Usage: /tmp/pwenv/bin/python mobile_probe_row.py [URL] [ROW_SELECTOR]

Prints the grid areas, each td's height/width/grid-area, and every chip width + top offset.
A chip `top` that differs from its siblings = the chip row WRAPPED (that is what makes a
mobile card 138px instead of ~85px). Fix by spanning the chip cell across all grid columns,
or by shortening the chip labels.
"""
import json
import sys

from playwright.sync_api import sync_playwright

CHROME = "/home/ubuntu/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome"
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8787/"
SEL = sys.argv[2] if len(sys.argv) > 2 else "tr.row"

JS = r"""
([sel]) => {
  const row = document.querySelector(sel);
  if (!row) return {err: 'no row for ' + sel};
  const out = {row: Math.round(row.getBoundingClientRect().height),
    grid: getComputedStyle(row).gridTemplateColumns, areas: getComputedStyle(row).gridTemplateAreas,
    tds: [], chips: []};
  row.querySelectorAll('td').forEach((td, i) => {
    const r = td.getBoundingClientRect();
    out.tds.push({i: i+1, h: Math.round(r.height), w: Math.round(r.width), L: Math.round(r.left),
      R: Math.round(r.right), area: getComputedStyle(td).gridArea,
      txt: td.textContent.trim().replace(/\s+/g,' ').slice(0,45)});
  });
  const c = row.querySelector('.chips');
  if (c) {
    out.chipsBox = {h: Math.round(c.getBoundingClientRect().height), w: Math.round(c.getBoundingClientRect().width)};
    c.querySelectorAll('.chip').forEach(ch => {
      const rr = ch.getBoundingClientRect();
      out.chips.push({t: ch.textContent.trim(), w: Math.round(rr.width), h: Math.round(rr.height), top: Math.round(rr.top)});
    });
  }
  const t = document.querySelector('.tw,.tc,table');
  if (t) out.tableW = Math.round(t.getBoundingClientRect().width);
  return out;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                        is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.goto(URL, wait_until="networkidle", timeout=45000)
    pg.wait_for_timeout(2500)
    print(json.dumps(pg.evaluate(JS, [SEL]), indent=1, ensure_ascii=False))
    b.close()
