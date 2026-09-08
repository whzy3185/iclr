# F0 Research Decision Table

SCIENTIFIC_DECISION: RESEARCH_LEAD_REQUIRED
Source run: `F0R-9f61bff4538465a7a96f`. No publication-readiness decision is made.

| Seed population | Count | State / interpretation |
| --- | ---: | --- |
| Official focal IDs | 5351 | measured denominator |
| Cached, parsed focal abstracts | 3737 | measured; not all 5351 |
| Source matching allowed | 2772 | provisional only |
| Flagged but matching allowed | 1753 | warnings preserved |
| Explicit solution repair queue | 965 | blocked from primary candidate matching |
| Structural/cache-missing failures | 1614 | retained, not negative model outcomes |
| Human-confirmed experimental blocks | unknown | pending review, not measured zero |

## Lexical Source Coverage - Unique Seeds Within Each Route Pair

| Pair | k=4 | k=6 | k=8 | k=12 |
| --- | ---: | ---: | ---: | ---: |
| R1 | 252 | 126 | 80 | 46 |
| R2 | 1627 | 1109 | 805 | 422 |
| R3 | 1047 | 551 | 327 | 159 |
| R4 | 107 | 34 | 11 | 2 |

Across pairs, deduplicated unique-seed coverage is {'12': 611, '4': 2139, '6': 1545, '8': 1119}.
Do not sum the route rows as independent seed counts.

## STRICT / BASE / RELAXED Frontier

All three canonical matching regimes, all T0/T1/T2 tiers, purity .60/.70/.80 and
k=4/6/8/12 are retained in `coverage_balance_frontier.csv` and the expanded typed
grid. Canonical semantic matching is **MISSING_COVARIATES**, not zero coverage.
Numeric purity is NOT_ASSESSED. T0/T1 date membership is UNKNOWN, not clean.
The additional `LEXICAL_LEGACY_NO_DATE_PROVISIONAL` regime is a separate
measured diagnostic; it is not a replacement for the canonical frontier.

## Largest Bottlenecks and Recommended Blocks

1. Semantic task compatibility, first-public dates and model-token length are
   not established; keyword purity is not a calibrated numeric probability.
2. 1614 focal abstracts were absent from the recovered cache. No missing title
   was turned into an invented abstract or a confirmed negative seed.
3. 965 focal-solution cases need repair/review; flagged cases remain provisional.
4. All four route contrasts have lexical audit candidates. The deterministic
   examples in `route_equipoise_audit_packet.csv` are recommended for **source
   review only**, not for ARS generation. No block is certified ARS eligible.
5. R4 remains a complementary/high-composability contrast requiring particular
   non-subsumption/equipoise review; it has not been dropped for poorer coverage.

No seed, route or matching parameter was selected using proposal effects.
