# RQ3b — Scanner detection accuracy against verified ground truth (Helm arm)

Companion to `tool_coverage_matrix.md`. The matrix compares what each tool
*can* check and how its *counts* compare; this analysis scores each tool against
the author-verified labels of the validation sample: for every sampled finding,
did the tool actually report the corresponding practice on that object?

## Method

Ground truth is the 126 Helm-arm rows of the validation sample
(`labeling_sample_v2_prelabelled.csv`), with final labels constructed as in
`precision_provisional.md`: the pre-label, replaced by the v3 recommendation
(`verification_divergence.csv`) for the 92 divergence rows. That gives 73 TP,
50 FP, 2 TP-hardening (IMG_NO_DIGEST with an explicit tag), and 1 EXCLUDED row
(K8S-436, dropped). The 2 TP-hardening rows are reported separately and enter
neither rate. Check-to-rule mapping follows `tool_coverage_matrix.md`, including
its semantics notes: union mappings where a tool splits one practice across two
checks (kubeaudit limits), and merged mappings where one check covers two of
our rules (kube-linter `latest-tag`). Three matrix cells list checks that
measure a *different property* than the rule (kube-linter `liveness-port` /
`readiness-port`, which validate probe ports rather than probe absence;
kube-linter `deprecated-service-account-field`, a field rather than an API
version; kube-linter `unsafe-sysctls`/`docker-sock` for dangerous capabilities);
following the matrix's own Finding 5, these are treated as **no check**. The
same applies to Polaris `pullPolicyNotAlways` for IMG_NO_DIGEST ("a proxy, not
pinning") and to Checkov's RBAC_CLUSTER_ADMIN_BINDING cell: the matrix cites
unspecified CKV2 graph checks (~4–23), and none of the CKV2 checks present in
the output (CKV2_K8S_1–5) is a cluster-admin-binding check, so no defensible
mapping exists.

Each tool's raw output (`results/tools/`) was parsed to (file, kind, name,
container, check) reports. kube-linter and Checkov outputs carry the source
file, so they join on (file, kind, name) — kube-linter also names the container
in its diagnostic messages (except `env-var-secret`, whose messages are
redacted in the raw output, and the host-* checks, which are object-level),
while Checkov reports at object level only. kubeaudit (run per file, but its
JSONL records carry no file name) and Polaris (no file name in its output) join
on (kind, name, container) instead. 12 of the 126 sampled objects share a
(kind, name) with an object in another chart (e.g. `pilot-postgresql` appears
in 4 charts); for those, a file-less tool is credited with DETECTED only when
the check fired on *every* instance of the key (or on none, for MISSED), and
is otherwise classified AMBIGUOUS_JOIN and excluded from that tool's rates.
This affected 2 rows for Polaris (K8S-031, K8S-192) and none for kubeaudit.
Per row and tool the classification is NO_CHECK (no mapped check for the rule),
DETECTED, MISSED, or AMBIGUOUS_JOIN; full per-row data is in
`tool_accuracy.csv`. Rates are Wilson 95% CIs throughout. Parser totals were
reconciled against the matrix: 64 of 65 mapped-check counts reproduce exactly;
the exception is Polaris `readinessProbeMissing` (204 failures in the raw
output vs 205 in the matrix — the raw output governs here).

## Headline results

| Tool | TP detection, check exists | TP detection, effective (all 73 TPs) | FP-flagging, check exists |
|---|---|---|---|
| kube-linter | 38/42 = 0.90 [0.78, 0.96] | 38/73 = 0.52 [0.41, 0.63] | 35/38 = 0.92 [0.79, 0.97] |
| kubeaudit | 40/41 = 0.98 [0.87, 1.00] | 40/73 = 0.55 [0.43, 0.66] | 36/38 = 0.95 [0.83, 0.99] |
| Polaris | 54/58 = 0.93 [0.84, 0.97] (+1 amb.) | 54/72 = 0.75 [0.64, 0.84] (+1 amb.) | 26/30 = 0.87 [0.70, 0.95] (+1 amb.) |
| Checkov | 47/62 = 0.76 [0.64, 0.85] | 47/73 = 0.64 [0.53, 0.74] | 42/49 = 0.86 [0.73, 0.93] |

