---
name: detect-mass-assignment
description: Use when a request body is bound directly to a model or object. Finds auto-binding sinks, checks which fields a client can set, and adds an explicit allowlist or read-only binding.
---

# Detect mass assignment

Mass assignment (over-posting) is when a framework binds every field in a request body to a model,
so a client can set fields the UI never exposed — `is_admin`, `role`, `credits`, `owner_id`,
`email_verified`. The fix is an explicit allowlist of assignable fields.

## Procedure

1. Find auto-binding sinks: they take the whole request payload, not a specific field.

       rg -n "request\.(json|body|data)|@RequestBody|params\[:user\]|strong_parameters|permit\(" src/ \
         | head -50

2. Inspect the target model's writable fields and compare against what the endpoint should accept:

       rg -n "class User|attr_accessible|guarded|@Column|@JsonProperty|fields\s*=" src/models 2>/dev/null

3. Probe by adding privileged fields that the UI does not send and observe whether they take effect:

       curl -s -X PATCH https://app.example.com/api/me \
         -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
         -d '{"display_name":"x","is_admin":true,"credits":999999,"role":"admin"}'

   Then re-read the profile and check whether `role`/`credits` changed.

4. Fix with an explicit allowlist. Framework idioms:

       # Rails: strong parameters
       params.require(:user).permit(:display_name, :email)
       # Django REST Framework
       read_only_fields = ["role", "credits", "is_admin"]
       # Spring: a DTO, not the entity
       public record UpdateProfileRequest(String displayName, String email) {}

5. Prefer a dedicated input DTO/view-model over binding to the persistence entity; the two should
   not be the same class.

6. Mark security-sensitive fields read-only at the model layer too (defence in depth), so a future
   endpoint cannot reassign them by accident.

7. Cover nested objects too: `{"profile":{"role":"admin"}}` if the parent binds nested models.

## Pitfalls

- A framework's `fillable`/`permit` list is easy to widen for a feature and never narrow back.
- `updated_at`, `id`, and foreign keys like `owner_id` are commonly over-postable and enable
  ownership transfer.
- PUT often replaces the whole object; a missing field becomes null rather than unchanged.
- GraphQL input types fed straight into an ORM update have the same exposure.
- Returning the full serialised entity then re-binding it round-trips attacker-set fields.
- Adding a new privileged column without updating the allowlist reopens the hole silently.

## Verification

    curl -s -X PATCH https://app.example.com/api/me \
      -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
      -d '{"role":"admin"}' | jq -r '.role'
    curl -s https://app.example.com/api/me -H "Authorization: Bearer $TOKEN" | jq -r 'has("is_admin")'

Pass: the response does not contain the injected `role`, and re-reading the profile shows it
unchanged. Report each binding sink, the fields exposed, and the allowlist now enforced.
