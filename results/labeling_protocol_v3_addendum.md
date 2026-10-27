# Addendum to labeling protocol v3 — 2026-10-27

**Status:** Adopted by the author on 2026-10-27, arising from the
adjudication of the blinded kappa subset. This addendum extends
`labeling_protocol_v3.md`; the v3 text is unchanged and retained as the
base document. Amendments here are numbered to continue v3's sequence
(v3 amendments 1–4, refinements 5–9).

## Background

The author labeled the 30-row blinded subset (`results/kappa_subset/`)
blind on 2026-10-27. Agreement with the AI pre-labels was 24/30 (80%),
Cohen's kappa = 0.526. The pre-labels predate protocol v3 (they were
produced under v2), and the disagreements decomposed as follows:

- Four disagreements (K8S-086, K8S-217, K8S-300, K8S-345) were
  RES_*/REL_* rows where v3's amendment 2 (production scoping) sides
  with the author's FP against the v2 definitional TP. No protocol
  change follows from these; they are the known cross-standard class,
  re-adjudicated at scale in the verification pass (divergence class B).
- Two disagreements (K8S-432, K8S-452) were genuine judgment calls
  where v3 gave no explicit test. They are resolved by the rule-level
  amendments below, which govern all similar rows, not only these two.

The kappa figure is retained as measured. Final labels are produced
under v3 plus this addendum during the author's verification pass.

## Amendment 10 — SEC_DANGEROUS_CAPABILITY joins the infrastructure class

Refinement 7 of v3 places SEC_PRIVILEGED and the host-namespace rules
in an infrastructure class (FP `infra-need` for node-level agents whose
function requires the access). That class now extends to
SEC_DANGEROUS_CAPABILITY, under both of these conditions:

1. the container's capability drops include `ALL` (a drop-ALL baseline);
2. the added capabilities are required by the container's
   node-infrastructure function (e.g. CNI agent cgroup setup, CSI
   driver mounts).

Added capabilities beyond that function, or the absence of a drop-ALL
baseline, remain TP.

*Adjudication:* K8S-432 (Cilium `mount-cgroup`: SYS_ADMIN, SYS_CHROOT,
SYS_PTRACE over `drop: [ALL]`, mounting the host cgroup filesystem) is
FP (`infra-need`). *Sample effect:* no pre-label changes — of the 17
SEC_DANGEROUS_CAPABILITY rows in the validation sample, the only
drop-ALL infrastructure row was already pre-labeled FP; the rest lack a
drop-ALL baseline or an infrastructure function.

## Amendment 11 — RBAC wildcards confined to the project's own API groups

For RBAC_WILDCARD_RESOURCES and RBAC_WILDCARD_VERBS: a wildcard grant
is FP (standard operator pattern) when every wildcard grant in the
role is confined to API groups owned by the same project that ships
the role — no wildcard apiGroup, and no wildcard grant in the core
group or in foreign groups. Wildcards that span `*` apiGroups, the
core group, or foreign groups remain TP. The test applies per wildcard
grant, not per role: a role may carry non-wildcard rules in other
groups without affecting the classification of its wildcard grants.

*Adjudication:* K8S-452 (Flux `crd-controller`: wildcard resources and
verbs confined to the six `*.toolkit.fluxcd.io` groups) is FP.
*Sample effect:* this ratifies the pattern the pre-labels already
follow on the shipped Flux, Kasten, and linkerd operator roles.
K8S-012 (Crossplane) is flagged for the verification pass, where the
test is applied to its individual wildcard grants.

## Amendment 12 — Production scoping is determined by content where the path indicates test material

Amendment 2's production scoping keys off source tags. Where a file's
path places it under test or fixture material (e.g. `testdata/`,
`fixtures/`, test directories), the content determines the class even
when the repository's source tag is production.

*Sample effect:* K8S-300 (a liveness-probe finding in kustomize's
`testdata2` tree, tagged production) is reclassified as fixture and
joins the class-B treatment. K8S-183, K8S-297, K8S-375, and K8S-446 —
already fixture-tagged, with testdata paths — are confirmed in the
same class.
