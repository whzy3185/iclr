# Round 62 — Semantic checkpoint audit and bounded F1 calibration

Date: 2026-09-20.
Inspected experiment branch: `codex/f0-semantic-temporal-20260909`.
Pinned experiment commit: `e0fbbf27bae69030e9487fdf1958a27e84a18335`.
Inspected main before this round: `a22dc5a32ce2d75815e455c7e970f5f3fc49b6b6`.

## Decision and scope

Accept this as a substantive source-side semantic-scoring checkpoint, not as certified scientific feasibility or an LLM result. Proceed to a bounded F1 calibration/source-repair task; do not launch proposal generation, baseline measurements, ARS search, P0/P1, or automatic certification of 96 blocks.

This round inspected repository reports, configuration, scoring/matching/source-preparation code, small manifests, and selected calibration records. It did NOT rerun 790,000 cross-encoder evaluations, recompute the full corpus hash, reproduce the experimental test suite, or human-certify 120 records. Concrete sample concerns below are analyst judgments, not a blinded human gold set or an estimated population error rate. A large certification-file read returned no usable content through the connector; no conclusion of file emptiness or corruption is drawn from that response.

## 1. What has materially advanced

The report and code identify actual BGE bi-encoder and cross-encoder computation rather than relabeling lexical scores. Dense scoring covers 5,351 seed records and 3,703 evidence documents; 3,950 allowed seeds receive 200 cross-encoder scores each, totaling 790,000. Another 1,401 source-gate-blocked seeds remain explicit. The source corpus hash remains `0d0f182481534214ee0255a76b884fd4a959f04cc3d7ba85dbde5869dd5f6807`. [R1,R2,R3]

`matching/coverage.json` distinguishes 15,800 measured seed-route blocks, 9,752 measured zeros, and 5,604 source-gate-blocked blocks. The corresponding nonzero count is 6,048. Arithmetic reconciliation: 3,950+1,401=5,351; 3,950*200=790,000; 15,800+5,604=5,351*4. These are checks of published aggregate arithmetic, not a replay of individual rows. [R4]

| Required slots | Unique candidate seeds | Fraction of 3,950 reranked seeds | Fraction of 5,351 official seeds |
|---|---:|---:|---:|
| k=4 | 1,495 | 37.85% | 27.94% |
| k=6 | 1,253 | 31.72% | 23.42% |
| k=8 | 1,018 | 25.77% | 19.02% |
| k=12 | 614 | 15.54% | 11.47% |

These describe the implemented candidate policy, not human-validity rates. The measured-zero fraction is 61.72% of measured blocks; it is not the fraction of invalid research problems.

| Route pair | k=4 | k=6 | k=8 | k=12 |
|---|---:|---:|---:|---:|
| R1 BUILD / DIAGNOSE | 236 | 78 | 30 | 6 |
| R2 BUILD / MEASURE | 1,273 | 1,003 | 753 | 435 |
| R3 BUILD / EXPLAIN | 1,007 | 649 | 419 | 184 |
| R4 DIAGNOSE / EXPLAIN | 22 | 9 | 3 | 0 |

Do not sum rows as distinct seeds. Do not infer that R2 will steer models more than R1, or that R4 is scientifically unimportant. Labels and candidate rules can create these differences. Sparse R4 at k=8 does not require dropping its k=4 calibration cases.

The previous lexical result of 1,119 k=8 seeds used a different eligible cohort (2,772), representation and matching policy. `1018/1119` is not a semantic survival rate. A paired comparison requires common seed IDs and unchanged scientific rules, with gained/lost/retained IDs and reasons.

## 2. Critical audit finding: semantic computation is not semantic certification

The declared matching rule uses raw reranker logit >=0, dense/reranker percentile gaps <=0.10 and a token-length ratio <=1.50. The BGE authors describe reranker outputs as unbounded relevance scores and caution that embedding-score cutoffs depend on the downstream data. Neither a rank percentile nor raw logit 0 is a universal boundary for scientific relevance. [R2,E1,E2]

Matching two similarly ranked papers can match two weakly related papers. The pipeline appropriately calls the thresholds engineering diagnostics, but downstream summaries must keep this limitation visible. Do not address it by arbitrarily replacing 0 with a larger number. Calibrate against source judgments on a developmental subset, then freeze and evaluate independently.

### Concrete sample A: calibration record 1

Block key `345b55b6ef513c049c91d1e1` concerns biases and reliability in `[MASKED_ENTITY]-as-a-Judge`. Its packet contains, among other topics, unreliable-feedback post-training, causal anomaly-root diagnosis, RAG trust, artistic-style identification, offline RL corruption, test-time adaptation attacks and web-agent robustness. [R5]

Some of these could be useful analogies, but the displayed material does not establish that each is direct evidence for this particular judge-bias problem. Direct topical support, justified cross-domain transfer and loose thematic similarity need separate labels. A raw positive score cannot certify the missing bridge.

