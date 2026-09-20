# F1 Calibration Review Fields

All human decision fields are intentionally null. This package is an instrument for human calibration, not a model-labelled dataset.

`seed_audit`: review source-faithfulness, duplicated problem text, generic masking, solution-prescribing spans, and comprehensibility. Deterministic diagnostics are provisional observations only.

`paper_relevance_route_audit`: one seed plus one abstract per row. Set DIRECT_RELEVANCE, TRANSFER_ONLY, OFF_TOPIC, or UNCLEAR; assign primary/secondary routes and quote a supporting sentence only after review. Relevance is seed-specific.

`block_admissibility_audit`: A/B order is randomized and decoded only through the private mapping. Review exactly four displayed slots. Do not certify k=8 or k=12 from this file.

`shadow_audit`: developmental false-exclusion audit for six measured-zero and six source-gate-blocked seeds selected by frozen hashes. It is not a pass threshold and is outside the 96-case queue.
