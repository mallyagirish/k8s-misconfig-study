# Lab notebook

## 2026-10-21 — Project start
- Project conceived as an independent (non-affiliated) empirical study of how Kubernetes workloads are actually configured in the open — whether the manifests people ship match the hardening guidance the ecosystem publishes. Research questions and full plan written (see study plan).
- Scaffolded repo; installed Helm v3.16.3 locally for chart rendering.
- Pilot goal: collect a first corpus (top Helm charts rendered with default values + raw manifests from public GitHub repos), run the taxonomy rule engine end-to-end, and sanity-check prevalence numbers before scaling.
- Taxonomy v1 seeded from the CIS Kubernetes Benchmark and NSA/CISA Kubernetes Hardening Guidance categories: security context, resource hygiene, image hygiene, RBAC, host namespaces, secrets handling, probes, deprecated APIs.
- Design decision: distinguish the two corpus arms (rendered Helm vs raw GitHub manifests) in all stats — the Helm-vs-raw split is RQ4 and a likely headline result.
- Design decision: RQ3 ("auditing the auditors") deferred to phase 2 — pilot validates the mining + rule engine first.

## 2026-10-21 — Pilot complete (same day)
- Helm arm: 41/60 top Artifact Hub charts rendered (~994 docs). Failures: 12 OCI-distributed charts (need `helm pull` support), 7 needing deps/values.
- GitHub arm: 9 seed repos, 1,721 files / 2,389 docs kept. argo-workflows dominates (1,185 docs) — stratification needed at scale-up.
- Analyzer ran clean: 3,383 docs, 460 workloads, 534 containers, 3,958 findings across 24 rules.
- Headline: curated charts are 2–3× better hardened than raw repo manifests (seccomp gaps 41% vs 89%; root-not-prevented 30% vs 65%; untagged images 0.8% vs 32.5%), but SA-token automounting (~90%+) and missing resource limits (~70–80%) are near-universal in both arms.
- Verdict: feasible; RQ4 contrast is real. Next: scale-up fixes, labeling sample, RQ3 tool-coverage matrix.

