---
name: sui-move
description: Sui blockchain and Move smart contract development. Use when the user asks about Sui, Move language, smart contracts, objects, transactions, or blockchain development on Sui.
version: 1.1.0
metadata:
  author: EasonClawdbot1
  tags: sui, move, blockchain, smart-contract, web3
  requires:
    bins: [sui, rg]
  install:
    - id: sui-cli
      kind: brew
      formula: sui
      bins: [sui]
      label: Install Sui CLI (brew)
---

# Sui Move Development

Comprehensive knowledge base for Sui blockchain and Move smart contract development.

**GitHub:** <https://github.com/EasonC13-agent/sui-skills/tree/main/sui-move>

## Setup References

Clone the official documentation:

```bash
# Create skill directory
mkdir -p {baseDir}/references && cd {baseDir}/references

# Clone Move Book (The Move Language Bible)
git clone --depth 1 https://github.com/MystenLabs/move-book.git

# Clone Sui docs (sparse checkout)
git clone --depth 1 --filter=blob:none --sparse https://github.com/MystenLabs/sui.git
cd sui && git sparse-checkout set docs

# Clone Awesome Move (curated examples and resources)
# Note: Some code examples may be outdated
git clone --depth 1 https://github.com/MystenLabs/awesome-move.git
```

## Additional Resources

### Awesome Move (`references/awesome-move/`)
A curated list of Move resources, including:
- Example projects and code snippets
- Libraries and frameworks
- Tools and utilities
- Learning resources

⚠️ **Note**: Some code examples in awesome-move may be outdated as the Move language and Sui platform evolve. Always verify against the latest Move Book and Sui documentation.

## Reference Structure

### Move Book (`references/move-book/book/`)
| Directory | Content |
|-----------|---------|
| `your-first-move/` | Hello World, Hello Sui tutorials |
| `move-basics/` | Variables, functions, structs, abilities, generics |
| `concepts/` | Packages, manifest, addresses, dependencies |
| `storage/` | Object storage, UID, transfer functions |
| `object/` | Object model, ownership, dynamic fields |
| `programmability/` | Events, witness, publisher, display |
| `move-advanced/` | BCS, PTB, cryptography |
| `guides/` | Testing, debugging, upgrades, BCS |
| `appendix/` | Glossary, reserved addresses |

### Sui Docs (`references/sui/docs/content/`)
- Concepts, guides, standards, references

## Quick Search

```bash
# Search Move Book for a topic
rg -i "keyword" {baseDir}/references/move-book/book/ --type md

# Search Sui docs
rg -i "keyword" {baseDir}/references/sui/docs/ --type md

# Find all files about a topic
find {baseDir}/references -name "*.md" | xargs grep -l "topic"
```

## Key Concepts

### Move Language Basics

**Abilities** - Type capabilities:
- `copy` - Can be copied
- `drop` - Can be dropped (destroyed)
- `store` - Can be stored in objects
- `key` - Can be used as a key in global storage (objects)

```move
public struct MyStruct has key, store {
    id: UID,
    value: u64
}
```

**Object Model**:
- Every object has a unique `UID`
- Objects can be owned (address), shared, or immutable
- Transfer functions: `transfer::transfer`, `transfer::share_object`, `transfer::freeze_object`

### Common Patterns

**Create and Transfer Object**:
```move
public fun create(ctx: &mut TxContext) {
    let obj = MyObject {
        id: object::new(ctx),
        value: 0
    };
    transfer::transfer(obj, tx_context::sender(ctx));
}
```

**Shared Object**:
```move
public fun create_shared(ctx: &mut TxContext) {
    let obj = SharedObject {
        id: object::new(ctx),
        counter: 0
    };
    transfer::share_object(obj);
}
```

**Entry Functions**:
```move
public entry fun do_something(obj: &mut MyObject, value: u64) {
    obj.value = value;
}
```

## CLI Commands

```bash
# Create new project
sui move new my_project

# Build
sui move build

# Test
sui move test

# Publish
sui client publish --gas-budget 100000000

# Call function
sui client call --package <PACKAGE_ID> --module <MODULE> --function <FUNCTION> --args <ARGS>

# Get object
sui client object <OBJECT_ID>
```

## Workflow

When answering Sui/Move questions:

1. **Search references first**:
   ```bash
   rg -i "topic" {baseDir}/references/move-book/book/ -l
   ```

2. **Read relevant files**:
   ```bash
   cat {baseDir}/references/move-book/book/<path>/<file>.md
   ```

3. **Provide code examples** from the references

4. **Link to official docs** when helpful:
   - Move Book: https://move-book.com
   - Sui Docs: https://docs.sui.io

## Topics Index

| Topic | Location |
|-------|----------|
| Hello World | `move-book/book/your-first-move/hello-world.md` |
| Hello Sui | `move-book/book/your-first-move/hello-sui.md` |
| Primitives | `move-book/book/move-basics/primitive-types.md` |
| Structs | `move-book/book/move-basics/struct.md` |
| Abilities | `move-book/book/move-basics/abilities-introduction.md` |
| Generics | `move-book/book/move-basics/generics.md` |
| Object Model | `move-book/book/object/` |
| Storage | `move-book/book/storage/` |
| Events | `move-book/book/programmability/events.md` |
| Testing | `move-book/book/guides/testing.md` |
| Upgrades | `move-book/book/guides/upgradeability.md` |
| PTB | `move-book/book/move-advanced/ptb/` |
| BCS | `move-book/book/move-advanced/bcs.md` |

## Related Skills

This skill is part of the Sui development skill suite:

| Skill | Description |
|-------|-------------|
| [sui-decompile](https://clawhub.ai/EasonC13/sui-decompile) | Fetch and read on-chain contract source code |
| **sui-move** | Write and deploy Move smart contracts |
| [sui-coverage](https://clawhub.ai/EasonC13/sui-coverage) | Analyze test coverage with security analysis |
| [sui-agent-wallet](https://clawhub.ai/EasonC13/sui-agent-wallet) | Build and test DApps frontend |

**Workflow:**
```
sui-decompile → sui-move → sui-coverage → sui-agent-wallet
    Study        Write      Test & Audit   Build DApps
```

All skills: <https://github.com/EasonC13-agent/sui-skills>

## Notes

- Move 2024 edition introduces new features (enums, method syntax, etc.)
- Sui uses a unique object-centric model different from other blockchains
- Gas is paid in SUI tokens
- Testnet/Devnet available for development
