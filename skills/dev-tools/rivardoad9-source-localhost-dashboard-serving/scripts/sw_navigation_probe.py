#!/usr/bin/env python3
"""Service-worker route-hijack probe (detects one page's SW serving its sibling page).

Symptom it catches: every curl/HTTP check returns 200 (server fine, tunnel fine), yet the user's
phone shows the wrong app / a blank page for one route. Cause: a service worker registered by page A
whose fetch handler treats every `req.mode === 'navigate'` as its own and caches responses under a
fixed key, so navigating to page B offline/flaky serves A's document from cache.

Usage:
    python sw_navigation_probe.py <BASE_URL> [SW_PAGE_PATH] [SIBLING_PATH]
    python sw_navigation_probe.py https://foo.trycloudflare.com /risk /

Exit code 0 = clean, 1 = findings printed. Requires the playwright venv described in SKILL.md:
    ~/.hermes/bin/uv venv /tmp/pwenv && ~/.hermes/bin/uv pip install --python /tmp/pwenv/bin/python playwright
    /tmp/pwenv/bin/python sw_navigation_probe.py <BASE_URL>
"""

from __future__ import annotations

import asyncio
import sys

from playwright.async_api import async_playwright

CHROME = "/home/ubuntu/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome"


async def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    base = sys.argv[1].rstrip("/")
    sw_path = (sys.argv[2] if len(sys.argv) > 2 else "/risk") or "/risk"
    sib_path = (sys.argv[3] if len(sys.argv) > 3 else "/") or "/"
    if not sw_path.startswith("/"):
        sw_path = "/" + sw_path
    if not sib_path.startswith("/"):
        sib_path = "/" + sib_path

    findings: list[str] = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        ctx = await browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        console_errors: list[str] = []
        pg.on("pageerror", lambda e: console_errors.append(str(e)[:150]))

        # 1. load the SW-registering page and let the SW take control
        await pg.goto(base + sw_path, wait_until="networkidle", timeout=70000)
        await pg.wait_for_timeout(6000)
        sw_title = (await pg.title()).split("—")[0].split("·")[0].strip()
        controlled = await pg.evaluate("!!navigator.serviceWorker.controller")
        regs = await pg.evaluate(
            "navigator.serviceWorker.getRegistrations().then(r=>r.map(x=>x.active?x.active.scriptURL:null))"
        )
        print(f"SW page {sw_path}: title={sw_title!r} controlled={controlled} regs={regs}")
        if not controlled and regs:
            print("  note: SW registered but not yet controlling this load (reload once) — continuing")

        # 2. click-through: the sibling link must actually navigate (title must change)
        link = await pg.query_selector(f'a[href="{sib_path}"]')
        if link is None:
            findings.append(f"no <a href=\"{sib_path}\"> on {sw_path} — cross-nav missing or JS-built")
        else:
            await link.click()
            await pg.wait_for_load_state("networkidle")
            await pg.wait_for_timeout(4000)
            after = (await pg.title()).split("—")[0].split("·")[0].strip()
            print(f"click {sib_path} -> {pg.url} title={after!r}")
            if sw_title and sw_title in after:
                findings.append(f"click on {sib_path} did not change the document (still {after!r})")

        # 3. hijack test: go back to the SW page, then OFFLINE, then navigate to the sibling
        await pg.goto(base + sw_path, wait_until="networkidle", timeout=70000)
        await pg.wait_for_timeout(4000)
        await ctx.set_offline(True)
        try:
            await pg.goto(base + sib_path, wait_until="load", timeout=15000)
            txt = await pg.inner_text("body")
            if sw_title and sw_title.lower() in txt.lower():
                findings.append(f"HIJACK: {sib_path} served the cached {sw_path} document while offline")
            else:
                print(f"ok: {sib_path} offline did not serve {sw_path}")
        except Exception as exc:  # noqa: BLE001
            print(f"ok: {sib_path} offline failed normally ({str(exc)[:60]}) — not hijacked")
        finally:
            await ctx.set_offline(False)

        if console_errors:
            print("page errors:", console_errors[:3])
        await browser.close()

    if findings:
        print("\nFINDINGS:")
        for f in findings:
            print(" -", f)
        return 1
    print("\nclean: no cross-route hijack detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
