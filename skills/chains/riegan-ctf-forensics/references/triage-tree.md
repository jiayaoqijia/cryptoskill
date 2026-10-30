# Triage tree — every artifact starts here

Per-artifact decision tree. Run the "always" block first, then follow the node
matching the real type. Commands assume the challenge dir layout from the `ctf`
router skill (`dist/`, `solve/`, `notes.md`).

## Always run (any artifact, ~90 seconds)

```bash
f=dist/blob.bin
file "$f"                                  # real type; compare vs extension
xxd "$f" | head -20                        # header: magic, version fields
xxd "$f" | tail -20                        # trailer: appended data, padding
exiftool "$f"                              # metadata: comment, author, GPS, history
strings -n 8 "$f" | grep -aiE 'flag|ctf\{|key|passw|secret|http' | head -40
binwalk "$f"                               # embedded signatures at offsets
binwalk -E "$f"                            # entropy plot (PNG written to cwd)
```

Reading the entropy plot: sustained ~8.0 blocks = compressed or encrypted
payload (zip/gzip/squashfs at the same offset = archive; nothing known there =
crypto or deliberate padding). ~0–3 regions = text/code. A sharp step at one
offset is the boundary between two glued files.

Entropy caveat: `binwalk -E` conflicts with `-e` (v3) — run separately.

## Node: image (PNG / JPEG / GIF / BMP / TIFF / WebP)

1. `file` mismatch or extension lying? Rename to real type before tools.
2. `exiftool -a -u -g1 img.jpg` — comment/artist fields, GPS, software.
3. Size vs expected: is the file far larger than the pixels need? → appended
   data (below). PNG whose `file` output says "palette" → palette tricks.
4. Go to `stego.md#images`.

## Node: audio (WAV / MP3 / FLAC / OGG)

1. `ffprobe file.mp3` (or exiftool) — codec, duration, bitrate; unusual
   duration vs file size = hidden stream.
2. Spectrogram first — most audio CTFs hide text there:
   `sox in.wav -n spectrogram -o spec.png` (mp3: `ffmpeg -i in.mp3 t.wav`
   first).
3. Go to `stego.md#audio`.

## Node: video (MP4 / AVI / WEBM / MOV)

1. `ffprobe -v error -show_format -show_streams v.mp4` — streams count;
   multiple video/audio/subtitle tracks = hidden track.
2. Extract everything, then frame-diff: `stego.md#video`.

## Node: document (PDF / DOC / DOCX / XLS / XLSX)

1. `file` — OLE2 (CFB, `\xd0\xcf\x11\xe0`) vs ZIP-based OOXML vs PDF.
2. Strings + `binwalk` on it: OLE-in-PDF embeds show up as CFB magic at an
   offset.
3. Go to `disk-docs.md#documents` (macros, hidden text/sheets, PDF streams).

## Node: archive (ZIP / 7Z / RAR / GZ / TAR)

1. `7z l a.zip` — names, sizes; same file at several depths = nesting chain.
2. `7z t a.zip` — corrupt? → carve (below) or repair (`zip -FF a.zip --out
   fixed.zip`).
3. Password: try `strings`/`exiftool` hints, archive comment
   (`7z l -slt a.zip`, `unzip -z a.zip`), then ziplist → `ctf-crypto` for the
   actual crack (john/zip2john or hashcat) — that skill owns it.
4. Nested archives: extract each layer into its own subdirectory, never the
   same dir (filename collisions overwrite evidence).

## Node: pcap / pcapng

1. `capinfos -u -a -e -d c.pcap` — capture window, interfaces, packet count.
2. `scripts/pcap-triage.sh c.pcap` — phs/conversations/http/objects/streams.
3. Go to `pcap.md`.

## Node: memory dump (RAW / .mem / .vmem / .dmp / .lime / .vmemx)

1. `strings -n 8 d.raw | grep -aE 'Windows|Linux version' | head` — guest OS
   and build (picks the volatility symbol table).
2. Go to `memory.md`.

## Node: disk image (DD / RAW / E01 / VMDK / VDI)

1. `mmls -B d.dd` — partition map with sector offsets; DOS vs GPT vs none.
2. `binwalk d.dd` — firmware-style images often carry squashfs/cramfs.
3. Go to `disk-docs.md`.

## Node: unknown blob ("data")

Work the signature trail:

```bash
xxd -l 64 blob | head                      # no known magic? try reversal:
xxd blob | tail -5                         # trailing magic = reversed file
binwalk blob                               # any embedded signature
strings -n 12 blob | head -50              # structure hints (paths, XML, JSON)
```

