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

## 2026-10-28 (night, later) — Review round 3 addressed: terminology, provenance, aggregate CI, new related work

- A third external review (same reviewer, updated) was triaged; its actionable items are now in the manuscript (22 edits): (1) TERMINOLOGY — the kappa measurement is renamed throughout from "inter-rater reliability" to "blinded author–AI agreement" (abstract, contribution list, Sections 3.4, 6, 7.1), with the protocol-version confound stated alongside kappa in 3.4 itself and the in-preparation two-human measurement (the second-rater packet) named there. (2) PROVENANCE — Section 3.4's Verification paragraph now states the label provenance exactly, computed from the files: of 451 matched rows, 111 (25%) carry author-produced or individually adjudicated labels (30 blind-labeled + 87 adjudicated divergence rows, 6 in both sets) and 340 (75%) retain AI pre-labels accepted in the verification pass; the dataset is described as "AI-annotated and author-adjudicated, not independently human-labeled" in both 3.4 and the threats section. (3) AGGREGATE UNCERTAINTY — per-rule binomial variances propagated: adjusted total 19,199, sd ~708, 95% CI [17,810, 20,587]; weighted precision 0.699 [0.649, 0.750]; recorded in precision_provisional.md and reported in Sections 3.5/4.3/abstract, with the extrapolation (not a verified count) stated. (4) Scanner claims scoped in 4.4 (sample-based; flagging shares are not population FPRs); "four most widely used" softened to "four widely used" in manuscript, README, and abstract. (5) Section 5 gains the exposure-vs-vulnerability scope note (SA token example). (6) NEW RELATED WORK verified and cited: Ghorab, Abdel Latif & Saied, arXiv:2609.27030 (Sep 2026) — taxonomy from 2,662 Stack Overflow issues + LLM repair; differentiated in 7.1 (developer reports vs manifest content; repair presupposes the validity we test). The draft header's stale "bibliography verification pending" note is corrected.
- LaTeX regenerated and recompiled: 13 pages, no undefined citations.
- Still open (author's steps): recruit the second rater; decide whether to hand-inspect all 451 matched rows (would upgrade the provenance claim); proofread; sn-jnl swap + table polish; tagged release + Zenodo DOI at submission.

## 2026-10-28 (night, final) — Review round 4: abstract rewritten, cluster bootstrap, secrets claim scoped

- A fourth review (abstract-focused) was triaged and worked. CLUSTER BOOTSTRAP (new script scripts/cluster_bootstrap.py; results/cluster_bootstrap.md; 2,000 replicates, sources resampled within arm, seed 20261028; 441 decided matched rows in 35 GitHub + 56 Helm clusters): weighted precision 0.699 [0.623, 0.840]; adjusted total 19,199 [17,120, 23,071]; pooled sample precision 0.633 [0.527, 0.714]; kappa 0.526 [0.167, 0.841]. The cluster intervals supersede the binomial/Wilson row-level intervals everywhere in the manuscript (Sections 3.5, 4.3, abstract); precision_provisional.md carries a superseded note.
- ABSTRACT REWRITTEN (340 -> 303 words): validation sentence now names the actual process (92 adjudicated + blinded 30 + retained pre-labels); population-weighted figure is the headline precision with the cluster interval; "explicit-danger rules" replaced by "unambiguous absence checks" (the two senses of 'explicit' are now kept apart); denominators stated (1.4% = production GitHub workloads); CPU limits flagged as a contested hardening practice in-line; Helm sentence carries the ratio with the selection-bias story moved to Section 4.2 (which already had it); "purely through counting semantics" -> "largely through"; tool claims scoped to the Helm arm with n=126 and "the engine's verified-genuine findings" (not recall); secrets claim scoped to the configuration run with Checkov's separate secrets framework acknowledged (also fixed in Section 4.4, plus a paragraph there stating the benign benchmark is our contextual standard, not the tools' own specification). Keywords verified complete (the reviewer's copy was truncated mid-word in transit; the file's line is intact). Helm chart names+versions and GitHub SHAs confirmed pinned in the logs and now stated in Data Availability.
- Abstract is 303 words vs Springer's ~150-250 guidance: one thread (the secrets sentence is the candidate) still has to go at submission if EMSE enforces the limit. Author's call then.

## 2026-10-28 (night, close) — Review round 5 (strategic): README reconciled, fallback sensitivity, wording

- A fifth, strategy-scoped review converged with the existing plan on most points (independent validation first, reproducibility release, benchmark-before-second-paper, endeavor framing). Its verifiable catches were checked and fixed: (1) README's Validation section still said "validation is complete ... verified the full sample" and "inter-rater reliability" — rewritten to match manuscript 3.4/3.5 exactly (provenance counts 111/340, author-AI agreement terminology, cluster-bootstrap intervals, second-rater in preparation); the Status line softened to match. (2) A real duplicated "blinded / blinded" in the contributions list (artifact of the round-3 terminology edit) is fixed; the positioning table's "author-verified" now reads "author-adjudicated". (3) BOOTSTRAP FALLBACK SENSITIVITY run: 42 of 50,000 rule-replicates have no decided rows for a rule (IMG_NO_DIGEST 23 of them); full-sample, pooled, and drop-and-renormalize fallbacks all give the identical weighted-precision interval [0.623, 0.840]. Recorded in cluster_bootstrap.md and one sentence in Section 3.5. (4) Scanner versions verified as already pinned: tool_coverage_matrix.md records kube-linter 0.8.3, kubeaudit 0.22.2, Polaris 10.2.5, Checkov 3.3.30, all default settings — confirmed against the binaries in bin/ and .venv-checkov.
- Deferred, named: cluster-bootstrap intervals for the RQ4 Helm-vs-GitHub ratios (released stats are arm-level aggregates; needs a per-source stats pass — January packaging sprint). Benchmark release (their option A) matches the planned checker + Zenodo release; a remediation study (their option B) is a new candidate for the post-submission shortlist; longitudinal re-collection (C) is already shortlist item 3.

