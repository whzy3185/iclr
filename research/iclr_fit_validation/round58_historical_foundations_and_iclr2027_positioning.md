# Round 58 — Historical foundations, paper identity, and ICLR 2027 submission audit

Date: 2026-09-20.
Status: literature/positioning/design audit, not an experimental result.
Execution authorization: unchanged. This document does not authorize scientific proposal generation, paid inference, or a new agent framework.

## 1. Scope and inspected repository state

The request for work from roughly ten years ago is interpreted primarily as 2014–2017, with a separate 1991–2012 foundation layer. Older examples are methodological exemplars, not evidence that the same effects occur in current LLMs.

At inspection, main was `40195c9a2e1579600bd368bfb7055be20462d024`; the completed abstract-corpus branch remained at `c5e4391f3af6f7ff67291352c632731d58350293`; the semantic/temporal task branch remained at `b57e83a6c85ce14d6d64b3e041709a2d14906a80`. The published corpus-completion checkpoint and the existing Round 54 design are the starting assets. No new corpus hash recomputation, model experiment, or human annotation was performed in this round. The separate LinearRAG branch was not treated as evidence for the scientific-choice hypothesis.

The completed abstract collection is infrastructure. Lexical matching counts are provisional construction measurements. Neither establishes semantically valid treatment blocks or a model-behavior effect. In particular, the earlier claim that lexical abundance rules out a shortage of valid scientific alternatives was too strong: semantic and construct validation could still substantially change coverage.

## 2. Executive decision and field identity

KEEP the research question, but classify the intended paper as **an empirical study of language-model behavior under controlled scientific-literature context**.

- Primary field: LLM evaluation and empirical understanding of context-conditioned generation.
- Secondary field: reliability of retrieval-augmented systems and scientific ideation.
- Application setting: AI-assisted ML research, using ICLR literature as the study population.
- Method: randomized assignment of frozen literature-packet policies, with construct validation and distributional outcomes.

Do not describe the current study as mechanistic interpretability: it does not yet intervene on internal representations or circuits. Do not describe it as causal representation learning: randomized inputs are a methodology, not a learned causal representation. Do not describe it as a new retrieval algorithm unless such an algorithm and its incremental benefit are actually established. ARS/Codex are research execution tools, not the scientific contribution.

A suitable working title is:

**How Retrieved Literature Shapes Scientific Research Choices in Language Models**

An equally safe pre-result title is:

**Same Question, Different Literature: A Controlled Study of LLM Research Choices**

The principal question should distinguish **content-sensitive adaptation** from **sensitivity to incidental framing**. A model changing its research route after receiving useful evidence is not, by itself, failing. Since A/B routes can both be legitimate, there is no general requirement that output route frequencies equal document frequencies or remain invariant to new evidence.

ICLR's published subject list includes language representation learning, datasets/benchmarks, causal reasoning, and general ML; the actual submission-form taxonomy must be checked before selecting an area. The reviewer guide does not require SOTA, but does require useful new knowledge and evidence supporting the claims. [P1, P3]

## 3. Historical foundations: what is already known

### 3.1 Examples can constrain creative generation

Jansson and Smith's *Design fixation* (1991) experimentally studied constraints imposed by example concepts. Smith, Ward and Schumacher's *Constraining effects of examples in a creative generation task* (1993) found example-feature conformity in three human experiments, including a condition instructing participants to differ from the examples. [H1, H2]

These are motivation and competing conceptual precedents. They do not establish identical cognitive mechanisms in language models. The correct 1993 DOI is `10.3758/BF03202751`; a neighboring DOI ending in `2752`, encountered through a later reference list, resolves to a different article and must not be used.

Kohn and Smith's *Collaborative fixation* (2011) is particularly relevant to the user's request for earlier work. Their three human brainstorming experiments distinguish quantity from the range of idea categories explored. Exposure to others' ideas can affect category breadth without reducing the number of ideas. [H3]

