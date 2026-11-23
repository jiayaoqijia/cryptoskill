#!/usr/bin/env python3
"""Read Gmail messages as raw MIME: print text parts, save attachments.

Why: `google_api.py gmail get <id>` returns `body: ""` for HTML-only mail (order confirmations,
e-tickets, invoices, most marketing) because it only lifts a text/plain part. This reads the raw
message, decodes EVERY part, and writes attachments to disk so they can be inspected/kept.

Run it with the SAME python that has the Google client (see the Usage section of this skill):

    PY=~/.hermes/hermes-agent/venv/bin/python       # or ~/.hermes/installs/*/environments/*/venv/bin/python
    $PY scripts/gmail_raw_read.py <message_id> [<message_id> ...] [--outdir DIR]

Auth is the shared token at ~/.hermes/google_token.json (refreshes automatically).
"""

import argparse
import base64
import email
import html
import os
import re

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN = os.path.expanduser(os.environ.get("GOOGLE_TOKEN", "~/.hermes/google_token.json"))


def clean(t: str) -> str:
    t = re.sub(r"<(script|style).*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"</(p|div|tr|h[1-6]|li)>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t\xa0]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("message_ids", nargs="+")
    ap.add_argument("--outdir", default="/tmp/gmail_parts")
    ap.add_argument("--chars", type=int, default=2500, help="max chars printed per text part")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    creds = Credentials.from_authorized_user_file(TOKEN)
    svc = build("gmail", "v1", credentials=creds)

    for mid in args.message_ids:
        raw = svc.users().messages().get(userId="me", id=mid, format="raw").execute()
        msg = email.message_from_bytes(base64.urlsafe_b64decode(raw["raw"]))
        print("=" * 70)
        print("ID:", mid)
        print("SUBJEK:", msg.get("Subject"))
        print("DARI:", msg.get("From"))
        print("TANGGAL:", msg.get("Date"))
        for part in msg.walk():
            ctype = part.get_content_type()
            payload = part.get_payload(decode=True) or b""
            filename = part.get_filename()
            if filename:
                safe = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
                path = os.path.join(args.outdir, f"{mid[:8]}_{safe}")
                with open(path, "wb") as fh:
                    fh.write(payload)
                print(f"LAMPIRAN: {filename} -> {path} ({len(payload)} byte)")
                continue
            if ctype in ("text/plain", "text/html") and payload:
                text = clean(payload.decode(part.get_content_charset() or "utf-8", "replace"))
                if text:
                    print(f"--- bagian {ctype} ---")
                    print(text[: args.chars])


if __name__ == "__main__":
    main()
