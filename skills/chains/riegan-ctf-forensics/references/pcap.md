# pcap analysis — tshark first, GUI only for screenshots

Install: `sudo pacman -S wireshark-cli` (provides tshark, capinfos, editcap;
the GUI is a separate `wireshark` package). One-shot triage:
`scripts/pcap-triage.sh cap.pcap`.

## First pass — shape of the capture

```bash
capinfos -u -a -e -d -c cap.pcap          # window, duration, packet count
tshark -r cap.pcap -q -z io,phs           # protocol hierarchy: what's inside
tshark -r cap.pcap -q -z conv,ip          # who talks to whom, bytes
tshark -r cap.pcap -q -z conv,tcp         # per-TCP-conversation
tshark -r cap.pcap -q -z conv,udp         # DNS/quic look different here
tshark -r cap.pcap -t ad                  # absolute timestamps, eyeball timeline
```

`-z io,phs` is the map: weird protocol on top (ftp, irc, telnet, smb, dns
larger than http) = the challenge. A protocol with massive byte counts but few
packets suggests exfil.

## Display filter cheat sheet

| Goal | Filter |
|---|---|
| HTTP requests | `http.request` |
| HTTP status | `http.response.code >= 400` |
| FTP control | `ftp.request.command == "USER" \|\| ftp.request.command == "PASS"` |
| DNS queries | `dns` / `dns.qry.type == 1` |
| Flag substring anywhere | `frame contains "flag"` (also try `flag{`, `CTF`, `secret`) |
| USB HID payloads | `usb.capdata \|\| usbhid.data` |
| ICMP (exfil channel) | `icmp` |
| IRC | `irc` |
| mail | `smtp \|\| imf` |
| TLS handshakes | `tls.handshake.type == 1` (client hello, SNI names) |
| WiFi probes | `wlan.fc.type_subtype == 4` |
| EAPOL (handshakes) | `eapol` |

Field extraction pattern:
`tshark -r cap.pcap -Y <filter> -T fields -e <field1> -e <field2> | sort | uniq -c | sort -rn`

## Streams

```bash
tshark -r cap.pcap -T fields -e tcp.stream | sort -un     # stream indexes
tshark -r cap.pcap -q -z follow,tcp,ascii,0               # stream 0, both dirs
tshark -r cap.pcap -q -z follow,udp,ascii,3               # udp stream 3
```

The follow dump marks directions (`>` client, `<` server). Scan followed text
for credentials and flags; for HTTP bodies the reassembled view beats raw
packets:

```bash
tshark -r cap.pcap -Y http -T fields -e http.file_data     # decoded bodies
```

Chunked/gzip transfers reassemble automatically in `http.file_data` and in
follow streams — raw packet hex looks broken, follow won't.

## Export objects (files that crossed the wire)

```bash
tshark -r cap.pcap --export-objects http,extracted/        # GET/POST bodies
tshark -r cap.pcap --export-objects imf,extracted/         # mail attachments
tshark -r cap.pcap --export-objects smb,extracted/         # SMB2 transfers
tshark -r cap.pcap --export-objects ftp,extracted/
tshark -r cap.pcap --export-objects tftp,extracted/
```

Output dir must exist. `file` everything afterwards — extensions are guessed
from content-type and lie.

## HTTP specifics

```bash
# request summary: who fetched what
tshark -r cap.pcap -Y http.request -T fields \
  -e frame.number -e http.request.method -e http.host -e http.request.uri \
  -e http.user_agent

# form logins (POSTs)
tshark -r cap.pcap -Y 'http.request.method == "POST"' -T fields \
  -e urlencoded-form.key -e urlencoded-form.value

# basic auth (base64 user:pass in header)
tshark -r cap.pcap -Y http.authorization -T fields -e http.authorization
echo 'dXNlcjpwYXNz' | base64 -d                            # decode each value

# file uploads: multipart boundaries -> carve from follow dump
tshark -r cap.pcap -q -z follow,tcp,ascii,N | grep -a filename
```

## Credentials by protocol

| Protocol | Extraction |
|---|---|
| FTP | `-Y ftp.request.command -T fields -e ftp.request.command -e ftp.request.arg` (USER/PASS in clear) |
| HTTP basic | `http.authorization` → `base64 -d` |
| IRC | `tshark -r c.pcap -Y irc -T fields -e irc.request`; or follow the TCP stream — NICK/PRIVMSG show passwords and bot commands |
| telnet/pop/imap | follow the stream; everything is cleartext |

## DNS exfiltration

Data rides in subdomain labels of queries to one authoritative NS.

```bash
tshark -r cap.pcap -Y 'dns.flags.response == 0' -T fields -e dns.qry.name | sort -u
```

Signs: many unique `<chunk>.tld` names under a fixed domain, labels of fixed
length, alphabet = base32/base64/hex. Reassemble:

```bash
# labels like 6d7367... .evil.com -> hex, or JBSWY... -> base32
tshark -r cap.pcap -Y 'dns.qry.name contains "evil.com"' -T fields -e dns.qry.name \
  | cut -d. -f1 | sort | tr -d '\n' | xxd -r -p    # hex variant
# base32 variant: ... | cut -d. -f1 | sort | tr -d '\n' | base32 -d
```

Ordering: if chunks carry a sequence index, sort by it, not lexically.
TXT-record exfil: `-e dns.txt`.

## ICMP exfiltration

