# Research Round 44 — Pairwise Matched Evidence-Slot Design

## 1. Trigger

Prior rounds require A/B evidence pools to be relevance-matched, but a packet-level balance criterion can still allow hidden differences:

```text
A packet has a few extremely relevant papers + weaker papers
B packet has uniformly medium-relevant papers
```

or route A may systematically contain newer/longer/more seed-specific papers.

A cleaner treatment construction is to create **matched A/B evidence slots** before packet generation.

## 2. Core idea

For one source-valid `seed × route-pair` block, construct matched pairs:

```text
slot 1:  A paper a1  ↔  B paper b1
slot 2:  A paper a2  ↔  B paper b2
...
slot J:  A paper aJ  ↔  B paper bJ
```

Within each slot, A/B papers are as similar as possible on non-route covariates while differing in the scientific route they represent.

An evidence packet then chooses **one member from each selected slot**.

This creates a natural paired/stratified randomization structure.

## 3. Matching variables

Use only pre-treatment/source variables:

### Primary

```text
reranker relevance to seed
dense relevance to seed
abstract token length
first-public date / time distance
topic/subfield embedding or cluster
```

### Optional if consistently available and frozen

```text
citation/popularity at a frozen date
paper type / theoretical-vs-empirical coarse flag
coarse Artifact/Knowledge family
```

Do not match on variables derived from model-generated proposals.

## 4. Matching cost

For candidate A paper `a` and B paper `b`, define a standardized pre-treatment cost such as:

```text
cost(a,b)
 = w1 * |z_rerank(a)-z_rerank(b)|
 + w2 * |z_dense(a)-z_dense(b)|
 + w3 * |z_length(a)-z_length(b)|
 + w4 * |z_date(a)-z_date(b)|
 + w5 * topic_distance(a,b)
```

Weights/rules are selected using source-only diagnostics and frozen before model outcomes.

Do not tune weights to increase a future treatment effect.

## 5. Bipartite matching

For each seed-route pair:

1. apply frozen relevance floor to A/B candidate papers;
2. construct pairwise match-cost matrix;
3. impose hard calipers for unacceptable relevance/topic mismatches;
4. solve a deterministic minimum-cost bipartite matching or nearest-neighbor matching without replacement;
5. retain all matched and unmatched candidates with status/reason.

Possible algorithms:

- Hungarian/min-cost assignment;
- optimal matching;
- greedy nearest neighbor with frozen tie-break rule.

Prefer the simplest deterministic method that achieves transparent balance.

## 6. Matched-slot bank

Do not stop at exactly `k` pairs if more evidence exists.

For a block, construct a bank:

```text
J >= k
```

matched A/B slots.

Example:

```text
J = 16 matched slots
packet k = 8
```

A packet realization samples 8 slots from the bank and selects A/B members according to alpha.

Advantages:

- multiple packet realizations;
- document-identity variance estimation;
- treatment compositions inherit local matching;
- not all evidence is reused in every context.

Exact `J` is determined by source feasibility, not post-outcome choice.

## 7. Treatment construction from slots

For selected `k=8` slots:

```text
alpha=0.00: choose B from all 8 slots
alpha=0.25: choose A from 2 slots, B from 6
alpha=0.50: choose A from 4 slots, B from 4
alpha=0.75: choose A from 6 slots, B from 2
alpha=1.00: choose A from all 8 slots
```

Within middle alpha levels, which slots receive A vs B is randomized using stored seeds and balanced across packet realizations.

Do not always place the highest-relevance A paper in mixed packets.

## 8. Strong paired design property

For the endpoint contrast using the same selected slots:

```text
alpha=0 packet = {b1,b2,...,bk}
alpha=1 packet = {a1,a2,...,ak}
```

Every A paper replaces a specific matched B paper.

This makes the causal contrast much easier to explain:

> The evidence set changes route while approximately preserving relevance/topic/length at every matched slot.

## 9. Middle-mixture factorial interpretation

Each slot can be viewed as a binary route assignment:

```text
Z_j ∈ {A,B}
```

The five alpha levels constrain the number of A assignments.

This provides a randomized combinatorial design without requiring every possible `2^k` packet.

It also enables future local document-replacement analysis naturally.

## 10. Packet realizations

A packet realization is defined by:

```text
slot subset
A/B assignment vector
paper order
```

Store all three in packet manifest.

Suggested confirmatory philosophy:

```text
multiple slot subsets
×
multiple balanced assignment vectors
×
limited generation repeats
```

rather than one canonical packet with many generations.

## 11. Balance diagnostics

Before treatment generation, report:

### Slot level

- distribution of |A-B reranker relevance|;
- dense relevance difference;
- token-length difference;
- date difference;
- topic distance.

### Pool level

- standardized mean differences A vs B;
- overlap plots/histograms;
- number of unmatched candidates;
- route-specific exclusion rates.

### Packet level

Simulate/freeze packet manifests and verify balance across alpha levels before model outcomes.

## 12. Caliper failure is informative

If a seed cannot form enough matched slots without relaxing relevance/topic calipers:

```text
RELEVANCE_MATCH_FAIL
```

or

```text
INSUFFICIENT_MATCHED_SLOTS
```

Do not weaken the caliper solely to preserve sample size.

This is exactly what F0 feasibility is supposed to discover.

## 13. Relation to scientific equipoise

Matched slots solve document-level comparability, not route-level scientific validity.

A block still requires human/source-only equipoise:

```text
both routes plausible
both directly address seed
neither obviously dominates
routes distinguishable/non-subsumed
```

Both gates are necessary.

## 14. Relation to lexical priming

Slot matching does not remove route-specific language—route-specific content is the treatment.

Round 23/42 P/F/M/L normalization is still needed to test whether the response reflects scientific findings/limitations vs explicit method/route words.

## 15. Natural RAG mapping

Natural top-k packets do not use matched slots.

Instead, the controlled slot design estimates the response law cleanly. Natural retrieval is then projected onto A/B composition and evaluated out-of-sample.

This preserves the distinction:

```text
controlled identification
vs
natural external validation
```

## 16. Implementation implication for Codex F0

Source feasibility should preferably report not just:

```text
n_A, n_B above relevance floor
```

but:

```text
maximum number of matched A/B slots under frozen calipers
median/quantile match cost
matched-slot bank size
```

for each seed-route pair and k target.

This may require a future source-only amendment/implementation update, but does not authorize generation.

## 17. Strong figure for methods appendix/main schematic

```text
Seed question
   |
   +-- slot 1: A1 ↔ B1
   +-- slot 2: A2 ↔ B2
   +-- slot 3: A3 ↔ B3
   ...

alpha=.25 packet:
A1, B2, B3, ...

alpha=.75 packet:
A1, A2, A3, ..., B8
```

The visual immediately communicates that route—not paper quality/relevance—is the manipulated dimension.

## 18. Decision

**PREFERRED TREATMENT CONSTRUCTION = PAIRWISE MATCHED EVIDENCE SLOTS.**

If source feasibility can support enough matched slots, this should replace looser packet-level matching in the confirmatory experiment because it gives a cleaner causal story and naturally supports packet replication/document-replacement controls.