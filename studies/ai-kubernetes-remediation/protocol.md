# Study Protocol — AI-Driven Kubernetes Security Remediation

**Version:** 0.1 (draft; not preregistered)  
**Status:** Design phase. Freeze this protocol before the confirmatory evaluation.

## 1. Motivation

A scanner finding is only the beginning of remediation. A patch can remove one warning while creating another vulnerability or making a service unavailable. The meaningful unit of success is a patch that passes independently specified security checks and operational invariants—not merely one that parses or suppresses a scanner finding.

## 2. Scope and unit of analysis

The unit is a **remediation task**: a Kubernetes workload configuration, a target finding, the context supplied to the system, and ground-truth acceptance tests.

Candidate task families, aligned with the existing study's taxonomy:

- service-account token automounting and workload identity;
- privileged containers and Linux capability minimization;
- privilege escalation and non-root execution;
- host namespaces and hostPath exposure;
- resource requests/limits where operational invariants can be specified;
- image tag/digest integrity;
- RBAC scope and wildcard permissions;
- Secret references and secret-handling patterns (never real secret values);
- seccomp/AppArmor or related pod/container settings with explicit version support.

Do not include a task unless its expected secure state and operational invariants can be stated and tested.

## 3. Systems to compare

1. **No-op / unchanged configuration:** negative control.
2. **Deterministic baseline:** hand-authored transformation where a safe generic fix exists.
3. **Prompt-only LLM:** finding and relevant manifest; no retrieval or tool loop.
4. **Context-grounded LLM:** prompt-only inputs plus bounded repository context and version-pinned authoritative guidance.
5. **Constrained tool-using agent:** may inspect files and run read-only validators, then propose a patch. It cannot deploy to persistent clusters or access external credentials.

Record exact provider/model/version, API date, prompts, decoding settings, tool definitions, context limits, retries, and cost. Capture resolved model versions when available.

## 4. Benchmark construction

### Inclusion criteria

Each task must:
- represent a real Kubernetes configuration pattern or justified synthetic variant;
- have a reproducible starting manifest;
- map to a clearly defined security objective;
- include an independent security acceptance test;
- include functional/operational invariants appropriate to the workload;
- identify Kubernetes API and cluster versions;
- have provenance and licensing recorded;
- be reviewed by someone other than its author where feasible.

### Exclusion criteria

Exclude tasks with unavailable application context, no reliable oracle, real credentials/customer data/private employer material, unclear redistribution rights, or YAML parsing as the sole success criterion.

### Pilot and scale

Start with a pilot of **20–30 tasks** across at least five task families. Use it to validate the harness, task clarity, and scoring; do not treat pilot results as confirmatory. After revision and protocol freeze, target **100–150 tasks** only if task quality and independent review support that scale. Report the actual count and rationale.

## 5. Inputs and context conditions

- **Manifest-only:** finding, relevant manifest, and minimal schema/version metadata.
- **Repository-context:** the above plus a bounded set of related manifests, Helm values/templates, or workload metadata selected by a documented deterministic procedure.

Evaluate each task under each applicable condition. Do not give one system privileged information unavailable to others in the same comparison.

## 6. Execution and isolation

- Use disposable, isolated environments; pin Kubernetes distribution/version, admission policies, and validator versions.
- Use network restrictions and no cloud credentials by default.
- Never apply generated patches to production or shared clusters.
- Run each attempt from a clean copy with timeouts, quotas, and retry limits.
- Capture stdout/stderr and structured outcomes; redact sensitive values.
- Preserve failed runs rather than silently dropping them.

## 7. Outcomes

### Primary outcome

**Safe remediation success (binary):** the patch passes all required security acceptance tests **and** all required operational/functionality invariants for that task.

A patch that merely parses or removes the target scanner finding is not a success.

### Secondary outcomes

