# Study Protocol — Safe AI Remediation for Kubernetes-Based LLM Inference

**Version:** 0.2 (scope revised after preliminary related-work scan; draft, not preregistered)  
**Status:** Design phase. Freeze before confirmatory evaluation.

## 1. Motivation and research gap

Generic Kubernetes security remediation is already an active research topic. This study narrows the question to LLM inference serving, where security changes interact with route-level API behavior, model loading, readiness, streaming, distributed serving components, GPU access, and model-cache storage.

The study evaluates whether an AI-assisted patch is both secure and operationally safe for an LLM-serving workload. A syntactically valid YAML patch or a suppressed scanner alert is not sufficient.

## 2. Scope and unit of analysis

The unit is a remediation task: a versioned Helm chart or Kubernetes configuration, a target LLM-serving security weakness, the context provided to a remediation system, and independently specified security and serving acceptance tests.

Candidate task families:
- API authentication and route coverage, including sibling inference/operational endpoints;
- Ingress/Gateway exposure, TLS, and route allowlisting;
- NetworkPolicy and distributed/Ray/KV-transfer port isolation;
- secret references for model registry/Hugging Face tokens and API credentials;
- GPU device/resource configuration and privileged GPU access;
- model/cache PVCs, hostPath, writable mounts, and initContainers;
- workload securityContext (non-root, privilege escalation, seccomp) where image behavior is known;
- readiness/startup and model-loading behavior;
- image provenance and immutable references.

Do not include a task unless its target security property and serving invariants can be tested. Where a property depends on cloud load balancers, external identity providers, real GPUs, or undocumented application behavior, either construct a controlled test fixture or mark it out of scope.

## 3. Remediation systems

1. No-op baseline: unchanged configuration.
2. Deterministic baseline: documented, hand-authored transformation for cases with a safe generic fix.
3. Prompt-only LLM: finding and relevant manifest/chart values only.
4. Context-grounded LLM: bounded repository context plus version-pinned official serving/Kubernetes documentation.
5. Constrained agent: read repository files and run read-only validators, then propose a patch. No external credentials, production access, or persistent-cluster deployment.

For every run, record exact provider/model/version, API date, prompt, decoding settings, tool permissions, context selection, retries, token use, cost, and latency.

## 4. Benchmark construction

### Inclusion criteria

Each task must:
- be a public, synthetic, or author-created LLM inference configuration with documented provenance and license;
- have a reproducible starting point and pinned chart/manifest version;
- target one clearly stated security weakness;
- include an independent security acceptance test;
- include serving invariants appropriate to the task (for example, expected HTTP route behavior, readiness, or model API contract);
- identify Kubernetes and Helm versions;
- be reviewed by someone other than the task author where feasible.

### Exclusion criteria

Exclude tasks with no reliable oracle, unavailable application context, real secrets/customer data/employer material, unclear redistribution rights, or success criteria based only on YAML parsing or scanner silence.

### Pilot and scale

Start with 15–25 carefully reviewed tasks across at least four LLM-serving task families. Use the pilot to validate test oracles and setup/teardown; do not treat it as confirmatory. Expand only if task quality and independent review justify it. A smaller, high-quality domain-specific benchmark is preferable to an inflated task count.

## 5. Context conditions and patch targets

Evaluate matched tasks under:
- Manifest-only context: target finding, relevant rendered YAML, and API/version metadata.
- Chart/repository context: the above plus relevant Helm templates, values schema, related resources, and bounded documentation selected by a deterministic procedure.

Where the source is Helm, distinguish:
- patching the chart's values/configuration;
- patching chart templates;
- patching only the rendered Kubernetes output.

A valid chart-level patch must preserve parameterization and render successfully for the pinned chart version. A rendered-manifest patch must not be presented as a chart fix.

## 6. Isolation and serving test harness

- Use disposable local clusters or isolated CI environments with pinned Kubernetes versions.
- Use mock inference containers or deterministic test servers for HTTP, streaming, readiness, and health invariants.
- Do not require paid cloud resources or real secrets.
- For GPU-related tasks, use static manifest/device-plugin contract checks unless actual GPU hardware is explicitly available; report this boundary.
- Apply patches only to clean disposable copies.
- Capture test output, patch diffs, resource usage, timeouts, and failures.
- Never test third-party live infrastructure or deploy to production.

## 7. Outcomes

### Primary outcome

Safe remediation success (binary): the patch passes every required security acceptance test and every required serving/operational invariant for that task.

### Secondary outcomes

- target weakness fixed;
- route-level authentication and allowlist correctness;
- serving/API contract regression rate;
- readiness/model-loading invariant pass rate;
- new security-risk rate;
- chart render/schema validation success;
- patch minimality and unrelated-change rate;
- explanation fidelity;
- human review time/edits, if independently measured;
- latency, tokens, API cost, retries, and tool calls.

### Failure taxonomy

- no patch/refusal/timeout;
- YAML/schema/chart-render invalid;
- target weakness remains;
- route bypass or incomplete authentication;
- insecure workaround (for example, privileged mode or broad network exposure);
- model-serving/API/streaming/readiness regression;
- GPU/device configuration regression;
- cache/storage or secret-handling regression;
- unrelated/excessive edits;
- hallucinated API/chart value;
- explanation mismatch;
- nondeterministic/unreproducible output.

## 8. Ground truth and independent review

Task authors define expected security properties and serving invariants before system evaluation. A second reviewer independently inspects each task and oracle. Resolve disagreements before confirmatory runs.

For subjective patch-quality outcomes, use a written rubric, blind raters to system identity where feasible, report agreement and confidence intervals, and preserve adjudication history. Do not treat author-versus-model agreement as inter-rater reliability.

## 9. Statistical analysis

The task is the paired unit. Compare systems on the same tasks and context conditions.
- Report numerator/denominator and confidence intervals for primary binary outcomes.
- Report paired differences and per-task-family results.
- Repeated model attempts are not independent tasks.
- Predefine treatment of timeouts/refusals; default is failure for primary outcome.
- Separate synthetic and public-derived tasks in sensitivity analysis.
- Correct for multiple comparisons where relevant.
- Choose final tests after benchmark structure is fixed, then freeze analysis before confirmatory evaluation.

## 10. Threats to validity

- External validity: public/synthetic configs may not represent production inference clusters.
- Oracle validity: mock services may not capture full model/GPU behavior.
- Construct validity: static checks can overstate exposure if external controls are unknown.
- Model drift: record immutable model/version information and dates.
- Task leakage: public configs may occur in model training data.
- Researcher bias: authors create tasks and oracles; independent review is essential.
- Domain coverage: selected serving engines and charts may not represent all inference stacks.

## 11. Ethics and reproducibility

Use only redistributable public, synthetic, or author-created artifacts. Never include real credentials or employer data. Publish task provenance, chart/Kubernetes versions, prompts, validators, environment definitions, raw outputs with sensitive values redacted, and analysis scripts where licensing permits.

## 12. Release gates

- [ ] Related-work review and novelty positioning completed
- [ ] Every task has independent security and serving oracles
- [ ] Chart-level and rendered-manifest patches are distinguished
- [ ] Mock-serving harness is reproducible
- [ ] GPU limitations are explicitly documented
- [ ] Independent task/oracle review completed
- [ ] Pilot exit criteria passed
- [ ] Protocol and analysis plan frozen before confirmatory runs
- [ ] All results regenerate from a pinned artifact release

## 13. Protocol deviations

Timestamp every change after protocol freeze, explain its reason and affected tasks/outcomes, and state whether it occurred before or after confirmatory evaluation. Never silently revise the primary outcome after inspecting results.