Implication for this project: count, embedding distance, route distribution, and scientific usefulness are different outcomes. More proposals do not by themselves imply broader exploration.

A recent direct conceptual neighbor is Oppenheimer and Patterson's *Thinking outside the box means thinking outside the search engine* (2025). The study randomizes internet access in an alternative-uses task with 244 participants and examines nominal-group diversity. Its individual-versus-collective result overlaps strongly with the project's original monoculture motivation. It does not test LLMs or scientific-paper route choice. [H4]

Therefore, neither examples influencing ideas nor individual assistance coinciding with reduced collective diversity should be claimed as newly discovered here.

### 3.2 Retrieval relevance versus diversity is an old objective

Carbonell and Goldstein's MMR paper (SIGIR 1998) and Kulesza and Taskar's DPP work (2012) are relevant precursors for nonredundant, high-quality subset selection. [R1, R2]

The proposed study can investigate the downstream consequences of source selection, but cannot claim to originate the relevance/diversity tradeoff. MMR and DPP belong in a retrieval-policy extension if one is pursued; neither is a substitute for the randomized matched-packet core. Do not add a novel retrieval objective merely to make the paper look algorithmic.

## 4. Target exemplars from approximately 2014–2017

### 4.1 Zhang et al., ICLR 2017 — main structural exemplar

*Understanding deep learning requires rethinking generalization* changes labels/input structure while preserving much of the experimental system. Random-label fitting challenges specific explanations of generalization; comparisons and theoretical analysis bound the interpretation. [E1]

What to borrow: write down a competing explanation and design an intervention that makes it distinguishable. Do not merely show another curve under another context.

For us: compare changes in scientific content with nuisance changes that preserve an audited proposition inventory. A striking figure is useful only when the reader understands what was held fixed and what alternative explanation it challenges.

What not to borrow: the fame of the paper, an assumed sample-size standard, or a claim that a behavioral result automatically supplies a complete theory. Their theorem is not a reason to append an unrelated theorem to our work.

### 4.2 Goodfellow et al., ICLR 2015 — explanation and prediction exemplar

*Explaining and Harnessing Adversarial Examples* develops a linear explanation as an alternative to earlier accounts and derives a practical perturbation procedure. [E2]

What to borrow: a useful explanation should predict behavior beyond the first observation.

For us: the existing common-slope nonlinear null must precede claims of baseline-dependent resistance. In `p=logistic(b+beta*x)`, a fixed beta can still produce smaller probability-scale changes when baseline probabilities saturate. An empirical interaction or threshold is not automatically a new mechanism. Additional structure should improve held-out prediction or survive a discriminating intervention.

### 4.3 Jia and Liang, EMNLP 2017 — input validity exemplar

*Adversarial Examples for Evaluating Reading Comprehension Systems* adds distractor text while preserving the correct answer. The first-page example and evaluation make the intended semantic invariant explicit. [E3]

What to borrow: explicitly state the invariant that makes an intervention interpretable.

What not to borrow: our A/B route replacement usually changes legitimate scientific information. Unlike an answer-preserving distractor, it need not leave the appropriate response unchanged. Calling every route shift an adversarial failure would therefore be unjustified.

This motivates a small, separately audited content-preserving presentation control, not relabeling the whole paper as an attack study.

### 4.4 Ribeiro et al., KDD 2016 — explanation validation exemplar

*Why Should I Trust You?* introduces local model-agnostic explanations and tests their usefulness, including human-facing evaluations. [E4]

What to borrow: validate the proposed explanatory instrument instead of relying on plausible verbal explanations. For this study, a model's self-reported reason for choosing a route is an outcome or hypothesis, not privileged access to its causal process.

### 4.5 Szegedy et al., ICLR 2014 — phenomenon and transfer exemplar

*Intriguing properties of neural networks* reports counterintuitive network behavior, including transferable adversarial perturbations. [E5]

