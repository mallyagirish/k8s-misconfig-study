#!/usr/bin/env python3
"""Cluster bootstrap (by source) for the precision aggregates and for kappa.

Findings from the same repository/chart are not independent (52.9% of v3
findings repeat a seen key), so row-level intervals are optimistic. This
script resamples SOURCES (GitHub repositories / Helm charts) with
replacement, stratified by arm, and recomputes, per replicate:

- the population-weighted precision (per-rule precision x v3 population),
- the adjusted finding total,
- the pooled sample-row precision,

falling back to a rule's full-sample precision when a replicate contains no
decided rows for it. It also bootstraps Cohen's kappa over the 30 blinded
agreement-subset pairs (author blind label vs AI pre-label).

Usage: python3 scripts/cluster_bootstrap.py [replicates]
Writes results/cluster_bootstrap.md. Stdlib only.
"""
import csv
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
REPS = int(__import__("sys").argv[1]) if len(__import__("sys").argv) > 1 else 2000
SEED = 20261028

pre = {r["sample_id"]: r for r in csv.DictReader(open(RES / "labeling_sample_v2_prelabelled.csv"))}
div = {r["sample_id"]: r["recommended_v3"] for r in csv.DictReader(open(RES / "verification_divergence.csv"))}
v3keys = set()
pop = defaultdict(int)
for line in open(RES / "findings_v3.jsonl"):
    f = json.loads(line)
    v3keys.add((f["arm"], f["source"], f["kind"], f["name"], f["container"] or "", f["rule"]))
    pop[f["rule"]] += 1


def cluster_of(r):
    if r["arm"] == "helm":
        return "helm:" + r["source_file"].split("/")[-1].replace(".yaml", "")
    return "github:" + r["source_file"].split("/", 1)[1].split("__")[0]


rows = []  # matched, decided (TP/FP) rows: (arm, cluster, rule, is_tp)
for sid, r in pre.items():
    if (r["arm"], r["source_file"], r["kind"], r["name"], r["container"], r["rule"]) not in v3keys:
        continue
    final = div.get(sid, r["prelabel"])
    if final in ("TP", "FP"):
        rows.append((r["arm"], cluster_of(r), r["rule"], 1 if final == "TP" else 0))

full_prec = {}
for rule in pop:
    tp = sum(t for _, _, ru, t in rows if ru == rule)
    n = sum(1 for _, _, ru, _ in rows if ru == rule)
    full_prec[rule] = tp / n if n else 1.0

by_cluster = defaultdict(list)
for row in rows:
    by_cluster[(row[0], row[1])].append(row)
arms = defaultdict(list)
for (arm, cl) in by_cluster:
    arms[arm].append(cl)
print(f"decided matched rows: {len(rows)}; clusters: github={len(arms['github'])}, helm={len(arms['helm'])}")

rng = random.Random(SEED)
w_prec, adj_tot, pooled = [], [], []
for _ in range(REPS):
    sample = []
    for arm, clusters in arms.items():
        for _ in range(len(clusters)):
            sample += by_cluster[(arm, rng.choice(clusters))]
    tp = sum(t for *_, t in sample)
    pooled.append(tp / len(sample))
    adj = 0.0
    for rule, n_pop in pop.items():
        r_tp = sum(t for _, _, ru, t in sample if ru == rule)
        r_n = sum(1 for _, _, ru, _ in sample if ru == rule)
        adj += (r_tp / r_n if r_n else full_prec[rule]) * n_pop
    adj_tot.append(adj)
    w_prec.append(adj / sum(pop.values()))


def ci(xs):
    xs = sorted(xs)
    return xs[int(0.025 * len(xs))], xs[int(0.975 * len(xs))]


w_lo, w_hi = ci(w_prec)
a_lo, a_hi = ci(adj_tot)
p_lo, p_hi = ci(pooled)
point_w = sum(full_prec[r] * pop[r] for r in pop) / sum(pop.values())
point_a = sum(full_prec[r] * pop[r] for r in pop)
point_p = sum(t for *_, t in rows) / len(rows)
print(f"weighted precision: {point_w:.3f} [{w_lo:.3f}, {w_hi:.3f}]")
print(f"adjusted total: {point_a:,.0f} [{a_lo:,.0f}, {a_hi:,.0f}]")
print(f"pooled sample precision: {point_p:.3f} [{p_lo:.3f}, {p_hi:.3f}]")

# --- kappa bootstrap ---------------------------------------------------------
kap_rows = list(csv.DictReader(open(RES / "kappa_subset" / "blind_sample.csv")))
prelabels = json.load(open(RES / "prelabels.json"))
pairs = [(r["blind_label"].strip().upper(), prelabels[r["sample_id"]]["label"]) for r in kap_rows]


def kappa_of(ps):
    n = len(ps)
    agree = sum(1 for a, b in ps if a == b)
    labels = sorted({a for a, _ in ps} | {b for _, b in ps})
    from collections import Counter
    ca, cb = Counter(a for a, _ in ps), Counter(b for _, b in ps)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in labels)
    return (agree / n - pe) / (1 - pe) if pe < 1 else 1.0


k_point = kappa_of(pairs)
ks = [kappa_of([pairs[rng.randrange(len(pairs))] for _ in pairs]) for _ in range(REPS)]
k_lo, k_hi = ci(ks)
print(f"kappa: {k_point:.3f} [{k_lo:.3f}, {k_hi:.3f}]")

with open(RES / "cluster_bootstrap.md", "w") as fh:
    fh.write(f"""# Cluster bootstrap intervals (by source)

Resamples sources (GitHub repositories / Helm charts) with replacement,
stratified by arm; {REPS} replicates, seed {SEED}
(`scripts/cluster_bootstrap.py`). Decided matched rows: {len(rows)} in
{len(arms['github'])} GitHub and {len(arms['helm'])} Helm clusters. Rules with
no decided rows in a replicate fall back to their full-sample precision.

| Quantity | Point | Cluster-bootstrap 95% CI |
|---|---:|---:|
| Population-weighted precision | {point_w:.3f} | [{w_lo:.3f}, {w_hi:.3f}] |
| Adjusted finding total | {point_a:,.0f} | [{a_lo:,.0f}, {a_hi:,.0f}] |
| Pooled sample-row precision | {point_p:.3f} | [{p_lo:.3f}, {p_hi:.3f}] |
| Cohen's kappa (30-row author–AI agreement subset) | {k_point:.3f} | [{k_lo:.3f}, {k_hi:.3f}] |

Row-level (independence-assuming) intervals are narrower — e.g. weighted
precision [0.649, 0.750] by binomial variance propagation — and are
superseded by these cluster-resampled intervals, since findings within a
source are correlated (52.9% of v3 findings repeat a seen key).
""")
print("wrote results/cluster_bootstrap.md")