TP rows with no check at all, by tool: kube-linter 31, kubeaudit 32, Polaris 14, Checkov 11. The "effective" column counts those as missed, so the gap between the two
TP columns is pure coverage; the gap between the check-exists column and 1.0 is
detection semantics.

Reading: where a tool has a check, it usually fires on verified TPs
(0.90–0.98 for kube-linter, kubeaudit, Polaris; 0.76 for Checkov). But the same
checks also fire on most verified FPs (FP-flagging 0.86–0.95): the tools share
the naive engine's context-blindness — the FP classes of taxonomy v2
(infrastructure agents, standard operator patterns, least-privilege capability
sets) fool the tools at roughly the same rate they fooled the unvalidated
rules. The tools' accuracy problem on this ground truth is therefore twofold:
coverage (effective TP detection only 0.52–0.75) and context, not raw
detection on the practices they do check. Checkov is the partial exception on
both axes: widest coverage (effective 0.64 despite the lowest check-exists
detection), because `CKV_K8S_23` systematically misses containers that run as
root *explicitly* (8 of its 15 check-exists TP misses are
SEC_RUN_AS_ROOT_EXPLICIT) and `CKV_K8S_49` catches only part of wildcard RBAC
(7 of 10 sampled TP wildcard rows missed).

TP-hardening rows (2, both IMG_NO_DIGEST): only Checkov has a check
(`CKV_K8S_43`) and it detects both; the other three tools have no check.

## Per-rule breakdown (rules with >= 5 verified TPs)

TP detection where a check exists (detected / checked TP rows):

| Rule | TP n | kube-linter | kubeaudit | Polaris | Checkov |
|---|---:|---:|---:|---:|---:|
| RBAC_CLUSTER_ADMIN_BINDING | 7 | no check | no check | 7/7 | no check |
| RBAC_WILDCARD_RESOURCES | 7 | no check | no check | no check | 2/7 |
| SEC_PRIVILEGED | 10 | 10/10 | 9/10 | 9/9 (+1 amb.) | 10/10 |
| SEC_RUN_AS_ROOT_EXPLICIT | 9 | 9/9 | 9/9 | 9/9 | 1/9 |

Notable: kube-linter and Checkov detect all 10 sampled privileged TPs;
Polaris detects 9 of 9 decidable rows (1 ambiguous join); kubeaudit detects
9 (the CronJob blind spot below). kube-linter and kubeaudit have no
wildcard-RBAC
check at all; Polaris has the only cluster-admin-binding checks and detects
all 7 sampled TPs, while Checkov has no mappable check for that rule.

## Per-family breakdown

