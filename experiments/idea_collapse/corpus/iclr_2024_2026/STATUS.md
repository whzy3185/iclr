# ICLR 2024-2026 Abstract Completion

Scope: data acquisition and validation only. No model/ARS/research experiment.

T1 COMPLETE: all three official denominators reconcile; duplicate IDs = 0;
legacy hash/parse validation failures = 0; network requests during inventory = 0.

| Year | Official | Verified cached abstracts | Missing |
| --- | ---: | ---: | ---: |
| 2024 | 2260 | 0 | 2260 |
| 2025 | 3703 | 3703 | 0 |
| 2026 | 5351 | 3737 | 1614 |

Inventory IDs, missing rows and hashes are retained in `inventory/`.
T2 now completes only the 3874 missing pages. No validated cache entry is replaced.

Legacy cache acquisition timestamps are unknown and stay null. New timestamps
are persisted with immutable acquisition attempts. Source pages are never
replaced; missing or invalid inputs receive bounded acquisition attempts.

Next: complete missing acquisitions, normalize twice, compare
all normalized bytes, publish exact counts and STOP.
