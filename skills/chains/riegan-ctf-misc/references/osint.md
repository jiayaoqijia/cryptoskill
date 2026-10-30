# OSINT — enumerate, verify, pivot

Workflow for every OSINT task, no exceptions:

1. **Enumerate**: list every artifact (handles, images, domains, emails,
   timestamps, "useless" flavor text). CTF OSINT plants exactly the needed
   clues; flavor text is usually load-bearing.
2. **Verify**: each hypothesis needs two independent confirmations before you
   pivot on it (a username match alone is not identity; a landmark alone is
   not a city).
3. **Pivot**: each verified fact becomes the next query (handle → email →
   breach mention → domain → subdomain → cert → IP → …).
4. Log every source URL + finding in `notes.md` as you go — OSINT loops
   forever otherwise.

The agent-side tools (web search, browser) do the heavy lifting; the value you
add is the query recipe and the discipline. Nothing below needs you to run
scanners.

## Per-goal technique table

| Goal | First moves | Then |
|---|---|---|
| person / username | search exact handle quoted; check handle variants (`,`, `_`, `-`, year suffixes); whatsmyname.app concept (username enumeration across 600+ sites) | per-platform profile archetypes: GitHub (commit emails, gists), pastebin, gravatar hash |
| image | reverse image search (Yandex images, Google Lens, TinEye — try all three; Yandex wins on landmarks/faces); `exiftool` on the original file (camera, GPS tag) | crop distinctive objects and reverse-search the crop; note language on signs, driving side, license plate format, utility pole style, bollard/road markings |
| location (geo) | match built environment against street view; skyline + sun direction (shadow length/angle gives rough time-of-day + hemisphere; sun position calculators like suncalc.org to confirm) | signage conventions, business names from storefronts (search exact), utility poles (jp-style transformers → Japan), domain TLD in photos |
| moving objects | aircraft: adsbexchange.com, flightradar24.com (historical playback); ships: marinetraffic.com, vesselfinder.com (AIS); satellites: n2yo.com | flight number / registration / MMSI → route → time → location cross-check |
| infra / domain | `dig` TXT/MX/SPF/NS (below), crt.sh for subdomains, wayback + archive.today for deleted content | Shodan/Censys/FOFA syntax table below; google dorks |
| company | site: search, LinkedIn headcount & employee titles, job postings (tech stack leaks), press releases, crunchbase-style registries | map subsidiaries → repeat domain enumeration per entity |
| crypto wallet | BTC: blockchain.com/explorer; EVM: etherscan.io; multi-chain: blockchair.com | tx graph: first/last tx time, counterparties, exchange deposit addresses |

## Query recipes (copy-adapt)

### Web search (agent tool)

```
"<exact handle>"                       # quoted — no stemming, exact match
"<name>" site:github.com OR site:pastebin.com
intitle:"index of" "<company>"          # open dir listings
inurl:wp-content/uploads site:<domain>  # forgotten uploads
filetype:pdf site:<domain>              # docs that leak internals
"<distinctive phrase from challenge text>"   # organizers often reuse text
"<email address>"                       # breach-mention search
```

### Certificate transparency (subdomain goldmine)

```
https://crt.sh/?q=%25.example.com&output=json        # %25 = wildcard *
```

Browse via agent `read` (JSON). New certs reveal pre-launch hostnames.

### DNS (passive, one dig per record type)

```bash
dig example.com TXT +short        # verification tokens, flag-shaped strings
dig example.com MX +short         # mail provider → org identity
dig _dmarc.example.com TXT +short # SPF/DKIM mention other domains
dig example.com NS +short
```

### Archives

```
http://web.archive.org/cdx/search/cdx?url=example.com*&output=json&limit=200
https://archive.ph/newest/example.com            # archive.today snapshots
```

Wayback CDX lists every captured URL — old `/admin`, `/flag`, git dirs.

### Device/search engines (paste into their web UI)

| Engine | Syntax examples |
|---|---|
| Shodan | `hostname:example.com`, `ssl.cert.subject.CN:example.com`, `http.title:"Dashboard"`, `org:"Acme Inc"`, `net:203.0.113.0/24` |
| Censys | `dns.names: example.com`, `services.http.response.html_title: "Login"`, `services.port: 8080` |
| FOFA | `domain="example.com"`, `title="console"`, `body="example string"`, `icon_hash="1234567"` |

These are read-only searches; the challenge flag is often in a banner,
`http.title`, or a service screenshot on these engines.

### Image forensics

```bash
exiftool image.jpg                  # install: sudo pacman -S perl-image-exiftool
# look for GPSLatitude/GPSLongitude, DateTimeOriginal, Make/Model, Software
```

Stego pipelines belong to `ctf-forensics` (stego reference) — link there if
the image is a stego challenge wearing an OSINT costume.

## Person-pivot archetypes

| Artifact | Pivot |
|---|---|
| GitHub account | repos → commit email in patch (`git log` of their repo clone), gists, org membership |
| email | quoted search; gravatar (md5 of email); breach data is OFF the table (see ethics) |
| username | cross-site enumeration; password-recovery flows are FORBIDDEN (active interaction) |
| photo metadata | camera model → their other photos (search); GPS → location |
| document (pdf/docx) | author field, template UUID, printer timestamps — see `misc-grab-bag.md` |

## Ethics and legality (hard rules)

1. **Passive collection only.** No logins, no password resets, no contacting
   people, no liking/following, no interactions that could alert or disturb a
   real human. CTF personas are usually fictional — until proven otherwise,
   treat every identity as real.
2. **Event rules override everything.** Many events forbid OSINT on other
   players or organizers. Read the rules; log the relevant clause.
3. **No intrusion.** Finding an IP or open service is fine; port-scanning or
   touching it needs the remote gate from the `ctf` skill and is almost always
   unnecessary for the flag.
4. Breach/cracked databases: using them is both cheating in most events and a
   legal gray zone. Do not.
5. Minimize: collect only what the challenge needs; keep findings in the
   challenge dir, not scattered.

## Common failure modes

- One-source confidence: verify twice (a "matching" LinkedIn that contradicts
  the photo timeline is a trap the authors set).
- Ignoring timestamps: file mtimes, photo EXIF, cert `notBefore`, tweet dates
  — build the timeline in `notes.md`; the flag question is usually "when" or
  "where was this person on date X".
- Searching the original image only: crop and rotate before reverse search.
- Forgetting translation: foreign-language clues need a literal search in the
  original language, not the English translation.
