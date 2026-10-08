---
name: fix-text-contrast-to-wcag-aa
description: Use when text or icons may fail contrast. Computes the WCAG ratio, picks the target 4.5:1 or 3:1 threshold by text size, and darkens the failing colour until it passes.
---

# Fix text contrast to WCAG AA

Brand greys and "subtle" placeholders routinely land at 3.1:1, which is fine for a heading and illegal for 14 px body text. Contrast is a measurable ratio, so compute it rather than eyeball it.

## Procedure

1. Convert both foreground and background to relative luminance per WCAG:
       def lum(hex):
           c = [int(hex[i:i+2],16)/255 for i in (1,3,5)]
           c = [x/12.92 if x <= 0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
           return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
       def ratio(a,b):
           la,lb = lum(a),lum(b); hi,lo = max(la,lb),min(la,lb)
           return (hi+0.05)/(lo+0.05)
2. Apply the threshold by role: `4.5:1` for normal text under 18.66 px bold or 24 px regular; `3:1` for large text, icons, borders and focus rings; `3:1` minimum for graphical objects.
3. Check every state, not just default — hover, disabled, placeholder, visited, error and dark-mode variants each get their own measurement.
4. Darken or lighten the foreground toward the accessible pole; do not drag the background if it is a brand surface. Adjust the text colour, keep the brand ink.
5. If the brand colour itself is the problem, keep it for large display use only and derive a darker `-text` variant for body copy: `--brand: #f97316; --brand-text: #b45309;`.
6. Never rely on opacity to create a "muted" label if it drops the ratio below 4.5:1 — pick a named grey that passes on the actual surface.
7. Re-check against the real background, including images and gradients. Sample the darkest region under the text; a caption over a photo passes on one half and fails the other.
8. Record the computed ratios next to each token so the next editor knows the margin.

## Pitfalls

- Testing only against pure white or pure black; a card at `#f7f7f7` lowers every ratio slightly and pushes borderline text under.
- Treating 18.66 px as "large" without checking boldness — the large-text exemption needs ≥ 24 px regular or ≥ 18.66 px bold.
- Using a checker on the hex before a CSS filter or blend mode renders it; the composited pixel is what users see and what the ratio must use.
- Assuming AA is enough everywhere: placeholders and disabled controls are exempt from WCAG, but 3:1 keeps them legible and should be your floor.

## Verification

    python3 - <<'PY'
    def lum(h):
        c=[int(h[i:i+2],16)/255 for i in (1,3,5)]
        c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
        return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
    def r(a,b):
        x,y=lum(a),lum(b); return (max(x,y)+.05)/(min(x,y)+.05)
    for fg,bg,label in [("#6b7280","#ffffff","body grey"),("#9ca3af","#ffffff","placeholder")]:
        print(label, round(r(fg,bg),2))
    PY

Every pair must print ≥ 4.5 (text) or ≥ 3.0 (large/graphics). Report the failing pairs, their old ratio, and the new colour that passes.