The seed also repeats the problem paragraph, appends a proposal-generation TASK instruction, and masks the generic model-class term. These are observable properties of the input. Their causal effect on retrieval remains untested.

### Concrete sample B: calibration record 24

Block key `03d24e1f3f0d2e26d3310901` concerns RL generalization but retains an explicitly suggested teacher/student curriculum solution while masking its name. Removing an acronym does not remove the solution prescription. [R6]

Its DIAGNOSE-side abstracts include papers explicitly proposing safe-transfer or robust-policy methods, often combined with diagnostic analysis. This does not prove that all labels are wrong; it shows why inherited single-primary-route/ROUTE_CLEAR labels must be checked for mixed contributions rather than treated as ground truth.

These were non-random calibration spot checks, partly selected for interpretability. No overall defect prevalence is inferred, and borderline calibration examples are not evidence that the 96-record certification queue has the same composition.

## 3. Route labels and query representation are still legacy components

`build_bank.py` imports source labels from the earlier recovery run and filters on `route_purity_descriptor == ROUTE_CLEAR`. New semantic scores have not independently validated those labels. `prepare_sources.py` preserves old extractable masked seeds and applies the same transformation to newly available records. [R3,R7]

`semantic_compute.py` embeds and reranks the full `method_masked_question` field, which in sampled records includes duplicated problem text and generation instructions. It truncates to 512 tokens; cross-encoder query and document share that budget. The bi-encoder manifests record full length/truncation, but the inspected reranker loop does not emit per-pair retained query/document lengths. [R8]

Required diagnostic, not an asserted result: compare existing Q0 against Q1 (deduplicated problem text, no generic generation instruction) on the same calibration seeds and fixed model checkpoints. Q2 may additionally repair method masking with traceable source spans; if no reliable source-grounded repair is available, keep Q2 pending. Do not infer improvement from larger k-coverage alone; use blinded query-document relevance judgments.

Do not treat the bi-encoder and same-provider cross-encoder as statistically independent validation. They are separate model computations, not human truth or proven independent error processes. This scope is already stated in the model code.

## 4. Temporal audit: complete date fields, incomplete historical knowledge

All 3,703 evidence and 5,351 focal records are `FALLBACK_ONLY`. The date-gap artifact has exactly one value: all 790,000 scored pairs have evidence-minus-seed difference -354 days. [R1,R9]

This means the observed cross-year ordering supplies no pair-level discrimination in this run. It is not evidence that every paper actually appeared for the first time 354 days before its focal question. Inspect exact per-paper and per-year date distributions before using any date term as a substantive balancing variable.

Let t_first be actual first availability and d_min the earliest date among sources found so far. Then t_first <= d_min. Knowing d_min is after a cutoff does NOT establish t_first after that cutoff. By contrast, a verified earlier version is evidence against a post-cutoff claim.

Separate three claims:

1. **Contemporary fixed-model context intervention:** randomized exposure can be studied with previously published/familiar documents. Familiarity affects interpretation and generalization, but is not automatically a confound of correctly randomized exposure. Claim only behavior under the specified current corpus/model conditions.
2. **Unseen/post-training-cutoff evidence:** needs model-specific cutoff reasoning and substantially stronger version-history evidence; fallback publication dates cannot support it.
3. **Historical forecasting:** needs genuinely available-at-t inputs and protection against focal-paper/future leakage. The current date map is insufficient.

Allow F1 construct calibration to proceed while researching version history for its selected documents. Do not block all calibration until 9,054 exhaustive histories exist. Do not silently rename the final scientific estimand: a present-day versus historical primary claim must be chosen and documented before model outcomes.

Use ordinary accessible first-party sources, title/author matching and version histories. arXiv API metadata distinguishes published from updated; publication and note-creation timestamps must be interpreted according to source semantics. Do not bypass challenge-required 403 responses or copy dates from an uncertain bibliographic match. Missing history remains UNKNOWN. [E3]

## 5. What anonymization PASS means

The renderer excludes outer title/author/venue/score/ID fields, but preserves scientific text, embedded URLs and distinctive method names. The sampled abstracts contain explicit repository links. This is **metadata-suppressed presentation**, not guaranteed unrecognizability. The report accurately discloses this boundary. [R1,R3,R5,R6]

Preserve raw originals. Do not silently edit all abstracts. If an identity-suppressed variant is later needed, implement it as a separate declared representation with a change map; separate availability-link removal from alteration of substantive scientific content.

## 6. F1 materials are useful calibration inputs, not certified treatment banks

The manifest reports 24 calibration and 96 certification-candidate records, disjoint by unique seed and selected by deterministic route/topic/score/cost strata. Human labels remain absent. [R10]

Three limitations matter:

