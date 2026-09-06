# TASK 0 - Specification and Repository Audit

Audit date: 2026-09-06. Role: experimental engineer and reproducibility guardian.
Audited upstream commit: `f8f1afb681924e8d444c63740b7ef5f86902eeeb`.
Scientific runs performed: **0**. New primary metrics introduced: **0**.

## Addendum: Research-Lead Updates During Execution

Before closing the checkpoint, `main` advanced to
`93ebaf74f6d155b017c372211ca6b3078d828b3d`. Both new files were read in full:
`research/round4_web_experiment_design.md` and
`experiments/idea_collapse/PRE_RUN_AMENDMENT_A.md`. They were merged without
editing the lead's text. No scientific output existed before this amendment.

Amendment A requires per-source score/year/ID, source-set mean/median score,
context token count, and optional topic/cluster and citation/popularity proxies.
Trace schema v2 adds these fields, retains missing optional values as null, and
labels unmeasured mock token counts unavailable. C0 has zero context tokens.
Scientific analysis must reject missing measured context-token provenance.
Legacy v1 mock evidence remains intact and is not backfilled with invented data.

The lead explicitly retains top-k/MMR as E0. Accordingly **S1 below is now a
design/interpretation warning, not a demand to replace E0 or a standalone reason
to block it**. The query-paraphrase schedule still needs freezing, but Codex
will not invent stochastic MMR or move dose-response experiments into the pilot.
E0 is insufficient for the final retrieval-causality claim. E1's matched-overlap
intervention remains behind the user's post-pilot hard gate; this amendment is
not `Decision: CONTINUE`. MUSES remains out of pilot scope.

Round 4 supplies an updated lead-side collision scan. Its existence is recorded,
but this engineering audit does not certify every external source. S2/S3
scientific definitions/control schedules and S4 model/execution choices remain
unresolved, while S5 still lacks actual frozen abstract corpora.

## Authority and Existing State

Read, in order, `README.md`, `research/round3_assumption_breaking_analysis.md`,
`experiments/idea_collapse/README.md`, and `CODEX_WORKFLOW.md`.
The root README and workflow identify the experiment README as the canonical
pilot specification. The research rationale includes later-phase work, not
permission to execute it during this pilot.

The repository tracks only those four Markdown files. There is no existing
code, dependency manifest, corpus, generated output, tests, STATUS, PILOT_LOCK,
PILOT_RESULT, or DECISION. A fresh clone was used; this thread's older unrelated
research code and results are outside this checkout and will not be imported.

## Scientific Scope That Must Not Change

- Shared-Retrieval Research Monoculture, specifically retrieval exposure to
  population-level problem/method convergence beyond generator prior.
- H1 is retrieval concentration; H2 is idea concentration; **pilot H3 is the
  quality sanity check**, not the selection-pressure H3 in the broad rationale.
- Exactly 3 domains x 3 conditions x 2 model families x 30 runs = 540 ideas.
- Each run asks for one idea with the five canonical structured fields.
- No outcome-dependent filtering, prompt normalization, parameter selection,
  primary-metric substitution, or rescue of negative results.
- No selection/refinement/mechanism experiment or paper writing before the
  completed pilot is committed and a research-lead-authored CONTINUE decision
  subsequently authorizes the next scope. Codex must not author that decision.

## Requirement-to-Implementation Map

