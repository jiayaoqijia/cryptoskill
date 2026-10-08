---
name: review-path-traversal-in-file-apis
description: Use when a handler turns user input into a filesystem path, including archive extraction. Traces the path from request to open, tests ../ and encoded traversal, and confines reads to a base directory.
---

# Review path traversal in file APIs

Any endpoint that builds a file path from user input — download, upload, template name, static
serve, or archive extraction — can be walked out of its intended directory with `../`. The canonical
defence is to resolve the final path and assert it stays inside a fixed base.

## Procedure

1. Find path-building sinks fed by input:

       rg -n "open\(|readFile|createReadStream|sendFile|os\.path\.join|path\.join|filepath\.Join|File\(|StreamReader" src/ \
         | rg -i "req|param|query|user|name|file|path|filename|key"

2. Trace the input to the sink. Note whether a filename comes from the URL, a JSON field, an
   uploaded part, or a zip entry name.

3. Probe with traversal payloads (raw and encoded) against staging:

       for p in '../../etc/passwd' '..%2f..%2fetc%2fpasswd' '....//....//etc/passwd' \
                '%2e%2e%2f%2e%2e%2fetc%2fpasswd' '..%252f..%252fetc%252fpasswd'; do \
         curl -s "https://app.example.com/files?name=$p" | head -c 40; echo; \
       done

4. Fix with a resolve-and-confine check, using the platform's realpath:

       import os
       BASE = os.path.realpath("/srv/data")
       target = os.path.realpath(os.path.join(BASE, user_name))
       if os.path.commonpath([BASE, target]) != BASE:   # or not target.startswith(BASE + os.sep)
           raise PermissionError("path escapes base")
       # symlinks are resolved by realpath, so a link out is caught too

5. Reject absolute paths and NUL bytes (`\x00`) before joining; strip directory components from
   bare filenames with `os.path.basename` / `filepath.Base` only when a flat namespace is intended.

6. For archive extraction (zip/tar), guard each member the same way — the "Zip Slip" class:

       for member in tar.getmembers():
           dest = os.path.realpath(os.path.join(BASE, member.name))
           if not dest.startswith(BASE + os.sep):
               raise PermissionError(member.name)

7. Store uploads outside the web root and serve them through the checked handler, not via the
   static server.

## Pitfalls

- Decoding the URL once then checking, while the filesystem call decodes again, reopens the hole.
- `os.path.join(BASE, "/etc/passwd")` returns `/etc/passwd` — joining does not neutralise an
  absolute path.
- A prefix check `startswith("/srv/data")` accepts `/srv/data-evil`; compare with the separator.
- Windows separators (`..\`) and UNC paths need the Windows branch of the check.
- Symlinks inside the base point outside it; only a resolved-path check catches them.
- Client-side validation of the filename is bypassable; enforce server-side.

## Verification

    curl -s --get --data-urlencode 'name=../../etc/passwd' https://app.example.com/files -o /dev/null -w '%{http_code}\n'
    curl -s --get --data-urlencode 'name=..%2f..%2fetc%2fpasswd' https://app.example.com/files -o /dev/null -w '%{http_code}\n'

Pass: every traversal payload returns 400/403/404 and never the file body. Report the sink, the
base directory enforced, and each payload's result.
