# Misconfigured by Default: The Prevalence, Validity, and Tool Coverage of Kubernetes Misconfigurations in the Wild

**Author:** Girish Mallya
**Status:** First full draft, 2026-10-28. All quantitative claims are drawn from the
verified results files in `results/` (engine v3 statistics, the author-verified
validation sample as reconciled against engine v3, and the RQ3 tool coverage
matrix). The bibliography requires a verification pass before submission.
**Target venue:** *Empirical Software Engineering* (Springer), journal route.

---

## Abstract

Kubernetes manifests are the de facto interface between developers and production
infrastructure, and their defaults are permissive: a workload that specifies nothing
about identity, resources, or isolation runs with an automounted service-account
token, no resource limits, and no sandboxing profile. We measure how the ecosystem
actually configures these knobs. We collected 16,243 YAML documents (2,811 workloads)
from two arms — 151 rendered Helm charts and 60 public GitHub repositories — and
applied a 25-rule detection engine covering security context, resources, images,
reliability, RBAC, and secrets. Because prevalence figures are only as good as the
rules that produce them, we validated the engine against a 457-finding stratified
sample under a documented labeling protocol, with a blinded inter-rater subset
(Cohen's κ = 0.526 against the initial labels, with disagreements decomposed into
protocol-version effects and adjudicated judgment calls) and full author
verification. Overall precision is 0.633 [0.587, 0.676], and it varies sharply by
rule: explicit-danger rules (privilege escalation, seccomp, root prevention) are
essentially exact, while context-sensitive rules (committed secrets, host
namespaces, probes) are dominated by benign-by-design cases. Adjusting for
precision, we estimate ≈19,200 of 27,460 raw findings are genuine
misconfigurations. The defaults dominate: service-account tokens are automounted
in 88.6% of production GitHub workloads and CPU limits are missing in 75.3%,
while explicitly dangerous settings are rare (privileged containers, 1.4%).
Curated Helm charts are better hardened than raw repository manifests, but only
by 1.3–1.7×, not the 2–3× a top-charts sample suggests. Finally, we audit the
auditors: on identical input, the four most widely used manifest scanners
(kube-linter, kubeaudit, Polaris, Checkov) cover at most ~16 of the 25 practices,
agree closely only on explicit dangers, and diverge by up to 1.4× on the same
practice purely through counting semantics; scored against our verified labels,
the tools detect 52–75% of genuine misconfigurations overall and also flag
86–95% of the findings verification judged benign. No tool inspects the *contents* of
committed Secret objects, where the credential-bearing minority hides. We release
the corpus manifest, the rule engine, the labeling protocol, and the full
validation data as a replication package.

**Keywords:** Kubernetes; configuration errors; empirical study; misconfiguration;
static analysis tools; measurement validity

---

## 1. Introduction

Almost every production system now runs on Kubernetes, and almost every Kubernetes
workload is described by a YAML manifest that its author wrote once and rarely
revisits. The platform's configuration surface is large, and its defaults were
chosen for convenience rather than safety. A container that says nothing about
security runs as whatever user its image specifies, with a service-account token
mounted into its filesystem, no CPU or memory limits, no seccomp profile, and
privilege escalation allowed. Each of these is a documented hardening gap; in
aggregate, they define the actual security posture of the cloud-native ecosystem.

Two questions follow. First, *descriptive*: how are real manifests actually
configured — which hardening practices are routine, which are rare, and how much
of the apparent risk is an artifact of counting test fixtures and examples as if
they were production code? Second, *instrumental*: the ecosystem's answer to this
problem is a family of static auditing tools, but those tools are themselves
rarely audited. If four widely used scanners are run on identical input, do they
cover the same practices, and do their counts agree?

Both questions are measurement questions, and both are easy to answer badly.
Manifest corpora scraped from public sources mix production code with tutorials,
test fixtures, and rendered templates; naive counting silently grades homework as
if it were infrastructure. Scanner comparisons, meanwhile, tend to report raw
finding counts without establishing whether any tool's findings are *correct* —
and our own validation shows that for several common rules, the majority of
flagged findings are benign in context.

This paper makes four contributions:

1. **A two-arm prevalence measurement** of 25 misconfiguration practices across
   16,243 documents (2,811 workloads), with source tagging that separates
   production manifests from examples and fixtures, cluster-level prevalence that
   corrects for duplicated content, and a Helm-vs-GitHub comparison that corrects
   a best-chart bias in the obvious sampling strategy (Section 4.1, 4.2).
2. **A validated rule engine.** Every prevalence number is paired with a per-rule
   precision estimate from a 457-finding stratified sample, judged under a
   written labeling protocol whose evolution (three versions), blinded
   inter-rater check, and adjudication amendments are documented and released.
   Precision, not raw counts, is the paper's unit of evidence (Section 4.3).
