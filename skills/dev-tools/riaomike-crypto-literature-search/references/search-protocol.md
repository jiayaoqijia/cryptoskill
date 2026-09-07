# Search Protocol

Use this protocol for discovery, screening, citation chaining, and stopping. Source verification is a separate stage.

## 1. Freeze the question and boundaries

Record:

- target deliverable and audience;
- claim/contribution being searched;
- publication date/language/type boundaries;
- domain, security/model, assumption, parameter, and implementation boundaries;
- available indexes/repositories/full-text access;
- time/result budget and update cutoff.

## 2. Decompose the search concept

Represent the target across independent dimensions:

```text
primitive/problem
+ property or security notion
+ model/setup/adversary
+ assumption/family
+ construction/proof technique
+ parameter regime
+ functionality or efficiency claim
```

Search dimensions separately before requiring the full conjunction. Build synonyms from:

- current and historical terminology;
- acronyms and expanded names;
- notation/problem variants;
- stronger/weaker security notions and neighboring models;
- ring/module/unstructured lattice variants;
- protocol-family, proof-technique, and implementation terms;
- spelling, hyphenation, and author-supplied keywords.

## 3. Use a layered discovery strategy

When available, cover complementary source classes:

1. field-specific preprint/ePrint repositories;
2. broad scholarly indexes and metadata registries;
3. publisher/proceedings/journal records;
4. author/project/institution records for version discovery;
5. backward and forward citation graphs;
6. surveys, standards, theses, and review articles as discovery maps;
7. patents or non-English sources only when the user includes them.

Secondary sources may expand terminology and citations but do not replace primary claim verification.

## 4. Run high-recall then high-precision searches

### High recall

- combine one or two dimensions per query;
- search titles, abstracts, keywords, full text, and citation neighborhoods when available;
- preserve borderline results until full-text screening;
- log every exact query and filter.

### High precision

- add formal notion/model/assumption qualifiers;
- search exact phrases, theorem terminology, construction names, authors, and citations from closest works;
- search known predecessor/successor terminology and negative results.

Do not report a query as run when it was only proposed.

## 5. Screen and deduplicate

Define inclusion/exclusion criteria before full-text conclusions. Apply stages:

1. discovery record;
2. title/abstract screening;
3. full-text eligibility;
4. identity/version verification;
5. claim extraction/verification;
6. closest-work inclusion.

Deduplicate by work/version graph, not title similarity alone. Preserve material changes in assumptions, theorem statements, parameters, experiments, and citations.

## 6. Expand through citation and author/venue chaining

For each closest work, when capabilities permit:

- inspect references for predecessors;
- inspect citing works for corrections, improvements, and competing claims;
- search key authors, construction names, and recurring venues;
- add new synonyms and rerun affected query families;
- inspect errata, withdrawn/revised versions, and negative/corrective work.

## 7. Stop under a documented rule

Possible stopping rules:

- predefined source/query coverage completed;
- two successive expansion rounds add no material closest work;
- result/time budget reached;
- update search reaches the prior search date;
- evidence gap requires user-provided access or a new scope decision.

Record the rule, final frontier, and unsearched sources. Saturation within the chosen corpus is not global exhaustiveness.

## 8. Synthesize without erasing uncertainty

Separate:

- discovered but unscreened;
- screened/excluded with reason;
- identity verified;
- exact version inspected;
- claim supported;
- contradictory/corrective evidence;
- inaccessible/unverified.

The final corpus size alone says nothing about coverage quality; report the search design and blind spots.

