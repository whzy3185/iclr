# Corpus Completion Report

Status: COMPLETE

```text
ICLR2024_OFFICIAL=2260
ICLR2024_ABSTRACTS=2260
ICLR2024_MISSING=0
ICLR2025_OFFICIAL=3703
ICLR2025_ABSTRACTS=3703
ICLR2025_MISSING=0
ICLR2026_OFFICIAL=5351
ICLR2026_ABSTRACTS=5351
ICLR2026_MISSING=0
TOTAL_OFFICIAL=11314
TOTAL_ABSTRACTS=11314
TOTAL_MISSING=0
CORPUS_SHA256=0d0f182481534214ee0255a76b884fd4a959f04cc3d7ba85dbde5869dd5f6807
TESTS=13 unit tests PASS; 2 byte-identical full passes; 11314 source-byte revalidations; replay requests=0
```

Every normalized ID reconciles with the frozen official Conference indexes.
Nonempty abstracts were reparsed from retained source bytes; no title-based
surrogate or generated abstract was used. All acquisition failures and missing
rows remain retained. Legacy retrieval timestamps are null when not historically
known, not fabricated from file modification times. New retrieval timestamps
are saved in immutable attempt records and reused in the second pass.

New requests in pass 1: 4010; pass 2: 0.
Source types: {'official_proceedings': 3874, 'official_proceedings_legacy_cache': 7440}.

No ARS, proposal generation, baseline/treatment, route or model experiment ran.
STOP after publishing this data-only checkpoint.

## Execution

T1 inventory completed without network requests; 7440 verified legacy pages reused.
T2 acquisition attempted only missing/invalid pages with six workers and at most
three attempts per source. T3/T4 normalization and identity checks completed.
T5 two complete pipeline executions compared byte-for-byte. T6 publication follows.
The inventory and both passes are retained separately; only execution manifest
request counts differ. See VERIFICATION.json and corpus_manifest.json.
