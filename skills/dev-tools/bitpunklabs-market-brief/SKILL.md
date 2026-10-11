---
name: market-brief
description: Produce evidence-based market briefs for China A-shares, U.S. equities, and Crypto using the packaged research prompts. Use for premarket, postmarket, daily, weekly, or monthly research, exporting a prompt, or explicitly maintaining this prompt library.
license: MIT
metadata:
  version: "0.1.0"
---

# Market Brief

Use the selected prompt as the research assignment and deliver the brief directly.
The complete prompts in `assets/prompts/` are the maintained source of truth.

## Select a prompt

Infer the market and cadence from the request or clear conversation context.
Ask a short question if either essential choice remains ambiguous. Preserve explicit
dates, periods, information cutoffs, focus, coverage restrictions, language, prior
reports, and output destinations. A focus adds depth; a restriction changes coverage.

Read only the matching prompt, using paths relative to this skill's directory:

| Market | Cadence | Prompt |
| --- | --- | --- |
| China A-shares / CN / A股 | Premarket / 盘前 | [CN premarket](assets/prompts/A股盘前prompt.md) |
| China A-shares / CN / A股 | Postmarket / 盘后 | [CN postmarket](assets/prompts/A股盘后prompt.md) |
| China A-shares / CN / A股 | Weekly / 周度 | [CN weekly](assets/prompts/A股周度复盘prompt.md) |
| China A-shares / CN / A股 | Monthly / 月度 | [CN monthly](assets/prompts/A股月度复盘prompt.md) |
| U.S. equities / US / 美股 | Premarket / 盘前 | [US premarket](assets/prompts/us-premarket-prompt.md) |
| U.S. equities / US / 美股 | Postmarket / 盘后 | [US postmarket](assets/prompts/us-postmarket-prompt.md) |
| U.S. equities / US / 美股 | Weekly / 周度 | [US weekly](assets/prompts/us-weekly-review-prompt.md) |
| U.S. equities / US / 美股 | Monthly / 月度 | [US monthly](assets/prompts/us-monthly-review-prompt.md) |
| Crypto | Daily / 日报 | [Crypto daily](assets/prompts/crypto-daily-brief-prompt.md) |
| Crypto | Weekly / 周度 | [Crypto weekly](assets/prompts/crypto-weekly-review-prompt.md) |
| Crypto | Monthly / 月度 | [Crypto monthly](assets/prompts/crypto-monthly-review-prompt.md) |

For an unsupported market or cadence, explain the available choices. A new library
entry requires an explicit adaptation or maintenance request.

## Produce the brief

Execute the selected prompt in the current agent using its available research tools.
Keep its research responsibilities and analytical structure; apply user parameters
to this execution without rewriting the library prompt. Explicit user requirements
override prompt defaults. Resolve unspecified dates and actual market calendars at
research time according to the prompt.

Default report language: Chinese for A-shares, English for U.S. equities and Crypto.
An explicit language request overrides this default. Use the prompt's time windows,
source requirements, evidence distinctions, outlook, and self-review instructions.
Only use prior reports actually available in the authorized context.

Deliver the complete report, with sources and the research period/cutoff, in chat.
Save UTF-8 Markdown when the user requests a destination. If browsing or important
data are unavailable, state the limitation and complete the verifiable portions as
the prompt directs; distinguish non-current analysis from a current market brief.

## Export a prompt

When the user asks for the prompt rather than the brief, return the selected file
verbatim by default. For a customized prompt, preserve its body and add explicit
task parameters; change conflicting clauses only where needed. Deliver the complete
ready-to-copy prompt or save it at the requested destination. Keep the library intact.

## Maintain the library

Modify library files only for an explicit maintenance request. Inspect the affected
prompt and any supplied report evidence first. Distinguish an execution mistake
from a prompt defect; make the smallest justified correction.

Preserve research coverage, depth, information boundaries, measurement distinctions,
and deliverable clarity. Keep each prompt independently usable. Check the affected
scenario and any neighboring scenario the change could impact; label text review,
offline checks, and executed-report evidence separately.

Summarize the change, its reason, and the validation performed. Use Git history for
versions; ordinary brief generation and customization do not write back to assets.
