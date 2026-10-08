---
name: validate-erc721-metadata-schema
description: Use when a tokenURI returns JSON that marketplaces must parse. Validates the ERC-721 metadata shape so tokens do not render as "no metadata".
---

# Validate ERC-721 metadata JSON

A marketplace expects a specific JSON shape; a missing `image`, a non-string `name`, or `attributes` in the wrong form silently renders the token as "no metadata".

## Procedure

1. Fetch metadata for a sample of ids directly from `tokenURI`:

   ```
   for i in 1 2 42 9999; do uri=$(cast call $NFT "tokenURI(uint256)(string)" $i --rpc-url $RPC | tr -d '"'); \
     if [[ $uri == ipfs://* ]]; then curl -sL "https://ipfs.io/ipfs/${uri#ipfs://}" -o "m$i.json"; else curl -sL "$uri" -o "m$i.json"; fi; done
   ```

2. Confirm the required fields are present and are strings:

   ```
   for f in m*.json; do jq -e '.name|type=="string"' "$f" >/dev/null && jq -e '.image|type=="string"' "$f" >/dev/null || echo "bad $f"; done
   ```

3. Confirm `attributes` is an array of objects with `trait_type` and `value`:

   ```
   jq -e '.attributes|type=="array" and all(.[]; has("trait_type") and has("value"))' m1.json
   ```

4. Check optional fields are well typed: `animation_url` a string, `background_color` six hex digits without `#`, `external_url` absolute.

5. Verify image data URIs use a valid prefix:

   ```
   jq -r '.image' m1.json | grep -qE '^(data:image/[a-z+]+;base64,|ipfs://|ar://|https://)' || echo "bad image prefix"
   ```

6. Reject any field that is `null` where a string is expected; parsers treat null as absent.

7. Run a strict schema validator over the sample:

   ```
   npx ajv-cli validate -s erc721-metadata.schema.json -d 'm*.json'
   ```

## Pitfalls

- `attributes` as an object keyed by trait name works in some viewers but violates the standard.
- A `tokenId` that is a string in one file and a number in the next breaks strict parsers.
- `background_color` with a leading `#` fails the spec, which wants only the six hex digits.
- Enormous inline `data:` images exceed some marketplace size limits and are dropped even though valid.
- A gateway serving the wrong `Content-Type` breaks some consumers; the contract's `data:` form avoids this.

## Verification

    npx ajv-cli validate -s erc721-metadata.schema.json -d 'm*.json'

Pass: every sampled file validates, has string `name` and `image`, and a well-formed `attributes` array. Report the ids checked, any field that failed, and whether the images use a durable scheme.