3. **A revised taxonomy** of Kubernetes misconfiguration that distinguishes
   misconfigurations proper from hardening gaps and manifest rot, and classifies
   false positives into reusable context classes (infrastructure agents,
   credential-free placeholders, standard operator patterns) (Section 4.3).
4. **An audit of four production scanners on identical input**, showing that
   coverage tops out at ~16 of 25 practices, that agreement is high only where
   misconfiguration is explicit, and that headline count divergences (up to
   ~1.4× on the same practice) are explained by counting semantics — pod- vs
   container-level units and merged checks; and that, scored against
   verified ground truth, the tools' real deficits are coverage and
   context-sensitivity, not detection on the practices they do check
   (Section 4.4).

The headline result is that the ecosystem's risk is concentrated in *defaults*,
not in explicit misbehavior. Privileged containers appear in 1.4% of production
workloads; automounted service-account tokens appear in 88.6%. Security effort —
human and tooling alike — is calibrated to the rare, explicit cases and largely
blind to the common, default ones.

## 2. Background and research questions

A Kubernetes workload manifest declares, among other things, a pod's security
context (user, capabilities, seccomp and AppArmor profiles, privilege escalation),
its containers' resource requests and limits, image references (tag and digest
pinning), health probes, service-account binding, and — in adjacent objects —
RBAC roles and Secrets. Nearly every field is optional, and the platform supplies
a permissive default when a field is absent. Misconfiguration, for this study, is
a manifest state that a documented hardening practice (the CIS Kubernetes
Benchmark, the NSA/CISA hardening guide, and the scanners' own rule catalogues)
identifies as a gap. Section 3.2 defines the 25 rules operationally; Section 3.4
describes how we establish that the rules measure what they name.

We ask four research questions:

- **RQ1 (Prevalence).** How common is each class of misconfiguration in
  real-world manifests, once production code is separated from examples and
  fixtures and duplicated content is accounted for?
- **RQ2 (Validity and taxonomy).** With what precision does a rule-based engine
  detect each practice — i.e., which of the 25 measurements can be taken at face
  value and which require contextual judgment — and what taxonomy organizes the
  true and false positives?
- **RQ3 (Tool coverage).** On identical input, how much of the observed taxonomy
  do the four widely used scanners cover, and do their counts agree? Where they
  diverge, is the divergence detection or bookkeeping?
- **RQ4 (Curation effect).** Do rendered Helm charts — the ecosystem's curated,
  templated distribution channel — differ from manifests committed directly to
  Git repositories, and by how much once sampling bias is handled?

## 3. Method

### 3.1 Corpus construction

The corpus has two arms, collected in October 2026 from public sources only.

**Helm arm.** We rendered the 151 most popular charts on Artifact Hub with
default values (`helm template`), yielding 2,616 documents and 402 workloads.
Default values are what an operator gets when they install a chart without
tuning it — the correct object of study for a question about defaults — but a
top-charts sample over-represents well-maintained projects; Section 4.2 quantifies
and corrects for this *best-chart bias* rather than ignoring it.

**GitHub arm.** We mined 60 public repositories (seed projects plus
search-discovered manifest collections), yielding 13,627 documents and 2,409
workloads. Snapshots are pinned by commit SHA (`results/github_commit_shas.json`).
Every file was source-tagged as *production*, *example*, or *fixture* by path and
repository role, so prevalence can be reported for production manifests alone;
an addendum to the labeling protocol (Section 3.4) resolves tag/content conflicts
in favor of content (e.g., a `testdata/` tree inside a production-tagged
repository counts as fixture).

The corpus itself is not redistributed (third-party manifests carry mixed
licenses); the collection scripts and per-source logs are the corpus manifest,
and running the collectors rebuilds it.

### 3.2 The rule engine

We implemented a 25-rule engine over parsed YAML (Deployments, StatefulSets,
DaemonSets, Jobs, CronJobs, Pods, and the RBAC/Secret objects adjacent to them).
Rules span six families: **images** (untagged, `:latest`, no digest pinning),
**resources** (missing CPU/memory limits, missing requests), **reliability**
(missing liveness/readiness probes), **security context** (privileged, root not
prevented, explicit root, privilege escalation not disabled, dangerous or any
added capabilities, missing seccomp), **host access** (host network/PID/IPC,
automounted SA token), **RBAC and secrets** (wildcard verbs/resources,
cluster-admin binding, committed Secret objects, literal secrets in environment
variables), and **API currency** (deprecated APIs — reported as manifest rot, not
misconfiguration; see Section 4.3). Engine v3 incorporates three correctness
fixes over v2 that matter for the results: the SA-token rule joins the
ServiceAccount object's own automount flag; init containers are excluded from
probe rules (a third of v2's Helm probe findings were on init containers); and
`seccompProfile.type=Unconfined` counts as no profile. Engine v3 reports 27,460
findings over the full corpus. The full rule definitions ship with the
replication package.

### 3.3 Tool audit setup (RQ3)

We ran kube-linter, kubeaudit, Polaris, and Checkov — the four most widely
adopted open-source manifest auditors — on the *identical* Helm-arm input (402
workloads, rendered with default values), each with its default configuration.
Default configuration is the treatment of interest: it is what a new adopter
runs, and, as Section 4.4 shows, several relevant checks are not in it. We mapped
each tool's checks to our 25 rules by hand from the tools' output on this input,
recording partial coverage (a check that covers a rule with narrower semantics)
as one half in coverage totals. Counts were reconciled rule by rule; where a
tool merges two of our rules into one check (e.g., untagged and `:latest`), we
report the merged figure rather than forcing an attribution. Separately, we
score each tool against ground truth: the 126 Helm-arm rows of the validation
sample (Section 3.4) carry author-verified labels, so for every sampled finding
we can ask whether the tool reported the corresponding practice on that object —
yielding detection rates on verified true positives and flagging rates on
verified false positives, per tool (full method and per-row data in
`results/tool_accuracy.md`).

### 3.4 Validation: labeling protocol, reliability, adjudication

Prevalence without precision is numerology, so we validated the engine on a
457-finding stratified sample: all findings of the two rarest high-severity
rules, stratified draws from the rest, and ~10% hidden duplicate rows. A sample
row is one finding with an *evidence packet* (the flagged object, its security
context, and its source context).

Labels (TP / FP / unsure) were assigned under a written protocol. The protocol's
history is part of the method and is reported, not hidden: an initial
*definitional* standard (v2: a finding is TP iff the manifest exhibits the
property the rule names, in context) was harmonized with an earlier
*exploitability* draft (v1) into a governing protocol (v3) that keeps the
definitional core and adds explicit contextual amendments — production scoping
for resource/probe rules, a two-tier treatment of digest pinning, an
escalation-path test for root/privilege-escalation rules, and a credential-material
test for committed secrets. AI pre-labels produced under v2 were treated as a
*first rater*, never as ground truth.

**Inter-rater reliability.** The author labeled a blinded 30-row subset
(spanning all 25 rules) before seeing any pre-labels. Agreement was 24/30 (80%),
Cohen's κ = 0.526 against the v2-standard pre-labels. We report this number as
measured, with its decomposition, because the decomposition is the finding:
four of six disagreements were resource/probe rows where the governing v3
production-scoping amendment sides with the author against the v2 definitional
labels — a standards difference, not rater noise — and the remaining two were
genuine judgment calls (a CNI agent's dangerous capabilities; an operator's
wildcard RBAC confined to its own API groups), which were adjudicated into two
further *rule-level* amendments (an infrastructure-class test requiring a
drop-ALL baseline plus function-required capabilities, and an own-API-group
scoping test for wildcard RBAC), adopted before the verification pass and now
part of the protocol (`results/labeling_protocol_v3_addendum.md`). Intra-rater
consistency, measured by the hidden duplicates, was 44/44 groups.

**Verification.** The author then verified the full sample (blank = accept,
per protocol), reviewing the 92 *divergence rows* — those whose labels can differ
between the v1 and v2 standards — first and accepting the v3 recommendations on
all 92 without override on 2026-10-27. Final labels are therefore author-verified
throughout. Rows whose flagged property cannot be observed in the source
(7, e.g. images injected by kustomize overlays) are excluded from precision
denominators with the count and reason disclosed.

### 3.5 Analysis

For each rule we report precision = TP / (TP + FP) over decided rows with Wilson
95% confidence intervals, *adjusted prevalence* = precision × population findings,
and workload-level prevalence (share of workloads with ≥1 finding) per corpus arm
and source tag. Because the validation sample was drawn under engine v2 and the
population is engine v3, we reconciled every sampled row against v3 findings on
(arm, source, kind, name, container, rule): 451 of 457 rows still exist in v3;
the headline figures are computed on that matched frame, and a distinct-finding
sensitivity check (one vote per unique key, collapsing the intentional
duplicates) is reported alongside. Cluster-level prevalence (share of
repositories/charts with ≥1 finding) addresses the non-independence of findings
within a source: 52.9% of v3 GitHub findings repeat an already-seen
(kind, name, container, rule) key, so document-level rates alone would overstate
how widespread each practice is — and, as Section 4.1 shows, the practices are
widespread anyway.

---

## 4. Results

### 4.1 RQ1 — Prevalence: the defaults are the finding

Table 1 reports workload-level prevalence for the headline practices, per arm,
with the GitHub arm restricted to production-tagged manifests. Three facts stand
out.

**Default-insecure settings are near-universal.** In production GitHub manifests,
service-account tokens are automounted in **88.6%** of workloads and CPU limits
are missing in **75.3%**; in rendered Helm charts the figures are 85.1% and 85.6%,
with **97.5%** of Helm workloads running at least one image that is not
digest-pinned (65.3% for production GitHub). Restricting to production code
barely moves the numbers (corpus-wide GitHub SA automount is 96.2%): the risky
defaults live in shipped manifests, not in test files.

**Explicit dangers are rare.** Privileged containers appear in **1.4%** of
production GitHub workloads (5.5% in Helm charts, where node-level agents are
common), and cluster-level prevalence tells the same story from the other side:
SA automount appears in **94%** of repositories and **90%** of charts, missing
seccomp in 94%/72%, unpinned digests in 91%/97% — but privileged containers in
only 22% of repositories and 8% of charts. The ecosystem has largely learned not
to do the obviously dangerous thing, and has largely not learned to turn off the
defaults.

**Table 1.** Workload-level prevalence, engine v3 (share of workloads with ≥1 finding).

| Practice | Helm charts | GitHub (production) | GitHub (all) |
|---|---:|---:|---:|
| Image not digest-pinned | 97.5% | 65.3% | — |
| SA token automounted | 85.1% | 88.6% | 96.2% |
| No CPU limit | 85.6% | 75.3% | 79.0% |
| Privileged container | 5.5% | 1.4% | — |

*Full per-rule tables for all 25 rules, both arms and all source tags, are in the
replication package (`results/stats_tagged_v3.json`).*

### 4.2 RQ4 — Curation helps, less than it looks

Rendered Helm charts are better hardened than raw GitHub manifests, but the gap
is **1.3–1.7×**, not the 2–3× suggested by comparing the most popular charts
against unfiltered repository mining. The mechanism is sampling: a top-151-charts
frame over-weights flagship projects with dedicated maintainers. Even taking the
favorable frame at face value, the curated channel's advantage is concentrated in
the explicit-danger rules; on default-insecure practices (automount, limits,
digest pinning) charts are statistically indistinguishable from — and on CPU
limits and digest pinning worse than — production GitHub code. Curation polishes
the visible edge of the configuration surface; it does not change the defaults
underneath.

### 4.3 RQ2 — Precision and taxonomy: which numbers can be believed

Overall precision on the reconciled, author-verified sample is **0.633
[0.587, 0.676]** (279 TP / 162 FP over decided rows), adjusting the 27,460 raw
findings to an estimated **≈19,200 genuine misconfigurations**. A
distinct-finding sensitivity analysis gives 0.626 — the intentional duplicate
rows do not move the result. But the aggregate conceals the paper's most useful
variation: precision is a property of the *rule*, and it splits the taxonomy
into rules that can be read at face value and rules that cannot.

**Face-value rules (precision ≈ 1.0).** Missing seccomp profile, privilege
escalation not disabled, root not prevented, and `:latest` images are
essentially never benign in context (all 1.000 on their samples); SA-token
automount (0.857) and dangerous capabilities (0.824, under the addendum's
infrastructure test) are close behind. For these, scanner output *is*
prevalence, up to sampling error.

**Context-dominated rules (precision ≤ 0.4).** Committed Secret objects are the
extreme: **0.125**. Under the credential-material test, most committed Secrets
are empty, operator-populated, or documented placeholders; the genuine exposure
is a credential-bearing minority that no content-blind rule can separate from
the noise. Host network (0.250) and host PID (0.214) findings are mostly node
infrastructure — CNI/CSI agents and node exporters whose function requires the
access. Missing liveness probes (0.214) and the resource rules (0.375–0.47) are
dominated by production scoping: examples, fixtures, and one-shot Jobs that a
context-free count grades as production gaps. Added capabilities (0.235) are
mostly least-privilege patterns (default-set additions, or `NET_BIND_SERVICE`
over a drop-ALL baseline).

**Table 2.** Per-rule precision (author-verified, reconciled to engine v3; Wilson 95% CIs).
Selected rules; full table in `results/precision_provisional.md`.

| Rule | Precision | 95% CI | Reading |
|---|---:|---|---|
| SEC_NO_SECCOMP | 1.000 | [0.82, 1.00] | face value |
| SEC_APE_NOT_DISABLED | 1.000 | [0.80, 1.00] | face value |
| SEC_ROOT_NOT_PREVENTED | 1.000 | [0.78, 1.00] | face value |
| IMG_LATEST | 1.000 | [0.80, 1.00] | face value |
| SA_TOKEN_AUTOMOUNTED | 0.857 | [0.60, 0.96] | face value |
| SEC_DANGEROUS_CAPABILITY | 0.824 | [0.59, 0.94] | face value |
| RBAC_WILDCARD_VERBS | 0.733 | [0.48, 0.89] | mostly |
| RBAC_WILDCARD_RESOURCES | 0.647 | [0.41, 0.83] | mostly |
| SEC_PRIVILEGED | 0.608 | [0.50, 0.71] | mixed |
| REL_NO_READINESS_PROBE | 0.538 | [0.29, 0.77] | context-heavy |
| RES_NO_REQUESTS | 0.471 | [0.26, 0.69] | context-heavy |
| RES_NO_CPU_LIMIT | 0.429 | [0.21, 0.67] | context-heavy |
| SECRET_LITERAL_ENV | 0.400 | [0.20, 0.64] | context-heavy |
| RES_NO_MEM_LIMIT | 0.375 | [0.18, 0.61] | context-heavy |
| HOST_NETWORK | 0.250 | [0.10, 0.49] | context-dominated |
| SEC_CAPABILITY_ADDED | 0.235 | [0.10, 0.47] | context-dominated |
| HOST_PID / REL_NO_LIVENESS_PROBE | 0.214 | [0.08, 0.48] | context-dominated |
| SECRET_COMMITTED | 0.125 | [0.03, 0.36] | context-dominated |

**Taxonomy v2.** The validation exercise reorganizes the 25 rules into a
three-tier taxonomy, and the false positives into five reusable context classes:

- **Tier 1 — Misconfigurations.** States that are wrong in essentially all
  contexts (the face-value rules above, plus wildcard RBAC and cluster-admin
  binding at 0.65–0.80 with the own-group exception below).
- **Tier 2 — Hardening gaps.** States that are genuine but lesser gaps, reported
  separately and never folded into misconfiguration precision: digest-unpinned
  images *with* an explicit version tag (7 of 14 sampled no-digest rows), and the
  context-heavy resource/probe rules when they occur in production code.
- **Tier 3 — Manifest rot.** Deprecated API versions: real, mechanically certain,
  and not a security misconfiguration; reported as their own line.

False positives concentrate in five context classes, each of which became an
explicit protocol test: **infra-need** (node agents whose function requires the
access, gated on a drop-ALL baseline for capabilities), **placeholder** (Secrets
and env values without credential material), **fixture** (test/example content,
decided by content over source tag), **standard operator pattern** (wildcard
RBAC confined to the operator's own API groups; least-privilege capability
additions), and **not-exploitable** (root/APE findings with no escalation path:
non-root enforced and no added capabilities). A scanner — or a study — that
implements these five distinctions recovers most of the precision the naive
rules lose.

### 4.4 RQ3 — Auditing the auditors

On identical Helm-arm input with default configurations, approximate coverage of
the 25 practices is: Checkov ~16, Polaris ~13, kube-linter ~11, kubeaudit ~11
(partial coverage counted as one half). Three results matter more than the
ranking.

**Nobody covers the long tail, and one gap is total.** Digest pinning — the
single most prevalent practice in the corpus — is checked by exactly one tool
(Checkov CKV_K8S_43). Wildcard RBAC has no *default-enabled* check that catches
it broadly: Checkov's CKV_K8S_49 flags 29 of the 155 wildcard findings on this
input, and kube-linter ships wildcard checks that are off by default. And
**no tool inspects committed Secret contents**: all four flag (or ignore) Secret
objects without distinguishing credential material from placeholders, which
Section 4.3 shows is a 7:1 noise-to-signal distinction. The most sensitive
objects in the corpus are the ones the tooling understands least.

**Agreement exists only where danger is explicit.** On privileged containers,
the four tools report 26–27 findings against our 27 — near-perfect consensus.
On missing CPU limits, the same input yields **343 / 411 / 416 / 497** findings
across the tools against 502 container-level cases in our engine. The spread is
bookkeeping, not detection: kubeaudit counts at pod level and merges "no limits
at all" (421) with "limits without CPU" (76); kube-linter merges limits with
requests (416); Checkov counts a narrower property (343). A consumer comparing
tools — or tracking one tool over time — sees a ~1.4× swing that has nothing to
do with the underlying manifests.

**Accuracy against verified ground truth.** Coverage and counts say what a
tool *can* check and how much it *reports*; the verified sample lets us ask
whether it is *right*. Where a tool has a check for a sampled practice, it
detects verified true positives reliably — kubeaudit 0.98, Polaris 0.93,
kube-linter 0.90 — with Checkov the outlier at 0.76 (its run-as-non-root check
systematically misses containers that run as root *explicitly*: 8 of its 15
misses). Counting practices with no check as missed, effective detection of
genuine misconfigurations is 0.52–0.75, and the ranking inverts the raw-count
intuition: Polaris leads (0.75) on the strength of coverage, not per-check
detection. The symmetric result is the more damning one: the same checks flag
**86–95% of the findings verification judged false positives**. The taxonomy's
context classes — infrastructure agents, standard operator patterns,
least-privilege capability sets — fool the production tools at about the same
rate they fooled our unvalidated rules. The tools' deficit on real manifests
is not detection; it is coverage and context.

| Tool | TP detection (check exists) | TP detection (effective) | FP-flagging (check exists) |
|---|---:|---:|---:|
| kube-linter | 0.90 [0.78, 0.96] | 0.52 | 0.92 |
| kubeaudit | 0.98 [0.87, 1.00] | 0.55 | 0.95 |
| Polaris | 0.93 [0.84, 0.97] | 0.75 | 0.87 |
| Checkov | 0.76 [0.64, 0.85] | 0.64 | 0.86 |

*Ground truth: 73 verified-TP and 50 verified-FP Helm-arm sample rows; rates
over rows where a mapped check exists, except the effective column, which
counts no-check practices as missed. Method, joins, and caveats:
`results/tool_accuracy.md`.*

**Defaults decide what gets found.** kube-linter's probe checks validate probe
*port correctness*, not probe existence; its SA-token and wildcard checks are
absent or opt-in; kubeaudit's SA check covers only the default service account.
The pattern is consistent: each tool's default configuration is tuned to the
explicit-danger tier of the taxonomy, and the default-insecure tier — where
Sections 4.1 and 4.3 show most genuine misconfiguration lives — is covered
partially, optionally, or not at all.

---

## 5. Discussion

**The risk is the default, and the default is a design outcome.** The practices
with the highest prevalence — automounted tokens, absent limits, unpinned
images, absent seccomp — are precisely those where doing nothing produces the
finding. Manifest authors are not choosing insecurity; they are accepting a
platform posture. Interventions aimed at author behavior (linters in editors,
review checklists) fight the last war: the durable fix is at the platform and
distribution layer — admission-time defaults (Pod Security Standards,
policy engines with the checks *enabled*), chart templates that ship hardened
security contexts, and image pipelines that pin digests at build time. Our
curation result (Section 4.2) is the cautionary evidence: even the ecosystem's
most maintained artifacts only partially overcome the defaults.

**Scanner output needs a validity label.** Two scanners can disagree by 1.4× on
the same manifests without either being "wrong" — they are counting different
units and different properties under the same English name. We suggest the field
adopt three reporting norms: state the counting unit (pod vs container), state
whether merged checks are decomposed, and state per-check precision on a public
validation corpus, as this study does for its own engine. A count without those
three qualifiers is not comparable across tools or across time.

**The five context classes are a checklist for tool authors.** Most of the
precision our naive rules lost is recoverable with distinctions that are
mechanical once named: join the ServiceAccount object before grading automount;
require credential material before calling a Secret committed; treat a
drop-ALL baseline plus function-required capabilities on a node agent as
infrastructure, not exposure; scope wildcard RBAC by API-group ownership; and
never grade fixtures as production. Several of these are one-join or one-test
changes. The tools' roadmaps, not their detection cores, are the bottleneck.

**For practitioners**, the actionable reading of Tables 1 and 2 is short:
the face-value rules are a reliable triage list (fix seccomp, privilege
escalation, root prevention, and `:latest` first — the findings are real), SA
tokens and resource limits are the largest genuine exposure by volume, and
committed-Secret alerts should be routed to content inspection rather than
counted.

## 6. Threats to validity

**Construct validity** rests on the labeling protocol. We mitigate by
*disclosing* rather than concealing its evolution: three protocol versions, a
blinded inter-rater subset (κ = 0.526 against the v2-standard labels, with the
disagreement decomposition showing 4 of 6 tracing to the v2→v3 standards change
itself), adjudicated rule-level amendments, and full author verification.
Readers who prefer the purely definitional standard can recompute precision
under it from the released sample (the v2 pre-labels are preserved); the
prevalence *rankings* are unchanged under either standard, though several
per-rule precisions move, as Section 4.3 reports. The κ figure is below the
conventional 0.7 benchmark and we do not claim otherwise; it measures agreement
with labels produced under a superseded standard, and the verification pass —
not the κ subset — is the ground truth of record.

**Internal validity.** Engine v3's three semantic fixes (SA-object join, init
containers in probe rules, Unconfined seccomp) each moved findings materially;
residual engine bugs would bias prevalence and are mitigated by the validation
sample itself — a systematically wrong rule shows up as low precision, and none
of the face-value rules do. For RQ3, check-to-rule mapping was manual; we
mitigated by reconciling counts rule by rule and reporting merged checks as
merged rather than forcing attribution.

**External validity.** The GitHub arm over-represents public, open-source
practice and under-represents private enterprise manifests, which plausibly
differ in both directions (more policy enforcement, more legacy). The Helm arm's
best-chart bias is measured in Section 4.2 and cuts toward *understating*
ecosystem-wide prevalence. All data is from October 2026; defaults and tooling
evolve, and the replication package is designed for re-collection.

**Reliability.** Intra-rater consistency was 44/44 on hidden duplicates. The
sample-to-population reconciliation (451/457 rows matched to engine v3) and the
distinct-finding sensitivity analysis (0.626 vs 0.633) bound the effect of the
v2→v3 frame change. Corpus snapshots are pinned by commit SHA; the corpus is
rebuildable from the released collectors and logs.

## 7. Related work

### 7.1 Empirical studies of Kubernetes misconfiguration

The closest predecessor is Rahman et al.'s empirical study of security
misconfigurations in open-source Kubernetes manifests [Rahman2023]. Mining
2,039 manifests from 92 repositories, they characterize 11 categories of
security misconfiguration, build a detection tool (SLI-KUBE) to quantify their
frequency (1,051 misconfigurations), and validate by reporting ten
misconfigurations to practitioners, who agreed to fix 60%. We build on their
characterization in four ways: an order-of-magnitude larger corpus with a
second, curated arm (rendered Helm charts) that supports a curation comparison;
a broader practice set (25 rules across security, resources, reliability,
images, RBAC, and secrets, rather than security alone); separation of
production manifests from examples and fixtures, which their manifest-level
counting does not attempt; and a validation design that estimates *per-rule
precision* over a stratified sample with a documented protocol and a blinded
reliability check, rather than fix-agreement on a small set of reports. Their
headline conclusion — insecure configurations are widespread — is corroborated
by our data at larger scale; our contribution is establishing *which* of the
counts can be believed, and by how much.

Minna et al. mine Helm charts from Artifact Hub and compare seven analyzer
tools by their default policies, then evaluate whether LLMs can mitigate the
reported misconfigurations [Minna2025] — in this journal. Their tool comparison
aggregates common and unique findings per tool and includes a manual
false-positive check on a subset. Our study asks the prior question their
pipeline assumes away: whether the tools' reports on natural input are
*correct*, rule by rule, against verified ground truth — and finds that for
context-sensitive rules they frequently are not (Section 4.3), a result that
also bears on their mitigation loop, since an LLM asked to fix a false positive
can only damage a working configuration. The studies are complementary: they
evaluate repair; we evaluate the measurement the repair depends on. We also add
the raw-manifest arm and the production/fixture separation their chart-only
corpus does not require.

Beyond Kubernetes, configuration errors have been studied empirically in
general-purpose systems and in infrastructure-as-code ecosystems (Dockerfiles,
Puppet, Terraform, CI configuration), generally finding insecure defaults and
smell-like patterns to be widespread. Those results motivate ours; the
Kubernetes setting differs in that the configuration surface is a single,
structured API with platform-supplied defaults for nearly every field, which
is what makes a uniform 25-rule measurement across two distribution channels
possible.

### 7.2 Scanner evaluation and benchmarks

Eom et al. present the first systematic benchmark of Kubernetes
misconfiguration scanners [Eom2026]: ten tools, whose documented coverage they
found too ambiguous to take at face value, so they reverse-engineered precise
detection targets from implementations and dynamic testing, then measured
recall on a constructed benchmark of 4,109 misconfiguration files (281 unique
misconfigurations), finding best recall of 43.8% (static) and 62.3% (dynamic).
Their ground truth is *constructed* — each benchmark file is a known
misconfiguration — which is the right design for measuring recall, and the
wrong one for measuring what happens on real manifests, where the open
question is not "does the tool fire on a seeded defect" but "is this firing,
on this real object, a genuine misconfiguration." That is the quantity we
measure: per-rule precision of findings on natural corpora, against
author-verified labels, plus prevalence — neither of which a seeded benchmark
can report. The two results also converge from opposite directions: their
finding that scanners adopt different criteria for the same documented
misconfiguration is the implementation-level explanation of our
measurement-level finding that identical input yields ~1.4× count spreads
through counting semantics (Section 4.4). Where they audit ten scanners
against a specification, we audit four against the wild.

Industry comparisons of hardening guidelines and scanner scoring (e.g., the
Dynatrace Research comparison of eight guidelines and ten scanners) likewise
report substantial coverage and scoring disparities; they share our conclusion
that scanner outputs are not mutually comparable, reached there by guideline
mapping rather than by validated findings.

### 7.3 Benchmarks and hardening guidance

The CIS Kubernetes Benchmark and the NSA/CISA Kubernetes Hardening Guide
define the practice standard our rules operationalize, and the Pod Security
Standards define the platform's own posture tiers. Taxonomy v2 (Section 4.3)
can be read as an empirical annotation of those documents: which of their
recommendations correspond to states that are wrong in essentially every
context (Tier 1), which to hardening opportunities (Tier 2), and which to
hygiene (Tier 3) — and, through the five false-positive context classes, where
the guidance needs contextual exceptions that the documents themselves do not
state (node-infrastructure agents being the largest).

### 7.4 Positioning

| Dimension | Rahman et al. 2023 | Minna et al. 2025 | Eom et al. 2026 | This study |
|---|---|---|---|---|
| Corpus | 2,039 manifests, 92 repos | Artifact Hub charts (all) | 4,109 constructed files | 16,243 docs, 2 arms (60 repos + 151 charts) |
| Practices | 11 security categories | tools' default policies | 281 misconfigurations (union of 10 tools) | 25 rules, 6 families |
| Ground truth | practitioner fix-agreement (10 reports) | manual FP check on a subset | constructed by design | 457-finding stratified sample, blinded subset, protocol + adjudication, author-verified |
| Tool treatment | builds one tool | 7 tools, common/unique counts + LLM repair | 10 tools, recall on benchmark | 4 tools on identical natural input: coverage, count semantics, accuracy vs verified labels |
| Production vs fixture | not separated | n/a (charts) | n/a (constructed) | separated; content-over-tag rule |
| Prevalence | manifest-level counts | chart-level counts | none (benchmark) | workload-level, cluster-level, precision-adjusted |

In one sentence: prior work establishes that Kubernetes misconfiguration
exists (Rahman et al.), that tools report it inconsistently and LLMs repair it
imperfectly (Minna et al.), and that scanners miss much of what they claim to
cover on seeded cases (Eom et al.). This study establishes how much of it
there is in production-shaped code, how much of what any rule reports is real,
and why the tools' numbers cannot be compared naively — the measurement
foundation the other three directions implicitly rely on.

## 8. Conclusion

Across 16,243 real-world documents, Kubernetes misconfiguration is not a story
of reckless operators but of permissive defaults accepted at scale: tokens
automounted in ~9 of 10 production workloads, limits and digest pinning absent
as the norm, and the explicitly dangerous settings comparatively rare. The
measurement itself needs care — a third of naive findings are benign in
context, and the scanners the ecosystem relies on cover at most two-thirds of
observed practices, agree mainly where danger is explicit, and diverge by
bookkeeping where it is not. Both conclusions point the same way: harden the
defaults, and label the measurements.

## Data availability and replication package

All artifacts are public: corpus collectors and per-source logs, the 25-rule
engine, per-arm and per-tag statistics, the RQ3 coverage matrix, the complete
labeling protocol (all versions and the 2026-10-27 addendum), the 457-row
validation sample with evidence packets and final labels, and the analysis
scripts, at https://github.com/mallyagirish/k8s-misconfig-study (Apache-2.0).
An archival DOI (Zenodo) will be minted at submission. The corpus manifests
themselves remain under their original licenses and are rebuilt, not
redistributed.

## References (verified entries; remaining general citations to be completed in the pre-submission pass)

- [Rahman2023] A. Rahman, S. I. Shamim, D. B. Bose, and R. Pandita, "Security
  Misconfigurations in Open Source Kubernetes Manifests: An Empirical Study,"
  *ACM Transactions on Software Engineering and Methodology* 32(4), 1–36, 2023.
  DOI: 10.1145/3579639.
- [Minna2025] F. Minna, F. Massacci, and K. Tuma, "Analyzing and Mitigating
  (with LLMs) the Security Misconfigurations of Helm Charts from Artifact Hub,"
  *Empirical Software Engineering* 30:132, 2025. DOI: 10.1007/s10664-025-10688-0.
- [Eom2026] H. Eom, B. Suk, and S. Hwang, "An Empirical Study and Benchmark of
  Kubernetes Misconfiguration Scanners," *Proc. ISSTA 2026*. DOI: 10.1145/3832297.
- CIS Kubernetes Benchmark, Center for Internet Security.
- NSA & CISA, *Kubernetes Hardening Guide*.
- Kubernetes documentation: Pod Security Standards; Security Context.
- Tool documentation and check catalogues: kube-linter, kubeaudit, Polaris, Checkov.
- General configuration-error and IaC studies cited in Section 7.1 (final selection
  and verification pending).
