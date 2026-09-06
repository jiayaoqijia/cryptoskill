# Walrus — off-chain blob storage

Source: https://docs.wal.app

Walrus is the decentralized storage protocol built on Sui for files too big to live on-chain. When a user asks how to store an image, audio, video, large JSON, ML model, or any arbitrary blob "on Sui" — the answer is **Walrus**, with an on-chain reference to the blob ID.

## Why not store files on-chain

- **250 KB max object size.** Move objects are capped; no single object can hold a megabyte file.
- **Storage fund economics.** Every on-chain byte pays into the storage fund, which distributes yield to validators to cover ongoing storage. It's designed for small, long-lived structured data, not file storage.
- **Read performance.** Full nodes aren't CDNs. Large reads would punish gRPC latency and rate-limit budgets.
- **Redundancy model.** Sui's validator set replicates every byte of state. Storing a video on every validator is wasteful.

Walrus is designed to fill this gap: erasure-coded storage across a distributed network, with on-chain availability certificates.

## Architecture at a glance

From the Walrus docs:

> Metadata is the only blob element ever exposed to Sui or its validators, as the content of blobs is always stored off-chain on Walrus storage nodes and caches.

> After uploading blob data off-chain, availability is certified on Sui:
> 1. Upload blob slivers to storage nodes off-chain.
> 2. Storage nodes provide an availability certificate.
> 3. Upload the certificate on-chain.

So the on-chain state is small (certificate + blob ID + metadata). The blob itself is off-chain, erasure-coded, and retrievable from storage nodes.

## Typical integration

A Move object (NFT, profile, marketplace listing, etc.) stores the **blob ID** and possibly metadata (MIME type, size). The frontend fetches the blob from Walrus using the ID.

```move
public struct NFT has key, store {
  id: UID,
  name: String,
  walrus_blob_id: String,   // reference to Walrus
  mime_type: String,
}
```

### Option 1: Walrus HTTP API (simpler, no extra dependency)

For basic upload/download, use the Walrus publisher and aggregator HTTP endpoints directly. This avoids adding the `@mysten/walrus` package.

**Testnet endpoints:**
- Publisher: `https://publisher.walrus-testnet.walrus.space`
- Aggregator: `https://aggregator.walrus-testnet.walrus.space`

```ts
// Upload a blob
const response = await fetch('https://publisher.walrus-testnet.walrus.space/v1/blobs', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/octet-stream' },
  body: fileBytes,  // ArrayBuffer or Blob
});
const result = await response.json();
// Response shape varies: check result.newlyCreated?.blobObject?.blobId
// or result.alreadyCertified?.blobId
const blobId = result.newlyCreated?.blobObject?.blobId
  ?? result.alreadyCertified?.blobId;

// Download a blob
const data = await fetch(
  `https://aggregator.walrus-testnet.walrus.space/v1/blobs/${blobId}`
).then(r => r.arrayBuffer());
```

### Option 2: `@mysten/walrus` SDK extension

```ts
// TypeScript — via the @mysten/walrus extension
import { SuiGrpcClient } from '@mysten/sui/grpc';
import { walrus } from '@mysten/walrus';

const client = new SuiGrpcClient({
  network: 'mainnet',
  baseUrl: 'https://fullnode.mainnet.sui.io:443',
}).$extend(walrus({ /* config */ }));

// Upload (write blob + commit on-chain certificate)
const { blobId } = await client.walrus.writeBlob({
  blob: fileBytes,
  deletable: false,      // permanent vs re-claimable
  epochs: 200,           // storage duration in epochs
});

