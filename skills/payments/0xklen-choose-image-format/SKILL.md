---
name: choose-image-format
description: Use when hero or content images dominate LCP bytes. Picks AVIF/WebP/JPEG per image, encodes with avifenc/cwebp, and serves via picture.
---

# Choose Image Format

Images are usually the largest byte cost on a page, and the wrong format wastes half of them. Encode per image and negotiate by `Accept`, not by a global default.

## Procedure

1. Find the heaviest decodable images first:

       npx unlighthouse --site https://shop.example.com | jq '.reports[].imageElements'

   or in DevTools, Network -> Img filter, sort by Transfer Size.
2. Identify the class. Photographs go to AVIF with a WebP fallback and a JPEG floor; UI icons and logos with flat colour go to SVG; screenshots of text stay PNG or a lossless WebP.
3. Encode both modern formats from the original, not from a re-compressed JPEG:

       avifenc -q 50 hero-original.png hero.avif
       cwebp -q 72 hero-original.png -o hero.webp
       cjpeg -quality 82 hero-original.png > hero.jpg

4. Compare `ls -l hero.avif hero.webp hero.jpg`; AVIF typically lands 20-40% under WebP at equal visual quality. Inspect at 100% zoom, not at thumbnail size.
5. Serve with a `<picture>` so the browser picks from `Accept`:

       <picture>
         <source srcset="hero.avif" type="image/avif">
         <source srcset="hero.webp" type="image/webp">
         <img src="hero.jpg" width="1600" height="900" alt="hero" fetchpriority="high">
       </picture>

6. Do the same with `sharp` in a build step when you cannot hand-encode every asset.
7. Remove the original PNG from the served path so it cannot be picked up by a stray reference.

## Pitfalls

- Encoding AVIF inside a request handler; the first encode takes hundreds of milliseconds and blocks the response. Pre-encode at build time.
- Converting already-lossy JPEGs to AVIF, stacking two generations of artefacts.
- Serving AVIF without measuring support — encode a fallback chain rather than relying on feature detection in JS.
- Shipping a 4000-px-wide source to a 400-css-px slot; format compression does not fix over-delivery.
- Using WebP for the LCP hero when AVIF exists and the encoder is available anyway.

## Verification

    identify -format '%f %[mime] %wx%h %b\n' hero.avif hero.webp hero.jpg

The AVIF must be smaller than the WebP, which must be smaller than the JPEG, at the intended pixel dimensions. Report each size and the format chain served.