What to borrow: distinguish a repeatable property from one cherry-picked example. Our equivalent replication dimensions are independent scientific seeds, packet banks, and frozen model families. The analogy does not make the proposed literature effect adversarial.

## 5. Bridge from the classics to the present project

Zhao et al., *Calibrate Before Use* (ICML 2021), investigates answer biases associated with prompts and examples, including order effects. Min et al., *Rethinking the Role of Demonstrations* (EMNLP 2022), shows on the studied classification/multiple-choice settings that demonstration format and distribution can matter substantially even when labels are randomized. These are direct reasons to separate source information from task/format cues; their results do not universally imply that semantics never matters. [B1, B2]

Si et al.'s ICLR 2025 human study establishes scientific ideation as a concrete evaluation setting and identifies diversity/self-evaluation issues. Spectrum Tuning (ICLR 2026) directly studies distributional coverage and in-context steerability. MetaMuse (ICLR 2026) uses external stimuli for algorithmic ideation. [B3–B5]

Our remaining potential increment is consequently narrower than 'context affects generation': validated scientific decision units, randomized matched literature policies, full route-distribution responses, and evidence that separates content use from incidental presentation effects. That is a proposed increment, not a certified novelty claim. A focused nearest-neighbor update is still required before submission; this round is not an exhaustive search of every concurrent preprint.

## 6. Experimental strategy: retain the core and add one discriminating contrast

### 6.1 Existing core, unchanged

Evidence: ICLR 2025. Seed candidates: ICLR 2026. The full 2024–2026 corpus remains a provenance-rich resource; collecting more years does not authorize mixing them into the primary study.

After source/construct review, form matched A/B evidence slots and randomize packet composition. Choose k using source validity, balance, and precision rather than model effect sizes. Equal per-document counts do not prove equal relevance, and matched observable covariates do not make the full scientific contents identical.

For outcome classes `A, B, MIXED, NEITHER, INVALID`, retain the full vector `p(alpha)`. The directional contrast remains:

`D(alpha) = P(A | alpha) - P(B | alpha)`

`Delta_content = D(1) - D(0)`

Technical failure, parsing failure, and unassessable annotation remain separately recorded; missing outcomes cannot silently disappear. The causal estimand concerns assignment to frozen packet policies, not an isolated abstract route label detached from the papers' contents.

### 6.2 Proposed compact diagnostic: content change versus presentation change

For a preregistered subset, cross the endpoint composition conditions with two presentation variants. Keep the RAW abstract arm as the ecological core.

A presentation-only variant is eligible only when an independent audit confirms the same substantive problem, findings, method assertions, and scope/limitations. Possible transformations include benign formatting/order and carefully checked non-substantive discourse edits. Do not delete scientific findings or methods and call the result semantically equivalent.

Estimate a within-content presentation contrast separately from `Delta_content`, with intervals and seed-level uncertainty. Do not introduce a ratio score with an unstable near-zero denominator.

Interpretations:

- A content response robust across presentations supports controlled evidence dependence, not automatically improved science.
- A presentation response at fixed audited scientific content identifies a candidate nuisance channel; its downstream cost still needs measurement.
- Both effects require reporting both rather than choosing the more dramatic story.
- Neither effect, with informative uncertainty and reliable measurement, limits the scope of evidence dependence; it is not proof that all retrieval is useless.

The existing PF/PFM/PFL content removals remain **information ablations**, not information-preserving controls. Their attenuation cannot by itself establish lexical priming. Direct-copy rate is a separate outcome, not a post-treatment exclusion criterion.

### 6.3 Sampling, annotation, and replication

Preserve development/confirmatory/natural-retrieval splits at unique-seed level; all route pairs for one seed remain in the same split. Track shared evidence across seeds and use bank-level sensitivity analyses when reuse is substantial. Generations improve conditional estimates but do not create independent scientific problems.

