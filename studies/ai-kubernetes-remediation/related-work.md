# Preliminary Related-Work Review and Novelty Decision

**Status:** Preliminary scan; not a systematic review. This review changed the project scope before any confirmatory experiment.

## Closely related publications

### General Helm-chart security and LLM repair

Minna, F., Massacci, F., and Tuma, K. (2025). “Analyzing and mitigating (with LLMs) the security misconfigurations of Helm charts from Artifact Hub.” Empirical Software Engineering, 30(5), 132. https://doi.org/10.1007/s10664-025-10688-0

The study mines 4,961 Helm chart templates, compares seven analyzers, and evaluates LLM-generated fixes. It reports that context size matters and that a model can remove unrelated configuration and break an application. This means generic Helm misconfiguration detection plus LLM remediation is not a defensible novelty claim.

### General Kubernetes misconfiguration and LLM repair

Ghorab, M. A., Abdel Latif, A., and Saied, M. A. (2026). “Kubernetes Misconfigurations in the Wild: Taxonomy, Evolution, and Automated Repair with Large Language Models.” arXiv:2609.27030; DOI: https://doi.org/10.1145/3805760.3814908

The reported study uses 2,662 Stack Overflow issues, studies misconfiguration taxonomy/evolution, and evaluates LLM remediation with schema-guided validation. It is directly overlapping with a broad benchmark of generic Kubernetes security repair. This project therefore narrows to LLM inference serving and serving-specific operational invariants.

### Community-prescribed Kubernetes security configurations

Shamim, S. I., Hu, H., and Rahman, A. (ICSE 2025). “On Prescription or Off Prescription?: An Empirical Study of Community-prescribed Security Configurations for Kubernetes.” https://akondrahman.github.io/publication/icse25

This work examines CIS-recommended configurations, 544 files, practitioner awareness, and static analyzer performance. It is relevant background for rule selection and scanner evaluation.

## Revised research question

Can AI-assisted systems remediate security weaknesses in Kubernetes-based LLM inference stacks while preserving endpoint authentication semantics, serving API behavior, readiness/model-loading behavior, Helm chart semantics, and GPU/model-cache constraints?

## Differentiation to test, not assume

The candidate contribution is not generic YAML repair, schema validation, or a broad Kubernetes misconfiguration taxonomy. It is a reproducible benchmark for LLM-inference-specific remediation where security and serving invariants are both evaluated. Candidate task families include route-level API authentication, gateway allowlists, distributed/Ray ports, model-token secret handling, GPU privilege/device settings, model-cache trust, and serving readiness.

The project should use mock OpenAI-compatible services and disposable local clusters for deterministic API/health tests. GPU behavior must be described as static/device-plugin-contract validation unless actual hardware experiments are performed.

## Required systematic review

Before freezing the protocol, search ACM Digital Library, IEEE Xplore, SpringerLink, USENIX, arXiv, and relevant serving-engine documentation using combinations of:
- Kubernetes LLM inference security;
- vLLM deployment hardening;
- TGI/SGLang/Ollama Kubernetes security;
- LLM serving API authentication and route authorization;
- GPU multi-tenancy and model-cache security;
- LLM-assisted infrastructure-as-code remediation;
- Kubernetes remediation benchmark and operational regression.

Record databases, date, query strings, inclusion/exclusion decisions, and all directly overlapping studies. If a substantially similar LLM-serving remediation benchmark exists, revise the contribution rather than forcing a novelty claim.