- **Security fix rate:** target weakness no longer present.
- **Regression rate:** one or more previously passing operational invariants fail.
- **New-risk rate:** patch introduces a separately defined security weakness.
- **Patch minimality:** changed lines/fields and proportion unrelated to the target fix, using a predeclared definition.
- **Completeness:** all required controls are addressed.
- **Explanation fidelity:** explanation accurately describes the patch and security effect, judged against a rubric.
- **Human review burden:** time and edits needed to reach an accepted patch, if a separate reviewer exercise is feasible.
- **Cost/latency:** wall-clock time, token usage, API cost, retries, and tool calls.

### Failure taxonomy

One or more labels per attempt:
- no patch, refusal, or timeout;
- syntactic/schema-invalid patch;
- target finding remains;
- incomplete remediation;
- insecure workaround (for example, broad privilege granted to make a workload run);
- operational regression;
- unrelated or excessive changes;
- hallucinated API field/resource;
- explanation does not match patch;
- nondeterministic or unreproducible result.

## 8. Ground truth and labeling

Task authors define expected security properties and operational invariants before evaluating systems. A second reviewer independently inspects each task and oracle. Resolve disagreements before confirmatory runs.

For subjective outcomes:
- use a written rubric with examples;
- blind raters to system identity where feasible;
- use at least two independent human raters for a subset or all examples, depending on feasibility;
- report raw agreement and an appropriate chance-corrected statistic with confidence intervals;
- adjudicate disagreements and retain original ratings.

Do not describe author-versus-model agreement as inter-rater reliability.

## 9. Statistical analysis plan

The task is the principal paired unit. Compare systems on the same tasks and context conditions.

- Report numerator/denominator and confidence intervals for binary outcomes.
- Report paired differences in safe-remediation success.
- Use task-family stratification and paired/cluster-aware methods as appropriate.
- Do not treat repeated model attempts on one task as independent tasks.
- Predefine handling of timeouts, refusals, malformed output, and missing observations. Default: a system failure counts as not safely remediated for the primary outcome.
- Report per-family results, not only pooled averages.
- Conduct sensitivity analyses excluding ambiguous tasks and separating synthetic from public-derived tasks.
- Correct for multiple comparisons when making multiple confirmatory claims.
- Publish analysis scripts and a data dictionary.

Choose the final method (for example, paired bootstrap, McNemar test, or mixed-effects logistic regression) after the final sample structure is known, then freeze it before confirmatory evaluation.

## 10. Threats to validity

- **Construct validity:** benchmark checks may not capture all operational constraints.
- **External validity:** synthetic/public tasks may not represent private production environments.
- **Oracle validity:** tests may be incomplete or tailored to expected fixes.
- **Model drift:** providers and aliases change; preserve versions and dates.
- **Prompt sensitivity:** document prompts and run sensitivity analysis.
- **Task leakage:** public tasks may occur in model training data; do not claim contamination-free evaluation.
- **Researcher degrees of freedom:** freeze selection, scoring, and primary comparisons before confirmatory runs.
- **Cost representativeness:** report measurement date and usage.

## 11. Ethics and data management

Use only public, synthetic, or author-created manifests that can lawfully be analyzed and redistributed. Never put real secrets in fixtures. Keep non-redistributable manifests out of the public artifact and publish derived metadata only when permitted. Do not test third-party live infrastructure. Disclose model/API use and comply with provider terms.

## 12. Reproducibility checklist

- [ ] Task IDs, provenance, license, Kubernetes version, and task-family metadata
- [ ] Immutable benchmark release/tag
- [ ] Versioned prompts and model identifiers
- [ ] Pinned validators, scanners, and cluster images
- [ ] Deterministic clean-room runner
- [ ] Explicit primary outcome and failure policy
- [ ] Independent oracle review
- [ ] Raw results and analysis scripts
- [ ] Environment and cost measurement documentation
- [ ] Limitations and deviations log

## 13. Protocol deviations

Timestamp every change after protocol freeze, record its reason and affected tasks/outcomes, and state whether it occurred before or after confirmatory evaluation. Never silently revise the primary outcome after inspecting results.
