#!/usr/bin/env python3
"""Render satu file markdown jadi PDF A4 lewat Chromium headless.

Pakai: python3 md_to_pdf.py <input.md> [output.pdf]
Path relatif aman: script me-resolve ke absolut sebelum dipakai,
karena Chromium/Path.as_uri() menolak path relatif ('relative paths
can't be expressed as file URIs').
"""
import pathlib
import subprocess
import sys

import markdown

CHROME = pathlib.Path("/home/ubuntu/.hermes/tools/chromium-1208/chrome-linux64/chrome")

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
* { box-sizing: border-box; }
body { font-family: "DejaVu Sans", "Liberation Sans", sans-serif; color:#17181c;
       font-size:10.5pt; line-height:1.55; margin:0; }
h1 { font-size:22pt; line-height:1.15; margin:0 0 4mm 0; letter-spacing:-.4pt; }
h2 { font-size:13pt; margin:8mm 0 2.5mm; padding-bottom:1.5mm;
     border-bottom:1.2pt solid #17181c; page-break-after:avoid; }
h3 { font-size:11pt; margin:5mm 0 1.5mm; page-break-after:avoid; }
p { margin:0 0 2.6mm; }
ul, ol { margin:0 0 3mm 0; padding-left:5.5mm; }
li { margin-bottom:1.4mm; }
table { width:100%; border-collapse:collapse; margin:3mm 0 4mm; font-size:9pt;
        page-break-inside:avoid; }
th { background:#17181c; color:#fff; text-align:left; padding:2mm 2.5mm; font-weight:600; }
td { padding:1.8mm 2.5mm; border-bottom:.6pt solid #ddd; vertical-align:top; }
tr:nth-child(even) td { background:#f7f7f8; }
code { font-family:"DejaVu Sans Mono", monospace; font-size:9pt;
       background:#f1f1f3; padding:.4mm 1.2mm; border-radius:1mm; }
hr { border:0; border-top:.6pt solid #ccc; margin:6mm 0; }
"""


def main() -> int:
    src = pathlib.Path(sys.argv[1]).expanduser().resolve()
    out = (pathlib.Path(sys.argv[2]).expanduser().resolve()
           if len(sys.argv) > 2 else src.with_suffix(".pdf"))
    body = markdown.markdown(src.read_text(encoding="utf-8"),
                             extensions=["extra", "tables", "fenced_code", "sane_lists"])
    html_path = out.with_suffix(".html")
    html_path.write_text(
        f'<!doctype html><html lang="id"><head><meta charset="utf-8">'
        f"<style>{CSS}</style></head><body>{body}</body></html>",
        encoding="utf-8",
    )
    subprocess.run(
        [str(CHROME), "--headless=new", "--no-sandbox", "--disable-gpu",
         "--no-pdf-header-footer", f"--print-to-pdf={out}", html_path.as_uri()],
        check=True, capture_output=True, timeout=180,
    )
    print(f"{out}: {out.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
