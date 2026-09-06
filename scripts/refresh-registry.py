#!/usr/bin/env python3
"""Build every registry artifact in dependency order; fail on the first error."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def update_stats():
    catalog = json.loads((ROOT / 'docs/skills.json').read_text())
    skills = catalog['skills']
    counts = Counter(s['category'] for s in skills)
    total, mcp, cats = len(skills), counts['mcp-servers'], len(counts)
    official = sum('official' in s['tags'] for s in skills)
    path = ROOT / 'docs/index.html'
    html = path.read_text()
    for field, value in {'statSkills': f'{total}+', 'statMCP': mcp, 'statCategories': cats}.items():
        html = re.sub(rf'(id="{field}">)[\d,+]+', lambda m: m[1] + str(value), html)
    html = re.sub(r'\b\d+\+ (?:crypto )?skills', f'{total}+ skills', html)
    html = re.sub(r'\b\d+ MCP servers', f'{mcp} MCP servers', html)
    html = re.sub(r'\b\d+ categories', f'{cats} categories', html)
    path.write_text(html)
    path = ROOT / 'README.md'
    text = path.read_text()
    for label, value in {'skills': total, 'MCP%20servers': mcp, 'official': official, 'categories': cats}.items():
        text = re.sub(rf'{label}-\d+', f'{label}-{value}', text)
    text = re.sub(r'#skills-\d+overview', '#skills-overview', text)
    text = re.sub(r'\*\*\d+ skills\*\* covering', f'**{total} skills** covering', text)
    text = re.sub(r'\*\*\d+ MCP servers\*\*', f'**{mcp} MCP servers**', text)
    text = re.sub(r'\[\d+ MCP servers\]', f'[{mcp} MCP servers]', text)
    text = re.sub(r'\*\*\d+ official skills\*\*', f'**{official} official skills**', text)
    text = re.sub(r'\*\*\d+ skills\*\* from verified project teams:', f'**{official} skills** classified as official in the source metadata:', text)
    display = {k: v.get('name', k) if isinstance(v, dict) else v for k, v in catalog['categories'].items()}
    start, end = text.index('## Skills Overview'), text.index('## Quality Scores')
    text = text[:start] + '## Skills Overview\n\n| Category | Skills |\n|---|---:|\n' + ''.join(
        f'| {display.get(cat, cat)} | {count} |\n' for cat, count in counts.most_common()) + '\n' + text[end:]
    # Keep historical project highlights, but derive the aggregate grade table.
    grades = Counter(s.get('score', {}).get('grade') for s in skills)
    text = re.sub(r'(\| \*\*([ABCDF])\*\* \| [^|]+ \| )\d+', lambda m: m[1] + str(grades[m[2]]), text)
    passed = sum(s.get('score', {}).get('risk_gate') == 'PASS' for s in skills)
    text = re.sub(r'\*\*Risk Gate\*\*: \d+% pass \(\d+/\d+\)',
                  f'**Risk Gate**: {passed / total:.0%} pass ({passed}/{total})', text)
    path.write_text(text)
    print(f'Registry: {total} skills, {mcp} MCP servers, {official} official, {cats} categories', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true', help='Refresh upstream sources before rebuilding')
    args, remaining = parser.parse_known_args()
    if remaining and not args.fetch:
        parser.error('fetch arguments require --fetch')
    # Require the canonical parser dependencies before changing any artifacts.
    import canonicalize  # noqa: F401
    if args.fetch:
        subprocess.run([sys.executable, str(ROOT / 'scripts/auto-update.py'), *remaining], check=True, cwd=ROOT)
        if '--dry-run' in remaining:
            return
    for script in ['update-catalog.py', 'score-skills.py', 'extract-capabilities.py',
                   'score-history.py', 'generate-pages.py']:
        print(f'Running {script}', flush=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], check=True, cwd=ROOT)
    update_stats()


if __name__ == '__main__':
    main()
