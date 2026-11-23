# Drive evidence package upload

Use when the user asks for a structured proof/deliverable package on Drive: one folder per project, screenshots, documents, raw test output.

## Non-negotiables

- **Never touch existing Drive content.** Create one new root folder with a dated, unmistakable name and write only inside it. If the user says "don't touch my other files", treat every pre-existing folder as read-only.
- **Private by default.** The owner token can open the folder; do not add `anyone`/`domain` permissions unless asked.
- **No client or sensitive financial data** in a package that might be shared later. Use demo/sample data for screenshots.

## Procedure

1. **Plan before writing.** Build an explicit mapping of local paths → Drive folder names, and validate every source path exists. Fail before creating folders, not halfway through an upload.
2. **Idempotent folder creation** — search by name + parent + folder mimeType + `trashed=false`; create only when absent:

```python
q = (f"'{parent}' in parents and name = '{name}' and "
     "mimeType = 'application/vnd.google-apps.folder' and trashed = false")
```

3. **Upload** with `MediaFileUpload` (non-resumable is fine below a few MB). Set MIME explicitly: `.md` should be `text/markdown`; `mimetypes.guess_type` returns `None` or an odd type for it.
4. **Mirror the evidence tree.** Each project folder gets `bukti/` with the raw artefacts (test logs, API JSON, CSV, calibration files) next to the human-readable PDF. Reviewers can then trace every number.
5. **Verify by read-back, not by the upload response**:
   - Fetch the folder tree recursively; compare each folder's file-name set against the expected set and report MISSING/EXTRA.
   - Count the total and assert it equals the number of planned uploads.
   - Download one binary back and compare `md5` with the local file. A matching hash is the only proof the bytes landed.
6. **Updating a document later**: delete + re-create changes the file id. If links must stay stable, use `files().update(fileId=..., media_body=...)` instead.

## Interpreter

The system `python3` often lacks `googleapiclient`. Probe the Hermes-managed environments and use the first that imports it:

```bash
for p in ~/.hermes/installs/*/environments/*/venv/bin/python ~/.hermes/hermes-agent/venv/bin/python; do
  [ -x "$p" ] && "$p" -c 'import googleapiclient' 2>/dev/null && echo "OK $p"
done
```

Run the whole upload from one script so a retry does not duplicate files: folder lookup is idempotent, and a re-run only adds what is missing.

## Reporting

Give the folder URL, the file count, the per-folder breakdown, and the verification result (tree match + hash match). If a planned screen was dropped (still loading, error page, empty state), say which and why — an honest gap is better than a screenshot that proves nothing.