// Read
const bytes = await client.walrus.readBlob({ blobId });
```

(Exact API names track the `@mysten/walrus` package version — consult `node_modules/@mysten/walrus/docs/llms-index.md` if installed. See the `sui-sdks` skill's `llm-docs.md`.)

## Blob lifecycle

- **Stored for a configurable duration** (in epochs). Expires if not renewed.
- **Deletable vs permanent.** Deletable blobs can be reclaimed; permanent blobs are locked for their full duration.
- **Availability certificate** on Sui proves the blob was uploaded and stored correctly by enough storage nodes.
- **Renewal** extends the storage duration without re-uploading.

## What goes on-chain

| Thing | Sui | Walrus |
|---|---|---|
| Ownership record | ✅ on-chain |  |
| Structured metadata (name, description, traits) | ✅ on-chain (under 250 KB) |  |
| Blob ID / Walrus reference | ✅ on-chain (small string) |  |
| Image / audio / video / large JSON |  | ✅ on Walrus |
| Availability certificate | ✅ on-chain (proof) |  |

## Cost model

- **Sui write**: storage fund contribution for the small on-chain object holding the blob reference.
- **Walrus write**: payment for N epochs of blob storage, paid in WAL tokens.
- **Reads**: free at the protocol level from storage nodes; actual cost depends on the client you use to fetch.

## Use cases

- **NFT media** — images, animations, audio.
- **Profile data** — large avatars, bios, off-chain attestations.
- **Gaming** — maps, skins, saved states too large for a Move object.
- **App state** — large JSON blobs that exceed the 250 KB cap.
- **Data availability** — rollup-style or oracle data that needs verifiable availability without on-chain bytes.

## Not for

- **Highly-interactive structured state** — if Move needs to read and reason about the data, it has to fit in an object. Walrus blobs are opaque bytes from Move's perspective.
- **Tiny metadata.** A 1 KB string belongs in a Move object. Walrus has per-blob overhead.

## Wiring Walrus blob IDs into Object Display

Store the blob ID in a struct field, then use the Walrus aggregator URL in the Display template to make wallets and explorers render the image directly:

```move
use sui::display_registry;

public struct NFT has key, store {
    id: UID,
    name: String,
    walrus_blob_id: String,
}

fun init(otw: MY_NFT, ctx: &mut TxContext) {
    let publisher = package::claim(otw, ctx);

    let (mut d, cap) = display_registry::new_with_publisher<NFT>(
        &mut display_registry::borrow_mut(),
        &mut publisher,
        ctx,
    );
    display_registry::set(&mut d, &cap,
        b"name".to_string(), b"{name}".to_string());
    display_registry::set(&mut d, &cap,
        b"image_url".to_string(),
        b"https://aggregator.walrus-testnet.walrus.space/v1/blobs/{walrus_blob_id}".to_string());
    display_registry::share(d);

    transfer::public_transfer(cap, ctx.sender());
    transfer::public_transfer(publisher, ctx.sender());
}
```

The `{walrus_blob_id}` placeholder is replaced at display time with the object's field value, producing a full aggregator URL that wallets fetch directly.

For mainnet, use the mainnet aggregator URL. The aggregator endpoint is read-only and free — no authentication or WAL tokens needed for reads.

The end-to-end flow:
1. Upload media to Walrus (HTTP API or `@mysten/walrus` SDK) → get `blobId`
2. Mint the NFT with `walrus_blob_id` set to the returned `blobId`
3. Display template resolves `{walrus_blob_id}` → aggregator serves the image

## Common mistakes

- **"Put the image in the NFT."** NFTs should hold the *blob ID*, not the image bytes. Images go to Walrus; the Move object references them.
- **Using a centralized CDN for "decentralized" apps.** Walrus is the decentralized equivalent. Using S3 / IPFS gateway / Pinata undermines the decentralization story.
- **Forgetting to renew blobs.** Blobs expire. If your app's NFTs reference blobs past their storage duration, the references break. Set renewal logic or use permanent blobs with long durations.
- **Conflating Walrus with IPFS.** IPFS is content-addressed but has no built-in economic guarantee of persistence. Walrus pairs content-addressing with paid storage + availability proofs on Sui.
- **Assuming Walrus replaces Sui.** Walrus is *additive*: Sui for logic/ownership/reference, Walrus for bytes.
