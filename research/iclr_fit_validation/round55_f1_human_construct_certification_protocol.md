# Research Round 55 — F1 Human Construct Certification Protocol

Date: 2026-09-08
Status: PRE-OUTCOME SOURCE/HUMAN DESIGN. No scientific proposal generation authorized.

## 1. Purpose

F0 can tell us whether large candidate multi-route source banks exist. It cannot certify that a masked seed is a genuinely open scientific problem or that two source-defined routes are both valid choices for that problem.

F1 is therefore a **human construct certification stage**, not a model experiment.

Goal:

> Convert the large semantic/source candidate space into a smaller, auditable bank of seed-route blocks that humans agree are understandable, route-neutral, scientifically plausible on both sides, distinguishable, and not trivially hierarchical.

No LLM research-proposal generation occurs in F1.

---

## 2. F1 has two phases

### F1-A — rubric calibration

Use a source-only stratified calibration sample.

The calibration sample intentionally spans:

- multiple subfields;
- R1–R4 where available;
- high/mid/low semantic relevance;
- easy and borderline seed leakage;
- high and low route purity;
- easy and difficult matched-slot cases;
- likely complementary/hierarchical route pairs.

Recommended order-of-magnitude: roughly 40–80 blocks, depending on reviewer bandwidth. This is a calibration resource, not a statistical sample-size claim.

During F1-A reviewers may:

- clarify rubric language;
- add examples/counterexamples;
- define categorical fatal flags;
- decide how to treat complementary but still meaningful route choices;
- determine operational certification thresholds.

They may **not** see any model treatment output because none exists.

At the end of F1-A freeze:

`F1_RUBRIC_V1.md`

`f1_rubric_version.json`

`f1_rubric_hash.txt`

After this freeze, certification criteria cannot be changed based on proposal-generation outcomes.

### F1-B — certification

Apply the frozen rubric to the remaining candidate blocks selected from the source-only F0 frame.

Every candidate retains a status/reason; no silent deletion.

---

## 3. Human review unit

Primary F1 unit:

`seed_id × route_pair_id`

Reviewer packet contains only source-side information:

- masked seed question;
- limited problem context if required;
- neutral route A description;
- neutral route B description;
- representative A source evidence;
- representative B source evidence;
- source IDs hidden behind anonymous IDs where practical;
- relevance summaries if included, shown symmetrically.

Do not show:

- focal paper method/solution;
- model outcomes;
- future treatment alpha;
- imagined effect sizes;
- paper-story labels such as "counter-prior".

---

## 4. Reviewer questions

Use both categorical flags and ordinal ratings.

### 4.1 Seed validity

`UNDERSTANDABLE_WITHOUT_FOCAL_SOLUTION`

`METHOD_NEUTRAL`

`MULTI_ROUTE_OPEN`

`NO_DISTINCTIVE_FOCAL_FINGERPRINT`

`TECHNICALLY_SUBSTANTIVE`

Fatal examples:

- the seed explicitly asks to design/build a new architecture when BUILD is one candidate route;
- the seed contains the focal method name/acronym;
- solving the problem requires information removed during masking;
- the seed is so broad that essentially any paper is relevant;
- the seed is so narrow that only one scientific action is plausible.

### 4.2 Route A/B relevance

Rate independently:

`A_RELEVANCE_TO_SEED`

`B_RELEVANCE_TO_SEED`

Reviewer question:

> Could work along this route reasonably and directly advance understanding or resolution of the masked scientific problem?

Do not equate lexical/topical similarity with scientific relevance.

### 4.3 Scientific plausibility

`A_SCIENTIFIC_PLAUSIBILITY`

`B_SCIENTIFIC_PLAUSIBILITY`

Question:

> Would a competent researcher plausibly choose this as the central route of a serious project addressing the seed?

This is not a judgment that A and B are equally likely to succeed.

### 4.4 Distinguishability

`DISTINGUISHABILITY`

Question:

> Can a future proposal meaningfully lean toward A versus B, or are the descriptions effectively the same scientific strategy?

### 4.5 Non-subsumption

`NON_SUBSUMPTION`

Question:

> Is one route merely a mandatory substep of the other rather than an alternative central research emphasis?

Example of likely failure:

- "build a new model" versus "evaluate the new model" when evaluation is only described as a routine validation step of BUILD.

Possible pass:

- "build a new long-context architecture" versus "construct a systematic diagnostic/evaluation study showing where current architectures fail" when either could independently be the central project.

### 4.6 Composability

`COMPOSABILITY`

High composability is not automatically fatal.

A proposal may validly be MIXED. The question is whether A and B remain distinguishable central emphases even if a sophisticated project could combine them.

### 4.7 Route dominance

Categorical:

`A_CLEARLY_MORE_JUSTIFIED`

`A_SOMEWHAT_MORE_JUSTIFIED`

`ROUGHLY_BALANCED`

`B_SOMEWHAT_MORE_JUSTIFIED`

`B_CLEARLY_MORE_JUSTIFIED`

`CANNOT_JUDGE`

Strong dominance is a warning for causal interpretation and may become a certification exclusion under the frozen rubric.

---

## 5. Reviewer assignment

Each certification block should receive at least two independent reviews.

Reviewer qualification:

- ML/AI research literacy sufficient to understand the seed;
- preferably subfield-aware for specialized blocks;
- no access to treatment outcomes;
- no instruction to maximize the number of passing blocks.

Material disagreements go to an adjudicator.

Do not average away categorical fatal disagreements automatically.

Example:

- reviewer 1: route B scientifically implausible;
- reviewer 2: route B strongly plausible.

This block requires adjudication, not a mean score of 3.

---

## 6. Reliability reporting

Report separately:

