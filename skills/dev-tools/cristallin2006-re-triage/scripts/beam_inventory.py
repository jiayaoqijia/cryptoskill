#!/usr/bin/env python3
"""Read-only BEAM/IFF inventory and bounded, non-executing ETF subset reader."""
import argparse
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import struct
import zlib


class Unsupported(ValueError):
    pass


@dataclass
class Limits:
    max_input: int = 16 * 1024 * 1024
    max_unpacked: int = 32 * 1024 * 1024
    max_items: int = 20000
    max_nodes: int = 100000
    max_depth: int = 48
    max_preview: int = 256

    def __post_init__(self):
        if any(type(v) is not int or v <= 0 for v in vars(self).values()):
            raise ValueError('Parser limits must be positive integers')


def read_local(path, maximum):
    p = Path(path)
    if p.is_symlink():
        raise ValueError('Provide a regular file, not a symlink')
    fd = os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > maximum:
            raise ValueError('Input is not a bounded regular file')
        data = stream.read(maximum + 1)
        after = os.fstat(stream.fileno())
    identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if len(data) > maximum or len(data) != before.st_size or identity(before) != identity(after):
        raise ValueError('Input changed while reading or exceeds input limit')
    return data


class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 0

    def take(self, n):
        if n < 0 or n > len(self.data) - self.pos:
            raise ValueError('Truncated field at byte ' + str(self.pos))
        value = self.data[self.pos:self.pos + n]
        self.pos += n
        return value

    def number(self, n):
        return int.from_bytes(self.take(n), 'big')

    def end(self):
        if self.pos != len(self.data):
            raise ValueError('Unexpected trailing bytes')


def inflate(data, expected, maximum):
    if expected > maximum:
        raise ValueError('Declared decompressed size exceeds limit')
    decoder = zlib.decompressobj()
    raw = decoder.decompress(data, min(expected, maximum) + 1)
    if len(raw) != expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError('Invalid, oversized or non-exact compressed stream')
    return raw


def blob(data, limit, kind='binary'):
    preview = data[:limit]
    return {'type': kind, 'length': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'hex_preview': preview.hex(), 'preview_truncated': len(data) > limit}


class ETF(Reader):
    def __init__(self, data, limits, budget):
        super().__init__(data)
        self.limits, self.budget = limits, budget

    def count(self, n):
        if n > self.limits.max_items:
            raise ValueError('Collection count exceeds configured limit')
        return n

    def term(self, depth=0):
        self.budget[0] += 1
        if depth > self.limits.max_depth or self.budget[0] > self.limits.max_nodes:
            raise ValueError('ETF depth/node limit exceeded')
        tag = self.number(1)
        if tag == 97:
            return {'type': 'integer', 'decimal': str(self.number(1))}
        if tag == 98:
            return {'type': 'integer', 'decimal': str(int.from_bytes(self.take(4), 'big', signed=True))}
        if tag == 70:
            value = struct.unpack('>d', self.take(8))[0]
            if not math.isfinite(value):
                raise ValueError('Non-finite float')
            return {'type': 'float', 'value': value}
        if tag in (100, 115, 118, 119):
            n = self.number(1 if tag in (115, 119) else 2)
            raw = self.take(n)
            atom = raw.decode('utf-8' if tag in (118, 119) else 'latin1')
            if len(atom) > 255:
                raise ValueError('Atom exceeds character limit')
            return {'type': 'atom', 'value': atom}
        if tag == 106:
            return {'type': 'nil'}
        if tag in (104, 105, 108, 116):
            n = self.count(self.number(1 if tag == 104 else 4))
            if tag == 116:
                return {'type': 'map', 'pairs': [[self.term(depth + 1), self.term(depth + 1)] for _ in range(n)]}
            values = [self.term(depth + 1) for _ in range(n)]
            result = {'type': 'list' if tag == 108 else 'tuple', 'items': values}
            if tag == 108:
                result['tail'] = self.term(depth + 1)
            return result
        if tag in (107, 109):
            raw = self.take(self.number(2 if tag == 107 else 4))
            return blob(raw, self.limits.max_preview, 'byte_list' if tag == 107 else 'binary')
        if tag in (110, 111):
            n = self.number(1 if tag == 110 else 4)
            if n > self.limits.max_preview:
                raise Unsupported('Large integer retained as opaque ETF')
            sign = self.number(1)
            if sign not in (0, 1):
                raise ValueError('Invalid large integer sign')
            return {'type': 'integer', 'decimal': str(int.from_bytes(self.take(n), 'little') * (-1 if sign else 1))}
        raise Unsupported('Unsupported ETF tag ' + str(tag))

    def decode(self):
        if self.number(1) != 131:
            raise ValueError('Missing ETF version marker')
        result = self.term()
        self.end()
        return result


