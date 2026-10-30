# Evidence Package

Use a small artifact directory per run. Do not commit it unless the repo workflow asks for checked-in evidence.

Recommended files:

- `recipe.json`: exact root recipe document used for the run.
- `recipe-resolution.json`: root/dependency digests and static call edges.
- `resolved-recipes/<digest>.recipe.json`: exact dependency documents named by the resolution graph.
- `summary.json`: run status, counts, timing, harness/runner provenance, and recipe-library metadata.
- `trace.json`: ordered node events with timestamps, status, intent, proof links, and linked artifacts.
- `artifact-manifest.json`: reviewer-facing artifact index.

Runner-generated recipe provenance, summary, trace, and screenshots are registered automatically. Use `index_artifacts` only for extra recipe-authored files. Follow the artifact directory printed by `mm-harness run` and keep that complete package; stdout alone is not recipe evidence.

`artifact-manifest.json` shape:

```json
{
  "version": 1,
  "runStatus": "pass",
  "artifacts": [
    {
      "path": "screenshots/send-valid-amount.png",
      "type": "screenshot",
      "label": "Valid amount screen after error clears",
      "nodeId": "capture",
      "proofTarget": "PT-2",
      "mimeType": "image/png"
    }
  ]
}
```

Useful artifact types:

- `screenshot`
- `video`
- `log`
- `trace`
- `summary`
- `json`
- `report`
- `metric`
- `diff`
- `recipe`

Evidence rules:

- Store relative paths in the manifest.
- Link each artifact to a node and proof target.
- Capture screenshots only after a settle condition.
- Prefer logs/reports for backend claims and screenshots/videos for visible UI claims.
- For "no error in logs" claims, include the log path, baseline offset/time, end offset/time, searched strings, and a proof that the watched window was live, such as a benign marker or nonzero appended bytes.
- Redact SRPs, private keys, bearer tokens, production account data, and private user data.
