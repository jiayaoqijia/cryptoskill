#!/usr/bin/env python3
"""Mobile/desktop layout probe for a local dashboard page.

Usage:
  /tmp/pwenv/bin/python mobile_probe.py [URL] [TAG]

Needs: playwright installed in a venv (~/.hermes/bin/uv pip install --python /tmp/pwenv/bin/python playwright)
and a chromium build on disk. On this host the binary is auto-detected below; no `chromium` on PATH needed.

Prints, per viewport: clientWidth vs scrollWidth (equal = no sideways scroll), every element whose
rect pokes past the viewport (the overflow offenders), row heights, and saves screenshots you can
then read with vision_analyze:
  /tmp/mob_<TAG>.png         full page, 390x844 @2x (phone)
  /tmp/mob_<TAG>_top.png     first phone screen
  /tmp/mob_<TAG>_edit.png    phone, first screen, ?k=TOKEN (edit mode)
  /tmp/mob_<TAG>_coins.png   phone, second tab, full page
  /tmp/mob_<TAG>_wal.png     phone, third tab, full page
  /tmp/desk_<TAG>.png        desktop 1366px (regression check)
"""
import glob
import json
import os
import sys

from playwright.sync_api import sync_playwright

CANDIDATES = sorted(glob.glob("/home/ubuntu/.cache/ms-playwright/chromium-*/chrome-linux64/chrome"))
CHROME = CANDIDATES[-1] if CANDIDATES else None
if not CHROME:
    # fall back to a plain-browser install if the playwright cache is gone
    for c in ("/usr/bin/chromium", "/usr/bin/google-chrome", "/usr/bin/chromium-browser"):
        if os.path.exists(c):
            CHROME = c
            break
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8787/"
TAG = sys.argv[2] if len(sys.argv) > 2 else "probe"

PROBE = r"""
() => {
  const vw = document.documentElement.clientWidth;
  const out = {vw, docScrollW: document.documentElement.scrollWidth,
    bodyScrollW: document.body.scrollWidth, overflow: [], rows: [], tabs: [], hdr: 0};
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (r.right > vw + 1.5 || r.left < -1.5) {
      out.overflow.push({tag: el.tagName.toLowerCase(), cls: (el.className||'').toString().slice(0,30),
        id: el.id||'', L: Math.round(r.left), R: Math.round(r.right), W: Math.round(r.width),
        txt: (el.textContent||'').trim().replace(/\s+/g,' ').slice(0,40)});
    }
  });
  document.querySelectorAll('tr.row').forEach((tr,i) => {
    if (i<3) { const r=tr.getBoundingClientRect();
      out.rows.push({i, h:Math.round(r.height), w:Math.round(r.width), L:Math.round(r.left), R:Math.round(r.right),
        txt:(tr.textContent||'').trim().replace(/\s+/g,' ').slice(0,70)}); }
  });
  const tb=document.querySelector('.tabs');
  if(tb){const r=tb.getBoundingClientRect(); out.tabs=[Math.round(r.left),Math.round(r.right),Math.round(r.width)];}
  const h=document.querySelector('header');
  if(h){out.hdr=Math.round(h.getBoundingClientRect().height);}
  return out;
}
"""


def dump(label, m):
    print(f"== {label} ==")
    print("vw", m["vw"], "docScrollW", m["docScrollW"], "bodyScrollW", m["bodyScrollW"],
          "headerH", m.get("hdr"), "tabs", m["tabs"])
    print("overflow", len(m["overflow"]), "| rows", [(r["h"], r["w"], r["R"]) for r in m["rows"]])
    for o in m["overflow"][:8]:
        print("   ", o["tag"], o["cls"], o["id"], "L", o["L"], "R", o["R"], "W", o["W"], "|", o["txt"][:38])


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"])
    phone = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                          is_mobile=True, has_touch=True)
    pg = phone.new_page()
    pg.goto(URL, wait_until="networkidle", timeout=45000)
    pg.wait_for_timeout(2500)
    dump("MOBILE 390x844", pg.evaluate(PROBE))
    pg.screenshot(path=f"/tmp/mob_{TAG}.png", full_page=True)
    pg.screenshot(path=f"/tmp/mob_{TAG}_top.png")

    pg.goto(URL + ("&" if "?" in URL else "?") + "k=TESTKEY", wait_until="networkidle", timeout=45000)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=f"/tmp/mob_{TAG}_edit.png", full_page=True)

    for i, name in enumerate(["coin", "wal"], start=2):
        pg.evaluate(f"tab('{name}')")
        pg.wait_for_timeout(700)
        dump(f"MOBILE tab {name}", pg.evaluate(PROBE))
        pg.screenshot(path=f"/tmp/mob_{TAG}_{name}.png", full_page=True)

    desk = b.new_context(viewport={"width": 1366, "height": 900}, device_scale_factor=1)
    pd = desk.new_page()
    pd.goto(URL, wait_until="networkidle", timeout=45000)
    pd.wait_for_timeout(2000)
    dump("DESKTOP 1366", pd.evaluate(PROBE))
    pd.screenshot(path=f"/tmp/desk_{TAG}.png", full_page=True)
    b.close()
    print(json.dumps({"shots": [f"/tmp/mob_{TAG}.png", f"/tmp/mob_{TAG}_top.png",
                                f"/tmp/mob_{TAG}_edit.png", f"/tmp/desk_{TAG}.png"]}))
