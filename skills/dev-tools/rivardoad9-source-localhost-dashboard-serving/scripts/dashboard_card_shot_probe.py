#!/usr/bin/env python3
"""Card-by-card evidence for a served dashboard: element screenshots + legibility + privacy mode.

Companion to mobile_probe.py (overflow) and dashboard_content_probe.py (values). This one answers:
  * does ONE card look right?  -> locator(sel).screenshot() per card (no scroll/viewport cut, no fixed
    bottom-nav overlay confusing the review, unlike a full_page slice)
  * is any label too small?    -> min computed font-size across the label selectors
  * does privacy mode actually hide every dollar figure? -> asserts no /\$[0-9]/ in body.innerText
    AFTER clicking the toggle, and that the state survives a reload (localStorage)

Usage:
  /tmp/pwenv/bin/python dashboard_card_shot_probe.py URL ["sel1,sel2,..."] [--hide '#btnH'] [--tag name]

Example:
  python dashboard_card_shot_probe.py http://127.0.0.1:8787/risk \
     "#ringkasan .card >> nth=1,#onchain .occard >> nth=0,#token .tok >> nth=0" --hide '#btnH'

Prints JSON + three ASSERT lines. Read the saved PNGs with vision_analyze ONE AT A TIME and ask a
targeted question ("any text cut off? are the % and $ columns aligned?").
"""
import glob
import json
import sys

from playwright.sync_api import sync_playwright

CANDS = sorted(glob.glob("/home/ubuntu/.cache/ms-playwright/chromium-*/chrome-linux64/chrome"))
CHROME = CANDS[-1] if CANDS else None  # installed build is often older than the driver expects

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = {a.split("=", 1)[0].lstrip("-"): (a.split("=", 1)[1] if "=" in a else True)
        for a in sys.argv[1:] if a.startswith("--")}
URL = args[0] if args else "http://127.0.0.1:8787/"
SELS = (args[1] if len(args) > 1 else "#ringkasan .card >> nth=0,#onchain .occard >> nth=0").split(",")
HIDE_SEL = opts.get("hide") or None
TAG = opts.get("tag", "card")

LABELS = ".oct .k,.mx .k,.whalerow .k,.tile .k,.chip,.leg .lit,.ni .m"
MONEY_RE = r"/\$\s?[0-9]/"


def main():
    out = {"url": URL, "cards": [], "hide": None, "errors": []}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: out["errors"].append("pageerror: " + str(e)[:200]))
        pg.on("console", lambda m: out["errors"].append(f"{m.type}: {m.text[:160]}")
              if m.type == "error" else None)
        pg.goto(URL, wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(2000)

        # ---- legibility: smallest computed label font on the page
        out["min_label_font_px"] = pg.evaluate(
            """(sel) => {const f=[...document.querySelectorAll(sel)]
                 .map(e=>parseFloat(getComputedStyle(e).fontSize)||99);
               return f.length?Math.min(...f):null;}""", LABELS)

        # ---- card-by-card element screenshots
        for i, sel in enumerate(s.strip() for s in SELS):
            sel = sel.strip()
            if not sel:
                continue
            path = f"/tmp/{TAG}_card{i}.png"
            try:
                n = pg.locator(sel).count()
                if not n:
                    out["cards"].append({"sel": sel, "error": "selector matched 0 elements"})
                    continue
                pg.locator(sel).first.screenshot(path=path)
                out["cards"].append({"sel": sel, "n": n, "shot": path,
                                     "text": pg.locator(sel).first.inner_text()[:220]})
            except Exception as exc:  # noqa: BLE001
                out["cards"].append({"sel": sel, "error": f"{type(exc).__name__}: {str(exc)[:120]}"})

        # ---- privacy mode: toggle, assert nothing leaks, assert persistence
        if HIDE_SEL:
            def leak():
                return pg.evaluate("() => [...new Set(document.body.innerText.match(/\\$[^\\s]*/g)||[])]")

            out["hide"] = {"preset": pg.inner_text(HIDE_SEL), "leftover_before": leak()[:6]}
            pg.click(HIDE_SEL)
            pg.wait_for_timeout(600)
            left = [s for s in leak() if s and s[1:2].isdigit()]      # $1,234 style leaks only
            out["hide"].update({
                "icon_after_click": pg.inner_text(HIDE_SEL),
                "leftover_amounts": left[:10],
                "masks": pg.evaluate("() => (document.body.innerText.match(/\\$\\u2022/g)||[]).length"),
                "ls": pg.evaluate("() => localStorage.getItem('zmz_hide')"),
            })
            pg.screenshot(path=f"/tmp/{TAG}_hide_top.png")
            pg.reload(wait_until="networkidle")
            pg.wait_for_timeout(1800)
            out["hide"]["hidden_after_reload"] = not [s for s in leak() if s and s[1:2].isdigit()]
            pg.locator(HIDE_SEL).click()          # restore for the user's own view
            pg.wait_for_timeout(400)
        b.close()

    print(json.dumps(out, ensure_ascii=False, indent=1))
    f = out.get("min_label_font_px")
    print(f"ASSERT min label font >=10.5px: {'OK' if (f or 0) >= 10.5 else 'FAIL ' + str(f)}")
    if out["hide"]:
        print("ASSERT no $ amount visible when hidden:",
              "OK" if not out["hide"]["leftover_amounts"] else f"FAIL {out['hide']['leftover_amounts']}")
        print("ASSERT hidden state survives reload:",
              "OK" if out["hide"]["hidden_after_reload"] else "FAIL")
    print("ASSERT no js errors:", "OK" if not out["errors"] else f"CHECK {out['errors'][:3]}")
    print("NEXT: vision_analyze each /tmp/%s_card*.png ONE AT A TIME with a targeted question." % TAG)


if __name__ == "__main__":
    main()
