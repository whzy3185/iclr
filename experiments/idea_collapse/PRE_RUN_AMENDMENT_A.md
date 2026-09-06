# Pre-Run Amendment A — Matched-Relevance Exposure Control

> Date: 2026-09-06  
> Status: **applies before any scientific generation run**  
> Reason: web-side collision scan identified a critical confound in binary `top-k vs MMR` comparisons.  
> Evidence source: `research/round4_web_experiment_design.md`

## Scope

This amendment does **not** change the P0 hypothesis, primary domains, required model families, trace schema, or hard kill/continue rule.

It adds one methodological requirement:

> Any claim that retrieval diversity / exposure overlap changes scientific idea diversity must distinguish **exposure diversity** from simply giving the model less relevant or differently distributed literature.

## Required logging for all retrieval conditions

For every retrieved source set, save:

- mean, median and per-item retrieval score;
- publication year;
- context token count;
- source/paper ID;
- cluster/topic ID if available;
- citation/popularity proxy if available without major engineering overhead.

Analysis must report whether retrieval conditions differ substantially on these marginals.

## Required controlled-overlap experiment if E0 shows a signal

Do not treat `top-k vs MMR` as sufficient causal evidence.

If the E0 baseline shows a meaningful problem/method-level difference, the next experiment must manipulate shared source exposure directly while approximately matching relevance.

### Treatment

Within a fixed relevance band (recommended initial pool: top 60 candidates), construct `k=12` source sets with assigned overlap:

```text
0%, 25%, 50%, 75%, 100%
```

Operationally:

```text
shared_count = 0, 3, 6, 9, 12
```

Replacement/unique sources should be sampled from the same relevance-score stratum as the shared source they replace, with year matching when feasible.

### Fixed factors

Hold constant within comparison:

- model/version;
- system/user prompt;
- k;
- context token budget;
- generation settings;
- topic/query;
- corpus snapshot.

### Primary outcome

The scientific conclusion must rely on problem/method-level structure, not only text embeddings.

At minimum:

- structured tuple collision;
- semantic diversity;
- effective number of idea clusters / cluster entropy.

### Gate

If assigned source-overlap changes realized exposure overlap but fails to produce a consistent change in problem/method-level idea diversity across multiple models/domains, **do not claim retrieval-induced monoculture**.

## MUSES follow-up

The MUSES/CiteRoots author-endorsed root-injection experiment described in `research/round4_web_experiment_design.md` is **not part of the first pilot** and must not block Task 0–4.

It becomes a follow-up only after the original pilot and controlled-overlap mechanism show a meaningful signal.

## Research discipline

This amendment was added before any scientific result was observed in this repository. It must remain committed as part of the preregistration history.