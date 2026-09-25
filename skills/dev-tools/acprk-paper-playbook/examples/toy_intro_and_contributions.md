# Toy introduction and contribution list — good vs bad

Invented paper T1 ("packed test polynomials"). Numbers are **illustrative** `[ill.]`.

## Contribution list

### Bad

```latex
\subsection{Our Contributions}
\begin{itemize}
\item We study LUT packing and prove Lemma 3 and Theorem 5.
\item Our method is 3.4x faster, although it uses more memory than [A23].
\item We investigate how to separate outputs.
\item We implement everything.
\end{itemize}
```

Problems: lemma numbers; concession inside contributions; "study/investigate";
numbers in the wrong bullet; no section pointers; no deliverable in the last bullet.

### Good

```latex
\subsection{Our Contributions}
Inspired by the observation that a test polynomial is read only inside a window of
width $2tw$, we determine the maximal number of tables that one blind rotation can
serve. Building on it, we propose packed test polynomials, a construction in which
every prior multi-value PBS is a special case. Our main contributions are:

\begin{itemize}
\item \textbf{From window width to a packing bound.} We show that the window width,
  not the number of tables, bounds the packing factor by $k\le N/(2tw)$, and construct
  interleaved test polynomials attaining it. This covers every table width up to
  $t=16$ at the standard ring degree, 75\% [ill.] of the table shapes in the
  benchmark circuits of \Cref{tab:coverage}.
\item \textbf{A unified view of multi-value PBS.} Multi-value PBS [A23] is the case
  $w=1$ and tree-based evaluation [B24] the case $k=1$; interior points of the $(k,w)$
  grid, unreachable by either, are optimal for mid-size tables. For any instance the
  best $(k,w)$ is selected by a closed-form rule (\Cref{sec:select}).
\item \textbf{Bootstrapping-free output separation.} We give the first evaluator that
  separates $k$ packed outputs with key switching only, costing one blind rotation
  plus $k$ key switches (\Cref{sec:alg}).
\item \textbf{Faster small-table evaluation.} Per-table latency drops by
  2.1--3.4$\times$ [ill.] over the strongest baseline in the same library, verified
  against cleartext outputs in \Cref{tab:main}.
\end{itemize}
```

## Opening funnel

### Bad

> FHE is a hot topic. Many papers have been written. PBS is slow. In this paper we
> make it faster.

### Good (structure only; wording illustrative)

> Fully homomorphic encryption (FHE) enables computation on encrypted data [..].
> Among FHE schemes, TFHE-like schemes are the ones of choice for non-linear
> functions over small integers, because each programmable bootstrapping (PBS)
> evaluates an arbitrary lookup table while refreshing noise [..]. This line of work
> [.., .., .., ..] has steadily reduced the cost of one PBS, yet circuits still pay
> one PBS per table. Concretely, a PBS factors into three stages:
> (i) modulus switching ..., cost O(n); (ii) blind rotation ..., cost n external
> products; (iii) sample extraction and key switching ..., cost O(nN).
> In this work we concentrate on the number of blind rotations per table. Every
> previous construction can be cast as
> \[ \min_{v}\ \#\mathrm{BR}(v)/k \quad \text{s.t. } v \text{ encodes } f_1,\dots,f_k. \tag{1}\]
> Whether structure in the test polynomial beyond its degree can lower (1) further
> has remained open.
