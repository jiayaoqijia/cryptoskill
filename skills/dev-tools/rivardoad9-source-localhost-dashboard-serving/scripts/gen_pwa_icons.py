#!/usr/bin/env python3
"""Generate 192/512 PWA icons by rendering an inline SVG in headless chromium.

Why not PIL: PIL is not installed on this host and PEP 668 blocks a casual pip install.
Headless chromium is already on the box for layout probes, so reuse it.

Usage:
    python3 gen_pwa_icons.py [OUTDIR] [--exe /path/to/chrome] [--label SHIELD]

Writes OUTDIR/icon-192.png and OUTDIR/icon-512.png (RGBA, transparent outside the rounded square).
The icon is pure SVG shapes on purpose: emoji glyphs render as tofu in headless chromium.

Playwright driver (once, throwaway venv):
    ~/.hermes/bin/uv venv /tmp/pwenv && ~/.hermes/bin/uv pip install --python /tmp/pwenv/bin/python playwright
"""
import argparse
import asyncio
import os
import sys

EXE_DEFAULT = "/home/ubuntu/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome"

# viewBox is fixed at 512; only width/height and the corner radius change per size.
TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;background:transparent}}</style></head><body>
<svg width="{S}" height="{S}" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#12203a"/><stop offset="1" stop-color="#070b14"/>
    </linearGradient>
    <linearGradient id="sh" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#5aa9ff"/><stop offset="1" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="{R}" fill="url(#bg)"/>
  <g transform="translate(256,266)">
    <path d="M0,-152 L120,-101 C120,22 71,113 0,152 C-71,113 -120,22 -120,-101 Z"
          fill="none" stroke="url(#sh)" stroke-width="20" stroke-linejoin="round"/>
    <circle r="60" fill="none" stroke="#1a2740" stroke-width="17"/>
    <circle r="60" fill="none" stroke="#ffc857" stroke-width="17" stroke-linecap="round"
            stroke-dasharray="226 377" transform="rotate(-90)"/>
    <circle cx="60" cy="0" r="9" fill="#ffc857"/>
  </g>
</svg></body></html>"""

SIZES = [(512, 112), (192, 42)]  # (px, corner radius)


async def run(outdir: str, exe: str) -> int:
    from playwright.async_api import async_playwright  # imported late for a clear error
    ok = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"], executable_path=exe)
        for size, rad in SIZES:
            out = os.path.join(outdir, f"icon-{size}.png")
            pg = await b.new_page(viewport={"width": size, "height": size}, device_scale_factor=1)
            await pg.set_content(TPL.format(S=size, R=rad))
            await pg.wait_for_timeout(180)
            await pg.screenshot(path=out, omit_background=True)
            await pg.close()
            print("wrote", out)
            ok += 1
        await b.close()
    return 0 if ok == len(SIZES) else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir", nargs="?", default=".", help="where to write icon-192/512.png")
    ap.add_argument("--exe", default=os.environ.get("PW_CHROME", EXE_DEFAULT),
                    help="chromium binary (playwright build under ~/.cache/ms-playwright)")
    ap.add_argument("--label", default="", help="unused placeholder for a future text variant")
    a = ap.parse_args()
    if not os.path.exists(a.exe):
        print(f"chromium not found: {a.exe}\nset --exe or PW_CHROME, or install a playwright build",
              file=sys.stderr)
        return 2
    os.makedirs(a.outdir, exist_ok=True)
    return asyncio.run(run(a.outdir, a.exe))


if __name__ == "__main__":
    raise SystemExit(main())
