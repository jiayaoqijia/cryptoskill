// Package hlpskill embeds the agent skill (SKILL.md) so the binary can print
// or install it (`hlp skill`, AGENT-UX #33) without the repository at hand.
package hlpskill

import _ "embed"

// Markdown is SKILL.md, front matter included.
//
//go:embed SKILL.md
var Markdown string