Payload sits in the ICMP echo data:

```bash
tshark -r cap.pcap -Y icmp -T fields -e icmp.type -e data.data | head -40
# data.data is hex; identifier/seq often carry chunk counters:
tshark -r cap.pcap -Y icmp -T fields -e icmp.ident -e icmp.seq
```

If `data.data` stays empty, the payload dissects differently: dump with
`-x` and parse the raw hex column manually.

## USB — keystroke recovery

Classic hardware-in-a-pcap: `usb.capdata` (or `usbhid.data`) holds HID
reports.

```bash
tshark -r cap.pcap -Y 'usb.capdata' -T fields -e usb.capdata | head
# 00:00:04:00:00:00:00:00  <- 8-byte boot-protocol report
# or short reports: 00:04  (modifier, keycode)
```

Decode (standard US layout): byte 0 = modifier bitmask (`0x01` LCtrl,
`0x02` LShift, `0x04` LAlt, `0x20` RShift), byte 1 reserved, bytes 2-7 =
simultaneously-held keys.

| HID code | Key | HID code | Key | HID code | Key |
|---|---|---|---|---|---|
| 0x04-0x1d | a-z | 0x28 | Enter | 0x36 | `,` `<` |
| 0x1e-0x27 | `1234567890` | 0x29 | Esc | 0x37 | `.` `>` |
| 0x1e-0x27 +shift | `!@#$%^&*()` | 0x2a | Backspace | 0x38 | `/` `?` |
| 0x2c | Space | 0x2d | `-` `_` | 0x2e | `=` `+` |
| 0x2f | `[` `{` | 0x30 | `]` `}` | 0x31 | `\` `\|` |
| 0x33 | `;` `:` | 0x34 | `'` `"` | 0x39 | CapsLock |

```bash
scripts/ctf python - <<'EOF'
import subprocess
rows = subprocess.run(['tshark','-r','cap.pcap','-Y','usb.capdata',
                       '-T','fields','-e','usb.capdata'],
                      capture_output=True, text=True).stdout.split()
LOWER = {0x04+i: chr(97+i) for i in range(26)}
LOWER.update({0x1e+i: '1234567890'[i] for i in range(10)})
LOWER.update({0x28:'\n',0x29:'<Esc>',0x2a:'<BS>',0x2b:'\t',0x2c:' ',
              0x2d:'-',0x2e:'=',0x2f:'[',0x30:']',0x31:'\\',0x33:';',
              0x34:"'",0x36:',',0x37:'.',0x38:'/'})
UPPER = {k: v.upper() if len(v) == 1 else {'-':'_','=':'+','[':'{',']':'}',
          '\\':'|',';':':',"'":'"',',':'<','.':'>','/':'?'}.get(v,v)
         for k, v in LOWER.items()}
for row in rows:
    b = bytes.fromhex(row.replace(':',''))
    # 8-byte boot report: [mod, reserved, k1..k6]. Some 2-byte captures are
    # [key, mod] instead — if output looks wrong, use mod, keys = b[1], b[0:1]
    mod, keys = (b[0], b[2:]) if len(b) >= 3 else (b[0], b[1:2])
    shift = bool(mod & 0x22)
    for k in keys:
        if k:
            print((UPPER if shift else LOWER).get(k, f'[{k:02x}]'), end='')
print()
EOF
```

Mouse variant: report `[btn, dx, dy]` — accumulate dx/dy between button-down
events and plot the points (pillow) to redraw the drawn path; flags hide as
mouse drawings. USB mass storage: `-Y usb.bulk` + `-z conv,usb`.

## TLS decryption (keys provided by the challenge)

```bash
tshark -r cap.pcap -o tls.keylog_file:keys.log -Y http -T fields \
  -e http.host -e http.request.uri
```

The keylog is the text file from the challenge (`CLIENT_RANDOM ...` lines).
Without it TLS content stays sealed — pivot to SNI
(`-e tls.handshake.extensions_server_name`) and DNS.

## WiFi captures

```bash
tshark -r w.pcap -Y 'wlan.fc.type_subtype == 4' -T fields -e wlan.ssid   # probes
tshark -r w.pcap -Y 'wlan.fc.type_subtype == 8' -T fields -e wlan.ssid   # beacons
tshark -r w.pcap -Y eapol | wc -l       # 4+ = full handshake present
```

Handshake + wordlist → cracking belongs to `ctf-crypto` (hashcat mode 22000;
aircrack-ng is also in the official repos). Deauth isn't CTF-forensics.
Bluetooth (HCI) captures are rare: try `-Y bthci_acl`, else plain `strings`
on the capture.

## Slicing big captures

```bash
editcap -c 100000 cap.pcap part.pcapng            # split by packet count
tshark -r cap.pcap -Y 'frame.time >= "2026-10-30 10:00:00"' -w slice.pcap
tshark -r cap.pcap -Y 'ip.addr == 10.0.0.5' -w host.pcap   # focus one host
mergecap part_*.pcapng > joined.pcapng
```

## Workflow order (per capture)

1. `pcap-triage.sh` (phs, convs, http summary, objects, streams, flag grep).
2. Read the protocol hierarchy — pick the unusual protocol.
3. Export objects; `file` everything.
4. Follow the interesting streams (indexes from step 1's streams dump).
5. Exfil patterns: DNS labels / ICMP data / long POSTs.
6. Credentials found → try them on other artifacts (archives, steghide).