Use source-only calibration to define admissibility and annotation rules. Do not require A/B to be psychologically or scientifically identical: require both to be viable, distinguishable responses to the same problem, while recording dominance/composability concerns.

If automated judges are used, identify them as automated judges. Repeated isolated calls to one model are not independent human experts. Validate route labels against an independently checked sample; keep treatment/model metadata hidden from the route-labeling interface.

Development observations can generate hypotheses, but these must be labeled exploratory and tested on protected data. The formal analysis plan, effect interpretation, and stopping rule are frozen before confirmatory outcomes. The number of seeds is a precision choice, not an ICLR acceptance threshold.

### 6.4 Natural retrieval and interventions

Held-out natural-RAG prediction is an external-validity extension, not mandatory proof of the controlled estimand. Its failure narrows the claim. A minimal presentation or retrieval intervention is worth adding only if a diagnosed problem suggests it and evaluation remains held out. A generic diversity-aware retriever or a complex ARS agent is not automatically a contribution.

## 7. Paper presentation

The paper should read as **question → competing explanations → experimental object → controlled results → discriminating tests → scope**, not as a data-pipeline manual.

Suggested initial-submission page budget, totaling nine pages:

| Section | Pages | Purpose |
|---|---:|---|
| Introduction | 1.0 | Concrete question and actual finding, once known |
| Related work and competing explanations | 0.75 | Historical roots plus nearest technical neighbors |
| Scientific choice units and source validity | 1.5 | Seeds, routes, provenance, temporal and relevance audits |
| Experimental design and estimands | 1.5 | Randomization, models, annotation, inference |
| Main distributional results | 1.5 | Full categories, seed/model variation, effect intervals |
| Content/presentation and alternative explanations | 1.5 | Discriminating controls, copying/quality outcomes |
| Held-out natural retrieval, if conducted | 0.75 | Transfer with frozen predictors, including negative result |
| Limitations and conclusion | 0.5 | Precisely bounded generalization |

If natural retrieval is not part of the final claim, reallocate its space rather than inserting an unperformed experiment.

Figure 1 should show one understandable seed, the manipulated packet policy, and measured response distribution—not the entire agent architecture. Figure 2 should expose full outcome mass and heterogeneity. Figure 3 should compare competing explanations. Figure 4 can present transfer or a narrow validated intervention. Counts/hashes/complete prompts and extended audit tables largely belong in the appendix, while essential identification and measurement validity belong in the main text.

Do not put a fabricated result in a preview figure. Infrastructure completeness, a large candidate bank, a significant p-value, or a nice title alone does not establish a publishable finding.

## 8. ICLR 2027 submission audit

Official sources checked on 2026-09-20: CFP, Dates, Author Guidelines, Reviewer Guidelines, author AI policy, and the September 2 policy blog. [P1–P6]

### Dates and eligibility

The abstract deadline is September 18, 2026, 23:59 AoE; the paper deadline is September 25, 2026, 23:59 AoE. These convert to September 19 and September 26 at 19:59 UTC+8. Today the abstract deadline has passed. Whether this project registered in time is **unknown**; GitHub is not evidence of an OpenReview registration. The author guide states that missing either deadline receives no accommodation. If no genuine abstract was registered, do not plan a new routine ICLR 2027 submission. Future-cycle rules must be rechecked when announced. [P1, P2, P4]

### Format and anonymity

Initial main text is at most nine pages; discussion/camera-ready allowance is ten. Use the 2027 LaTeX template. References and appendices are outside the main-text limit; reviewers need not read appendices. Main and supplementary submissions must be anonymous. New authors cannot be added after the abstract deadline. Simultaneous substantially similar archival submissions are prohibited. [P2]

The webpage has stale/inconsistent boilerplate: its camera-ready paragraph describes ten pages as identical to submission, whereas the dedicated Paper formatting clause explicitly states nine at submission and ten during discussion/finalization. Use the explicit initial-submission clause; do not use residual FAQ dates as the official deadline.

