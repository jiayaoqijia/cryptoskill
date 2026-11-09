#!/usr/bin/env python3
"""Render a CDP CPU profile as a sample-weighted caller graph and self ranking."""
import argparse
from collections import defaultdict
from html import escape
import json
import math
from pathlib import Path


def render(profile):
    nodes = {node['id']: node for node in profile['nodes']}
    samples, deltas = profile.get('samples', []), profile.get('timeDeltas', [])
    if not samples or len(samples) != len(deltas):
        raise ValueError('CPU samples and matching timeDeltas are required')
    if any(not isinstance(d, (int, float)) or not math.isfinite(d) or d < 0 for d in deltas):
        raise ValueError('invalid sample time delta')
    parents = {}
    for node in nodes.values():
        for child in node.get('children', []):
            if child not in nodes or child in parents:
                raise ValueError('invalid CPU call tree')
            parents[child] = node['id']
    own, total = defaultdict(float), defaultdict(float)
    for sample, delta in zip(samples, deltas):
        if sample not in nodes:
            raise ValueError('sample references an unknown CPU node')
        own[sample] += delta
        cursor, seen = sample, set()
        while cursor is not None:
            if cursor in seen:
                raise ValueError('cycle in CPU call tree')
            seen.add(cursor)
            total[cursor] += delta
            cursor = parents.get(cursor)
    weight = sum(deltas)
    if weight <= 0:
        raise ValueError('CPU profile has no positive sampled time')
    roots = [key for key in nodes if key not in parents and total[key]]
    boxes, depth = [], 0

    def label(key):
        frame = nodes[key]['callFrame']
        # Raw profiles remain local; the view needs names and locations, no URL queries.
        url = frame.get('url', '').split('?', 1)[0].split('#', 1)[0].rsplit('/', 1)[-1]
        return f"{frame.get('functionName') or '(anonymous)'} {url}:{frame.get('lineNumber', -1) + 1}"

    def draw(key, x, level):
        nonlocal depth
        pending = [(key, x, level)]
        while pending:
            key, x, level = pending.pop()
            depth = max(depth, level)
            width = total[key] / weight * 1200
            text = label(key)
            title = escape(f'{text}: inclusive {total[key] / 1000:.3f} ms; self {own[key] / 1000:.3f} ms')
            color = f'hsl({sum(map(ord, text)) % 55},80%,72%)'
            boxes.append(f'<g><title>{title}</title><rect x="{x:.3f}" y="{level * 22}" '
                         f'width="{width:.3f}" height="21" fill="{color}" stroke="white"/>')
            if width > 12:
                boxes.append(f'<text x="{x + 3:.3f}" y="{level * 22 + 15}">{escape(text[:max(0, int(width / 7) - 1)])}</text>')
            boxes.append('</g>')
            child_x = x
            children = []
            for child in sorted(nodes[key].get('children', []), key=lambda c: total[c], reverse=True):
                if total[child]:
                    children.append((child, child_x, level + 1))
                    child_x += total[child] / weight * 1200
            pending.extend(reversed(children))

    x = 0
    for root in roots:
        draw(root, x, 0)
        x += total[root] / weight * 1200
    rows = ''.join(f'<tr><td>{escape(label(key))}</td><td>{own[key] / 1000:.3f}</td>'
                   f'<td>{total[key] / 1000:.3f}</td></tr>'
                   for key in sorted(own, key=own.get, reverse=True) if own[key])
    window = (profile['endTime'] - profile['startTime']) / 1000
    return f'''<!doctype html><meta charset="utf-8"><title>JS CPU profile</title>
<style>body{{font:14px system-ui;margin:24px}}svg{{font:12px monospace}}td,th{{text-align:left;padding:4px 14px 4px 0}}</style>
<h1>JS CPU profile</h1><p>{len(samples)} samples; window {window:.3f} ms;
weighted time {weight / 1000:.3f} ms; largest sample delta {max(deltas) / 1000:.3f} ms.</p>
<p>Top-down caller graph. Width is sample-weighted time, not exact function duration.
Hover for location and self/inclusive estimates. Check idle-only or missing stall coverage against the recipe timeline.</p>
<svg viewBox="0 0 1200 {(depth + 1) * 22}" role="img" aria-label="Sample-weighted CPU caller graph">{''.join(boxes)}</svg>
<h2>Self-time ranking</h2><table><tr><th>Function / location</th><th>Self ms</th><th>Inclusive ms</th></tr>{rows}</table>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile', type=Path)
    parser.add_argument('html', type=Path)
    args = parser.parse_args()
    try:
        page = render(json.loads(args.profile.read_text()))
        with args.html.open('x') as output:
            output.write(page)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f'profile-flame: {error}\n')


if __name__ == '__main__':
    main()
