# Round 52 — Identification, Measurement, and Recovery of the Interrupted F0

Date: 2026-09-08. Audience: research lead and Codex. Scope: the ICLR research-choice study, not a new topic search.

**Decision: KEEP the research question; MODIFY the identification and execution rules. F0 remains source-only. No research-proposal generation is authorized.**

This is one substantive audit round, not a declaration that the hypothesis is true. The executable examples accompanying this report are mathematical counterexamples, not LLM observations or a power calculation for the actual study.

## 1. New repository evidence

At the start of this review, main was `47376a2032630ead4b1d05fa41d14d8fcb0147e0`. A newer engineering marker exists at `codex/f0-source-only-snapshot-api`, commit `5ee1a014e03f5f1dd2543c5c8de0b3ccd553e1c9`.

The marker's `experiments/idea_collapse/feasibility_1/CURRENT_SNAPSHOT.md` reports:

- 3,703/3,703 ICLR 2025 abstract pages cached locally;
- approximately 3,737/5,351 ICLR 2026 abstract pages cached locally;
- a local source-only script using provisional labels, TF-IDF retrieval, and a BM25-like reranker;
- an initial artifact set where an automatic leakage gate rejected every seed, preventing matching;
- a correction allowing extractable seeds awaiting human review into exploratory source matching, followed by interruption before corrected matching completed.

`STATUS.md` states the local source commit `e3eb75948dcd6745eb77f1def0ad0898cb1c839b` was not transferred and that the remote branch is a marker. These are **Codex's reported local facts**, not independently verified counts. The remotely inspectable F0 artifacts are the two marker documents, not the script, caches, matched-slot tables, or completed report. We have not rerun Codex's pipeline or tests.

The engineering snapshot started from `a36d1bb...`, before the v2 gate revision. Preserve this work and its caches; do not discard it or restart ingestion merely because branch names differ. First publish inspectable code/config/manifests, then reconcile to the current source-only contract.

