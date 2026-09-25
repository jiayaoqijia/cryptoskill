"""Tests for anon_check.py on small synthetic inputs (run: python3 -m pytest -q or python3 this_file)."""
# TOY: synthetic identities only ("Alice Example", "aexample")
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import anon_check as ac  # noqa: E402

DENY = ac.DenyList(["Alice Example", "aexample", "re:example\\s+univ(ersity)?"])

LEAKY_TEX = r"""\documentclass{llncs}
\begin{document}
\title{Toy}
\author{Alice Example}
\maketitle
In our earlier paper~\cite{a} we proved a bound.
See https://aexample.github.io/toy for code.
\end{document}
"""


def _kinds(findings):
    return {f.kind for f in findings}


def test_selftest_passes():
    assert ac.selftest() == 0


def test_tex_leaks_detected():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "main.tex"
        p.write_text(LEAKY_TEX)
        k = _kinds(ac.run([str(p)], DENY, []))
        assert {"tex-\\author", "first-person-self-cite", "deny-term"} <= k
        assert "url-deny-term" in k


def test_regex_deny_and_comment_downgrade():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "a.tex"
        p.write_text("% Example University internal note\nText from Example Univ.\n")
        fs = ac.run([str(p)], DENY, [])
        sev = sorted(f.severity for f in fs if f.kind == "deny-term")
        assert sev == ["HIGH", "MEDIUM"], sev


def test_allow_url():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "a.tex"
        p.write_text("\\url{https://github.com/thirdparty/lib}\n")
        assert "personal-host-url" in _kinds(ac.run([str(p)], DENY, []))
        assert "personal-host-url" not in _kinds(ac.run([str(p)], DENY, [r"github\.com/thirdparty"]))


def test_embedded_figure_path():
    if not shutil.which("pdflatex"):
        return
    with tempfile.TemporaryDirectory() as td:
        figdir = Path(td) / "aexample_figs"
        figdir.mkdir()
        (figdir / "f.tex").write_text("\\documentclass{article}\\pagestyle{empty}\\begin{document}x\\end{document}\n")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "f.tex"], cwd=figdir, capture_output=True)
        main = Path(td) / "m.tex"
        main.write_text("\\documentclass{article}\\usepackage{graphicx}\\begin{document}"
                        f"\\includegraphics{{{figdir / 'f.pdf'}}}\\end{{document}}\n")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "m.tex"], cwd=td, capture_output=True)
        pdf = Path(td) / "m.pdf"
        if not pdf.exists():
            return
        fs = ac.run([str(pdf)], DENY, [])
        assert any(f.kind == "pdf-embedded-path" and f.severity == "HIGH" for f in fs), [f.fmt() for f in fs]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
