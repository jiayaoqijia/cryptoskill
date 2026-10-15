#!/usr/bin/env python3
"""Compatibility entrypoint; canonical implementation lives in runtime/analysis-v1/guarded_run.py."""
import os
from pathlib import Path
import runpy
import sys
_root = Path(os.environ.get('DSH_HOME', str(Path.home() / '.dsh')))
_target = _root / 'runtime/analysis-v1/guarded_run.py'
if not _target.is_file():
    raise RuntimeError('migration implementation missing: ' + str(_target))
sys.path.insert(0, str(_target.parent))
if __name__ == '__main__':
    runpy.run_path(str(_target), run_name='__main__')
else:
    globals().update({k: v for k, v in runpy.run_path(str(_target)).items() if not k.startswith('__')})
