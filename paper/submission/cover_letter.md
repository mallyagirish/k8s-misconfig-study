# Cover letter — EMSE submission (DRAFT for Girish's review)

Dear Editors,

I submit the manuscript "Misconfigured by Default: The Prevalence, Validity,
and Tool Coverage of Kubernetes Misconfigurations in the Wild" for
consideration as a Research Paper in *Empirical Software Engineering*.

The paper measures how Kubernetes manifests in the wild — 151 rendered Helm
charts and 60 public GitHub repositories — are actually configured across 25
security, resource, image, and reliability practices, and it validates its
own measurement: the findings of a 25-rule detection engine are checked
against a 457-finding stratified sample labeled under a documented protocol,
with a blinded agreement measurement and cluster-bootstrap uncertainty,
yielding per-rule precision and a taxonomy that separates genuine
misconfigurations from benign-by-design cases. The paper then scores four
widely used manifest scanners against those verified labels.

I believe the paper fits the journal's scope and readership. It is an
empirical measurement study with a fully public replication package (corpus
sources pinned by commit SHA and chart version; the engine, labeling
protocol, validation sample, and analysis scripts are all released), and it
extends the line of work the journal published in Minna et al. (2025) on Helm
chart misconfigurations — adding validated per-rule precision on natural
corpora, a production/fixture separation, and a per-tool accuracy analysis.

The manuscript is original, has not been published previously, and is not
under consideration elsewhere. I am the sole author; there are no competing
interests and no funding to declare. The replication package will be archived
with a Zenodo DOI at submission, and a preprint will be posted to arXiv.

Thank you for your consideration.

Girish Mallya
Independent Researcher, Bellevue, WA, USA
girishm60@gmail.com
