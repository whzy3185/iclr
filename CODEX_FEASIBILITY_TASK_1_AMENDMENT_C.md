# Codex Feasibility Task 1 — Amendment C: Pairwise Matched Evidence Slots

> Applies to: `CODEX_FEASIBILITY_TASK_1.md` + Amendments A/B
> Status: PRE-OUTCOME SOURCE-ONLY AMENDMENT
> Scientific generation remains FORBIDDEN.

## Trigger

Research Round 44 strengthens the causal treatment construction from loose packet-level balance to **pairwise matched A/B evidence slots**.

The source-only audit should determine whether this cleaner design is constructible before any model outcomes exist.

Read:

`research/iclr_fit_validation/round44_pairwise_matched_evidence_slot_design.md`

---

# 1. New primary matchability object

For every promising `seed × route pair`, attempt to form matched slots:

```text
slot_j = (A_paper_j, B_paper_j)
```

where A/B papers are matched on frozen source-only covariates while representing different research routes.

Required matching variables at minimum:

```text
dense relevance
reranker relevance if available
abstract token length
first-public date / time distance
topic cluster or topic embedding distance
```

Optional consistently available covariates may be reported separately.

---

# 2. Matching algorithm requirements

Codex may implement a deterministic source-only matching algorithm such as:

- minimum-cost bipartite/Hungarian matching;
- optimal matching;
- deterministic greedy nearest neighbor without replacement.

The implementation must:

- use no model proposal outcomes;
- record matching cost definition;
- record hard calipers;
- preserve unmatched papers/reasons;
- use deterministic tie-breaking;
- save code/config/hash.

Do not optimize match weights against any future treatment effect.

---

# 3. New feasibility outputs

For each `seed × route pair`, report:

```text
n_A_above_floor
n_B_above_floor
max_matched_slots_under_calipers
median_match_cost
p90_match_cost
max_match_cost
matched_relevance_difference_summary
matched_length_difference_summary
matched_date_difference_summary
matched_topic_distance_summary
```

Evaluate whether matched-slot banks can support target packet sizes:

```text
k = 6
k = 8
k = 12
```

Use statuses:

```text
MATCHED_SLOTS_K6
MATCHED_SLOTS_K8
MATCHED_SLOTS_K12
INSUFFICIENT_MATCHED_SLOTS
CALIPER_FAILURE
```

A seed may support k=6 but not k=8/12; report rather than force one global k prematurely.

---

# 4. Matched-slot audit artifact

Add:

```text
experiments/idea_collapse/feasibility_1/matched_evidence_slots.csv
```

Fields at minimum:

```text
block_candidate_id
slot_id
route_A_paper_id
route_B_paper_id
A_dense_relevance
B_dense_relevance
A_reranker_relevance
B_reranker_relevance
A_token_length
B_token_length
A_first_public_date
B_first_public_date
topic_distance
match_cost
caliper_pass
```

This is source-only and contains no generated outcomes.

---

# 5. Packet feasibility simulation is allowed

Codex may create **paper-ID-only packet manifests** from matched slots to verify pre-treatment balance.

For example, for a candidate bank with J matched slots and k=8, simulate/freeze source-only assignment patterns at:

```text
alpha = 0,.25,.5,.75,1
```

This is not scientific generation.

Output optional/encouraged:

```text
feasibility_1/packet_balance_simulation.csv
```

Report balance across alpha on:

- relevance;
- total tokens;
- dates;
- topic distance/coverage.

Do not call any LLM research-proposal generator on these packets.

---

# 6. FEASIBILITY_RESULT additions

Answer:

1. How many unique seeds have at least one route pair with `>=6` matched slots?
2. How many with `>=8`?
3. How many with `>=12`?
4. Which R1–R4 route pairs provide the largest clean matched-slot banks?
5. Does pairwise slot matching materially reduce source coverage versus loose packet-level matching?
6. Are match-cost/relevance distributions comparable enough to justify a paired treatment design?
7. Does the source universe appear broad enough for multiple packet realizations per block?

Prefer the pairwise matched-slot design if feasible; report if it is too restrictive rather than silently reverting to loose matching.

---

# 7. Recommendation categories unchanged

Use:

```text
SOURCE_FEASIBLE_BROAD
SOURCE_FEASIBLE_NARROW
MARGINAL
NOT_FEASIBLE
```

The recommendation remains about source constructibility only.

---

# 8. Hard stop reiterated

Still forbidden:

- any no-context proposal generation;
- any evidence-conditioned proposal generation;
- any baseline route-propensity estimation;
- treatment outcome annotation;
- route redefinition based on imagined/model effects.

Stop after updated source-only feasibility artifacts and `FEASIBILITY_RESULT.md`.