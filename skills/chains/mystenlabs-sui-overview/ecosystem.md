# The Sui Stack and Ecosystem

The Sui Stack is the full set of native primitives and infrastructure that Sui provides for building apps. Beyond the core blockchain, the stack includes specialized components that handle common application needs without leaving the ecosystem. These are native primitives, not third-party add-ons.

---

## Sui Stack Primitives

### Randomness

Onchain verifiable random number generation, built into the Sui framework. Use `sui::random::Random` (shared object at `0x8`) to generate unpredictable, unbiasable random values inside Move functions. The randomness is produced by the validator set using a distributed key generation (DKG) protocol, so no single validator can predict or manipulate the output.

**When to use:** Lotteries, raffles, randomized game mechanics (loot drops, critical hits), fair selection algorithms, random NFT trait assignment.

**Key points:**
- Access via `random::new_generator(random, ctx)` in a Move function that takes `&Random`
- Generates random u8/u16/u32/u64/u128/u256, bytes, and values within ranges
- Functions using randomness must be `entry` only (not `public`) to prevent test-and-abort attacks
- Cannot be used in `public` functions — this is enforced by the framework

### zkLogin

Zero-knowledge proof authentication that lets users sign Sui transactions using OAuth credentials (Google, Apple, Facebook, Twitch, etc.) without exposing their Web2 identity onchain. The user's Sui address is derived from their OAuth provider and subject identifier, but the link between the two is hidden by a zero-knowledge proof.

**When to use:** Consumer-facing apps where onboarding friction must be minimal, gasless experiences, any app where users should not need to manage seed phrases or browser extensions.

**Key points:**
- User authenticates with an OAuth provider and receives a JWT
- A ZK proof is generated (client-side or via a proving service) that the JWT is valid without revealing the JWT contents
- The resulting Sui address is deterministic for a given provider + user pair
- Combines with sponsored transactions for fully gasless onboarding
- Users can recover their account through the same OAuth provider

### Walrus

Decentralized blob storage for files and media that do not belong directly onchain. Walrus uses erasure coding to split files into slivers distributed across storage nodes, providing redundancy and availability without full replication. An availability certificate is stored on Sui, linking the blob to the on-chain object that references it.

**When to use:** NFT images/media, game assets, documents, any file over Sui's 256 KB object size limit, user-generated content, frontend hosting via Walrus Sites.

**Key points:**
- Store blob IDs on-chain in Move structs (e.g., `walrus_blob_id: u256`); store the actual file on Walrus
- Blobs have a lifecycle measured in Walrus epochs (not Sui epochs); they can be permanent or deletable
- Access via the `@mysten/walrus` TypeScript SDK extension or the Walrus CLI
- Walrus Sites allow hosting full frontends (HTML/CSS/JS) on Walrus, served via a gateway
- Cost is proportional to blob size and storage duration
- Sui objects hold metadata and references; Walrus holds the bytes

### Nautilus

Secure offchain computation with onchain verification. Nautilus runs code in a Trusted Execution Environment (TEE) and produces an attestation that the computation was performed correctly. The attestation can be verified on-chain, enabling use cases where sensitive data must be processed off-chain but results need on-chain trust guarantees.

**When to use:** Private data processing (e.g., credit scoring without exposing financial data), oracle data feeds with integrity proofs, AI/ML model inference with verifiable results, any computation too expensive or too sensitive for on-chain execution.

**Key points:**
- Code runs inside a TEE (hardware-isolated enclave)
- Produces a cryptographic attestation that the specific code ran on the specific inputs
- The attestation is verified on-chain in a Move function
- Enables "trust but verify" patterns where off-chain services prove correctness

### DeepBook

A fully on-chain central limit order book (CLOB) for trading, built as a shared Move object. DeepBook provides the matching engine, order book management, and settlement layer for building exchanges, AMMs with limit orders, and any app that needs on-chain price discovery.

**When to use:** DEX / exchange interfaces, limit orders, on-chain price discovery, any trading application that needs order matching.

**Key points:**
- Orders are placed and matched entirely on-chain
- Supports limit orders, market orders, and fill-or-kill
- Each trading pair is a shared `Pool` object
- Integrates with PTBs — you can place an order, swap, and transfer in a single transaction
- Provides real-time on-chain price feeds that other contracts can read

### Kiosk

A decentralized commerce and digital asset management standard. Kiosk provides a framework for listing, purchasing, and transferring digital assets with creator-defined transfer policies. Creators can enforce royalties, restrict transfers to approved buyers, or require specific conditions before an asset can change hands.

**When to use:** NFT marketplaces, in-game item shops, any asset trading where creators need to enforce transfer rules (royalties, allowlists, escrow).

**Key points:**
- Each user has their own `Kiosk` object that holds their listed assets
- `TransferPolicy<T>` defines the rules for transferring a given asset type (set by the creator)
- Policies can enforce royalties, allowlists, lock periods, or custom conditions via policy rules
- Assets in a Kiosk can be listed, delisted, borrowed (for display), or exclusively listed
- Works with Object Display for rendering assets in UIs
- The `kiosk` module is part of the Sui framework

### Seal

Decentralized access control and encryption for on-chain data. Seal lets you encrypt data so that only addresses or objects meeting specific on-chain conditions can decrypt it. Access policies are defined in Move smart contracts, and decryption keys are distributed by a threshold network of key servers that verify the on-chain policy before releasing key shares.

