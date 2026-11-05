# arXiv submission metadata — "Misconfigured by Default"

Prepared 2026-11-04. Package status: **ready for Girish's review; not yet submitted.**
The manuscript was submitted to *Empirical Software Engineering* on 2026-11-04
(Editorial Manager ID EMSE-D-26-00027; Zenodo replication package v1.0.7).

## Title

Misconfigured by Default: The Prevalence, Validity, and Tool Coverage of Kubernetes Misconfigurations in the Wild

## Author

Girish Mallya (sole author; affiliation as in the manuscript: Independent Researcher, Bellevue, WA, USA)

## Abstract (plain text, 247 words — paste as-is into the arXiv abstract field)

Kubernetes manifests are the de facto interface to production infrastructure, with permissive defaults: a workload specifying nothing runs with an automounted token, no resource limits, and no explicitly configured seccomp profile. We measure configuration in 151 Helm charts and 60 public GitHub repositories (16,243 documents, 2,811 workloads) with a 25-rule engine. We validated the engine on a 457-finding stratified sample: AI-generated pre-labels were author-checked -- the 92 protocol-sensitive rows adjudicated, a blinded 30-row subset (author--AI agreement: kappa = 0.526 [0.17, 0.84]) -- the rest retain accepted pre-labels, 16 corrected by a blinded re-labeling audit. Population-weighted precision is 0.676 [0.60, 0.81] (cluster bootstrap by source): ~18,600 [16,500, 22,100] of 27,460 raw findings are estimated genuine. Precision is rule-dependent: absence checks (seccomp, privilege escalation, root prevention) showed no false positives in the validation sample, while context-sensitive rules (committed secrets, host namespaces, probes) are mostly benign-by-design. The defaults dominate: tokens automount in 88.6% of production GitHub workloads, CPU limits -- a contested hardening practice -- are missing in 75.3%; 1.4% run a privileged container. Helm charts beat raw manifests on most practices, but by only 1.3--1.7x in workload-level prevalence. We also audit the auditors: on identical input, four scanners cover at most 16 of the 25 practices, diverging up to 1.4x on the same practice through counting semantics. Scored against reference labels (Helm arm, n = 126), they effectively detect 51--72% of the engine's reference-positive findings and flag 84--95% of reference-benign findings where a check exists, under our contextual protocol.

> Note for review: the LaTeX source's `\abstract{...}` block ends with a trailing
> fragment — "static analysis tools; measurement validity" — the tail of the
> keywords line that was absorbed into the abstract's closing brace during the
> Markdown→LaTeX conversion. It renders at the end of the abstract in the
> submitted EMSE PDF as well (both PDFs are text-identical). The 247-word
> abstract above excludes that fragment. Left as-is for fidelity to the
> submitted manuscript; flagging in case Girish wants it treated differently
> for arXiv.

## Categories

- **Primary: cs.SE** (Software Engineering) — the paper is an empirical
  software-engineering measurement study: a validated rule engine, a labeled
  validation sample with agreement statistics, and an evaluation of static
  analysis tools against reference labels. This is also where the EMSE
  readership looks.
- **Cross-list: cs.CR** (Cryptography and Security) — the subject matter is
  security configuration of production infrastructure, and the scanner audit
  speaks directly to the security-tooling community.
- Alternative if preferred: cs.DC (Distributed, Parallel, and Cluster
  Computing) covers the Kubernetes/cluster angle, but it is a weaker fit than
  cs.CR for this paper's contribution; recommendation is cs.SE + cs.CR.

## Comments field (draft)

21 pages, 3 figures. Replication package archived at https://doi.org/10.5281/zenodo.23969482. Submitted to Empirical Software Engineering.

## License

Recommended: **arXiv's default non-exclusive license to distribute**
(arXiv.org perpetual, non-exclusive, non-royalty-free distribution license).
It is the standard choice and is compatible with Springer's EMSE policies.
Alternative: CC BY 4.0, if maximal reuse rights are preferred; nothing in the
current plan requires it.

## Account and endorsement — read before upload day

- Upload requires Girish's personal arXiv account (to be created/logged in by
  him; nothing has been created as part of this prep).
- As a first-time submitter listing a non-institutional affiliation
  ("Independent Researcher"), arXiv may require an **endorsement** for cs.SE
  and/or cs.CR before the first submission is accepted. Endorsement is
  per-category and can take days. Recommendation: create the arXiv account
  early and check endorsement status for cs.SE/cs.CR well before the intended
  posting date, so endorsement latency doesn't gate the announcement.
- The actual upload (submitting `arxiv_submission.tar.gz` from this folder)
  is a separate step, to be done with Girish present, after he approves this
  package and the metadata above.

## Package contents (`arxiv_submission.tar.gz`)

- `main.tex` — manuscript source (v1.0.7, identical to the EMSE submission source)
- `main.bbl` — compiled bibliography (arXiv does not run BibTeX; the `.tex` keeps
  `\bibliography{references}` and uses this `.bbl`)
- `sn-jnl.cls`, `sn-basic.bst` — Springer class/style, bundled because arXiv does
  not ship them
- `figures/fig1_prevalence.pdf`, `figures/fig2_precision_forest.pdf`,
  `figures/fig3_scanners.pdf`

Verified 2026-11-04: a clean-room copy of exactly these files compiles with
pdflatex only (no BibTeX) to a 21-page PDF with all 3 figures, 0 undefined
citations/references, and extracted text identical to the submitted
`paper/submission/main.pdf`. See `arxiv_preview.pdf` in this folder.
