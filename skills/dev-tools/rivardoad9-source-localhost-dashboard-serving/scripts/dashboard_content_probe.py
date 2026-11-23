#!/usr/bin/env python3
"""Content + layout probe for a local dashboard page (companion to mobile_probe.py).

mobile_probe.py answers "does it overflow / wrap?". This one answers "does it render the RIGHT VALUES?",
which is what catches formatter bugs (`+0.0%M`), charts that silently dropped a segment, and JS that
throws before painting — none of which are visible in a screenshot.

Usage:
  /tmp/pwenv/bin/python dashboard_content_probe.py URL [SELECTOR[,SELECTOR...]] [TAG]

Default selectors are the ones that mattered on the portfolio-risk page; pass your own list for another
page, e.g. ".leg .it,.mx .v,.ni .t". Prints JSON:
  viewports[]        overflow px per viewport (0 = good), section/card counts, screenshot path
  checks[]           count + innerText of each selector
  errors[]           pageerrors and console errors/warnings (a silent JS syntax error shows up here)
  json_meta          _age_s / _running / _err if the page's /api/... payload carries them

Needs playwright in a venv + a chromium build in ~/.cache/ms-playwright (auto-detected; `executable_path`
is passed explicitly because the installed build is often OLDER than the driver's expectation and launch
otherwise fails with "Executable doesn't exist").
"""
import glob
import json
import os
import sys

from playwright.sync_api import sync_playwright

CANDS = sorted(glob.glob("/home/ubuntu/.cache/ms-playwright/chromium-*/chrome-linux64/chrome"))
CHROME = CANDS[-1] if CANDS else None

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8787/"
SELS = (sys.argv[2] if len(sys.argv) > 2 else ".leg .it,.ocgrid,.tok,.ni,.note").split(",")
TAG = sys.argv[3] if len(sys.argv) > 3 else "probe"


def snapshot(pg, w, h):
    """Overflow + structure counts for one viewport."""
    return pg.evaluate("""() => ({
      vw: document.documentElement.clientWidth,
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      cards: document.querySelectorAll('.card').length,
      h1: (document.querySelector('h1')||{}).textContent,
      stamp: (document.getElementById('stamp')||{}).textContent,
      counts: {leg: document.querySelectorAll('.leg .it').length,
               tok: document.querySelectorAll('.tok').length,
               ni: document.querySelectorAll('.ni').length},
      svg_segments: document.querySelectorAll('svg circle').length,
      donut_center: (document.querySelector('.donut .mid')||{}).innerText
    })""").update({"w": w, "h": h}) or None


def run(pg, w, h, shot):
    errs = []
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:200]))
    pg.on("console", lambda m: errs.append(f"{m.type}: {m.text[:200]}")
          if m.type in ("error", "warning") else None)
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(1500)
    info = pg.evaluate("""() => ({
      vw: document.documentElement.clientWidth,
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      cards: document.querySelectorAll('.card').length,
      h1: (document.querySelector('h1')||{}).textContent,
      stamp: (document.getElementById('stamp')||{}).textContent,
      counts: {leg: document.querySelectorAll('.leg .it').length,
               tok: document.querySelectorAll('.tok').length,
               ni: document.querySelectorAll('.ni').length},
      svg_segments: document.querySelectorAll('svg circle').length,
      donut_center: (document.querySelector('.donut .mid')||{}).innerText
    })""")
    checks = []
    for s in SELS:
        s = s.strip()
        if not s:
            continue
        checks.append({"sel": s, "n": pg.eval_on_selector_all(s, "els => els.length"),
                       "text": pg.eval_on_selector_all(
                           s, "els => els.slice(0,8).map(e => (e.innerText||'').replace(/\\s+/g,' ').trim())")})
    pg.screenshot(path=shot, full_page=True)
    return {"w": w, "h": h, "shot": shot, "info": info, "checks": checks, "errors": errs}


def main():
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"])
        for w, h, tag in [(390, 844, "hp"), (1366, 900, "desk")]:
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2 if w < 500 else 1)
            out[tag] = run(pg, w, h, f"/tmp/content_{TAG}_{tag}.png")
        b.close()
    print(json.dumps(out, ensure_ascii=False, indent=1))
    bad = [f"{k}: overflow={v['info']['overflow']}" for k, v in out.items() if v["info"]["overflow"]]
    errs = [(k, e) for k, v in out.items() for e in v["errors"]]
    print("ASSERT overflow==0:", "OK" if not bad else "FAIL " + "; ".join(bad))
    print("ASSERT no js errors:", "OK" if not errs else f"CHECK {errs[:4]}")
    print("REMINDER: compare the printed innerText values against the source dataset — "
          "the page is a view, not the truth.")


if __name__ == "__main__":
    main()
