# Safe AI Remediation for Kubernetes-Based LLM Inference

**Working title:** Safe Remediation of Security Misconfigurations in Kubernetes-Based LLM Inference: A Benchmark of AI-Assisted Changes Under Serving Invariants

**Status:** Research proposal and protocol development. No empirical results are claimed.

## Motivation

Kubernetes-hosted LLM inference stacks combine ordinary workload security with serving-specific concerns: OpenAI-compatible API authentication, route-level authorization, gateway exposure, model and tokenizer endpoints, Ray/distributed control ports, GPU device access, model-cache volumes, secret injection, and readiness during long model loads. A patch that removes a generic scanner alert can still expose an inference endpoint, break streaming/API behavior, prevent model loading, or grant excessive access to GPU nodes.

This study proposes a benchmark focused specifically on safe remediation of LLM inference serving configurations. It will compare deterministic fixes, prompt-only LLMs, context-grounded LLMs, and constrained tool-using agents. A successful patch must satisfy independently defined security checks and serving/operational invariants.

## Research questions

- **RQ1 — Security correctness:** Does the patch close the targeted LLM-serving security weakness, including relevant route and resource context?
- **RQ2 — Serving preservation:** Does the patch preserve API behavior, health/readiness, model-serving configuration, and declared operational constraints?
- **RQ3 — Context value:** Does access to the full Helm chart/repository and version-pinned serving documentation improve results over manifest-only prompts?
- **RQ4 — Safe minimality:** Do approaches avoid broad privileges, disabled functionality, unrelated edits, and brittle hard-coded changes?
- **RQ5 — Cost and reliability:** What are safe-remediation success, failure modes, latency, token/API cost, and reproducibility?

## Proposed contributions

1. A versioned benchmark of LLM-inference-specific Kubernetes remediation tasks.
2. Independent security and serving acceptance oracles, including route-level and chart-level checks where feasible.
3. A comparative evaluation of deterministic and AI-assisted remediation under matched context conditions.
4. A failure taxonomy for security regressions, serving outages, invalid chart changes, and unsafe workarounds.

## Relationship to existing work

The parent Misconfigured by Default study measures detection and labeling quality for general Kubernetes misconfigurations. The companion llm-serving-k8s-hardening-study measures the prevalence of proposed security indicators in public LLM-serving configurations. This study asks a different question: whether AI can remediate those LLM-serving-specific issues while preserving serving behavior.

The literature already includes broad Helm-chart misconfiguration analysis and LLM-assisted repair, and recent work on Kubernetes misconfiguration taxonomies and schema-guided LLM repair. Therefore, this project will not claim novelty for generic Kubernetes YAML repair or schema validation alone. Its proposed differentiator is the LLM-inference domain and evaluation against serving-specific invariants (API routes/authentication, model-serving health, chart semantics, GPU and model-cache constraints). The literature review must test whether that gap remains before confirmatory work begins.

## Scope and safety boundaries

- Public, synthetic, and author-created LLM-serving configurations only.
- No employer-private manifests, customer data, credentials, or production clusters.
- Use disposable local clusters and mocked inference services for repeatable API/health tests.
- GPU-specific configuration may be assessed with static/device-plugin fixtures; do not claim real GPU performance validation unless hardware tests are actually performed.
- Never deploy generated patches to production.
- Record exact model versions, prompts, parameters, validators, chart versions, and dates.
- Separate chart-source/values remediation from rendered-manifest remediation; do not treat them as interchangeable.

## Milestones

- [x] Initial proposal and protocol drafted
- [x] Preliminary literature scan identified closely related prior work
- [ ] Complete structured related-work review and novelty decision
- [ ] Freeze LLM-serving task taxonomy and benchmark schema
- [ ] Build fixtures and independent security/serving oracles
- [ ] Implement baselines and isolated runner
- [ ] Pilot, revise, and freeze protocol
- [ ] Confirmatory evaluation and statistical analysis
- [ ] Manuscript, artifact release, and submission

## Reproducibility

Publish task definitions, fixtures, prompts, scripts, validators, and aggregate results where licensing permits. Each task must include provenance, Kubernetes/Helm version, expected security properties, serving invariants, and an independent review status.

**Important:** this repository currently contains a proposal, not completed experimental evidence. Do not cite planned task counts, expected improvements, or hypotheses as results.