## 2026-10-28 (evening) — EMSE submission moved up to this week; submission package built

- Girish moved the EMSE submission from January 2027 to this week. Verified against the journal's own submission guidelines (link.springer.com/journal/10664, crawled today): Editorial Manager (editorialmanager.com/emse), article type Research Papers; SINGLE-blind review (no anonymization needed); abstract must be 150-250 words; keywords 4-6 (we have 6); a "Statements and Declarations" section is mandatory (missing declarations are returned as incomplete); no submission or publication fee (Open Choice optional after acceptance); first decision typically < 3 months. EM compiles uploads on TeX Live 2018, flat files only; Springer's author support calls the inlined-.bbl variant the most reliable upload.
- ABSTRACT CUT 303 -> 249 words (the secrets sentence and the selection-bias clause were dropped from the abstract only; both remain in Sections 4.2/4.4; every headline number survived).
- SN-JNL CONVERSION DONE: class + sn-basic.bst obtained (vendored copy via rstudio/rticles; EMSE's own linked macro zip is the deprecated svjour3 package); skeleton now sn-jnl [pdflatex, sn-basic] with the declarations retitled "Statements and Declarations"; amsmath added (the class hook requires it); convert.py breaks long rule-name tokens at underscores inside tables; bib years added to the three living-document entries. Compiles clean: 16 pages, 0 undefined citations, no overfull boxes.
- SUBMISSION BUNDLE in paper/submission/: main.tex + references.bib + sn-jnl.cls + sn-basic.bst, a self-contained main_bbl.tex (bibliography inlined), main.pdf, cover_letter.md (draft). Both variants verified to compile from a flat directory, EM-style. Remaining (Girish): proofread; Zenodo toggle on the repo (then Muse tags the release, DOI mints, DOI goes into Data Availability + CITATION.cff); Editorial Manager registration + upload + approve + submit. arXiv after the journal submission (first-submission endorsement may take days). The paper is submitted BEFORE second-rater labels return; the manuscript already frames that labeling as in preparation, and the packet is ready if reviewers ask.

## 2026-11-02 — Review round 6: validation wording pass, two new references, citation fix

- WORDING PASS (external reviewer's catch; the README was fixed in round 5 but the manuscript was not): "verified ground truth", "author-verified labels", "verified true/false positives" and variants replaced throughout the manuscript and both LaTeX sources with "reference labels" / "protocol-based reference labels (AI-annotated, author-adjudicated)" / "reference-positive" / "reference-benign" terminology, matching Section 3.4's provenance statement (111/451 author-produced or adjudicated, 340 retained pre-labels). Targeted grep is clean in all three text sources. Also scoped: the introduction's opening adoption claim softened (no citation existed for it); "the four most widely adopted" -> "four widely used"; the contributions list now scopes the coverage/context deficit claim to the versions and default configurations evaluated.
- NEW RELATED WORK, verified against publisher/arXiv records and added to Section 7.1, the positioning table (now 7 columns), and both bibliographies: Zhang, Paul, d'Amorim & Rahman, "Configuration Defects in Kubernetes", IEEE TSE 2026 (DOI 10.1109/TSE.2026.3659785) — 719 mined defects, 15 categories, 8 tools at category level; differentiated on ground truth (historical defects vs protocol reference labels on identical input, incl. false-positive flagging and counting semantics). Bufalino, Martin-Navarro, Di Francesco & Aura, "Inside Job", Proc. ACM on Networking 3 (CoNEXT) 2025 (DOI 10.1145/3749220) — 634 network misconfigurations across 287 applications, disclosure, 30+ fixes; positioned as the practitioner-impact end vs this study's measurement end.
- CITATION DEFECT FOUND AND FIXED: the six in-text citations in Section 7 had survived the sn-jnl conversion as literal "CITEKEY_..._END" tokens (pandoc escaped the token underscores, so convert.py's replacement never fired), and the compiled bibliography contained only the four \nocite'd living-document entries. Tokens converted to \cite in both LaTeX sources; convert.py now catches the escaped form and knows the two new keys. Bibliography is now 12 entries; both submission variants recompile clean (18 pages, 0 undefined citations, 0 overfull boxes). The earlier 16-page count was partly an artifact of the truncated reference list.
- CORPUS DOCUMENTATION: Section 3.1 now states the Artifact Hub selection precisely (registry package search, kind = Helm, most-starred, collected 2026-10-21, names/versions pinned in results/helm_render_log.json) and the GitHub discovery criteria from the collectors (seed sets 9 + 12; four search queries sorted by stars; size 200 KB-400 MB; discovery cap 40).

## 2026-11-03 — Review round 7: second-rater framing removed

- Girish decided not to use a second rater for this study at all (2026-11-03), superseding the submit-before-labels plan of 2026-10-28: there is no planned independent labeling pass, and the manuscript no longer says there is. The blinded packet in `results/second_rater/` stays in the repo as a preparation artifact; it is not part of the study as reported.
- REMOVED, in the manuscript, both LaTeX sources, and the README: Section 3.4's "A two-human measurement — an independent researcher labeling a 150-row subsample under the frozen v3 protocol, blind to all existing labels — is in preparation; the packet ships in the replication package" is replaced by "The κ figure is the only agreement measurement in this study; no independent second labeling was performed." README's Validation section and Status line lose the "second-rater labeling ... in preparation" sentences the same way (Validation now ends the provenance paragraph with "with no independent second labeling"; the `results/second_rater/` pointer is gone from the README).
- LIMITATIONS: Section 6 (Construct validity) previously ended the provenance discussion "...single-author and AI-assisted; an independent human labeling under the frozen protocol is in preparation and is the obvious strengthening step." It now reads "...single-author and AI-assisted: every reference label rests on one author's adjudication, and no independent labeling pass checks it. We regard this as the validation's main limitation."
- UNCHANGED: all numbers and provenance counts (111/451 author-produced or adjudicated, 340 retained pre-labels); the abstract (no second-rater mention; still 249 words by the package count); Section 3.4's statement that the dataset is "AI-annotated and author-adjudicated, not independently human-labeled" — already the current-state framing. Submission package rebuilt and recompiled (see compile results in the round-7 commit).

## 2026-11-03 — Review round 8: terminology remnant fix

§4.4 said scanners flag "86–95% of the findings verification judged false positives" while the same paragraph used "judged benign" — replaced with "findings verification judged benign (reference-benign findings)" in the markdown draft, both LaTeX trees, and the regenerated main_bbl.tex. Aligned results/tool_accuracy.md heading/labels to reference-label terminology. Text-only change; package still 18 pages, 0 undefined citations, 0 overfull boxes. External review round 8 triaged the same day: its other terminology and opener quotes were stale (already fixed in rounds 6–7); its stats-strengthening suggestions (CIs for scanner metrics, sensitivity excluding AI-retained labels) remain available as revision-stage work; the second-rater recommendation is moot after the 2026-11-03 decision.

## 2026-11-03 — Self-audit packet built: blind re-labeling of the retained pre-labels

- CONTEXT: with the second-rater study dropped (round 7, above), the validation's open flank is the 340 matched rows that retain AI pre-labels accepted in the verification pass. Girish approved a single-author substitute on 2026-11-03: he re-labels a random subsample of the retained findings blind, and the label-change rate is reported as an annotation-stability audit. It is NOT inter-rater reliability (no second rater) and NOT independent validation (same author, second pass); the packet README and the scorer both say so in those words.
- POPULATION, reconstructed from the data files and verified by assertion in the builder: final labels = pre-labels with the 92 divergence rows replaced by their v3 recommendations; matched frame recomputed against findings_v3.jsonl = 451 rows (the 6 dropped rows are exactly the reconciliation doc's K8S-113/202/207/213/236/371), finals 279 TP / 162 FP / 7 TP-hardening / 3 EXCLUDED; author set within the frame = 87 divergence + 30 blind, 6 in both = 111; the remainder is exactly the published 340, every one with final label equal to its pre-label (227 TP / 113 FP). Deduped to 301 distinct finding keys (39 keys appear twice by the sample's design), following the kappa and second-rater subsamples, which also drew over distinct keys.
- DRAW: seed 20261103; 100 findings; allocation per rule proportional to the deduped population, floor 2, cap 14 (SEC_PRIVILEGED capped at 14 of its 72), largest-remainder to exactly 100; within a rule the allocation splits across source groups proportionally, mirroring build_labeling_sample.py's group stratification. Draw: 70 GitHub / 30 Helm findings, standing for 108 of the 340 rows. Three rules have no retained rows at all — IMG_NO_DIGEST, SEC_APE_NOT_DISABLED, SEC_ROOT_NOT_PREVENTED: every matched row of those rules was blind-labeled or individually adjudicated, so there is nothing to audit.
- PACKET in results/self_audit/packet/ (builder scripts/build_self_audit_packet.py): audit_sample.csv under blinded SA-### IDs with the original label schema (audit_label TP / FP / TP-hardening / unsure, FP reason codes, notes), packets.md / packets.jsonl evidence in the same extraction as the original labeling, protocol_for_audit.md (verbatim copy of the frozen v3 protocol's labeling edition), README.md with the blinding rules. The sealed key (audit ID -> sample ID + original final label) is local-only under the same .gitignore pattern as the second-rater key, to be committed with the replication package after scoring. sample_manifest.md (author-side, contains the draw's label distribution) is committed, as with the second-rater packet.
- SCORER: scripts/score_self_audit.py — overall label-change rate with a 95% Wilson interval, change rates per rule family (Section 3.2 families) and per rule, direction counts, and every changed row with both labels; audit-unsure rows are reported separately and excluded from the rate. Smoke-tested end-to-end on a temp copy with 5 planted flips and 2 unsure: all 5 detected (5/98 decided = 5.1% [2.2%, 11.4%] on the synthetic sheet). The real packet is untouched and unlabeled; the labeling pass is Girish's step.

## 2026-11-04 — Zenodo release v1.0.0; DOI minted

With the Zenodo–GitHub integration enabled on the repo, tagged release v1.0.0 ("EMSE submission version") on main at ce42bec. Zenodo archived the release zip and minted the DOIs: version DOI 10.5281/zenodo.23966670 (v1.0.0), concept DOI 10.5281/zenodo.23966669 (all versions). Data Availability in the manuscript draft and both LaTeX trees now reads "An archival copy is deposited on Zenodo (DOI: 10.5281/zenodo.23966670)"; CITATION.cff gained the doi field. Package rebuilt: still 18 pages, 0 undefined citations, 0 overfull boxes; abstract unchanged. Release: https://github.com/mallyagirish/k8s-misconfig-study/releases/tag/v1.0.0 — record: https://doi.org/10.5281/zenodo.23966670

## 2026-11-04 — Self-audit completed and scored

Girish labeled all 100 blinded audit rows (58 TP / 36 FP / 6 unsure; FP reason codes: infra-need 18, standard-practice 7, fixture 5, placeholder 5, parser-artifact 1). Scorer output in results/self_audit/audit_results.md: 94 decided rows, 16 label changes vs the retained AI pre-labels = 17.0% [95% Wilson CI 10.8, 25.9]; direction TP→FP 10, FP→TP 6. Changes concentrate in context-sensitive rules (SA_TOKEN_AUTOMOUNTED 3/4, SEC_RUN_AS_ROOT_EXPLICIT 2/4, SECRET_LITERAL_ENV 2/5, RBAC rules 4 across three rules); absence checks (seccomp, host namespaces, probes, secrets-committed) were stable. The filled sheet was edited in Numbers and uploaded via the GitHub web UI, which overwrote audit_sample.csv with the .numbers binary; converted back to CSV with LibreOffice, verified 100/100 labels present, stray .numbers removed.

## 2026-11-04 — Self-audit corrections adopted; all results recomputed

Girish's decision (2026-11-04): "Audit label wins on all 16 — recompute." The 16 audit labels were adopted wholesale (results/self_audit/adjudication.csv, final_notes record the rule) and applied to the reference labels by appending 16 rows with divergence_class = self_audit_correction to results/verification_divergence.csv, so the unmodified pipeline construction (final = recommended_v3 if in the divergence file, else prelabel) picks them up. All 16 changed findings have rows_covered = 1, so exactly 16 sample rows changed (list: results/self_audit/label_change_log.md): matched-frame totals move from 279 TP / 162 FP to 275 TP / 166 FP. Provenance: 324 of the 340 retained rows still carry the accepted pre-label, 16 carry audit-corrected labels; the 111 author-produced/adjudicated rows are unchanged.

VERIFICATION GATE (before any label change): the repo pipeline reproduced every published number exactly from the pre-change labels — pooled 0.633, weighted 0.699 [0.623, 0.840], adjusted 19,199 [17,120, 23,071] (cluster_bootstrap.py, 2,000 reps, seed 20261028), the full per-rule table in precision_provisional.md, and every per-tool rate computed from tool_accuracy.csv (conditional 0.98/0.93/0.90/0.76; effective 0.75/0.64/0.55/0.52 for Polaris/Checkov/kubeaudit/kube-linter; FP-flagging 0.86–0.95). Note: there is no standalone tool-accuracy script — tool_accuracy.csv (504 rows) is the pipeline artifact and the published rates were recomputed from it; after the label flips the same recomputation produced the new rates, and the CSV's final_label column was updated for the 24 rows of the 6 changed Helm findings (Helm ground-truth totals unchanged: 73 TP / 50 FP).

Old → new (audit-corrected):
- Pooled precision 0.633 [0.527, 0.714] → 0.624 [0.519, 0.705]
- Population-weighted precision 0.699 [0.623, 0.840] → 0.676 [0.601, 0.805]
- Adjusted true findings 19,199 [17,120, 23,071] → 18,556 [16,500, 22,118]
- Distinct-finding sensitivity 0.626 → 0.613; fallback sensitivity CIs now [0.601, 0.805] under all three rules
- Tools (conditional / effective / FP-flagging): kube-linter 0.90 [0.77, 0.96] / 0.51 / 0.92; kubeaudit unchanged 0.98 / 0.55 / 0.95; Polaris 0.93 [0.83, 0.97] / 0.72 / 0.88; Checkov 0.77 [0.66, 0.86] / 0.66 / 0.84
- Per-rule movers: SA_TOKEN_AUTOMOUNTED 0.857 → 0.643 (adjusted 2,294 → 1,720 — the main driver of the weighted drop; it moves from the face-value tier to "mostly" in Section 4.3/Table 2); SEC_RUN_AS_ROOT_EXPLICIT 1.000 → 0.882 (adjusted 40 → 35); IMG_UNTAGGED 0.818 → 0.909 (488 → 535); RBAC_CLUSTER_ADMIN_BINDING 0.800 → 0.900; RBAC_WILDCARD_VERBS 0.733 → 0.800; RBAC_WILDCARD_RESOURCES 0.647 → 0.706; RES_NO_REQUESTS 0.471 → 0.412 (adjusted 1,104 → 966); SECRET_LITERAL_ENV 0.400 → 0.267; SEC_CAPABILITY_ADDED 0.235 → 0.176; SEC_PRIVILEGED 0.608 → 0.595; HOST_NETWORK 0.250 → 0.312

Manuscript: abstract/§3.4 (κ note + new "Stability audit of the retained labels" passage)/§3.5/§4.3 (incl. Table 2 reorder — SA automount now reads "mostly")/§4.4/§6 updated in all three sources; §6 keeps single-author adjudication as the main limitation, with the audit described as a same-author stability check that mitigates it only partly. README validation section reconciled. Abstract unchanged in length (249 words by the package count). Package rebuilt: 18 pages, 0 undefined citations, 0 overfull boxes in all variants; submission main.pdf refreshed. The pre-correction figures remain recorded in the audit-correction note in results/precision_provisional.md.

## 2026-11-04 — Zenodo v1.0.1: archival copy updated to the corrected package

The v1.0.0 Zenodo archive predated the self-audit label correction, so the DOI cited in the paper pointed at a package with the old numbers. Tagged release v1.0.1 on main at 0c39c19 (the recompute commit); Zenodo archived it as version DOI 10.5281/zenodo.23966954 (concept DOI unchanged: 10.5281/zenodo.23966669, which resolves to the latest version). The cited DOI was swapped from 10.5281/zenodo.23966670 to 10.5281/zenodo.23966954 in the manuscript draft, both LaTeX trees, the regenerated main_bbl.tex, and CITATION.cff — one line each; the abstract and all other text are unchanged. Package rebuilt: still 18 pages, 0 undefined citations, 0 overfull boxes. The v1.0.0 entry above stands as the historical record of the first release. Release: https://github.com/mallyagirish/k8s-misconfig-study/releases/tag/v1.0.1 — record: https://doi.org/10.5281/zenodo.23966954

## 2026-11-04 — Self-audit weighting correction: design-weighted change-rate estimate

External review (round 10) flagged a real methodological error: the scorer's
headline audit figure was the unweighted 16/94 = 17.0% with a plain Wilson
interval, but the audit packet was not a simple random sample — allocation
was fixed per rule in proportion to the rule's share of the 301 distinct
retained findings (floor 2, cap 14; SEC_PRIVILEGED capped at 14 of its 72
findings), with each rule's allocation split across source groups
proportionally. Sampling fractions therefore differ by rule, and the Wilson
interval does not match the design.

Fix: scripts/score_self_audit.py now also computes the stratified
population-weighted change rate. Strata are rules — the level at which
allocation was set and the finest level at which every stratum but one has
decided rows (the within-rule group split is proportional, i.e.
self-weighting up to integer rounding, and 11 rule × source-group cells of
one finding received no draw, so the finer grid cannot carry the estimate;
reported as a sensitivity: 18.1% over 277 of 301 findings). Stratum
populations are reconstructed with the builder's derivation; the 16
self_audit_correction rows appended to verification_divergence.csv after the
draw are excluded, so the frame is the one the packet was drawn from
(asserted: 451 matched / 340 retained / 301 deduped). Interval: stratified
bootstrap, resampling decided findings within each rule, 2,000 replicates,
seed 20261104, percentile interval.

Results (results/self_audit/audit_results.md): population-weighted change
rate 16.4% [stratified bootstrap 95% CI 10.1, 23.1], covering 288 of the 301
distinct retained findings. DEPRECATED_API contributes no decided rows — all
5 of its draws were labeled unsure — so its 13 findings sit outside the
coverage. Unsure sensitivity: counting all 6 unsure findings as unchanged vs
changed bounds the weighted estimate at [15.6, 20.8] (unweighted bounds
[16.0, 22.0] over all 100 returned findings). The unweighted 17.0% [Wilson
10.8, 25.9] is retained as the description of the sample as drawn. The
§3.4 stability-audit passage in all three manuscript sources now reports the
weighted estimate as the population figure, keeps the 16-of-94 sample fact,
and notes the DEPRECATED_API coverage gap and the unsure bounds; abstract
and README state no audit rate and are unchanged (abstract still 249 words).
Package rebuilt: 18 pages, 0 undefined citations, 0 overfull boxes in all
variants. (Build note: the rule name needed a LaTeX-escaped underscore,
DEPRECATED\_API, in the .tex sources.)

## 2026-11-04 — Zenodo v1.0.2: archival copy updated to the weighting-corrected package

The v1.0.1 archive predated the self-audit weighting correction, so the cited
DOI again pointed at a package whose Section 3.4 reported the superseded
unweighted audit figure. Tagged release v1.0.2 on main at 79f3182 (the
weighting-fix commit); Zenodo archived it as version DOI
10.5281/zenodo.23967366 (concept DOI unchanged: 10.5281/zenodo.23966669,
which resolves to the latest version). The cited DOI was swapped from
10.5281/zenodo.23966954 to 10.5281/zenodo.23967366 in the manuscript draft,
both LaTeX trees, the regenerated main_bbl.tex, and CITATION.cff — one line
each; no other text changed. Package rebuilt: still 18 pages, 0 undefined
citations, 0 overfull boxes. The v1.0.0 and v1.0.1 entries above stand as the
historical record. Release:
https://github.com/mallyagirish/k8s-misconfig-study/releases/tag/v1.0.2 —
record: https://doi.org/10.5281/zenodo.23967366

## 2026-11-04 — Consistency bundle: CI bound conformed, §3.4 interpretation clarified, self-audit key published

Four small fixes from an external review of the weighting-fix commit
(79f3182), verified against the live repo before applying:

1. **CI bound conformed.** The scorer's deterministic output (seed 20261104)
   gives the audit's stratified bootstrap 95% CI as [10.1, 23.1], but the
   manuscript and the weighting-fix entry above said 23.2. Every 23.2
   referring to this interval — manuscript draft, both LaTeX trees (and the
   regenerated main_bbl.tex), and that entry — now reads 23.1, matching the
   scorer and results/self_audit/audit_results.md.
2. **§3.4 interpretation made explicit** (same clauses in all three
   manuscript sources): the 16.4% figure is the design-weighted change rate
   among the covered strata and its interval is conditional on those strata
   (288 of the 301 distinct retained findings); the interval is an
   approximate rule-stratified bootstrap interval, not an exact
   design-based one — resampling is within rules, so the finer
   rule × source-group allocation and the without-replacement draw are not
   reproduced.
3. **Self-audit key published.** results/self_audit/KEY_sealed.csv (columns:
   audit_id, sample_id, final_label, ai_prelabel, rule, arm, source_group,
   rows_covered — IDs and labels only) is now tracked; the .gitignore entry
   was removed and the sample manifest's key note updated to past tense.
   The second-rater key stays gitignored and unpublished. Rationale per the
   manifest's original plan: the key stays out of git only while the audit
   is blind; the audit is scored and adjudicated, so the scorer can now be
   rerun from a clean checkout.
4. **Draft date** in the manuscript header updated to 2026-11-04 (the
   2026-10-28 bibliography-verification parenthetical stands — that is when
   verification happened).

Package rebuilt after the edits: all three variants (submission main,
submission main_bbl, latex main) compile to 18 pages with 0 undefined
citations and 0 overfull boxes; the submission main.pdf was refreshed, and
the abstract is unchanged (249 words, as verified in the previous round).
Clean-checkout check: `git archive` of this commit into a fresh directory
and `python3 scripts/score_self_audit.py` there reproduces audit_results.md
exactly — 16.4% [10.1, 23.1], 16/94 sample description, 288/301 coverage.

## 2026-11-04 — Zenodo v1.0.3: archival copy updated to the consistency-bundle package

Tagged release v1.0.3 on main at 4ab4ba8 (the consistency-bundle commits);
Zenodo archived it as version DOI 10.5281/zenodo.23967708 (concept DOI
unchanged: 10.5281/zenodo.23966669, resolving to the latest version). The
cited DOI was swapped from 10.5281/zenodo.23967366 to
10.5281/zenodo.23967708 in the manuscript draft, both LaTeX trees, the
regenerated main_bbl.tex, and CITATION.cff — one line each; no other text
changed. Package rebuilt: 18 pages, 0 undefined citations, 0 overfull boxes
in all variants, and the new DOI verified in the rendered PDF. The v1.0.0,
v1.0.1, and v1.0.2 entries above stand as the historical record. Release:
https://github.com/mallyagirish/k8s-misconfig-study/releases/tag/v1.0.3 —
record: https://doi.org/10.5281/zenodo.23967708

## 2026-11-04 — Close-out round: audit-key column rename, abstract terminology, precision language

Final text corrections before freezing the submission package (all three
manuscript sources, same wording):

1. **Audit-key column renamed.** In results/self_audit/KEY_sealed.csv the
   pre-audit label column was named `final_label`, although it holds the
   label the finding carried before the audit — the audit/adjudication
   outcome is the final one. Renamed to `original_label` in the key header,
   in scripts/build_self_audit_packet.py (header writer), and in
   scripts/score_self_audit.py (reader; its pair comment already called it
   the original label). Unrelated `final_label` columns were deliberately
   left: results/self_audit/adjudication.csv (the genuinely final,
   post-adjudication label) and results/tool_accuracy.csv (the reference
   label). Earlier entries in this notebook that list the key's columns
   stand as the historical record of the name at the time.
2. **Abstract seccomp terminology.** "no sandboxing profile" → "no
   explicitly configured seccomp profile" — the engine measures explicit
   seccomp configuration, not sandboxing mechanisms generally.
3. **Perfect-precision language softened.** The abstract's "are essentially
   exact" → "showed no false positives in the validation sample"; §4.3's
   "are essentially never benign in context (all 1.000 on their samples)" →
   "showed no benign cases in their samples (all 1.000)". Both claims are
   now bounded by the validation sample that supports them.
4. **Abstract word budget.** Items 2–3 lengthened the text, so filler was
   trimmed to compensate (sentence 2 recast from "measure how … configure
   these knobs, using" to "measure configuration in … with"; "individually"
   and the redundant "labeled blind" dropped from the validation sentence;
   "later" dropped before "corrected by a blinded re-labeling audit";
   "unambiguous" dropped before "absence checks"; trailing "cases" dropped
   after "benign-by-design"; "our" dropped before "reference labels"). No
   number or claim changed. Abstract recount: 247 words (EMSE limit 250).

Package rebuilt after the edits: all three variants (submission main,
submission main_bbl, latex main) compile to 18 pages with 0 undefined
citations and 0 overfull boxes; the submission main.pdf was refreshed, and
the new abstract wording verified in the rendered PDF. Clean-checkout check: `git
archive` of this commit into a fresh directory and `python3
scripts/score_self_audit.py` there reproduces audit_results.md exactly —
16.4% [10.1, 23.1], 16/94 sample description, 288/301 coverage — the
rename changed no numbers.

## 2026-11-04 — Zenodo v1.0.4: frozen submission package

Tagged release v1.0.4 on main at 7ef7923 (the close-out commit); Zenodo
archived it as version DOI 10.5281/zenodo.23968066 (concept DOI unchanged:
10.5281/zenodo.23966669, resolving to the latest version). This is the
frozen submission package: audit-key column renamed for clarity, abstract
terminology and precision language corrected, no result changed. The
cited DOI was swapped from 10.5281/zenodo.23967708 to
10.5281/zenodo.23968066 in the manuscript draft, both LaTeX trees, the
regenerated main_bbl.tex, and CITATION.cff — one line each; no other text
changed. Package rebuilt: 18 pages, 0 undefined citations, 0 overfull
boxes in all variants, abstract 247 words, and the new DOI verified in
the rendered PDF. The v1.0.0–v1.0.3 entries above stand as the historical
record. Release:
https://github.com/mallyagirish/k8s-misconfig-study/releases/tag/v1.0.4 —
record: https://doi.org/10.5281/zenodo.23968066

## 2026-11-04 — Heading-numbering fix: sections promoted, numbers un-doubled

The author spotted the defect in his proofread of the v1.0.4 PDF: every
heading printed two numbers — "0.1 1. Introduction", "0.3.4 3.4
Validation: …". Cause: the LaTeX conversion had declared the eight
top-level headings as \subsection and the thirteen subsections as
\subsubsection, with the intended numbers typed into the titles by hand.
sn-jnl therefore auto-numbered them under a phantom section 0 and printed
its numbers next to the manual ones; even Data availability — meant to be
unnumbered — rendered as "0.9".

Fix, applied identically to both LaTeX trees (the Markdown draft keeps its
manual numbers): the 8 top-level headings promoted to \section and the 13
subsections to \subsection, manual "N. "/"N.M " prefixes stripped from all
21 titles, \label{}s preserved. "Data availability and replication
package" promoted to \section* so it renders unnumbered as intended; the
starred Statements and Declarations block (\section* + five \subsection*
declarations) already rendered unnumbered and is untouched. No deeper
heading levels (\paragraph etc.) exist in the document. main_bbl.tex
regenerated by the splice method; its diff against the previous version is
the heading lines only.

Verification: all three variants (submission main, submission main_bbl,
latex main) compile to 18 pages with 0 undefined citations and 0 overfull
boxes. Headings extracted from the rebuilt submission PDF read exactly
"1 Introduction", "2 Background and research questions", "3 Method",
"3.1 Corpus construction", …, "3.4 Validation: labeling protocol,
reliability, adjudication", "4 Results", "4.3 RQ2 — …", "7.4 Positioning",
"8 Conclusion", followed by the unnumbered back matter — the automatic
numbers match the old manual numbers one-for-one, so every in-text
"(Section 3.4)"-style reference still points at the section it names, and
no "0."-prefixed or doubled heading remains anywhere in the document.

## 2026-11-04 — Zenodo v1.0.5: heading-numbering correction

Tagged release v1.0.5 on main at 17423b8 (the heading-numbering fix
above); Zenodo archived it as version DOI 10.5281/zenodo.23968269
(concept DOI unchanged: 10.5281/zenodo.23966669, resolving to the latest
version). v1.0.5 supersedes the v1.0.4 frozen package: the only change is
the heading correction — sections promoted to their proper levels with
numbers generated by the class, the doubled "0.1 1." numbers eliminated,
and Data Availability unnumbered. No result, number, or other text
changed; the abstract is unchanged at 247 words. The cited DOI was
swapped from 10.5281/zenodo.23968066 to 10.5281/zenodo.23968269 in the
manuscript draft, both LaTeX trees, the regenerated main_bbl.tex, and
CITATION.cff — one line each. Package rebuilt and re-verified: 18 pages,
0 undefined citations, 0 overfull boxes in all variants, headings
re-extracted from the rendered PDF and matching the intended numbering
exactly, and the new DOI verified in the rendered PDF. The v1.0.0–v1.0.4
entries above stand as the historical record. Release:
https://github.com/mallyagirish/k8s-misconfig-study/releases/tag/v1.0.5 —
record: https://doi.org/10.5281/zenodo.23968269

## 2026-11-04 — Three figures added: prevalence, precision forest, scanner accuracy

- The manuscript had no figures; three were added, one per results
  section, all generated by `scripts/plot_figures.py` from the existing
  results data (files in `paper/figures/`, PDF for LaTeX, PNG for the
  Markdown draft):
  - Figure 1 (§4.1): grouped bars, workload-level prevalence of eight
    default-posture practices, Helm vs production-tagged GitHub
    (`results/stats_tagged_v3.json`).
  - Figure 2 (§4.3): forest plot of all 25 rules' precision with Wilson
    95% CIs and TP/FP counts (`results/precision_provisional.md`,
    post-audit labels).
  - Figure 3 (§4.4): scanner conditional/effective detection and
    benign-flagging with Wilson whiskers, recomputed from
    `results/tool_accuracy.csv`.
- The plotting script asserts every plotted value against the
  manuscript's printed numbers before drawing (Table 1's four pairs, all
  25 per-rule precisions + CIs with totals 275 TP / 166 FP, and §4.4's
  twelve scanner rates + CIs); all assertions pass, so the figures plot
  exactly the numbers the text reports.
- Inserted with captions and in-text references in all three manuscript
  sources; `main_bbl.tex` regenerated by the splice method. Package
  rebuilt in all variants: 21 pages (was 18), 0 undefined citations,
  0 undefined references, 0 overfull boxes; figure captions and
  numbering (1 = prevalence, 2 = precision, 3 = scanners) verified in
  the rendered PDF.

## 2026-11-04 — Zenodo v1.0.6: archival copy updated to the three-figures package

- GitHub release v1.0.6 cut on the figures commit; Zenodo archived it as
  version DOI 10.5281/zenodo.23968533 (concept DOI unchanged:
  10.5281/zenodo.23966669, resolving to the latest version). v1.0.6
  supersedes v1.0.5: the only change is the three figures and their
  captions/references — no result, number, or other text changed. The
  cited DOI was swapped from 10.5281/zenodo.23968269 to
  10.5281/zenodo.23968533 in the manuscript draft, both LaTeX trees, the
  regenerated main_bbl.tex, and CITATION.cff — one line each. Package
  rebuilt and re-verified: 21 pages, 0 undefined citations, 0 undefined
  references, 0 overfull boxes in all variants, all three figure
  captions present in the rendered PDF, and the new DOI verified in the
  rendered PDF. The v1.0.0–v1.0.5 entries above stand as the historical
  record. Release:
  https://github.com/mallyagirish/k8s-misconfig-study/releases/tag/v1.0.6 —
  record: https://doi.org/10.5281/zenodo.23968533

## 2026-11-04 — Figure-placement fix: forest plot out of the end matter

Girish spotted Figures 2 and 3 at the very end of the PDF (pages 20–21,
after the references) instead of inside §4.3/§4.4. Cause: all three
figures used [t], and the precision forest plot is 475pt tall — over the
class's top-fraction limit (~0.7 × \textheight), so it could never sit
at a page top and was deferred indefinitely; the scanner figure queued
behind it, since floats cannot overtake. Fix, applied identically to
both LaTeX trees with main_bbl.tex regenerated by the splice method:
all three figures now use [!t]; placeins is loaded and \FloatBarrier
closes §4.3 and §4.4 so the figures cannot escape their sections. The
first [!t] build put the forest plot in §4.3 but with a 3.3pt overfull
\vbox on its page, so scripts/plot_figures.py now draws it at figsize
height 6.0 instead of 6.6 (432pt tall; row spacing tightened, fonts
unchanged) and the figure was regenerated — the script's hard gates
re-asserted all 25 precisions/CIs and the 275/166 totals. Verified
placement in the rebuilt PDF: §4.1 starts p7, Fig. 1 p8; §4.3 starts
p9, Fig. 2 p11; §4.4 starts p12, Fig. 3 p13; §5 Discussion p14. All
variants: 21 pages, 0 undefined citations, 0 undefined references,
0 overfull boxes.

## 2026-11-04 — Zenodo v1.0.7: archival copy updated to the placement-fixed package

Tagged release v1.0.7 on main at the figure-placement fix commit;
Zenodo archived it as version DOI 10.5281/zenodo.23969482 (concept DOI
unchanged: 10.5281/zenodo.23966669, which resolves to the latest
version). v1.0.7 supersedes v1.0.6: the only change is the corrected
figure placement described in the entry above — no result, number, or
other text changed. The cited DOI was swapped from
10.5281/zenodo.23968533 to 10.5281/zenodo.23969482 in the manuscript
draft, both LaTeX trees, the regenerated main_bbl.tex, and
CITATION.cff — one line each. Package rebuilt and re-verified after
the swap: 21 pages, 0 undefined citations, 0 undefined references,
0 overfull boxes in all variants; placement unchanged (Fig. 1 p8,
Fig. 2 p11, Fig. 3 p13; Discussion p14); the new DOI verified in the
rendered PDF. The v1.0.0–v1.0.6 entries above stand as the historical
record. Release:
https://github.com/mallyagirish/k8s-misconfig-study/releases/tag/v1.0.7 —
record: https://doi.org/10.5281/zenodo.23969482
