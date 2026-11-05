# Cluster bootstrap intervals (by source)

Resamples sources (GitHub repositories / Helm charts) with replacement,
stratified by arm; 2000 replicates, seed 20261028
(`scripts/cluster_bootstrap.py`). Decided matched rows: 441 in
35 GitHub and 56 Helm clusters. Rules with
no decided rows in a replicate fall back to their full-sample precision.

| Quantity | Point | Cluster-bootstrap 95% CI |
|---|---:|---:|
| Population-weighted precision | 0.676 | [0.601, 0.805] |
| Adjusted finding total | 18,556 | [16,500, 22,118] |
| Pooled sample-row precision | 0.624 | [0.519, 0.705] |
| Cohen's kappa (30-row author–AI agreement subset) | 0.526 | [0.167, 0.841] |

Row-level (independence-assuming) intervals are narrower — e.g. weighted
precision [0.649, 0.750] by binomial variance propagation — and are
superseded by these cluster-resampled intervals, since findings within a
source are correlated (52.9% of v3 findings repeat a seen key).

## Sensitivity to the no-decided-rows fallback (added 2026-10-28; recomputed 2026-11-04 on the audit-corrected labels)

In 42 of 50,000 rule-replicates (0.08%) a resample contains no decided rows
for a rule — most often IMG_NO_DIGEST (23), whose decided rows sit in few
clusters. Re-running the bootstrap under three handlings gives
weighted-precision intervals identical to within 0.001:

| Fallback for a missing rule | Weighted precision 95% CI |
|---|---:|
| Full-sample precision (as reported) | [0.601, 0.805] |
| Pooled sample precision (0.624) | [0.601, 0.804] |
| Drop the rule's population, renormalize | [0.601, 0.805] |

The fallback choice does not affect the reported intervals.
