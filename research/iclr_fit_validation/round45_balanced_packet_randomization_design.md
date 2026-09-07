# Research Round 45 — Balanced Packet Randomization Design

## 1. Trigger

Round 44 creates pairwise matched evidence slots. We can further reduce document-identity and position confounding by constructing all alpha conditions from the **same selected slot set** within a packet family and using balanced/complementary A/B assignments.

This yields a randomized blocked design rather than five unrelated evidence packets.

## 2. Packet family

For block `b`, let the source-only matched-slot bank contain `J` pairs.

A **packet family** `f` samples/fixes `k` matched slots:

```text
F_f = {slot_1, ..., slot_k}
```

The same slot set `F_f` is used for all five alpha levels:

```text
alpha = 0,.25,.5,.75,1
```

Only which member of each A/B slot is shown changes.

## 3. Example with k=8

Suppose packet family contains slots 1–8.

### alpha=0

```text
B1 B2 B3 B4 B5 B6 B7 B8
```

### alpha=.25

Choose exactly 2 slots to expose A members:

```text
A1 A2 B3 B4 B5 B6 B7 B8
```

### alpha=.5

```text
A1 A2 A3 A4 B5 B6 B7 B8
```

### alpha=.75

Use a complementary or balanced pattern:

```text
A1 A2 A3 A4 A5 A6 B7 B8
```

### alpha=1

```text
A1 A2 A3 A4 A5 A6 A7 A8
```

A single realization should not always assign A to the same first slots; assignment is randomized and balanced across packet families/replicates.

## 4. Complementary assignments

For middle alpha conditions, use complementary assignment vectors where possible.

For k=8:

```text
alpha=.25 vector z
alpha=.75 vector 1-z
```

For alpha=.5, pair assignment vector `z` with complement `1-z` across realizations.

Advantages:

- each matched slot spends comparable exposure time as A and B;
- slot-specific salience is less correlated with route;
- route-position/doc-identity effects average out;
- packet comparisons become highly paired.

## 5. Balanced incomplete assignment across families

If `R` packet families/assignment realizations are used, design assignment vectors so each slot index is selected for A approximately equally often at each alpha.

Example for one fixed 8-slot family with 4 `.25` assignments:

```text
run 1: A at {1,2}
run 2: A at {3,4}
run 3: A at {5,6}
run 4: A at {7,8}
```

Then `.75` uses complements.

For `.5`, choose balanced 4-of-8 subsets such that every slot appears as A in the same number of realizations.

Exact construction can use a deterministic balanced design generated before outcomes.

## 6. Slot subset replication

There are two layers of evidence replication:

### Layer 1 — assignment replication

Same selected matched slots, different balanced A/B assignment vectors.

### Layer 2 — slot-family replication

Different `k`-slot subsets sampled from a larger J-slot bank.

This separates:

```text
route composition effect
slot/document-specific effect
choice of evidence subset
```

## 7. Paper order

Route assignment and document display position must be independent.

Preferred procedure:

1. select packet family/slots;
2. assign A/B members by alpha assignment vector;
3. draw a stored document-order permutation;
4. ideally reuse paired order structures across alpha so position does not systematically correlate with route.

Do not display all A-route abstracts first followed by all B-route abstracts.

## 8. Primary P1 design recommendation

If source coverage supports it:

```text
k = 8
3–4 distinct slot families per block
balanced A/B assignment vectors within each family
5 alpha levels
~10 stochastic generations per packet condition
```

The exact family/replicate counts remain subject to P0 variance results.

## 9. P0 simplification

For P0 engineering pilot:

```text
alpha = 0,.5,1
```

Use a smaller number of packet families but preserve the same paired-slot logic.

P0 should validate:

- packet construction determinism;
- balance;
- model context/format;
- annotation;
- document identity variance.

## 10. Randomization inference opportunity

Because A/B membership is randomized within matched slots for mixed conditions, a model-light randomization test can permute assignment vectors within the allowed balanced design.

This is useful as robustness but not necessary as the sole primary inference.

## 11. Local document influence is built in

Round 29's cross-route vs within-route replacement can reuse matched slots directly:

```text
B_i → A_i
```

is a one-slot cross-route replacement under excellent pre-treatment matching.

Within-route replacements can use alternative same-route matched candidates from the slot bank.

Thus the primary packet construction and mechanism robustness share one coherent source design.

## 12. Avoid deterministic route order

If A/B route descriptions shown to human annotators are randomized, the generator does not see route descriptions at all.

The generator sees only anonymous abstracts.

Therefore route A/B naming/order should not appear in the generation prompt or packet formatting.

## 13. Packet manifest fields added

Store:

```text
packet_family_id
slot_bank_id
selected_slot_ids
alpha
assignment_vector
assignment_design_version
paper_ids_after_assignment
order_permutation
packet_text_sha256
```

This supports exact reconstruction.

## 14. Strong causal interpretation

With paired slots and balanced assignment, the main contrast becomes close to:

> For the same set of evidence positions/topics/relevance strata, replace matched papers supporting one scientific strategy with matched papers supporting another and observe how the model's research-choice distribution changes.

This is substantially stronger than comparing two independent RAG searches.

## 15. Decision

**USE BLOCKED/BALANCED PACKET FAMILIES IN P1 IF F0 MATCHED-SLOT COVERAGE SUPPORTS THEM.**

This design improves causal precision without adding a new scientific claim or large conceptual scope.