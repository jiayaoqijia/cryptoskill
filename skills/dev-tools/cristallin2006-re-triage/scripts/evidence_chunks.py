#!/usr/bin/env python3
"""Assemble explicitly saved chunks; no network, retries or target execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def bounded(path, maximum):
    path = Path(path)
    if path.is_symlink():
        raise ValueError('Symlink input refused')
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > maximum:
            raise ValueError('Input must be a bounded regular file')
        data = stream.read(maximum + 1)
        after = os.fstat(stream.fileno())
    if len(data) > maximum or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
        raise ValueError('Input changed while reading')
    return data


def integer(value):
    if type(value) is not int or value < 0:
        raise ValueError('Sizes, generations and offsets must be nonnegative integers')
    return value


def sha(value):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
        raise ValueError('Expected lowercase SHA-256')
    return value


def context(value):
    if not isinstance(value, dict) or set(value) != {'identity', 'generation', 'version'}:
        raise ValueError('Source needs identity, generation and version (possibly null)')
    if not isinstance(value['identity'], str) or not value['identity']:
        raise ValueError('Source identity must be nonempty')
    integer(value['generation'])
    if value['version'] is not None and (not isinstance(value['version'], str) or not value['version']):
        raise ValueError('Source version must be a nonempty reference or null')
    return value


def assemble(manifest, root, max_size=64 * 1024 * 1024, max_chunks=20000, max_read=256 * 1024 * 1024):
    if any(type(n) is not int or n <= 0 for n in (max_size, max_chunks, max_read)):
        raise ValueError('Resource limits must be positive integers')
    if not isinstance(manifest, dict) or set(manifest) != {'version', 'source', 'size', 'source_sha256', 'chunks'} or type(manifest['version']) is not int or manifest['version'] != 1:
        raise ValueError('Expected version=1, source, size, source_sha256 and chunks')
    source, size = context(manifest['source']), integer(manifest['size'])
    expected = manifest['source_sha256']
    if expected is not None:
        sha(expected)
    if size > max_size or not isinstance(manifest['chunks'], list) or len(manifest['chunks']) > max_chunks:
        raise ValueError('Declared artifact or chunk count exceeds configured limit')
    root = Path(root).resolve(strict=True)
    data, covered, receipts = bytearray(size), bytearray(size), []
    conflicts, conflict_bytes, read_bytes = [], 0, 0
    for index, item in enumerate(manifest['chunks']):
        keys = {'offset', 'path', 'sha256', 'source', 'length', 'requested_length'}
        if not isinstance(item, dict) or set(item) != keys or context(item['source']) != source:
            raise ValueError('Chunk fields or source generation/version do not match')
        offset, length, requested = integer(item['offset']), integer(item['length']), integer(item['requested_length'])
        if length > requested or offset > size or length > size - offset:
            raise ValueError('Chunk length/offset exceeds request or artifact')
        relative = Path(item['path']) if isinstance(item['path'], str) else None
        if relative is None or relative.is_absolute() or '..' in relative.parts or not relative.parts:
            raise ValueError('Chunk path must stay within the manifest directory')
        path = root / relative
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError('Chunk path escapes manifest directory')
        raw = bounded(path, max_size)
        read_bytes += len(raw)
        if read_bytes > max_read:
            raise ValueError('Aggregate chunk input exceeds configured resource limit')
        if len(raw) != length or digest(raw) != sha(item['sha256']):
            raise ValueError('Chunk length/hash changed at entry ' + str(index))
        for position, byte in enumerate(raw, offset):
            if covered[position] and data[position] != byte:
                conflict_bytes += 1
                if len(conflicts) < 128:
                    conflicts.append(position)
            else:
                data[position], covered[position] = byte, 1
        receipts.append({'index': index, 'offset': offset, 'actual_length': length, 'requested_length': requested,
                         'short_read': length < requested, 'sha256': digest(raw)})
    missing = covered.count(0)
    gaps, cursor = [], 0
    while len(gaps) < 128:
        start = covered.find(b'\x00', cursor)
        if start < 0:
            break
        end = covered.find(b'\x01', start)
        end = size if end < 0 else end
        gaps.append([start, end])
        cursor = end
    complete = missing == 0 and conflict_bytes == 0
    local_hash = digest(data) if complete else None
    matches = local_hash == expected if complete and expected is not None else None
    valid = complete and matches is not False
    result = {'status': 'complete' if valid else 'invalid' if conflict_bytes or matches is False else 'incomplete',
              'complete': valid, 'size': size, 'missing_bytes': missing, 'gap_ranges': gaps,
              'gap_ranges_omitted': cursor < size and covered.find(b'\x00', cursor) >= 0,
              'conflict_observations': conflict_bytes, 'conflict_positions': conflicts,
              'conflict_positions_omitted': conflict_bytes > len(conflicts), 'chunks': receipts,
              'sha256': local_hash, 'matches_declared_source_digest': matches,
              'snapshot': 'caller_declared_version' if source['version'] is not None else 'unknown',
              'authority': 'local reconstruction against caller-provided identity/digest; no independently verified remote snapshot'}
    return result, bytes(data) if valid else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('--out', help='create a new artifact only if complete; never overwrite')
    parser.add_argument('--max-size', type=int, default=64 * 1024 * 1024)
    parser.add_argument('--max-chunks', type=int, default=20000)
    parser.add_argument('--max-read', type=int, default=256 * 1024 * 1024)
    parser.add_argument('--max-manifest', type=int, default=8 * 1024 * 1024)
    args = parser.parse_args()
    try:
        if args.max_manifest <= 0:
            raise ValueError('Manifest limit must be positive')
        path = Path(args.manifest)
        manifest = json.loads(bounded(path, args.max_manifest))
        value, body = assemble(manifest, path.parent, args.max_size, args.max_chunks, args.max_read)
        if args.out and body is not None:
            target = Path(args.out)
            fd, temporary = tempfile.mkstemp(prefix='.dsh-chunks-', dir=target.parent)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(body)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.link(temporary, target)
            finally:
                Path(temporary).unlink()
            value['written'] = True
        else:
            value['written'] = False
        print(json.dumps(value, ensure_ascii=True))
        return 0 if value['complete'] else 2
    except (OSError, ValueError, TypeError) as e:
        print(json.dumps({'status': 'invalid', 'complete': False, 'written': False, 'error': str(e)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
