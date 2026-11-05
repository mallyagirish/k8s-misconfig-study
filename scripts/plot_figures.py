#!/usr/bin/env python3
"""Generate the manuscript's three figures from the results data.

Figure 1 (Section 4.1): workload-level prevalence of default-posture
    practices, Helm arm vs production-tagged GitHub arm
    (results/stats_tagged_v3.json).
Figure 2 (Section 4.3): per-rule precision forest plot against the
    reference labels (table in results/precision_provisional.md,
    post-self-audit labels).
Figure 3 (Section 4.4): scanner accuracy against the Helm-arm reference
    labels, recomputed from results/tool_accuracy.csv.

Every plotted value is asserted against the numbers printed in the
manuscript (Table 1, Table 2 / precision_provisional.md, and the
Section 4.4 accuracy table) before anything is drawn; the script stops
rather than plot a number the paper does not report.

Outputs: paper/figures/fig{1,2,3}_*.pdf (for LaTeX) and .png (for the
Markdown draft). Run from the repository root:

    python3 scripts/plot_figures.py
"""
import csv
import json
import re
from math import sqrt
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

DARK = "#262626"
LIGHT = "#bdbdbd"
ACCENT = "#4e6e8e"  # the single muted accent, used once per figure at most

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 8.5,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 0.6,
})


def wilson(k, n, z=1.96):
    """Wilson score interval; returns (p, lo, hi)."""
    if n == 0:
        raise ValueError("wilson with n=0")
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return p, (c - m) / d, (c + m) / d


def r2(x):
    return round(x + 1e-12, 2)


