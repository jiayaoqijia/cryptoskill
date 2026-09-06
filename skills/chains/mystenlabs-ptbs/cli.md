# Building PTBs from the CLI

How to construct and execute programmable transaction blocks using `sui client ptb` directly from the command line.

Source: https://docs.sui.io/references/cli/client

## Overview

`sui client ptb` lets you compose multi-command transactions from the shell without writing TypeScript. Every operation that can be done with the SDK `Transaction` class can also be done from the CLI.

## Basic syntax

```bash
sui client ptb [OPTIONS] [COMMANDS...]
```

Commands are chained in order. Each command produces results that subsequent commands can reference.

## Common commands

### Transfer SUI

```bash
sui client ptb \
  --split-coins gas "[1000000000]" \
  --assign coin \
  --transfer-objects "[coin]" @0xRECIPIENT_ADDRESS
```

### Transfer an object

```bash
sui client ptb \
  --transfer-objects "[@0xOBJECT_ID]" @0xRECIPIENT_ADDRESS
```

### Merge coins

Instead of `sui client merge-coin`, use `sui client ptb`:

```bash
sui client ptb \
  --merge-coins @0xPRIMARY_COIN_ID "[@0xCOIN_TO_MERGE_ID]"
```

To merge multiple coins:

```bash
sui client ptb \
  --merge-coins @0xPRIMARY_COIN_ID "[@0xCOIN_A, @0xCOIN_B, @0xCOIN_C]"
```

### Split coins

```bash
sui client ptb \
  --split-coins gas "[1000000, 2000000, 3000000]" \
  --assign coins \
  --transfer-objects "[coins.0, coins.1, coins.2]" @0xRECIPIENT
```

### Call a Move function

```bash
sui client ptb \
  --move-call 0xPACKAGE::module::function '<TYPE_ARG>' arg1 arg2
```

With object arguments:

```bash
sui client ptb \
  --move-call 0xPACKAGE::game::mint_sword @0xGAME_OBJECT 100u64
```

### Chaining multiple commands

```bash
sui client ptb \
  --move-call 0xPACKAGE::hero::new \
  --assign hero \
  --move-call 0xPACKAGE::hero::equip_sword hero 42u64 \
  --transfer-objects "[hero]" @0xRECIPIENT
```

## Argument syntax

| Argument type | Syntax | Example |
|---|---|---|
| Object ID | `@0x...` | `@0xabc123` |
| Gas coin | `gas` | `gas` |
| u8/u16/u32/u64/u128/u256 | `<value><type>` | `100u64`, `42u8` |
| bool | `true` / `false` | `true` |
| address | `@0x...` | `@0xabc123` |
| Vector | `"[elem1, elem2]"` | `"[1u64, 2u64, 3u64]"` |
| String | `"hello"` | `"hello"` |
| Assigned result | variable name | `coin`, `hero` |
| Indexed result | `name.N` | `coins.0`, `coins.1` |
| Type argument | `'<type>'` | `'0x2::sui::SUI'` |

## CLI PTB syntax quick-reference

| Syntax | Meaning | Example |
|---|---|---|
| `vector[...]` | Vector literal (not JSON `[...]`) | `vector["a", "b"]` |
| `--assign name` | Bind the previous command's result to `name` | `--move-call ... --assign item` |
| `[name]` | Reference a bound result in an argument | `--transfer-objects "[item]" @0xADDR` |
| `'"my string"'` | String argument (single-quote wrapping double quotes) | `'"Hello, world!"'` |
| `@0x...` | Object reference (object ID) | `@0xabc123` |
| `@0x...` | Address value | `@0x1234` |
| `@sender` | The active CLI address | `--transfer-objects "[coin]" @sender` |

> **Vector syntax pitfall:** the CLI uses `vector["a", "b"]`, not JSON-style `["a", "b"]`. JSON arrays are for homogeneous numeric/object lists inside `--split-coins` and `--merge-coins` arguments; `vector[...]` is the general-purpose Move vector literal.

## Assigning results

Use `--assign` to name the result of the previous command for use in subsequent commands:

```bash
sui client ptb \
  --split-coins gas "[5000000000]" \
  --assign payment \
  --move-call 0xPACKAGE::shop::buy @0xSHOP payment \
  --assign item \
  --transfer-objects "[item]" @0xBUYER
```

## Gas budget

```bash
sui client ptb \
  --gas-budget 100000000 \
  --transfer-objects "[@0xOBJECT]" @0xRECIPIENT
```

If not specified, the CLI will estimate gas automatically.

## Preview mode

Use `--preview` to see the PTB structure without executing:

```bash
sui client ptb \
  --preview \
  --split-coins gas "[1000000000]" \
  --assign coin \
  --transfer-objects "[coin]" @0xRECIPIENT
```

## Dry run

Use `--dry-run` to simulate execution without committing:

```bash
sui client ptb \
  --dry-run \
  --move-call 0xPACKAGE::module::function @0xOBJECT
```

## Common patterns

### Airdrop SUI to multiple addresses

```bash
sui client ptb \
  --split-coins gas "[1000000, 1000000, 1000000]" \
  --assign coins \
  --transfer-objects "[coins.0]" @0xALICE \
  --transfer-objects "[coins.1]" @0xBOB \
  --transfer-objects "[coins.2]" @0xCHARLIE
```

### Calling a function that returns an object

When a Move function returns an object, use `--assign` to bind the result, then `--transfer-objects` to send it to an address:

```bash
sui client ptb \
  --move-call 0xPACKAGE::weapon::forge 100u64 50u64 \
  --assign sword \
  --transfer-objects "[sword]" @sender
```

Without the `--transfer-objects`, the returned object has no owner and the PTB fails with `UnusedValueWithoutDrop`.

### Mint and transfer an NFT

```bash
sui client ptb \
  --move-call 0xPACKAGE::nft::mint "My NFT" "An awesome NFT" "https://example.com/image.png" \
  --assign nft \
  --transfer-objects "[nft]" @0xRECIPIENT
```

## Why `sui client ptb` over legacy helpers

The CLI includes legacy convenience commands like `sui client merge-coin`, `sui client split-coin`, `sui client transfer`, etc. Prefer `sui client ptb` because:

- **Composable:** chain multiple operations in a single atomic transaction.
- **Consistent:** uses the same PTB mental model as the SDK.
- **Powerful:** any combination of commands, not just single-purpose operations.
- **Future-proof:** legacy helpers may be deprecated.
