# F0 Semantic / Temporal Source-side Result

```text
CORPUS_SHA256=0d0f182481534214ee0255a76b884fd4a959f04cc3d7ba85dbde5869dd5f6807
DENSE_BACKEND=BAAI/bge-base-en-v1.5@a5beb1e3e68b9ab74eb54cfd186867f64f240e1a MEASURED (5351 seeds, 3703 evidence)
RERANKER_BACKEND=BAAI/bge-reranker-base@2cfc18c9415c912f9d8155881c133215df768a70 MEASURED
TEMPORAL_2025_COVERAGE=3703/3703 discovered dates; statuses={'FALLBACK_ONLY': 3703}; historical completeness NOT_CERTIFIED
TEMPORAL_2026_COVERAGE=5351/5351 discovered dates; statuses={'FALLBACK_ONLY': 5351}; historical completeness NOT_CERTIFIED
SEMANTIC_SEEDS_PROCESSED=3950
K4_UNIQUE_SEEDS=1495
K6_UNIQUE_SEEDS=1253
K8_UNIQUE_SEEDS=1018
K12_UNIQUE_SEEDS=614
ROUTE_PAIR_K8_COUNTS={"R1": 30, "R2": 753, "R3": 419, "R4": 3}
ANONYMIZATION_LEAK_TESTS=PASS_METADATA_TEMPLATE_AND_F1_FIELDS; intrinsic content identifiers retained
MATCHING_TESTS=PASS_MAX_CARDINALITY_THEN_COST_AND_SOURCE_NONREUSE
F1_CALIBRATION_BLOCKS=24
F1_CERTIFICATION_BLOCKS=96
SCIENTIFIC_PROPOSAL_GENERATIONS=0
SCIENTIFIC_HYPOTHESIS_STATUS=UNTESTED
NEXT_GATE=F1_HUMAN_CONSTRUCT_CERTIFICATION
```

## Measured Scope

The frozen corpus and roles reconcile. Real dense inference covers all 5351
seed records; the independent cross-encoder scored 790000
pairs for 3950 existing source-gate-allowed seeds.
1401 records remain BLOCKED_SOURCE_GATE;
their missing reranker values are not zeros and are not silently discarded.
No model or threshold was chosen using proposal outcomes. Models and thresholds
were frozen before source scoring. The default BAAI checkpoints were retained.

The matching objective maximizes cardinality before minimizing declared nuisance
cost. All eligibility exclusions, unmatched reasons and cost components are
retained. No full-abstract A/B embedding-distance caliper was applied. The fixed
logit floor and nuisance calipers are engineering diagnostics, not calibrated
scientific truth. Counts do not authorize a scientific PASS/KILL decision.

## Temporal Limitation

The OpenReview API returned challenge-required 403 and was not bypassed. Two
arXiv references were inspected but did not identify the focal papers, so their
dates were not borrowed. The current dates therefore rely on verifiable official
publication metadata, not filenames, cache times or conference-year arithmetic.
These are minimum **discovered** dates. They do not establish actual earliest
availability or guarantee historical evidence-before-seed cleanliness.

The candidate bank satisfies the declared discovered-date ordering policy only.
It must not be presented as a certified temporal-clean bank. Human/source-history
review remains necessary; see temporal failures, date events and gap distributions.

## Source Anonymity and Human Gate

Visible F1 records contain the unchanged masked seed, neutral route descriptions,
and whitespace/Unicode-normalized raw abstracts. Metadata fields, scores and
source IDs are kept out of the visible evidence. Method names, findings, embedded
URLs and years in the scientific abstract remain, as required. This does not
guarantee that a knowledgeable reader cannot recognize a source.

Calibration and certification use disjoint unique seeds and deterministic
source-side strata. If targets were not reached, no extra low-quality blocks
were manufactured. Only visible candidate files should be distributed to human
annotators, not the hidden provenance, scores or full source corpus. No human
labels, proposal generations, baseline measurements or treatment outcomes exist.

STOP at the F1 human construct certification gate. The hypothesis is UNTESTED.
