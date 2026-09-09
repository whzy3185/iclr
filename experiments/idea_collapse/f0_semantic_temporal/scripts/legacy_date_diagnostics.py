"""Calendar gap distribution on the already existing F0 candidate relationships."""
from collections import Counter
import csv
from datetime import date
import gzip

from common import BASE, RECOVERY, read_rows, save, sha

dates = {r["paper_id"]: r for r in read_rows(BASE / "temporal/earliest_public_dates.jsonl")}
source = RECOVERY / "runs/F0R-9f61bff4538465a7a96f/retrieval_candidates.csv.gz"
gaps = Counter()
with gzip.open(source, "rt") as handle:
    for row in csv.DictReader(handle):
        seed = dates[row["seed_id"].removeprefix("SEED_")]["earliest_public_date"]
        evidence = dates[row["paper_id"]]["earliest_public_date"]
        value = "UNKNOWN" if seed is None or evidence is None else str((date.fromisoformat(evidence)-date.fromisoformat(seed)).days)
        gaps[value] += 1
save(BASE / "temporal/existing_candidate_date_gaps.json", {
    "source_sha256": sha(source), "date_map_sha256": sha(BASE / "temporal/earliest_public_dates.jsonl"),
    "relationships": sum(gaps.values()), "evidence_minus_seed_days": dict(gaps),
    "status": "MEASURED_DISCOVERED_DATE_DIFFERENCES", "historical_cleanliness": "NOT_CERTIFIED",
    "scope": "previously computed lexical candidate relationships; dates from source fields, not conference year"})
print(dict(gaps))
