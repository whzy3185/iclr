# Research Round 53 — F0 Experimental Conclusion

Date: 2026-09-08

## Executive conclusion

The completed recovery run does not test the scientific hypothesis about LLM research-route steering. It establishes a narrower but important source-space result:

> The ICLR 2025/2026 literature contains a large provisional multi-route candidate space, and the source-matching problem is computationally tractable, but current evidence is still insufficient to certify scientifically valid matched treatment blocks because semantic relevance, temporal cleanliness, route purity/equipoise, and human construct validity remain unresolved.

Decision: **KEEP the research question. Do not interpret F0 as evidence for or against H1/H2/H3. Finish source/construct validation before any ARS or proposal-generation pilot.**

## What is measured

From the recovery branch `codex/f0-recovery-20260908`, commit `5baa860fddbdd083d945bf750b9963f0b12a91e4`:

- official ICLR 2026 focal-paper denominator: 5,351;
- cached/parsed ICLR 2026 abstracts: 3,737;
- source-matching-allowed provisional seeds: 2,772;
- flagged but still matchable seeds: 1,753;
- explicit-solution repair queue: 965;
- missing/structural focal failures: 1,614;
- seed-route blocks actually matched under the lexical provisional backend: 11,088;
- pairwise matched slots: 35,273;
- measured zero-match blocks: 2,767;
- deduplicated provisional lexical coverage: k=4: 2,139 seeds; k=6: 1,545; k=8: 1,119; k=12: 611.

These counts are source-engineering measurements, not LLM outcomes.

## What these measurements support

### C1 — The experiment is not failing because the source universe is obviously empty

Under the provisional lexical backend, many seeds admit multiple candidate route-specific paper pools and pairwise source matches. The existence of 35,273 matched slots across 11,088 route blocks rules out the strongest early failure hypothesis: that ICLR simply lacks enough contemporaneous alternative-route literature to construct candidate contrasts.

This conclusion is deliberately weak: it establishes candidate-space abundance, not scientific validity of the candidates.

### C2 — Source abundance is highly uneven across route contrasts

At k=8, provisional per-pair coverage is:

- R1 BUILD vs DIAGNOSE: 80 seeds;
- R2 BUILD vs MEASURE: 805;
- R3 BUILD vs EXPLAIN: 327;
- R4 DIAGNOSE vs EXPLAIN: 11.

Thus the apparent source space is not balanced across the predeclared route system. R2 dominates, R3 is substantial, R1 is much narrower, and R4 is extremely sparse at larger packet sizes. This means a future paper cannot honestly present the four route contrasts as equally supported unless semantic/human validation changes this pattern materially.

### C3 — Packet size creates a real breadth tradeoff

Among the 2,772 provisional matchable seeds, lexical coverage drops from roughly 77% at k=4 to 56% at k=6, 40% at k=8, and 22% at k=12. The exact percentages are descriptive of the lexical provisional run only.

This validates the decision not to hard-code k=8 or k=12 before source/construct review. The final packet size should be chosen before scientific outcomes using the source-feasibility/construct-validity/precision tradeoff, not by future effect size.

### C4 — Seed construction is currently the dominant construct-validity risk

Of 2,772 provisional matching seeds, 1,753 retain risk flags, and 965 additional extractable focal cases are held in explicit-solution repair. Therefore source abundance cannot be converted directly into experimental sample size.

The bottleneck is no longer only `can we find papers?`; it is `are the seed questions and route contrasts meaningful, neutral, and human-auditable?`

### C5 — The lexical run demonstrates engineering feasibility, not semantic treatment validity

The recovery report explicitly labels the backend `LEXICAL_PROVISIONAL`: TF-IDF and BM25-like signals are not the intended dense semantic relevance measures, dates are unavailable in matching, semantic embedding calipers were not run, purity thresholds were not assessed, and human-approved blocks are still unknown.

Therefore the 1,119 k=8 lexical seeds are not 1,119 valid experimental seeds.

## What cannot be concluded

F0 provides no evidence for any of the following:

- scientific literature causally changes LLM research-route choice;
- stronger baseline route propensity causes resistance to evidence;
- grounding attenuates with abstraction;
- retrieval induces research monoculture;
- any route pair produces a larger model effect than another;
- any model family is more or less steerable;
- the current design is publication-ready.

Scientific proposal generations remain zero.

## Strongest current scientific interpretation

The most defensible one-sentence conclusion is:

> **The source universe appears rich enough to justify completing a rigorous feasibility and construct-validation stage, but the current experiment has not yet established a valid treatment bank or tested any LLM-behavior hypothesis.**

A stronger internal planning interpretation is:

> Source sparsity is probably not the main existential risk. Seed neutrality, route/equipoise validity, semantic relevance, and temporal audit are now the main risks.

## Implication for next stage

Do not launch broad ARS/model generation from all 2,772 provisional seeds.

Next stage should convert the large candidate space into a smaller certified development/confirmatory bank by:

1. completing semantic retrieval/reranking and date resolution;
2. repairing/auditing method-masked seeds;
3. human-auditing route clarity, relevance, plausibility, non-subsumption, and equipoise;
4. recomputing the matched-slot frontier under validated covariates;
5. freezing the source/treatment bank before baseline model measurements.

Only after this should a small development pilot estimate annotation variance, invalid-output rates, packet variance, and implementation noise.

## Current decision

**Research direction: KEEP.**

**Source feasibility: promising but unvalidated.**

**Scientific hypothesis status: untested.**

**ARS / proposal-generation authorization: HOLD until source and construct validation is accepted.**
