# F0 Recovery Result

F0_DATA_STATUS: F0_INCOMPLETE
SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
SCIENTIFIC_PROPOSAL_GENERATIONS: 0

## Published Inputs and Execution

The actual R0 snapshot was published at `748110d50126067091ae08d213d91b447048c292`
before corrected matching. Original source commit `049a313ed2900f1acd9c2d6673abd2124280b85f`
and its caches were retained unchanged. Baseline main is
`b9cbbfdf0bafcf30adc7b8e261fdad6f08eb0ff8`. Source run `F0R-9f61bff4538465a7a96f` executed
code commit `78dbb1ebf7bb6a4b74fda96f86e951074ef9f857` with per-file code/config/spec hashes.
See the final run manifest for exact commands and source/transport provenance.

ICLR 2025: 3703/3703 cached title/abstract pairs verified. ICLR 2026: 3737/5351
verified. All 9054 official IDs remain in the acquisition manifest. No source
page was downloaded again; the missing 1614 remain an explicit incompleteness.

## Gate Recovery

First-run outputs are retained as INCOMPLETE_GATE_SHORT_CIRCUIT. Their empty
matching tables mean NOT_RUN. The legacy script had subsequently been edited,
so exact first-run code/output alignment is unknown rather than fabricated.

Corrected gate: 2772 source-matching candidates,
including 1753 flagged candidates; 965
explicit solution cases stay in repair; 1614 structural
failures remain retained. Confirmatory eligibility is false pending human review.

## Matching Actually Performed

- Backend: LEXICAL_PROVISIONAL. TF-IDF and BM25-like scores are not dense scores.
- Candidate rows: 831600.
- Exact source matchings solved: 11088 seed-route blocks.
- Maximum-cardinality-then-minimum-declared-integer-cost slots: 35273.
- Measured zero blocks: 2767.
- Unmatched source rows by reason: {'CAPACITY_COMPETITION': 181688, 'NO_ADMISSIBLE_EDGE': 55048}.
- Canonical typed cells: 2311632; statuses: {'MISSING_COVARIATES': 1197504, 'BLOCKED': 1114128}.

The declared lexical diagnostic inherits original lexical floors/gaps, uses
NetworkX 3.6.1 maximum-flow minimum-cost matching with deterministic tie rules,
and omits unavailable dates **explicitly**, not as zero. Costs use declared
micro-units. This is not calibrated semantic matching or scientific feasibility.
Full-abstract embedding-caliper comparisons were NOT_RUN because embeddings
were unavailable. Numeric purity .60/.70/.80 cells remain NOT_ASSESSED.

## Verification and Independence

Recovery unit tests passed, including the 3-edge fixture (cardinality 2, cost 4)
and 30 brute-force tiny-graph comparisons. The separate six Round 52 mathematical
tests passed; these are not LLM observations. All 18
normalized output artifacts replayed byte-identically. Volatile manifests are
separated; per-bank source non-reuse and table/grid counts reconcile.

`source_reuse_summary.json` distinguishes seeds, route blocks, source banks,
slots and packet assignments. Cyclic packet permutations are not new independent
banks. k=6 uses exact 0/0.5/1 fractions and does not claim quarter treatments.

## Remaining Scope and Stop

The cached-source lexical recovery is complete; full F0 is not. Missing focal
pages, semantic matching, first-public-date evidence and source/route audit remain.
The latest user permits ARS preparation/pilot after Task 1/2 completion, but the
complete source-feasibility prerequisite is not satisfied. Therefore no ARS
model selection, proposal generation, effect estimate or paper conclusion was
produced. Existing results are source measurements, not the proposed science.
