# Experiment Matrix — LLM Inference Remediation Benchmark

## A. Core experiment matrix

| Dimension | Planned levels | Notes |
|---|---|---|
| Remediation system | No-op; deterministic; prompt-only LLM; context-grounded LLM; constrained agent | Record exact model/version and permissions |
| Context | Rendered manifest only; chart/repository context | Paired within task |
| Patch target | Values; Helm templates; rendered manifest | Analyze separately; not interchangeable |
| Task family | API auth/routes; ingress/network; secrets; GPU/device; model-cache/storage; workload security; readiness | Final levels depend on oracle quality |
| Serving tests | HTTP API; streaming; health/readiness; model-load contract | Mock server unless actual model environment is available |
| GPU tests | Static/device-plugin contract; optional hardware-backed | Never imply GPU runtime validation from static checks |
| Primary outcome | Safe remediation success | All security and serving oracles must pass |
| Secondary outcomes | Target fix; regressions; new risks; chart render; minimality; explanation; cost/latency | Freeze scoring before confirmatory run |

## B. Task record schema

Each task should record:
- task_id, source_type, source_uri, source_commit, license;
- engine/chart name and version;
- Kubernetes and Helm versions;
- task_family and finding_id;
- input_files and patch_target (values/template/rendered-manifest);
- security_invariants;
- serving_invariants;
- expected_change_scope;
- setup/teardown and oracle commands;
- oracle_version;
- review_status and reviewer roles.

## C. Candidate task families and oracle design

1. API authentication and route coverage: verify intended routes require auth and sensitive sibling routes are blocked; test unauthenticated and authenticated requests against a mock OpenAI-compatible API.
2. Ingress and network boundaries: verify only intended routes/ports are reachable in a local cluster; do not infer cloud internet exposure from Service type alone.
3. Secret references: verify token values are not embedded in ConfigMaps or plain env values and reference injection still works using synthetic credentials.
4. GPU privilege and resource configuration: verify least-privilege manifest structure and device-plugin contract. Runtime GPU behavior requires explicit hardware-backed tests.
5. Model/cache storage: verify mounts, access modes, and permissions against a declared trust model; test mock model load and cache write requirements.
6. Workload securityContext: verify non-root/privilege constraints and that the mock inference process still starts.
7. Readiness and startup: verify a slow-starting mock model becomes ready only after initialization and that probes do not cause restart loops.
8. Helm chart semantics: patch values/templates, render the pinned chart, and assert the resulting resources and application contract.

## D. Primary outcome and failure policy

A task succeeds only when all required security assertions and all serving invariants pass. A patch that parses, renders, or suppresses a scanner alert but fails a serving check is not a success. A timeout/refusal/no-patch counts as failure for the primary outcome.

## E. Pilot exit criteria

- every task has clean setup and teardown;
- security and serving oracles fail on the original vulnerable configuration where expected;
- safe reference remediation passes all required oracles;
- deliberately unsafe workarounds are rejected;
- chart values/templates render deterministically;
- no task relies on unrecorded cloud settings or credentials;
- independent review resolves ambiguous task expectations;
- protocol and analysis plan are frozen before confirmatory evaluation.
