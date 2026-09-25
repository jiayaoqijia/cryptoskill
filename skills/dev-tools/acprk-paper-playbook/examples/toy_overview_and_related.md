# Toy technique overview and related-work table

Invented papers; all numbers and citations illustrative.

## Related-work table (T3, PSI)

```latex
\begin{table}[t]
\centering\scriptsize
\caption{Asymptotic comparison of unbalanced PSI protocols. $n$: server set size;
$m$: client set size; $\sigma$: statistical security; $\lambda$: computational
security. $\dagger$: semi-honest only. $\ddagger$: requires FHE.}
\label{tab:related}
\renewcommand{\arraystretch}{0.92}
\begin{tabular}{llccc}
\toprule
Technique & Method & Communication & Server comp. & Rounds \\
\midrule
\multirow{2}{*}{OPRF-based} & [E21]$^\dagger$ & $O(n\,(\sigma+\log nm))$ & $O(n)$ & 2 \\
                            & [G23]          & $O(n\,\sigma)$           & $O(n)$ & 2 \\
\midrule
FHE-based & [F22]$^\ddagger$ & $O(m\log n)$ & $O(n)$ HE ops & 1 \\
\midrule
\textbf{Ours} & & $O(n\,\sigma/c)$ & $O(n)$ & 2 \\
\bottomrule
\end{tabular}
\end{table}
```

Rules shown: caption defines every symbol; daggers mark scope; last row "Ours"
matches the formula in the abstract.

## Contrasting-verb bullets (T1)

> Recently, two independent lines of work exploit the structure of the test
> polynomial rather than its degree alone:
> - **Multi-value PBS** restricts *what* is encoded: several tables share one
>   polynomial whose coefficients factor through a common term [A23]; however, it
>   requires tables with a common factor, leaving general tables open.
> - **Tree-based PBS** restricts *how* a table is read: a large table is split into
>   levels evaluated by successive rotations [B24]; the number of rotations grows with
>   the table size.

## Bad vs good overview headings

| bad | good |
|---|---|
| "Why packing is needed" | "Window width, not table count, bounds the packing factor." |
| "Where the cost goes" | "Output separation is linear and therefore free of bootstrapping." |
| "The SAT model" | "Clustering turns a trail search into a model-counting problem." |
| "Our hashing" | "Fingerprint length alone fixes the false-positive rate." |

## Tiny worked example (T2)

> Take the 4-bit S-box S = [6,4,12,5,0,7,2,14,1,15,3,13,8,10,9,11] [ill.]. Its DDT has
> maximum entry 4 [ill.], so a single-trail bound gives 2^{-2} per active S-box. The
> input difference 0x3 maps to 0x3 with probability 2^{-2} [ill.] through two rounds
> via 4 [ill.] distinct characteristics, so the differential probability is 2^{-1}
> [ill.], a factor of 2 [ill.] above the single-trail bound.

Every number in such an example must be recomputable by a script (e.g. with the
`cryptomath.symmetric` DDT helper) listed in `EVIDENCE.md`.