Families (this analysis' grouping of the 25 rules): Images (IMG_*), Resources
(RES_*), Reliability (REL_*), Security context (SEC_*), Host & identity
(HOST_* + SA_TOKEN_AUTOMOUNTED), RBAC, secrets & API (RBAC_*, SECRET_*,
DEPRECATED_API). Cells give detected/n over rows where a check exists,
TP detection first, then FP-flagging.

| Family | Tool | TP detection | FP-flagging |
|---|---|---|---|
| Images | kube-linter | 5/5 = 1.00 | 1/1 = 1.00 |
| Images | kubeaudit | 2/2 = 1.00 | 1/1 = 1.00 |
| Images | Polaris | 5/5 = 1.00 | 1/1 = 1.00 |
| Images | Checkov | 5/5 = 1.00 | 1/1 = 1.00 |
| Resources | kube-linter | 10/11 = 0.91 | — (no checked rows) |
| Resources | kubeaudit | 7/7 = 1.00 | — (no checked rows) |
| Resources | Polaris | 7/11 = 0.64 | — (no checked rows) |
| Resources | Checkov | 11/11 = 1.00 | — (no checked rows) |
| Reliability | kube-linter | — (no checked rows) | — (no checked rows) |
| Reliability | kubeaudit | — (no checked rows) | — (no checked rows) |
| Reliability | Polaris | 6/6 = 1.00 | 0/1 = 0.00 |
| Reliability | Checkov | 6/6 = 1.00 | 0/1 = 0.00 |
| Security context | kube-linter | 23/26 = 0.88 | 23/24 = 0.96 |
| Security context | kubeaudit | 29/30 = 0.97 | 25/26 = 0.96 |
| Security context | Polaris | 29/29 = 1.00 (+1 amb.) | 23/26 = 0.88 |
| Security context | Checkov | 22/30 = 0.73 | 25/26 = 0.96 |
| Host & identity | kube-linter | — (no checked rows) | 10/10 = 1.00 |
| Host & identity | kubeaudit | — (no checked rows) | 10/11 = 0.91 |
| Host & identity | Polaris | — (no checked rows) | — (no checked rows) |
| Host & identity | Checkov | — (no checked rows) | 11/11 = 1.00 |
| RBAC, secrets & API | kube-linter | — (no checked rows) | 1/3 = 0.33 |
| RBAC, secrets & API | kubeaudit | 2/2 = 1.00 | — (no checked rows) |
| RBAC, secrets & API | Polaris | 7/7 = 1.00 | 2/2 = 1.00 (+1 amb.) |
| RBAC, secrets & API | Checkov | 3/10 = 0.30 | 5/10 = 0.50 |

## Misses worth naming (all verified against the raw outputs)

- **kubeaudit is blind to CronJob templates in this run**: it produced zero
  records of any kind for `pilot-zammad-cronjob-reindex`, missing a verified
  privileged TP (K8S-218) that kube-linter and Polaris both catch.
- **kube-linter's privilege-escalation check fires only on explicit
  `allowPrivilegeEscalation: true`**, not on the unset case — 3 of its 4
  check-exists TP misses are SEC_APE_NOT_DISABLED on unset containers (its
  arm-wide count for the check is 34 against 309 engine findings).
- **Polaris's resource misses concentrate on CronJob and init containers**
  (K8S-004/269 CronJob `check-db-ready`; K8S-026/135 an init container),
  suggesting its pod-spec traversal skips those in this version.
- **Checkov `CKV_K8S_23`** (run-as-root) did not fire on any of 8 sampled
  explicit-root TPs — mostly `volume-permissions`-style init containers with
  `runAsUser: 0` — even on objects where it reported 15 other failed checks.

## Caveats

- **Small ground truth.** 126 rows (123 TP/FP) is a modest set, and it is a
  *stratified* sample, not a random draw of findings: SEC_PRIVILEGED is
  deliberately over-represented (29 rows). Rates are per sampled row, not
  population estimates; per-rule cells with n < 5 are grouped into families
  for that reason, and CIs are wide throughout.
- **Engine-findings-only scope.** Ground truth consists of findings *our
  engine* produced. A tool cannot be scored on objects the engine never
  flagged, so this analysis measures agreement-with-verified-engine-findings,
  not absolute recall or precision of the tools. (E.g. all four tools flag
  missing `readOnlyRootFilesystem`, a practice our taxonomy v1 lacks.)
- **Matching granularity differs by tool.** Checkov is object-level only, so
  a report on the right object but a different container would still count as
  DETECTED; kube-linter and Polaris match at container level where their
  output supports it (kube-linter `env-var-secret` excepted — its messages are
  redacted), and kubeaudit pod-level auditors (e.g. `LimitsNotSet`) match at
  object level. Cross-tool comparisons inherit this asymmetry.
- **Merged checks** (flagged per row in the CSV) count as a detection for
  either merged rule: e.g. kube-linter `latest-tag` cannot distinguish
  IMG_UNTAGGED from IMG_LATEST, and `unset-*-requirements` cannot distinguish
  missing limits from missing requests. This flatters those tools slightly
  on both merged rules.
- **Broader/narrower/composite checks** keep their matrix semantics: e.g.
  Polaris `linuxHardening` (seccomp composite) firing does not prove the
  seccomp sub-property was the failing one; kubeaudit `AutomountSAToken...`
  covers only the default service account; kube-linter
  `drop-net-raw-capability` covers only NET_RAW.
- **Ambiguous joins** (file-less tools, duplicated (kind, name) keys) are
  excluded from rates, not silently resolved: 2 Polaris rows. If credited as
  detections, Polaris's TP figures would rise slightly; as misses, fall.
- kubeaudit's `SeccompProfileMissing` mapping follows the matrix; the raw
  output also contains 1 `SeccompDisabledPod` record, not mapped to any rule.

Files: `tool_accuracy.csv` (504 rows = 126 sampled findings x 4 tools).
Analysis script: rerun from the raw outputs in `results/tools/`; parser
totals reconciled against `tool_coverage_matrix.md` as described above.
