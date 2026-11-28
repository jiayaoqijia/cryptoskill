# Contract Decoding

> **Prerequisite:** Read the [main skill](../SKILL.md) for authentication, global flags, and key concepts.

Submit smart contracts so Dune decodes their events and calls into tables, and track the submissions.

Before submitting:

- Check the contract is not decoded yet: `dune dataset search-by-contract --contract-address <addr>`.
- Get the exact chain name from `dune dataset blockchains`.
- Have the ABI. For a proxy, submit the **implementation's** ABI and set `--proxy`.

---

## contract submit

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--blockchain` | `string` | Yes | -- | e.g. `ethereum`, `base` |
| `--address` | `string` | Yes | -- | 0x-prefixed for EVM chains |
| `--project` | `string` | Yes | -- | Namespace for the tables, e.g. `uniswap`; case-sensitive |
| `--contract-name` | `string` | Yes | -- | Used in table names, e.g. `UniswapToken`; case-sensitive |
| `--abi` | `string` | Yes for new | -- | ABI JSON array, `@path`, or `@-` |
| `--proxy` | `bool` | No | `false` | The address is a proxy; the ABI is the implementation's |
| `--multiple-instances` | `bool` | No | `false` | Several deployed instances share the ABI |
| `--factory` | `bool` | No | `false` | Instances are created by a factory |
| `--manual-abi` | `bool` | No | `false` | The ABI was written or edited by hand |
| `--type` | `string` | No | `new` | `new`, `upgrade`, `rename`, `delete`, or `other` |
| `--reason` | `string` | No | -- | Required for `delete` and `other` |
| `--old-project` | `string` | No | -- | Current project; required for `rename` |
| `--old-contract-name` | `string` | No | -- | Current name; required for `rename` |
| `--idempotency-key` | `string` | No | -- | Makes a retry return the existing submission |
| `--batch` | `string` | No | -- | JSON array of up to 100 submissions instead of the single-contract flags |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

```bash
dune contract submit --blockchain ethereum --address 0x1f98...F984 --project uniswap --contract-name UniswapToken --abi @uni.abi.json -o json
```

Reuse the same `--project` and `--contract-name` when submitting the same contract on more chains. Free plans can submit new contracts for one blockchain per call; upgrades, renames, deletions, and other requests need a paid plan and go to manual review.

---

## contract submissions

List the user's submissions, newest first, including ones made on dune.com.

| Flag | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `--status` | `string` | No | -- | pending, approved, processed, needs_manual_review, rejected, in_progress, cancelled |
| `--blockchain` | `string` | No | -- | Filter by chain |
| `--address` | `string` | No | -- | Filter by address |
| `--project` | `string` | No | -- | Filter by project; case-sensitive |
| `--contract-name` | `string` | No | -- | Filter by contract name; case-sensitive |
| `--limit` | `int` | No | `50` | Maximum results (1-250) |
| `--cursor` | `string` | No | -- | Next cursor from the previous page |
| `-o, --output` | `string` | No | `text` | Output format: `text` or `json` |

`processed` means the decoded tables exist. Decoding takes minutes and manual review can take days: check back later instead of polling.

> [!CAUTION]
> `contract submit` is a **write** command. Confirm the contract, chain, and names with the user first.
