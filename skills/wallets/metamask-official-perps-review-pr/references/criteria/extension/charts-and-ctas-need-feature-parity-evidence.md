# Charts and CTAs Need Feature-Parity Evidence

- **Loading and loaded section order differ**: Reserve space for every conditional section above stable controls, including a populated watchlist. Compare loading and loaded layouts with that data present.
- **Measurements ignore rendered state**: Invalidate cached widths when selection, icons or labels change. Keep measurement out of unused layouts and live-data render loops; prove the clear/overflow control stays reachable at the smallest supported width.

A chart or CTA change keeps the old chart context, gates the CTA by capability, and ships event coverage or an explicit deferral.

- **Advanced chart drops volume or realtime signal** — preserve old chart context unless intentionally removed.
- **CTA shown for unsupported asset/context** — gate by capability, not generic asset presence.
- **New CTA lacks analytics** — action buttons need event coverage or explicit deferral.
