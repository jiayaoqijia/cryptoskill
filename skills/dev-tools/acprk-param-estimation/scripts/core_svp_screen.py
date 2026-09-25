#!/usr/bin/env python3
"""Quick core-SVP screen for LWE parameters (uSVP / primal attack, GSA model).

Screening only -- final numbers must come from lattice-estimator.  Core-SVP omits the
polynomial overhead that estimator 'rop' figures include, so it is typically 10-30 bits LOWER
than the estimator's rop for the same beta; compare beta, not bits, across tools.  Model:
  delta(beta) = ((pi*beta)^(1/beta) * beta / (2*pi*e))^(1/(2*(beta-1)))
  success if  sigma*sqrt(beta) <= delta^(2*beta - d) * q^(m/d),  d = m + n + 1 (Kannan embedding),
  optimising over the number of samples m <= m_max.
  cost_bits = 0.292*beta (classical) / 0.265*beta (quantum).

Usage:  python3 core_svp_screen.py N LOG2Q SIGMA [--secret-sigma S] [--m-max M]
Self-check: python3 core_svp_screen.py --selftest
"""
from __future__ import annotations

import argparse
import math
import sys


def delta(beta: int) -> float:
    return ((math.pi * beta) ** (1.0 / beta) * beta / (2 * math.pi * math.e)) ** (1.0 / (2 * (beta - 1)))


def usvp_beta(n: int, log2q: float, sigma: float, secret_sigma: float | None = None, m_max: int | None = None) -> tuple[int, int]:
    """Smallest beta (and the m achieving it) for the primal uSVP attack.

    If ``secret_sigma`` < sigma, the secret is rescaled (standard normalisation for small secrets).
    """
    m_max = m_max or 2 * n
    scale = 1.0
    if secret_sigma is not None and secret_sigma < sigma:
        scale = sigma / secret_sigma  # rescale secret coordinates -> volume factor
    best = None
    for beta in range(40, 2 * n + 2):
        lhs = sigma * math.sqrt(beta)
        dl = math.log(delta(beta))
        for m in range(max(1, n // 4), m_max + 1, max(1, n // 64)):
            d = m + n + 1
            # log volume^(1/d) with secret scaling: (m*log q + n*log scale)/d
            rhs = (2 * beta - d) * dl + (m * log2q * math.log(2) + n * math.log(scale)) / d
            if math.log(lhs) <= rhs:
                best = (beta, m)
                break
        if best:
            return best
    return (2 * n + 1, m_max)


def screen(n: int, log2q: float, sigma: float, secret_sigma: float | None = None, m_max: int | None = None) -> dict:
    beta, m = usvp_beta(n, log2q, sigma, secret_sigma, m_max)
    return {"n": n, "log2q": log2q, "sigma": sigma, "secret_sigma": secret_sigma, "beta": beta, "m": m,
            "classical_bits": round(0.292 * beta, 1), "quantum_bits": round(0.265 * beta, 1),
            "model": "core-SVP uSVP/GSA screen (NOT a final estimate)"}


def _selftest() -> int:
    # Monotonicity sanity: larger q -> weaker; larger n -> stronger. Toy values only.
    a = screen(512, 20, 3.2)["beta"]
    b = screen(512, 30, 3.2)["beta"]
    c = screen(1024, 30, 3.2)["beta"]
    assert b < a, (a, b)
    assert c > b, (b, c)
    assert 1.0 < delta(100) < 1.02
    print("core_svp_screen self-test OK", {"n512_q20": a, "n512_q30": b, "n1024_q30": c})
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("n", type=int, nargs="?")
    p.add_argument("log2q", type=float, nargs="?")
    p.add_argument("sigma", type=float, nargs="?")
    p.add_argument("--secret-sigma", type=float, default=None)
    p.add_argument("--m-max", type=int, default=None)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)
    if a.selftest or a.n is None:
        return _selftest()
    import json
    print(json.dumps(screen(a.n, a.log2q, a.sigma, a.secret_sigma, a.m_max)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
