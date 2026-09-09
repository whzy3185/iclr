import json
import time
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

torch.set_num_threads(4)
path = "work/semantic-models/bge-reranker-base"
tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True, trust_remote_code=False)
model = AutoModelForSequenceClassification.from_pretrained(path, local_files_only=True,
    use_safetensors=True, trust_remote_code=False, dtype=torch.float16).eval().to("mps")
pairs = [("A source-only engineering workload. " * 80, "A technical source paragraph. " * 160)] * 16
inputs = tokenizer(pairs, padding=True, truncation=True, max_length=512, return_tensors="pt").to("mps")
with torch.inference_mode():
    model(**inputs)
    torch.mps.synchronize()
    start = time.monotonic()
    for _ in range(3):
        model(**inputs)
    torch.mps.synchronize()
elapsed = time.monotonic() - start
print(json.dumps({"purpose": "synthetic_engineering_throughput_only", "pair_scores_not_inspected": True,
    "model": "BAAI/bge-reranker-base", "device": "mps", "dtype": "float16", "pairs": 48,
    "tokens_per_pair": 512, "seconds": elapsed, "pairs_per_second": 48 / elapsed,
    "projected_hours_for_1070200_pairs": 1070200 / (48 / elapsed) / 3600,
    "mps_driver_allocated_bytes": torch.mps.driver_allocated_memory()}))
