# Chunked Upload

Optional extension of the SMTP gateway protocol for messages that do not fit one ingress call (~2 MiB). A canister that does not implement it keeps receiving `smtp_request` as before. Oversize mail for it is refused with a permanent error, and the sender gets a normal bounce.

## When the gateway uses it

- The encoded `SmtpRequest` is larger than 2,097,152 bytes, **and** `smtp_capabilities` returned both `upload_protocol_version >= 1` and `max_message_size > 0`. The check fails closed: a missing field, `0`, or no `smtp_capabilities` method at all means single-call delivery only.
- The gateway queries `smtp_capabilities` during `RCPT TO`, concurrently with `smtp_request_validate`, and caches the answer for 10 minutes. A missing method is cached as "no chunked upload".
- When the sender declared the message size up front (`SIZE=` on `MAIL FROM`), an oversize message is refused at `RCPT TO` with `552 5.3.4 Recipient accepts at most <limit> bytes.`, where the limit is your advertised `max_message_size` or 2,097,152 for a canister without chunked upload.
- Too large for a canister without chunked upload: `550 5.5.0 Permanent delivery error: message is too large (<n> bytes encoded, limit is 2097152) and canister <id> does not support chunked upload`.
- The gateway enforces your advertised `max_message_size` only on this path. Enforce it yourself too, with 552.
- By default the gateway accepts at most 1,996,800 bytes per message (header block and body together), so with default settings chunked upload is rarely triggered.

## What the gateway sends

- Every chunk repeats `version`, `message_id`, `envelope`, `total_chunks`, `chunk_size` and `body_size`. `headers` and `gateway_flags` are only on chunk 0. `message_id` is the same per-transaction UUIDv7 as in `smtp_request`.
- `chunk_size` is at most 1 MiB. Headers are never split, and a header block too large to leave 256 KiB of payload in chunk 0 is a permanent failure.
- Up to 2 chunks per canister are in flight at once (16 across all canisters), so chunks arrive **in any order**. A failed chunk is retried up to twice (after 250 ms and 500 ms; after 2 s and 4 s on a 429 or 503).
- `smtp_upload_commit` is sent exactly once. If its reply is lost (timeout or transport error), the gateway makes **one** `smtp_upload_status` query. A committed upload with an `Ok` result counts as delivered, and a committed `Err` is mapped by its class. Anything else is reported as temporary (450), and the sending server retries the whole message later with a new `message_id`.
- `smtp_upload_abort` is fire-and-forget, sent when the gateway gives up on a chunk. Never rely on it: expire uncommitted uploads yourself.
- The whole delivery is bounded by 90 seconds. The gateway never re-sends a commit, so a retained verdict only has to outlive that window. Keep it for a few minutes.

## Obligations

| The canister must | Code if violated |
|---|---|
| Reject a `version` it does not implement, on both chunk and commit | 504 |
| Recompute `SHA256(payload)` and compare it with `payload_sha256` **before** storing the chunk | 554 |
| Check `total_chunks == ceil(body_size / chunk_size)` and `index < total_chunks`, and bound `total_chunks` **before** any allocation or offset arithmetic (`chunk_size = 1` with `total_chunks = 4_000_000_000` is an allocation attack) | 554 |
| Check the payload length: `min(chunk_size, body_size - index * chunk_size)` | 554 |
| Reject a chunk that disagrees with the upload already in progress under the same `message_id`, including a resent index with different bytes | 450 (a collision is worth retrying) |
| Accept an identical resend of a chunk as a no-op | — |
| Keep the upload when a commit arrives before all chunks: the rest may still come | 450 |
| Derive the commit digest from the payloads **it stored**, never from the caller's `payload_sha256` values | 554 on mismatch |
| Make `smtp_upload_commit` idempotent: retain the verdict per `message_id` and return it for a repeated commit and from `smtp_upload_status` | — |
| Return 530 for an unauthorized caller; a trap is retried | 530 |
| Cap concurrent uploads and buffered bytes, and expire uploads that are never committed | 452 |

