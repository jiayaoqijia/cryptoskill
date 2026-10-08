---
name: choose-deletion-vs-anonymisation
description: Use when a subject asks to be removed or a dataset is released and you must pick between deleting and anonymising. Choose per purpose and prove the result is really gone or really unlinkable.
---

# Choose deletion vs anonymisation

Deleting and anonymising solve different problems. This skill picks the right one per request and proves the result is what it claims to be.

## Procedure

1. Ask what the data is needed for after the request. Nothing means delete. Aggregate statistics means anonymise. A legal record means retain the minimum and restrict who can read it.

2. Deletion means the bytes are unrecoverable in active systems, backups, caches, search indexes, and analytics. Enumerate all five before claiming deletion.

3. Anonymisation must be irreversible. Removing a name from a row that still holds a unique `user_id` is pseudonymisation, not anonymisation.

4. Test reversibility before claiming anonymisation: try to re-join the anonymous table to the identity table. Any join returning the person means it is not anonymous.

5. For deletion, run children first:
   `delete from sessions where user_id=$1; delete from events where user_id=$1; delete from users where id=$1;`

6. For anonymisation, overwrite rather than drop columns so counts and joins survive:
   `update users set email=null, name='', phone=null where id=$1`

7. Record which choice was made and why, per subject, in an audit row with timestamp and operator. This is what answers a regulator.

8. Where both apply, delete the identifiers and keep the anonymised activity: an events table with a per-subject random salt is no longer linkable.

9. Re-check every downstream copy after 24h; async pipelines and mirrors lag behind the primary.

## Pitfalls

- `DELETE` in Postgres does not reclaim space until vacuuming; disk forensics can read the tuple until the page is reused.
- A soft-delete flag such as `deleted_at` keeps the data. It is not deletion.
- Increment-only aggregates (region counts) cannot identify a person and are worth keeping.
- Removing direct identifiers while leaving quasi-identifiers (postcode plus date of birth plus sex) still permits re-identification.
- A legal retention obligation on one field means you delete activity data but keep the invoice; be explicit about which field stays.

## Verification

    psql "$DATABASE_URL" -c "select count(*) from users where id=$SUBJECT_ID"        # expect 0
    psql "$DATABASE_URL" -c "select count(*) from events e left join users u on u.id=e.user_id where u.id is null and e.uid_key=$SUBJECT_ID"  # orphans = residue

Report the choice made per subject, the systems confirmed clean, and any copy still pending or retained under a legal basis.
