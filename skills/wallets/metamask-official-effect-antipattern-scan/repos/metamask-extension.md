---
repo: metamask-extension
parent: effect-antipattern-scan
---

## Paths

- Component sources: [`ui/`](https://github.com/MetaMask/metamask-extension/tree/main/ui)
- Shared hooks: [`ui/hooks/`](https://github.com/MetaMask/metamask-extension/tree/main/ui/hooks)

## Commands

```bash
# Pattern 1: JSON.stringify in deps
grep -rnE 'useEffect\([^)]*\[.*JSON\.stringify' ui/ --include="*.ts" --include="*.tsx"

# Pattern 3: setInterval / setTimeout
grep -rnE 'setInterval|setTimeout' ui/ --include="*.ts" --include="*.tsx"

# Pattern 4: fetch inside useEffect (manual review required for context)
grep -rn 'fetch(' ui/ --include="*.ts" --include="*.tsx"
```

## Reference Docs

- [Frontend Performance Optimization Guidelines](https://github.com/MetaMask/contributor-docs/pull/159) (contributor-docs PR #159)
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
