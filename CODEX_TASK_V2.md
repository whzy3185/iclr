# Codex Task V2 — Implement Preregistration V1 Without Generating Scientific Outcomes Yet

> Repository: `whzy3185/iclr`  
> Status: current Codex handoff  
> Scientific contract: `experiments/idea_collapse/PREREGISTRATION_V1.md`

---

## Master instruction

You are the experimental engineering partner for this ICLR research project.

The old broad `idea collapse / top-k vs MMR` task is historical. Do not implement it as the main scientific experiment.

Read in this order:

1. `experiments/idea_collapse/PREREGISTRATION_V1.md`
2. `research/iclr_fit_validation/round8_selection_independent_design.md`
3. `research/iclr_fit_validation/round7_internal_validity_and_dataset_design.md`
4. `research/iclr_fit_validation/taxonomy_design_draft.md`
5. `research/iclr_fit_validation/novelty_claim_matrix.md`
6. `README.md`
7. historical `CODEX_WORKFLOW.md` only for reproducibility / anti-p-hacking discipline

Current question:

> Can retrieved scientific literature override an LLM's default scientific-method / research-mode prior, and does evidence uptake weaken at higher abstraction levels?

Your current job is **not to answer that question yet**.

Your current job is to prove that the dataset, treatment construction, taxonomy, temporal-cleanliness logic, and matching pipeline are valid enough that a scientific generation run would mean something.

---

# HARD STOP FOR THIS TASK

Proceed autonomously through V2 Tasks 0–5 below.

After producing the treatment-selection and evidence-matching artifacts, **STOP BEFORE P0-A/P0-B scientific model generation**.

Do not run large LLM generation batches until the research lead reviews the pre-treatment construction.

---

# V2 Task 0 — Repository/spec audit

Confirm:

- no existing treatment outcome should be mixed into preregistration;
- which historical files are superseded operationally by `PREREGISTRATION_V1.md`;
- current repo state / branch / commit;
- environment, Python/dependency constraints;
- storage layout for corpora/manifests/caches.

Create/update:

```text
experiments/idea_collapse/STATUS.md
```

Record exact commands and commits.

---

# V2 Task 1 — Official ICLR metadata ingestion

Build reproducible ingestion for:

## Evidence universe

ICLR 2025 accepted papers.

Prefer official ICLR proceedings / OpenReview metadata as canonical IDs/titles/abstracts/decisions.

Fields at minimum:

```text
paper_id
openreview_id if available
title
abstract
keywords/area if available
decision
proceedings_url/openreview_url
first_public_date
first_public_source
possible_earlier_version
```

## Seed universe

ICLR 2026 accepted papers with equivalent metadata.

### Data provenance

Every downloaded/generated metadata file needs:

- source URL/API;
- retrieval date;
- raw-file hash;
- processing-script commit;
- processed-table hash.

Do not silently substitute a third-party paper list if the official source is unavailable. A third-party dataset may be used only as a clearly marked cross-check/cache accelerator.

---

# V2 Task 2 — Temporal-cleanliness pipeline

Primary clean cutoff:

```text
2024-08-31
```

Implement a reproducible process for identifying first-public date and earlier versions.

Potential sources, in descending priority as appropriate:

- OpenReview submission date;
- arXiv first-submission date;
- official/public preprint metadata;
- DOI/publication metadata.

Do not infer first-public date from the ICLR proceedings publication date alone if an earlier arXiv version exists.

Create:

```text
experiments/idea_collapse/model_cutoff_manifest.json
experiments/idea_collapse/corpus_manifest.json
```

`model_cutoff_manifest.json` should include source citations/URLs for:

- Llama 3.1 cutoff (Dec 2023);
- Gemma 3 cutoff (Aug 2024);
- exact planned checkpoint IDs if known.

Produce a temporal-cleanliness report with:

- total ICLR 2025 accepted;
- number with resolvable first-public dates;
- number passing post-2024-08-31 rule;
- ambiguous/excluded counts and reasons;
- subfield coverage after filtering.

Do not generate model outputs in this task.

---

# V2 Task 3 — Seed-question extraction pipeline

From ICLR 2026 papers, create method-masked candidate research questions.

Important distinction:

The source paper method is not a gold answer.

For every seed record:

```text
seed_id
focal_paper_id
subfield
raw_problem_context
method_masked_question
removed_solution_tokens/entities
focal_first_public_date
quality_flags
```

### Method masking

Remove:

- title/author identifiers;
- explicit name of proposed method;
- focal model/dataset names introduced by the paper;
- wording that directly gives away the solution.

Preserve enough technical content that multiple scientifically plausible approaches remain possible.