Source records:
- [Snapshot](https://github.com/whzy3185/iclr/blob/5ee1a014e03f5f1dd2543c5c8de0b3ccd553e1c9/experiments/idea_collapse/feasibility_1/CURRENT_SNAPSHOT.md)
- [Status](https://github.com/whzy3185/iclr/blob/5ee1a014e03f5f1dd2543c5c8de0b3ccd553e1c9/experiments/idea_collapse/feasibility_1/STATUS.md)

## 2. Keep the ICLR object, not a stronger story than the evidence

The object remains the behavior of a frozen model under controlled literature packets. Si et al. establish scientific ideation as an evaluation setting; Spectrum Tuning studies distributional coverage and in-context steerability; MetaMuse already uses external stimuli for algorithmic ideation. These precedents do not establish our proposed matched-literature result, and they prevent generic context steering or ideation diversity from being our novelty claim. [S1–S3]

This round rechecked these close precedents and methodological sources. It was **not** an exhaustive update of all concurrent literature. Novelty remains provisional. Good experimental controls are necessary, but a collection of controls is not by itself a new scientific finding.

Neutral research question:

> Under a frozen, auditable scientific task, what changes in open-ended research-route choice are caused by assignment to different literature-packet policies, and what additional structure remains after accounting for ordinary nonlinear response geometry?

Use 'behavioral response model' rather than claiming an internal neural mechanism. Comparing two model families does not isolate the causal effect of a parametric prior: architecture, training, instruction following and knowledge differ too.

## 3. Major correction: baseline-dependent probability movement can be automatic

Earlier rounds proposed that a stronger baseline preference requiring more counter-direction evidence would identify resistance. That observation alone is insufficient.

Consider the explicitly hypothetical model

`p(A | b, alpha) = sigmoid(b + beta * (2*alpha - 1))`.

Set `beta = 1` for every baseline. There is no baseline-by-evidence interaction on the log-odds scale.

| b | Assumed no-context p(A) | p(A), alpha=0 | p(A), alpha=1 | Probability difference | Log-odds difference |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.5000 | 0.2689 | 0.7311 | 0.4621 | 2.0000 |
| 1 | 0.7311 | 0.5000 | 0.8808 | 0.3808 | 2.0000 |
| 2 | 0.8808 | 0.7311 | 0.9526 | 0.2215 | 2.0000 |

A plot of probability movement against baseline concentration looks like resistance even though every model has the same coefficient. Nonlinear interaction interpretation requires distinguishing scales. [S4]

The zero crossing is also algebraically constrained:

`alpha_star = 1/2 - b/(2*beta)`.

Its dependence on b is not independent evidence for a new mechanism. With a context-presence intercept c, replace b with b+c. Values outside [0,1] mean no crossing in the tested range; do not extrapolate a threshold or clip it into range.

### Revised model-comparison contract

Keep no-context distinct from a 50:50 packet: the latter adds information, length and examples. Do not assume equal distributions.

Compare pre-specified models, initially within family and route contrast:

1. baseline plus a context-presence term;
2. baseline plus context presence plus a common evidence-mixture slope;
3. the previous model plus baseline-by-mixture interaction and/or a limited pre-specified nonlinear term.

For example, an A/B log-ratio component can use latent baseline b, a context intercept, seed/contrast structure, mixture z=2*alpha-1, and an optional b*z term. The baseline counts must contribute a measurement model or an uncertainty analysis; b is not an error-free observed covariate.

Estimate the full outcome distribution, not only the A/B conditional subset. Assess whether the richer model improves held-out seed prediction and calibrated uncertainty beyond the additive nonlinear comparator. A probability-scale interaction is a valid descriptive estimand, but is not automatically evidence for a special 'prior resistance' mechanism.

Counterexample code: `design_checks/round52/design_counterexamples.py`. It has no model calls or research data.

## 4. Major correction: do not remove post-treatment copying or invalidity

Previous anti-priming proposals included excluding outputs that copy a supplied method. Copying can itself be changed by the evidence treatment. Conditioning on it can destroy the randomized comparison. Post-treatment filtering is a recognized source of experimental bias. [S5]

Exact toy example, not data:

- Both treatment arms originally contain 50 A outputs and 50 B outputs: true full-sample A difference is zero.
- In arm 0, remove 5 A and 25 B outputs as copies: retained A proportion is 45/70 = 0.6429.
- In arm 1, remove 25 A and 5 B outputs as copies: retained A proportion is 25/70 = 0.3571.
- The filtered contrast becomes -0.2857 solely because of selection.

### Revised rule

Preserve every scheduled request and every returned output. Source-level exclusions decided before assignment remain allowed. Do not remove returned outputs based on copying, citation uptake, scientific quality, route clarity, or agreement with the desired effect in the primary analysis.

Measure copying as an additional outcome. A predeclared joint event such as 'A route AND not a direct copy' may be estimated on the full denominator; it is not the same as conditioning on non-copying. A filtered analysis, if reported, is descriptive and cannot by itself identify a direct effect independent of copying.

For a mechanism test, intervene on the input representation on a predeclared subset and preserve its outputs. This estimates an input-transformation effect; it does not identify mediation through copying without further assumptions.

## 5. Preserve the outcome vector before compressing to a score

The -2 to +2 ordinal score assumes a common ordered continuum and comparable spacing. MIXED is not the same as NEITHER; neither is the same as INVALID. Refusing or failing to answer is not a neutral scientific preference.

Recommended raw measurement:

`route_class = A | B | MIXED | NEITHER | UNASSESSABLE`

with separate fields for substantive validity, parse status, transport status, copying, and annotation uncertainty. In the full response distribution, failed substantive outputs receive an explicit INVALID category; unresolved assessment remains visible rather than silently imputed.

Report at least the full vector:

`p(alpha) = (p_A, p_B, p_MIXED, p_NEITHER, p_INVALID)`

plus unresolved-label and transport-missing counts. Parser failure alone is not scientific invalidity: a coherent unstructured response can be manually annotated.

A pre-specified directional summary remains useful:

`D(alpha) = p_A(alpha) - p_B(alpha)`

`Delta_D = D(1) - D(0)`.

This is a bounded probability contrast, not an interval-scale human score. It must be presented alongside its component probabilities. A shift from (A=.4,B=.4,MIXED=.2) to (A=.1,B=.1,MIXED=.8) has Delta_D=0 but a large change in composition. The companion script verifies this counterexample.

Use ordinal intensity secondarily if F1 validates that construct. Never infer 'no evidence influence' from a single near-zero compressed metric.

### Missing outputs and denominators

Keep scheduled, attempted, returned, annotated and unresolved counts distinct. Transport failure is not a model's scientific choice. A deterministic outcome-independent retry policy is permitted, with all attempts preserved. For missing outcomes, report sensitivity bounds as well as completed-response summaries; do not silently assume missingness is random.

For the directional variable g in {-1,0,+1}, a schedule with n attempts, n_miss unresolved outputs, and observed sum T has worst-case mean bounds `(T-n_miss)/n` to `(T+n_miss)/n`. These are conservative missingness bounds, not confidence intervals. Statistical uncertainty is additional.

## 6. Identify a packet-policy effect; do not overclaim a pure route-label effect

Let s denote a unique seed, r a route contrast, m a frozen model, and Pi_sr,alpha a pre-specified distribution over matched packets. The experiment targets

`E_C~Pi_sr,alpha E_Y~M(.|s,C) [g(Y)]`.

Randomized packet assignment identifies the effect of the packet policy under the design assumptions. A/B papers necessarily differ in findings, methods and other semantic content. Matching observed covariates does not make the abstract route label the only changing property.

Therefore the primary claim is about controlled literature composition under the audited policy, not 'the isolated causal effect of scientific route independent of all semantic content'. Multiple slot banks, within-route swaps and transferred prediction strengthen that interpretation but do not prove away all unmeasured content differences.

Relevance matching needs substantive validation, not just rank proximity. Matching guidance emphasizes covariate choice, overlap and balance; it does not provide universal cosine calipers for scientific documents. [S6]

### Change the role of full-abstract embeddings

Full-abstract similarity contains both nuisance topic information and the intended route/method contrast. A universal stringent full-abstract cosine caliper may remove the treatment contrast or select unusual, route-ambiguous papers. This is a design concern specific to our treatment, not a claim that all embedding matching is biased.

Keep three feature roles separate:

- task relevance and problem compatibility: source-derived problem description, seed compatibility, explicit human audit;
- nuisance variables: token length, public-date evidence, source formatting;
- intended contrast: route objective, approach and finding structure.

Use full-abstract embedding distance initially as a diagnostic. Any problem-only representation must itself be audited; merely rewriting text with an LLM does not guarantee the intended contrast was preserved.

Top-200 rank is a retrieval budget, not proof of absolute relevance. Two equally low-quality candidates can match perfectly. Sample candidates across rank strata and rejected boundaries for F1, not only successful matches.

## 7. Repair F0 statuses instead of choosing looser gates blindly

The all-seed rejection in the reported snapshot is evidence of an operational problem, not of corpus impossibility. We still need the script to determine its exact cause.

Separate these objects in code:

- `extractable`: actual source text permits a candidate problem statement;
- `risk_flags[]`: possible solution leakage, ambiguity, excessive breadth;
- `source_matching_allowed`: exploratory source audit is permitted;
- `confirmatory_eligible`: all later required reviews are complete.

A nonempty, source-derived seed with a lexical-similarity warning may enter provisional matching while retaining its warning and `confirmatory_eligible=false`. A seed explicitly encoding the proposed solution must be repaired before entering the primary candidate analysis; it can remain in a diagnostic ledger. Missing source text, ID corruption and focal-paper self-inclusion are hard structural failures.

Do not treat expected shared problem vocabulary as conclusive method leakage. Conversely, do not turn all warning flags off to recover counts. Publish each heuristic, the triggered spans, and a deterministic audit sample of both flagged and unflagged items.

### Retrieval and annotation provenance

The snapshot reports TF-IDF and BM25-like scores. These can support an inexpensive provisional lexical screen, but are not dense semantic retrieval and are not independent expert relevance validation. Record `LEXICAL_PROVISIONAL` if used. Missing dense/reranker scores stay null, not zero and not renamed lexical scores.

A heuristic or model's self-reported purity/confidence is not a calibrated probability. Retain qualitative evidence spans and annotation provenance. Emit unavailable purity-grid cells as `NOT_ASSESSED`; do not invent decimal purity to fill the grid.

### Matching implementation needs a precise objective

To estimate maximum feasible slot count, solve lexicographically:

1. maximize the number of admissible disjoint A/B pairs;
2. minimize the matching cost among maximum-cardinality solutions;
3. apply deterministic tie-breaking.

Unconstrained minimum cost selects the empty matching when every edge has positive cost. Greedy lowest-cost pairing can understate feasibility: edges A0-B0=1, A0-B1=2, A1-B0=2 give greedy cardinality 1 but optimum cardinality 2. The companion script is an exact tiny test fixture, not a scalable matcher.

Distinguish `measured_zero`, `not_run`, `blocked`, `missing_covariates` and `pending_review`. Only a measured result may become zero in a coverage table.

## 8. Normalization failure is not automatically proof of lexical priming

Deleting method or limitation text also changes information content and may remove precisely the scientific evidence responsible for the effect. Before interpreting attenuation, F1 must audit both relevance and preservation of the intended contrast.

The low-cost representation study should begin with original anonymous abstracts versus a source-faithful format-normalized version. Component deletion (P/F/M/L) is a later information-ablation study, not an automatically clean lexical control. It needs its own length/information accounting and paired source mapping.

Do not assert a universal hierarchy from citation frequency to method choice: those measures have different opportunity counts, ranges and annotation difficulty. Audit each separately and compare calibrated effects or discriminability, not raw bars that manufacture an attenuation gradient.

A model may also react rationally against a literature route because the sources show saturation or a failed approach. Route proportion is not evidence truth strength, and alpha is not a target probability the model ought to match. Preserve negative, flat and nonlinear slopes. Interpret failure only against a pre-specified scientific claim, not because the desired positive slope is absent.

## 9. Development and confirmation: flexibility must be labeled, not forbidden

Round 51 correctly separates source exploration from confirmation, but its blanket prohibition on learning hypotheses from a pilot is too strong. Exploratory discovery followed by a new independent confirmatory study is legitimate; hiding that transition is not. [S7]

Proposed partition by **unique focal seed** before proposal generation:

- D: development/engineering/annotation pilot;
- C: confirmatory controlled-packet study;
- N: held-out natural-retrieval validation.

All contrasts of the same seed remain in one partition. Also record source-paper reuse across partitions; seed holdout and source-neighborhood holdout are different generalization claims. Exact partition sizes wait for source feasibility and precision analysis.

D may reveal parser, prompt or rubric failures and suggest new hypotheses. Record what was seen, version the design, and use new C data for confirmation. No D outcomes become part of an allegedly untouched confirmatory test. Within C, blocks cannot be selected by effects. Integrity prohibits pretending exploration was confirmation; it does not prohibit scientific learning.

A blinded nuisance-variance pilot is an option, not guaranteed by hiding a condition column: route-rich text can reveal the treatment. Record who could see which outputs. Do not claim double blinding unless implemented.

## 10. Effect thresholds and stopping: remove two remaining ambiguities

The smallest scientifically meaningful effect and the minimum detectable effect are different. Human interpretation and the scientific question justify delta; variance and resources determine whether the study can estimate it. Do not widen delta after a noisy pilot merely to obtain an easy equivalence conclusion.

For the first confirmatory study, prefer a fixed number of independent seeds and frozen replicate allocation. A predeclared rule that repeatedly recomputes ordinary confidence intervals and stops when width is small is not automatically anytime-valid. Adaptive stopping requires a method justified for that design, such as an appropriate confidence sequence; it is not made valid merely by being written in advance. [S8]

Do not mix frequentist confidence intervals with posterior ROPE probabilities. Recommended default: report 95% confidence intervals; if equivalence is a declared goal, use two one-sided tests with predeclared bounds and family/error policy. At alpha=.05, TOST corresponds to a 90% CI entirely within the bounds. Using a 95% interval is more conservative, but 'mostly inside' is not a formal decision rule. [S9]

Predeclare a small claim family: directional policy effect first; richer baseline-response modeling second. Correct or hierarchically structure multiple confirmatory tests. Treat unplanned abstraction, subgroup and representation findings as exploratory until independently checked.

## 11. Replication units and natural-RAG prediction

The independent replication target is the unique scientific seed, not each generated proposal and not automatically each seed-route block. Several route contrasts for one seed are correlated. Weight seeds explicitly so seeds with many eligible contrasts do not dominate the average.

Report variability by seed, slot bank, assignment, decoding replicate and annotator. Use a hierarchical or design-aware uncertainty analysis checked under simulation; never bootstrap pairwise similarity rows as independent data. If sources are heavily reused, add source-reuse diagnostics and state whether inference is conditional on that fixed source bank.

For N, compare baseline-only, baseline plus context presence, composition-only, additive baseline-plus-composition, and the predeclared interaction model. Fit on D/C training partitions only as allowed and freeze before N outcomes. Natural packets may contain other routes: record the full composition and out-of-support cases instead of renormalizing everything into A/B.

Natural-RAG failure limits transportability. It does not erase a valid controlled policy effect. A successful model-prediction test does not forecast human scientific progress.

## 12. Concrete next execution, without expanding the project

The immediate Codex task is **F0 recovery and evidence publication**, detailed in `CODEX_F0_RECOVERY_TASK.md`:

1. preserve the interrupted local branch and caches;
2. publish script/config/manifests so code can actually be reviewed;
3. separate structural errors from review warnings;
4. test maximum-cardinality matching and missingness semantics;
5. publish source-only frontier tables and a deterministic human audit sample;
6. stop before any proposal generation.

Do not implement multinomial model fitting, post-training, a new retriever, a neural-mechanism study, or every ablation during recovery. The analysis corrections here are D0/D1 requirements, not new prerequisites for downloading abstracts.

Review outcomes are: REPAIR_PIPELINE, PREPARE_F1, REVISE_SOURCE_DESIGN, or REQUEST_MISSING_ARTIFACTS. None is an automatic paper verdict based on one count.

## 13. Verification performed this round

Executed locally:

`python design_counterexamples.py --test`

Six deterministic tests passed, covering identical logit effects, unsupported zero crossings, post-treatment selection, scalar-outcome compression, matching cardinality, and exact quarter mixtures. The script also emitted `design_counterexamples.json`.

No LLM/API calls, no real proposal outcomes, and no F0 corpus computations were performed in these checks. They establish mathematical/implementation counterexamples only. They do not validate an estimator's actual false-positive rate, power, or the Codex implementation.

## 14. Source ledger and search stop

Accessed 2026-09-08. Original papers/official proceedings only for substantive claims.

- **S1** Si, Yang and Hashimoto. *Can LLMs Generate Novel Research Ideas?* ICLR 2025. Official abstract: https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html . Supports ideation setting and diversity/evaluation limitations, not our causal result.
- **S2** Sorensen et al. *Spectrum Tuning: Post-Training for Distributional Coverage and In-Context Steerability*. ICLR 2026. https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html . Supports the nearest distributional-steerability boundary.
- **S3** Ma et al. *MetaMuse: Algorithm Generation via Creative Ideation*. ICLR 2026. https://proceedings.iclr.cc/paper_files/paper/2026/hash/85632be2cd69e9a0ef4ba054c096fac9-Abstract-Conference.html . Supports external-stimulus ideation precedent.
- **S4** Norton, Wang and Ai. *Computing Interaction Effects and Standard Errors in Logit and Probit Models*. Stata Journal 4(2), 154–167, 2004. https://doi.org/10.1177/1536867X0400400206 . Publisher abstract verified; our numerical example is independently derived.
- **S5** Montgomery, Nyhan and Torres. *How Conditioning on Posttreatment Variables Can Ruin Your Experiment and What to Do about It*. AJPS 62, 760–775, 2018. https://doi.org/10.1111/ajps.12357 . Publisher abstract explicitly includes elimination/subsetting after treatment.
- **S6** Stuart. *Matching Methods for Causal Inference: A Review and a Look Forward*. Statistical Science 25(1), 1–21, 2010. https://doi.org/10.1214/09-STS313 ; https://arxiv.org/abs/1010.5586 . Methodological guidance; not a validated document-matching threshold.
- **S7** Nosek et al. *The Preregistration Revolution*. PNAS 115, 2600–2606, 2018. https://doi.org/10.1073/pnas.1708274114 . Supports separating exploration, registered predictions and holdout confirmation.
- **S8** Howard et al. *Time-uniform, nonparametric, nonasymptotic confidence sequences*. Annals of Statistics 49(2), 1055–1080, 2021. https://arxiv.org/abs/1810.08240 ; https://doi.org/10.1214/20-AOS1991 . Supports time-uniform inference, not a ready-made implementation for our clustered design.
- **S9** Lakens. *Equivalence Tests: A Practical Primer for t Tests, Correlations, and Meta-Analyses*. SPPS 8(4), 355–362, 2017. https://doi.org/10.1177/1948550617697177 . Publisher text verifies TOST, equivalence bounds and the 90% CI relationship.

Search families: exact ICLR nearest titles; nonlinear logit interactions; post-treatment conditioning; matching balance; preregistration and held-out confirmation; equivalence tests; time-uniform confidence sequences. Stopped when the load-bearing design criticisms had primary support and executable counterexamples. Some PMC full-page opens returned a browser challenge; publisher/search records supplied the cited evidence. No unsupported inference of full-paper access is made.

## 15. Previous belief, update, and next decision

Previous belief: strict source gates plus baseline interaction, copy exclusion and response thresholds would be enough to protect the claim.

Update: strict gates can suppress all observations; bounded scales can manufacture apparent resistance; post-treatment exclusion can manufacture an effect; normalized text can remove the intended treatment. A planned analysis is not automatically a valid one.

Decision: continue the source-only program, replace automatic failure with typed evidence states, require a nonlinear comparator, preserve the outcome distribution, and separate development from confirmation.

Next decision requires an inspectable F0 code/data snapshot and human-audit material—not another imagined response curve.
