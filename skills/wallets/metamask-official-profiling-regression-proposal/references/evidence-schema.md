# Evidence schema

The caller provides a single JSON object. Field names may evolve, but the
security boundary does not: only values present in this object may appear as
facts in the proposal.

```json
{
  "runId": "123",
  "runUrl": "https://github.com/example/actions/runs/123",
  "currentSha": "abc",
  "previousRunId": "122",
  "previousSha": "def",
  "findings": [
    {
      "scenario": "Perps add funds",
      "owner": "team-name",
      "jsWorkMs": 12600,
      "baselineMedianJsWorkMs": 3000,
      "ratio": 4.2,
      "baselineRuns": 3
    }
  ],
  "frames": [
    {
      "scenario": "Perps add funds",
      "name": "usePerpsOrderForm",
      "url": "app/example.ts",
      "line": 40,
      "selfMs": 800
    }
  ],
  "pullsOverlappingTheProfile": [
    {
      "number": 123,
      "title": "Example",
      "url": "https://github.com/example/pull/123",
      "files": [
        {
          "path": "app/example.ts",
          "patch": "+changed line"
        }
      ]
    }
  ],
  "pullsMergedWithNoProfileFile": [
    {
      "number": 124,
      "title": "Unrelated",
      "url": "https://github.com/example/pull/124"
    }
  ]
}
```

`pullsOverlappingTheProfile` is computed by deterministic tooling before model
invocation. The model must not promote entries from
`pullsMergedWithNoProfileFile` based on titles or prior knowledge.