## 2026-10-21 — Scale-up complete
- Fixes shipped: Artifact Hub pagination (API caps limit at 60), OCI chart pulls, dependency-update retries with a budget cap (gitlab's dep update hangs >90s — budget exhaust is a feature, not a bug).
- Corpus v2: Helm 151 charts / 2,616 docs; GitHub 60 repos / 13,627 docs; total 16,243 docs, 2,811 workloads, 28,109 findings. Stats: results/stats_v2.json (pilot preserved as stats_pilot.json).
- Effect-size correction: Helm-vs-GitHub security gap narrowed from the pilot's 2–3× to ~1.3–1.7× once less-polished charts entered the sample. Pilot's top-60 was a best-case slice. Recorded honestly in the memo.
- New taxonomy insight: privileged containers concentrate in infrastructure DaemonSets (by design) — taxonomy v2 needs an infra-agent vs application workload split.
- Corpus concentration risk: top-3 GitHub sources ≈49% of v2 docs; kubescape/regolibrary contains intentional good/bad test fixtures. Source tagging (production / example / fixture) is now a prerequisite for prevalence claims.
- Analyzer hardened: real-world YAML includes dict-shaped `containers` fields and other malformed specs; rule engine now coerces/skips safely.

## 2026-10-21 (evening) — Sensitivity, RQ3, labeling sample
- Source tagging shipped (scripts/analyze_tagged.py): production-only cut (1,780 files / 438 workloads) keeps the headline intact (SA tokens 89.7%, no CPU limit 75.3%) — findings are not fixture-driven. One correction en route: kubernetes/examples initially tagged production by path heuristics; repo-identity override added.
- RQ3 complete on the Helm arm (identical input, default settings): kube-linter 0.8.3 (1,925 reports), kubeaudit 0.22.2 (3,379 results; prints its own deprecation notice), Polaris 10.2.5, Checkov 3.3.30 (6,178 failed checks). Matrix: results/tool_coverage_matrix.md. Headlines: best tool covers ~16/25 rules; digest pinning checked by 1 of 4 tools; committed Secrets and wildcard RBAC by none; CPU-limit counts spread 76–416 across tools vs 502 actual.
- Taxonomy v2 changes queued from RQ3: add read-only-rootfs rule (all four tools have it; we don't); keep infra-agent split.
- Labeling sample v2 built: 457 rows, seed 42, all SEC_PRIVILEGED + RBAC_CLUSTER_ADMIN_BINDING, stratified rest, ~10% hidden duplicates for kappa. Protocol: results/labeling_protocol.md. Awaiting Girish's labeling pass.
- Ops note: a runtime restart mid-run killed two background jobs; kube-linter output survived and validated, the rest were re-run cleanly. Verify-before-retry paid off.



## 2026-10-21 — Validation sample built (evening)
- Built stratified 302-finding hand-labeling sample from pilot findings (`labeling_sample_pilot_v1.csv`, seeded RNG for reproducibility).
- Design: ALL high-severity/rare findings (SEC_PRIVILEGED 11, RBAC_CLUSTER_ADMIN_BINDING 2, HOST_NETWORK 14, HOST_PID 7, HOST_IPC 2, SEC_DANGEROUS_CAPABILITY 7, SEC_RUN_AS_ROOT_EXPLICIT 4, RBAC_WILDCARD_{VERBS,RESOURCES} 29, SECRET_LITERAL_ENV 37, SECRET_COMMITTED sampled 40 arm-stratified) + all SEC_CAPABILITY_ADDED 30 + DEPRECATED_API 30 + IMG_{UNTAGGED,LATEST} 40 + 50-finding round-robin sample across the 10 common rules.
- Each row: sample_id, arm, rule, severity, kind, name, container, source_file, absolute corpus_path, blank label_TP_FP_unsure, blank reviewer_notes. Verified: all 302 corpus paths resolve.
- Labeling protocol to use: label each finding TP/FP/unsure against taxonomy v1; double-label a random 10% subset (S001..S030) with a second reviewer to report Cohen's kappa.

## 2026-10-21 — AI pre-labeling of the v2 validation sample (late evening)
- Girish approved AI pre-labeling with author verification (his labels remain ground truth).
- Built evidence packets for all 457 rows (extract_packets.py); judged each row with a written one-line justification → results/labeling_sample_v2_prelabelled.csv (prelabel + prelabel_reason + blank your_label/your_notes).
- Outcome: 328 TP / 122 FP / 7 unsure (draft precision ≈73%). Blind duplicate agreement 44/44 groups. Spot-checks (5 rows across rules) verified against raw YAML.
- Taxonomy-v2 signals: SECRET_COMMITTED must require credential material (12% as defined); SEC_CAPABILITY_ADDED must exclude least-privilege patterns (24%); host-namespace rules + SEC_PRIVILEGED need the infra-agent class; SECRET_LITERAL_ENV must exclude *_FILE/_NAME references and policy settings (40%).
- Extraction caveat found: duplicate-named ClusterRoles in Argo CD bundles (4 rows hand-verified).
- NEXT: Girish's verification pass on the pre-labeled CSV → final per-rule precision → taxonomy v2.

## 2026-10-22 — Methods audit: protocol harmonization + reliability fix

- An external review flagged, and I verified against the repo: (1) two conflicting labeling protocols existed — root labeling-protocol.md (v1, exploitability standard) vs results/labeling_protocol.md (v2, definitional; pre-labels follow v2). (2) The 44/44 blind-duplicate agreement is intra-rater consistency, not inter-rater reliability; the v1 design called for a second labeler on a 30-row overlap for Cohen's kappa.
- Fix kit built (scripts/build_fix_kit.py): results/labeling_protocol_v3.md is now the single governing protocol (v2 core + v1 amendments: IMG_NO_DIGEST two-tier, RES/REL production-scoping, APE/ROOT escalation-path test, DEPRECATED_API as rot tier; SECRET/CAPABILITY/infra refinements carried). v1 and v2 files banner-marked superseded, retained for provenance.
- Divergence list (results/divergence_list.csv): 92 of 457 rows are standard-sensitive — A: 14 IMG_NO_DIGEST (re-tier as TP-hardening), B: 42 RES/REL TPs from example/fixture sources (FP under v3), C: 29 APE/ROOT TPs needing escalation-path verification (none auto-flip on packet evidence), D: 7 evidence-absent unsure rows (kustomize-injected images K8S-113/207/236/371 + unlocatable K8S-189; excluded from precision denominators, disclosed).
- Blinded kappa subset built (results/kappa_subset/): 30 unique-content rows across all 25 rules + packets + instructions; scripts/score_kappa.py computes author-vs-AI Cohen's kappa (smoke-tested). NEXT: Girish labels the blind subset cold (~30-60 min), then the verification pass (divergence rows first).

## 2026-10-22 (evening) — Second external review: RQ3 headlines corrected, engine v3

- A second external review was verified claim-by-claim against the raw tool outputs and engine code. Two RQ3 headlines were WRONG and are corrected in README + matrix: (1) the "CPU limits ~5x swing (76 vs 416)" — kubeaudit's LimitsNotSet (421, no limits at all) + LimitsCPUNotSet (76, limits block without CPU) = 497 vs engine 502 (~1% agreement; memory 474 vs 479); the real spread is 343-497 (~1.4x, counting units). The matrix's data rows were right; the narrative cherry-picked 76. (2) "Wildcard RBAC flagged by none" — the matrix itself lists Checkov CKV_K8S_49 at 29 findings; kube-linter ships wildcard checks off by default, so the legend now reads "no default-enabled check". The Secrets claim is reframed: no tool inspects Secret CONTENTS for credential material (~88% of sampled Secrets are empty/placeholder; the gap is the credential-bearing minority).
- Engine v3 (analyze.py + analyze_tagged.py): SA-token rule joins the ServiceAccount object's own automount flag (same file); init containers excluded from probe rules; seccompProfile.type=Unconfined counts as no profile; containers with no image field are not scored for IMG rules (counted as containers_no_image). Re-ran both arms on the identical corpus: findings 28,109 -> 27,460 (stats_v3.json / findings_v3.jsonl / stats_tagged_v3.json). Biggest deltas: Helm probe findings -30% (303->211 liveness) — a third of v2 probe findings were on init containers; SA barely moves (Helm 88.8%->85.1% of workloads, GitHub 96.4%->96.2%) so the v2 upper bound was tight; seccomp Helm 363->370.
- Non-independence addressed in results/cluster_prevalence.md: 52.9% of GitHub findings repeat a seen (kind,name,container,rule) key, but cluster-level presence is ecosystem-wide (SA automount in 94% of repos / 90% of charts; privileged only 22% / 8%).
- Reproducibility: GitHub arm was collected with git clone --depth 1 and no SHAs logged; the local clones were untouched since collection, so HEAD SHAs for all 60 repos are now recorded in results/github_commit_shas.json.
- README scope fixes: "16,243 manifests" -> YAML documents (2,811 workloads); whole-corpus counts (415/341) removed from the Helm-arm RQ3 claims.
- NEXT: Girish's blind kappa subset + verification pass (protocol v3, divergence rows first); then taxonomy v2 (adds readOnlyRootFilesystem) and the paper draft.

## 2026-10-27 — Blinded kappa scored; protocol v3 addendum adopted

- Girish labeled all 30 blinded kappa rows (20 TP / 10 FP / 0 unsure). Agreement with the AI pre-labels: 24/30 (80%), Cohen's kappa = 0.526 — below the 0.7 target, and the decomposition matters more than the headline: the pre-labels were produced under v2, so the measurement is partly cross-standard.
- Four disagreements (K8S-086, 217, 300, 345; all RES_*/REL_*) are v3 amendment 2 siding with the author's FP over the v2 definitional TP — the known divergence class B, settled at scale in the verification pass. K8S-300 also exposed a tagging miss (kustomize testdata filed under a production-tagged repo).
- Two genuine judgment calls adjudicated into rule-level amendments, drafted as results/labeling_protocol_v3_addendum.md (pending author sign-off to commit): (10) SEC_DANGEROUS_CAPABILITY joins the infrastructure class when the container runs over a drop-ALL baseline and the caps serve its node-infra function — K8S-432 (Cilium mount-cgroup) FP infra-need; scan of all 17 sample rows for this rule: no pre-label changes. (11) RBAC wildcards confined to the project's own API groups in its shipped controller role are FP (standard operator pattern) — K8S-452 (Flux) FP; ratifies the existing Flux/Kasten/linkerd FP pattern; K8S-012 (Crossplane) flagged for per-grant adjudication in the verification pass. (12) Content beats tag: testdata/fixtures paths count as fixture for production scoping regardless of the repo tag — K8S-300 reclassified; K8S-183/297/375/446 confirmed.
- Kappa is logged as measured (0.526); final labels will be produced under v3 + addendum in the verification pass, and the methods section reports the sequence (v2 pre-labels -> kappa -> adjudication amendments -> v3 verification).
- NEXT: author sign-off on the addendum, then the verification pass (divergence rows first, 92), then final per-rule precision and taxonomy v2.

## 2026-10-27 (evening) — Provisional precision under v3 + addendum

- Computed provisional per-rule precision by applying the verification worklist's v3 recommendations to the 92 divergence rows over the v2 pre-labels (results/precision_provisional.md). Overall 0.630 [0.584, 0.673] (279 TP / 164 FP, 7 TP-hardening tiered, 7 excluded) vs the ~0.73 v2 definitional draft — the gap is the v3 contextual standards: production scoping (RES_NO_MEM_LIMIT 0.375, REL_NO_LIVENESS_PROBE 0.214), credential-material (SECRET_COMMITTED 0.125), infra class (HOST_NETWORK 0.250, HOST_PID 0.214), least-privilege exclusions (SEC_CAPABILITY_ADDED 0.235). Clean rules: SEC_NO_SECCOMP, SEC_APE_NOT_DISABLED, SEC_ROOT_NOT_PREVENTED, IMG_LATEST all 1.000; SA_TOKEN_AUTOMOUNTED 0.857; SEC_DANGEROUS_CAPABILITY 0.824 under amendment 10.
- Adjusted true findings ~19,062 of 27,460 raw — with a frame-drift caveat: the sample was drawn from engine-v2 findings while population counts are v3 (SEC_PRIVILEGED sample 79 > v3 population 74; HOST_IPC 17 > 16). Precision stands; adjusted prevalence for small-count rules needs a row-level sample-to-v3 reconciliation before the paper run.
- K8S-012 resolved: per-grant inspection shows one wildcard grant in the core group (verbs * on secrets) alongside five Crossplane-group grants, so amendment 11's own-groups test fails and the row stays TP. The addendum flag is closed with no label change.
- NEXT: Girish's verification pass on the worklist (his overrides recompute everything), the sample-to-v3 reconciliation, then taxonomy v2 and the draft.

## 2026-10-27 (late) — Author verified the divergence worklist; precision stands

- Girish reviewed the 92-row verification worklist and the provisional precision results and accepted the v3/addendum recommendations without override ("the numbers look good"). The divergence rows now carry author-verified labels; precision_provisional.md is re-marked VERIFIED. Non-divergence rows stand on their pre-labels under blank-equals-accept.
- Standing results: overall precision 0.630 [0.584, 0.673]; per-rule table in results/precision_provisional.md (rename to precision_final at the paper run, after the frame reconciliation).
- NEXT: sample-to-v3 frame reconciliation for adjusted prevalence; taxonomy v2; checker release packaging; January EMSE draft.

## 2026-10-28 — Sample-to-v3 reconciliation adopted; manuscript first draft

- The reconciliation (results/reconciliation_v3_DRAFT.md, prepared by background analysis) was adopted as the basis for the paper's figures: 451/457 sampled rows persist in engine v3; overall precision on the matched frame 0.633 [0.587, 0.676]; adjusted true findings 19,199; only REL_NO_READINESS_PROBE moves (0.467 -> 0.538). The sample>population paradox is explained by design (all-findings rules + ~10% intentional duplicates; 457 rows = 413 distinct keys, all 44 duplicate pairs agree). precision_provisional.md updated accordingly (caveat marked resolved, readiness row + adjusted total replaced, distinct-key sensitivity 0.626 noted).
- First full manuscript draft written: paper/manuscript_draft.md ("Misconfigured by Default") — abstract, intro, RQs, method (corpus, engine, tool audit, validation protocol with the kappa decomposition reported openly), results (RQ1 prevalence, RQ4 curation 1.3-1.7x, RQ2 precision + taxonomy v2 with the five FP context classes, RQ3 tool audit), discussion, threats, related-work skeleton, data availability. One number caught and fixed during drafting: Polaris coverage is ~13 of 25, not ~15.
- REMAINING before submission: bibliography verification pass (Section 7 citations are structural), LaTeX conversion to Springer format, Zenodo DOI at submission, author proofread. Target: January 2027 EMSE submission.

## 2026-10-28 (afternoon) — Related work rewritten against the three named prior studies

- An external review of the repo (via ChatGPT) named the three adjacent works the paper must differentiate from; all three were located and verified bibliographically: Rahman, Shamim, Bose & Pandita, TOSEM 32(4) 2023 (DOI 10.1145/3579639; 2,039 manifests/92 repos, 11 categories, SLI-KUBE, practitioner fix-agreement validation); Minna, Massacci & Tuma, EMSE 30:132 2025 (DOI 10.1007/s10664-025-10688-0; Artifact Hub charts, 7 tools by default policies, LLM mitigation, subset FP check); Eom, Suk & Hwang, ISSTA 2026 (DOI 10.1145/3832297; 10 scanners, constructed benchmark of 4,109 files/281 misconfigurations, best recall 43.8% static).
- Section 7 rewritten: per-study differentiation plus a positioning table (corpus, practices, ground truth, tool treatment, production/fixture separation, prevalence). Our defensible claim: verified per-rule precision on natural corpora + FP context taxonomy + counting-semantics analysis + two-arm curation comparison. References now carry the three verified entries. The review's other P0s were already closed (validation complete; README status text was stale and has been corrected in a8cf53c).
- NEXT (author-approved sequence): per-tool detection accuracy on the verified Helm-arm ground-truth rows, then fold into RQ3 (the positioning table already anticipates it).

## 2026-10-28 (later) — Per-tool accuracy against verified ground truth

- New analysis (results/tool_accuracy.md + .csv): each scanner's reports on the Helm arm were joined object-by-object to the 126 Helm-arm validation rows (73 verified TP, 50 FP, 2 TP-hardening, 1 excluded). Joins reconcile with the coverage matrix on 64/65 mapped checks; file-less tools (kubeaudit, Polaris) join on (kind, name, container) with a saturation rule for cross-chart name collisions (2 Polaris rows AMBIGUOUS_JOIN, excluded from its rates). Mapping judgment calls documented (different-property checks treated as no check; Checkov's cluster-admin cell unmappable).
- Results: TP detection where a check exists — kubeaudit 0.98, Polaris 0.93, kube-linter 0.90, Checkov 0.76 (its CKV_K8S_23 systematically misses explicitly-root containers, 8 of 15 misses). Effective TP detection (no-check = missed): Polaris 0.75, Checkov 0.64, kubeaudit 0.55, kube-linter 0.52. FP-flagging where a check exists: 0.86–0.95 for all four — the tools share the naive engine's context blindness almost exactly.
- Folded into the manuscript: abstract, contribution 4, Section 3.3 method note, a new RQ3 subsection with the accuracy table, and the positioning table's tool-treatment cell. RQ3's conclusion sharpens: the tools' deficit is coverage and context, not detection.
- REMAINING before submission: residual bibliography verification, LaTeX conversion, Zenodo DOI, tagged release, author proofread. Target January 2027 EMSE.

## 2026-10-28 (evening) — Independent second-rater packet built

- Prompted by the external review round (both reviews converged on it): the validation has no independent human labeler — kappa 0.526 is author-vs-AI, and the remaining rows were accepted by verification rather than independently labeled. A blinded packet for a second human rater is now built and ready to hand over.
- Design (scripts/build_second_rater_packet.py, seed 20261028): frame = the 450 rows with final verified labels, deduped to 407 distinct finding keys; 150 drawn, rule-stratified (proportional, floor 2, cap 14), split Batch A (98) / Batch B (52) so Batch A alone is a valid measurement if the rater's time runs out. Draw composition (author-side, in sample_manifest.md): 89 TP / 59 FP / 2 TP-hardening.
- Packet (results/second_rater/packet/): README (instructions, ~2–3h for Batch A at 1–2 min/row), protocol_for_rater.md (v3 + addendum amendments 1–12 restated as decision rules; process history and all sample IDs stripped; the adjudicated cases kept only as anonymized worked examples), blind_sample.csv (empty label columns), packets.md + packets.jsonl (evidence packets re-keyed to blinded IDs), mapping_audit.md (the check-to-rule matrix plus the 10 documented judgment calls as an agree/disagree checklist — covers the reviews' mapping-validation ask as an optional second task).
- Blinding hygiene: leak-checked — no sample IDs, no label fields, no pre-label/final-label references anywhere in the packet. The sealed key (blind_id -> sample_id + final label) is gitignored and stays local until the rater returns the sheet, then gets committed with the replication package. Scorer: scripts/score_second_rater.py (agreement, 3-class and binary kappa, confusion, per-rule agreement, disagreement list for adjudication) — smoke-tested on a synthetic return.
- STATUS: ready to hand to a rater; recruiting the rater is the author's step. Once labels return: score, adjudicate disagreements with the rater, log kappa in the notebook, and report in the manuscript's methods/threats.

## 2026-10-28 (evening, later) — Weighting note, claim scoping, bibliography completed, CITATION.cff

- Statistical weighting (from the review round's checklist): the manuscript now distinguishes the two precision aggregates explicitly in Section 3.5 — the sample-row rate 0.633 (the stratified sample over-represents rare rules by design) vs the population-weighted 0.699 (19,199 / 27,460), with a note that all adjusted prevalence is built per rule and is identical under either. A standards sensitivity sentence is included: the same sample under the superseded v2 definitional standard scores ~0.73; the gap is the v3 amendments working. Section 4.3 carries the pointer.
- Claim scoping (review round, item 3): the introduction's headline is now corpus-bounded ("in this corpus"), the security-effort sentence is framed as a pattern the data suggests, and the conclusion closes with an explicit scope sentence — the claims describe public, production-shaped manifests and rendered charts, not the private state of running clusters.
- Bibliography: the last pending references are pinned and verified — Yin et al., SOSP 2011 (configuration errors in commercial and open-source systems) and Xu & Zhou, ACM Computing Surveys 47(4):70, 2015 (DOI 10.1145/2791577) — now cited in Section 7.1 and listed in References, which no longer carries a "verification pending" note for named works.
- CITATION.cff added at the repo root (title, author, repo, Apache-2.0, abstract); version and date-released fields land with the tagged release.
- REMAINING before January 2027 EMSE submission: second-rater labels (packet out, awaiting a rater), LaTeX conversion + Springer formatting (incl. the formal AI-use declarations line), Zenodo DOI at the tagged release, author proofread.

## 2026-10-28 (night) — LaTeX conversion compiles

- paper/latex/ now holds the submission-format build: convert.py (markdown -> LaTeX pipeline: splits the draft's meta block/abstract/keywords, maps the bracket citation keys to \cite, converts unicode math, strips section numbers, unnumbers Data Availability), main_skeleton.tex (article-class preamble + title block + Declarations), main.tex (generated), references.bib (the five verified papers + CIS/NSA/Kubernetes/tool documents).
- Declarations added per Springer requirements: funding (none), competing interests (none), ethics (n/a — public artifacts), sole-author contributions, and a Use of AI tools statement disclosing the v2 pre-labeling with v3 author verification and the AI assistance in development/editing, with author responsibility stated.
- Compiles clean with pdflatex + bibtex: 12 pages A4, no errors, no undefined citations. Known polish items for the submission pass: swap article for Springer's sn-jnl class, and tune the three wide tables (worst overfull ~51pt, positioning table) to the journal measure.
- REMAINING before January 2027 EMSE submission: second-rater labels (packet out), author proofread of the compiled PDF, sn-jnl swap + table polish, tagged release + Zenodo DOI.
