# Public Acton/Tolk example corpus

Use this file when porting a FunC project and you need an idiomatic Acton/Tolk reference implementation with an upstream FunC baseline.

Primary corpus:

- Acton/Tolk examples: `https://github.com/ton-blockchain/acton-contracts`
- Acton docs: `https://ton-blockchain.github.io/acton/`
- Tolk idioms: `https://docs.ton.org/languages/tolk/idioms-conventions`

## How to use the corpus

For a target FunC project:

1. Pick the closest `acton-contracts` suite by domain and message pattern.
2. Read that suite's README to confirm the original FunC source link.
3. Compare the original FunC source against the Acton/Tolk version for TL-B layout, opcode policy, storage shape, bounce behavior, send modes, getters, and tests.
4. Use the Tolk suite's structure as the style target, not as a source to copy blindly.

Prefer searching by opcode hex, message type name, storage field name, getter name, or error code. For multi-contract systems, compare the contract graph and wrappers too.

## Suite mapping

- `config`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/config`
  - Original FunC: `https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/config-with-ownable-params.fc`
  - Study for governance proposal flow, voting, validator-set/ticktock behavior, config dictionaries, and custom parameter parsing.

- `elector`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/elector`
  - Original FunC: `https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/elector-code.fc`
  - Study for validator election lifecycle, stake accounting, complaint handling, ticktock, and benchmarked happy paths.

- `dns`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/dns`
  - Original FunC: `https://github.com/ton-blockchain/dns-contract`
  - Related specs: `https://github.com/ton-blockchain/TEPs/blob/master/text/0081-dns-standard.md`, `https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md`, `https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md`
  - Study for DNS record maps, NFT-style collection/item ownership, auction flow, and explicit initialized/uninitialized item state.

- `w5`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/w5`
  - Original FunC: `https://github.com/ton-blockchain/wallet-contract-v5`
  - Study for signed external messages, extension actions, C5 action validation, internal execution, get methods, and replay-sensitive storage.

- `highload-v3`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/highload-v3`
  - Original FunC: `https://github.com/ton-blockchain/highload-wallet-contract-v3`
  - Study for batched dispatch, replay bitmaps, timeout cleanup, outbound raw message validation, and strict shape checks before forwarding.

- `multisig-v2`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/multisig-v2`
  - Original FunC: `https://github.com/ton-blockchain/multisig-contract-v2`
  - Study for multisig/order contract coordination, seqno modes, action execution, fee-aware lifecycle logic, and helper-level unit tests.

- `nft`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/nft`
  - Original FunC: `https://github.com/ton-blockchain/nft-contract`
  - Related specs: `https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md`, `https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md`, `https://github.com/ton-blockchain/TEPs/blob/master/text/0066-nft-royalty-standard.md`
  - Study for collection/item split, transfer payloads, royalty data, metadata content, and initialized-vs-uninitialized item storage.

- `jetton-v2`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/jetton-v2`
  - Original FunC: `https://github.com/ton-blockchain/jetton-contract/tree/jetton-2.0`
  - Minter FunC: `https://github.com/ton-blockchain/jetton-contract/blob/jetton-2.0/contracts/jetton-minter.fc`
  - Wallet FunC: `https://github.com/ton-blockchain/jetton-contract/blob/jetton-2.0/contracts/jetton-wallet.fc`
  - Related specs: `https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md`, `https://github.com/ton-blockchain/TEPs/blob/master/text/0089-jetton-wallet-discovery.md`, `https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md`
  - Study for minter/wallet protocols, bounce restore, sharding helpers, fee management, metadata, admin handoff, and protocol validation tests.

- `notcoin`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/notcoin`
  - Original FunC: `https://github.com/OpenBuilders/notcoin-contract`
  - Study for a production jetton variant with admin/governance behavior, bounce handling, gas profiling, and wallet behavior tests.

- `counter`
  - Acton/Tolk: `https://github.com/ton-blockchain/acton-contracts/tree/master/counter`
  - Original FunC: none
  - Study only for minimal Acton package mechanics, wrappers, tests, and scripts.

## Common target layout

Most production suites use:

- `contracts/errors.tolk` for error constants
- `contracts/messages.tolk` for TL-B message structs, opcode tags, and union types
- `contracts/storage.tolk` for persistent structs and `load/save` helpers
- `contracts/*-contract.tolk` for entrypoints, getters, and core behavior
- `tests/*.test.tolk` for native Acton tests
- `tests/wrappers/*.tolk` or generated wrappers for deployment, sends, and getters
- `scripts/*.tolk` for deploy, info, and operational flows

## Search targets

- Opcodes: search for the hex value in both FunC and Tolk.
- Message schemas: search for `op::` in FunC and `struct (` or `type Allowed` in Tolk.
- Storage: search for `load_data`, `save_data`, `get_data`, and matching fields in `storage.tolk`.
- Dictionaries: search for `udict_` in FunC and typed `map<...>` aliases or helpers in Tolk.
- Outgoing messages: search for `send_raw_message` in FunC and `createMessage` or `.send(SEND_MODE_...)` in Tolk.
- Tests: compare original JS/TS Sandbox flows with native Tolk tests and benchmark snapshots where present.
