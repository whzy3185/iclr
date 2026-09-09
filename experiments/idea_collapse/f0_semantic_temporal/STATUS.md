# Source-side Semantic / Temporal Checkpoint

Base: c5e4391f3af6f7ff67291352c632731d58350293.
Task source: research/f0-semantic-temporal-20260908 at b57e83a6c85ce14d6d64b3e041709a2d14906a80.
Scientific proposal generations: 0. F1 human labels: NOT_RUN.

T0 COMPLETE: corpus SHA and 11314 IDs/0 missing reconcile. ICLR 2025 only is
evidence. Existing 3737 available seed records retained; formerly missing 1614
rebuilt with the unchanged masking function. 3950 pass the existing provisional
source gate; all 5351 seed records remain present.

T1 MEASURED_WITH_HISTORY_LIMITATION: all 9054 causal-core records have verified
proceedings publication-date metadata. All are FALLBACK_ONLY. OpenReview public
bulk metadata returned challenge-required 403 and was not bypassed; the source
pages supplied no matched arXiv date links. These are earliest discovered dates,
not proof of no earlier versions or historical temporal cleanliness.

T2 IN PROGRESS: default BAAI models downloaded at fixed revisions. Mac MPS FP16
is used; CUDA host was unreachable. Dense embeddings and top-200 candidates are
computed for all 5351 seeds over 3703 evidence papers. Cross-encoder scoring will
process every top-200 pair for the 3950 source-gate-allowed seeds, retaining the
other seeds as BLOCKED_SOURCE_GATE, not silently removing them.

Reranker synthetic 512-token engineering profile: 62.31 pairs/s at batch 16,
not a relevance/quality comparison. Models were not replaced and scope was not
reduced to improve coverage. Approximately 3.5 hours for 790000 pairs is an
engineering estimate, not a result or fixed resource guarantee.

T4 metadata-only anonymization produced 3703 abstracts; content identifiers are
retained. No method/finding deletion or LLM rewrite. F1 source identity remains
potentially inferable from intrinsic content; this is recorded, not concealed.

The encoder execution source is retained in `semantic/code_snapshots/`.
The later change only repairs idempotent cached replay of diagnostic logs; it
does not change model scores, preprocessing, thresholds or seed selection.

T3/T5/T6/T7 await complete cross-encoder scoring. No F1 labels or outcome work
is authorized by this status. The final T8 checkpoint will stop at human review.
