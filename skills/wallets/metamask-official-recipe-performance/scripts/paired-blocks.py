#!/usr/bin/env python3
"""Run alternating capture blocks; the caller supplies the screen adapter."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    parser.add_argument('rounds', type=int, help='timed opens per scenario per block')
    parser.add_argument('repeats', type=int, help='blocks per state, at least two')
    parser.add_argument('baseline', help='label:commit')
    parser.add_argument('candidate', help='label:commit')
    parser.add_argument('capture', type=Path, help='executable screen capture adapter')
    args = parser.parse_args()
    states = [value.split(':', 1) for value in (args.baseline, args.candidate)]
    if (args.rounds < 1 or args.repeats < 2 or any(len(s) != 2 or not all(s) for s in states)
            or states[0][0] == states[1][0]):
        parser.error('use positive rounds, at least two repeats and distinct label:commit states')
    capture = str(args.capture.resolve(strict=True))
    args.out.mkdir(parents=True, exist_ok=False)
    manifest = {'rounds': args.rounds, 'repeats': args.repeats, 'states': states, 'blocks': []}
    for repeat in range(1, args.repeats + 1):
        for arm, (state, ref) in enumerate(states):
            block = f'{"ab"[arm]}{repeat}'
            directory = (args.out / block).resolve()
            directory.mkdir()
            with (directory / 'capture.log').open('w') as log:
                result = subprocess.run([capture, state, ref, str(directory), str(args.rounds)],
                                        stdout=log, stderr=subprocess.STDOUT)
            row = {'block': block, 'state': state, 'requestedRef': ref,
                   'status': 'pass' if result.returncode == 0 else 'failed',
                   'exitCode': result.returncode}
            manifest['blocks'].append(row)
            (args.out / 'blocks.json').write_text(json.dumps(manifest, indent=2) + '\n')
            print(f'{block} {state} status={row["status"]}', flush=True)
            if result.returncode:
                return result.returncode
    return 0


if __name__ == '__main__':
    sys.exit(main())
