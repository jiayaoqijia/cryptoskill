# Stego — images, audio, video, embedded payloads

Rule one: know the carrier format before touching a tool. Wrong tool on wrong
format wastes an hour (steghide on PNG does nothing; zsteg on JPEG does
nothing). Triage first (`triage-tree.md`), then use the matching section.

## Images

### Carrier → tool matrix

| Carrier | First tool | Then | Why |
|---|---|---|---|
| PNG | `zsteg -a f.png` | `scripts/lub.py`, bit planes | lossless → pixel LSB works |
| BMP | `zsteg -a f.bmp` | `scripts/lub.py` | same, uncompressed |
| JPEG | `steghide extract -sf f.jpg -p ""` | stegseek, outguess, exiftool, EOI-append | lossy → DCT/embedded tools, not pixel LSB |
| GIF | frame diff | exiftool, palette | 256-color palette tricks |
| TIFF/WebP | convert: `ffmpeg -i f.webp f.png` | re-run PNG path | tools don't read them directly |
| any | `exiftool -a -u -g1 f` | strings, binwalk | metadata/appended data first — cheapest win |

### PNG/BMP LSB — zsteg

```bash
zsteg -a img.png                 # try all known methods (b1..b8, all channels)
zsteg img.png 2b,b,lsb,xy        # param shortcut: 2 bits, blue, LSB, order xy
zsteg img.png -b 1-3 -c rgba --lsb -o yx    # explicit
zsteg img.png -E '1b,rgb,lsb,xy' > out.bin  # extract a found payload
```

Read the output: `b1,rgb,lsb,xy .. text: "..."` means 1 bit per sample, RGB
channels, LSB first, row-major; `b2,g,lsb,xy .. file: PNG image` means bit 2 of
green is a nested file — extract it. `zsteg -l 0` removes the 256-byte scan
limit for long payloads.

Install: `gem install zsteg` (ruby). No ruby / want scripting? Use
`scripts/lub.py`:

```bash
scripts/ctf python skills/ctf-forensics/scripts/lub.py img.png          # scan printable runs
scripts/ctf python skills/ctf-forensics/scripts/lub.py img.png --bits 2 --channels rgba
scripts/ctf python skills/ctf-forensics/scripts/lub.py img.png --raw stream.bin
scripts/ctf python skills/ctf-forensics/scripts/lub.py img.png --plane 0 --out plane0.png
```

### PNG structure corruption (IHDR lies)

`file` says PNG but viewers crop or refuse: the IHDR width/height is usually
tampered and the CRC no longer matches. Fix: patch dims and recompute CRC.

```python
#!/usr/bin/env python3
# fix-ihdr.py <in.png> <width> <height> <out.png>
import struct, sys, zlib
d = bytearray(open(sys.argv[1], 'rb').read())
w, h = int(sys.argv[2]), int(sys.argv[3])
struct.pack_into('>II', d, 16, w, h)          # IHDR data starts at offset 16
crc = zlib.crc32(d[12:29]) & 0xffffffff       # chunk type (12) .. end of data (29)
struct.pack_into('>I', d, 29, crc)
open(sys.argv[4], 'wb').write(d)
```

Get real dims first: bytes 16-23 hold width/height (big-endian); the true
height is often visible in a hexdump of IDAT size, or just try tall values
(e.g. original height × 2). Data hidden below the declared bottom row appears
once height grows. Other PNG header checks by hand: `IHDR` at offset 12,
chunks `tEXt`/`zTXt`/`iTXt` (exiftool shows these; `zTXt` is zlib-compressed
text — decompress the payload).

### JPEG

1. **Metadata**: `exiftool -a -u -g1 f.jpg` — Comment, Artist, UserComment,
   GPS (`GPS Position` → paste into maps), embedded thumbnail larger than the
   image.
2. **Appended after EOI**: `binwalk f.jpg`, or
   `off=$(grep -abo $'\xff\xd9' f.jpg | head -1 | cut -d: -f1)` then dd from
   `off+2` (`triage-tree.md` manual carving).
3. **steghide** (AUR): always empty password first — half of CTF steghide
   carries none:
   ```bash
   steghide info f.jpg                       # does it contain anything?
   steghide extract -sf f.jpg -p ''          # empty password
   steghide extract -sf f.jpg -p 'password'  # hinted password
   ```
   Carriers: JPEG, BMP, WAV, AU. Wrong password = "could not extract any data
   with that password".
4. **stegseek** (AUR) — steghide brute force, thousands/sec:
   ```bash
   stegseek f.jpg /path/to/wordlist          # hits print + auto-extract
   stegseek --seed f.jpg                     # brute the embedding seed instead
   ```
   No wordlist packaged on Arch — bring your own (rockyou from a mirror you
   trust, or a generated one from challenge hints).
5. **outguess** (AUR): `outguess -r f.jpg out.bin` (add `-k key` if hinted).
   Older challenge sets (jphide/outguess era) — try after steghide.
6. **stegdetect — honest note**: unmaintained since ~2004, tuned for
   jphide/outguess/F5 of that era, often false-positives on modern JPEGs.
   Don't install it for a modern challenge; go DCT-tool-hunting only when the
   challenge text or tags hint at it (F5, JSteg, JPHide — each needs its own
   extractor).

### GIF

- Frame tricks: `ffmpeg -i f.gif frame_%03d.png` then diff consecutive frames
  (see video section diff loop).
- Delay anomalies: `exiftool -Delay f.gif` — one frame with odd timing.
- Palette: `zsteg` on the GIF raw won't work; convert frames to PNG first.

### Bit-plane viewing (visual stego)

Some stego is only visible as an image in one bit plane (a faint watermark, a
QR code in plane 1-2).