### Audit

Manually inspect / prepare for human inspection a stratified sample before using seeds in experiments.

Create:

```text
experiments/idea_collapse/seed_manifest.json
```

with candidate status; do not only save selected seeds.

---

# V2 Task 4 — Taxonomy development and pre-treatment audit

Use `research/iclr_fit_validation/taxonomy_design_draft.md` only as a starting draft.

### Source material allowed for taxonomy development

- ICLR source-paper abstracts;
- candidate seed descriptions;
- if needed, engineering-only no-outcome examples not drawn from treatment runs.

Do NOT inspect treatment effects because they do not exist yet.

Create a candidate:

```text
experiments/idea_collapse/TAXONOMY.md
```

covering:

## Layer A — scientific move

Initial candidates:

- BUILD_IMPROVE
- DIAGNOSE_STRESS_TEST
- MEASURE_EVALUATE
- EXPLAIN_MECHANISM_THEORY
- OPTIMIZE_EFFICIENCY
- VERIFY_FALSIFY_REPLICATE

## Layer B — method inventory

Reuse/adapt established Carlon-style methodology dimensions rather than inventing a new ontology.

### Annotation sample

Construct a blinded sample across:

- subfields;
- years;
- source-paper types;
- expected scientific moves.

Prepare independent labels where human annotators are available; otherwise create the infrastructure and a clearly marked pending-human-audit artifact.

Create:

```text
experiments/idea_collapse/annotation_audit_pre_treatment.md
experiments/idea_collapse/taxonomy_version.json
```

### Taxonomy gate

If categories cannot be distinguished reliably, revise/merge now.

Do not optimize labels for an effect that has not been measured.

---

# V2 Task 5 — Selection-independent treatment construction

This is the most important current task.

For every candidate seed:

1. retrieve a large pool of temporally clean ICLR 2025 papers;
2. compute frozen relevance features;
3. annotate source scientific moves using frozen taxonomy;
4. apply relevance floor;
5. enumerate mode pairs with enough evidence;
6. evaluate matching feasibility;
7. choose treatment pair using a deterministic model-output-independent rule.

Recommended pair-selection rule from Preregistration V1:

```text
enumerate all pairs passing count + matching gate
→ maximize minimum matched evidence count
→ global frozen priority order breaks ties
```

Do not know or use any model's P0 scientific prior when choosing the pair.

### Retrieval/matching outputs

For every evidence candidate save:

```text
seed_id
paper_id
mode_label
dense_relevance
reranker_relevance
token_length
public_date
topic_cluster
other frozen matching covariates
```

Create:

```text
experiments/idea_collapse/TREATMENT_MODE_SELECTION.md
experiments/idea_collapse/treatment_selection_hash.json
experiments/idea_collapse/evidence_matching_report.md
```

### Evidence matching report must include

- eligible / excluded seed counts;
- exclusion reasons;
- selected mode pair per seed;
- candidate counts per mode;
- relevance overlap;
- standardized mean differences or equivalent balance diagnostics;
- token/date/topic balance;
- example packets;
- lexical separability diagnostic plan;
- seeds that fail matching.

### Packet generation

You may generate/freeze **paper ID lists / evidence packet definitions** during Task 5.

Do NOT call scientific generation models on those packets yet.

---

# Required tests

At minimum:

- deterministic metadata normalization test;
- corpus hash reproducibility;
- temporal cutoff boundary tests;
- seed masking unit tests / schema tests;
- taxonomy JSON/schema validation;
- deterministic treatment pair selection;
- no leakage of focal paper into its seed evidence pool;
- packet-size and relevance-strata tests;
- evidence order randomization reproducibility;
- duplicate paper-ID detection;
- config/hash snapshot tests.

---

# Forbidden shortcuts

Do not:

- use all ICLR 2025 papers without checking first-public dates for the clean subset;
- choose treatment modes based on model outputs;
- use off-topic/random papers to create diversity;
- let an LLM-generated summary silently add a future-work recommendation;
- hard-code a few hand-picked seeds because they look promising;
- drop failed matching seeds from the manifest;
- call an LLM novelty score ground truth;
- begin writing results/abstract as if the phenomenon has been observed.

---

# End-of-task deliverable

Update `STATUS.md` with:

- exact repo commit;
- corpus counts;
- temporal-clean counts;
- candidate seed counts;
- taxonomy status/reliability status;
- treatment-eligible seed counts;
- matching quality;
- all blockers/deviations;
- exact command that WOULD start P0-A, but do not run it.

Then stop and hand the repository back for scientific review.

The next research decision will be whether the pre-treatment construction is valid enough to authorize P0-A/P0-B generation.
