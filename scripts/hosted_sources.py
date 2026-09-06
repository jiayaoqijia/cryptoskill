"""Verify curated hosted MCP documentation without connecting to accounts."""
from __future__ import annotations

import hashlib
import html
from html.parser import HTMLParser
import logging
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from sync_sources import ROOT, write_json


class DocumentationText(HTMLParser):
    """Join inline spans without losing URLs split by a rich-text renderer."""
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden = True
        elif tag in ('p', 'div', 'li', 'br'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = False
        elif tag in ('p', 'div', 'li'):
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def read_documentation(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Documentation must use a public HTTPS URL without credentials')
    request = urllib.request.Request(url, headers={'User-Agent': 'CryptoSkill-Source-Check/1'})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read(8 * 1024 * 1024 + 1)
        if len(body) > 8 * 1024 * 1024:
            raise ValueError('Documentation exceeds size limit')
        return body


def check_hosted_sources(sources, root=ROOT, dry_run=False):
    results = []
    for source in sources:
        row = {key: source[key] for key in ('slug', 'project', 'endpoint', 'documentation')}
        try:
            body = read_documentation(source['documentation'])
            text = html.unescape(body.decode('utf-8', errors='replace')).replace('\\/', '/')
            parser = DocumentationText()
            parser.feed(text)
            if source['endpoint'] not in text and source['endpoint'] not in ''.join(parser.parts):
                raise ValueError('Document no longer names the recorded endpoint; review the connection guide')
            row.update(status='documented', document_sha256=hashlib.sha256(body).hexdigest())
        except Exception as error:
            row.update(status='needs_review', detail=str(error))
            logging.warning('%s hosted source: %s', source['slug'], error)
        results.append(row)
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'sources': results,
              'scope': 'Documentation verification only; no account login or trading tools invoked.'}
    if not dry_run:
        write_json(root / 'docs/hosted-mcp-status.json', report)
    return report
