# Section Order — CCS, IEEE S&P, NDSS

The body order a security-venue paper is expected to have. This is the default, not a
straitjacket: a deviation is allowed when it is recorded with a reason, because a reviewer
reads an unrecorded deviation as an accident. Page budgets, templates, ethics and
AI-disclosure rules are read from the venue's own current call; this file does not carry them.

## Default body order

1. Introduction — problem, gap, mechanism at a glance; contributions as a bullet list
   (a standalone "Contributions" subsection is acceptable; a "Roadmap" subsection is not);
   the technical overview may be 1.1.
2. Preliminaries — notation, definitions, the primitive imported from prior work.
3. Threat model — standalone: parties and trust assumptions, adversary capabilities,
   security goals and explicit non-goals, stated once, in prose. If it is embedded in the
   system overview, record the reason in the revision notes.
4. Design / construction.
5. Security analysis.
6. (optional) Auxiliary construction or a second primitive.
7. Applications and evaluation — the applications the evaluation instantiates as
   subsections, then the measurements, then threats to validity.
8. Related work.
9. Discussion, limitations, and conclusion — limitations as prose grouped by theme, then a
   short conclusion. A standalone numbered "Open Problems" section is a workshop form, not
   a conference form; an "open directions" paragraph inside this section is fine.
10. Appendix — proofs and extra measurements only.

## Structure conformance check (record before freeze)

Run it and record the result in the revision notes; a failure is fixed or recorded as a
human decision, never silently waived.

- main-section count and order: target 8–10 sections, and every section present keeps the
  relative order above;
- banned forms: a "Roadmap" subsection; a standalone numbered "Open Problems" section; a
  central result named "Claim" instead of Theorem/Proposition; bare work-plan labels
  (`A1`, `G1`, `E1`, `U1`, `C3`) in running prose — assumptions must live in an
  `assumption` environment and be cited as "Assumption N";
- threat-model placement: standalone, or embedded with a recorded reason;
- no meta-narrative ("This section will discuss ...", "The rest of the paper is organized
  as follows ...") outside the single roadmap sentence allowed in the introduction.