| Symptom | Likely | Move |
|---|---|---|
| High entropy everywhere, no signatures | encrypted or base64/hex layer | try `base64 -d`, `xxd -r -p`; else `ctf-crypto` |
| `ELF`/`MZ` inside at offset | executable appended/embedded | carve below, then `ctf-rev` |
| `hsqs`/`sqsh`/`ustar`/`JFFS` inside | filesystem blob | carve + mount/extract |
| Readable SQL text (`SQLite format 3` at 0) | sqlite db | `sqlite3 f.db .tables` |
| `\xd0\xcf\x11\xe0` at offset | OLE/CFB inside | carve, `olevba`/`7z x` |
| Only `\x00\x20-\x7e` bytes | encoded text | encoding analysis, `ctf-crypto` |

## Containers within containers (the classic forensics trick)

Challenge files hide a second file inside a carrier. Find the seam, carve, then
repeat triage on the carve — the inner artifact gets the full treatment again.

### Zip appended after image EOF markers

PNG ends at the `IEND` chunk; JPEG at `\xff\xd9`. Anything after is payload:

```bash
f=img.png
# PNG: 4-byte length + "IEND" + 4-byte CRC = 12 bytes for the IEND chunk
off=$(python3 - "$f" <<'EOF'
import sys
d = open(sys.argv[1],'rb').read()
i = d.find(b'IEND')
print(i + 8 if i > 0 else -1)   # IEND type at i, +4 CRC -> end at i+8
EOF
)
dd if="$f" of=tail.bin bs=1 skip="$off" 2>/dev/null; file tail.bin
```

`binwalk` reports the same offset ("Zip archive" after PNG); `-e` extracts it.
For JPEG: `off=$(grep -abo $'\xff\xd9' "$f" | head -1 | cut -d: -f1)` then skip
`off+2`.

### Squashfs / CPIO / firmware blobs

```bash
binwalk fw.bin                     # "Squashfs filesystem, ..., compression: xz/lzma"
binwalk -Me fw.bin                 # extract recursively (squashfs-tools installed)
# manual: dd from the reported offset, then
unsquashfs squashfs.bin            # -> squashfs-root/
```

v3 note (Arch ships binwalk 3.x): `-e` extract, `-M` recursive, `-C <dir>`
output dir, `-E` entropy. v2 flags like `--dd` do not exist.

### OLE/CFB embedded in a PDF

PDF streams can carry any bytes. `binwalk f.pdf` shows `Microsoft Office`
signature at an offset; carve with dd, then `olevba` on the carve. Also run
`qpdf --qdf --object-streams=disable f.pdf flat.pdf` and grep the flat PDF for
`/EmbeddedFile`, `/JavaScript`, `/OpenAction` (`disk-docs.md#pdf`).

### Nested / renamed archives

Extension lies constantly: `file` first, extract per layer into fresh dirs:

```bash
7z x outer.zip -oouter/ && file outer/*   # inner "image" is really 7z?
```

## Manual carving (any signature, any carrier)

```bash
# 1. find offset(s) of a magic string (choose from table below)
grep -abo $'PK\x03\x04' blob.bin          # zip local file header
grep -abo $'7z\xbc\xaf\x27\x1c' blob.bin   # 7z
# 2. carve from offset (skip_bytes makes skip absolute regardless of bs)
dd if=blob.bin of=carved.zip bs=1M iflag=skip_bytes skip=$OFF 2>/dev/null
# 3. or let binwalk/foremost do it: binwalk -e blob.bin ; foremost -i blob.bin -o carve/
```

`dd iflag=skip_bytes` needs coreutils (present). `foremost -o` requires a
non-existent output dir.

### Common magics

| Bytes (ASCII/hex) | Format |
|---|---|
| `\x89PNG\r\n\x1a\n` / `IEND` | PNG start / end |
| `\xff\xd8\xff` / `\xff\xd9` | JPEG start / end |
| `PK\x03\x04` / `PK\x05\x06` | zip file entry / end of central dir |
| `7z\xbc\xaf\x27\x1c` | 7z |
| `Rar!\x1a\x07` | RAR |
| `\x1f\x8b` | gzip |
| `BZh` | bzip2 |
| `hsqs` / `sqsh` | squashfs LE / BE |
| `\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1` | OLE2/CFB (doc, xls, msi) |
| `%PDF-` | PDF |
| `\x00\x01\x00\x00` | TTF; `OTTO` = OpenType |
| `SQLite format 3\x00` | sqlite |
| `MDMP` | minidump |
| `\x7fELF` / `MZ\x90\x00\x03` | ELF / Windows PE (carved binary -> `ctf-rev`) |

## When stuck

1. Re-run `file` on every carve; loops hide one more layer than expected.
2. Hexdump the exact suspicious region, not the whole file:
   `xxd -s $OFF -l 256 blob`.
3. Compare lengths: `ls -l` vs sum of parts — unexplained bytes = padding or a
   third layer.
4. Byte-frequency histogram (python, stdlib) — bimodal = two files glued;
   flat 1/256 = encryption/compression.
5. Wrong skill? XOR/ciphers → `ctf-crypto`; binaries → `ctf-rev`;
   the flag regex and submission → `ctf` router.
