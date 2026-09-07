# Research Round 51 — Hard-Gate and Workflow Audit

## 1. Trigger

The current F0 engineering prompt introduced explicit numeric source-feasibility thresholds and matching calipers. Before Codex executes them at scale, audit whether those hard gates are scientifically justified or whether they could create premature topic killing, design overfitting, or incentives to optimize source construction toward passing a threshold.

This audit occurs before F0 results and before any scientific proposal generation.

---

## 2. Executive conclusion

The staged workflow is directionally strong, but the current gate system mixes three different things that should be separated:

1. **non-negotiable scientific invariants**;
2. **engineering completeness checks**;
3. **scientific decision thresholds that require F0/F1/P0 information**.

Only category (1) should be hard-frozen now.

The current numeric F0 recommendation thresholds (`>=30 k=8 seeds`, route-pair counts, subfield concentration, etc.) are too strong to act as automatic kill/continue rules because they are not derived from power, precision, or a validated construct. They should be treated as planning reference points, not mechanical scientific gates.

Likewise, current route-purity confidence thresholds and matching calipers are useful sensitivity grids, but should not be allowed to define scientific feasibility automatically before human construct validation.

Decision:

> **KEEP the staged workflow, REVISE hard gates.**

---

## 3. What should remain truly hard

These rules are scientific integrity constraints and should not be relaxed later.

### H0.1 No scientific outcomes during F0/F1

No research-proposal generation, no baseline propensity estimation, no treatment effect estimation before authorization.

### H0.2 No outcome-dependent source/treatment construction

Routes, seed masking, retrieval, source inclusion, matching, packet construction, and analysis definitions cannot use proposal outcomes.

### H0.3 Preserve denominators and failures

No silent dropping of failed papers, seeds, route pairs, ambiguous labels, unmatched sources, invalid generations, or failed annotations.

### H0.4 No off-topic evidence to manufacture route contrast

If valid route-specific evidence does not exist at acceptable topical relevance, the block fails.

### H0.5 Treatment construction precedes baseline measurement

Evidence treatment blocks must be frozen before measuring no-context model route behavior.

### H0.6 Human construct validity cannot be rescued by an LLM classifier

If humans cannot reliably distinguish the intended scientific routes or judge both routes scientifically plausible, the block/contrast is not confirmatory-eligible.

### H0.7 Pilot outcomes cannot redefine the confirmatory hypothesis

P0 may inform variance, annotation burden, invalid-rate estimates, engineering decisions, and precision planning. It must not be used to select only high-effect blocks, routes, prompts, or model families.

### H0.8 Confirmatory stopping cannot use repeated significance peeking

Full-study stopping must use a fixed-N or predeclared precision rule.

These are genuine hard gates.

---

## 4. What should NOT be a hard gate yet

### 4.1 Exact number of F0 matched seeds

The previous `>=30 unique k=8 seeds` rule is a useful ambition but is not scientifically grounded enough to automatically define BROAD vs NARROW.

Why:

- required N depends on block heterogeneity and annotation variance;
- P0 can estimate those quantities;
- a 20-seed low-variance design may be more informative than a 40-seed high-noise design;
- a narrower but clean multi-subfield study may still produce a defensible controlled-behavior paper.

Therefore F0 should report coverage, not mechanically decide paper viability.

### 4.2 `k=8` as the only meaningful packet-size gate

`k=8` is a good default because it supports exact quarter mixtures, but F0 should report source feasibility at multiple packet sizes.

Recommended reporting grid:

```text
k = 4 / 6 / 8 / 12
```

Notes:

- `k=4`, `8`, `12` naturally support 0/.25/.5/.75/1 mixtures;
- `k=6` remains useful as an intermediate source-coverage diagnostic;
- choosing the final confirmatory k after F0/F1 but before any scientific outcomes is legitimate design selection, not p-hacking.

### 4.3 Route purity/confidence >= .70

A model/parser self-reported `0.70` confidence is not calibrated scientific evidence.

Use `0.60/.70/.80` as source-only sensitivity descriptors, but do not allow a provisional classifier confidence threshold to kill the study.

Human F1 route audit should determine which papers/contrasts are genuinely route-clear.

### 4.4 STRICT/BASE/RELAXED matching calipers

These are useful predeclared sensitivity tiers, but the particular numeric calipers were not empirically calibrated.

They should answer:

> How does coverage trade off against observable balance?

rather than:

> Does BASE pass, yes/no?

F0 should publish the complete coverage–balance frontier across the predeclared tiers. The research lead chooses the final matching regime before scientific generation, using source-only balance and human validity evidence.

### 4.5 Common temporal-clean subset as the only viable design

`first_public > 2024-08-31` is a valuable conservative common-cutoff subset for Llama 3.1 + Gemma 3, but it should not be interpreted as proof of contamination absence or the only possible causal design.

F0 should report at least:

```text
T0_COMMON_STRICT: first public > 2024-08-31
T1_LLAMA_CLEANER: first public > 2023-12-31
T2_ALL_ACCEPTED: all ICLR 2025, clearly marked contamination-uncertain
```

The final primary tier is selected before model outcomes.

This avoids killing an otherwise strong Llama-based causal design solely because the Gemma-common cutoff is source-sparse.

---

## 5. Revised F0 purpose

F0 should be a **descriptive source-feasibility map**, not an automatic scientific judge.

Codex should return a multidimensional scorecard:

### Coverage axis

- unique seeds with >=2 supported routes;
- unique seeds at k=4/6/8/12 matched slots;
- route-pair distribution;
- subfield distribution;
- number of independent packet realizations.

### Balance axis

For each matching tier:

- relevance differences;
- reranker differences;
- token-length ratio;
- date differences;
- topic distance;
- match-cost distributions.

