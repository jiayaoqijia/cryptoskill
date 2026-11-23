# Emailing deliverables with attachments

Use when the user says "kirim ke email gw" after producing files (deck, PDF,
docx, spreadsheet) and the payload is more than a body of text.

`google_api.py gmail send` takes `--body` only — no attachment flag. The
bundled `scripts/gmail_send_attachments.py` closes that gap with stdlib
(`email.message.EmailMessage` + `urllib`), so it does not need
`googleapiclient`:

```bash
python scripts/gmail_send_attachments.py \
  --to campus-email@example.edu --cc your-email@example.com \
  --subject "Deck dan naskah presentasi H&M (versi final)" \
  --body-file /tmp/body.txt \
  --attach out/deck.pptx --attach out/deck.pdf \
  --attach out/script.docx --attach out/script.pdf
```

It prints `{"id": ..., "labels": [...]}`. A correct send returns labels
`SENT`; `UNREAD`/`INBOX` also appear when the sender is in To or Cc, which is
normal and not a failure.

## Which address

Academic/course deliverables: send to the campus address and Cc the personal
account, both taken from the profile — do not stall the send on a question when
both addresses already exist. Anything sensitive (finance, identity, third-party
correspondence) still needs an explicit confirmation first.

## Verify, do not assume

`messages.send` returning an id proves the API accepted the payload, not that
the files arrived. Read the message back and walk the MIME tree:

```python
GET /gmail/v1/users/me/messages/{id}?format=full
```

Check three things and report them: the `To`/`Cc`/`Subject` headers, each
`part.filename` with its `mimeType` and `body.size`, and the total
`sizeEstimate`. Attachment sizes should match the local files to within a few
hundred bytes (base64/metadata slack). Confirm attachment filenames survive
non-ASCII subjects — Gmail stores the raw MIME filename, so a stray `?` in a
filename is the tell of a broken Content-Disposition.

## Pitfalls

- **Attach the PDF next to every editable file.** The PPTX/DOCX reference fonts
  by name; a recipient machine without them reflows the layout. The PDF is what
  they will actually read on a phone.
- **A 25 MB ceiling is hard.** Four files including a photo-backed deck land
  around 1.5 MB, but a video or a bundled dataset will not. The script refuses
  above 24 MB instead of letting Gmail reject the whole message.
- **Message body: say what each file is and where the numbers came from.** The
  body is the only context that survives forwarding; one numbered line per
  attachment is enough.
- **Do not re-send on a partial failure without checking `SENT`.** Query
  `messages.list` with `q=subject:"..." newer_than:1d` first; a duplicate deck
  email is worse than a delayed one.
