---
name: ctf-router
description: Routes any CTF challenge prompt in the CTF project to the right specialist skill and tools. Use whenever the user pastes a CTF challenge, flag-hunting request, a challenge file, a remote host/port, a CTF URL or CTFd link, or asks to solve, analyse, decode or exploit something for a capture-the-flag event. It classifies the challenge, checks the project's MCP servers (ctf-kali, stego, playwright) and browser tooling, routes HTTP/API-heavy challenges through the ctf-web ops loop first, picks the category skill (ctf-web, ctf-pwn, ctf-crypto, ctf-reverse, ctf-forensics, ctf-osint, ctf-malware, ctf-ai-ml, ctf-cloud, ctf-jail, ctf-hardware, ctf-misc) and hands off to solve-challenge for the full workflow. Do not use it for general (non-CTF) security questions or for building features in other projects.
license: MIT
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch Skill
metadata:
  user-invocable: "true"
  argument-hint: "[challenge description, file path, host:port or URL]"
---

# CTF Router (project dispatcher)

This project is set up for CTF work. Your job on a CTF prompt is to route it fast, not to solve it from memory. Work in this order and keep the chat short.

## Scope and safety

- Only attack targets the user names as CTF challenges, or infrastructure they own or are authorised to test. If the target is an unknown public host that is not a CTF, stop and ask.
- Do not run destructive actions against shared CTF infrastructure (no flooding, no brute force beyond the challenge's own hints, no persistence on shared boxes).
- Keep every artifact under the project: challenge work goes in `ctf-solver/workspaces/<challenge-name>/`. Create it if missing. Do not write outside the project.

## Step 0: Container contract (do this first)

All artifact work runs inside the `ctf-solver` container, never on the host:

```bash
scripts/ctf.sh status     # container + /health + tool probe
scripts/ctf.sh up         # create/recreate it, waits for /health
scripts/ctf.sh py scripts/stego/sweep.py <file>   # presets run on /opt/venv/bin/python
scripts/ctf.sh run nmap -sV <target>
```

For any image, audio, video or GIF file, run the stego preset **before** classifying further — it answers the standard checks without re-deriving them. Do not install tools on the host.

Ready-made media presets (in the container at `/app/presets`, files in `/app/workspaces`):

```bash
docker exec ctf-solver python3 /app/presets/frame_diff.py /app/workspaces/<chal>/<video-or-gif>   # video/GIF frame diffs
docker exec ctf-solver python3 /app/presets/lsb_extract.py /app/workspaces/<chal>/<image>           # image LSB streams
docker exec ctf-solver python3 /app/presets/qr_decode.py /app/workspaces/<chal>/<image>            # QR / barcode
docker exec ctf-solver python3 /app/presets/audio_spectrum.py /app/workspaces/<chal>/<audio>       # spectrogram + DTMF
docker exec ctf-solver python3 /app/presets/gif_frames.py /app/workspaces/<chal>/<gif> --x X --y Y --hi H --lo L
```

Run the matching preset, then `ctf-stego` (sweep) for anything they do not answer. Do not write a new extractor for a standard filter.

## Step 1: Classify (one pass, no deep dive)

Look at what the user gave you:

| Input | Likely category | First skill |
|---|---|---|
| `.pcap`, `.pcapng`, `.E01`, `.dd`, `.raw`, memory dump, disk image, `.evtx` | forensics | `/ctf-forensics` |
| `.mp4`, `.mkv`, `.avi`, `.webm`, `.mov` (video) | forensics (media) | `/ctf-forensics` Media Triage, then `stego` `video_*` tools |
| `.gif` (animated or not) | forensics (media) | `/ctf-forensics` Media Triage, then `stego` `gif_*` tools |
| `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a` (audio) | stego (hidden-in-audio) OR forensics (SSTV/Morse/DTMF/RF signal) | `/ctf-stego` first for LSB/spectrogram; if SSTV/Morse/DTMF/RF -> `/ctf-forensics` or `/ctf-misc` (audio.md, rf-sdr.md) |
| `.png`, `.jpg`, `.bmp`, `.webp` with no obvious content, "hidden", "stego", LSB, bit plane, palette, QR or barcode | stego | `/ctf-stego` (runs `scripts/stego/sweep.py` first) |
| `.pdf`, `.docx`, `.xlsx`, `.zip` with no obvious content | forensics (documents) | `/ctf-forensics` PDF Analysis, then `stego` `doc_*` / `file_*` tools |
| Unknown or generic binary (`file` says `data`, odd magic bytes, "find the flag" with no clear type) | forensics (carving) | `file *`, then `/ctf-forensics` (`binwalk`, `foremost`, `strings`) |
| `.elf`, `.exe`, `.so`, ELF with a `nc host port` service, "buffer overflow", "ROP", "heap" | pwn (or reverse first) | `/ctf-reverse` if you do not understand it, else `/ctf-pwn` |
| eBPF verifier, kernel module, KASLR, slab, seccomp | pwn | `/ctf-pwn` (kernel.md) |
| Solana/Firedancer or other blockchain VM, custom bytecode interpreter with memory bugs | pwn (understand-only -> reverse) | `/ctf-reverse` to characterize, then `/ctf-pwn` |
| `.py`/`.sage` with numbers, "RSA", "AES", "cipher", "prime", "lattice" | crypto | `/ctf-crypto` |
| URL, HTML/JS/PHP source, "XSS", "SQLi", "JWT", "SSTI", "SSRF", admin bot, "report URL" | web | `/ctf-web` |
| browser extension, service worker, CSP bypass, shadow DOM, iframe sandbox, DOM-extraction puzzle | web | `/ctf-web` (client-side advanced) |
| `.apk`, `.wasm`, `.pyc`, "obfuscated", "reverse" | reverse | `/ctf-reverse` |
| "jail", pyjail, restricted shell, `eval`/`exec` filter, "no quotes", `disable_functions` | jail | `/ctf-jail` |
| `kubeconfig`, SA token, `docker.sock`, IAM/S3/Lambda, `169.254.169.254`, "container escape" | cloud | `/ctf-cloud` |
| firmware blob, `.sr`/`.sal`/`.vcd` logic capture (Saleae/sigrok), UART/JTAG/SPI, CAN log, SDR/IQ for hardware | hardware | `/ctf-hardware` |
| "encoding", "esolang", "SDR" demod of an IQ file, "QR", constraint puzzle, game theory | misc | `/ctf-misc` |
| "find who", "where was this photo", usernames, locations | OSINT | `/ctf-osint`, then `/osint-ctf-databases` |
| `.safetensors`, `.pt`, `.onnx`, prompt injection, LoRA | AI/ML | `/ctf-ai-ml` |
| MCP server, AI agent with tools, tool-call injection, `file://` tool, agent tool abuse | AI/ML | `/ctf-ai-ml` (llm-attacks.md Tool Use) |
| C2 traffic, packed scripts, RAT artifacts | malware | `/ctf-malware` |

If several fit, pick the one that gets the first flag fastest and note the secondary category for pivoting.

## Step 2: Check the project's tools

The project already configures these MCP servers in `.agents/mcp.json`:

- **`ctf-kali`**: the local Kali server on `http://127.0.0.1:5055`. Confirm it is healthy with `curl -s http://127.0.0.1:5055/health` before relying on it; if it is down, use local shell tools and say so. Its tools by category:
  - Recon/web: `nmap_scan`, `gobuster_scan`, `dirb_scan`, `nikto_scan`, `sqlmap_scan`, `wpscan_analyze`, `enum4linux_scan`, `network_reconnaissance`, `web_application_testing`
  - Pwn/reverse: `checksec_binary`, `find_rop_gadgets`, `analyze_with_radare2`, `disassemble_binary`, `extract_strings`, `run_pwntools_exploit`, `start_interactive_shell`, `pwnable_challenge_workflow`, `reversing_challenge_workflow`
  - Crypto: `rsa_attack`, `factordb_query`, `sage_execute`, `hashcat_crack`, `john_crack`, `openssl_operation`, `crypto_challenge_workflow`
  - Forensics/stego: `binwalk_analyze`, `steghide_extract`, `foremost_carve`, `exiftool_analyze`, `volatility_analyze`, `tesseract_ocr`, `forensics_challenge_workflow`
  - Methodology: `ctf_strategy`, `get_safety_guide`, `get_common_wordlists`
- **`stego`**: the `steganography-mcp` server from `stego-mcp/`. Use it for image, audio, video, GIF, QR, document, text and JPEG hiding checks before generic tools. Media prefixes: `video_*` (detect, structure, metadata, frame_extract, frame_compare, frame_lsb, inter_frame, eof_data), `gif_*` (detect, frame_analysis, palette, palette_lsb, comment, appext, structure, lzw_analysis), `qr_*` (detect, data_extract, structure, module_analysis, ecc_analysis, compare), `mp3_*`. Other entry points: `img_lsb_detect`, `img_bitplane`, `img_chi_square`, `img_known_tools`, `audio_lsb_extract`, `audio_spectrum`, `text_zwc_detect`, `text_invisible_scan`, `text_homoglyph`, `file_identify`, `file_appended`, `file_polyglot`, `jpeg_structure`, `doc_pdf_streams`.
- **`osint-toolbox`**: ExifTool, Sherlock, Maigret, subfinder, dnsrecon, dnstwist, theHarvester, plus built-in RDAP, DNS, crt.sh and Wayback. Call `osint_toolbox_status` first; only installed tools are exposed. For Sherlock through this server use `output_format: "txt"` (the default CSV path passes a removed `--no-txt` flag on Sherlock 0.16). Use Maigret when Sherlock is rate-limited.
- **`playwright`**: official Microsoft Playwright MCP, configured to launch the installed system Chrome (`--browser chrome`). Use it for structured accessibility snapshots, form fills, console/network bodies, and storage-state handoff. For persistent CTF login sessions prefer `agent-browser`; Playwright is best for a stable element tree and network bodies.
- **agent-browser** (installed globally): the fast local browser path for web challenges and browser-only CTF platforms. Always use a named session (`agent-browser session id --scope worktree --prefix ctf`) and pass `--session` on every command. Prefer it for the first visit and HAR capture; use Playwright MCP when you need a stable element tree.

Use the project's tools before installing anything new. Install only what the chosen category skill's Prerequisites section lists, and only when it is missing.

## Step 3: Get the challenge context

1. Put the files in `ctf-solver/workspaces/<name>/` and run `file *`.
2. If the prompt links a CTF platform, check for CTFd (`curl -s "$CTF_URL/api/v1/" | head -5`). If CTFd, ask the user for an API token before using the API. Otherwise drive it with agent-browser.
3. If there is a remote target, check connectivity once (`nc -vz host port` or `curl -sI`), then continue.

## Step 4: Hand off

- For any HTTP, API, SPA, or browser-heavy challenge, invoke `/ctf-web`: run its ops loop first (lane selection, HAR capture, `har_map.py`) to map the API surface, then jump to the technique file for the bug class.
- Invoke the category skill from Step 1 for its techniques. For OSINT, invoke `/ctf-osint` for technique breadth and `/osint-ctf-databases` for primary-source APIs, geometry checks and confidence labels.
- Jail and sandbox prompts go to `/ctf-jail` even when the wrapper looks like misc; cloud/container/Kubernetes prompts go to `/ctf-cloud` (its SSRF-to-metadata path pairs with `/ctf-web`); firmware, logic-capture, CAN and side-channel prompts go to `/ctf-hardware`.
- For a challenge that spans categories or where the category is unclear, invoke `/solve-challenge` instead; it runs the full triage, pivot and write-up workflow.
- Keep notes in `ctf-solver/workspaces/<name>/notes.md`: what you tried, what worked, and any flag candidates.

## Step 5: Verify and report

- Validate any flag candidate against the format in the challenge or the CTF rules. Search the whole corpus for multiple candidates and prefer the one tied to the intended artifact.
- When solved, run `/ctf-writeup` for the submission write-up and save it next to the notes.
- Report: category, the tool and skill used, the flag (only when verified), and what remains if not solved. Never claim a flag you have not verified.

## Quick router examples

- "Here's a pcap, find the flag" -> forensics; check `ctf-kali` health; run `file`, then `/ctf-forensics`.
- "Where was this photo taken?" -> OSINT; call `osint_toolbox_status`, run `/ctf-osint` and `/osint-ctf-databases`, then verify with a second source.
- "nc chall.example 1337, buffer overflow" -> pwn; run `checksec` on the binary; `/ctf-pwn`.
- "Hidden message in this PNG" -> forensics stego; try the `stego` MCP first, then `/ctf-forensics`.
- "CTF platform at https://ctf.example.com, log in and solve" -> agent-browser named session; check CTFd first; then the category skill.
- "Solve this RSA challenge" with `chal.py` -> `/ctf-crypto`.
