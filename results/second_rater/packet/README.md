# Independent labeling packet — Kubernetes misconfiguration study

Thank you for doing this. This study measures how common various Kubernetes
misconfigurations are in public manifests, and — critically — how often an
automated checker's findings are actually correct. The findings were labeled
once already; your task is to label a sample of them **independently**, under
the same written protocol, so the study can report genuine inter-rater
reliability (agreement between two people, not just one person's
consistency). Your labels are compared against the existing ones only after
you return them.

## Contents

- `protocol_for_rater.md` — the complete labeling standard. Every decision
  rule you need is in it.
- `blind_sample.csv` — the 150 rows to label, in two batches: **Batch A
  (100 rows)** and **Batch B (50 rows)**. Please complete Batch A first; it
  is a self-contained measurement on its own.
- `packets.md` — one evidence packet per row, in the same order as the CSV
  (`packets.jsonl` is the same content in machine-readable form).
- `mapping_audit.md` — an optional, shorter second task (see below).

## How to label

1. Read `protocol_for_rater.md` first (~10 minutes).
2. For each row: find its packet, apply the protocol's test for that rule,
   and fill in three columns of `blind_sample.csv`:
   - `blind_label`: `TP`, `FP`, `TP-hardening`, or `unsure`
   - `blind_reason`: for FPs, the reason code from the protocol
     (`infra-need`, `placeholder`, `fixture`, `standard-practice`,
     `parser-artifact`, `not-exploitable`); leave blank otherwise
   - `blind_notes`: anything that made the row hard, in a few words
3. Work from the packet and the protocol alone. The packet is designed to
   contain everything the judgment needs; if a row still can't be decided,
   mark it `unsure` rather than guessing.
4. Budget: most rows take 1–2 minutes. Batch A is roughly 2–3 hours total;
   feel free to split it across sittings.

Two requests that keep the measurement valid:

- **Don't look for prior labels.** None are included in this packet, and
  please don't go looking for the study's other materials — a label formed
  after seeing someone else's answer isn't independent anymore.
- **Questions about the protocol are welcome; questions about specific rows
  should wait** until after you've returned the sheet, so your judgment on
  each row stays your own.

When you're done, return the filled `blind_sample.csv` (Batch A alone is
fine if that's what time allows — just say so). You will get the comparison
results, including every row where the two label sets disagree, once they're
scored.

## Optional second task: scanner-mapping audit (~30 minutes)

`mapping_audit.md` lists how the study mapped four popular scanners'
checks onto its 25 rules, with the judgment calls flagged. If you know these
tools (kube-linter, kubeaudit, Polaris, Checkov), marking agree/disagree on
the flagged calls would independently validate the study's scanner
comparison. Entirely optional, and it can be returned separately.
