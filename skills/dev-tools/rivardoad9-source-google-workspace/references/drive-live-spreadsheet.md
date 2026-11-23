# Uploading a workbook as a live Google Sheet

## When to Use

Use when the user asks for a spreadsheet they will keep updating themselves ("upload ke Drive biar gampang nambahin"). A plain `.xlsx` upload opens read-only in the Drive preview and forces a convert-copy on every edit; a native Sheet is editable from the phone, which is what they actually asked for.

## Which interpreter

The system `python3` usually lacks `googleapiclient`. Probe for an interpreter that imports it, then use that one for every call in the session:

```bash
for p in ~/.hermes/google_venv/bin/python ~/.hermes/installs/*/environments/*/venv/bin/python ~/.hermes/hermes-agent/venv/bin/python; do
  [ -x "$p" ] && "$p" -c 'import googleapiclient' 2>/dev/null && echo "OK $p"
 done
```

Token: `~/.hermes/google_token.json` (scopes include `drive` and `spreadsheets`). Refresh and write the token back, or the next session starts from an expired file:

```python
creds = Credentials.from_authorized_user_file(TOKEN)
if not creds.valid:
    creds.refresh(Request())
    open(TOKEN, "w").write(creds.to_json())
```

## Upload with conversion

The conversion happens through `mimeType` in the **metadata body**, not through the API method:

```python
media = MediaFileUpload(path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
drive.files().create(
    body={"name": name, "parents": [folder_id],
          "mimeType": "application/vnd.google-apps.spreadsheet"},  # <- makes it a Sheet
    media_body=media,
    fields="id,name,mimeType,webViewLink",
).execute()
```

Without that field the file stays an Excel binary in Drive.

## Idempotent replace

Re-uploading the same deliverable must not leave five copies and five dead links. Create the folder once (query by name + folder mimeType), then list `name='<title>' and '<folder_id>' in parents and trashed=false`, delete every hit, and create the new one. Expect the share link to change on every replace — send the new `webViewLink` to the user each time and say the old link is dead.

## Verification (also the cheapest formula check)

Google Sheets recalculates formulas on import, so reading the uploaded file back proves the formulas are right without LibreOffice:

```python
sh.spreadsheets().values().get(spreadsheetId=fid, range="Ringkasan!A1:B20").execute()
```

Check the computed totals against values you wrote by hand (row count vs. number of records, MIN/MAX vs. the known price ladder). A summary cell that comes back negative or blank is a formula bug, not a formatting issue — fix it in the generator, re-run, re-upload. Pull the sheet list from `spreadsheets().get` too, to confirm every tab survived the conversion.

## What survives conversion

Formulas, number formats (`"Rp"#,##0`), fills, merges, freeze panes, autofilter and validation lists carry over. Charts usually survive but may be re-anchored or lose styling. Anything that matters visually should still be checked in the Sheet, and the generator script should stay in the workspace so the workbook can be rebuilt with one command instead of hand-edited.

Deliver both: the `.xlsx` in chat (the archive copy that opens anywhere) and the Sheet link (the working copy).