Practical release recommendation: preserve the public research history, but produce a separate anonymous review snapshot without personal paths, identifying repository URLs, author metadata, or `.git` history. Retain scholarly attribution for the source papers; anonymizing the study authors is not removing source-paper citations.

### AI use and responsibility

A mandatory AI-use section and submission-form disclosure apply. Hypothesis/model development, experiment design, implementation, data cleaning, and interpretation are relevant to the present ChatGPT/Codex workflow. Describe actual uses and human checks; do not call model labels human labels. Authors remain accountable for false claims and fabricated citations. The AI-use section is outside the page limit. [P5]

### Reviewing and publication readiness

The policy caps any author at 20 submissions and limits papers without a qualified reciprocal-reviewer author to one per author. Check every author's actual eligibility; do not add an honorary coauthor to meet a requirement. The official blog explains the policy's rationale. [P2, P6]

The reviewer guide emphasizes a specific question, literature placement, rigorous evidence, and meaningful new knowledge, not compulsory SOTA. A causal study can fit, but merely calling it a mechanism paper does not satisfy those criteria. Public discussion is not an opportunity to replace an unfinished submission with a substantially different project. [P3]

## 9. Next actions and scope controls

1. Continue the existing semantic/temporal/anonymization source task on the completed corpus; do not restart ingestion or merge unrelated branches.
2. Review a stratified source/seed sample, including boundary and failed cases, before converting candidates into certified blocks. Semantic matching alone is not scientific certification.
3. Prepare the nine-page scaffold and a short competing-explanations matrix now, leaving all results blank. Add the historical foundation citations rather than only 2025–2026 neighbors.
4. After source/construct review, seek a narrow development-pilot authorization. Predefine the content-versus-presentation diagnostic before outcomes; no present paid/model execution is authorized here.
5. Decide paper scope from evidence. A robust controlled effect may support an empirical LLM paper; a superficial wording-only effect requires a narrower framing study; imprecise nulls are inconclusive, not failure of science. Do not promise acceptance from sample counts.

Only one administrative fact requires clarification before planning for ICLR 2027: whether an authentic abstract and correct author list were registered before the deadline.

## 10. Source ledger and access limits

All links below were located/checked in this round. Publisher or proceedings records are used for claims; secondary summaries are not evidence. Selected classic PDF pages were visually inspected for experiment/figure structure. This is not an exhaustive collision scan, a replication of the cited experiments, or a reread of every prior repository round.

### Historical foundations

- H1. Jansson & Smith. *Design fixation*. Design Studies, 1991. Publisher abstract inspected. https://doi.org/10.1016/0142-694X(91)90003-F
- H2. Smith, Ward & Schumacher. *Constraining effects of examples in a creative generation task*. Memory & Cognition, 1993. Publisher abstract and PubMed metadata checked; not subscription full text. https://link.springer.com/article/10.3758/BF03202751 ; https://pubmed.ncbi.nlm.nih.gov/8289661/
- H3. Kohn & Smith. *Collaborative fixation: Effects of others' ideas on brainstorming*. Applied Cognitive Psychology 25:359–371, 2011. Publisher methods/abstract inspected. https://onlinelibrary.wiley.com/doi/10.1002/acp.1699
- H4. Oppenheimer & Patterson. *Thinking outside the box means thinking outside the search engine*. Memory & Cognition, 2025. Publisher article inspected. https://link.springer.com/article/10.3758/s13421-025-01732-x
- R1. Carbonell & Goldstein. *The use of MMR, diversity-based reranking for reordering documents and producing summaries*. SIGIR, 1998. Publisher bibliographic record. https://doi.org/10.1145/290941.291025
- R2. Kulesza & Taskar. *Determinantal Point Processes for Machine Learning*. Foundations and Trends in Machine Learning, 2012. Author manuscript abstract inspected. https://arxiv.org/abs/1207.6083

