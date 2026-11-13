"""tree_hash.py: the content-hash for an audit evidence card (audit-skill.md stage 7).

Usage: python3 tree_hash.py <dir>   -> prints one sha256 hex digest.

For each entry, sorted by relative path (POSIX '/' separators), the digest takes
    relpath + "\\0" + type + "\\0" + str(size) + "\\0" + bytes
where type is "f" (regular file: bytes = file contents) or "l" (symlink: bytes =
the link target string, never followed). Dotfiles and `.git/` are
included (hash what you copy). The path and size framing means moving bytes between files, or
renaming a file, changes the hash. Stdlib only; exit 2 on usage or read error, or on
any entry that is neither a regular file nor a symlink (FIFO, socket, device).
"""
import hashlib
import os
import sys


def entries(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        keep = []
        for d in dirnames:
            p = os.path.join(dirpath, d)
            if os.path.islink(p):
                filenames.append(d)  # symlinked dir: hash its target, never follow
            else:
                keep.append(d)
        dirnames[:] = keep
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            out.append((rel, p))
    return sorted(out)


def tree_hash(root):
    h = hashlib.sha256()
    for rel, p in entries(root):
        if os.path.islink(p):
            kind, data = b"l", os.readlink(p).encode("utf-8", "surrogateescape")
        else:
            if not os.path.isfile(p):
                raise OSError("not a regular file: %s" % rel)
            kind = b"f"
            with open(p, "rb") as f:
                data = f.read()
        h.update(rel.encode("utf-8", "surrogateescape") + b"\0" + kind + b"\0"
                 + str(len(data)).encode() + b"\0" + data)
    return h.hexdigest()


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print("usage: python3 tree_hash.py <dir>")
        return 2
    try:
        print(tree_hash(os.path.abspath(sys.argv[1])))
    except OSError as e:
        print("ERROR: %s" % e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
