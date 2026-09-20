# Round 59 — CCF-B venue retargeting

Date: 2026-09-20.
Status: submission-strategy research, not an experimental result or model-execution authorization.
Trigger: the user confirmed that no ICLR 2027 abstract was registered and requested a CCF-B conference alternative.
Inspected main before this round: 7e83dc3986ef2995873d2f850578b29c1e1af939. Round 58 remains the scientific positioning reference. No branch merge, corpus change, paid inference, submission, or deadline reminder was executed.

## Decision

Recommend COLING 2027 main-conference long paper as the best-fit near-term option, with NAACL 2027 as an alternative within the same ARR cycle. This is a topic-fit recommendation, not a claim that either is easy or that the current manuscript is ready.

If a complete, auditable model-behavior study cannot be finished for the October ARR deadline, do not rush a source-feasibility report into that cycle. ECAI 2027 offers a later, officially posted submission window. EMNLP 2027 remains a topic-aligned future option, but its main-paper deadline was not verified in this search. IJCAI 2027 is another general-AI option under the new CCF directory; no official 2027 main-paper deadline was verified.

Do not change the research question, lower validity requirements, or discard negative findings to fit a conference label. The core remains a controlled empirical study of scientific-literature-conditioned language-model generation.

## CCF category verification

Read the 2026 seventh-edition CCF directory, hosted by Lishui University's research office. Visually checked PDF pages 58 and 59 (zero-based pages 57 and 58). COLING, NAACL, EMNLP, ECAI, UAI, and IJCAI appear in the AI B-category table. AISTATS appears in the C-category table and is therefore not included as a CCF-B recommendation. [R1]

The CCF website's category page was not consistently accessible. The university-hosted source is the CCF directory document, not a conference-deadline aggregator. Universities may apply different directory vintages or track-recognition policies; verify the user's institutional rule before claiming formal credit. Do not automatically equate Findings, workshops, demonstrations, or industry tracks with the main-conference research-paper category.

## Verified submission windows

| Target | Submission route and dates | Planning interpretation |
|---|---|---|
| COLING 2027 | ARR submission 2026-10-12, 23:59 AoE; commitment 2026-12-23; acceptance notification 2027-02-10. Macau, 2027-05-09 to 2027-05-14. [R2, R3] | Strong topic fit; only usable if the study is genuinely ready. |
| NAACL 2027 | Same final ARR submission and commitment dates. Official main-call search content lists notification 2027-02-10 and meeting 2027-06-01 to 2027-06-05. [R4, R5] | Same-cycle alternative, not a simultaneous second submission. |
| ECAI 2027 | Official homepage lists full-paper deadline 2027-04-14 and notification 2027-07-15; main meeting 2027-10-04 to 2027-10-07 in Athens. [R6] | More development time. Recheck complete CFP, abstract-registration requirement and timezone when published. |
| EMNLP 2027 | Main-paper deadline not verified. Joint workshop call is not a main-paper CFP. | Future NLP option, not a dated commitment. |
| IJCAI 2027 | Official IJCAI homepage confirms 2027 meeting, but no main-paper submission deadline was verified. [R7] | Monitor only; do not invent January/February deadlines from past years. |

The October 12 AoE paper deadline corresponds to October 13 at 19:59 in UTC+8. ARR means submit a completed paper for review first and commit the reviewed paper to a venue later; it is not an abstract-only placeholder opportunity. COLING long papers allow eight pages of main content. [R2, R3, R8]

COLING and NAACL share the October ARR cycle. One primary venue must be selected at commitment; double commitment is not permitted. NAACL's current FAQ describes an optional secondary-consideration preference, but explicitly does not guarantee second-venue consideration. Do not market this as two guaranteed review/acceptance opportunities. [R5]

## Fit and paper adjustments

COLING's CFP explicitly includes evaluation, information retrieval, NLP-model analysis, generation and LLM applications. NAACL welcomes empirical and evaluation contributions. These align more directly with the present study than introducing a new architecture solely to look like a general-ML methods paper. [R2, R4]

Suggested pre-result title: **Same Question, Different Literature: A Controlled Study of LLM Research Choices**.

Retain the validated task definition, randomized literature-packet policies, complete outcome distributions, independent-seed analysis, and content-versus-presentation controls. Treat broad prior-resistance, natural-RAG generalization, and additional model scales as separately justified extensions, not automatic prerequisites or promised results. No required count of seeds or models guarantees acceptability.

The ICLR abstract corpus can remain the study corpus for an NLP conference. Venue change alone is not a reason to replace the corpus or mix conference populations. Cross-venue replication should be motivated by a concrete generalization claim and separately designed.

## Costs and registration

The user previously preferred zero publication/APC charges and low overall cost. No zero-total-cost guarantee can be given. COLING 2027's registration page says details will be announced; NAACL's main-call content requires a registered presenting author and describes in-person/virtual presentation. This does not establish a zero registration fee or a confirmed price. ECAI 2027 prices and complete publication terms were not verified. [R4, R9]

Separate submission/APC, author registration, membership, optional extras, travel, and compute in any later budget. Do not substitute previous-year registration rates for 2027 prices. Fee status is a pending check before a financial commitment.

## Operational next step

Continue the already authorized semantic/temporal/source-validity work. Prepare an eight-page NLP empirical-paper structure without invented results. Decide whether October ARR is appropriate only after checking actual model-experiment and measurement artifacts. If not ready, choose a later verified venue window; no deadline-driven relaxation of experimental validity. No simultaneous submissions.

## Sources and access notes

R1. CCF, 2026 seventh-edition directory, original PDF hosted by Lishui University; visual inspection of AI B/C conference pages:
https://kyc.lsu.edu.cn/_upload/article/files/20/77/2cbaa3754eb9aff9ed74cafed8ff/23a8de02-594c-445f-b084-69b0193c05b3.pdf
University publication notice:
https://kyc.lsu.edu.cn/2026/0518/c2834a367789/page.htm

R2. COLING 2027 main-conference CFP:
https://2027.coling-iccl.org/calls/main_conference_papers/

R3. COLING 2027 official homepage and ACL-hosted CFP:
https://2027.coling-iccl.org/
https://www.aclweb.org/portal/node/14560

R4. NAACL 2027 main-conference CFP:
https://2027.naacl.org/calls/main_conference_papers/
Access note: fresh official search content contains the full CFP; one open-tool fetch returned an older 'Coming soon' snapshot. Shared submission/commitment dates were independently corroborated on ARR and COLING. Reviewer-registration and meta-review-release dates differ slightly across official pages; they are intentionally not frozen here.

R5. NAACL 2027 FAQ:
https://2027.naacl.org/faq/

R6. ECAI 2027 official homepage:
https://ecai2027.org/
Access note: dated content retrieved in official-domain search; direct open returned a cache error. Verify complete CFP and timezone before scheduling submission.

R7. IJCAI official homepage:
https://www.ijcai.org/

R8. ACL Rolling Review, Dates and Venues:
https://aclrollingreview.org/dates

R9. COLING 2027 registration:
https://2027.coling-iccl.org/registration/

Search scope: current CCF category, official main-paper CFP, ARR submission/commitment, timing and registration. Third-party deadline estimates were not used as official deadlines. This is a focused shortlist, not a comprehensive review of all CCF-B conferences.
