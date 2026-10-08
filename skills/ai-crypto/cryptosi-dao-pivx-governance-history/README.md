# pivx-governance-history

Chain-verifiable reconstruction of PIVX governance history: every passed
and failed proposal, vote data, and actual treasury payout receipts from
superblocks on-chain.

See [SKILL.md](./SKILL.md) for the full method, gotchas, and data-source
notes. Tool: [scripts/pivx_gov_history.py](./scripts/pivx_gov_history.py)
(Python 3 stdlib only).

```bash
python3 scripts/pivx_gov_history.py --help
```

## Verified facts baked into the method

- Pass rule: net-yes ≥ 10% of total masternodes (~190–200 votes at
  ~1,900 MNs) — not simple majority. A 59%-yes proposal can fail.
- `pivx.org/proposals/past` is a server-rendered 1MB table of ~560 rows
  (no JS needed); failing rows use the same `pass-fund` class with a
  `Failing` label and negative `data-order`.
- Superblock spacing is ~33,600 blocks (~24 days) as measured
  Sep 16 → Oct 10 2026, not the stale "43,200 / 30 days" figure.
- Sample payout receipt: block 5,586,823 (2026-09-16) tx
  `c0dea62bfa52590345002ccdf691591a1745bd0b71127a6bd0482147b3146250`
  paid 138,558 + 117,978 PIV.