- Local: `scripts/lub.py img.png --plane 1 --out p1.png` (bit set = black).
- Browser: StegOnline — <https://georgeom.net/StegOnline> — upload and flip
  through planes/channels. Fine for challenges; it's a third-party site, so no
  real-world evidence.
- Java classic: Stegsolve (`java -jar Stegsolve.jar`) — frame/plane browser;
  grab the jar from the author's distribution (search "Stegsolve.jar",
  java 21 runs it).

### Alpha / transparency channel

PNG alpha is a favorite 4th channel: `zsteg f.png -c a` and lub.py
`--channels rgba`. Visually invisible, LSB-visible.

## Audio

Convert to WAV first when the tool wants raw PCM: `ffmpeg -i in.mp3 t.wav`.

### Spectrogram (do this first)

```bash
sox t.wav -n spectrogram -o spec.png         # open spec.png, look at the image
sox t.wav -n spectrogram -z 100 -o spec.png  # more contrast (dB range)
```

Text/flags drawn into the frequency domain show up immediately. For
scrollable, per-band inspection use sonic-visualiser (`sudo pacman -S
sonic-visualiser`): Pane → Add Spectrogram. Hidden text at 17-20 kHz is
inaudible but visible.

### LSB in WAV

```python
import wave
w = wave.open('t.wav')
d = bytearray(w.readframes(w.getnframes()))
bits = (b & 1 for b in d)                    # LSB of every sample byte
out = bytearray()
acc = n = 0
for bit in bits:
    acc = (acc << 1) | bit; n += 1
    if n == 8: out.append(acc); acc = n = 0
open('lsb.bin','wb').write(out)              # then: file lsb.bin / strings lsb.bin
```

In Audacity/sonic-visualiser, LSB payloads look like a thin noise floor stuck
to the bottom of the spectrogram. Sample widths: 16-bit PCM hides in either
byte of each pair — try both (slice `d[::2]` and `d[1::2]`).

### DTMF / morse / modem tones

```bash
multimon-ng -a DTMF -t wav t.wav        # phone-keypad digits
multimon-ng -a MORSE_CW -t wav t.wav    # morse; finicky — verify by ear/spectrogram
```

DTMF → digits → could be a phone number or a numeric password. Morse by hand
when the demod fails: spectrogram + dot/dash table.

### SSTV (image transmitted as audio)

```bash
scripts/ctf sstv -d sstv.wav -o out.png     # sstv CLI (pip, in .venv)
```

Mode auto-detect covers Robot36, Martin, Scottie. GUI alternative with visual
tuning: qsstv (AUR). Frequencies usually 1500-2300 Hz; if decode is garbage,
check the spectrogram to confirm it is SSTV at all.

### Carrier-specific stego tools (know they exist)

- **MP3Stego** (Petitcolas, Windows binary): `decode -X -P pass file.mp3`
  under wine or a Windows VM. Rare, but the challenge saying "mp3stego" in
  metadata means exactly this.
- **DeepSound** (WAV/FLAC carrier, password-protected, Windows/Java GUI).
  If `file` shows a DeepSound header marker, run the official tool; no solid
  CLI clone exists — use podman with a windows container or ask for a VM.

## Video

```bash
ffprobe -v error -show_format -show_streams v.mp4   # stream inventory
ffmpeg -i v.mp4 -vf fps=1 frames/f_%04d.png         # mkdir frames first
ffmpeg -i v.mp4 -vn audio.wav                       # audio gets the audio path
ffmpeg -i v.mp4 -an -c copy silent.mp4              # strip audio, cheap re-check
exiftool v.mp4                                      # encoder, creation tags
```

- Frame diff (one changed frame hides a QR/text):
  ```bash
  scripts/ctf python - <<'EOF'
  import os
  from PIL import Image, ImageChops
  fs = sorted('frames/' + f for f in os.listdir('frames') if f.endswith('.png'))
  for a, b in zip(fs, fs[1:]):
      d = ImageChops.difference(Image.open(a).convert('RGB'),
                                Image.open(b).convert('RGB'))
      if d.getbbox():                                # None = identical
          print('differs:', a, b, d.getbbox())
  EOF
  ```
  `d.getbbox()` prints the changed rectangle — crop it
  (`im.crop(bbox).resize(...)`) if it's tiny.
- All-frames variant for short clips: `ffmpeg -i v.mp4 frames/f_%05d.png`.
- Subtitle/attachment streams: `ffmpeg -dump_attachment:v sub -i v.mkv` or
  `-map 0:s:0 sub.srt`.
- Metadata and EOF-append tricks are the same as images (binwalk, tail hex).

## Files containing archives

```bash
binwalk -e carrier              # v3: extract to ./extractions/
foremost -i carrier -o carve/   # signature carve (dir must not exist)
```

Manual path (`triage-tree.md`): `grep -abo $'PK\x03\x04' carrier` → dd from
offset → `7z l`/`7z x`. If the embedded zip is XOR-encoded or keyed, the
attack is key recovery, not forensics → `ctf-crypto` (crib `PK\x03\x04` /
`flag{` against repeated-key XOR).

## Priority order when nothing works

1. Re-check the carrier type with `file` — tools silently no-op on mismatches.
2. Metadata (exiftool) and appended data (binwalk + tail hex) — cheapest.
3. zsteg/lub full sweep, every channel and bit depth (PNG/BMP).
4. steghide empty password → stegseek wordlist → outguess (JPEG/WAV).
5. Visual bit planes (lub.py/StegOnline).
6. Spectrogram (audio) / frame diff (video).
7. Challenge text re-read: passwords are usually hinted, not brute-forced.
