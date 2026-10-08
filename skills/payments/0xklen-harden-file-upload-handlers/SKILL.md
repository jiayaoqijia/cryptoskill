---
name: harden-file-upload-handlers
description: Use when an endpoint accepts file uploads. Checks type validation by content, storage location, size limits, filename handling, and safe serving, then closes the classic bypasses.
---

# Harden file upload handlers

An upload endpoint is a path from untrusted bytes onto your filesystem and back out to other users.
The risks are execution (interpret the file as code), traversal (the filename is a path), storage
denial of service (no size cap), and stored XSS (an HTML/SVG served inline).

## Procedure

1. Locate upload handlers by parsing multipart input or writing request bodies to disk:

       rg -n "multipart|UploadFile|\.files\[|req\.file|formData|busboy|multer|FileField|UploadedFile" src/

2. Validate the *content*, not the claimed name. Check the magic bytes and, for images, decode:

       import imghdr
       kind = imghdr.what(None, header=file.read(2048))   # or python-magic / filetype lib
       if kind not in {"png", "jpeg", "gif"}:
           raise ValueError("unsupported type")

   The `Content-Type` header and the extension are attacker-controlled — never sole gates. A file
   named `x.png` with a PHP body is the canonical bypass.

3. Never build the stored path from the client filename. Generate a random name and keep the
   extension from the *detected* type:

       import secrets, pathlib
       ext = {"png": ".png", "jpeg": ".jpg"}[kind]
       safe = pathlib.Path("/srv/uploads") / (secrets.token_hex(16) + ext)
       if pathlib.Path(safe).resolve().parent != pathlib.Path("/srv/uploads").resolve():
           raise PermissionError

4. Store outside the web root. The web server must not execute anything in the upload directory:

       # nginx: uploads dir must not run PHP/scripts
       location /uploads/ { location ~ \.(php|phtml|jsp)$ { deny all; } }

5. Cap the size at the proxy *and* the app (reject early), and limit total upload quota per user.

6. Re-encode images (strip EXIF and embedded scripts) rather than storing the raw bytes:

       from PIL import Image
       Image.open(upload).convert("RGB").save(out, "JPEG", quality=85)

7. Serve user files with `Content-Disposition: attachment` and a `Content-Type` you set, plus
   `X-Content-Type-Options: nosniff`, so an HTML/SVG file cannot run in your origin.

8. If the file is parsed (archive, office doc, PDF), do it out of process or in a sandbox.

## Pitfalls

- An allowlist of extensions without content checks passes `shell.png` renamed `shell.png.php`.
- Double extensions and trailing dots/spaces (`x.php.`, `x.php%00.png`) defeat naive checks.
- SVG is XML and can carry `<script>`; treat it as HTML, not as an image.
- Storing under the web root with the original name enables overwrite and, on misconfigured
  servers, execution.
- No size limit lets a single request fill the disk; decompression bombs (zip) do the same inside.
- Trusting the client `Content-Type` is the most common bypass; verify bytes.

## Verification

    file --mime-type /srv/uploads/* | rg -v 'image/(png|jpeg|gif)' && echo "UNEXPECTED TYPE"
    curl -s -F 'file=@shell.php;type=image/png' https://app.example.com/upload -o /dev/null -w '%{http_code}\n'

Pass: the PHP payload is rejected (400/415), stored files match the allowlist by real content, and
serving returns `Content-Disposition: attachment` with `nosniff`. Report the checks added, the
storage path, and each bypass now blocked.
