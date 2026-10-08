---
name: verify-on-chain-svg-render-parity
description: Use when an NFT renders an SVG or media blob inside the contract. Decodes tokenURI, validates the SVG, and compares the on-chain render against the reference art for escaping and layout bugs.
---

# Verify on-chain SVG render parity

An on-chain SVG must render identically across the browsers and wallets that consume it; gas-optimized encoders routinely emit invalid or visually wrong output that only shows on some viewers.

## Procedure

1. Pull the token URI and decode the embedded image:

   ```
   cast call $NFT "tokenURI(uint256)(string)" $ID --rpc-url $RPC \
     | jq -r '.image' | sed 's#^data:image/svg+xml;base64,##' | base64 -d > out.svg
   ```

2. Validate it parses as XML/SVG:

   ```
   xmllint --noout out.svg
   ```

   A stray unescaped `&` or `<` in a trait name fails here.

3. Render it to a raster and look at it:

   ```
   rsvg-convert -w 512 out.svg -o out.png
   ```

4. Compare against the reference image for the same id to catch a decoding divergence:

   ```
   python3 -c "from PIL import Image,ImageChops; a=Image.open('out.png'); b=Image.open('ref.png').resize(a.size); print(ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox())"
   ```

5. Confirm every dynamic value is properly escaped. Base64-encoding the whole payload avoids escaping entirely; a raw `data:image/svg+xml,` URI does not.

6. Test an extreme token (longest name, largest id) for fixed-width clipping:

   ```
   cast call $NFT "tokenURI(uint256)(string)" 9999 --rpc-url $RPC | jq -r '.image' | sed 's#.*base64,##' | base64 -d | xmllint --noout -
   ```

7. Confirm no font or image is referenced by external URL; an on-chain SVG must use generic families or embedded glyphs.

## Pitfalls

- Non-ASCII trait names in a raw SVG data URI break rendering; base64 the whole payload.
- A typo between `urn:image/svg+xml` and `data:image/svg+xml` yields blank output that still parses as text.
- Percentage viewBoxes (`0 0 100% 100%`) render differently across engines; use fixed integer units.
- Decimal coordinates from Solidity fixed-point math produce per-viewer sub-pixel shifts.
- Some wallets strip `<style>` blocks, so inline presentation attributes are safer than CSS classes.

## Verification

    xmllint --noout out.svg && rsvg-convert -w 256 out.svg -o out.png && file out.png

Pass: `xmllint` exits 0, the PNG is non-blank, and the diff bbox against the reference is empty or explainable. Report the id tested, the viewer used, and any escaping or layout fix applied.
