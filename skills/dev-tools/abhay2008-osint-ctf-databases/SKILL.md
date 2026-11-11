---
name: osint-ctf-databases
description: Authoritative public databases and live APIs for OSINT CTF work. Use for geolocation, map/POI proximity, Wikidata/Commons verification, domain/RDAP/certificate history, web archives, corporate registries, flight/vessel enrichment, and turning a vague clue into a reproducible source trail.
license: MIT
compatibility: Requires bash, Python 3.10+, and internet access. Optional MCP server osint-toolbox for ExifTool, Sherlock, Maigret, subfinder, dnsrecon, dnstwist and theHarvester.
metadata:
  user-invocable: "true"
  author: Freebuff CTF workspace
---

# OSINT CTF Databases

Use this skill when the answer must come from a **primary public source**, not a search-result snippet. Pair it with `/ctf-osint` for technique breadth and `/ctf-similar-search` only when writeup precedent is useful.

**Scope:** CTF events, fictional personas, your own infrastructure, and authorized research. Do not investigate private individuals, do not contact targets, and do not bypass logins, paywalls, CAPTCHAs or rate limits.

## Operating loop

1. **Define the oracle.** What exact string/number/coordinate will be submitted? If the flag format is unknown, find it before searching.
2. **Classify the seed:** pixel, metadata, username, email, domain, IP/ASN, organization, phone, document, archive, map feature, or transport.
3. **Go passive first.** Archives, certificate transparency, RDAP, DNS, public registries, OSM/Wikidata. Active scanning only inside the CTF's authorized scope.
4. **Corroborate on a second domain.** One source is a lead; two independent sources are evidence. Record URL, retrieval time, and the exact field used.
5. **Prefer structured APIs over scraping.** They are faster, reproducible, and less likely to break.
6. **Keep a trail.** Save raw JSON next to notes; never overwrite the original artifact. Redact unrelated personal data from the final writeup.

## Source tier list for CTF work

| Tier | Source | Best for | Access / caveat |
|---|---|---|---|
| S | OpenStreetMap + Overpass | POIs, parks, shops, rail, infrastructure, polygon/way IDs | Free; public endpoints can be busy — use bbox queries, backoff, and `api.openstreetmap.org` for small areas |
| S | Google Lens / Yandex / TinEye / Bing Visual Search | Reverse image, cropped regions, faces (Yandex), exact copies (TinEye) | Browser-only; manual/captcha limits |
| S | Internet Archive Wayback CDX | Deleted pages, renames, old profiles, first/last capture | Free API; capture time ≠ publication time |
| S | crt.sh | Subdomains and historical hostnames from Certificate Transparency | Free; flaky/timeouts; retry and dedupe |
| S | RDAP (rdap.org / registry) | Registrar, creation/expiry, nameservers, status | Free; follow redirects; WHOIS privacy hides registrant |
| S | Wikimedia Commons + Wikidata | Landmark verification, coordinate/name reconciliation, image search | Free APIs; Commons metadata is community-maintained |
| A | ExifTool | GPS, camera, author, software, timestamps, XMP | Local; social platforms often strip EXIF |
| A | GeoNames | 8M+ place names, alternate names, postal codes | API needs a free account; bulk dumps are CC BY 4.0 |
| A | Common Crawl index | Pages/links not in search engines, historical crawls | Free; index lookup by URL/domain |
| A | GDELT 2.0 DOC API | News/event pivots, outlet country, timelines | Free; machine-generated noise |
| A | OpenSky Network | Aircraft state vectors, callsign/ICAO24 | Free anonymous tier is rate-limited |
| A | GLEIF LEI API | Legal entity identity, parent relationships | Free; only entities with an LEI |
| A | SEC EDGAR full-text search | US public-company filings, exhibits, names | Free; fair-access User-Agent required |
| A | FEC OpenFEC | US campaign finance, committees, donors | Free `DEMO_KEY` is rate-limited |
| A | RIPEstat / PeeringDB / bgp.tools | ASN, prefix, routing, interconnection | Free; network ownership ≠ user location |
| B | Shodan / Censys / VirusTotal | Internet exposure, certs, reputation | API key required; do not scan outside scope |
| B | What3Words / Google Street View | 3 m squares / panorama metadata | API key or browser; Street View coverage varies |
| B | MarineTraffic / VesselFinder | Vessel identity, IMO, track | Mostly paid; public pages may be enough |

## The local query tool