### Construct-risk axis

- route ambiguity;
- provisional route-purity distribution;
- lexical shortcut strength;
- seed leakage rates;
- high-composability/subsumption frequency.

### Temporal-risk axis

- T0/T1/T2 coverage;
- UNKNOWN/AMBIGUOUS public-date rates;
- subfield-dependent attrition.

### Concentration axis

- subfield concentration;
- route-pair concentration;
- seed attrition waterfall.

F0 itself should return only an engineering state:

```text
F0_COMPLETE
F0_INCOMPLETE
F0_BLOCKED
```

Scientific feasibility classification is reserved for the research lead after reviewing F0 artifacts.

---

## 6. Revised stage workflow

Recommended order:

```text
F0A — source acquisition + temporal map
F0B — provisional routes + retrieval + matching frontier
      ↓
RESEARCH-LEAD SOURCE REVIEW
      ↓
F1 — human seed / route / equipoise / annotation construct audit
      ↓
D0 — PRE-OUTCOME DESIGN FREEZE
     choose temporal tier, k, route roster, matching regime,
     source purity rules, prompt, annotation rubric
      ↓
P0 — blinded engineering / variance pilot
      ↓
D1 — CONFIRMATORY PRECISION FREEZE
     fix SESOI/ROPE, N or CI-width target, models, packet realizations,
     alpha grid, holdout split
      ↓
P1 — confirmatory matched-mixture study
      ↓
G1 — interval-based scientific decision
      ↓
P2 — anti-priming / mechanism robustness
      ↓
G2
      ↓
P3 — held-out natural-RAG prediction
      ↓
G3 — paper-scope decision
```

---

## 7. Important revision to P0/G0

The existing workflow says full expansion requires that `some route movement is plausible enough` in P0.

This can create a hidden winner's-curse channel: only expand if the pilot looks promising.

Replace this with:

> P0 is primarily for construct reliability, invalid rates, packet variance, annotation variance, prompt/order nuisance, and sample-size/precision planning.

Preferred discipline:

- keep treatment labels masked from the research lead while estimating variance where practical;
- do not choose route pairs/models based on pilot effect magnitude;
- use P0 effect estimates only for documented exploratory diagnostics;
- a pilot may kill for **precise practical nullity** only after a ROPE/SESOI has been defined independently of the observed effect;
- otherwise inconclusive pilot effects do not determine continuation.

G0 should ask whether the confirmatory study can estimate the predeclared scientific quantity with adequate construct validity and precision—not whether the pilot happens to look exciting.

---

## 8. SESOI / ROPE timing

Do not hard-code a scientific effect-size threshold during F0.

Set the smallest effect size of interest after F1/P0 has established:

- what one unit of the human ordinal route score means;
- annotation reliability;
- within-block stochastic variance;
- between-seed heterogeneity;
- feasible number of independent seeds.

But set SESOI/ROPE **before unblinding or launching P1 confirmatory outcomes**.

Possible form:

```text
ROPE = [-delta_min, +delta_min]
```

where `delta_min` is justified by human interpretability and precision, not by the observed P0 treatment estimate.

---

## 9. Revised G1 decision logic

After P1, use interval logic rather than significance alone.

### Meaningful effect

Primary estimate CI lies materially outside the predeclared ROPE in the predicted direction, with no fatal construct/quality failure.

### Precise null

Primary estimate CI lies substantially inside the ROPE.

Interpret as evidence against a practically meaningful average H1 effect.

### Inconclusive

CI overlaps both the ROPE and meaningful-effect region.

Do not call positive or negative. Expand only if a predeclared precision rule allows additional sampling.

### Heterogeneous

Average effect masks strong predeclared model/subfield interactions.

A narrower claim may survive if heterogeneity was modeled and is replicated; do not automatically force an average-effect story.

---

## 10. Revised G2/G3 interpretation

### G2

Do not require every anti-priming test to pass.

Require that the strongest plausible trivial explanation is materially weakened by a predeclared core robustness set, for example:

- direct-copy exclusion;
- cross-route vs within-route replacement;
- method-cue-reduced context.

Mechanism analyses beyond that are explanatory extensions, not automatic paper gates.

### G3

Natural-RAG failure should narrow the claim to controlled-context behavior, not automatically invalidate a strong causal result.

Strong natural-RAG prediction substantially upgrades paper significance and ecological relevance.

---

## 11. Current assessment of existing workflow

| Component | Assessment | Action |
|---|---|---|
| F0 before generation | Strong | Keep hard |
| Codex stage authorization | Strong | Keep hard |
| denominator preservation | Strong | Keep hard |
| treatment before baseline | Strong | Keep hard |
| human equipoise gate | Strong | Keep hard |
| exact `>=30 k=8` F0 threshold | Too rigid | Demote to planning reference |
| `0.70` route confidence hard filter | Not calibrated | Sensitivity only until F1 |
| BASE calipers as yes/no feasibility | Too rigid | Use balance–coverage frontier |
| common temporal cutoff only | Too restrictive | Report tiered temporal designs |
| P0 continuation based on apparent effect | Selection-risk | Remove |
| P1 confirmatory stage | Strong | Keep |
| G1 significance-style interpretation | Too vague | Use ROPE/interval logic |
| P2 anti-priming before natural RAG | Strong | Keep |
| P3 held-out prediction | Strong | Keep, but claim-narrowing not automatic kill |

---

## 12. Decision

**WORKFLOW: KEEP WITH REVISION.**

The main principle is:

> Freeze integrity rules early; defer scientific effect/coverage thresholds until the information required to justify them exists, while still freezing them before confirmatory outcomes.

This is more conservative than both extremes:

- it avoids relaxing standards after seeing outcomes;
- it also avoids killing a valid design using arbitrary pre-data numbers.
