#!/usr/bin/env python3
"""Convert paper/manuscript_draft.md into paper/latex/main.tex (complete).

Pipeline: split off the draft's meta block, abstract, and keywords; replace
[Key] citation markers with tokens; run pandoc (markdown -> latex) on the
abstract and body; post-process (unicode math, section-number stripping,
unnumbered Data availability section); inject into the main.tex skeleton
(the version of main.tex containing %%ABSTRACT%%/%%KEYWORDS%%/%%BODY%% —
kept as main_skeleton.tex after the first run).

Usage: python3 paper/latex/convert.py   (requires pandoc on PATH)
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MD = HERE.parent / "manuscript_draft.md"
CITE_KEYS = ["Rahman2023", "Minna2025", "Eom2026", "Yin2011", "XuZhou2015", "Ghorab2026"]

text = MD.read_text()
lines = text.split("\n")

# --- split -----------------------------------------------------------------
abs_start = next(i for i, l in enumerate(lines) if l.startswith("## Abstract"))
intro_start = next(i for i, l in enumerate(lines) if l.startswith("## 1. Introduction"))
ref_start = next(i for i, l in enumerate(lines) if l.startswith("## References"))
abstract_lines = lines[abs_start + 1:intro_start]
keywords = ""
abstract_body = []
for l in abstract_lines:
    if l.startswith("**Keywords:**"):
        keywords = l.replace("**Keywords:**", "").strip()
    elif l.strip() != "---":
        abstract_body.append(l)
body = "\n".join(lines[intro_start:ref_start])

# --- citation tokens ---------------------------------------------------------
for k in CITE_KEYS:
    body = body.replace(f"[{k}]", f"CITEKEY_{k}_END")

UNICODE_MATH = {"κ": r"$\kappa$", "×": r"$\times$", "≈": r"$\approx$",
                "≥": r"$\geq$", "≤": r"$\leq$", "→": r"$\rightarrow$"}


def pandoc(md_text):
    out = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex"],
                         input=md_text, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"pandoc failed: {out.stderr}")
    return out.stdout


def post(tex, abstract=False):
    for u, m in UNICODE_MATH.items():
        tex = tex.replace(u, m)
    for k in CITE_KEYS:
        tex = tex.replace(f"CITEKEY_{k}_END", rf"\cite{{{k}}}")
    if not abstract:
        tex = re.sub(r"\\section\{(\d+)\.\s*", r"\\section{", tex)
        tex = re.sub(r"\\subsection\{(\d+)\.(\d+)\s*", r"\\subsection{", tex)
        tex = tex.replace(r"\section{Data availability and replication package}",
                          r"\section*{Data availability and replication package}")
    return tex


abstract_tex = post(pandoc("\n".join(abstract_body)), abstract=True)
body_tex = post(pandoc(body))

skeleton_path = HERE / "main_skeleton.tex"
if not skeleton_path.exists():
    skeleton_path.write_text((HERE / "main.tex").read_text())
skeleton = skeleton_path.read_text()
out = (skeleton.replace("%%ABSTRACT%%", abstract_tex.strip())
               .replace("%%KEYWORDS%%", keywords)
               .replace("%%BODY%%", body_tex.strip()))
(HERE / "main.tex").write_text(out)
print(f"main.tex written ({len(out.split())} words incl. markup); keywords: {keywords[:60]}...")
