#!/usr/bin/env python3
"""Small, dependency-free queries against public OSINT sources.

Designed for CTF evidence gathering: stable endpoints, a descriptive
User-Agent, bounded retries, and JSON on stdout so results can be saved.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

UA = "OSINT-CTF-Lab/1.0 (authorized CTF research; contact: local-user)"
TIMEOUT = 45
RETRIES = 3


def _request(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    data: dict[str, str] | None = None,
    accept: str = "application/json",
    timeout: int = TIMEOUT,
) -> bytes:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"
    body = urllib.parse.urlencode(data).encode() if data else None
    headers = {"User-Agent": UA, "Accept": accept}
    last: Exception | None = None
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code not in (429, 500, 502, 503, 504) or attempt == RETRIES - 1:
                raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            if attempt == RETRIES - 1:
                raise
        time.sleep(2**attempt)
    raise RuntimeError(f"request failed: {last}")


def _json(url: str, **kwargs: Any) -> Any:
    return json.loads(_request(url, **kwargs))


def overpass(query: str) -> Any:
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.private.coffee/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
    ]
    errors: list[str] = []
    for endpoint in endpoints:
        try:
            raw = _request(endpoint, data={"data": query}, timeout=180)  # type: ignore[call-arg]
            return {"endpoint": endpoint, "data": json.loads(raw)}
        except Exception as exc:  # noqa: BLE001 - report the endpoint failure
            errors.append(f"{endpoint}: {exc}")
            time.sleep(1)
    raise RuntimeError("all Overpass endpoints failed:\n" + "\n".join(errors))


def nominatim(query: str, reverse: bool = False) -> Any:
    base = "https://nominatim.openstreetmap.org"
    if reverse:
        lat, lon = query.split(",")
        params = {"lat": lat.strip(), "lon": lon.strip(), "format": "jsonv2", "addressdetails": 1}
        return _json(f"{base}/reverse", params=params)
    params = {"q": query, "format": "jsonv2", "addressdetails": 1, "limit": 5}
    return _json(f"{base}/search", params=params)


def commons_geo(lat: str, lon: str, radius: str) -> Any:
    params = {
        "action": "query",
        "format": "json",
        "generator": "geosearch",
        "ggscoord": f"{lat}|{lon}",
        "ggsradius": radius,
        "ggslimit": 30,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
    }
    return _json("https://commons.wikimedia.org/w/api.php", params=params)


def wikidata(sparql: str) -> Any:
    return _json(
        "https://query.wikidata.org/sparql",
        params={"query": sparql, "format": "json"},
        accept="application/sparql-results+json",
    )


def crt(domain: str) -> Any:
    return _json(
        "https://crt.sh/",
        params={"q": f"%.{domain}", "output": "json"},
        accept="application/json",
    )


def rdap(target: str) -> Any:
    kind = "ip" if target.replace(".", "").isdigit() else "domain"
    return _json(f"https://rdap.org/{kind}/{target}", accept="application/rdap+json")


def wayback(pattern: str, limit: int = 200) -> Any:
    params = {
        "url": pattern,
        "output": "json",
        "fl": "timestamp,original,statuscode,mimetype,digest",
        "collapse": "digest",
        "limit": limit,
    }
    raw = _request("https://web.archive.org/cdx/search/cdx", params=params)
    text = raw.decode("utf-8", "replace").strip()
    return json.loads(text) if text else []


def osm_way(way_id: str) -> Any:
    return _json(
        f"https://api.openstreetmap.org/api/0.6/way/{way_id}/full.json",
        accept="application/json",
    )


def ripestat(dataset: str, resource: str) -> Any:
    safe = dataset.replace("_", "-")
    return _json(
        f"https://stat.ripe.net/data/{safe}/data.json",
        params={"resource": resource},
    )


def gleif(name: str) -> Any:
    params = {"filter[entity.legalName]": name, "page[size]": 10}
    return _json("https://api.gleif.org/api/v1/lei-records", params=params)


def gdelt(query: str) -> Any:
    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "maxrecords": 50,
        "sort": "hybridrel",
    }
    return _json("https://api.gdeltproject.org/api/v2/doc/doc", params=params)


def opensky(bbox: str) -> Any:
    lamin, lomin, lamax, lomax = (x.strip() for x in bbox.split(","))
    return _json(
        "https://opensky-network.org/api/states/all",
        params={"lamin": lamin, "lomin": lomin, "lamax": lamax, "lomax": lomax},
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    q = sub.add_parser("overpass", help="run an Overpass QL query, with endpoint fallback")
    q.add_argument("query", help="query text or @path/to/query.overpassql")

    n = sub.add_parser("nominatim-search", help="geocode a place name")
    n.add_argument("query")
    nr = sub.add_parser("nominatim-reverse", help="reverse geocode lat,lon")
    nr.add_argument("query", help="e.g. 40.508889,141.543769")

    c = sub.add_parser("commons-geo", help="Commons images near a coordinate")
    c.add_argument("lat")
    c.add_argument("lon")
    c.add_argument("radius", nargs="?", default="500")

    w = sub.add_parser("wikidata", help="run a SPARQL query")
    w.add_argument("query", help="SPARQL text or @path/to/query.rq")

    cr = sub.add_parser("crt", help="certificate transparency names")
    cr.add_argument("domain")
    r = sub.add_parser("rdap", help="domain or IP registration data")
    r.add_argument("target")
    wb = sub.add_parser("wayback", help="Wayback CDX index")
    wb.add_argument("pattern", help="e.g. example.com/*")
    wb.add_argument("--limit", type=int, default=200)

    ow = sub.add_parser("osm-way", help="OSM way geometry and tags")
    ow.add_argument("way_id")

    rs = sub.add_parser("ripestat", help="RIPEstat dataset lookup")
    rs.add_argument("dataset", help="prefix-overview, as-overview, routing-status, ...")
    rs.add_argument("resource")

    g = sub.add_parser("gleif", help="legal entity LEI lookup")
    g.add_argument("name")
    gd = sub.add_parser("gdelt", help="GDELT news/event search")
    gd.add_argument("query")
    os_ = sub.add_parser("opensky", help="aircraft states in a bbox")
    os_.add_argument("bbox", help="lamin,lomin,lamax,lomax")

    args = p.parse_args()

    def load(value: str) -> str:
        if value.startswith("@"):
            with open(value[1:], encoding="utf-8") as fh:
                return fh.read()
        return value

    handlers = {
        "overpass": lambda: overpass(load(args.query)),
        "nominatim-search": lambda: nominatim(args.query),
        "nominatim-reverse": lambda: nominatim(args.query, reverse=True),
        "commons-geo": lambda: commons_geo(args.lat, args.lon, args.radius),
        "wikidata": lambda: wikidata(load(args.query)),
        "crt": lambda: crt(args.domain),
        "rdap": lambda: rdap(args.target),
        "wayback": lambda: wayback(args.pattern, args.limit),
        "osm-way": lambda: osm_way(args.way_id),
        "ripestat": lambda: ripestat(args.dataset, args.resource),
        "gleif": lambda: gleif(args.name),
        "gdelt": lambda: gdelt(args.query),
        "opensky": lambda: opensky(args.bbox),
    }

    try:
        result = handlers[args.command]()
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        print(f"error: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