- Round-robin stratification is suitable for instrument calibration but is not a representative sample of the 1,018 k=8 seeds. Do not extrapolate an unweighted validity rate to that population.
- The package builder displays only `slots[:4]` per block. Auditing four pairs does not certify all eight or twelve pairs in a larger later treatment bank. Record exactly which paper pairs were reviewed.
- Generic BUILD/DIAGNOSE/MEASURE/EXPLAIN descriptions are not already seed-local, scientifically admissible alternatives. Reviewers must assess their applicability and mixedness; do not invent an entirely new route taxonomy to force agreement. [R3]

Recommended F1 process:

A. **Seed audit:** source-faithfulness, generic-term masking, solution prescription, duplication and comprehensibility. Reviewer can access focal context for leakage checking; keep a separate blinded relevance/route assignment task.
B. **Paper audit:** each seed-paper pair gets direct relevance/transfer-only/off-topic/unclear, source-supported route labels (including secondary routes), and source spans. Hide current route labels, ranking scores and matching success to reduce confirmation bias.
C. **Block audit:** both routes' plausibility and relation (alternative/complementary/hierarchical/unclear), pair relevance balance and usable reviewed slots. Randomize displayed A/B orientation and map back.

Use a development calibration then freeze the rubric before beginning the 96-record candidate queue. If query or source rules change, retain original IDs/artifacts and rebuild versioned candidates rather than quietly replacing inconvenient cases. Human fields remain blank unless actual humans supplied them; automated suggestions require explicit non-human provenance.

A small deterministic shadow sample of source-gate-blocked and zero-match cases should be prepared to audit false exclusion. It is not authority to un-block them or enlarge a scientific treatment effect.

## 7. Concrete next-stage decision

**Engineering/source scoring: accept the checkpoint with disclosed limitations.**
**F1 calibration and source-only repair: proceed.**
**96-record final certification: defer until calibration rubric and reviewed scope are frozen.**
**P0/ARS/scientific proposal generation: not authorized.**
**Historical-clean claim: not established.**

Do not repeat whole-corpus acquisition or 790,000 pair scores merely to show progress. Start with 24 calibration records, at most 192 current seed-paper exposures before deduplication. Reuse unchanged embedding/score caches. Query/label repairs are developmental, logged and evaluated using source judgments, not hypothetical model outcomes. The 96 candidates are a review queue, not a required number of accepted samples.

## 8. Paper strategy after the change to CCF-B targets

Two viable questions share this work:

- A retrieval/evaluation paper asks whether high ranking scores and pairwise score balance correspond to genuine scientific-task compatibility and approach coverage. It requires validated judgments, multiple retrieval baselines, held-out queries and substantive findings. This checkpoint plus two suspicious examples is not yet such a finding.
- The original generation study additionally requires source-admissible alternative-route blocks and actual controlled model outputs. Do not pay for that experiment before validating the measurement instrument.

If calibration shows useful retrieval judgments but few clean competing routes, that may favor the first paper form rather than killing the data project. No venue ranking, deadline update or submission decision is made here.

## 9. Reproducibility qualification

The inference provenance openly records execution beginning before the implementation checkpoint commit. Per-file hashes are helpful provenance but do not retroactively constitute a prospective commit freeze. Preserve this fact. For later confirmatory execution, commit immutable source/config/code before launch and hash the manifest. The current result remains a developmental source-scoring run. [R11]

## References and inspected evidence

All repository paths below are relative to the pinned experiment commit at:
https://github.com/whzy3185/iclr/tree/e0fbbf27bae69030e9487fdf1958a27e84a18335/experiments/idea_collapse/f0_semantic_temporal

R1. F0_SEMANTIC_TEMPORAL_RESULT.md
R2. config.json
R3. scripts/build_bank.py
R4. matching/coverage.json
R5. f1_package/F1_CALIBRATION_CANDIDATES.jsonl, record 1, block 345b55b6ef513c049c91d1e1
R6. Same file, record 24, block 03d24e1f3f0d2e26d3310901
R7. scripts/prepare_sources.py
R8. scripts/semantic_compute.py
R9. temporal/evidence_minus_seed_distribution.json
R10. f1_package/F1_PACKAGE_MANIFEST.json; FINAL_VERIFICATION.json
R11. semantic/inference_provenance.json; README.md

E1. BAAI, bge-reranker-base model card, raw unbounded logits and reference inference example:
https://huggingface.co/BAAI/bge-reranker-base
E2. BAAI, bge-base-en-v1.5 model card, task-dependent score threshold FAQ:
https://huggingface.co/BAAI/bge-base-en-v1.5/blob/main/README.md
E3. arXiv API User's Manual, bibliographic records and published/updated fields:
https://info.arxiv.org/help/api/user-manual.html

External documentation was used to check score/date semantics, not to certify the experimental labels. No unavailable source was used as proof of a completed step.
