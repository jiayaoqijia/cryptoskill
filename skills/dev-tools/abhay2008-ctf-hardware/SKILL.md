---
name: ctf-hardware
description: Provides hardware, firmware and embedded attack techniques for CTF challenges. Use when the challenge ships a firmware blob, router or IoT image, an ESP32/STM32/ARM/MIPS dump, a logic-analyzer capture (.sr, .sal, VCD), an SDR/IQ recording, a CAN bus log, a PCB photo with test pads, or asks for UART, JTAG, SWD, SPI flash, side-channel or fault-injection work. Also use when a flag is "in the device" and you must extract, reflash, sniff or emulate it. Do not use it for pure disk, memory or network forensics, or for ordinary binary exploitation with no hardware layer.
license: MIT
compatibility: Requires filesystem-based agent (Claude Code or similar) with bash, Python 3, and internet access. Physical hardware steps assume you have the device or a provided capture.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch Skill
metadata:
  user-invocable: "false"
---

# CTF Hardware & Firmware

Most "hardware" CTF challenges never need a soldering iron: they hand you a dump, a capture, or an IQ file. Decide which of those you have before touching a pinout.

## Scope and safety

Only work on hardware the challenge or the user owns. Do not connect to live production devices, and never reflash a device you cannot afford to brick. Keep dumps and scripts under `ctf-solver/workspaces/<challenge>/`.

## Step 1: Identify the artifact

