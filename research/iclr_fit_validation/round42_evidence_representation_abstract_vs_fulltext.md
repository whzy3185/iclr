# Research Round 42 — Evidence Representation: Abstract vs Full Text vs Structured Cards

## 1. Trigger

The intervention is defined over scientific evidence, but the actual context representation matters. Giving entire papers, raw abstracts, titles, or extracted evidence cards can produce different behavior and different confounds.

Scientific ideation/RAG systems commonly use titles, abstracts, or summaries as flat literature context. Recent systems such as Graph2Idea explicitly identify flat titles/abstracts/summaries as the standard baseline and propose structured representations as an alternative.

The core experiment therefore needs one ecologically recognizable representation and one stronger anti-priming/mechanism representation, without mixing them into a single ambiguous treatment.

## 2. Primary ecological representation — anonymized raw abstract

Recommended primary controlled treatment representation:

```text
[Paper 1]
<original abstract text>

[Paper 2]
<original abstract text>
...
```

Remove from the prompt:

- paper title;
- author names;
- venue metadata;
- citation counts;
- explicit route labels;
- paper popularity/status indicators.

Retain the original abstract body verbatim except for deterministic normalization of whitespace/formatting.

### Why abstracts

- abstracts summarize problem, method, main findings and claimed contribution;
- abstracts are a common unit in literature retrieval/ideation systems;
- context length is manageable across many papers;
- k can be held fixed;
- relevance can be measured directly against the same text supplied to the model;
- source reputation/title cues are reduced when titles/authors are hidden;
- no additional full-text chunk-selection algorithm becomes a confound.

## 3. Why not full papers as the causal core

Whole papers introduce new treatment variables:

```text
paper length
section structure
which portions fit context
chunk selection
ordering of sections
equation/code density
citation/reference lists
appendix length
```

A full-paper RAG system would require another retrieval layer **inside each paper**, making it difficult to attribute behavior to scientific route composition rather than chunking.

Full papers also dramatically reduce the number of evidence documents that can fit under a fixed context budget.

Therefore full-text evidence is not necessary for the primary causal question.

## 4. Important wording constraint for the final paper

If the core uses abstracts, write precisely:

> `retrieved scientific paper abstracts / literature abstracts`

rather than implying that models received the complete papers.

The broad scientific evidence claim refers to real paper evidence, but experimental representation must be explicit.

## 5. Why remove titles

Titles frequently contain route-defining language:

```text
Benchmarking...
Uncovering...
Efficient...
Mechanistically Explains...
A New Method for...
```

They can also expose famous method names or the source paper's contribution type before the abstract is read.

Therefore titles are metadata for provenance/retrieval but should not appear in the primary generator context.

A secondary ecological sensitivity test can add titles back if needed, but title inclusion should not define the core effect.

## 6. Abstract length handling

Do not blindly truncate every abstract to the same token length, because truncation may preferentially remove results/conclusions.

Preferred approach:

1. match evidence pools partly on abstract token length;
2. keep complete abstracts whenever the packet fits the fixed context budget;
3. set a predeclared maximum per-paper length only for extreme outliers;
4. if truncation is required, use a deterministic source-independent rule and report frequency;
5. run sensitivity excluding truncated papers.

## 7. Packet token-budget matching

Fixed paper count `k` is not sufficient if one route has much longer abstracts.

For every packet record:

```text
k
raw token count
total packet tokens
mean per-paper tokens
route-specific token totals
```

Match/stratify A/B pools on length and require packet-level token balance within a predeclared tolerance.

Do not pad one condition with meaningless text solely to equalize exact tokens; matching actual source length is preferable.

## 8. Prompt structure

The generator should be told neutrally:

> The following are relevant prior research abstracts. Use them as background evidence when developing your proposal. You may build on, challenge, combine, or depart from them when scientifically justified.

Do **not** say:

- choose a route represented by the papers;
- diversify from the literature;
- follow the dominant method;
- find a gap specifically in the supplied papers.

The seed task remains the driver; literature is background evidence.

## 9. Source-order randomization

Randomize abstract order within each packet using stored seeds.

For primary treatment:

- route composition fixed;
- paper set fixed for a packet realization;
- order randomized across generation batches or dedicated order-control subset.

Order effects are nuisance, not part of route exposure.

## 10. Mechanism representation — standardized P/F/M/L cards

Round 23's representation becomes the principal anti-priming mechanism layer:

```text
P — scientific problem/context
F — finding/observation
M — method/intervention
L — limitation/implication
```

Core variants:

```text
PF
PFM
PFL
```

Titles, authors, future-work commands, explicit route labels and unsupported recommendations are removed.

This representation is not claimed to be more ecological. It is a controlled decomposition used to identify what information drives route movement.

## 11. Extraction model risk

If an LLM is used to produce P/F/M/L cards:

- extraction prompt/version is frozen;
- extraction is grounded to source text;
- every field stores supporting source span(s) where practical;
- human audit checks hallucination/route leakage;
- cards are constructed before scientific treatment outcomes;
- the same extraction pipeline applies to all routes.

A deterministic/manual template is preferable for the small key robustness subset if feasible.

## 12. Natural-RAG representation consistency

For the main held-out natural-RAG prediction, use the **same abstract representation** as the controlled ecological experiment:

```text
natural top-k retrieval
→ anonymized retrieved abstracts
→ free-form proposal
```

This keeps the controlled-to-natural bridge interpretable.

Do not fit controlled response on abstracts and then test natural RAG with full papers unless explicitly framed as a representation-transfer experiment.

## 13. Optional title/full-text external validity

Only if the core paper is already viable, a small appendix experiment may compare:

```text
abstract only
vs
title + abstract
vs
retrieved full-text evidence chunks
```

Question:

> Does the direction of the evidence-response law survive richer literature representations?

This is optional and must not block core execution.

## 14. Relationship to literature

Graph-structured ideation work argues that flat text can obscure cross-paper relations, while evidence-grounded systems often explicitly structure assumptions/limitations/findings.

That literature motivates our robustness layers but does not require us to propose a new representation system.

The paper remains a **behavioral causal study of evidence composition**, not a new scientific-RAG architecture.

## 15. Key anti-priming interpretation

A strong sequence would be:

```text
RAW ABSTRACT: clear A/B route response
PF: substantial response remains
PFL: limitation/framing information restores or strengthens response
PFM: method information adds some response
```

This would show that scientific observations/limitations, not merely method names, influence research choice.

A weak sequence:

```text
RAW: large
PF: near zero
PFL: near zero
PFM: large
```

would imply method imitation/priming and substantially weaken the scientific story.

## 16. Decision

**PRIMARY EVIDENCE REPRESENTATION = ANONYMIZED COMPLETE ABSTRACTS.**

**MECHANISM REPRESENTATION = AUDITED P/F/M/L CARDS.**

Full-text context is optional later external validity, not part of the causal core.