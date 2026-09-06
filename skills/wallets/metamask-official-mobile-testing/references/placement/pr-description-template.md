# PR description template (always update)

Create or update the PR body on every run (ANALYZE and IMPLEMENT). Describe every task.

```markdown
## Summary
<1–3 lines: ticket + scope + mode (analyze plan vs implemented)>

Jira: <TICKET-URL>
Report: <link to Jira comment or “see ticket comment”>

## Test layer placement

**Scope:** <paths>
**Mode:** Analyze (proposed) | Implement (applied)

### Inventory
- Unit: …
- CV: …
- Integration: …
- E2E: …

### Tasks
- [ ] <ADD CV: Component — scenario>
- [ ] <MIGRATE unit→CV: Component — scenario>
- [ ] <DELETE shallow unit: Component — scenario (covered by CV)>
- [ ] <KEEP / add pure unit: helper — scenario>
- [ ] <EXTRACT+UNIT: extract \`foo\` + unit matrix>  <!-- only if needed -->
- [ ] <ADD integration: …>  <!-- if applicable -->
- [ ] <E2E: document gap / no change / add>  <!-- if applicable -->
- [ ] Post final Jira report + canvas
- [ ] Re-run unit/CV (integration) for touched files

### App code
- None | Pure extract only: \`path\` — why

### Residual / follow-ups
- [ ] …

## Test plan
- [ ] \`yarn jest …\` (touched unit files)
- [ ] \`yarn jest -c jest.config.view.js …\` (touched CV)
- [ ] Integration command if touched
- [ ] Confirm no intentional product UX change
```

### Agent rules

- ANALYZE: leave all placement tasks unchecked; title/body may say “plan”.
- IMPLEMENT: check completed items; leave residuals unchecked.
- Prefer editing the existing PR linked from the ticket; create a draft PR if the user expects one and none exists.
- Do not commit spike-only markdown dumps into the mobile repo.