# ---------------------------------------------------------------- Figure 1
def figure_prevalence():
    stats = json.loads((ROOT / "results/stats_tagged_v3.json").read_text())
    helm, gh = stats["helm"]["rules"], stats["github_production"]["rules"]

    # (rule, label) — the default-posture practices Section 4.1 leads with,
    # plus the resource/security-context defaults of the same kind, and the
    # explicit opt-in (privileged) as the contrast row.
    rules = [
        ("IMG_NO_DIGEST", "Image not digest-pinned"),
        ("SA_TOKEN_AUTOMOUNTED", "SA token automounted"),
        ("RES_NO_CPU_LIMIT", "No CPU limit"),
        ("RES_NO_MEM_LIMIT", "No memory limit"),
        ("RES_NO_REQUESTS", "No resource requests"),
        ("SEC_NO_SECCOMP", "No seccomp profile"),
        ("SEC_APE_NOT_DISABLED", "Privilege escalation not disabled"),
        ("SEC_PRIVILEGED", "Privileged container"),
    ]
    # Hard gate: Table 1 of the manuscript.
    table1 = {
        "IMG_NO_DIGEST": (97.5, 65.3),
        "SA_TOKEN_AUTOMOUNTED": (85.1, 88.6),
        "RES_NO_CPU_LIMIT": (85.6, 75.3),
        "SEC_PRIVILEGED": (5.5, 1.4),
    }
    vals = []
    for rule, _label in rules:
        h = helm[rule]["pct_workloads"]
        g = gh[rule]["pct_workloads"]
        if rule in table1:
            assert (round(h, 1), round(g, 1)) == table1[rule], (
                f"Table 1 mismatch for {rule}: data ({h}, {g}) vs "
                f"manuscript {table1[rule]}")
        vals.append((h, g))
    print("Figure 1: Table 1 values reproduced from stats_tagged_v3.json")

    labels = [lbl for _r, lbl in rules][::-1]
    hv = [v[0] for v in vals][::-1]
    gv = [v[1] for v in vals][::-1]
    y = range(len(rules))
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    ax.barh([i + 0.19 for i in y], hv, height=0.36, color=DARK,
            label="Helm charts")
    ax.barh([i - 0.19 for i in y], gv, height=0.36, color=LIGHT,
            edgecolor="#444444", linewidth=0.5,
            label="GitHub (production)")
    for i, (h, g) in enumerate(zip(hv, gv)):
        ax.text(h + 1.5, i + 0.19, f"{h:.0f}", va="center", fontsize=7.5)
        ax.text(g + 1.5, i - 0.19, f"{g:.0f}", va="center", fontsize=7.5)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.set_xlim(0, 108)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_xlabel("Workloads with at least one finding")
    ax.legend(loc="lower right", frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout()
    fig.savefig(OUT / "fig1_prevalence.pdf")
    fig.savefig(OUT / "fig1_prevalence.png", dpi=300)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 2
def figure_precision_forest():
    text = (ROOT / "results/precision_provisional.md").read_text()
    rows = {}
    pat = re.compile(
        r"^\| ([A-Z_]+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| "
        r"([\d.]+) \| \[([\d.]+), ([\d.]+)\] \|", re.M)
    for m in pat.finditer(text):
        rule, tp, fp, hard, _excl = m.group(1), *map(int, m.groups()[1:5])
        prec, lo, hi = map(float, m.groups()[5:8])
        p, wlo, whi = wilson(tp, tp + fp)
        # Hard gate: recomputed values must match the printed table.
        # The printed table gives precision to 3 dp and CIs to 2 dp;
        # agreement within half a unit of the last printed place.
        assert abs(p - prec) <= 0.0005 + 1e-9 \
            and abs(wlo - lo) <= 0.005 + 1e-9 \
            and abs(whi - hi) <= 0.005 + 1e-9, (
            f"precision table mismatch for {rule}: recomputed "
            f"{p:.3f} [{wlo:.3f}, {whi:.3f}] vs printed "
            f"{prec} [{lo}, {hi}]")
        rows[rule] = (tp, fp, hard, p, wlo, whi)
    assert len(rows) == 25, f"expected 25 rules, parsed {len(rows)}"
    assert sum(v[0] for v in rows.values()) == 275, "total TP != 275"
    assert sum(v[1] for v in rows.values()) == 166, "total FP != 166"
    print("Figure 2: all 25 per-rule precisions + CIs reproduced; "
          "totals 275 TP / 166 FP")

    order = sorted(rows.items(), key=lambda kv: (-kv[1][3], -kv[1][4],
                                                 -(kv[1][0] + kv[1][1])))
    fig, ax = plt.subplots(figsize=(5.2, 6.6))
    for i, (rule, (tp, fp, _hard, p, lo, hi)) in enumerate(order):
        yy = len(order) - 1 - i
        ax.plot([lo, hi], [yy, yy], color="#888888", lw=1.1, zorder=2)
        ax.plot([p], [yy], marker="o", ms=4.2, color=DARK, zorder=3)
        ax.text(1.045, yy, f"{tp}/{fp}", va="center", fontsize=7,
                color="#444444")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([r for r, _v in order][::-1], family="monospace",
                       fontsize=7.6)
    ax.axvline(0.5, color="#cccccc", lw=0.7, zorder=1)
    ax.set_xlim(0, 1.16)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.50", "0.75", "1.00"])
    ax.set_xlabel("Precision against the reference labels (Wilson 95% CI)")
    ax.text(1.045, len(order) - 0.15, "TP/FP", fontsize=7, color="#444444",
            va="bottom")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_precision_forest.pdf")
    fig.savefig(OUT / "fig2_precision_forest.png", dpi=300)
    plt.close(fig)


# ---------------------------------------------------------------- Figure 3
def figure_scanners():
    rows = list(csv.DictReader((ROOT / "results/tool_accuracy.csv")
                                .open()))
    tools = ["kube-linter", "kubeaudit", "Polaris", "Checkov"]
    # Hard gate: Section 4.4's accuracy table (rate, CI lo, CI hi).
    expected = {
        "kube-linter": {"cond": (0.90, 0.77, 0.96), "eff": 0.51,
                        "benign": (0.92, 0.80, 0.97)},
        "kubeaudit": {"cond": (0.98, 0.87, 1.00), "eff": 0.55,
                      "benign": (0.95, 0.83, 0.99)},
        "Polaris": {"cond": (0.93, 0.83, 0.97), "eff": 0.72,
                    "benign": (0.88, 0.72, 0.95)},
        "Checkov": {"cond": (0.77, 0.66, 0.86), "eff": 0.66,
                    "benign": (0.84, 0.71, 0.91)},
    }
    data = {}
    for tool in tools:
        tr = [r for r in rows if r["tool"] == tool]
        tp = [r for r in tr if r["final_label"] == "TP"]
        fp = [r for r in tr if r["final_label"] == "FP"]
        tpc = [r for r in tp if r["check_exists"] == "yes"
               and r["classification"] != "AMBIGUOUS_JOIN"]
        tpd = [r for r in tp if r["classification"] != "AMBIGUOUS_JOIN"]
        fpc = [r for r in fp if r["check_exists"] == "yes"
               and r["classification"] != "AMBIGUOUS_JOIN"]
        cond = wilson(sum(r["classification"] == "DETECTED" for r in tpc),
                      len(tpc))
        eff = wilson(sum(r["classification"] == "DETECTED" for r in tpd),
                     len(tpd))
        ben = wilson(sum(r["classification"] == "DETECTED" for r in fpc),
                     len(fpc))
        e = expected[tool]
        assert (r2(cond[0]), r2(cond[1]), r2(cond[2])) == e["cond"], (
            f"{tool} conditional mismatch: {cond} vs {e['cond']}")
        assert r2(eff[0]) == e["eff"], f"{tool} effective mismatch"
        assert (r2(ben[0]), r2(ben[1]), r2(ben[2])) == e["benign"], (
            f"{tool} benign mismatch: {ben} vs {e['benign']}")
        data[tool] = (cond, eff, ben)
    print("Figure 3: all scanner rates + CIs reproduced from "
          "tool_accuracy.csv")

    labels = ["Conditional\n(check exists)", "Effective\n(all practices)",
              "Benign findings\nflagged"]
    colors = [DARK, ACCENT, LIGHT]
    x = range(len(tools))
    w = 0.26
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    for j in range(3):
        xs = [i + (j - 1) * w for i in x]
        vs = [data[t][j] for t in tools]
        ax.bar(xs, [v[0] for v in vs], width=w, color=colors[j],
               edgecolor="#444444" if j == 2 else "none",
               linewidth=0.5, label=labels[j].replace("\n", " "))
        ax.errorbar(xs, [v[0] for v in vs],
                    yerr=[[v[0] - v[1] for v in vs],
                          [v[2] - v[0] for v in vs]],
                    fmt="none", ecolor="#333333", elinewidth=0.8,
                    capsize=2)
    ax.set_xticks(list(x))
    ax.set_xticklabels(tools)
    ax.set_ylim(0, 1.12)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_ylabel("Share of sampled findings")
    ax.legend(loc="upper left", frameon=False, ncols=1,
              bbox_to_anchor=(0.0, 1.14), handlelength=1.2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout()
    fig.savefig(OUT / "fig3_scanners.pdf")
    fig.savefig(OUT / "fig3_scanners.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    figure_prevalence()
    figure_precision_forest()
    figure_scanners()
    print("figures written to", OUT)
