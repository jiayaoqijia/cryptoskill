#!/usr/bin/env python3
"""Report how empty each PDF page is at the bottom.

A table or figure that jumps to the next page leaves a large hole above it.
Chars-per-page does not catch that; the distance from the last body block to
the bottom margin does.

Usage:
    python pdf_page_fill.py file.pdf [--margin-cm 2.5] [--threshold-cm 3]

Prints one line per flagged page plus a JSON summary on the last line.
"""
import argparse
import json
import sys

import pymupdf


def page_gaps(path, margin_cm=2.5, footer_skip_pt=40.0):
    doc = pymupdf.open(path)
    margin_pt = margin_cm / 2.54 * 72.0
    rows = []
    for i, page in enumerate(doc):
        blocks = [b for b in page.get_text("blocks")
                  if b[3] < page.rect.height - footer_skip_pt]
        if not blocks:
            rows.append({"page": i + 1, "gap_cm": None,
                         "landscape": page.rect.width > page.rect.height})
            continue
        bottom = max(b[3] for b in blocks)
        gap = (page.rect.height - margin_pt - bottom) / 28.35
        rows.append({"page": i + 1, "gap_cm": round(gap, 1),
                     "landscape": page.rect.width > page.rect.height})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--margin-cm", type=float, default=2.5)
    ap.add_argument("--threshold-cm", type=float, default=3.0)
    args = ap.parse_args()

    rows = page_gaps(args.pdf, args.margin_cm)
    flagged = []
    for r in rows:
        if r["gap_cm"] is None:
            continue
        if r["gap_cm"] > args.threshold_cm:
            flagged.append(r)
            shape = "landscape" if r["landscape"] else "portrait"
            print(f"page {r['page']:>3} ({shape}): gap {r['gap_cm']} cm")
    if not flagged:
        print("no page exceeds the gap threshold")
    print(json.dumps({"pages": len(rows), "flagged": flagged,
                      "threshold_cm": args.threshold_cm}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
