# Codex Feasibility Task 1 — Amendment B: Seed Validity, Equipoise, and Multi-Route Coverage

> Applies to: `CODEX_FEASIBILITY_TASK_1.md` + Amendment A
> Status: PRE-OUTCOME SOURCE-ONLY AMENDMENT
> Scientific generation remains FORBIDDEN.

## Trigger

Research Rounds 27–34 add several pre-treatment validity requirements that materially affect whether the scientific experiment is constructible:

- route-pair scientific equipoise;
- route composability / non-subsumption;
- seed method leakage and neutrality;
- multi-route openness;
- possible three-route coverage;
- explicit attrition/generalization accounting.

This amendment updates the source-only feasibility task. It does **not** authorize any model research-proposal generation.

---

# 1. Read these additional research files

Before completing feasibility, also read:

1. `research/iclr_fit_validation/round27_route_equipoise_and_admissibility_audit.md`
2. `research/iclr_fit_validation/round30_seed_validity_method_masking_and_accessibility.md`
3. `research/iclr_fit_validation/round31_three_route_simplex_extension.md`
4. `research/iclr_fit_validation/round33_staged_execution_and_hard_gates.md`
5. `research/iclr_fit_validation/round34_last_30d_collision_update.md`

Where older feasibility wording conflicts, this amendment is newer for source-only validity requirements.

---

# 2. Seed validity fields

Extend `seed_candidates.jsonl` with provisional source-only fields:

```text
problem_clarity
background_sufficiency
method_neutrality
multi_route_openness
technical_substance
iclr_relevance
focal_method_leak
solution_prescribed
distinctive_phrase_leak
too_broad
too_narrow
post_cutoff_concept_needs_definition
```

These may initially be machine-assisted/provisional, but prepare a human-audit sample.

Do not call an LLM to propose a solution to the seed.

## Text leakage diagnostics

Record:

- seed-to-focal-title lexical similarity;
- seed-to-focal-abstract similarity;
- distinctive n-gram/acronym overlap;
- explicit removed method/entity strings where available.

The goal is to detect whether the masked seed still acts as a fingerprint for the focal solution.

---

# 3. Route-pair equipoise audit packet

For each promising `seed × route pair`, prepare a source-only human audit row containing:

```text
seed_id
route_A_neutral_description
route_B_neutral_description
A representative evidence IDs
B representative evidence IDs
A relevance summary
B relevance summary
A evidence count
B evidence count
```

and blank human-rating columns for:

```text
A_RELEVANCE_TO_SEED 1–5
B_RELEVANCE_TO_SEED 1–5
A_SCIENTIFIC_PLAUSIBILITY 1–5
B_SCIENTIFIC_PLAUSIBILITY 1–5
DISTINGUISHABILITY 1–5
EQUIPOISE 1–5
NON_SUBSUMPTION 1–5
ANNOTATABILITY 1–5
COMPOSABILITY 1–5
ROUTE_DOMINANCE {A_CLEAR,A_SOMEWHAT,ROUGHLY_EQUAL,B_SOMEWHAT,B_CLEAR,CANNOT_JUDGE}
```

Codex may prepare this packet but may not invent human ratings.

Create:

```text
experiments/idea_collapse/feasibility_1/route_equipoise_audit_packet.csv
```

---

# 4. Route description rule

Neutral route descriptions must be source-derived and approximately matched in length.

Do not use value-laden language such as:

- `stronger`;
- `more rigorous`;
- `novel`;
- `better`.

Descriptions should specify scientific objective/framing, not exact implementation.

---

# 5. Composability / route-pair type

For every global route pair and seed, record a provisional pair type where possible:

```text
TYPE_I_COMPETING_STRATEGIC
TYPE_II_COMPETING_EPISTEMIC
TYPE_III_COMPLEMENTARY_HIGH_COMPOSABILITY
TYPE_IV_HIERARCHICAL_OR_SUBSUMED
UNCLEAR
```

This is source-only metadata, not a scientific outcome.

Report how many candidate pairs appear obviously hierarchical/subsumed or highly composable.

Do not silently exclude them from the manifest.

---

# 6. Three-route coverage audit

For every candidate seed, additionally report whether **three or more** distinct routes have sufficient evidence above the relevance floor and plausible matching support.

Add fields:

```text
n_supported_routes
eligible_3plus_routes_provisional
best_triplet_if_any
triplet_min_evidence_count
triplet_matchability_status
```

This is only to assess future simplex feasibility.

Do not prioritize 3-route seeds over valid 2-route seeds for the core experiment.

---

# 7. Attrition accounting

`FEASIBILITY_RESULT.md` must include a waterfall/attrition table:

```text
ICLR 2026 candidate focal papers
→ extractable method-masked seeds
→ seed validity/leakage pass candidates
→ multi-route-open candidates
→ >=2 source-supported routes
→ relevance-matchable route pairs
→ candidate equipoise-valid route pairs (pending human audit where applicable)
→ potential final experimental blocks
```

If human equipoise ratings are not yet available, distinguish:

```text
SOURCE-FEASIBLE
PENDING-HUMAN-EQUIPOISE
```

Do not call a block final/eligible before the human gate.

---

# 8. New feasibility summary outputs

Add to `feasibility_1/`:

```text
seed_validity_audit_packet.csv
route_equipoise_audit_packet.csv
multi_route_coverage.csv
attrition_waterfall.csv
```

and summarize:

- number of unique seeds with >=2 supported routes;
- number with >=3 supported routes;
- route-pair coverage by subfield;
- route-pair coverage by R1–R4;
- likely high-composability/hierarchical fraction;
- seed leakage/neutrality concern counts;
- source-matchable blocks awaiting human equipoise review.

---

# 9. Updated recommendation vocabulary

At source-only completion use one of:

```text
SOURCE_FEASIBLE_BROAD
SOURCE_FEASIBLE_NARROW
MARGINAL
NOT_FEASIBLE
```

This recommendation concerns constructibility only.

It does not authorize scientific generation.

---

# 10. Hard prohibition reiterated

Still forbidden:

- no-context research proposal generation;
- treatment research proposal generation;
- model route propensity estimation;
- route-effect estimation;
- scientific outcome annotation;
- changing R1–R4 because of imagined effect size;
- paper result writing.

Stop after updated `FEASIBILITY_RESULT.md` and source-only audit artifacts.