def inspect(data, limits=None):
    limits = limits or Limits()
    if len(data) > limits.max_input:
        raise ValueError('Input limit exceeded')
    r = Reader(data)
    if r.take(4) != b'FOR1' or r.number(4) != len(data) - 8 or r.take(4) != b'BEAM':
        raise ValueError('Not an exact BEAM FOR1 container')
    chunks, seen = [], set()
    while r.pos < len(data):
        if len(chunks) >= limits.max_items:
            raise ValueError('Chunk count exceeds configured limit')
        ident = r.take(4).decode('ascii')
        size, offset = r.number(4), r.pos
        raw = r.take(size)
        r.take((-size) % 4)
        if ident in seen:
            raise ValueError('Duplicate chunk ' + ident)
        seen.add(ident)
        chunks.append((ident, offset, raw))
    result = {'format': 'BEAM/IFF', 'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data),
              'container_valid': True, 'chunks': [{'id': i, 'file_offset': o, 'size': len(b)} for i, o, b in chunks],
              'atoms': [], 'imports': [], 'exports': [], 'locals': [], 'literals': [], 'issues': [],
              'debug_info': 'present_uninterpreted' if 'Dbgi' in seen else 'absent',
              'scope': 'static inventory; no module loading, opcode disassembly, source or route completeness proof'}
    atoms = []
    if 'Atom' in seen and 'AtU8' in seen:
        raise ValueError('Ambiguous atom tables')
    for ident, offset, raw in chunks:
        if ident not in ('Atom', 'AtU8'):
            continue
        if atoms:
            raise ValueError('Ambiguous atom tables')
        a = Reader(raw)
        count = a.number(4)
        if count > limits.max_items:
            raise ValueError('Unsupported atom format or atom count exceeds limit')
        for i in range(count):
            position = a.pos
            value = a.take(a.number(1)).decode('utf-8' if ident == 'AtU8' else 'latin1')
            atoms.append(value)
            result['atoms'].append({'index': i + 1, 'value': value, 'chunk': ident, 'file_offset': offset + position})
        a.end()
    def atom(index):
        if not 1 <= index <= len(atoms):
            raise ValueError('Invalid atom table index')
        return atoms[index - 1]
    budget = [0]
    for ident, offset, raw in chunks:
        if ident in ('ImpT', 'ExpT', 'LocT'):
            a = Reader(raw)
            count = a.number(4)
            if count > limits.max_items:
                raise ValueError('Import/export count exceeds limit')
            for i in range(count):
                position = a.pos
                x, y, z = a.number(4), a.number(4), a.number(4)
                item = {'index': i, 'file_offset': offset + position}
                if ident == 'ImpT':
                    item.update(module=atom(x), function=atom(y), arity=z)
                else:
                    item.update(function=atom(x), arity=y, label=z)
                result[{'ImpT': 'imports', 'ExpT': 'exports', 'LocT': 'locals'}[ident]].append(item)
            a.end()
        elif ident == 'LitT':
            a = Reader(inflate(raw[4:], Reader(raw).number(4), limits.max_unpacked))
            count = a.number(4)
            if count > limits.max_items:
                raise ValueError('Literal count exceeds limit')
            for i in range(count):
                position, size = a.pos, a.number(4)
                term = a.take(size)
                item = {'index': i, 'chunk': 'LitT', 'compressed_chunk_file_offset': offset,
                        'decompressed_entry_offset': position, 'size': size, 'sha256': hashlib.sha256(term).hexdigest()}
                try:
                    item.update(state='decoded_subset', value=ETF(term, limits, budget).decode())
                except Unsupported as e:
                    item.update(state='unsupported', reason=str(e))
                result['literals'].append(item)
            a.end()
    result['literal_coverage'] = {'decoded': sum(v['state'] == 'decoded_subset' for v in result['literals']),
                                  'unsupported': sum(v['state'] == 'unsupported' for v in result['literals'])}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file')
    for key, value in vars(Limits()).items():
        parser.add_argument('--' + key.replace('_', '-'), type=int, default=value)
    args = parser.parse_args()
    try:
        limits = Limits(**{k: getattr(args, k) for k in vars(Limits())})
        value = inspect(read_local(args.file, limits.max_input), limits)
        print(json.dumps({'ok': True, **value}, ensure_ascii=True))
        return 0
    except (ValueError, OSError, zlib.error, OverflowError) as e:
        print(json.dumps({'ok': False, 'error': str(e), 'scope': 'static parsing only'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
