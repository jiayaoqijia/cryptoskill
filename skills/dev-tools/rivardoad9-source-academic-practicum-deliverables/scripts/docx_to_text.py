#!/usr/bin/env python3
"""Ekstrak teks + tabel dari file .docx tanpa dependency (stdlib saja).

Dipakai kalau `read_file` gagal di dokumen ("document extraction failed") atau kalau
tabel modul perlu dibaca per baris (rubrik penilaian, tabel bobot, daftar tugas).

Pakai:
    python3 docx_to_text.py modul.docx              # print teks + tabel
    python3 docx_to_text.py modul.docx --no-tables  # hanya paragraf

Cara kerja: .docx = ZIP berisi word/document.xml. Parsing pakai xml.etree.
"""
import sys
import xml.etree.ElementTree as ET
import zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _text_of(elem):
    return "".join(t.text or "" for t in elem.iter(f"{W}t"))


def para_text(root):
    out = []
    for p in root.iter(f"{W}p"):
        line = _text_of(p).strip()
        if line:
            out.append(line)
    return out


def table_texts(root):
    """Kembalikan list tabel; tiap tabel = list baris; tiap baris = list sel."""
    tables = []
    for tbl in root.iter(f"{W}tbl"):
        rows = []
        for tr in tbl.findall(f"{W}tr"):
            cells = [_text_of(tc).strip() for tc in tr.findall(f"{W}tc")]
            if any(cells):
                rows.append(cells)
        if rows:
            tables.append(rows)
    return tables


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    path = sys.argv[1]
    show_tables = "--no-tables" not in sys.argv

    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))

    print(f"### {path}")
    print("entri:", [n for n in z.namelist() if n.startswith("word/")][:12])
    paras = para_text(root)
    print(f"\n=== {len(paras)} paragraf ===")
    print("\n".join(paras))

    if show_tables:
        tables = table_texts(root)
        print(f"\n=== {len(tables)} tabel ===")
        for i, t in enumerate(tables, 1):
            print(f"\n-- tabel {i} ({len(t)} baris)")
            for row in t:
                print("   | " + " | ".join(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
