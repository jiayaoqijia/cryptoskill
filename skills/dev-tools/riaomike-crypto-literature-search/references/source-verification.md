# Source and Citation Verification

Use this reference before citing a work as verified or using it to support a technical claim.

## 1. Keep three statuses separate

| Layer | Question |
|---|---|
| Bibliographic identity | Does this title/author/year/identifier record refer to a real work? |
| Version identity | Which ePrint/preprint/conference/journal/revision was inspected? |
| Claim support | Does that exact version support the specific nearby claim? |

Passing one layer never implies the next.

## 2. Identity record

Record when available:

- normalized title and complete author list;
- publication state/type and venue;
- stable identifier: DOI, IACR ePrint, arXiv, proceedings/publisher record, or repository identifier;
- publication/revision dates;
- authoritative landing page and inspected document location;
- access date and verification status.

Do not autocomplete missing fields from memory or a plausible citation pattern.

## 3. Version graph

Represent relations explicitly:

```text
work
├── early preprint/ePrint
├── revised preprint/ePrint
├── conference/proceedings version
└── journal/extended/corrected version
```

For each version record identifier, date, inspected status, and material differences in claims, definitions, theorem numbering, assumptions, parameters, experiments, or corrections.

## 4. Claim-support check

For every extracted claim:

1. open the exact version;
2. locate the statement, proof, definition, result, table, or measurement;
3. inspect surrounding hypotheses, caveats, model, parameter regime, and negations;
4. distinguish author assertion from a proved or measured result;
5. record page/section/theorem/table/paragraph location appropriate to the version;
6. quote minimally and verify exact wording if a quotation is necessary.

Titles, abstracts, snippets, citation counts, and generated summaries support discovery, not detailed theorem/security claims.

## 5. Conflicts and inaccessible sources

- Preserve conflicting metadata and identify authoritative records consulted.
- If theorem numbering or conclusions differ, cite the exact supporting version.
- If full text is inaccessible, mark content/claim support unverified while retaining bibliographic discovery status.
- If only a secondary citation is available, record it as secondary evidence and search for the primary source.
- If a source is withdrawn, corrected, or superseded, make that status prominent.

## 6. Verification status vocabulary

- **identity verified:** bibliographic record reconciled.
- **version inspected:** exact document opened.
- **claim verified:** exact source location supports the recorded claim within stated limits.
- **supported with limitations:** caveat/model/parameter restriction materially limits the claim.
- **unverified:** required source/version/content unavailable or unresolved.
- **contradicted:** inspected evidence conflicts with the recorded claim.

