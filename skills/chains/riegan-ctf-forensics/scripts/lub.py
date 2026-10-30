#!/usr/bin/env python3
"""lub.py — LSB stego triage for images (PNG/BMP/TIFF, anything Pillow opens).

Default mode: extract the low --bits bits of the chosen channels, then report
printable-ASCII runs in the stream (how "flag hidden in LSB" payloads look).
--raw dumps the whole extracted stream for other tools; --plane renders one
bit plane as an image for visual stego.

Bit order convention: pixels row-major; channels in the order you pass them;
within each sample the low bits are taken LSB-first; the bit stream is
regrouped into bytes MSB-first (first extracted bit becomes the byte's high
bit). That is the common "b1,rgb,lsb,xy" layout — for exhaustive permutations
use zsteg.

Pillow is needed only when an image is actually analyzed:
    uv pip install --python .venv/bin/python pillow
(it is already part of this repo's .venv — run via scripts/ctf python lub.py)
"""
import argparse
import sys

CHANNELS = {"r": 0, "g": 1, "b": 2, "a": 3}
PRINTABLE = set(range(0x20, 0x7F)) | {0x09, 0x0A, 0x0D}


def die(msg, code=2):
    print(f"lub.py: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_channels(spec, has_alpha):
    if spec == "all":
        spec = "rgba" if has_alpha else "rgb"
    idx = []
    for ch in spec:
        if ch not in CHANNELS:
            die(f"bad channel '{ch}' (use r/g/b/a, rgb, rgba, bgr, all)")
        if ch == "a" and not has_alpha:
            die("image has no alpha channel; use --channels rgb")
        if CHANNELS[ch] not in idx:
            idx.append(CHANNELS[ch])
    return idx


def load_image(path):
    try:
        from PIL import Image
    except ImportError:
        die("Pillow is required: uv pip install --python .venv/bin/python pillow")
    try:
        im = Image.open(path)
    except (OSError, ValueError) as e:
        die(f"cannot open {path}: {e}")
    if im.mode == "P":
        print("# note: palette image converted to RGB; palette-index LSB is "
              "invisible to this tool — use zsteg on the original for that")
        im = im.convert("RGB")
    elif im.mode in ("RGBA", "LA", "PA"):
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    return im


def extracted_bytes(im, ch_idx, bits, max_bytes):
    """Low `bits` bits per selected sample, LSB-first, bytes MSB-first."""
    out = bytearray()
    acc = n = 0
    for px in im.getdata():
        for ci in ch_idx:
            s = px[ci]
            for k in range(bits):
                acc = (acc << 1) | ((s >> k) & 1)
                n += 1
                if n == 8:
                    out.append(acc)
                    acc = n = 0
                    if len(out) >= max_bytes:
                        return bytes(out)
    return bytes(out)


def printable_runs(data, min_run):
    runs, start = [], None
    for i, b in enumerate(data):
        if b in PRINTABLE:
            if start is None:
                start = i
        elif start is not None:
            if i - start >= min_run:
                runs.append((start, data[start:i]))
            start = None
    if start is not None and len(data) - start >= min_run:
        runs.append((start, data[start:]))
    return runs


def dump_plane(im, ch_idx, plane, out_path):
    from PIL import Image

    w, h = im.size
    data = [0 if ((px[ch_idx] >> plane) & 1) else 255 for px in im.getdata()]
    img = Image.new("L", (w, h))
    img.putdata(data)
    img.save(out_path)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="lub.py",
        description="LSB extractor / bit-plane dumper / printable-run scanner",
        epilog="examples:\n"
               "  lub.py img.png\n"
               "  lub.py img.png --bits 2 --channels rgba\n"
               "  lub.py img.png --raw stream.bin\n"
               "  lub.py img.png --plane 1 --out plane1.png\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("image", help="input image (PNG/BMP/... anything Pillow reads)")
    ap.add_argument("--bits", type=int, default=1, metavar="N",
                    help="low bits per sample (1-8, default 1)")
    ap.add_argument("--channels", default="rgb", metavar="SPEC",
                    help="channels: r/g/b/a/rgb/rgba/bgr/all (default rgb)")
    ap.add_argument("--min-run", type=int, default=6, metavar="N",
                    help="minimum printable run length (default 6)")
    ap.add_argument("--max-bytes", type=int, default=4 * 1024 * 1024,
                    help="extraction cap in bytes (default 4194304)")
    ap.add_argument("--raw", metavar="FILE",
                    help="write the full extracted stream to FILE")
    ap.add_argument("--plane", type=int, default=None, metavar="N",
                    help="render bit plane N (0=LSB..7=MSB) instead of scanning")
    ap.add_argument("--out", metavar="FILE",
                    help="output image for --plane (required with it)")
    args = ap.parse_args(argv)

    if not 1 <= args.bits <= 8:
        die("--bits must be 1-8")
    if args.plane is not None:
        if not 0 <= args.plane <= 7:
            die("--plane must be 0-7")
        if not args.out:
            die("--plane needs --out FILE")

    im = load_image(args.image)
    has_alpha = im.mode == "RGBA"
    ch_idx = parse_channels(args.channels, has_alpha)
    ch_names = "".join(k for k, v in CHANNELS.items() if v in ch_idx)
    print(f"# {args.image}: {im.size[0]}x{im.size[1]} {im.mode} "
          f"channels={ch_names} bits={args.bits}")

    if args.plane is not None:
        dump_plane(im, ch_idx, args.plane, args.out)
        print(f"# bit plane {args.plane} of channel '{ch_names[0]}' "
              f"written to {args.out} (set bit = black)")
        return

    data = extracted_bytes(im, ch_idx, args.bits, args.max_bytes)
    print(f"# extracted {len(data)} bytes (cap {args.max_bytes}); "
          f"head: {data[:32].hex(' ')}")

    if args.raw:
        with open(args.raw, "wb") as f:
            f.write(data)
        print(f"# raw stream written to {args.raw}")

    runs = printable_runs(data, args.min_run)
    print(f"# printable runs >= {args.min_run}: {len(runs)}")
    for off, run in runs[:80]:
        text = run.decode("ascii", "replace")
        if len(text) > 120:
            text = text[:117] + "..."
        print(f"{off:#08x}  len={len(run):<5d} {text!r}")
    if len(runs) > 80:
        print(f"# ... {len(runs) - 80} more runs")
    print("# tip: pipe to `file`-like checks — try --raw out.bin then "
          "`file out.bin`, `strings out.bin`, `xxd out.bin | head`")


if __name__ == "__main__":
    main()