- raw agreement on fatal flags;
- agreement on A/B route dominance;
- ordinal reliability for relevance/plausibility/distinguishability;
- disagreement rate requiring adjudication;
- reliability by route pair and subfield.

Do not collapse all dimensions into one kappa score.

If one route contrast is consistently hard for humans to distinguish, that is evidence about the construct and may justify dropping that contrast before model outcomes.

---

## 7. Certification statuses

Every block receives one final source/human status:

`CERTIFIED`

`FAIL_SEED_LEAKAGE`

`FAIL_SEED_NOT_OPEN`

`FAIL_A_RELEVANCE`

`FAIL_B_RELEVANCE`

`FAIL_A_PLAUSIBILITY`

`FAIL_B_PLAUSIBILITY`

`FAIL_ROUTE_INDISTINGUISHABLE`

`FAIL_HIERARCHICAL_SUBSUMPTION`

`FAIL_ROUTE_DOMINANCE`

`FAIL_INSUFFICIENT_MATCHED_EVIDENCE`

`UNRESOLVED_REVIEW_DISAGREEMENT`

`OTHER_SOURCE_VALIDITY_FAILURE`

Multiple reason codes may be retained in a secondary field even if one primary status is used.

---

## 8. Source-bank certification after human review

A block is not experiment-ready merely because its seed/routes pass human review.

After F1 human certification, recompute/verify the matched evidence bank using the final source-only matching regime selected at D0.

Required checks:

- both route pools remain semantically relevant;
- pairwise slots exist at final k;
- matching nuisance differences are acceptable under the frozen source-only rule;
- packet assignment does not create major token/relevance/date imbalance;
- source identity metadata can be removed cleanly;
- focal paper is absent from the evidence bank.

Only then label:

`TREATMENT_BANK_CERTIFIED`.

---

## 9. D0 pre-outcome design freeze

After F1-B and before any proposal generation, freeze:

- certified seed-route bank;
- final temporal tier;
- final packet k;
- route roster actually represented;
- matching regime/config/hash;
- matched slot banks;
- packet assignment schedule;
- source anonymization rules;
- generator prompt template;
- human outcome rubric draft;
- seed-level D/C/N split;
- model families eligible for P0.

Create a manifest/hash so later changes are deviations rather than silent replacements.

---

## 10. D/C/N split

Split **unique seeds**, not generations or route blocks.

All route pairs for one seed remain together.

### D — development

Used for P0 engineering/variance pilot and later prompt/annotation debugging.

After any scientific generation occurs on a D seed, it is permanently excluded from C/N confirmatory use.

### C — controlled confirmatory

Used only after D1 confirmatory freeze.

### N — natural-retrieval holdout

Reserved for final out-of-sample ordinary-RAG prediction.

Do not inspect N natural-RAG proposal outcomes while fitting the controlled response model.

Exact proportions depend on certified-bank size and are frozen at D0.

Stratify where possible on:

- subfield;
- route pair;
- semantic relevance regime;
- source-bank size.

---

## 11. Outcome-label rubric preparation

F1 defines the conceptual categories for future model outputs:

`A_LEANING`

`B_LEANING`

`MIXED`

`NEITHER`

`INVALID`

But actual reliability on model-generated proposals can only be measured during D/P0.

Therefore do not declare the output-label instrument validated merely because source routes are human-certified.

P0 must separately test whether humans can classify real generated proposals reliably.

---

## 12. What F1 can and cannot conclude

### F1 can conclude

- humans can or cannot construct a reliable multi-route scientific-choice object;
- which route contrasts are naturally supported;
- how much the F0 candidate bank shrinks under human validity requirements;
- whether final treatment banks can be frozen without model outcomes.

### F1 cannot conclude

- literature changes model research choice;
- one route is easier to steer toward;
- baseline propensity predicts response;
- model family differences;
- paper-level effect significance.

---

## 13. F1 success pattern

Strong F1 does not require thousands of certified seeds.

What matters is a sufficiently broad and reliable bank to support seed-level confirmatory inference after P0 precision planning.

Desired qualitative pattern:

- multiple subfields survive;
- at least two route contrasts survive;
- no single idiosyncratic seed family dominates;
- human fatal-flag agreement is high enough to make certification auditable;
- route dominance/subsumption does not eliminate most blocks;
- final matched source banks remain sufficiently relevant and balanced.

No arbitrary count is an automatic paper verdict at this stage.

---

## 14. F1 failure pattern

Major redesign/kill if source-only human review shows that:

- most masked seeds prescribe a route;
- one side of candidate contrasts is routinely scientifically weaker;
- humans cannot distinguish the intended route alternatives;
- valid route pairs are mostly hierarchical rather than alternative central strategies;
- semantic matching requires obviously off-topic evidence;
- a usable bank exists only by hand-picking a tiny unrepresentative set.

This is the correct place to discover such failure, before model generations create incentives to rescue the story.

---

## 15. Recommended artifacts

Create under:

`experiments/idea_collapse/f1_construct/`

Suggested files:

`F1_RUBRIC_V1.md`

`f1_rubric_version.json`

`calibration_sample.csv`

`calibration_reviews.csv`

`certification_frame.csv`

`certification_reviews_blinded.csv`

`adjudication_log.csv`

`certified_blocks.csv`

`f1_attrition_waterfall.csv`

`f1_reliability_report.md`

`TREATMENT_BANK_MANIFEST.json`

`D0_FREEZE.md`

`D0_HASH.txt`

No model proposal outputs belong in this directory.

---

## 16. Decision

F1 should be the next scientific-validity stage after F0 semantic/date completion.

The core principle is:

> **Use humans to certify that the intervention really represents multiple valid scientific choices before asking whether an LLM changes its choice.**

This is more important for the eventual paper than increasing the number of provisional lexical matches.