**When to use:** Token-gated content, private messaging, NFTs with hidden content (reveal-on-purchase), subscription paywalls, DAO-gated documents, any use case where on-chain conditions should control who can read off-chain data.

**Key points:**
- Encrypt data client-side using a policy-derived key; store the ciphertext on Walrus or any storage layer
- Define access policies in Move (e.g., "must own an NFT of type T", "must hold ≥ 100 tokens", "must be a DAO member")
- Key servers verify the caller meets the policy before releasing threshold key shares for decryption
- No single key server can decrypt alone — threshold cryptography ensures decentralization
- Policies are composable: combine ownership checks, time locks, and custom conditions
- Works with Walrus for storing encrypted blobs and with zkLogin for identity-based policies

### Time Primitives

Sui provides two mechanisms for time-based logic:

- **Clock object (`0x6`):** A shared system object providing the current network timestamp in milliseconds. More precise than epoch timestamps. Pass it to Move functions as `&Clock`. Because the Clock is a shared object, accessing it forces the transaction through consensus, making it incompatible with single-owner fastpath transactions. The Clock updates approximately every 1/4 second at the checkpoint rate.
- **`ctx.epoch()` / `ctx.epoch_timestamp_ms()`:** Returns the current epoch number and epoch start timestamp. Less precise but does not require an additional object parameter and keeps the transaction on the fastpath when only owned objects are involved.

**When to use:** Auctions, deadlines, vesting schedules, time-locked releases, cooldown periods.

---

## Use cases Sui enables

Sui's object-centric model, parallel execution, and native primitives make it well suited for:

- **DeFi:** DeepBook provides on-chain order books. PTBs enable complex multi-step financial operations atomically. Kiosk supports asset trading with royalty enforcement. Seal enables private order flow and encrypted trade data.
- **Gaming:** Sub-second finality and parallel execution support real-time game state. On-chain randomness enables provably fair mechanics. Objects naturally represent game items with ownership and transferability. Walrus stores game assets. Nautilus enables server-side game logic with verifiable results.
- **NFTs and digital assets:** Objects are the native representation of unique digital items. Kiosk provides a commerce layer with creator-controlled transfer policies. Walrus stores associated media. Object Display is the standard for rendering NFT metadata (name, description, image URL, and custom fields) in wallets and explorers — define a `Display<T>` template once and all objects of that type render consistently across the ecosystem. Seal enables hidden content revealed on purchase.
- **Identity and authentication:** zkLogin removes the need for users to manage private keys directly, lowering the onboarding barrier. Addresses are pseudonymous by default. Seal can gate access based on on-chain identity attributes.
- **Social and content platforms:** Walrus handles media storage at scale. Objects represent posts, profiles, and social graphs. Parallel execution supports high-throughput social feeds. Seal enables private messaging and subscriber-only content.
- **Supply chain and real-world assets:** Object versioning provides an auditable history. Immutable objects serve as tamper-proof records. Shared objects enable multi-party workflows. Nautilus enables off-chain data verification with on-chain trust.

---

## How components work together

The Sui development workflow connects these components in layers:

1. **Write smart contracts in Move.** Define your objects, their abilities, and the functions that create and modify them. Use `init` for one-time setup. Move's resource safety guarantees correctness at compile time.
2. **Publish packages to the network.** The Sui CLI compiles and deploys your Move code, returning a package ID and an `UpgradeCap`. Use PTBs to restrict upgrade policies at publish time.
3. **Interact through transactions.** Call published functions, passing objects as inputs. Use programmable transaction blocks to compose multiple operations atomically. Split and merge coins, transfer objects, and call multiple functions in a single transaction.
4. **Build frontends with dApp Kit.** Connect wallets, construct PTBs, and display on-chain state using React hooks and components. Use sponsored transactions and zkLogin for gasless onboarding.
5. **Extend with Sui Stack primitives.** Add randomness for fair mechanics, zkLogin for frictionless auth, Walrus for file storage, Seal for access-controlled content, DeepBook for trading, Kiosk for commerce, or Nautilus for verified off-chain computation — as your use case requires.

Each layer builds on the one before it. Move provides the on-chain logic. Transactions execute that logic. The CLI and SDKs provide developer and programmatic access. dApp Kit connects end users. The Sui Stack primitives add specialized capabilities without leaving the ecosystem.

---

## Choosing the right primitive

| Need | Primitive | Why |
|------|-----------|-----|
| Fair random outcomes | Randomness | Unbiasable, validator-set-backed RNG |
| Passwordless user onboarding | zkLogin | OAuth login → Sui address, no seed phrase |
| Storing files > 256 KB | Walrus | Decentralized blob storage with on-chain references |
| Private/gated content | Seal | On-chain policy controls who can decrypt |
| Off-chain computation with trust | Nautilus | TEE execution + on-chain attestation verification |
| Trading / order matching | DeepBook | Native on-chain CLOB |
| Asset commerce with creator rules | Kiosk | Transfer policies, royalties, allowlists |
| Time-sensitive logic | Clock (`0x6`) | Millisecond network timestamp |
| Epoch-level checks | `ctx.epoch()` | Epoch number, staking windows |
