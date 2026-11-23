# Ticket / order email → Google Calendar event

Use when the user says some version of "check my email, I just paid for X, put it in my calendar, and put the
ticket details + location in the description". The same file covers a screenshot of a dated table ("here's my
exam / class schedule") — see §10.

## 1. Find the receipt

```bash
$GAPI gmail search "newer_than:14d (tiket OR ticket OR invoice OR pembayaran OR konfirmasi OR order OR payment OR e-ticket)" --max 25
```

One purchase normally lands as THREE mails: the ticketing platform (venue, dates, ticket tier, attachment), a
payment gateway (amount actually paid, promo code, reference ID), and the bank/e-wallet notice. Take the event
facts from the ticketing mail, the money from the gateway mail. Promo/newsletter hits for *other* events of the
same organizer are noise — the DATE in a snippet is often a different event's date.

## 2. Read them properly

These mails are always HTML-only, so `$GAPI gmail get <id>` returns `body: ""`. Use
`scripts/gmail_raw_read.py <id> …`: it prints the text parts and saves the attachments. Then read the e-ticket
PDF with `read_file` (PDF text extraction works) — it carries attendee name, ticket type and ticket/order IDs,
but usually NOT the daily hours.

## 3. Extract the checklist

Order ID, ticket ID, attendee name, ticket tier + what it includes (a student tier means an ID check at the
door), amount paid vs list price + promo code, payment method and timestamp, venue name, date range, organizer
site. Report the correction if the user's assumed date is wrong — they asked about "11/12" and the ticket says
November, not October.

## 4. Venue → a real address

The venue string on the ticket ("Kuningan City, Grand Ballroom") is not an address. Geocode it and put the full
street address in `location`; the user navigates from `location`.

```bash
curl -s -A "hermes-agent/1.0 (calendar event lookup)" \
  "https://nominatim.openstreetmap.org/search?q=Kuningan+City+Mall+Jakarta&format=json&limit=3&addressdetails=1"
```

## 5. Hours: all-day if unannounced

Check the organizer's site and socials for a daily agenda before assuming. If only dates are published, create an
ALL-DAY event (date-only start/end — see the Calendar section of SKILL.md) and say in the reply that the hours
aren't announced plus where to check. An invented 09:00–18:00 is worse than a whole-day block: the user plans
around it.

## 6. Description template (the user wants ticket + location HERE)

Plain text, `==` headers, no tables. Written in the user's language:

```
== TIKET ==
Jenis: <tier> (<what it includes>, <mandatory ID at entry>)
Order ID: …
Ticket ID: …
Atas nama: <name> / <email>
Harga: <list price> dibayar <paid> (promo <code>)
Cara bayar: <method> lewat <gateway>, <date + time>
Bukti bayar: email "<subject>" dari <sender> + e-ticket PDF terlampir
File tiket lokal: ~/tickets/<event>-<tier>.pdf

== ACARA ==
<nama event> (<tagline>)
Tanggal: <range>, <n days>
Lokasi: <venue> — <full street address>
Situs: <url>
Jam: belum diumumin (email & halaman resmi cuma nulis tanggal), cek <IG/site> menjelang hari-H

== BAWA ==
<ID that is mandatory for this tier>, e-ticket PDF/QR di HP, KTP kalau diminta
```

Multi-day events: state which day the user attends and which is skipped, and why — that decision was theirs, the
event description should record it.

## 7. Verify, then sweep for collisions

1. Read the event back (`events().get`) and report the stored summary/start/end/location and description length.
   The insert response alone is not verification.
2. List `timeMin`/`timeMax` = ±3 days around it with `singleEvents=True, orderBy=startTime`, then tell the user:
   - a pre-existing entry for the same event → duplicate; ASK before deleting, never delete unasked;
   - a real clash with their own recurring schedule (classes etc.) → surface it as a question, don't move their
     other events;
   - confirm genuine free space so the entry isn't quietly overlapping something.

## 8. Keep the artifact

Copy the e-ticket PDF out of `/tmp` into a durable path (`~/tickets/<event>-<tier>.pdf`), name that path in the
description, and attach the PDF in the chat reply. `/tmp` gets pruned; the ticket must outlive the session.

## 9. Editing, enriching, or replacing an existing entry

- **Never reuse a truncated event id.** Calendar ids are opaque base32 strings longer than they look; a
  `get`/`update`/`delete` with `id[:22]` returns `404 Not Found`, which reads like "the event vanished" but is
  your own cut-off string. Re-list the window inside the SAME script, match on `summary` + start date, and use
  the id the API just handed back.
- "replace aja, ganti yang baru" = delete the old one, keep the new one. Guard the delete with all three:
  summary matches, start falls on the expected day, and `id !=` the event you created.
- To enrich an existing event, `get` its body, append to `description` only if your marker text is absent, then
  `update` passing the whole fetched body back so nothing else is dropped. Re-read afterwards and report the new
  description length as proof it stored.
- Set reminders explicitly at create time (`reminders: {"useDefault": False, "overrides": [{"method": "popup",
  "minutes": 1440}]}`). Leaving it on calendar defaults can mean the user gets no reminder at all.

## 10. Screenshot of a dated table → calendar

The user sends a schedule image (exams, class list, shift roster) and says some version of "here's my schedule".
The expected result is that it gets RECORDED, not acknowledged.

1. Transcribe it verbatim with `vision_analyze` — one row per line, every column, no summarizing. You need cell
   values (room, seat number, time), not a gist.
2. List the covered window FIRST. A previous session has often already created these entries; inserting again
   produces exactly the duplicates of §7. Match on title + start and report agreement instead of adding.
3. Enrich, don't duplicate: put the fields the existing event lacks (seat/row number, exam type, source
   document) into its description, and add a H-1 reminder if none is set.
4. Write the whole table to a durable note (`~/obsidian-vault/<Topic> (<Month Year>).md`) with a status column
   (passed / next / upcoming) so the record outlives the screenshot.
5. Report what was already there and matched, what you changed, the next date in the list, and a conflict flag if
   that date already holds another commitment.
