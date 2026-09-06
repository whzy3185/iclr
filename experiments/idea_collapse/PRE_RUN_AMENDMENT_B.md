# PRE-RUN AMENDMENT B — Evidence Composition, Not RAG Quantity

> Date: 2026-09-06  
> Status: **PRE-SCIENTIFIC-RUN AMENDMENT**  
> Reason: ICLR-specific literature validation uncovered a decisive existing ablation that changes the primary hypothesis.  
> Supersedes no historical file: original README and Amendment A remain intact for provenance.

---

## 1. New evidence that triggered this amendment

Si, Yang & Hashimoto, *Can LLMs Generate Novel Research Ideas?* (ICLR 2025), Appendix A.29, explicitly ablates the number of retrieved papers included in the RAG prompt:

| `k` | Non-Duplicates (%) |
|---:|---:|
| 0 | 18.8 |
| 5 | 18.4 |
| 10 | 19.1 |
| 20 | 19.4 |

They conclude that varying the number of retrieved papers has minimal impact on their diversity metric. Their metric marks ideas as duplicates using all-MiniLM-L6-v2 cosine similarity > 0.8 to a previous idea.

They also show large backbone differences in non-duplicate rate, so model identity is a major confound that must be modeled explicitly.

Primary source:
https://proceedings.iclr.cc/paper_files/paper/2025/file/ea94957d81b1c1caf87ef5319fa6b467-Paper-Conference.pdf

This evidence was identified **before any scientific generation runs appear in the repository**.

---

## 2. Hypothesis change

### Previous broad H2

> Diversified retrieval produces more diverse scientific ideas than top-k retrieval.

This is no longer an acceptable primary hypothesis because it mixes:

- retrieval quantity;
- relevance differences;
- source composition;
- retrieval algorithm effects;
- generic generation diversity.

### Revised primary hypothesis H2-B

> **At fixed retrieval quantity and matched topical relevance, changing the composition of the evidence packet changes the structural distribution of generated scientific hypotheses.**

Primary object is **hypothesis structure**, not near-duplicate text diversity.

### Revised secondary hypothesis H2-C

> The composition effect can remain strong even when a Si-style near-duplicate metric changes little.

This is a deliberately falsifiable prediction, not an assumption.

---

## 3. Required E0 baseline

Before claiming a composition effect, reproduce/approximate the ICLR 2025 quantity ablation:

```text
k = 0 / 5 / 10 / 20
```

Report a compatible near-duplicate measure.

A near-null result here is **not** grounds to kill the revised topic. It is compatible with the revised hypothesis and establishes comparability with the accepted ICLR baseline.

---

## 4. Revised primary experiment: matched evidence packets

### Fixed variables

For each topic/model block:

- same model/version;
- same generator prompt text and language;
- same decoding parameters;
- same evidence count `k`;
- same approximate context-token budget;
- same corpus snapshot/hash;
- same query/topic;
- same relevance-score strata/histogram;
- matched year distribution;
- matched venue/quality/popularity when feasible.

### Manipulated variable

**Which evidence items are present.**

No condition may be called “more diverse” merely because it contains lower-relevance or random documents.

---

## 5. Controlled-overlap dose response

Construct evidence packets with target source-set overlap across independent runs:

```text
0%, 25%, 50%, 75%, 100%
```

Default `k=12` gives illustrative shared counts:

```text
0%   -> 0 shared + 12 matched unique
25%  -> 3 shared + 9 matched unique
50%  -> 6 shared + 6 matched unique
75%  -> 9 shared + 3 matched unique
100% -> 12 shared
```

Replacement documents must be drawn from the same pre-specified relevance strata.

Do not tune overlap levels after inspecting outcome curves.

---

## 6. Add a framing-composition intervention

Source overlap alone could still be dismissed as an obvious same-input effect.

Therefore, if corpus annotation is reliable, create matched evidence packets enriched for interpretable research framings, e.g.:

- method/architecture improvement;
- failure/stress testing;
- evaluation/measurement;
- mechanism/explanation;
- optimization/efficiency.

Pre-register packet-construction criteria without consulting downstream generations.

Test whether the evidence framing distribution predicts the downstream hypothesis framing distribution.

---

## 7. Revised primary outcomes

### Primary

Structured hypothesis tuple:

```text
(
  problem_object,
  failure_or_assumption,
  mechanism_or_explanation,
  intervention_or_method,
  evaluation_target
)
```

Report:

- category entropy/effective number;
- tuple/partial-tuple collision;
- Jensen–Shannon divergence between condition distributions;
- mutual information between context condition and hypothesis mode;
- blind human substantive-equivalence audit on a stratified subset.

### Secondary

- Si-style near-duplicate percentage;
- semantic embedding distances;
- cluster entropy;
- lexical diversity.

**A primary scientific conclusion must not rely only on embeddings or lexical metrics.**

---

## 8. Model effect handling

Because Si et al. report very large backbone diversity differences, analyses must include:

- within-model condition effects;
- model × evidence-composition interaction;
- pooled result only after stratified reporting.

A large model-family main effect does not invalidate the topic, but the composition effect must be non-negligible within at least two model families.

---

## 9. Prompt/query-language collision control

A July 2026 preprint reports that translating a RAG query changes retrieved sources and downstream scientific proposals.

To isolate our mechanism:

- all primary matched-packet generations use one fixed generator language;
- do not rely on multilingual query perturbation;
- directly intervene on the retrieved evidence packet;
- separately measure prompt paraphrase/order variance as a nuisance/noise floor.

---

## 10. Revised kill criteria

KILL / major pivot if:

1. matched evidence composition does not change structural hypothesis distributions beyond prompt/order noise in >=2 model families;
2. effects disappear after relevance/year/length matching;
3. differences are only lexical or embedding-level and fail blind substantive audit;
4. context composition cannot predict downstream framing on held-out topics;
5. a newly found direct paper already provides equivalent matched-packet causal evidence at comparable breadth.

Do **not** kill solely because E0 reproduces the prior near-null duplicate-rate result.

---

## 11. Continue criteria

Continue to mechanism experiments if most hold:

- composition effect reproducible in >=2 model families;
- >=3 ICLR-relevant subareas;
- effect exceeds prompt/order noise floor;
- structural metrics + human audit agree;
- evidence-framing enrichment has an interpretable directional effect;
- quality/testability does not collapse.

---

## 12. Stretch experiment is not part of the primary pilot

MUSES (arXiv:2609.00313) provides author-endorsed intellectual-root labels and motivates a later root-vs-relevance-matched evidence injection experiment.

Do not let MUSES integration delay or contaminate the primary matched-composition pilot. It requires a separate temporal-leakage design review before use.

---

## 13. Updated main-paper target

If the experiment succeeds, the intended claim is:

> **Retrieved evidence composition acts as a structured inference-time prior over LLM hypothesis search, and this steering can be invisible to standard duplicate-based ideation diversity metrics.**

Not:

> RAG makes ideas more/less diverse.