The commit digest is `body_sha256 = SHA256(d_0 || d_1 || ... || d_{n-1})` with `d_i = SHA256(payload_i)`, in index order: it hashes 32 bytes per chunk, not the body again. It depends on `chunk_size`, so it checks the transfer, not the content: never use it to deduplicate mail. Compute it with the crate's `ic_smtp_gateway_protocol::body_sha256(&digests)` so that both sides use the same construction.

The chunked Candid types, unlike `SmtpRequest`, use required fields on purpose: a malformed chunk fails to decode instead of arriving as an empty record. Counter widths are exact (`index : nat32`; a `nat64` does not decode).

```candid
type SmtpCapabilities = record {
  upload_protocol_version : opt nat32;
  max_message_size : opt nat64;   // header block + body, in bytes
};
type SmtpUploadChunk = record {
  version : nat32;
  message_id : text;
  envelope : Envelope;
  index : nat32;                   // 0-based
  total_chunks : nat32;
  chunk_size : nat64;              // payload length of every chunk but the last
  body_size : nat64;
  payload_sha256 : blob;           // 32 bytes
  payload : blob;
  headers : opt vec Header;        // chunk 0 only
  gateway_flags : opt vec text;    // chunk 0 only
};
type SmtpUploadChunkOk = record { chunks_received : nat32 };
type SmtpUploadChunkResponse = variant { Ok : SmtpUploadChunkOk; Err : SmtpRequestError };
type SmtpUploadCommit = record {
  version : nat32;
  message_id : text;
  body_sha256 : blob;
  total_chunks : nat32;
};
type SmtpUploadId = record { message_id : text };
type SmtpUploadStatus = record { known : bool; committed : bool; result : opt SmtpResponse };
type SmtpUploadStatusResponse = variant { Ok : SmtpUploadStatus; Err : SmtpRequestError };

// service additions
smtp_capabilities : () -> (SmtpCapabilities) query;
smtp_upload_chunk : (SmtpUploadChunk) -> (SmtpUploadChunkResponse);
smtp_upload_commit : (SmtpUploadCommit) -> (SmtpResponse);
smtp_upload_status : (SmtpUploadId) -> (SmtpUploadStatusResponse) query;
smtp_upload_abort : (SmtpUploadId) -> (SmtpResponse);
```

## Implementation