`scripts/osint_query.py` is a dependency-free wrapper around the stable endpoints. It prints JSON and retries transient failures. Run it from this skill directory:

```bash
python3 scripts/osint_query.py overpass 'nwr["leisure"="park"](around:200,40.5089,141.5438); out center tags;'
python3 scripts/osint_query.py nominatim-reverse 40.508889 141.543769
python3 scripts/osint_query.py nominatim-search 'Kamisawamakime Park Aomori'
python3 scripts/osint_query.py commons-geo 40.508889 141.543769 500
python3 scripts/osint_query.py wikidata 'SELECT ?item ?itemLabel WHERE { ?item wdt:P31 wd:Q570116; wdt:P131 wd:Q146790. SERVICE wikibase:label { bd:serviceParam wikibase:language "en,ja". } } LIMIT 10'
python3 scripts/osint_query.py crt example.com
python3 scripts/osint_query.py rdap example.com
python3 scripts/osint_query.py wayback 'example.com/*'
python3 scripts/osint_query.py osm-way 556701681
python3 scripts/osint_query.py ripestat prefix 1.1.1.0/24
python3 scripts/osint_query.py gleif 'OpenAI'
python3 scripts/osint_query.py gdelt 'Aomori park'
```

Use `python3` only if it is a real interpreter. On this machine `/usr/bin/python3` is currently broken by an Xcode shim; use `/opt/homebrew/bin/python3.12`.

## Playbook: geolocation and map proximity

1. Run `exiftool -a -G1 -s image.jpg`; check GPS, XMP, copyright, software, dates. If GPS exists, reverse-geocode it but still verify the scene.
2. If no GPS, crop the most distinctive region (shop sign, facade, pole, road marking) and reverse-search the crop. Google Lens usually beats a full-scene search.
3. Identify country from script, driving side, plates, bollards, road signs, architecture, vegetation. Then narrow region/city.
4. Match micro-landmarks in Street View: utility poles, bollards, planters, roof lines, background buildings, shadow direction. Camera position matters as much as the subject.
5. For OSM questions, use `nwr`, not just `node`/`way`: `nwr["shop"="convenience"]`.
6. For “within N metres” questions, do not rely on a single centroid. Check:
   - centroid-to-centroid,
   - nearest polygon vertex/edge,
   - and, if needed, the pairwise distances between the three features.
   The challenge wording often tolerates “approximately”.
7. Verify the final object with `osm-way <id>` and `nominatim-reverse`; submit the **way ID**, not the display name, when the flag asks for a Way Number.

Worked hard example — DIVER OSINT CTF 2025 `convenience`:

- Target: southernmost Aomori park with a convenience store and supermarket within ~100 m.
- Answer: OSM way `556701681` (`上沢巻目公園`, Kamisawamakime Park), around `40.508889, 141.543769`.
- Verification: supermarket `ユニバース湊高台店` ~61 m from the park centroid; FamilyMart ~75 m from the supermarket and ~111 m from the park boundary. This is why “approximately 100 m” must be interpreted against the actual geometry, not one center point.
- Resilience: if Overpass returns 502/504, use a small `api.openstreetmap.org/api/0.6/map?bbox=...` request and compute haversine distances locally. Do not hammer the public endpoint.

## Playbook: domain / infrastructure

```bash
dig +short A example.com
dig +short MX example.com
dig +short NS example.com
dig +short TXT example.com
whois example.com                 # if available
curl -sL -A 'OSINT-CTF-Lab/1.0' https://rdap.org/domain/example.com | jq .
curl -sL -A 'OSINT-CTF-Lab/1.0' 'https://crt.sh/?q=%25.example.com&output=json' | jq -r '.[].name_value' | sort -u
curl -sL -A 'OSINT-CTF-Lab/1.0' 'https://web.archive.org/cdx/search/cdx?url=example.com/*&output=json&fl=timestamp,original,statuscode&collapse=digest' | jq .
subfinder -d example.com -silent
theHarvester -d example.com -b duckduckgo,bing -l 100
```

Rules:
- `crt.sh` requires the `%25` wildcard form and may time out; retry with backoff.
- RDAP is the modern WHOIS. Follow redirects and send a User-Agent.
- Certificate SANs can reveal internal/staging hostnames; treat them as leads, not proof of current resolution.
- `dnstwist` finds lookalikes but can be slow; cap the TLD set for CTF work.
- Do not run `nmap`, `sqlmap`, `hydra` or brute force against a domain unless the CTF explicitly authorizes it.

