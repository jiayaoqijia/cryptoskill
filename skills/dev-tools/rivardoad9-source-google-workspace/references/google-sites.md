# Google Sites: what an agent can and cannot do

Check this before answering "can you connect to Google Sites?" or agreeing to build/update a Site.

## Read is possible through Drive

A Site is a Drive file with `mimeType = application/vnd.google-apps.site`. With the Drive scope
already on the token you can:

```python
dv.files().list(q="mimeType='application/vnd.google-apps.site'").execute()
```

Useful fields: `owners`, `lastModifyingUser`, `createdTime`, `modifiedTime`, `parents`,
`webViewLink`. `lastModifyingUser` is how you tell which account actually built a shared site.

Reading the page text is also possible without any Sites API — export it:

```python
dv.files().export(fileId=SITE_ID, mimeType="text/plain").execute()
```

A site that has never been filled exports as the default template only (site name, "Halaman Muka",
"Judul halaman Anda" / "Your page title"). That is a fast, reliable way to prove a site is still
empty — far cheaper than asking the user to screenshot the editor.

## Write is not available

There is no public REST API to create pages, add text or images, or publish. Google retired the
Sites API in 2017; `https://sites.googleapis.com/v1/sites` answers 404. Do not plan an automation
around the Sites editor, and do not promise it after "checking again" later.

## What to offer instead

1. **Static HTML deployed elsewhere** — Vercel, GitHub Pages, Netlify. These have real APIs, so the
   page can be built, deployed and updated end to end without the user touching an editor.
2. **Content authored by the agent, pasted by the user** — deliver the final copy and the section
   order, plus a screenshot of the reference design, so filling the Sites editor is mechanical.
3. **Hosted page + one Embed block** — the best of both when he wants the site to keep its Sites URL:
   deploy the page (option 1), then he adds a single `Embed → By URL` block in Sites, once. Every later
   update happens in the repo and the embedded page changes without touching Sites again. Say this
   explicitly, because "I can't edit Sites" alone reads as "this can't be done".

Driving the editor itself is possible only through an authenticated browser session (append `/edit` to
`/d/<siteId>/`; headless lands on `accounts.google.com` with no session). If the user insists, the login
must come from the password vault, never from chat, and the canvas editor makes every step fragile —
present it as a last resort next to the three options above, not as the plan.

State the limitation in one sentence and move to option 1; do not stall on the limitation.
