#!/usr/bin/env python3
"""Tap every bottom-nav button in a real browser and PROVE each one works.

Why: an inline page-level `function scrollTo(id){...}` shadows window.scrollTo, so nav
clicks become silent no-ops -- no JS error, tap lands on the button, nothing moves.
"pageerror is empty" is NOT proof the wiring works; you have to exercise the click.

Usage:
  /tmp/pwenv/bin/python nav_tap_probe.py [url] [data-go-id ...]
  # url defaults to http://127.0.0.1:8787/risk; ids default to whatever the page declares
  # e.g. nav_tap_probe.py http://127.0.0.1:8787/risk ringkasan onchain news token

Pass criteria: every section top lands within a few px of the first one (i.e. the nav
scrolls each section to the same spot under the sticky header), the active tab matches
the tapped id, window.scrollTo is not shadowed, and there are no page errors.

Playwright chromium already exists on this host at the path below (no `chromium` on PATH).
"""
import asyncio
import sys

from playwright.async_api import async_playwright

EXE = "/home/ubuntu/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome"


async def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8787/risk"
    ids = sys.argv[2:]
    errs = []
    problems = []

    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=EXE,
                                    args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = await b.new_context(viewport={"width": 390, "height": 844},
                                  device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(url, wait_until="domcontentloaded")
        await pg.wait_for_timeout(2600)

        shadowed = await pg.evaluate("String(window.scrollTo).includes('getElementById')")
        print("window.scrollTo shadowed by page JS:", shadowed, "(must be False)")
        if shadowed:
            problems.append("window.scrollTo is shadowed by a page function -> nav taps no-op")

        if not ids:
            ids = await pg.evaluate(
                "[...document.querySelectorAll('.nav button')].map(b => b.dataset.go)")

        landings = []
        for i, sid in enumerate(ids, start=1):
            await pg.tap(f".nav button:nth-child({i})")
            await pg.wait_for_timeout(1100)
            r = await pg.evaluate(
                """(sid) => {const el = document.getElementById(sid);
                   const on = document.querySelector('.nav button.on');
                   return {top: el ? Math.round(el.getBoundingClientRect().top) : null,
                           on: on ? on.textContent.trim() : null,
                           y: Math.round(window.scrollY)};}""", sid)
            landings.append(r["top"])
            ref = next((x for x in landings if x is not None), None)
            ok = r["top"] is not None and ref is not None and abs(r["top"] - ref) <= 8
            print(f"tap {sid:10s} -> section top {str(r['top']):>5}px  active={r['on']!r}  "
                  f"scrollY={r['y']:>6}  {'OK' if ok else 'MISMATCH'}")
            if not ok:
                problems.append(f"tap {sid}: section did not land at the same offset ({r['top']})")
            if r["on"] and sid.lower() not in r["on"].lower().replace("-", ""):
                problems.append(f"tap {sid}: active tab is {r['on']!r}")

        # observer must follow a manual scroll once the programmatic one has settled
        last = ids[-1]
        await pg.evaluate("document.getElementById(arguments[0]).scrollIntoView()", last)
        await pg.wait_for_timeout(1300)
        on = await pg.evaluate("(document.querySelector('.nav button.on')||{}).textContent")
        print("after manual scroll to last section, active tab:", (on or "").strip())

        print("JS errors:", errs[:3] or "none")
        if errs:
            problems.append(f"page errors: {errs[:3]}")
        await b.close()

    print("RESULT:", "PASS" if not problems else "FAIL")
    for x in problems:
        print(" -", x)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