| Artifact | Path |
|---|---|
| `firmware.bin`, `.img`, vendor update file | Firmware extraction |
| `.sr` / `.sal` / `.vcd`, `sigrok`/PulseView capture | Logic analysis |
| `.iq`, `.cf32`, `.cs16`, `.cu8`, `.wav` from SDR | SDR — see [../ctf-misc/rf-sdr.md](../ctf-misc/rf-sdr.md) |
| `.log`, `candump` output, DBC file | CAN bus |
| Photo of a board, "find the UART" | UART / JTAG |
| "power trace", CSV of samples, timing measurements | Side channel |
| `.elf` for ARM/MIPS/Xtensa, no hardware given | Firmware reversing — [../ctf-reverse/platforms.md](../ctf-reverse/platforms.md#embedded--iot-firmware-re) |

## Firmware extraction

```bash
file firmware.bin
binwalk firmware.bin                 # signatures first
binwalk -Me firmware.bin             # recursive extract (installed in the image)
unsquashfs -l squashfs-root.sqfs     # SquashFS listing
jefferson -d out jffs2.img           # JFFS2 (pip install jefferson)
ubidump ubi.img --extract-file       # UBI volumes (pip install ubidump)
7z x firmware.bin -oextracted        # catches many vendor containers
```

Then mine the filesystem, which is where the flag usually is:

```bash
grep -rniE 'flag|passwd|secret|token|admin' squashfs-root/etc 2>/dev/null | head
cat squashfs-root/etc/shadow            # crack weak hashes with hashcat -m 1800/500
cat squashfs-root/etc/init.d/*          # boot scripts reveal services and keys
find squashfs-root -name '*.conf' -o -name 'nvram*' -o -name '*.pem'
```

Watch for: encrypted or XOR-obfuscated sections (entropy near 8 means compressed or encrypted), a header with a key, `nvram` defaults containing Wi-Fi PSKs, and firmware that ships its own private key.

**Architecture check before emulating:**

```bash
readelf -h ./bin/busybox | grep -E 'Machine|Class|Data'
qemu-arm -L /usr/arm-linux-gnueabihf ./bin 2>/dev/null
qemu-mipsel -L /usr/mipsel-linux-gnu ./bin
```

`apt install qemu-user qemu-user-static gdb-multiarch` gives you the cross-arch path. The container currently has **no qemu at all** (`binwalk` and `unsquashfs` are present), so install before planning an emulation step.

## UART

1. **Find the pads** — usually a 3- or 4-pin header near the SoC. GND is continuous with the shield/ground plane; VCC reads ~3.3 V. TX/RX are the remaining two.
2. **Sniff first, do not transmit.** Connect only GND and the pad that emits data at boot. A USB-TTL adapter at 3.3 V, never 5 V.
3. **Baud** — 115200 8N1 is the default on most routers; 57600 and 9600 are next. If you see garbage, try the neighbouring rates before rewiring.

```bash
ls /dev/tty.usbserial* /dev/ttyUSB*
picocom -b 115200 /dev/ttyUSB0        # Ctrl-A Ctrl-X to exit
screen /dev/ttyUSB0 115200
```

What you are looking for in the boot log: a U-Boot prompt (`=>`), a login prompt, or a shell. From U-Boot:

```
printenv
setenv bootargs 'console=ttyS0,115200 init=/bin/sh'
boot
```

A U-Boot prompt with `fatload`/`md` can also read raw flash without a shell. If the boot log prints the flag during init, you only needed the sniff.

## JTAG / SWD / SPI flash

```bash
openocd -f interface/ftdi/ft2232h.cfg -f target/stm32f1x.cfg
# in the openocd console:
#   halt; dump_image flash.bin 0x08000000 0x100000
```

- **SWD** (Cortex-M) needs SWDIO, SWCLK, GND, and often NRST — four wires, more reliable than JTAG on small boards.
- **SPI flash** in-circuit with a SOIC-8 clip and CH341A: `flashrom -p ch341a_spi -r dump.bin`, then `binwalk -Me dump.bin`. Read-only first; writing risks bricking.
- If the chip is read-protected, look for the flag in the bootloader's UART output or in a second, unprotected chip instead of attacking the lock bits.

## Logic analysis (sigrok / PulseView)

A `.sr` capture is usually SPI, I2C, or UART between an MCU and a peripheral.

```bash
sigrok-cli -i capture.sr -P uart:baudrate=115200:rx=D0 -A uart=rx_data
sigrok-cli -i capture.sr -P spi:cs=D0:clk=D1:mosi=D2:miso=D3 -A spi=mosi-data
sigrok-cli -i capture.sr -P i2c:scl=D0:sda=D1 -A i2c=data-read
sigrok-cli -d fx2lafw --config samplerate=1m --channels D0,D1 -o live.sr   # live capture
```

`sigrok-cli` is **not** installed in the container — `apt install sigrok-cli` (or use PulseView locally) before promising a decode. Practical order: guess the protocol from the channel count and clock regularity, decode with defaults, then adjust baud/polarity/bit order until the bytes look like ASCII. A flag written to an LCD or EEPROM shows up as a run of printable bytes in the decode.

## CAN bus

```bash
candump -L can0                    # log with timestamps
candump can0,7DF:7FF              # filter an ID range
cansend can0 123#DEADBEEF         # raw frame
python3 -c "import cantools; db=cantools.database.load_file('x.dbc'); print(db.messages)"
```

Look for a challenge that replays a "locked" frame: capture the unlock exchange, find the counter or checksum, and replay with the payload you want. `can-utils` is not in the container — install it, or parse the log text directly if the challenge only gives you `candump` output.

## Side channel and fault injection

- **Power/timing traces**: align traces, compute the Hamming weight of the key guess, correlate. For AES the standard target is the first S-box output; peak correlation at the right key byte beats noise.
- **Simple attacks first** — if the challenge prints timing for a comparison, it is usually a byte-by-byte oracle, not a real DPA.
- **Fault injection**: single-bit ROM flips (see [../ctf-reverse/platforms-hardware.md](../ctf-reverse/platforms-hardware.md) for the XOR-constant pattern), voltage glitches to skip an auth branch, and clock glitches to misread a compare. A `chipwhisperer`/`glitchkit` setup is only worth modelling when the challenge hands you measurements.

## Embedded reversing pointers

- ESP32/Xtensa with no IDA support: load the ESP-IDF ROM linker script in radare2 — [../ctf-reverse/patterns-ctf-3.md](../ctf-reverse/patterns-ctf-3.md#esp32xtensa-firmware-reversing-with-rom-symbol-map-insomnihack-2017)
- ARM/MIPS userland binaries: [../ctf-reverse/unicorn-emulation.md](../ctf-reverse/unicorn-emulation.md) for MMIO-heavy firmware
- UEFI and bootkits: [../ctf-reverse/languages.md](../ctf-reverse/languages.md)
- Android APK on a device: [../ctf-reverse/tools.md](../ctf-reverse/tools.md#android-apk)

## Common flag locations

- Firmware filesystem: `/etc/flag`, `/root/flag`, a config value, NVRAM defaults
- Raw flash at a fixed offset (`strings dump.bin | grep -i flag`)
- UART boot log, U-Boot environment, a shell after `init=/bin/sh`
- A decoded SPI/I2C/UART transaction headed for a display or EEPROM
- A demodulated SDR frame or a CAN payload

## When to pivot

- The dump is just a binary to reverse, no hardware semantics → `/ctf-reverse`
- The device exposes a network service you can attack → `/ctf-web` or `/ctf-pwn`
- The capture is audio (SSTV, Morse, DTMF) rather than digital → [../ctf-misc/audio.md](../ctf-misc/audio.md)
- The signal is RF modulation analysis (QAM/PSK, IQ formats) → [../ctf-misc/rf-sdr.md](../ctf-misc/rf-sdr.md)

## Verify

```bash
binwalk --help | head -3
command -v sigrok-cli picocom openocd flashrom ubidump jefferson
file firmware.bin && binwalk -Me firmware.bin
```

State plainly which steps you could not run because the tool or the hardware was absent — a firmware conclusion based on `strings` alone is a hypothesis, not a result.

## Saleae `.sal` captures (Logic 2)

- A `.sal` file is a zip of digital/analog captures. Open in Saleae Logic 2, or extract and decode with sigrok: `sigrok-cli -i capture.sal -P uart:baudrate=115200:rx=D0 -A uart=rx_data`. If sigrok is unavailable, unzip the `.sal` and parse the binary sample streams manually.
- Guess the protocol from channel count and clock regularity, decode with defaults, then adjust baud/polarity/bit order until the bytes look like ASCII. A flag written to an LCD or EEPROM shows up as a run of printable bytes.
