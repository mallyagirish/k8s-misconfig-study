# Experiment Matrix and Benchmark Task Template

## A. Core experiment matrix

| Dimension | Planned levels | Notes |
|---|---|---|
| Remediation system | No-op; deterministic; prompt-only LLM; context-grounded LLM; constrained agent | Record exact model/version and permissions |
| Context | Manifest-only; bounded repository context | Paired within task |
| Task family | Security context; identity/RBAC; host access; image integrity; resource/reliability; secret references | Final families depend on oracle quality |
| Repetitions | Pilot to estimate variance; confirmatory repetitions pre-specified | Retries are not independent tasks |
| Primary outcome | Safe remediation success | Must pass security and operational oracles |
| Secondary outcomes | Fix rate; regression; new risk; minimality; explanation; latency/cost | Define scoring before confirmatory run |

## B. Benchmark task record

Each task should record:
- task_id: stable unique identifier;
- source_type: synthetic, author-created, or public-derived;
- source_uri and source_commit: provenance where applicable;
- license: license or redistribution decision;
- kubernetes_version: target API/server version;
- task_family: controlled taxonomy label;
- finding_id: stable weakness identifier;
- description: concise issue description;
- input_files: fixture paths;
- security_invariants: assertions that must hold after remediation;
- operational_invariants: assertions that must continue to hold;
- expected_change_scope: fields/resources expected to change, without overconstraining valid alternatives;
- oracle_version: version of tests and expected-outcome definition;
- review_status: author-reviewed, independently-reviewed, or adjudicated.

## C. Illustrative task record

~~~yaml
task_id: K8S-REM-0001
source_type: synthetic
source_uri: null
source_commit: null
license: CC0-1.0
kubernetes_version: "1.30"
task_family: security-context
finding_id: run-as-root
description: >
  A workload container runs as root without a documented requirement.
input_files:
  - fixtures/K8S-REM-0001/deployment.yaml
security_invariants:
  - container_must_not_run_as_root
  - privilege_escalation_must_be_disabled
operational_invariants:
  - deployment_rollout_completes
  - service_health_check_passes
expected_change_scope:
  - pod.spec.securityContext
  - pod.spec.containers[*].securityContext
oracle_version: "0.1"
review_status: author-reviewed
~~~

## D. Initial task families and oracle questions

1. **Non-root execution:** Does the image support a non-root UID? Can the test prove the process runs as non-root rather than merely checking a YAML field?
2. **Privilege escalation:** Is disabling privilege escalation compatible with the workload? Does the test catch a workaround that grants broader privileges?
3. **Service-account tokens:** Does the workload need Kubernetes API access? If disabled, does the application still function? If enabled, is RBAC least-privilege?
4. **RBAC wildcard:** Can required verbs/resources be inferred from an explicit workload contract? Does the proposed role avoid wildcard permissions while preserving required operations?
5. **HostPath/host namespaces:** Can the dependency be removed or replaced? Does the test detect a patch that merely changes the path?
6. **Image integrity:** Is an immutable digest available and compatible with deployment workflow? Never invent a digest.
7. **Resource bounds:** Are limits/requests based on workload evidence? Do not assert arbitrary values as universally correct.
8. **Secret handling:** Does the patch preserve reference-based injection without exposing values or embedding credentials?

## E. Draft scoring rubric

| Score | Interpretation |
|---|---|
| 0 | No usable patch, invalid patch, or target weakness remains |
| 1 | Target finding removed but security or operational regression occurs |
| 2 | Security checks pass, but operational invariants fail or are unverified |
| 3 | Security and operational invariants pass; patch has material unnecessary changes |
| 4 | Security and operational invariants pass; patch is minimal, reviewable, and explanation is accurate |

Use the binary primary outcome for statistical comparison. The 0–4 rubric is secondary and must be independently rated with documented criteria. A score of 4 cannot substitute for passing automated oracles.

## F. Pilot exit criteria

Do not start confirmatory evaluation until:
- every pilot task has reproducible setup and teardown;
- the primary outcome is computable without subjective interpretation;
- the oracle detects plausible unsafe workarounds in each relevant task family;
- system inputs and permissions are equivalent within each comparison;
- all failure categories can be represented in the result schema;
- independent review has resolved task ambiguity;
- the analysis plan and exclusions are frozen.
