# P0 Pilot — Shared-Retrieval Research Monoculture

> Status: **READY FOR CODEX IMPLEMENTATION**  
> Decision owner: research/round3_assumption_breaking_analysis.md  
> Purpose: 24–48h falsifiable pilot. This directory is not a paper implementation yet.

## 1. Scientific question

Do literature-grounded scientific ideation pipelines create **population-level research monoculture** because independent runs retrieve highly overlapping evidence neighborhoods?

We are not testing the already-known broad claim that “LLM outputs can be homogeneous.”

The pilot tests a narrower causal mechanism:

```text
shared corpus
    ↓
relevance-ranked retrieval
    ↓
source exposure overlap
    ↓
problem/method framing overlap
    ↓
research idea collision
```

Primary pilot goal: isolate the `retrieval → idea` arrow.

Do **not** implement judge/refinement agents until the retrieval-stage signal passes the hard gate.

---

## 2. Pre-registered pilot hypotheses

### H1 — Retrieval concentration

For the same research-area prompt and corpus, independent `top-k relevance` runs expose the generator to a more concentrated paper set than diversity-aware retrieval.

Expected direction:

```text
source_overlap(topk) > source_overlap(diversified)
source_coverage(topk) < source_coverage(diversified)
```

### H2 — Causal idea concentration

Manipulating source exposure overlap changes downstream research-question / method overlap.

Expected direction:

```text
idea_collision(topk) > idea_collision(diversified)
idea_diversity(topk) < idea_diversity(diversified)
```

### H3 — Quality is not identical to diversity

A diversity-aware retrieval intervention can increase portfolio diversity without collapsing feasibility / technical depth.

This is secondary in the pilot; quality must nevertheless be recorded because “more random output” is not a scientific win.

---

## 3. Domains

Use three ICLR-relevant areas with different literature structures so that a result is not an artifact of one subfield:

1. **Model editing / knowledge updating**
2. **LLM agents / tool-use evaluation**
3. **Post-training / optimization dynamics**

For the pilot, build a frozen corpus from ICLR 2024–2026 paper titles + abstracts + metadata.

### Corpus inclusion

For each area:

- target: 200–500 papers after topic filtering;
- fields: `paper_id, year, title, abstract, keywords, openreview_url`;
- freeze one corpus snapshot before generation;
- compute and save SHA256 of the source table;
- never silently add newly discovered papers mid-run.

If one area has fewer than ~150 reasonably matched papers, broaden its query taxonomy rather than padding with unrelated papers.

---

## 4. Experimental conditions

Run the same base research-idea prompt under three required conditions.

### C0 — topic_only_no_retrieval

Generator sees only:

- research area;
- identical task instruction;
- no retrieved paper abstracts.

Purpose: estimate generator prior / intrinsic convergence.

### C1 — topk_relevance

Use a standard relevance retriever.

Pilot default:

- dense embeddings;
- cosine similarity;
- fixed `k = 12`;
- identical query-construction function across runs.

If the query is deterministic and therefore every run receives exactly the same sources, that is useful evidence about shared-exposure concentration, but add one controlled query-paraphrase seed so we can separate “identical query” from “relevance ranking” effects.

### C2 — diversified_retrieval

Use the same candidate pool and embedding model, but impose diversity.

Pilot default: **MMR**.

Also support one stronger controlled variant if trivial to implement:

```text
disjoint_neighborhood
```

where independent seeds are assigned low-overlap source neighborhoods subject to a relevance floor.

Do not optimize MMR hyperparameters using final idea-diversity results.

---

## 5. Generation design

### Minimum scale

```text
3 domains
× 3 retrieval conditions
× 2 model families
× 30 independent runs
= 540 generated ideas
```

If API/cost constraints require staging, run 10 seeds first only as a smoke test; **do not make a scientific decision from the smoke test**.

### Model requirements

- at least 2 distinct model families;
- pin exact model/version string;
- temperature/top-p/max tokens identical across retrieval conditions within each family;
- preserve raw model response;
- do not use the same LLM to rewrite all ideas into a common style before diversity measurement.

### Base generation task

Each run must return structured fields:

```json
{
  "research_question": "...",
  "claimed_gap": "...",
  "method_sketch": "...",
  "key_experiment": "...",
  "why_nontrivial": "..."
}
```

The system prompt must explicitly ask for **one** best idea, not a list, to avoid within-run list diversity confounding population diversity.

---

## 6. Trace schema

Save one JSONL row per generation:

```json
{
  "run_id": "...",
  "timestamp": "...",
  "domain": "model_editing",
  "condition": "topk_relevance",
  "seed": 17,
  "model_provider": "...",
  "model_version": "...",
  "temperature": 0.7,
  "prompt_sha256": "...",
  "corpus_sha256": "...",
  "retrieval_query": "...",
  "retriever_name": "...",
  "retriever_version": "...",
  "retrieved": [
    {"paper_id": "...", "rank": 1, "score": 0.82}
  ],
  "raw_response": "...",
  "research_question": "...",
  "claimed_gap": "...",
  "method_sketch": "...",
  "key_experiment": "...",
  "why_nontrivial": "..."
}
```

No run may be discarded because the idea “looks bad.” Parse failures should be retained and marked.

---

## 7. Primary measurements

The pilot must not stand on one embedding metric.

### 7.1 Retrieval exposure

Report at minimum:

- pairwise Jaccard overlap of retrieved paper IDs;
- weighted overlap using retrieval ranks/scores;
- unique-source coverage across N runs;
- source-frequency HHI;
- source-frequency Gini.

### 7.2 Idea diversity

Report at minimum two non-equivalent families:

