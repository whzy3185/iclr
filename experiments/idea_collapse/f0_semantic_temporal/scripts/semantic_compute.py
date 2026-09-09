"""Frozen bi-encoder/cross-encoder inference only; no generative model API."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import time

import numpy as np
import torch
import transformers
from transformers import AutoModel, AutoModelForSequenceClassification, AutoTokenizer

from common import BASE, hash_value, read_rows, save, sha, text


def store_array(path, values):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if not np.array_equal(np.load(path), values):
            raise ValueError("cached numeric artifact differs")
        return
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("xb") as handle:
        np.save(handle, values, allow_pickle=False)
    os.link(tmp, path)
    tmp.unlink()


def model_files(directory):
    return {p.name: sha(p) for p in sorted(directory.iterdir()) if p.is_file() and p.name != "README.md"}


def initialize(path, classifier=False):
    tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True, trust_remote_code=False)
    cls = AutoModelForSequenceClassification if classifier else AutoModel
    model = cls.from_pretrained(path, local_files_only=True, trust_remote_code=False,
                               use_safetensors=True, dtype=torch.float16).eval().to("mps")
    return tokenizer, model


def setup(args):
    if not torch.backends.mps.is_available():
        raise RuntimeError("MPS unavailable; no silent CPU/lexical fallback")
    torch.set_num_threads(4)
    torch.manual_seed(0)
    config = json.loads((BASE / "config.json").read_text())
    seeds, evidence = read_rows(BASE / "seeds.jsonl"), read_rows(BASE / "evidence.jsonl")
    manifest = {"dense": config["dense"], "reranker": config["reranker"], "device": "mps", "dtype": "float16",
        "torch": torch.__version__, "transformers": transformers.__version__, "numpy": np.__version__,
        "platform": platform.platform(), "python": platform.python_version(),
        "tokenizers": __import__("tokenizers").__version__, "dense_files": model_files(args.dense_path),
        "reranker_files": model_files(args.reranker_path), "config_sha256": sha(BASE / "config.json"),
        "seed_inputs_sha256": sha(BASE / "seeds.jsonl"), "evidence_inputs_sha256": sha(BASE / "evidence.jsonl"),
        "normalization": "CLS L2 for bi-encoder; raw cross-encoder logits, not calibrated probabilities",
        "independence_scope": "separate frozen cross-encoder weights and computation, not independent training-data claim",
        "repeat_atol": config["inference_repeat_atol"], "MPS_fallback": os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK", "unset"),
        "model_usage": "source-side semantic scoring only; no generate() call"}
    save(BASE / "semantic/model_manifest.json", manifest)
    return config, seeds, evidence, manifest


def encode_all(config, seeds, evidence, model_path):
    tokenizer, model = initialize(model_path)
    cache = BASE / "semantic/cache"
    repeat_path = BASE / "semantic/embedding_repeat_check.json"
    repeat = json.loads(repeat_path.read_text()) if repeat_path.exists() else []
    for label, objects, texts in [
        ("seed", seeds, [config["dense"]["query_prefix"] + text(s["method_masked_question"]) for s in seeds]),
        ("evidence", evidence, [text(e["abstract"]) for e in evidence]),
    ]:
        arrays, rows = [], []
        batch_size = config["dense"]["batch_size"]
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            fingerprint = hash_value({"model": config["dense"], "dtype": "float16", "device": "mps", "texts": batch})
            path = cache / f"{label}-{start:05d}-{fingerprint[:16]}.npy"
            raw_lengths = [len(ids) for ids in tokenizer(batch, truncation=False)["input_ids"]]
            if path.exists():
                values = np.load(path, allow_pickle=False)
            else:
                inputs = tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt").to("mps")
                with torch.inference_mode():
                    outputs = model(**inputs).last_hidden_state[:, 0].float()
                    values = torch.nn.functional.normalize(outputs, p=2, dim=1).cpu().numpy()
                    if start == 0:
                        again = torch.nn.functional.normalize(model(**inputs).last_hidden_state[:, 0].float(), p=2, dim=1).cpu().numpy()
                        delta = float(np.max(np.abs(values - again)))
                        if delta > config["inference_repeat_atol"]:
                            raise ValueError("embedding inference repeat exceeds declared tolerance")
                        repeat.append({"kind": label, "rows": len(batch), "max_abs_diff": delta, "atol": config["inference_repeat_atol"]})
                if not np.isfinite(values).all():
                    raise ValueError("non-finite embeddings")
                store_array(path, values)
            arrays.append(values)
            for offset, (value, length) in enumerate(zip(values, raw_lengths)):
                obj = objects[start + offset]
                rows.append({"id": obj.get("seed_id", obj.get("paper_id")), "row": start + offset,
                    "input_sha256": hashlib.sha256(batch[offset].encode()).hexdigest(), "token_count_full": length,
                    "truncated": length > 512, "embedding_row_sha256": hashlib.sha256(value.tobytes()).hexdigest(),
                    "cache_file": str(path.relative_to(BASE)), "cache_sha256": sha(path)})
            if start % 256 == 0:
                print(f"encoded {label} {min(start+batch_size,len(texts))}/{len(texts)}", flush=True)
        matrix = np.concatenate(arrays).astype(np.float32)
        store_array(BASE / f"semantic/{label}_embeddings.npy", matrix)
        save(BASE / f"semantic/{label}_embeddings_manifest.jsonl", rows, rows=True)
    save(BASE / "semantic/embedding_repeat_check.json", repeat)
    del model
    torch.mps.empty_cache()
    queries = np.load(BASE / "semantic/seed_embeddings.npy")
    docs = np.load(BASE / "semantic/evidence_embeddings.npy")
    similarity = queries @ docs.T
    k = config["candidate_k"]
    # Stable sort uses the frozen evidence ID order for ties.
    indices = np.argsort(-similarity, axis=1, kind="stable")[:, :k]
    values = np.take_along_axis(similarity, indices, axis=1)
    store_array(BASE / "semantic/dense_indices.npy", indices.astype(np.int32))
    store_array(BASE / "semantic/dense_scores.npy", values.astype(np.float32))
    rows = [{"seed_id": s["seed_id"], "status": "MEASURED", "source_matching_allowed": s["source_matching_allowed"],
             "paper_ids": [evidence[i]["paper_id"] for i in ids], "dense_scores": scores.tolist(),
             "rank_encoding": "1-based array position", "k": k}
            for s, ids, scores in zip(seeds, indices, values)]
    save(BASE / "semantic/dense_candidates.jsonl", rows, rows=True)


def rerank_all(config, seeds, evidence, model_path):
    tokenizer, model = initialize(model_path, classifier=True)
    indices = np.load(BASE / "semantic/dense_indices.npy")
    dense_scores = np.load(BASE / "semantic/dense_scores.npy")
    texts = [text(e["abstract"]) for e in evidence]
    full_lengths = [len(t) for t in tokenizer(texts, truncation=False)["input_ids"]]
    save(BASE / "semantic/reranker_evidence_token_lengths.json", {e["paper_id"]: n for e, n in zip(evidence, full_lengths)})
    cache = BASE / "semantic/reranker_cache"
    started = time.monotonic()
    done = 0
    pair_count = 0
    records = []
    repeat_check = None
    for index, seed in enumerate(seeds):
        if not seed["source_matching_allowed"]:
            records.append({"seed_id": seed["seed_id"], "status": "BLOCKED_SOURCE_GATE", "reranker_scores": None,
                            "reason": seed["repair_reason"] or seed["hard_errors"]})
            continue
        ids = indices[index]
        pairs = [(text(seed["method_masked_question"]), texts[i]) for i in ids]
        fingerprint = hash_value({"model": config["reranker"], "dtype": "float16", "device": "mps", "pairs": pairs})
        path = cache / f"{seed['seed_id']}-{fingerprint[:16]}.npy"
        if path.exists():
            scores = np.load(path, allow_pickle=False)
        else:
            cache.mkdir(parents=True, exist_ok=True)
            save(path.with_suffix(".request.json"), {"seed_id": seed["seed_id"], "input_sha256": fingerprint,
                "model": config["reranker"], "candidate_ids": [evidence[i]["paper_id"] for i in ids]})
            result = []
            for first in range(0, len(pairs), config["reranker"]["batch_size"]):
                batch = pairs[first:first + config["reranker"]["batch_size"]]
                inputs = tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt").to("mps")
                with torch.inference_mode():
                    batch_scores = model(**inputs).logits.reshape(-1).float().cpu().numpy()
                    if repeat_check is None:
                        again = model(**inputs).logits.reshape(-1).float().cpu().numpy()
                        delta = float(np.max(np.abs(batch_scores - again)))
                        if delta > config["inference_repeat_atol"]:
                            raise ValueError("reranker repeat exceeds declared tolerance")
                        repeat_check = {"pairs": len(batch), "max_abs_diff": delta, "atol": config["inference_repeat_atol"]}
                        save(BASE / "semantic/reranker_repeat_check.json", repeat_check)
                result.append(batch_scores)
            scores = np.concatenate(result)
            if len(scores) != config["candidate_k"] or not np.isfinite(scores).all():
                raise ValueError("invalid reranker result")
            store_array(path, scores)
        done += 1
        pair_count += len(scores)
        records.append({"seed_id": seed["seed_id"], "status": "MEASURED", "paper_ids": [evidence[i]["paper_id"] for i in ids],
                        "dense_scores": dense_scores[index].tolist(), "reranker_scores": scores.tolist(),
                        "cache_file": str(path.relative_to(BASE)), "cache_sha256": sha(path)})
        if done % 10 == 0:
            print(f"reranked seeds={done}/{sum(s['source_matching_allowed'] for s in seeds)} pairs={pair_count} elapsed_s={time.monotonic()-started:.1f}", flush=True)
    save(BASE / "semantic/reranked_candidates.jsonl", records, rows=True)
    summary = {"measured_seeds": done, "measured_pairs": pair_count,
        "source_gate_blocked_seeds": len(seeds) - done, "elapsed_seconds": time.monotonic() - started,
        "scientific_proposal_generations": 0}
    summary_path = BASE / "semantic/reranking_summary.json"
    if summary_path.exists():
        original = json.loads(summary_path.read_text())
        if any(original[k] != v for k, v in summary.items() if k != "elapsed_seconds"):
            raise ValueError("cached rerank summary mismatch")
    else:
        save(summary_path, summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["encode", "rerank"])
    parser.add_argument("--dense-path", type=Path, required=True)
    parser.add_argument("--reranker-path", type=Path, required=True)
    args = parser.parse_args()
    config, seeds, evidence, manifest = setup(args)
    if args.stage == "encode":
        encode_all(config, seeds, evidence, args.dense_path)
    else:
        rerank_all(config, seeds, evidence, args.reranker_path)
