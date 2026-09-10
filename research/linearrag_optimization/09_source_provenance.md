# Source provenance

## Primary paper

```text
Title: LinearRAG: Linear Graph Retrieval Augmented Generation on Large-scale Corpora
Venue label in PDF: Published as a conference paper at ICLR 2026
Pages: 23
Primary reading scope: pages 1–10
Appendix selectively read: pages 17–22 for efficiency, retrieval quality, hyperparameters, case study, FAQ
Local PDF SHA256: 433abc166fa2ae1712d6e6df9e20e82bd20afca619ff7c0ce7c80b35e56f9e4e
```

The analysis documents distinguish direct paper claims from implementation audit and new hypotheses.

## Upstream implementation inspected

```text
Repository: DEEP-PolyU/LinearRAG
Default branch: main
Observed HEAD during audit: bcc94e66c221f798801255efba09311d6fbcd8d6
Audit date: 2026-09-10
```

Files inspected:

```text
src/LinearRAG.py
src/config.py
src/ner.py
src/embedding_store.py
scripts/run.sh
run.py
```

Open-discussion material inspected:

```text
Issue #25: Reproducibility concerns
Issue #26: vector/matrix retrieval parameter/performance mismatch on MuSiQue
```

Important: issue reports are community observations, not automatically accepted facts. Where an author/collaborator response exists, the research notes preserve that response as part of the context.

## Experiment provenance

The code in `experiments/linearrag_optimization` was written independently for this branch from the mathematical description and audit observations. It does not copy the upstream implementation.

Current prototype outputs are generated from synthetic graphs and CPU microbenchmarks only. They must not be mixed into a real benchmark result table.