**Semantic**

- pairwise embedding cosine distance on `research_question`;
- pairwise distance on concatenated `research_question + method_sketch`;
- cluster entropy / effective number of clusters.

**Structural**

Extract a normalized tuple:

```text
(problem object, failure/assumption, intervention/method, evaluation target)
```

Then calculate:

- exact tuple collision;
- partial-field collision;
- nearest-neighbor collision under a pre-specified tuple similarity rule.

Tuple extraction can use an LLM as a parser, but the parser output is not treated as ground truth. Save parser model/version and manually audit a stratified subset later if the pilot passes.

### 7.3 Portfolio growth

Plot diversity as the number of sampled ideas increases:

```text
N = 5, 10, 20, 30, ...
```

This is important because homogenization is a population property; a single pairwise comparison is insufficient.

---

## 8. Quality control measurement

For the pilot, use a deliberately weak claim:

> diversified retrieval should not produce an obvious quality collapse.

Record:

- feasibility;
- technical depth;
- literature grounding;
- specificity of falsifiable experiment.

Use cross-family judging if available; never let `generator == sole quality judge` become the only evidence.

If the pilot proceeds to a paper, add blinded human annotation.

---

## 9. Statistical plan

Primary comparison:

```text
C1 topk_relevance vs C2 diversified_retrieval
```

within each `domain × generator_family` stratum.

Report:

- mean/median difference;
- bootstrap 95% CI;
- standardized effect size where meaningful;
- pooled mixed-effects / hierarchical estimate only after per-domain plots exist.

Do not report only p-values.

For portfolio metrics, bootstrap at the **run** level, not at the pairwise-distance row level, to avoid pseudo-replication from O(n²) pairs.

### Causal mediation extension

Only if H1/H2 pass:

Test whether source-overlap manipulation explains idea-overlap changes using a randomized exposure design or controlled disjoint-source assignment. Do not label ordinary correlation as mediation causality.

---

## 10. Mandatory controls

At pilot stage:

- same corpus snapshot;
- same generator settings across retrieval conditions;
- same prompt except injected evidence;
- prompt paraphrase robustness on a subset;
- retrieval `k` fixed;
- document count / token budget matched between C1 and C2;
- identical relevance floor when comparing top-k and diversified retrieval where possible.

Potential full-paper controls if the pilot survives:

- BM25 vs dense retrieval;
- multiple `k` values;
- multiple embedding models;
- high-temperature generation;
- persona prompting;
- multi-model generation;
- random-relevant retrieval;
- fixed candidate pool + random vs LLM selection;
- same-family vs cross-family generator/judge.

---

## 11. Hard kill criteria

**Stop this topic** if any of the following survives basic debugging:

1. diversified retrieval changes wording but not problem/method-level diversity;
2. controlled changes to source overlap do not produce stable changes in idea overlap;
3. the effect exists only for one embedding representation;
4. ordinary prompt paraphrases erase the effect;
5. increased diversity is mostly malformed / infeasible ideas;
6. a fresh 30–60 day collision scan finds a paper already performing essentially the same literature-grounded stage-wise causal decomposition.

Do not rescue a failed pilot by adding more agent modules.

---

## 12. Continue gate

Escalate to a full paper only if **at least 3** of the following are true:

- >=2 model families reproduce the top-k concentration effect;
- >=2 non-equivalent diversity measurements agree;
- effect holds in >=2 of 3 domains, ideally all 3;
- controlled source-overlap intervention changes idea collision in the predicted direction;
- a simple diversity-aware retrieval intervention preserves most quality;
- the central result can be expressed in one sentence without referring to a bespoke metric.

Preferred main claim if supported:

> Relevance-optimized literature retrieval improves or preserves individual idea quality while systematically reducing portfolio-level scientific diversity through concentrated evidence exposure.

This sentence is **not** a conclusion until supported by experiments.

---

## 13. Required outputs from Codex

Codex should produce exactly these first:

```text
experiments/idea_collapse/
├── configs/
│   ├── pilot.yaml
│   └── prompts/
├── corpus/
│   ├── build_corpus.py
│   └── topic_filters.yaml
├── retrieval/
│   ├── dense.py
│   ├── mmr.py
│   └── assign_disjoint.py
├── generation/
│   ├── schema.py
│   └── run.py
├── metrics/
│   ├── retrieval_overlap.py
│   ├── semantic_diversity.py
│   ├── tuple_collision.py
│   └── portfolio_growth.py
├── analysis/
│   ├── pilot_analysis.py
│   └── bootstrap.py
├── runs/.gitkeep
└── results/.gitkeep
```

Minimum executable commands should converge to something like:

```bash
python corpus/build_corpus.py --config configs/pilot.yaml
python generation/run.py --config configs/pilot.yaml
python analysis/pilot_analysis.py --config configs/pilot.yaml
```

Exact CLI design is left to Codex, but one config must reproduce the whole pilot.

---

## 14. Reproducibility rules

Every result figure/table must be traceable to:

```text
Git commit
corpus hash
prompt hash
model version
retriever version
seed/run_id
analysis config
```

No manually edited CSV should sit between generation and final analysis without a transformation script.

Record negative results. Do not delete conditions that contradict H1/H2.

---

## 15. What Codex should NOT do yet

- no new agent framework;
- no large UI/dashboard;
- no paper LaTeX;
- no new custom diversity metric unless existing measures demonstrably fail;
- no expensive human study before a machine-measurable main effect exists;
- no hyperparameter search aimed at maximizing the preferred story;
- no claiming causality from observational source-overlap correlations.

The next decision is binary: **kill or continue** based on the pilot.
