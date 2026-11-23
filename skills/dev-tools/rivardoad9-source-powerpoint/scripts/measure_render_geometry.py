#!/usr/bin/env python3
"""Measure content geometry of a rendered slide PNG, in inches.

Vision models hallucinate layout defects ("ghost text", "uneven widths") and
miss real 4 px overlaps. Measure first; redesign only when the numbers agree.

Usage:
  python measure_render_geometry.py render/s05.png --band 2.1 5.3
  python measure_render_geometry.py render/s07.png            # whole page

--band takes inches from the top of the slide. Output: one line per vertical
content run (each phone, box, or text block) with left edge, width and gap.
"""
import argparse
import json
import sys

import numpy as np
from PIL import Image


def runs(mask, min_count=5, join=2):
    cols = mask.sum(axis=0)
    out, start = [], None
    for x, v in enumerate(cols):
        on = v > min_count
        if on and start is None:
            start = x
        elif not on and start is not None:
            out.append((start, x))
            start = None
    if start is not None:
        out.append((start, len(cols)))
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] <= join:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("png")
    ap.add_argument("--band", nargs=2, type=float, metavar=("Y0", "Y1"),
                    help="vertical band in inches from the top")
    ap.add_argument("--width", type=float, default=13.333, help="slide width in inches")
    ap.add_argument("--height", type=float, default=7.5, help="slide height in inches")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    im = Image.open(args.png).convert("L")
    px_per_in = im.width / args.width
    y0, y1 = args.band if args.band else (0, im.height / px_per_in)
    top = max(0, int(y0 * px_per_in))
    bottom = min(im.height, int(y1 * px_per_in))
    if bottom <= top:
        sys.exit("empty band")

    band = np.array(im.crop((0, top, im.width, bottom))).astype(int)
    found = runs(band < 245)

    items, prev_end = [], None
    for a, b in found:
        gap = None if prev_end is None else (a - prev_end) / px_per_in
        items.append({
            "left": round(a / px_per_in, 3),
            "right": round(b / px_per_in, 3),
            "width": round((b - a) / px_per_in, 3),
            "gap_before": None if gap is None else round(gap, 3),
        })
        prev_end = b

    if args.json:
        print(json.dumps({"band": [y0, y1], "runs": items}, indent=1))
        return

    print(f"{args.png}  band {y0}-{y1} in  ({len(items)} runs)")
    for i, it in enumerate(items):
        gap = "—" if it["gap_before"] is None else f"{it['gap_before']:.2f}"
        print(f"  {i:02d}  left {it['left']:5.2f}  width {it['width']:5.2f}  gap {gap:>5}")
    if items:
        widths = [round(i["width"], 2) for i in items]
        gaps = [round(i["gap_before"], 2) for i in items if i["gap_before"] is not None]
        if len(set(widths)) > 1:
            print(f"  widths vary: {sorted(set(widths))}")
        if len(set(gaps)) > 1:
            print(f"  gaps vary:   {sorted(set(gaps))}")
        print(f"  margins: left {items[0]['left']:.2f} in, right {args.width - items[-1]['right']:.2f} in")


if __name__ == "__main__":
    main()