### Older paper-shape exemplars

- E1. Zhang et al. *Understanding deep learning requires rethinking generalization*. ICLR, 2017; first preprint 2016. Manuscript text and a PDF page inspected. https://arxiv.org/abs/1611.03530 ; https://arxiv.org/pdf/1611.03530
- E2. Goodfellow, Shlens & Szegedy. *Explaining and Harnessing Adversarial Examples*. ICLR, 2015; first preprint 2014. Manuscript and Figure 1 page inspected. https://arxiv.org/abs/1412.6572 ; https://arxiv.org/pdf/1412.6572
- E3. Jia & Liang. *Adversarial Examples for Evaluating Reading Comprehension Systems*. EMNLP, 2017. Official proceedings and first PDF page inspected. https://aclanthology.org/D17-1215/ ; https://aclanthology.org/D17-1215.pdf
- E4. Ribeiro, Singh & Guestrin. *Why Should I Trust You?: Explaining the Predictions of Any Classifier*. KDD, 2016. Full KDD paper's abstract/record, not the shorter NAACL demonstration publication. https://doi.org/10.1145/2939672.2939778 ; https://arxiv.org/abs/1602.04938
- E5. Szegedy et al. *Intriguing properties of neural networks*. ICLR, 2014; first preprint 2013. Author manuscript abstract inspected. https://arxiv.org/abs/1312.6199

### Bridge and close technical precedents

- B1. Zhao et al. *Calibrate Before Use: Improving Few-shot Performance of Language Models*. ICML, 2021. Official proceedings. https://proceedings.mlr.press/v139/zhao21c.html
- B2. Min et al. *Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?* EMNLP, 2022. Official proceedings. https://aclanthology.org/2022.emnlp-main.759/
- B3. Si, Yang & Hashimoto. *Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers*. ICLR, 2025. Official proceedings. https://proceedings.iclr.cc/paper_files/paper/2025/hash/ea94957d81b1c1caf87ef5319fa6b467-Abstract-Conference.html
- B4. Sorensen et al. *Spectrum Tuning: Post-Training for Distributional Coverage and In-Context Steerability*. ICLR, 2026. Official proceedings and manuscript abstract. https://proceedings.iclr.cc/paper_files/paper/2026/hash/7b6d77bf723ab4fed4f88baf544683fb-Abstract-Conference.html ; https://arxiv.org/abs/2510.06084
- B5. Ma et al. *MetaMuse: Algorithm Generation via Creative Ideation*. ICLR, 2026. Official proceedings. https://proceedings.iclr.cc/paper_files/paper/2026/hash/85632be2cd69e9a0ef4ba054c096fac9-Abstract-Conference.html

### Official rules, accessed 2026-09-20

- P1. ICLR 2027 Call for Papers. https://iclr.cc/Conferences/2027/CallForPapers
- P2. ICLR 2027 Author Guidelines, especially Deadlines, Paper formatting, anonymity and policy sections. https://iclr.cc/Conferences/2027/AuthorGuidelines
- P3. ICLR 2027 Reviewer Guidelines. https://iclr.cc/Conferences/2027/ReviewerGuidelines
- P4. ICLR 2027 Dates and Deadlines. https://iclr.cc/Conferences/2027/Dates
- P5. ICLR 2027 AI Policy for Authors. https://iclr.cc/Conferences/2027/AIPolicyForAuthors
- P6. ICLR Program Chairs. *Submission policies for ICLR 2027*, September 2, 2026. https://blog.iclr.cc/2026/09/02/submission-policies-for-iclr-2027/

Access note: the style-file URL was confirmed in the official guide, but the ZIP download failed in this environment. No claim is made that the template compiled or that a manuscript was rendered. One version-specific arXiv screenshot failed; the unversioned paper PDF was subsequently available. The 2017 OpenReview forum presented a browser challenge; paper content/venue identification were checked through the author manuscript instead.
