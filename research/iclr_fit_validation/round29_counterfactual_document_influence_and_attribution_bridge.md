# Research Round 29 — Counterfactual Document Influence and Attribution Bridge

## 1. Trigger

The main experiment changes the composition of entire evidence packets. A remaining objection is that the effect could be driven by a few unusually salient documents rather than a route-level property of scientific evidence.

A stronger mechanism test asks:

> When one matched paper is changed at a time, does replacing it across scientific routes have a larger and directionally consistent effect than replacing it within the same route?

This provides a local counterfactual bridge between document-level context and high-level research choice.

## 2. Secondary experiment scope

Run only after a primary route response exists.

Use a representative stratified subset of:

- seed-route blocks;
- model families;
- packet realizations;
- preferably middle exposure levels (`alpha=.25/.5/.75`) where both route types are present.

Do not scale this before the main effect is established.

## 3. Matched single-document perturbations

Start from frozen packet `C` of size `k`.

For a selected paper `p` in `C`, create two matched perturbations.

### W — within-route replacement

Replace `p` with a different paper `p_same` from the **same route**, matched on:

- relevance;
- token length;
- date;
- topic cluster;
- other frozen covariates.

This changes document identity while approximately preserving route composition.

### X — cross-route replacement

Replace `p` with a paper `p_cross` from the **opposite route**, using the same matching requirements.

This changes route composition by one paper while keeping document-level covariates similar.

The strongest local composition evidence is:

```text
|effect(cross-route replacement)|
  >
|effect(within-route replacement)|
```

with directional consistency across many papers/blocks.

## 4. Local influence estimand

For packet `C` and replacement `r` define:

```text
I_r = E[S | C_r] - E[S | C]
```

where `S` is blinded signed route score.

For an A→B replacement, expected composition-consistent sign is negative; for B→A, positive.

Do not orient sign based on observed model baseline.

Primary local contrast:

```text
LCI = mean directional effect of cross-route replacements
      - mean directional effect magnitude of within-route replacements
```

Use seed-clustered uncertainty.

## 5. Why not plain leave-one-out as the main diagnostic?

Deleting one paper changes:

- context length;
- information quantity;
- formatting;
- number of citations/sources.

A matched replacement is cleaner because context quantity is held approximately fixed.

Leave-one-out may still be exploratory for context attribution but should not be the main causal document-influence test.

## 6. Paper identity variance

The experiment also quantifies how much route response varies between interchangeable papers within one route.

If within-route replacements are almost as influential as cross-route replacements, the claimed route-level mechanism is weak.

Possible interpretation:

```text
document identity / idiosyncratic content dominates
```

Then composition summaries may be insufficient for natural-RAG prediction.

## 7. Optional context-attribution bridge

ICLR 2026 work provides context-attribution methods for RAG, including ARC-JSD-style sentence/context influence diagnostics.

For open models on a limited subset, apply an established attribution method to estimate which supplied papers/sentences contribute to the generated response.

This is **not a new attribution-method contribution**.

Compare two different quantities:

```text
response attribution mass
vs
counterfactual route-choice impact
```

They need not coincide.

## 8. Particularly informative dissociation

Possible pattern:

```text
Paper B receives high response attribution / concepts are visibly used
but replacing/removing B has little effect on high-level route choice.
```

This would show that low-level grounding/attribution and high-level decision influence are distinct.

Conversely:

```text
route-consistent attribution mass predicts counterfactual route shift
```

would support a more direct evidence-to-choice pathway.

Do not pre-assume either pattern.

## 9. Component-level variant

Combine with Round 23 standardized evidence cards:

- replace a P/F/M/L card from A with matched B card;
- keep representation format identical;
- test whether local route influence persists without raw abstract style.

This is expensive and optional.

## 10. Statistical treatment

The local replacement results are nested within the same seed and packet.

Use:

- seed-clustered summaries;
- paired comparison of cross-route vs within-route changes from the same base packet;
- distribution of local influences, not just pooled generation-level p-values.

## 11. Strong result

A strong mechanism pattern is:

```text
within-route replacement   ~ small / symmetric noise
cross-route replacement    directional shift
whole-packet mixture       larger cumulative dose response
```

This is exactly what a route-composition mechanism predicts.

## 12. Weak / kill-relevant result

If:

```text
within-route paper identity effects
≈
cross-route effects
```

then low-dimensional route composition may not be the right explanatory variable.

Natural-RAG prediction should then be expected to require richer document features, weakening the simplicity of the paper's mechanism claim.

## 13. Decision

**HIGH-VALUE MECHANISM ROBUSTNESS, CONDITIONAL ON CORE EFFECT.**

This experiment is a cleaner bridge than immediately attempting activation-level mechanistic interpretability. It stays close to the causal variable the paper actually claims to study.