The reference implementation is the mock canister in the protocol repository, which CI builds and tests: [`examples/mock-canister/src/lib.rs`](https://github.com/dfinity/ic-smtp-gateway-protocol/blob/4e376c5c15300d1d14b4dbc51986a322a4a0c3e8/examples/mock-canister/src/lib.rs) in `dfinity/ic-smtp-gateway-protocol`, pinned to commit `4e376c5`. Its `smtp_capabilities` and `smtp_upload_*` methods implement every obligation above. To adapt it:

- Take the types and `body_sha256()` from the `ic-smtp-gateway-protocol` crate, and add `sha2 = "0.11"` for the per-chunk digests.
- `InitArg` and the `mock_*` methods are test scaffolding. Replace them with your own configuration and with the `check_caller` and `check_envelope` from `SKILL.md`. The mock's single `authorized` principal makes caller restriction mandatory, but restriction is optional (`SKILL.md` Pitfall 7).
- Keep upload state keyed by `(caller, message_id)`, as the mock does, so that another principal cannot collide with or probe the gateway's uploads.
- The mock keeps uploads on the heap. An upgrade in the middle of an upload loses it: the commit then gets 450 and the sending server retries the whole message. Buffer chunks in stable memory (`stable-memory` skill) if you handle many large messages.
- `ic_cdk::export_candid!()` resolves method types at the crate root. If the chunked methods live in a submodule, import `SmtpCapabilities`, `SmtpUploadChunk`, `SmtpUploadChunkResponse`, `SmtpUploadCommit`, `SmtpUploadId` and `SmtpUploadStatusResponse` in `lib.rs`, or the build fails with `cannot find type SmtpUploadChunk in this scope`.

## Test it locally

The body `hello world` split into `"hello "` and `"world"` (`chunk_size = 6`, `body_size = 11`) has these digests, written as Candid blob literals. Every number carries its Candid type, so the commands also work against a canister without embedded Candid metadata:

```bash
D0='\5e\32\35\a8\34\6e\5a\45\85\f8\c5\85\62\f5\05\2b\8f\e2\6a\3b\b1\22\e1\e9\6c\76\78\49\64\df\c4\61'      # SHA256("hello ")
D1='\48\6e\a4\62\24\d1\bb\4f\b6\80\f3\4f\7c\9a\d9\6a\8f\24\ec\88\be\73\ea\8e\5a\6c\65\26\0e\9c\b8\a7'      # SHA256("world")
BODY='\66\18\9e\d7\99\1e\1e\0f\ce\06\53\99\c5\ca\05\fc\15\c2\81\86\5a\7a\29\91\bd\d6\67\c1\46\6a\91\a4'  # SHA256(D0 || D1)
ENV='envelope = record { from = record { user = "alice"; domain = "example.com" }; to = vec { record { user = "support"; domain = "example.icp0.io" } } }'

# Expected: the upload_protocol_version and max_message_size you advertise
icp canister call backend smtp_capabilities '()'

# Chunk 1 first: order is not guaranteed. Expected: Ok, chunks_received = 1
icp canister call backend smtp_upload_chunk "(record { version = 1 : nat32; message_id = \"m1\"; $ENV; index = 1 : nat32; total_chunks = 2 : nat32; chunk_size = 6 : nat64; body_size = 11 : nat64; payload_sha256 = blob \"$D1\"; payload = blob \"world\" })"

# Commit too early. Expected: Err 450 "upload is incomplete" (the upload is kept)
icp canister call backend smtp_upload_commit "(record { version = 1 : nat32; message_id = \"m1\"; body_sha256 = blob \"$BODY\"; total_chunks = 2 : nat32 })"

# Chunk 0 carries the headers. Expected: Ok, chunks_received = 2
icp canister call backend smtp_upload_chunk "(record { version = 1 : nat32; message_id = \"m1\"; $ENV; index = 0 : nat32; total_chunks = 2 : nat32; chunk_size = 6 : nat64; body_size = 11 : nat64; payload_sha256 = blob \"$D0\"; payload = blob \"hello \"; headers = opt vec { record { name = \"Subject\"; value = \" Big\\r\\n\" } } })"

# Commit, then commit again. Expected: Ok both times (idempotent)
icp canister call backend smtp_upload_commit "(record { version = 1 : nat32; message_id = \"m1\"; body_sha256 = blob \"$BODY\"; total_chunks = 2 : nat32 })"
icp canister call backend smtp_upload_commit "(record { version = 1 : nat32; message_id = \"m1\"; body_sha256 = blob \"$BODY\"; total_chunks = 2 : nat32 })"

# Expected: known = true; committed = true; result = opt variant { Ok = record {} }
icp canister call backend smtp_upload_status '(record { message_id = "m1" })'

# Allocation attack. Expected: Err 554 "malformed chunk layout", not a trap
icp canister call backend smtp_upload_chunk "(record { version = 1 : nat32; message_id = \"m3\"; $ENV; index = 0 : nat32; total_chunks = 4000000000 : nat32; chunk_size = 1 : nat64; body_size = 4000000000 : nat64; payload_sha256 = blob \"$D0\"; payload = blob \"hello \" })"
```

In zsh, print these variables with `print -r` rather than `echo`: zsh's `echo` interprets the backslashes and corrupts the digests.
