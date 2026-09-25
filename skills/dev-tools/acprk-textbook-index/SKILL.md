---
name: textbook-index
description: Build and query a table-of-contents index of math and crypto textbooks to answer "which book and chapter proves X?". Use when a proof needs a standard lemma, when idea mining needs an external mathematical structure, or when adding books to references/textbooks.
---

# textbook-index

## Build / extend the index

```bash
python3 skills/textbook-index/scripts/extract_toc.py <book-or-dir> ... \
        --out-dir references/textbooks/toc --summary /tmp/toc.json [--max-level 2]
python3 skills/textbook-index/scripts/extract_toc.py --selftest
```

- PDF with bookmarks → `bm` (pages = physical PDF pages).
- No usable bookmarks → parses the printed "Contents" pages (`txt`, printed page numbers); rejects OCR garbage
  using a dictionary hit-rate check (needs `/usr/share/dict/words`; otherwise accepts with a warning).
- Scanned (no text layer), DjVu without `djvused`, or noisy OCR → stub; fill a chapter-level TOC from the
  publisher's public page and label it `TOC from public source`.
- Output contains only bibliographic data + TOC; never commit PDFs or body text. Then add a row to
  `references/textbooks/CATALOG.md` and, if it fills a gap, to `TOPIC-MAP.md`.

## Query ("which book/chapter proves X?")

1. `TOPIC-MAP.md` row for the topic → first look / second opinion.
2. `grep -ril "<term>" references/textbooks/toc/` for terms the map lacks; beware homonyms
   (Frobenius *norm* vs Frobenius *automorphism* vs Frobenius *group*; "character" of a group vs of a field;
   "lattice" of subgroups vs Euclidean lattice; "trace" of a matrix vs field trace).
3. Open your own copy at the section; copy the exact statement, and **check each hypothesis against your
   setting** (characteristic, ring vs field, finite vs infinite group, prime vs prime power modulus, Galois vs
   non-Galois extension). Most mis-citations fail here, not at the conclusion.
4. Record in `MATH-REFS.md`:
   `| id | statement we use | source (book, section, printed page) | hypotheses checked? | used in |`.
5. If the statement is load-bearing, hand it to `theorist` for a Sage/Lean check.

## Ignition pattern for idea mining

"Book B chapter C + concrete bottleneck step S": ask what structure in C acts on the objects of S
(a group action, a grading, a decomposition, a norm, an extremal bound). This pairing, not "give me ideas",
is what produces candidate free parameters for `idea-mining-loop`.
