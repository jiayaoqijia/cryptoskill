# Jira report template (markdown mirror of canvas)

Post as a comment on the ticket after ANALYZE (proposed) or IMPLEMENT (final).
Also create a Cursor canvas with the same numbers when useful.

```markdown
## Test layer placement report — <TICKET>

**Mode:** Analyze | Implement
**Scope:** <folders / components>
**PR:** <url or number>
**Verdict:** Improved | Improved with gaps | Needs follow-up | Plan ready (analyze)

### App / production code
- **Changed?** Yes / No / Proposed only
- **Files:** …
- **Why:** (required if Yes — e.g. extract pure feedback helper so toast matrix stays unit-owned without shallow screen mocks)

### Inventory (what was in place)
| Module | Unit | CV | Integration | E2E |
| --- | --- | --- | --- | --- |
| … | … | … | … | … |

### Volume
| Layer | Before | After / Proposed | Δ |
| --- | ---: | ---: | ---: |
| Shallow unit `it`s |  |  |  |
| CV `it`s |  |  |  |
| Pure unit `it`s (helpers) |  |  |  |
| Integration `it`s |  |  |  |
| E2E cases |  |  |  |

**Ratio (overlap passes):** unit removed / CV added ≈ …

### Disposition
| Scenario | Decision | Target layer / file | Note |
| --- | --- | --- | --- |
| … | KEEP / ADD / MIGRATE / DELETE / EXTRACT+UNIT / GAP | … | … |

For any **ADD E2E** row, Note (or extra columns) **must** include: why CV insufficient / why integration insufficient / required device-native boundary. If those cannot be filled, do not ADD E2E.

### Residual risks
| Risk | Status |
| --- | --- |
| … | Closed / Accepted / Open |

### Tasks
Mirror the PR checklist (done vs proposed).

### How to re-run
Follow mobile-testing `references/placement.md`. Overlap sub-pass: `placement/unit-cv-overlap.md` / personal `test-layer-overlap-audit`.
Canvas path: `~/.cursor/projects/<workspace>/canvases/<ticket>-test-layer-placement.canvas.tsx`
```

## Canvas checklist

- Stats: adds/migrates/deletes per layer
- Before/after volumes
- Disposition table
- Callout if any production code changed or proposed (why)
