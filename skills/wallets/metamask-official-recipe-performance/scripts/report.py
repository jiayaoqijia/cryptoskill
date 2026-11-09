#!/usr/bin/env python3
"""Extract paired JS-window metrics, interpolated percentiles and block separation."""
import argparse
import json
from pathlib import Path
import statistics
import sys


def percentile(values, fraction):
    values = sorted(values)
    position = (len(values) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    return values[lower] + (values[upper] - values[lower]) * (position - lower)


def timings(path, start_mark, end_mark, layout_mark, spans, events):
    data = json.loads(path.read_text())
    if isinstance(data, str):  # CDP evaluators may wrap their JSON result in a JSON string.
        data = json.loads(data)
    marks = {}
    for mark in data['marks']:
        marks.setdefault(mark['n'], mark['t'])
    start = marks.get(start_mark)
    ends = [marks.get(name) for name in end_mark.split(',')]
    if start is None or any(end is None for end in ends):
        raise ValueError(f'{path}: missing or invalid {start_mark}/{end_mark} window')
    end = max(ends)
    if end <= start:
        raise ValueError(f'{path}: missing or invalid {start_mark}/{end_mark} window')
    frames = data['frames']
    if any(b < a for a, b in zip(frames, frames[1:])):
        raise ValueError(f'{path}: frame timestamps are not chronological')
    gaps = [b - a for a, b in zip(frames, frames[1:]) if b > start and a < end]
    after = [frame for frame in frames if frame > start]
    if not gaps or not after or frames[0] > start or frames[-1] < end:
        raise ValueError(f'{path}: frame probe did not cover the open')
    result = {'window ms': end - start,
              'fps': sum(start <= frame <= end for frame in frames) / ((end - start) / 1000),
              '>100 ms frames': sum(gap > 100 for gap in gaps),
              'longest frame': max(gaps),
              'blocked ms': sum(max(0, gap - 50) for gap in gaps),
              'next JS frame ms': after[0] - start}
    if layout_mark:
        result['layout ms'] = marks[layout_mark] - start if layout_mark in marks else None
    trace = {}
    for item in data.get('traces', []):
        trace.setdefault((item['n'], item['ph']), item['t'])
    for label, name in spans:
        result[label] = (trace[(name, 'e')] - trace[(name, 's')]
                         if (name, 's') in trace and (name, 'e') in trace else None)
    for label, name in events:
        times = [item[3] for item in data.get('calls') or []
                 if item[0] == 'event' and item[2] == name and item[3] >= start]
        result[label] = min(times) - end if times else None
    return result


def blocks(root):
    manifest = root / 'blocks.json'
    if manifest.exists():
        data = json.loads(manifest.read_text())
        rows = data['blocks']
        if len(rows) != len(data['states']) * data['repeats']:
            raise ValueError('incomplete alternating block manifest')
        return rows, data['rounds']
    rows = []
    for line in (root / 'blocks.txt').read_text().splitlines():
        fields = line.split()
        if fields:
            rows.append({'block': fields[0], 'state': fields[1],
                         'status': 'pass' if 'status=pass' in fields else 'failed'})
    return rows, None


def separation(base, candidate, higher):
    better = min(candidate) > max(base) if higher else max(candidate) < min(base)
    worse = max(candidate) < min(base) if higher else min(candidate) > max(base)
    if better:
        return 'better-separated'
    if worse:
        return 'worse-separated'
    return 'not-separated'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('baseline')
    parser.add_argument('candidate')
    parser.add_argument('--scenario', action='append', default=[], metavar='LABEL=RELATIVE_GLOB')
    parser.add_argument('--rounds', type=int, help='required for legacy blocks.txt exports')
    parser.add_argument('--start-mark', default='press')
    parser.add_argument('--end-mark', default='open-complete', help='comma-separated required marks; latest first occurrence wins')
    parser.add_argument('--layout-mark')
    parser.add_argument('--span', action='append', default=[], metavar='LABEL=SPAN_NAME')
    parser.add_argument('--event', action='append', default=[], metavar='LABEL=EVENT_KEY')
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    scenarios = [entry.split('=', 1) for entry in args.scenario or ['open=data/timed-*.json']]
    spans = [entry.split('=', 1) for entry in args.span]
    events = [entry.split('=', 1) for entry in args.event]
    if any(len(pair) != 2 or not all(pair) for pair in scenarios + spans + events):
        parser.error('scenario/span/event options require LABEL=VALUE')
    rows, recorded_rounds = blocks(args.root)
    rounds = args.rounds or recorded_rounds
    if not rounds or rounds < 1 or (recorded_rounds and rounds != recorded_rounds):
        parser.error('supply the planned --rounds; it must match blocks.json')
    if not rows or any(row['status'] != 'pass' for row in rows):
        raise ValueError('every planned block must pass; retain failed captures separately')
    states = [args.baseline, args.candidate]
    if set(row['state'] for row in rows) != set(states):
        raise ValueError('block states do not match the requested comparison')
    if any(row['state'] != states[index % 2] for index, row in enumerate(rows)):
        raise ValueError('blocks must alternate baseline/candidate')
    if any(sum(row['state'] == state for row in rows) < 2 for state in states):
        raise ValueError('at least two blocks per state are required for the noise check')
    output = {}
    for scenario, pattern in scenarios:
        per_state = {state: [] for state in states}
        for row in rows:
            paths = sorted((args.root / row['block']).glob(pattern))
            if len(paths) != rounds:
                raise ValueError(f'{row["block"]}/{scenario}: expected {rounds} opens, found {len(paths)}')
            samples = [timings(p, args.start_mark, args.end_mark, args.layout_mark, spans, events)
                       for p in paths]
            per_state[row['state']].append({'block': row['block'], 'samples': samples})
        metrics = {}
        for key in per_state[states[0]][0]['samples'][0]:
            summaries = {}
            for state in states:
                values = [sample[key] for block in per_state[state] for sample in block['samples']
                          if sample[key] is not None]
                medians = [statistics.median(values) if values else None for values in
                           [[sample[key] for sample in block['samples'] if sample[key] is not None]
                            for block in per_state[state]]]
                summaries[state] = {'n': len(values), 'p50': statistics.median(values) if values else None,
                                    'p75': percentile(values, .75) if values else None,
                                    'blockP50': medians}
            complete = all(summary['n'] == rounds * len(per_state[state])
                           for state, summary in summaries.items())
            noise = (separation(summaries[states[0]]['blockP50'], summaries[states[1]]['blockP50'], key == 'fps')
                     if complete and key not in dict(events) else 'not-checked')
            metrics[key] = {'states': summaries, 'blockSeparation': noise}
        output[scenario] = {'blocks': per_state, 'metrics': metrics}
        print(f'\n### {scenario}\n\n| metric (p50 / p75) | {states[0]} | {states[1]} | block check |')
        print('| --- | --- | --- | --- |')
        for key, metric in metrics.items():
            cells = []
            for state in states:
                summary = metric['states'][state]
                fmt = (lambda n: f'{n:.1f}') if key == 'fps' else (lambda n: f'{n:,.0f}')
                cells.append(f'{fmt(summary["p50"])} / {fmt(summary["p75"])} (n={summary["n"]})'
                             if summary['n'] else 'missing (n=0)')
            print(f'| {key} | {cells[0]} | {cells[1]} | {metric["blockSeparation"]} |')
    if args.json:
        args.json.write_text(json.dumps(output, indent=2) + '\n')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
