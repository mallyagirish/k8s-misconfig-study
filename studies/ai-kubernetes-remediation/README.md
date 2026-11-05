# Beyond Detection: Evaluating AI Agents for Safe Kubernetes Security Remediation

**Status:** Research proposal and protocol development. No empirical results are claimed.

## Abstract

Kubernetes scanners can identify configuration weaknesses, but detection does not ensure a workload is made safer. Remediation requires interpreting findings in context, changing the right fields, preserving application behavior, and proving that security and operational constraints still hold. A syntactically valid patch can remain insecure, incomplete, or operationally harmful.

This study proposes a reproducible benchmark for evaluating AI-generated Kubernetes security remediations. It will compare deterministic rule-based fixes, prompt-only LLMs, retrieval-grounded LLMs, and constrained tool-using agents on curated vulnerable configurations. Evaluation will measure security correctness, functional preservation, patch minimality, explanation fidelity, execution cost, and failure modes. All tests will use isolated, non-production workloads and explicit ground-truth invariants.

## Research questions

- **RQ1 — Remediation correctness:** How often does each approach actually remove the target security weakness?
- **RQ2 — Operational safety:** How often does a security fix preserve workload functionality and declared operational invariants?
- **RQ3 — Context sensitivity:** Does repository/workload context improve remediation quality compared with a finding and manifest alone?
- **RQ4 — Patch quality:** How do approaches compare on minimality, unnecessary changes, explanation fidelity, and reviewability?
- **RQ5 — Cost and reliability:** What are latency, token/API cost, retry rate, and reproducibility characteristics?

## Proposed contributions

1. A versioned benchmark of Kubernetes remediation tasks with explicit security properties and operational invariants.
2. A comparative evaluation of deterministic and AI-based remediation strategies.
3. A failure taxonomy covering incomplete fixes, unsafe privilege changes, behavior-breaking patches, hallucinated fields, and unsupported claims.
4. A practical human-in-the-loop workflow for validating AI-generated infrastructure changes.

## Relationship to the existing study

The parent study, *Misconfigured by Default*, measures the prevalence of Kubernetes configuration weaknesses and the coverage/precision of manifest-auditing tools. This follow-on asks what happens after a weakness is detected. It has distinct research questions and outcome measures; prevalence estimates from the parent study will not be presented as remediation evidence.

## Study boundaries

- Kubernetes manifests and Helm-rendered manifests; no live production clusters.
- Public, synthetic, and deliberately constructed test workloads only.
- No real secrets, credentials, customer data, employer code, or employer systems.
- Patches evaluated in disposable local clusters or isolated CI environments.
- No autonomous deployment to production.
- Record model names, versions, prompts, parameters, tool versions, and evaluation dates.
- Distinguish benchmark performance from claims about production effectiveness.

## Milestones

- [x] Research question and initial scope drafted
- [x] Initial protocol and evaluation dimensions drafted
- [ ] Literature review and novelty check
- [ ] Benchmark task specification and inclusion criteria
- [ ] Build task corpus and independent ground-truth review
- [ ] Implement baseline remediation systems
- [ ] Implement isolated validation harness
- [ ] Pilot study and protocol freeze
- [ ] Full evaluation, statistical analysis, and sensitivity checks
- [ ] Manuscript, artifact documentation, and submission

## Reproducibility

Publish code, task definitions, manifests, scoring rules, and aggregate results where licensing and safety permit. Every benchmark item will include provenance and a versioned expected-outcome specification. Retain model-generated patches and logs with sensitive values redacted.

## Important

This repository currently contains a **proposal**, not completed experimental evidence. Do not cite projected sample sizes, expected improvements, or hypotheses as findings. Refine the protocol after a literature review and pilot.
