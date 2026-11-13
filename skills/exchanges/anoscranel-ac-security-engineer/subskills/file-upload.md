---
name: file-upload
domain: security-hardening/file-upload
trigger: Accepting file uploads from users and storing, scanning or serving them back, including archives and images.
anti_trigger: Validating non-file input (subskills/input-output.md); scanning dependencies and artifacts in the build (subskills/supply-chain.md).
scope: Type, size, storage, scanning and serving of uploads
status: seedling
---

# File Upload

## Standard

- OWASP File Upload Cheat Sheet controls: allow-list extensions after input validation; validate the real type — "don't trust the Content-Type header"; rename to an app-generated filename; limit filename length and characters; set a size limit; only authorised users upload; store outside the webroot and serve via an id→file handler; run antivirus or sandbox; run Content Disarm & Reconstruction for PDF/DOCX; protect the upload from CSRF.
- OWASP ASVS 5.0 **V5 File Handling**: 5.1.1 document permitted types and max sizes (L2) · 5.2.1 size limit (L1) · 5.2.2 extension and magic bytes match, including inside archives (L1) · 5.2.3 max uncompressed size and entry count before unpacking (L2) · 5.2.4 per-user quota (L3) · 5.2.5 reject symlinked archives (L3) · 5.2.6 max image pixel size (L3) · 5.3.1 public-folder files never execute as code (L1) · 5.3.2 paths from internal data, not user filenames (L1) · 5.3.3 decompression ignores user paths — zip slip (L3) · 5.4.1 ignore user filenames, set `Content-Disposition` (L2) · 5.4.2 encode served filenames (RFC 6266) (L2) · 5.4.3 AV-scan untrusted sources (L2). ⚠️ Some levels were read from truncated rows — re-check before relying on them.

## Decision rules

1. The declared `Content-Type` is a claim, not evidence: check magic bytes, and the extension allow-list after that.
2. Rename every upload to an app-generated identifier; the user's filename never touches the filesystem.
3. Store uploads outside the webroot, or in a store that will not execute them; serve through a handler that sets the safe content type and disposition.
4. Bound three sizes before work: file size, uncompressed size, archive entry count.
5. Scan files from untrusted sources; use CDR for document formats where available.
6. Rate-limit and quota the upload endpoint — an open upload form is a storage-billing attack (API4).

## Procedure

1. Document permitted types, extensions, maximum sizes and unpacked limits (ASVS 5.1.1) before building.
2. Require authentication; apply CSRF protection to the upload form.
3. Validate: extension allow-list → magic bytes → size → archive limits. Reject on any failure, with a generic message.
4. Store under a generated id in private storage; record metadata (owner, type, size) in the database.
5. Serve via a handler that maps id→file, sets `Content-Type` from the verified type, sets `Content-Disposition` with an RFC 6266-encoded filename, and never exposes the storage path.
6. For archives: reject symlink entries, ignore embedded paths (zip slip), unpack only after the uncompressed-size check.

## Anti-patterns

- Serving uploads from the webroot with the original filename.
- Trusting the client's `Content-Type` or file extension.
- Unpacking an archive before checking its uncompressed size or entries (zip bomb, zip slip).
- No quota on the upload endpoint.

## Done checklist

- [ ] Permitted types, sizes and unpacked limits documented.
- [ ] Upload requires authentication and CSRF protection.
- [ ] Extension and magic-byte checks both enforced.
- [ ] Files stored under generated ids outside the webroot.
- [ ] Downloads served via handler with safe type and disposition.
- [ ] Archive checks (size, count, symlinks, paths) run before unpacking.
- [ ] Upload endpoint rate-limited and quota'd.

## Sources

- Primary: OWASP File Upload Cheat Sheet; OWASP ASVS 5.0 V5 (5.1.1–5.4.3); RFC 6266.
- <https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html>
- <https://owasp.org/www-project-application-security-verification-standard/>
