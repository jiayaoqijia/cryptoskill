# App metadata: showing your app's name, description, and logo

By default the Internet Identity sign-in screens identify an app by its **origin** alone. To also show a name, a short tagline, and a logo, serve a JSON document at `/.well-known/ii-app-metadata`. Publishing it is permissionless: there is no list to join and no approval step. A valid document replaces the curated entry II still ships for a small set of known apps.

```json
{
  "name": "Example App",
  "description": "A short tagline shown on the sign-in screen",
  "logo": "/logo.png"
}
```

## Which origin serves it

II fetches the document from the origin identities are derived for: the validated `derivationOrigin` when the auth request sets one, and the request's own origin otherwise. Publish it once on the derivation origin and every alternative origin that origin certifies shows the same name, description, and logo. A copy served only on the alternative origin the user visits is never read.

## Validation rules

All three fields are optional and unknown fields are ignored, so a document stays valid as II adds fields.

- `name` is at most 40 characters and `description` at most 120, counted in **Unicode code points on the value as served**, before whitespace collapsing. Collapsing is display-only and never rescues an over-long value.
- Each field must contain at least one visible character. A field holding only whitespace or invisible characters is rejected, not treated as absent.
- Rejected characters: control characters (other than the ASCII whitespace `\t`, `\n`, `\v`, `\f`, `\r`), `U+FEFF`, and the bidirectional embeddings and overrides `U+202A` to `U+202E`. Accepted: the marks `U+200E`, `U+200F`, `U+061C`, the isolates `U+2066` to `U+2069`, and the zero-width characters `U+200B` to `U+200D`. Isolates must be **balanced**: a field closes every isolate it opens and none it did not open.
- **One bad field invalidates the whole document.** None of it is applied (not half of it); II falls back to its curated entry if it ships one for the app, and to the origin alone otherwise. II logs the offending field to the browser console on the sign-in screen. A document carrying no field II recognises is ignored too.
- `logo` must be a **raster** image URL on the **same origin** as the document (relative URLs resolve against it), served as `image/png`, `image/jpeg`, `image/webp`, `image/gif`, or `image/avif`, at most 1 MiB and 4096 pixels per axis. `image/svg+xml` is rejected: serve a rasterised copy. II downloads the image (it is never hotlinked), redraws it at up to 512 pixels on its longest side (an animated image is flattened to its first frame), and renders that copy, so ship a roughly square PNG or WebP of about 512 pixels.
- **Write the logo URL relative** (`/logo.png`). II normalizes a canister gateway origin onto `ic0.app` and tries its `icp0.io` and `icp.net` twins in turn, so the document may be fetched from a sibling gateway domain of the same canister, and the same-origin check runs against whichever answered. An absolute URL pinned to one of them is cross-origin at the other two.
- Only the *shape* of `logo` (a non-empty URL on the document's own origin) is part of document validation. Once that passes, a logo that cannot be fetched or decoded, or that breaks the content-type, size, or dimension rules, costs the logo alone: the name and description still render.
- The document must not exceed 8 KiB, must be answered with `200`, and must not redirect (II follows redirects for neither the document nor the logo). II requests it without credentials and gives up after 10 seconds.

## CORS

The document and the logo are both read cross-origin, so both need CORS headers. With `@dfinity/static-site`, add them to the `_headers` file at the root of the build directory:

```
/.well-known/ii-app-metadata
  Content-Type: application/json
  Access-Control-Allow-Origin: *

/logo.png
  Access-Control-Allow-Origin: *
```

`.well-known/` is uploaded automatically, but the document has no file extension, so its media type must be set with the bare `Content-Type:` line.

Missing, unreachable, or invalid metadata never blocks sign-in. Publishing it verifies nothing about the app: II keeps showing the origin next to whatever the document provides, because the origin is the part users can check.
