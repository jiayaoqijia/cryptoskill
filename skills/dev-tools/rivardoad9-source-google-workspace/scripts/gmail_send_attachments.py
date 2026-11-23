#!/usr/bin/env python3
"""Send a Gmail message with file attachments, stdlib only.

Exists because `google_api.py gmail send` has no --attach flag, and because
importing googleapiclient can hang for minutes on a cold/broken env while a
raw HTTPS call to the REST endpoint returns in under a second.

Usage:
  python gmail_send_attachments.py --to a@b.c [--cc d@e.f] \
      --subject "Deck final" --body-file body.txt \
      --attach deck.pptx --attach deck.pdf

Reads ~/.hermes/google_token.json (refresh_token + client_id/secret), exchanges
it for an access token, sends multipart/mixed, and prints the message id.
Verify afterwards with messages.get?format=full (see references/gmail-send-attachments.md).
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.parse
import urllib.request
from email.message import EmailMessage

TOKEN_PATH = os.path.expanduser("~/.hermes/google_token.json")
SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"


def access_token():
    tok = json.load(open(TOKEN_PATH))
    data = urllib.parse.urlencode({
        "client_id": tok["client_id"],
        "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(
        tok["token_uri"], data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["access_token"]


def build(args):
    body = open(args.body_file, encoding="utf-8").read() if args.body_file else args.body or ""
    msg = EmailMessage()
    msg["To"] = args.to
    if args.cc:
        msg["Cc"] = args.cc
    msg["From"] = args.sender or args.cc or args.to
    msg["Subject"] = args.subject
    msg.set_content(body)
    for path in args.attach or []:
        ctype, _ = mimetypes.guess_type(path)
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        with open(path, "rb") as fh:
            msg.add_attachment(fh.read(), maintype=maintype, subtype=subtype,
                               filename=os.path.basename(path))
    size = len(msg.as_bytes())
    if size > 24 * 1024 * 1024:
        sys.exit(f"message would be {size/1e6:.1f} MB, over Gmail's 25 MB limit")
    return msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True)
    ap.add_argument("--cc")
    ap.add_argument("--sender")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body")
    ap.add_argument("--body-file")
    ap.add_argument("--attach", action="append")
    args = ap.parse_args()

    raw = base64.urlsafe_b64encode(build(args).as_bytes()).decode()
    req = urllib.request.Request(
        SEND_URL, data=json.dumps({"raw": raw}).encode(), method="POST",
        headers={"Authorization": f"Bearer {access_token()}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r)
    print(json.dumps({"id": out.get("id"), "labels": out.get("labelIds")}))


if __name__ == "__main__":
    main()