| Canonical requirement | Implementation target | Required artifact/test |
| --- | --- | --- |
| 3 specified domains; ICLR 2024-2026 | `configs/pilot.json`, `corpus/build_corpus.py` | validated year/ID/title/abstract/domain provenance; duplicate rejection |
| 200-500 relevant records per domain where feasible | corpus validation and acquisition manifest | exact counts and documented taxonomy; report shortage, never pad |
| Immutable source tables | `generation/provenance.py`, corpus builder | raw-byte SHA256, exclusive output creation, source metadata |
| C0 has no literature | generation prompt/context construction | test zero retrieved entries and no injected abstracts |
| C1 cosine dense retrieval, k=12 | `retrieval/dense.py` | normalized vectors, deterministic ties, exact IDs/scores/ranks |
| C2 same corpus/encoder, MMR | `retrieval/mmr.py` | exact same candidate matrix; explicit lambda and relevance floor |
| Query paraphrase control | frozen query schedule in config | identical construction across arms; record actual query/hash |
| Generation prompt paraphrase subset | prompt versions and paired design manifest | predefined subset; no paraphrase chosen from downstream outcomes |
| Matched C1/C2 count and context-token budget | context serialization and tokenizer-aware packing | no silent overflow/truncation; per-model token accounting |
| Two exact model families/versions | minimal `generation/providers.py` interface | family, provider, requested/resolved model, settings, version evidence |
| Identical generation settings within family | config validation | condition-specific overrides rejected |
| All run provenance | provenance and `generation/schema.py` | commit, corpus/prompt/config/analysis hashes, seed, run ID, retriever |
| Raw outputs and failures retained | immutable per-run JSON, materialized JSONL | malformed/refused/provider-error outputs remain counted |
| Cache/resume without hidden regeneration | run ID from frozen inputs; exclusive writes | cached runs do not call provider; incomplete/failed run is not silently retried |
| H1: Jaccard, weighted overlap, coverage, HHI, Gini | `metrics/retrieval_overlap.py` | hand-checkable fixtures, full corpus denominator for Gini |
| H2: question and question+method cosine distances | `metrics/semantic_diversity.py` after representation freeze | distinct fields; zero/invalid vector handling; retained denominators |
| H2: cluster entropy/effective cluster count | semantic metrics with frozen clustering rule | thresholds/algorithm/version explicit, not fit to preferred effects |
| H2: four-field structural tuple | frozen parser schema/prompt/version and saved output | parsing is fallible; no silent model repair/rewrite |
| Exact/partial/predefined-neighbor collisions | `metrics/tuple_collision.py` | fixed normalization, field weights, neighborhood rule; missingness |
| Portfolio growth at N=5,10,20,30 | `metrics/portfolio_growth.py` | fixed order/permutation seed; no best-looking ordering |
| H3 feasibility/depth/grounding/falsifiability | separate frozen quality instrument | no sole same-family judge; quality measurement is not candidate selection |
| Per-domain/model C1-C2 contrasts | `analysis/pilot_analysis.py` | all 6 strata shown before pooled output; reversals retained |
| Effect sizes and bootstrap 95% CIs | `analysis/bootstrap.py` | resample runs, not pair rows; fixed bootstrap seed/count; undefined effects labeled |
| No scientific use of mocks/smoke | run-purpose enum, segregated directories, analysis guard | reject mixed mock/smoke/scientific datasets |
| Full design cannot be silently reduced | pilot manifest expected run grid | expected/attempted/success/parse-error/API-error/missing counts |
| Preregistration freeze | `runs/PILOT_LOCK.json` only after TASK 3 | hashes of scientific choices and complete run grid; immutable |
| Final artifacts | PILOT_RESULT, pilot_summary.json, metric tables, diagnostic plots | actual design, H1/H2/H3, limitations, negative evidence, deviations |
| Hard scientific gate | workflow/CLI scope allowlist | no TASK 5+ command, no automatic DECISION creation |
| Recent collision scan | acquisition/search log and lead adjudication | 30-60 day window, searched sources/coverage, unverified items visible |

## Minimal File/CLI Plan

Use standard-library Python 3.12 for TASK 1, with `unittest`. No agent
framework, database server, job scheduler, dashboard, or model SDK is needed.
Add numerical/encoder dependencies only when TASK 2's choices are fixed.

Planned CLI entry points, all invoked from repository root:

```sh
python3 -m unittest discover -s experiments/idea_collapse/tests -v
python3 -m experiments.idea_collapse.generation.run --config CONFIG --purpose mock --output-root OUTPUT
python3 -m experiments.idea_collapse.corpus.build_corpus --input NORMALIZED_JSONL --output NEW_SNAPSHOT --manifest NEW_MANIFEST
python3 -m experiments.idea_collapse.analysis.pilot_analysis --lock LOCK --traces TRACE_DIRECTORY
```

TASK 1 implements the offline/mock execution and corpus validation paths.
The final analysis CLI is an implementation target, not a claim that analysis
choices are already approved. Scientific execution must fail closed while
required scientific configuration is null/draft or PILOT_LOCK is absent.

## Config and Trace Contracts

JSON is chosen over YAML/TOML to avoid an unnecessary parser dependency.
Canonical serialization uses sorted keys, UTF-8, no non-finite numbers, and
explicit schema versions. Files used as inputs additionally retain raw-byte
hashes; canonical-object hashes do not replace raw-source hashes.

Config must carry: schema/run-purpose, design, domains, conditions, model
families/provider/model/revision/settings, corpus paths/hashes, generation
prompt paths/hashes, query and prompt-paraphrase schedules, retrieval encoder
and revision/k/MMR/floor, tokenizer/context-budget policy, analysis config,
tuple parser, quality instrument, bootstrap/growth/clustering rules, and any
external-call authorization/budget. Unresolved scientific fields remain null.

