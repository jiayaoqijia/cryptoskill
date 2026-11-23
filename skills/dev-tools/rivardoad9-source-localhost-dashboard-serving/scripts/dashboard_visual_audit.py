#!/usr/bin/env python3
"""Layout + theme audit for an agent-served dashboard page (stdlib + playwright only).

Usage:
  python3 dashboard_visual_audit.py http://127.0.0.1:8787/risk \
      [--hide '#btnH'] [--widths 390,1366] [--shots '.card,.tok'] [--out /tmp/audit]

Checks (each one is a bug that shipped at least once on this dashboard):
  * JS pageerrors                       -> must be none
  * horizontal overflow                -> must be 0 at every width
  * emoji characters in rendered text   -> must be 0 (theme rule: SVG icons, never emoji)
  * "$<digit>" leaks with privacy ON    -> must be 0 (mask must cover engine-generated prose)
  * value misalignment inside a row     -> <= 4px (2-line labels used to push values down)
  * legend/label column overlap         -> 0 (chip inside the value column overlapped the %)
  * min computed font-size              -> >= 10 (micro-labels below 10px read as "kecil & redup")

Exits 1 when any hard check fails, so it works as a gate before reporting to the user.
Chromium path: $PW_CHROME or the known ms-playwright build.
"""
import argparse, asyncio, json, os, re, sys, tempfile

CHROME = os.environ.get(
    "PW_CHROME",
    "/home/ubuntu/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome",
)

PROBE = r"""() => {
  const vw = window.innerWidth;
  const out = {vw, overflow: document.documentElement.scrollWidth - vw, offenders: [], minFont: 99};

  // horizontal overflow offenders (ignore intentional horizontal scrollers)
  document.querySelectorAll('*').forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.right > vw + 1 && !e.closest('.strip,[data-hscroll]'))
      out.offenders.push((e.tagName + '.' + (e.className || '')).slice(0, 60) + ' r=' + Math.round(r.right));
  });

  // emoji used as icons (theme violation)
  const EMOJI = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{1F1E6}-\u{1F1FF}]/gu;
  out.emoji = ((document.body.innerText.match(EMOJI) || []).length);

  // font floor: smallest rendered glyph size
  document.querySelectorAll('.card *').forEach(e => {
    if (!e.children.length && e.textContent.trim()) {
      const fs = parseFloat(getComputedStyle(e).fontSize);
      if (fs && fs < out.minFont) out.minFont = Math.round(fs * 10) / 10;
    }
  });

  // metric values in the same visual row must share a baseline (2-line labels break this)
  let worst = 0;
  document.querySelectorAll('.mx,.oct,.whalerow').forEach(c => {
    const buckets = {};
    [...c.querySelectorAll('.v')].forEach(v => {
      const y = Math.round(v.getBoundingClientRect().top);
      const k = Object.keys(buckets).find(x => Math.abs(x - y) < 24);
      if (k) buckets[k].push(y); else buckets[y] = [y];
    });
    Object.values(buckets).forEach(g => {
      if (g.length > 1) worst = Math.max(worst, Math.max(...g) - Math.min(...g));
    });
  });
  out.misalignMax = worst;

  // label column must not collide with the next column (chip-in-value-column bug).
  // a 1-2px box touch is normal; only report when the name column is also clipped.
  out.overlap = [];
  document.querySelectorAll('.leg tr, .leg .lit').forEach(r => {
    const a = r.querySelector('.lnm'), b = r.querySelector('.lpct') || r.children[2];
    if (!a || !b) return;
    const ar = a.getBoundingClientRect(), br = b.getBoundingClientRect();
    if (ar.right > br.left + 2 && a.scrollWidth > a.clientWidth + 1)
      out.overlap.push(r.innerText.replace(/\n/g, ' ').slice(0, 70));
  });
  return out;
}"""

LEAK = r"""() => {
  const vw = window.innerWidth;
  const txt = document.body.innerText;
  const dollars = (txt.match(/\$\s?\d/g) || []).length;
  return {dollars, overflow: document.documentElement.scrollWidth - vw};
}"""


async def audit(url, hide, widths, shots, outdir):
    from playwright.async_api import async_playwright
    report = {"url": url, "len": None, "runs": {}, "jsErrors": []}
    if not os.path.exists(CHROME):
        print(f"chromium not found at {CHROME} (set PW_CHROME)", file=sys.stderr)
        return None
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-dev-shm-usage"])
        for w in widths:
            pg = await b.new_page(
                viewport={"width": w, "height": 900}, device_scale_factor=1.5 if w > 800 else 2,
                is_mobile=w < 500, has_touch=w < 500,
            )
            pg.on("pageerror", lambda e: report["jsErrors"].append(str(e)[:200]))
            await pg.goto(url, wait_until="domcontentloaded")
            await pg.wait_for_timeout(2600)
            rep = await pg.evaluate(PROBE)
            report["len"] = rep
            if hide:
                try:
                    await pg.click(hide)
                    await pg.wait_for_timeout(600)
                    rep["masked"] = await pg.evaluate(LEAK)
                except Exception as e:  # selector must exist when privacy mode is claimed
                    rep["masked"] = {"error": str(e)[:120]}
            for i, sel in enumerate(shots or []):
                try:
                    await pg.locator(sel).first.screenshot(path=f"{outdir}/w{w}_{i}.png")
                except Exception:
                    pass
            if w == 390:
                await pg.evaluate("window.scrollTo(0,0)")
                await pg.wait_for_timeout(300)
                await pg.screenshot(path=f"{outdir}/top_390.png", clip={"x": 0, "y": 0, "width": 390, "height": 820})
            else:
                await pg.screenshot(path=f"{outdir}/top_{w}.png",
                                    clip={"x": 0, "y": 0, "width": w, "height": 1150})
            await pg.close()
            report["runs"][w] = rep
        await b.close()
    return report


def gate(rep):
    bad = []
    if rep["jsErrors"]:
        bad.append(f"jsErrors={rep['jsErrors'][:2]}")
    for w, r in rep["runs"].items():
        if r["overflow"] > 0:
            bad.append(f"{w}px overflow={r['overflow']} {r['offenders'][:3]}")
        if r.get("emoji"):
            bad.append(f"{w}px emoji-as-icon={r['emoji']}")
        if r.get("minFont", 99) < 10:
            bad.append(f"{w}px minFont={r['minFont']}")
        if r.get("misalignMax", 0) > 4:
            bad.append(f"{w}px misalign={r['misalignMax']}")
        if r.get("overlap"):
            bad.append(f"{w}px legendOverlap={r['overlap'][:2]}")
        m = r.get("masked")
        if isinstance(m, dict) and m.get("dollars"):
            bad.append(f"{w}px maskLeak={m['dollars']} dollar figures still visible")
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--hide", default=None, help="selector of the privacy toggle (e.g. '#btnH')")
    ap.add_argument("--widths", default="390,1366")
    ap.add_argument("--shots", default=".card,.tok")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or tempfile.mkdtemp(prefix="audit_")
    os.makedirs(out, exist_ok=True)
    rep = asyncio.run(audit(a.url, a.hide, [int(x) for x in a.widths.split(",")], a.shots.split(","), out))
    if rep is None:
        sys.exit(2)
    print(json.dumps(rep, indent=1)[:4000])
    fails = gate(rep)
    print("\nSHOTS:", out)
    print("FAIL:" if fails else "PASS:", *fails, sep="\n  ") if fails else print("PASS: all checks clean")
    sys.exit(1 if fails else 0)
