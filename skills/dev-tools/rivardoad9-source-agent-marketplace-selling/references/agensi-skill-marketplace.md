# Agensi (and SKILL.md-style) marketplaces

Agensi sells **skills**, not services: the buyer's agent reads text files. That changes both what is
sellable and how the package must be built. Rules below are from the official creator docs plus one
end-to-end conversion of a Node repository into a listed-shaped skill.

## What the buyer actually receives

The upload is one ZIP containing `SKILL.md` at the root plus supporting text files, each under 50 MB,
fewer than 1,000 files, no executables. The bytes are delivered over MCP; only **text** files reach
the buyer's agent.

This is the constraint that kills most repo-to-listing ideas:

1. **A script runs alone.** The agent writes the script to a temp file and runs it there, so it cannot
   import a sibling module, read a `references/` file, or load a `config.json` from the package. Anything
the script needs at run time is either fetched over the network or embedded in the script itself.
2. **No bundled dependencies.** No `node_modules`, no `pip install`, no venv. Python standard library
   or Node built-ins only, and keep the script under ~20 KB of logic; split into several scripts only
   when each is independently useful.
3. **Images and PDFs are allowed in the ZIP but the agent cannot read them.** Screenshots are page
   decoration for humans. Never make the workflow depend on the agent seeing a PNG, and never ship a
   dashboard as the deliverable — print text.
4. **Zip layout matters.** `SKILL.md` at the archive root, not inside a wrapper directory; many tools
   reject a nested root. Build with `arcname=os.path.relpath(p, src)`.

## Frontmatter and listing fields

`SKILL.md` frontmatter carries `name`, `description`, `summary`, `version`, `tags`, `keywords`,
`use_cases`, optional `docs_url`. The `description` is what the marketplace searches, so lead with the
outcome the buyer asks for, not the technique. State permissions explicitly (which hosts the script
calls, whether it needs a credential) and a support window.

## Converting a repo into a skill: the audit order

1. **Can it run without the author's private data?** If it reads a sealed snapshot, a watchlist, or a
   local dump, it is not a product. Reproduce that dependency by running the repo against a synthetic
   fixture: if the model silently falls back to hard-coded constants and reports `R² 0.000` or `0%
   blind test`, the accuracy claim in its README belongs to data nobody else has. Do not list the claim.
2. **Does every number you plan to quote reproduce?** If not, drop it from the description and say in
   `references/method.md` which claim was not reproduced and why. Listing an unverifiable backtest is a
   refund and a review, not marketing.
3. **Secret scan** before packaging: `grep -rInE "sk-[A-Za-z0-9]{16,}|PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|api[_-]?key\s*[:=]"`.
   Also check `.env` history is absent, not just the working tree.
4. **Vendored files need their own licence header.** A file copied from a challenge kit or another
   project, with no copyright line, cannot be resold. Drop it and rewrite the logic, even when the
   repo's own LICENSE is MIT.
5. **Cross-check the data licence separately from the code licence.** MIT on the script says nothing
   about redistributing an API's dataset. Fetching live at run time avoids the question; bundling a
   dump does not.

## Verify the signal field before building a screen

A public dataset's fields are not equally trustworthy, and a research skill is worth what its screen
discriminates. Count the rows where the field you plan to key on is actually populated **before**
writing the screen, and check whether it is a property of the entity or an artefact of the feed.
Worked case: on a protocol list, `symbol` is filled for nearly every row including entities with no
liquid token, market cap exists only on tokenized parents, and child entries (`V2`, `Bridge`, `Earn`,
`Staked`, `Vault`, `DEX`) repeat the parent's market cap verbatim. Keying "has a token" on `symbol`
labelled thousands of non-tokens as candidates; keying it on `mcap > 0` and dropping child names plus
rows sharing a market-cap value with another row left a usable list. Two rules follow: absence of the
field is `unknown`, never `candidate`; and duplicate values across rows are a hierarchy, not a
coincidence. Say which signal you keyed on in `references/method.md` so a buyer can audit it.

## Rebuild shape that passes review

One self-contained script with `--input <file>` (offline, same schema as the live source), `--json`
output, `--as-of` for anything time-dependent so runs are reproducible, and a fixture plus test suite
that assert the method against a known answer rather than against the live world. Print markdown; do
not write a dashboard. Tests must run with no network and no key.

Prove it the way a buyer would: extract the ZIP into an empty directory, run the tests, run one live
call, confirm the output. A package that only works in the author's tree is not shipped.

## Economics on the terms Agensi confirmed

Creator 70%, Agensi 30%, Stripe fees borne by the platform, tool calls billed separately to the buyer
with no creator share. So the creator's net is simply `0.70 × price`, and the tool-call clause is
irrelevant for a skill that makes no tool calls — it only bites skills whose value is a hosted tool.
Marginal cost of a compute-only skill is approximately zero (one free API request, a second of CPU).

Observed price anchors in the quant / crypto-research neighbourhood: roughly $6.49 to $39 for
single-script skills, with a $250 outlier that was a book plus companion. Before picking a price,
search the marketplace category and read the **direct competitor's** pitch, dataset and example output.
The obvious angle is usually already listed at the floor price; if so, say the differentiation is thin
rather than inventing a premium.

Never project sales. Category depth, listing count and a live competitor are the honest inputs; say
revenue is unknown until the first sales exist.

## Approval gate

Draft the listing text, price and package, then stop. No submit, no publish, no public draft, until the
owner approves. Same rule as any marketplace: drafting is reversible, publishing is not.