One immutable generation record contains: run ID, attempt timestamp, purpose,
domain/condition/seed, Git commit and clean-tree status, raw/canonical hashes,
provider/family/requested and resolved model version, version-evidence status,
generation settings, actual prompt and injected context, query, retriever
name/version/config, retrieved IDs/ranks/scores/abstracts, request hash, raw
response, parse status, parsed five fields, provider error status, and analysis
config/hash. No secret or authorization header is written to a trace.

Run IDs bind every outcome-affecting input, including commit and purpose.
Resuming the same ID reads the retained record; changed inputs create a new
ID rather than overwriting evidence. Provider/parse failures are terminal
records unless a separately recorded retry is explicitly authorized. A crash
leaves an explicit incomplete marker, not a fabricated success.

## Scientific Ambiguities and Blocking Decisions

### S1: Within-set versus between-run diversity - initial finding; see addendum

With a fixed corpus, query, encoder, deterministic tie rule, and lambda,
both top-k and MMR return the same set on every run. Both therefore have
between-run Jaccard 1 and coverage 12, even if MMR's set is internally diverse.
Generator seeds do not change this. This is a design identity, not an observed
P0 result. Do not add random source assignment or tune lambda to force H1.

The canonical spec calls for a query-paraphrase control but does not specify
its schedule or whether it is the main intervention versus an added subset.
Research lead must clarify the across-run exposure construction (including
whether/how a fixed paraphrase schedule is used in both arms). MMR remains the
required default; disjoint exposure cannot silently replace C2.

### S2: Measurement definitions - blocks scientific lock

Encoder/revision, clustering algorithm/thresholds, tuple parser and normalization,
partial/neighbor similarity rules, quality rubric, alternative representation,
and quality-collapse/effect decision thresholds are unspecified. These affect
the scientific estimands and must be frozen before downstream measurement.
No scalar acceptance score or significance threshold will be invented by Codex.
Rank-weighted Jaccard with weights 1/rank is a possible documented engineering
implementation of weighted overlap, not an additional primary metric.

### S3: Mandatory controls and gate interpretation - blocks scientific lock

Prompt-paraphrase robustness is mandatory but its sample subset is unspecified.
One-embedding-only evidence is a kill criterion, whereas an alternative encoder
appears later in TASK 7. The lead must resolve whether the pilot must run a
second representation or mark that criterion unresolved. Matched context-token
budget also needs a frozen packing policy; equal document count alone is not
equal model-token exposure.

The broader rationale requests selection/human checks in its continue criteria;
the canonical pilot defers them. Follow the canonical pilot for execution;
do not run selection or human studies to satisfy the broader rationale early.

### S4: Providers, exact models, and cost authorization - blocks live calls

No OPENAI_API_KEY, ANTHROPIC_API_KEY, HF_TOKEN, OPENAI_BASE_URL, or OLLAMA_HOST
is set in the current process (only presence checked; no secret values read).
No exact generator families, encoder, parser, quality model, external provider,
or approved budget is specified. Existing local MPS/CUDA availability does not
identify scientifically suitable models or authorize a paid substitute.
Offline code/mocks may proceed. No unpublished research content will be sent
to a configured external service merely because a credential later exists.

### S5: Corpus and recent related-work evidence - blocks full pilot readiness

No corpus is committed. The official proceedings root is reachable and lists
2024, 2025, 2026. This establishes an acquisition route, not sufficient domain
coverage. Accepted main-conference papers are the conservative provenance
scope; topic matching and any documented taxonomy expansion must be retained.
The previous turn's unrelated trace dataset cannot replace ICLR abstracts.
No new 30-60 day collision scan has been completed for this P0; source statements
in the rationale are research-lead material, not independently verified here.

## Costs and Hardware

Offline unit tests, corpus validation and mocks require no model API calls.
Corpus download uses public endpoints without uploading research content.
Embedding is a separate explicit local-model download/compute operation.
Live pilot requires 540 generations plus any preregistered paraphrase subset,
tuple extraction and cross-family quality measurement. Numeric cost is unknown
until exact models, tokens, and provider pricing are fixed; no estimate of zero
cost or unlimited quota is made. Mac CPU/MPS and the known 8 GB CUDA host are
available candidates, not a pooled-memory device or proof of model capacity.

## Acceptance Tests and Task Boundary

TASK 0 is complete when the audit and status are committed. No experiment has
run. TASK 1 can proceed for hashing, strict schemas, retained failures, cache,
mock traces, provider interfaces, source serialization and corpus validation.
TASK 2 can receive offline tooling, but cannot be labeled COMPLETE until actual
corpora and the intervention are frozen. TASK 3/4 cannot run with unresolved
scientific settings or mocked data. Missing specifications are not ordinary
code failures and cannot be resolved by silently changing the study.
