# Cluster bootstrap intervals (by source)

Resamples sources (GitHub repositories / Helm charts) with replacement,
stratified by arm; 2000 replicates, seed 20261028
(`scripts/cluster_bootstrap.py`). Decided matched rows: 441 in
35 GitHub and 56 Helm clusters. Rules with
no decided rows in a replicate fall back to their full-sample precision.

| Quantity | Point | Cluster-bootstrap 95% CI |
|---|---:|---:|
| Population-weighted precision | 0.699 | [0.623, 0.840] |
| Adjusted finding total | 19,199 | [17,120, 23,071] |
| Pooled sample-row precision | 0.633 | [0.527, 0.714] |
| Cohen's kappa (30-row author–AI agreement subset) | 0.526 | [0.167, 0.841] |

Row-level (independence-assuming) intervals are narrower — e.g. weighted
precision [0.649, 0.750] by binomial variance propagation — and are
superseded by these cluster-resampled intervals, since findings within a
source are correlated (52.9% of v3 findings repeat a seen key).