## Playbook: username / person (fictional or consenting targets only)

1. Use `whatsmyname.app` manually, or the WhatsMyName dataset for scripting. Do not trust HTTP 200 alone: Telegram, TikTok, Smule and Instagram produce false positives.
2. Run Sherlock and Maigret with a timeout; Maigret's `all_sites` mode can take minutes.
3. Prefer first-party profile APIs (Bluesky public API, GitHub API, Reddit JSON) over scraping.
4. Pivot on durable identifiers: numeric user IDs, commit author emails, avatar hashes, linked domains, reused bios.
5. Check the Wayback CDX for renamed/deleted accounts. A `t.co` redirect can preserve an old username.
6. Through `osint-toolbox`, set `output_format: "txt"`. The default CSV path in `osint-toolbox-mcp 1.1.0` passes `--no-txt`, which Sherlock 0.16.2 removed; `txt` works.
7. Stop at the flag. Do not collect unrelated personal data, do not contact the persona, and do not attempt credential access.

## Playbook: archives and deleted content

```bash
# CDX index: captures, status, digest, mimetype
curl -sL -A 'OSINT-CTF-Lab/1.0' \
  'https://web.archive.org/cdx/search/cdx?url=target.example/*&output=json&fl=timestamp,original,statuscode,mimetype,digest&collapse=digest'

# Common Crawl collection list, then a URL lookup
curl -sL https://index.commoncrawl.org/collinfo.json | jq -r '.[0:3][] | .id'
curl -sL 'https://index.commoncrawl.org/CC-MAIN-2025-30-index?url=target.example/*&output=json'
```

- Distinguish **capture timestamp** from **content timestamp** (a page may describe an older event).
- `collapse=digest` removes duplicate content and makes timeline review much faster.
- Archive.today is a separate crawler; check it manually when Wayback has no capture.
- Preserve the raw HTML/JSON and the exact capture URL in notes.

## Playbook: corporate, transport, and event enrichment

- **GLEIF**: `https://api.gleif.org/api/v1/lei-records?filter[entity.legalName]=...` for legal entity identity and parent relationships.
- **SEC EDGAR**: use a descriptive User-Agent and `https://efts.sec.gov/LATEST/search-index?q=%22...%22` for full-text filings.
- **OpenFEC**: `https://api.open.fec.gov/v1/...?api_key=DEMO_KEY`; the demo key is heavily rate-limited.
- **OpenSky**: `https://opensky-network.org/api/states/all?lamin=...&lomin=...&lamax=...&lomax=...`; anonymous access is limited, so cache results.
- **GDELT**: `https://api.gdeltproject.org/api/v2/doc/doc?query=...&mode=artlist&format=json&maxrecords=50`.
- **Wikidata**: use `SERVICE wikibase:label` and cite the `Q` ID; do not trust a single label match.
- **Commons**: `generator=geosearch` + `prop=imageinfo&iiprop=url|extmetadata` is the fastest way to find crowd photos for a candidate landmark.

## Confidence labels for the final answer

- **Verified**: primary source + independent corroboration + exact field/geometry checked.
- **Probable**: two sources agree but one is derivative, or geometry is approximate.
- **Lead**: one source only; never submit as a flag without another check.

Report the confidence label. A wrong confident answer is worse than a documented uncertainty.

## Failure modes and fallbacks

| Failure | Fallback |
|---|---|
| Overpass 502/504 | Smaller bbox, `out center`, local haversine; OSM map API for tiny areas; retry with exponential backoff |
| crt.sh timeout | Retry; use Censys/Shodan only if already authorized/configured; check `crt.sh` HTML manually |
| RDAP empty | Follow redirects with `-L`; query the registry RDAP directly (e.g. `rdap.verisign.com/com/v1/domain/...`) |
| Reverse image search blocked | Yandex/Bing/TinEye; crop; try a mirrored/reflected version; search by place name instead of pixels |
| EXIF stripped | Visual clues, reverse image, Wayback original file, platform-specific metadata behavior |
| Tool rate-limited | Cache, slow down, use a documented API key, or switch to a primary registry |
| MCP tool missing | Fall back to the CLI or the direct API; record which path worked |

## Safety

Use only CTF/fictional targets or infrastructure you own or are explicitly authorized to test. Never doxx, stalk, harass, contact a target, bypass authentication, or publish unrelated personal data. If a challenge appears to target a real private person, stop and ask the organizer or your team lead.
