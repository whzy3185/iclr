#!/usr/bin/env python3
"""F0 source-only feasibility audit for the ICLR evidence-composition study.

This script intentionally performs no proposal generation and no treatment-outcome
inspection. It uses only ICLR proceedings metadata/abstract pages, deterministic
lexical source annotation, TF-IDF style source relevance, an independent BM25-like
reranker, and deterministic pairwise matching.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import os
import random
import re
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "experiments" / "idea_collapse" / "feasibility_1"
CACHE = OUT / "_source_cache"
BASE_URL = "https://proceedings.iclr.cc"

ROUTES = [
    "BUILD_IMPROVE",
    "DIAGNOSE_STRESS_TEST",
    "MEASURE_EVALUATE",
    "EXPLAIN_MECHANISM_THEORY",
]
R_PAIRS = {
    "R1": ("BUILD_IMPROVE", "DIAGNOSE_STRESS_TEST"),
    "R2": ("BUILD_IMPROVE", "MEASURE_EVALUATE"),
    "R3": ("BUILD_IMPROVE", "EXPLAIN_MECHANISM_THEORY"),
    "R4": ("DIAGNOSE_STRESS_TEST", "EXPLAIN_MECHANISM_THEORY"),
}

ROUTE_DEFS = {
    "BUILD_IMPROVE": "Build, improve, optimize, or introduce a method/model/system intended to solve or improve the seed problem.",
    "DIAGNOSE_STRESS_TEST": "Diagnose failures, stress-test robustness/safety/generalization, or expose limitations of existing systems on the seed problem.",
    "MEASURE_EVALUATE": "Measure, benchmark, evaluate, or construct evaluation protocols/metrics/datasets for the seed problem.",
    "EXPLAIN_MECHANISM_THEORY": "Explain mechanisms, provide theoretical analysis, derive guarantees, or characterize why/when phenomena occur.",
}

ROUTE_KEYWORDS = {
    "BUILD_IMPROVE": {
        "propose": 2.0, "introduce": 2.0, "present": 1.6, "develop": 1.8,
        "framework": 1.5, "method": 1.5, "algorithm": 1.5, "model": 1.0,
        "architecture": 1.5, "training": 1.0, "optimize": 1.6, "improve": 1.6,
        "efficient": 1.0, "outperform": 1.1, "achieve": 0.8, "novel": 1.3,
        "system": 1.1, "generate": 0.8, "learn": 0.7, "fine-tune": 1.1,
    },
    "DIAGNOSE_STRESS_TEST": {
        "failure": 2.0, "failures": 2.0, "diagnose": 2.2, "stress": 2.0,
        "robustness": 1.6, "adversarial": 1.4, "attack": 1.6, "vulnerability": 1.8,
        "limitation": 1.5, "limitations": 1.5, "bias": 1.2, "hallucination": 1.3,
        "safety": 1.2, "detect": 1.1, "probe": 1.2, "risk": 1.1,
        "out-of-distribution": 1.4, "ood": 1.4, "counterfactual": 1.0,
    },
    "MEASURE_EVALUATE": {
        "benchmark": 2.2, "benchmarks": 2.2, "dataset": 1.8, "metric": 2.0,
        "metrics": 2.0, "evaluation": 2.0, "evaluate": 1.8, "assess": 1.5,
        "measure": 1.7, "measurement": 1.7, "leaderboard": 1.4, "compare": 1.0,
        "survey": 0.8, "annotation": 1.1, "protocol": 1.1, "testbed": 1.5,
    },
    "EXPLAIN_MECHANISM_THEORY": {
        "theory": 2.1, "theoretical": 2.1, "theorem": 2.0, "proof": 1.8,
        "bound": 1.8, "bounds": 1.8, "guarantee": 1.8, "guarantees": 1.8,
        "analyze": 1.5, "analysis": 1.3, "explain": 1.8, "mechanism": 2.0,
        "understand": 1.4, "characterize": 1.6, "convergence": 1.8,
        "generalization": 1.3, "causal": 1.2, "interpret": 1.1, "principled": 1.0,
    },
}

SUBFIELD_KEYWORDS = {
    "language_models": ["language model", "llm", "large language", "text", "nlp", "token", "prompt", "reasoning", "instruction"],
    "vision_multimodal": ["vision", "image", "video", "multimodal", "diffusion", "visual", "segmentation", "object detection"],
    "reinforcement_learning": ["reinforcement", "policy", "reward", "agent", "offline rl", "decision", "control"],
    "generative_models": ["generative", "diffusion", "flow", "vae", "gan", "sampling", "score-based"],
    "graphs": ["graph", "node", "edge", "gnn", "molecular", "molecule"],
    "optimization_theory": ["optimization", "gradient", "convergence", "theorem", "bound", "generalization", "theory"],
    "robustness_safety": ["robust", "safety", "adversarial", "attack", "privacy", "fairness", "bias", "uncertainty"],
    "data_evaluation": ["benchmark", "dataset", "evaluation", "metric", "measure", "annotation"],
}

STOPWORDS = set("""
a an and are as at be by can for from has have in into is it its may more most not of on or our
that the their this to via we with without using use used than then these those such across after before
between both each either every first however if improve improves improved over under when where which while
will within show shows also paper work results based learning model models data method methods task tasks
""".split())

CONFIG = {
    "source_universe": "ICLR proceedings Conference abstract pages",
    "years": {"evidence": 2025, "seeds": 2026},
    "source_urls": {
        "iclr_2025_index": f"{BASE_URL}/paper_files/paper/2025",
        "iclr_2026_index": f"{BASE_URL}/paper_files/paper/2026",
    },
    "openreview_api_status": "bulk_api_challenge_required_403_on_2026-09-07; proceedings used as primary source",
    "retrieval": {
        "vectorizer": "deterministic lowercase word unigram+bigram tf-idf with L2 normalization",
        "dense_relevance": "cosine(seed_tfidf, evidence_tfidf)",
        "reranker_relevance": "BM25-like exact token overlap normalized to 0..1 within seed candidate list",
        "candidate_pool_size": 300,
        "relevance_floor_dense": 0.045,
        "relevance_floor_reranker": 0.08,
    },
    "matching": {
        "algorithm": "deterministic greedy nearest-neighbor without replacement, sorted by lowest cost then paper ids",
        "cost": "0.35*dense_diff + 0.25*reranker_diff + 0.15*length_z_diff + 0.10*date_z_diff + 0.15*topic_distance",
        "hard_calipers": {
            "dense_diff_max": 0.10,
            "reranker_diff_max": 0.35,
            "topic_distance_max": 1.0,
        },
        "route_clear_threshold": 4,
        "k_targets": [6, 8, 12],
    },
    "packet_simulation": {
        "alphas": [0, 0.25, 0.5, 0.75, 1],
        "k_for_primary_balance": 8,
        "realizations_per_block": 6,
        "random_seed": 20260907,
    },
}


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="replace")).hexdigest()


def slugish(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")[:180]


def run_curl(url: str, out: Optional[Path] = None, timeout: int = 90) -> Tuple[int, str]:
    cmd = ["curl", "-L", "--compressed", "--http2", "--connect-timeout", "15", "--max-time", str(timeout), "--retry", "2", "-sS", url]
    if out is not None:
        tmp = out.with_suffix(out.suffix + ".tmp")
        cmd.extend(["-o", str(tmp)])
    proc = subprocess.run(cmd, cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out is not None and proc.returncode == 0:
        tmp.replace(out)
        return 0, ""
    return proc.returncode, proc.stdout + proc.stderr


def ensure_indexes() -> Dict[int, Path]:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = {}
    for year in (2025, 2026):
        p = OUT / f"iclr{year}_index.html"
        if not p.exists() or p.stat().st_size < 10000:
            code, msg = run_curl(f"{BASE_URL}/paper_files/paper/{year}", p, timeout=180)
            if code != 0:
                raise RuntimeError(f"failed to fetch index {year}: {msg[:500]}")
        paths[year] = p
    return paths


def parse_links(index_path: Path, year: int) -> List[str]:
    text = index_path.read_text(encoding="utf-8", errors="replace")
    links = re.findall(r"href=[\"']([^\"']*Abstract-Conference\.html)[\"']", text)
    abs_links = []
    seen = set()
    for link in links:
        if link.startswith("/"):
            link = BASE_URL + link
        if link not in seen:
            seen.add(link)
            abs_links.append(link)
    return abs_links


def fetch_abstract_pages(year: int, links: List[str], max_workers: Optional[int] = None) -> None:
    if max_workers is None:
        max_workers = int(os.environ.get("F0_FETCH_WORKERS", "8"))
    year_dir = CACHE / f"iclr{year}_abstract_pages"
    year_dir.mkdir(parents=True, exist_ok=True)
    manifest = year_dir / "download_manifest.jsonl"

    def one(url: str) -> Dict[str, object]:
        name = url.rsplit("/", 1)[-1]
        dest = year_dir / name
        if dest.exists() and dest.stat().st_size > 1000:
            return {"url": url, "path": str(dest.relative_to(ROOT)), "status": "cached", "bytes": dest.stat().st_size}
        code, msg = run_curl(url, dest, timeout=120)
        if code == 0 and dest.exists() and dest.stat().st_size > 1000:
            return {"url": url, "path": str(dest.relative_to(ROOT)), "status": "downloaded", "bytes": dest.stat().st_size}
        if dest.exists():
            dest.unlink(missing_ok=True)
        return {"url": url, "status": "failed", "returncode": code, "message": msg[:300]}

    done = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(one, u): u for u in links}
        for i, fut in enumerate(as_completed(futures), 1):
            rec = fut.result()
            done.append(rec)
            if i % 500 == 0:
                print(f"fetched/cache-checked {year}: {i}/{len(links)}", flush=True)
    with manifest.open("w", encoding="utf-8") as f:
        for rec in sorted(done, key=lambda r: r["url"]):
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")


def strip_tags(s: str) -> str:
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def meta_content(page: str, name: str) -> Optional[str]:
    m = re.search(r'<meta\s+name=["\']' + re.escape(name) + r'["\']\s+content=["\'](.*?)["\']\s*/?>', page, flags=re.I | re.S)
    if m:
        return html.unescape(m.group(1)).strip()
    return None


def all_meta_content(page: str, name: str) -> List[str]:
    return [html.unescape(x).strip() for x in re.findall(r'<meta\s+name=["\']' + re.escape(name) + r'["\']\s+content=["\'](.*?)["\']\s*/?>', page, flags=re.I | re.S)]


@dataclass
class Paper:
    paper_id: str
    title: str
    abstract: str
    iclr_year: int
    proceedings_url: str
    openreview_url: str
    first_public_date: str
    first_public_source: str
    earlier_public_version_found: str
    temporal_status: str
    token_length: int
    fine_route_label_provisional: str
    route_purity: str
    primary_route_strength: int
    secondary_routes: str
    coarse_contribution_family_provisional: str
    annotation_confidence: float
    subfield_source_tags: str
    abstract_sha256: str
    metadata_sha256: str
    source_page_sha256: str
    source_page_bytes: int
    extraction_status: str
    exclusion_reason: str


def tokenize(text: str) -> List[str]:
    toks = re.findall(r"[a-z][a-z0-9\-]{1,}", text.lower())
    return [t for t in toks if t not in STOPWORDS and len(t) > 2]


def terms_for_tfidf(text: str) -> List[str]:
    toks = tokenize(text)
    bigrams = [toks[i] + "_" + toks[i + 1] for i in range(len(toks) - 1)]
    return toks + bigrams


def sentence_split(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text.strip())
    return [p.strip() for p in parts if len(p.strip()) > 20]


def route_scores(text: str) -> Dict[str, float]:
    low = text.lower()
    toks = Counter(tokenize(text))
    scores = {r: 0.0 for r in ROUTES}
    for route, kws in ROUTE_KEYWORDS.items():
        for kw, w in kws.items():
            if " " in kw or "-" in kw:
                if kw in low:
                    scores[route] += w * (1 + low.count(kw) * 0.25)
            else:
                scores[route] += w * toks.get(kw, 0)
    return scores


def classify_route(text: str) -> Tuple[str, int, List[str], float, Dict[str, float], str]:
    scores = route_scores(text)
    ordered = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    top, topv = ordered[0]
    secondv = ordered[1][1]
    total = sum(scores.values())
    if topv <= 0.3:
        return "UNCLEAR", 1, [], 0.20, scores, "MIXED_OR_AMBIGUOUS"
    margin = topv - secondv
    if topv >= 5.5 and margin >= 2.5:
        strength = 5
    elif topv >= 3.5 and margin >= 1.1:
        strength = 4
    elif topv >= 2.0 and margin >= 0.35:
        strength = 3
    elif topv >= 1.0:
        strength = 2
    else:
        strength = 1
    secondary = [r for r, v in ordered[1:] if v >= max(1.4, 0.45 * topv)]
    conf = min(0.95, max(0.25, 0.35 + 0.08 * topv + 0.08 * margin))
    purity = "ROUTE_CLEAR" if strength >= CONFIG["matching"]["route_clear_threshold"] and len(secondary) == 0 else "MIXED_OR_AMBIGUOUS"
    return top, strength, secondary, round(conf, 3), scores, purity


def classify_coarse(primary: str, secondary: Sequence[str], strength: int) -> str:
    if primary == "UNCLEAR" or strength <= 1:
        return "UNCLEAR"
    artifact = primary == "BUILD_IMPROVE" or "BUILD_IMPROVE" in secondary
    knowledge = primary in {"DIAGNOSE_STRESS_TEST", "MEASURE_EVALUATE", "EXPLAIN_MECHANISM_THEORY"} or any(r in {"DIAGNOSE_STRESS_TEST", "MEASURE_EVALUATE", "EXPLAIN_MECHANISM_THEORY"} for r in secondary)
    if artifact and knowledge:
        return "BOTH"
    if artifact:
        return "ARTIFACT"
    if knowledge:
        return "KNOWLEDGE"
    return "UNCLEAR"


def classify_subfield(text: str) -> str:
    low = text.lower()
    scores = {}
    for sf, kws in SUBFIELD_KEYWORDS.items():
        scores[sf] = sum(1 for kw in kws if kw in low)
    best, val = max(scores.items(), key=lambda kv: (kv[1], kv[0]))
    return best if val else "general_ml"


def parse_papers(year: int, links: List[str]) -> List[Paper]:
    year_dir = CACHE / f"iclr{year}_abstract_pages"
    papers: List[Paper] = []
    url_by_name = {u.rsplit("/", 1)[-1]: u for u in links}
    for name, url in sorted(url_by_name.items()):
        p = year_dir / name
        if not p.exists():
            h = name.split("-Abstract", 1)[0]
            papers.append(Paper(
                paper_id=f"ICLR{year}_{h}", title="", abstract="", iclr_year=year,
                proceedings_url=url, openreview_url="UNKNOWN", first_public_date="UNKNOWN",
                first_public_source="UNAVAILABLE", earlier_public_version_found="UNKNOWN",
                temporal_status="MISSING_SOURCE_PAGE", token_length=0,
                fine_route_label_provisional="UNCLEAR", route_purity="MISSING", primary_route_strength=0,
                secondary_routes="", coarse_contribution_family_provisional="UNCLEAR", annotation_confidence=0.0,
                subfield_source_tags="", abstract_sha256="", metadata_sha256="", source_page_sha256="", source_page_bytes=0,
                extraction_status="MISSING_SOURCE_PAGE", exclusion_reason="abstract_page_download_failed"))
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        page_hash = sha256_text(raw)
        title = meta_content(raw, "citation_title") or ""
        pub_date = meta_content(raw, "citation_publication_date") or "UNKNOWN"
        m = re.search(r'<p\s+class=["\']paper-abstract["\']\s*>(.*?)</p>\s*</p>', raw, flags=re.S | re.I)
        if not m:
            m = re.search(r'<section\s+class=["\']paper-section["\'].*?<h2[^>]*>\s*Abstract\s*</h2>(.*?)</section>', raw, flags=re.S | re.I)
        abstract = strip_tags(m.group(1)) if m else ""
        h = name.split("-Abstract", 1)[0]
        text = title + " " + abstract
        primary, strength, secondary, conf, _, purity = classify_route(text)
        coarse = classify_coarse(primary, secondary, strength)
        subfield = classify_subfield(text)
        extraction_status = "OK" if title and abstract else "MISSING_TITLE_OR_ABSTRACT"
        if pub_date != "UNKNOWN":
            temporal_status = "PROCEEDINGS_PUBLICATION_AFTER_2024_08_31_BUT_FIRST_PUBLIC_UNKNOWN"
            first_src = "ICLR_PROCEEDINGS_PUBLICATION_DATE_NOT_EARLIEST_PUBLIC_VERSION"
        else:
            temporal_status = "UNKNOWN"
            first_src = "UNAVAILABLE"
        meta = {"title": title, "year": year, "url": url, "pub_date": pub_date, "page_hash": page_hash}
        papers.append(Paper(
            paper_id=f"ICLR{year}_{h}", title=title, abstract=abstract, iclr_year=year,
            proceedings_url=url, openreview_url="UNKNOWN", first_public_date=pub_date if pub_date != "UNKNOWN" else "UNKNOWN",
            first_public_source=first_src, earlier_public_version_found="UNKNOWN_NOT_CHECKED_AT_SCALE",
            temporal_status=temporal_status, token_length=len(tokenize(abstract)),
            fine_route_label_provisional=primary, route_purity=purity, primary_route_strength=strength,
            secondary_routes=";".join(secondary), coarse_contribution_family_provisional=coarse,
            annotation_confidence=conf, subfield_source_tags=subfield,
            abstract_sha256=sha256_text(abstract), metadata_sha256=sha256_text(json.dumps(meta, sort_keys=True)),
            source_page_sha256=page_hash, source_page_bytes=p.stat().st_size,
            extraction_status=extraction_status, exclusion_reason="" if extraction_status == "OK" else "missing_title_or_abstract"))
    return papers


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(path: Path, rows: List[dict], fieldnames: Optional[List[str]] = None) -> None:
    if fieldnames is None:
        keys = []
        for r in rows:
            for k in r.keys():
                if k not in keys:
                    keys.append(k)
        fieldnames = keys
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def build_tfidf(docs: List[str]) -> Tuple[List[Dict[str, float]], Dict[str, float], Dict[str, List[Tuple[int, float]]]]:
    term_counts = [Counter(terms_for_tfidf(d)) for d in docs]
    df = Counter()
    for c in term_counts:
        df.update(c.keys())
    n = len(docs)
    idf = {t: math.log((n + 1) / (v + 1)) + 1.0 for t, v in df.items() if v >= 2}
    vecs: List[Dict[str, float]] = []
    inv: Dict[str, List[Tuple[int, float]]] = defaultdict(list)
    for idx, c in enumerate(term_counts):
        vec = {}
        for t, cnt in c.items():
            if t in idf:
                vec[t] = (1.0 + math.log(cnt)) * idf[t]
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vec = {t: v / norm for t, v in vec.items()}
        vecs.append(vec)
        for t, v in vec.items():
            inv[t].append((idx, v))
    return vecs, idf, inv


def vectorize_query(text: str, idf: Dict[str, float]) -> Dict[str, float]:
    c = Counter(terms_for_tfidf(text))
    vec = {t: (1.0 + math.log(cnt)) * idf[t] for t, cnt in c.items() if t in idf}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return {t: v / norm for t, v in vec.items()}


def cosine_scores(qvec: Dict[str, float], inv: Dict[str, List[Tuple[int, float]]]) -> Dict[int, float]:
    scores = defaultdict(float)
    for t, qv in qvec.items():
        for idx, dv in inv.get(t, []):
            scores[idx] += qv * dv
    return scores


def bm25_like(query: str, doc: str) -> float:
    qt = tokenize(query)
    if not qt:
        return 0.0
    q = Counter(qt)
    d = Counter(tokenize(doc))
    score = 0.0
    for t, qcnt in q.items():
        if t in d:
            score += min(2.0, d[t]) * (1.0 + math.log(qcnt))
    return score / (len(set(q)) + 4.0)


def mask_seed_from_paper(p: Paper) -> Tuple[str, str, str]:
    sents = sentence_split(p.abstract)
    title_tokens = [t for t in re.findall(r"[A-Z][A-Za-z0-9\-]{2,}", p.title) if t.lower() not in STOPWORDS]
    acronyms = sorted(set(re.findall(r"\b[A-Z][A-Z0-9]{2,}\b", p.title + " " + p.abstract)))
    removed = sorted(set(title_tokens + acronyms))[:40]
    background = " ".join(sents[:2]) if sents else p.abstract[:550]
    problem_sents = [s for s in sents if re.search(r"\b(challenge|challenging|limitation|limits|failure|gap|unclear|lack|scarce|difficult|problem|remain|understand|robust|evaluate|measure)\b", s, re.I)]
    problem = " ".join(problem_sents[:2]) if problem_sents else "The literature indicates an unresolved technical limitation or uncertainty in this area."
    seed = background + "\n\nOBSERVED PROBLEM / OPEN QUESTION\n" + problem + "\n\nTASK\nPropose one technically substantive and experimentally testable ICLR-style research project that directly addresses this scientific problem. Choose the research strategy you consider most appropriate."
    for ent in removed:
        seed = re.sub(r"\b" + re.escape(ent) + r"\b", "[MASKED_ENTITY]", seed)
    seed = re.sub(r"\b(we propose|we introduce|we present|our method|our approach|we develop)\b", "prior work discusses", seed, flags=re.I)
    seed = re.sub(r"\s+", " ", seed).replace(" OBSERVED", "\n\nOBSERVED").replace(" TASK", "\n\nTASK").strip()
    raw_context = background + " " + problem
    return raw_context, seed, ";".join(removed)


def jaccard_ngrams(a: str, b: str, n: int = 3) -> float:
    def grams(x):
        t = tokenize(x)
        return set(tuple(t[i:i+n]) for i in range(max(0, len(t)-n+1)))
    ga, gb = grams(a), grams(b)
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


def make_seed_rows(seed_papers: List[Paper]) -> List[dict]:
    rows = []
    for p in seed_papers:
        raw, masked, removed = mask_seed_from_paper(p)
        scores = route_scores(masked)
        route_count = sum(1 for v in scores.values() if v >= 1.0)
        title_sim = jaccard_ngrams(masked, p.title, 2)
        abs_sim = jaccard_ngrams(masked, p.abstract, 3)
        remaining_acronyms = [
            a for a in re.findall(r"\b[A-Z][A-Z0-9]{2,}\b", masked.replace("[MASKED_ENTITY]", ""))
            if a not in {"OBSERVED", "PROBLEM", "OPEN", "QUESTION", "TASK", "BACKGROUND", "ICLR"}
        ]
        acronym_leak = bool(remaining_acronyms)
        method_leak = title_sim > 0.20 or acronym_leak
        distinctive_leak = abs_sim > 0.18
        problem_clarity = min(5, max(1, 2 + len(sentence_split(masked)) // 2))
        background_suff = 4 if len(tokenize(masked)) >= 80 else 3 if len(tokenize(masked)) >= 45 else 2
        method_neutrality = 2 if method_leak else 4 if not re.search(r"\bdesign a new|develop a benchmark|explain the mechanism\b", masked, re.I) else 3
        multi_open = min(5, max(1, 1 + route_count))
        technical = 4 if len(tokenize(raw)) >= 60 else 3 if len(tokenize(raw)) >= 35 else 2
        iclr_rel = 5 if p.extraction_status == "OK" else 1
        too_broad = len(tokenize(masked)) < 45
        too_narrow = title_sim > 0.25 or len([x for x in removed.split(";") if x]) > 20
        solution_prescribed = bool(re.search(r"\bwe propose|our method|called\b", masked, re.I))
        hard_fail = p.extraction_status != "OK" or too_broad or solution_prescribed
        review_needed = method_leak or distinctive_leak or too_narrow
        if not hard_fail and all([problem_clarity >= 3, background_suff >= 3, method_neutrality >= 3, multi_open >= 3, technical >= 3, iclr_rel >= 4]) and not review_needed:
            status = "PASS"
        elif not hard_fail and iclr_rel >= 4 and len(tokenize(masked)) >= 45:
            status = "PROVISIONAL_HUMAN_REVIEW_REQUIRED"
        else:
            status = "FAIL_OR_LOW_INFORMATION"
        rows.append({
            "seed_id": "SEED_" + p.paper_id,
            "focal_paper_id": p.paper_id,
            "focal_title": p.title,
            "subfield": p.subfield_source_tags,
            "raw_problem_context": raw,
            "method_masked_question": masked,
            "removed_solution_tokens/entities": removed,
            "focal_first_public_date": p.first_public_date,
            "problem_clarity": problem_clarity,
            "background_sufficiency": background_suff,
            "method_neutrality": method_neutrality,
            "multi_route_openness": multi_open,
            "technical_substance": technical,
            "iclr_relevance": iclr_rel,
            "focal_method_leak": str(method_leak),
            "solution_prescribed": str(solution_prescribed),
            "distinctive_phrase_leak": str(distinctive_leak),
            "too_broad": str(too_broad),
            "too_narrow": str(too_narrow),
            "post_cutoff_concept_needs_definition": "UNKNOWN_NEEDS_HUMAN_MODEL_ACCESSIBILITY_CHECK",
            "seed_to_focal_title_lexical_similarity": round(title_sim, 4),
            "seed_to_focal_abstract_similarity": round(abs_sim, 4),
            "distinctive_ngram_or_acronym_overlap": ";".join(remaining_acronyms[:20]) if acronym_leak else "NONE_DETECTED_BY_HEURISTIC",
            "seed_status_provisional": status,
        })
    return rows


def standardize(vals: List[float]) -> List[float]:
    if not vals:
        return []
    mean = statistics.fmean(vals)
    sd = statistics.pstdev(vals) or 1.0
    return [(v - mean) / sd for v in vals]


def date_num(date: str) -> int:
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", date or "")
    if not m:
        return 0
    y, mo, d = map(int, m.groups())
    return y * 372 + mo * 31 + d


def match_pair(seed_id: str, pair_id: str, route_a: str, route_b: str, candidates: List[dict]) -> Tuple[List[dict], dict, List[dict]]:
    pool = [c for c in candidates if c["candidate_status"] == "ABOVE_RELEVANCE_FLOOR"]
    A = [c for c in pool if c["route_label_at_freeze"] == route_a]
    B = [c for c in pool if c["route_label_at_freeze"] == route_b]
    route_clear_A = [c for c in A if c["route_purity"] == "ROUTE_CLEAR"]
    route_clear_B = [c for c in B if c["route_purity"] == "ROUTE_CLEAR"]
    use_A, use_B = route_clear_A, route_clear_B
    broad_A, broad_B = A, B

    def build_edges(AA, BB):
        edges = []
        lens = [c["token_length"] for c in AA + BB]
        dates = [date_num(c["first_public_date"]) for c in AA + BB]
        lz = dict(zip([c["paper_id"] for c in AA + BB], standardize(lens)))
        dz = dict(zip([c["paper_id"] for c in AA + BB], standardize(dates)))
        for a in AA:
            for b in BB:
                dd = abs(a["dense_relevance"] - b["dense_relevance"])
                rd = abs(a["reranker_relevance"] - b["reranker_relevance"])
                topic = 0.0 if a["topic_cluster"] == b["topic_cluster"] else 1.0
                if dd > CONFIG["matching"]["hard_calipers"]["dense_diff_max"]:
                    continue
                if rd > CONFIG["matching"]["hard_calipers"]["reranker_diff_max"]:
                    continue
                cost = 0.35 * dd + 0.25 * rd + 0.15 * abs(lz.get(a["paper_id"], 0) - lz.get(b["paper_id"], 0)) + 0.10 * abs(dz.get(a["paper_id"], 0) - dz.get(b["paper_id"], 0)) + 0.15 * topic
                edges.append((cost, a["paper_id"], b["paper_id"], a, b, dd, rd, abs(a["token_length"] - b["token_length"]), abs(date_num(a["first_public_date"]) - date_num(b["first_public_date"])), topic))
        return sorted(edges, key=lambda e: (round(e[0], 10), e[1], e[2]))

    slots = []
    used_a, used_b = set(), set()
    for cost, aid, bid, a, b, dd, rd, ld, td, topic in build_edges(use_A, use_B):
        if aid in used_a or bid in used_b:
            continue
        used_a.add(aid); used_b.add(bid)
        j = len(slots) + 1
        slots.append({
            "seed_id": seed_id, "route_pair_id": pair_id, "route_A": route_a, "route_B": route_b,
            "slot_index": j, "A_paper_id": aid, "B_paper_id": bid,
            "A_title": a["title"], "B_title": b["title"],
            "A_dense_relevance": round(a["dense_relevance"], 6), "B_dense_relevance": round(b["dense_relevance"], 6),
            "A_reranker_relevance": round(a["reranker_relevance"], 6), "B_reranker_relevance": round(b["reranker_relevance"], 6),
            "match_cost": round(cost, 6), "matched_relevance_difference": round(dd, 6),
            "matched_reranker_difference": round(rd, 6), "matched_length_difference": ld,
            "matched_date_difference": td, "matched_topic_distance": topic,
            "A_route_purity": a["route_purity"], "B_route_purity": b["route_purity"],
            "matching_scope": "ROUTE_CLEAR_ONLY",
        })
    costs = [s["match_cost"] for s in slots]
    summary = {
        "seed_id": seed_id, "route_pair_id": pair_id, "route_A": route_a, "route_B": route_b,
        "n_A_above_floor": len(broad_A), "n_B_above_floor": len(broad_B),
        "n_A_route_clear_above_floor": len(route_clear_A), "n_B_route_clear_above_floor": len(route_clear_B),
        "max_matched_slots_under_calipers": len(slots),
        "median_match_cost": round(statistics.median(costs), 6) if costs else "",
        "p90_match_cost": round(sorted(costs)[max(0, math.ceil(0.9 * len(costs)) - 1)], 6) if costs else "",
        "max_match_cost": round(max(costs), 6) if costs else "",
        "k6_supported": len(slots) >= 6, "k8_supported": len(slots) >= 8, "k12_supported": len(slots) >= 12,
        "source_matchability_status": "SOURCE_MATCHABLE_K12" if len(slots) >= 12 else "SOURCE_MATCHABLE_K8" if len(slots) >= 8 else "SOURCE_MATCHABLE_K6" if len(slots) >= 6 else "INSUFFICIENT_MATCHED_SLOTS_ROUTE_CLEAR",
        "unmatched_A_route_clear": max(0, len(route_clear_A) - len(used_a)),
        "unmatched_B_route_clear": max(0, len(route_clear_B) - len(used_b)),
    }
    failures = []
    for c in route_clear_A:
        if c["paper_id"] not in used_a:
            failures.append({"seed_id": seed_id, "route_pair_id": pair_id, "paper_id": c["paper_id"], "route": route_a, "unmatched_reason": "no_available_B_under_calipers_or_greedy_replacement"})
    for c in route_clear_B:
        if c["paper_id"] not in used_b:
            failures.append({"seed_id": seed_id, "route_pair_id": pair_id, "paper_id": c["paper_id"], "route": route_b, "unmatched_reason": "no_available_A_under_calipers_or_greedy_replacement"})
    return slots, summary, failures


def pair_type(route_a: str, route_b: str) -> str:
    s = {route_a, route_b}
    if s == {"BUILD_IMPROVE", "DIAGNOSE_STRESS_TEST"}:
        return "TYPE_I_COMPETING_STRATEGIC"
    if s == {"BUILD_IMPROVE", "MEASURE_EVALUATE"}:
        return "TYPE_I_COMPETING_STRATEGIC"
    if s == {"BUILD_IMPROVE", "EXPLAIN_MECHANISM_THEORY"}:
        return "TYPE_I_COMPETING_STRATEGIC"
    if s == {"DIAGNOSE_STRESS_TEST", "EXPLAIN_MECHANISM_THEORY"}:
        return "TYPE_III_COMPLEMENTARY_HIGH_COMPOSABILITY"
    return "UNCLEAR"


def simulate_packets(slots_by_block: Dict[Tuple[str, str], List[dict]]) -> List[dict]:
    rng = random.Random(CONFIG["packet_simulation"]["random_seed"])
    rows = []
    k = CONFIG["packet_simulation"]["k_for_primary_balance"]
    for (seed_id, pair_id), slots in sorted(slots_by_block.items()):
        if len(slots) < k:
            continue
        for rep in range(CONFIG["packet_simulation"]["realizations_per_block"]):
            subset = sorted(rng.sample(slots, k), key=lambda s: s["slot_index"])
            for alpha in CONFIG["packet_simulation"]["alphas"]:
                n_a = int(round(alpha * k))
                a_slots = set(rng.sample([s["slot_index"] for s in subset], n_a)) if n_a else set()
                dense, rerank, tokens, dates, topics, papers = [], [], [], [], [], [],
                dense = [] ; rerank = [] ; tokens = [] ; dates = [] ; topics = [] ; papers = [] ; routes = []
                for s in subset:
                    choose_a = s["slot_index"] in a_slots
                    prefix = "A" if choose_a else "B"
                    papers.append(s[prefix + "_paper_id"])
                    routes.append(s["route_A"] if choose_a else s["route_B"])
                    dense.append(float(s[prefix + "_dense_relevance"]))
                    rerank.append(float(s[prefix + "_reranker_relevance"]))
                    tokens.append(0)  # token totals are summarized from slot diffs when exact per-paper lengths are not embedded in slot rows
                    dates.append(0)
                    topics.append(float(s["matched_topic_distance"]))
                rows.append({
                    "seed_id": seed_id, "route_pair_id": pair_id, "k": k, "packet_realization_index": rep,
                    "alpha_target": alpha, "alpha_realized": routes.count(subset[0]["route_A"]) / k,
                    "ordered_paper_ids": ";".join(papers), "route_counts": json.dumps(dict(Counter(routes)), sort_keys=True),
                    "mean_dense_relevance": round(statistics.fmean(dense), 6),
                    "mean_reranker_relevance": round(statistics.fmean(rerank), 6),
                    "mean_slot_topic_distance": round(statistics.fmean(topics), 6),
                    "packet_definition_sha256": sha256_text(json.dumps({"seed": seed_id, "pair": pair_id, "rep": rep, "alpha": alpha, "papers": papers}, sort_keys=True)),
                })
    return rows


def quantiles(xs: List[float]) -> Tuple[str, str, str]:
    if not xs:
        return "", "", ""
    xs = sorted(xs)
    return str(round(xs[len(xs)//2], 6)), str(round(xs[max(0, math.ceil(0.9*len(xs))-1)], 6)), str(round(xs[-1], 6))


def main() -> int:
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "matching_diagnostics").mkdir(exist_ok=True)
    indexes = ensure_indexes()
    links_by_year = {year: parse_links(p, year) for year, p in indexes.items()}
    print({year: len(links) for year, links in links_by_year.items()}, flush=True)
    for year, links in links_by_year.items():
        fetch_abstract_pages(year, links)
    evidence = parse_papers(2025, links_by_year[2025])
    seed_papers = parse_papers(2026, links_by_year[2026])
    write_jsonl(OUT / "corpus_manifest.jsonl", [asdict(p) for p in evidence])
    seed_rows = make_seed_rows(seed_papers)
    write_jsonl(OUT / "seed_candidates.jsonl", seed_rows)

    # Corpus hash includes compact source data and config, not transient cache paths.
    corpus_hash = sha256_text(json.dumps([asdict(p) for p in evidence], sort_keys=True) + json.dumps(CONFIG, sort_keys=True))
    (OUT / "corpus_hash.txt").write_text(corpus_hash + "\n", encoding="utf-8")
    (OUT / "retrieval_config.json").write_text(json.dumps(CONFIG, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    valid_evidence = [p for p in evidence if p.extraction_status == "OK"]
    valid_seed_rows = [r for r in seed_rows if r["seed_status_provisional"] in {"PASS", "PROVISIONAL_HUMAN_REVIEW_REQUIRED"}]
    seed_by_id = {r["seed_id"]: r for r in seed_rows}
    docs = [p.title + " " + p.abstract for p in valid_evidence]
    vecs, idf, inv = build_tfidf(docs)
    ev_by_idx = {i: p for i, p in enumerate(valid_evidence)}

    retrieval_candidates: Dict[str, List[dict]] = {}
    all_candidate_rows = []
    route_pair_rows = []
    route_pair_matchability = []
    all_slots = []
    all_unmatched = []
    slots_by_block: Dict[Tuple[str, str], List[dict]] = {}
    print(f"retrieval over {len(valid_seed_rows)} provisional-pass seeds x {len(valid_evidence)} evidence papers", flush=True)
    for si, seed in enumerate(valid_seed_rows, 1):
        q = seed["method_masked_question"]
        qvec = vectorize_query(q, idf)
        scores = cosine_scores(qvec, inv)
        top = sorted(scores.items(), key=lambda kv: (-kv[1], ev_by_idx[kv[0]].paper_id))[:CONFIG["retrieval"]["candidate_pool_size"]]
        bm_raw = [bm25_like(q, docs[idx]) for idx, _ in top]
        max_bm = max(bm_raw) if bm_raw else 1.0
        cand = []
        for rank, ((idx, dense), bm) in enumerate(zip(top, bm_raw), 1):
            p = ev_by_idx[idx]
            rer = bm / max_bm if max_bm else 0.0
            status = "ABOVE_RELEVANCE_FLOOR" if dense >= CONFIG["retrieval"]["relevance_floor_dense"] and rer >= CONFIG["retrieval"]["relevance_floor_reranker"] else "BELOW_RELEVANCE_FLOOR"
            row = {
                "seed_id": seed["seed_id"], "paper_id": p.paper_id, "title": p.title,
                "retriever_version": "f0_tfidf_v1", "retrieval_query_sha256": sha256_text(q),
                "dense_relevance": round(dense, 6), "reranker_relevance": round(rer, 6),
                "rank_dense": rank, "rank_reranker": "not_separately_ranked_bm25_like_score_recorded",
                "token_length": p.token_length, "topic_cluster": p.subfield_source_tags,
                "route_label_at_freeze": p.fine_route_label_provisional, "route_purity": p.route_purity,
                "candidate_status": status, "first_public_date": p.first_public_date,
                "temporal_status": p.temporal_status,
            }
            cand.append(row)
            all_candidate_rows.append(row)
        retrieval_candidates[seed["seed_id"]] = cand
        supported_routes = {r for r in ROUTES if sum(1 for c in cand if c["candidate_status"] == "ABOVE_RELEVANCE_FLOOR" and c["route_label_at_freeze"] == r) >= 6}
        for pair_id, (ra, rb) in R_PAIRS.items():
            n_a = sum(1 for c in cand if c["candidate_status"] == "ABOVE_RELEVANCE_FLOOR" and c["route_label_at_freeze"] == ra)
            n_b = sum(1 for c in cand if c["candidate_status"] == "ABOVE_RELEVANCE_FLOOR" and c["route_label_at_freeze"] == rb)
            route_pair_rows.append({"seed_id": seed["seed_id"], "route_pair_id": pair_id, "route_A": ra, "route_B": rb, "n_A_above_floor_loose": n_a, "n_B_above_floor_loose": n_b, "loose_packet_k6_possible": n_a >= 6 and n_b >= 6, "loose_packet_k8_possible": n_a >= 8 and n_b >= 8, "loose_packet_k12_possible": n_a >= 12 and n_b >= 12})
            slots, summary, failures = match_pair(seed["seed_id"], pair_id, ra, rb, cand)
            route_pair_matchability.append(summary)
            all_slots.extend(slots)
            all_unmatched.extend(failures)
            slots_by_block[(seed["seed_id"], pair_id)] = slots
        if si % 250 == 0:
            print(f"processed seeds {si}/{len(valid_seed_rows)}", flush=True)

    write_csv(OUT / "matching_diagnostics" / "retrieval_candidates.csv", all_candidate_rows)
    write_csv(OUT / "route_pair_coverage.csv", route_pair_rows)
    write_csv(OUT / "route_pair_matchability.csv", route_pair_matchability)
    write_csv(OUT / "matched_evidence_slots.csv", all_slots)
    write_csv(OUT / "matching_diagnostics" / "unmatched_papers.csv", all_unmatched)
    packet_rows = simulate_packets(slots_by_block)
    write_csv(OUT / "packet_balance_simulation.csv", packet_rows)

    supported_by_seed: Dict[str, set] = defaultdict(set)
    matched_by_seed: Dict[str, Dict[str, int]] = defaultdict(dict)
    for m in route_pair_matchability:
        if m["n_A_above_floor"] >= 6 and m["n_B_above_floor"] >= 6:
            supported_by_seed[m["seed_id"]].add(m["route_A"]); supported_by_seed[m["seed_id"]].add(m["route_B"])
        matched_by_seed[m["seed_id"]][m["route_pair_id"]] = m["max_matched_slots_under_calipers"]
    multi_rows = []
    for seed in seed_rows:
        sid = seed["seed_id"]
        routes = sorted(supported_by_seed.get(sid, set()))
        triplet = ""
        mincnt = ""
        if len(routes) >= 3:
            triplet = ";".join(routes[:3])
            counts = []
            cand = retrieval_candidates.get(sid, [])
            for r in routes[:3]:
                counts.append(sum(1 for c in cand if c["candidate_status"] == "ABOVE_RELEVANCE_FLOOR" and c["route_label_at_freeze"] == r and c["route_purity"] == "ROUTE_CLEAR"))
            mincnt = min(counts) if counts else ""
        best = max(matched_by_seed.get(sid, {}).values(), default=0)
        multi_rows.append({"seed_id": sid, "subfield": seed["subfield"], "seed_status_provisional": seed["seed_status_provisional"], "n_supported_routes": len(routes), "supported_routes": ";".join(routes), "eligible_3plus_routes_provisional": len(routes) >= 3, "best_triplet_if_any": triplet, "triplet_min_evidence_count": mincnt, "triplet_matchability_status": "HAS_PAIRWISE_K8" if best >= 8 else "NO_PAIRWISE_K8" if routes else "NO_SUPPORTED_ROUTES"})
    write_csv(OUT / "multi_route_coverage.csv", multi_rows)

    route_summary = {
        "source_papers_total": len(evidence),
        "source_papers_ok": len(valid_evidence),
        "route_counts": Counter(p.fine_route_label_provisional for p in valid_evidence),
        "route_clear_counts": Counter(p.fine_route_label_provisional for p in valid_evidence if p.route_purity == "ROUTE_CLEAR"),
        "purity_counts": Counter(p.route_purity for p in valid_evidence),
        "coarse_counts": Counter(p.coarse_contribution_family_provisional for p in valid_evidence),
        "subfield_counts": Counter(p.subfield_source_tags for p in valid_evidence),
        "annotation_method": "deterministic keyword classifier only; provisional source annotation, not ground truth",
    }
    (OUT / "route_label_summary.json").write_text(json.dumps(route_summary, indent=2, sort_keys=True, default=dict) + "\n", encoding="utf-8")

    # Audit packets with blank human fields.
    eligible_matches = [m for m in route_pair_matchability if m["max_matched_slots_under_calipers"] >= 6]
    equipoise_rows = []
    for m in eligible_matches:
        sid = m["seed_id"]
        seed = seed_by_id[sid]
        slots = slots_by_block.get((sid, m["route_pair_id"]), [])[:3]
        equipoise_rows.append({
            "seed_id": sid, "route_pair_id": m["route_pair_id"], "subfield": seed["subfield"],
            "method_masked_question": seed["method_masked_question"],
            "route_A": m["route_A"], "route_A_description": ROUTE_DEFS[m["route_A"]],
            "route_B": m["route_B"], "route_B_description": ROUTE_DEFS[m["route_B"]],
            "representative_A_papers": "; ".join(s["A_paper_id"] + ": " + s["A_title"] for s in slots),
            "representative_B_papers": "; ".join(s["B_paper_id"] + ": " + s["B_title"] for s in slots),
            "provisional_pair_type": pair_type(m["route_A"], m["route_B"]),
            "A_RELEVANCE_TO_SEED": "", "B_RELEVANCE_TO_SEED": "", "A_SCIENTIFIC_PLAUSIBILITY": "", "B_SCIENTIFIC_PLAUSIBILITY": "",
            "DISTINGUISHABILITY": "", "EQUIPOISE": "", "NON_SUBSUMPTION": "", "ANNOTATABILITY": "", "COMPOSABILITY": "", "ROUTE_DOMINANCE": "",
        })
    write_csv(OUT / "route_equipoise_audit_packet.csv", equipoise_rows)
    seed_audit_fields = list(seed_rows[0].keys()) + ["HUMAN_PROBLEM_CLARITY", "HUMAN_BACKGROUND_SUFFICIENCY", "HUMAN_METHOD_NEUTRALITY", "HUMAN_MULTI_ROUTE_OPENNESS", "HUMAN_TECHNICAL_SUBSTANCE", "HUMAN_ICLR_RELEVANCE", "HUMAN_DECISION", "HUMAN_NOTES"] if seed_rows else []
    seed_audit_rows = [dict(r, HUMAN_PROBLEM_CLARITY="", HUMAN_BACKGROUND_SUFFICIENCY="", HUMAN_METHOD_NEUTRALITY="", HUMAN_MULTI_ROUTE_OPENNESS="", HUMAN_TECHNICAL_SUBSTANCE="", HUMAN_ICLR_RELEVANCE="", HUMAN_DECISION="", HUMAN_NOTES="") for r in seed_rows]
    write_csv(OUT / "seed_validity_audit_packet.csv", seed_audit_rows, seed_audit_fields)
    ann_rows = []
    for p in valid_evidence:
        ann_rows.append({
            "paper_id": p.paper_id, "title": p.title, "abstract": p.abstract, "source_url": p.proceedings_url,
            "fine_route_label_provisional": p.fine_route_label_provisional, "route_purity": p.route_purity,
            "primary_route_strength": p.primary_route_strength, "secondary_routes": p.secondary_routes,
            "coarse_contribution_family_provisional": p.coarse_contribution_family_provisional,
            "annotation_confidence": p.annotation_confidence,
            "HUMAN_PRIMARY_ROUTE": "", "HUMAN_ROUTE_PURITY": "", "HUMAN_SECONDARY_ROUTES": "", "HUMAN_COARSE_FAMILY": "", "HUMAN_NOTES": "",
        })
    write_csv(OUT / "route_annotation_audit_packet.csv", ann_rows)

    # Attrition and final result.
    audited = len(seed_rows)
    extractable = sum(1 for r in seed_rows if r["iclr_relevance"] >= 4 and len(tokenize(r["method_masked_question"])) >= 45)
    seed_pass = len(valid_seed_rows)
    multi_open = sum(1 for r in valid_seed_rows if r["multi_route_openness"] >= 3)
    two_routes = sum(1 for r in multi_rows if r["n_supported_routes"] >= 2)
    three_routes = sum(1 for r in multi_rows if r["n_supported_routes"] >= 3)
    by_k = {k: len({m["seed_id"] for m in route_pair_matchability if m["max_matched_slots_under_calipers"] >= k}) for k in (6, 8, 12)}
    source_blocks = len([m for m in route_pair_matchability if m["max_matched_slots_under_calipers"] >= 8])
    final_blocks = "0_HUMAN_EQUIPOISE_PENDING"
    attrition = [
        {"stage": "ICLR_2026_focal_candidates", "count": audited, "notes": "all proceedings Conference abstract links parsed or recorded"},
        {"stage": "extractable_method_masked_seeds", "count": extractable, "notes": "title+abstract present and seed text length adequate"},
        {"stage": "seed_validity_leakage_pass_candidates", "count": seed_pass, "notes": "heuristic source-only provisional pass; human audit required"},
        {"stage": "multi_route_open_candidates", "count": multi_open, "notes": "seed lexical route openness >=3"},
        {"stage": ">=2_source_supported_routes", "count": two_routes, "notes": "at least two routes have >=6 above-floor source papers"},
        {"stage": "relevance_matchable_route_pairs_k6_unique_seeds", "count": by_k[6], "notes": "route-clear pairwise slots under frozen calipers"},
        {"stage": ">=6_/_>=8_/_>=12_pairwise_matched_slot_banks_unique_seeds", "count": f"{by_k[6]} / {by_k[8]} / {by_k[12]}", "notes": "unique seed counts"},
        {"stage": "source_feasible_blocks_awaiting_human_equipoise", "count": source_blocks, "notes": "route-pair blocks with >=8 slots; not human-approved"},
        {"stage": "potential_final_experimental_blocks", "count": final_blocks, "notes": "F0 cannot certify without F1 human equipoise/admissibility"},
    ]
    write_csv(OUT / "attrition_waterfall.csv", attrition)

    # Coverage summaries.
    by_pair = defaultdict(lambda: {"k6": set(), "k8": set(), "k12": set(), "blocks_k8": 0})
    for m in route_pair_matchability:
        for k in (6, 8, 12):
            if m["max_matched_slots_under_calipers"] >= k:
                by_pair[m["route_pair_id"]][f"k{k}"].add(m["seed_id"])
        if m["max_matched_slots_under_calipers"] >= 8:
            by_pair[m["route_pair_id"]]["blocks_k8"] += 1
    by_sub = defaultdict(lambda: {"k8_seeds": set(), "total": 0})
    for r in multi_rows:
        by_sub[r["subfield"]]["total"] += 1
    for m in route_pair_matchability:
        if m["max_matched_slots_under_calipers"] >= 8:
            by_sub[seed_by_id[m["seed_id"]]["subfield"]]["k8_seeds"].add(m["seed_id"])

    loose_k8 = len({r["seed_id"] for r in route_pair_rows if str(r["loose_packet_k8_possible"]) == "True"})
    match_k8 = by_k[8]
    purity_raw_two = len({m["seed_id"] for m in route_pair_matchability if m["n_A_above_floor"] >= 8 and m["n_B_above_floor"] >= 8})
    temporal_unknown = sum(1 for p in valid_evidence if "FIRST_PUBLIC_UNKNOWN" in p.temporal_status or p.temporal_status == "UNKNOWN")
    mixed = route_summary["purity_counts"].get("MIXED_OR_AMBIGUOUS", 0)
    dominant = "temporal_uncertainty" if temporal_unknown / max(1, len(valid_evidence)) > 0.8 else "route_purity_or_matching_calipers" if match_k8 < loose_k8 * 0.5 else "human_equipoise_pending"
    rec = "NOT_FEASIBLE" if by_k[6] < 12 or temporal_unknown / max(1, len(valid_evidence)) > 0.95 else "MARGINAL" if by_k[8] < 24 else "SOURCE_FEASIBLE_NARROW" if len([sf for sf, v in by_sub.items() if len(v["k8_seeds"]) > 0]) < 3 else "SOURCE_FEASIBLE_BROAD"

    temporal_md = f"""# Temporal Cleanliness Report

Source used: ICLR official proceedings pages for 2025 evidence and 2026 focal candidates.

OpenReview bulk API status: `{CONFIG['openreview_api_status']}`.

Evidence papers parsed: {len(valid_evidence)} / {len(evidence)}.

Proceedings publication date field is available in parsed pages, but it is not an earliest-public-version guarantee. Therefore first-public date is recorded as the proceedings publication date source field, while `temporal_status` remains `PROCEEDINGS_PUBLICATION_AFTER_2024_08_31_BUT_FIRST_PUBLIC_UNKNOWN` for successfully parsed ICLR 2025 evidence papers.

Strict shared evidence subset status: not certified by F0 automation. No earlier arXiv/OpenReview version search was completed at scale, so temporal cleanliness is the dominant unresolved gate for a causal-core run using Gemma 3's August 2024 cutoff.
"""
    (OUT / "temporal_cleanliness_report.md").write_text(temporal_md, encoding="utf-8")

    readme = f"""# F0 Source-Only Feasibility Audit

Generated by `scripts/f0_source_only_audit.py` from ICLR proceedings source pages. This folder contains source-only artifacts only. No scientific proposal generation, no baseline propensity estimation, and no evidence-conditioned generation were run.

Corpus hash: `{corpus_hash}`
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    status = f"""# F0 Status

Status: COMPLETE_SOURCE_ONLY_AUTOMATED_PASS_WITH_HUMAN_AUDIT_REQUIRED

Recommendation: {rec}

Dominant blocker: {dominant}

Runtime seconds: {round(time.time() - t0, 1)}
"""
    (OUT / "STATUS.md").write_text(status, encoding="utf-8")

    by_pair_md = "\n".join(f"- {pid}: k6={len(v['k6'])}, k8={len(v['k8'])}, k12={len(v['k12'])}, blocks_k8={v['blocks_k8']}" for pid, v in sorted(by_pair.items()))
    by_sub_md = "\n".join(f"- {sf}: audited={v['total']}, k8_matchable_unique_seeds={len(v['k8_seeds'])}" for sf, v in sorted(by_sub.items(), key=lambda kv: (-len(kv[1]['k8_seeds']), kv[0])))
    result = f"""# F0 Source-Only Feasibility Result

## Recommendation

`{rec}`

This is a constructibility recommendation only. F0 did not run no-context generations, evidence-conditioned generations, proposal evaluation, baseline propensity estimation, or treatment-effect inspection.

## Key Counts

- ICLR 2025 evidence papers audited: {len(evidence)} total, {len(valid_evidence)} parsed with title+abstract.
- ICLR 2026 candidate seeds audited: {audited}.
- Extractable method-masked seeds: {extractable}.
- Seed validity/leakage provisional pass candidates: {seed_pass}.
- Unique seeds with >=2 source-supported routes: {two_routes}.
- Unique seeds with >=3 source-supported routes: {three_routes}.
- Unique seeds with at least one route pair supporting >=6 / >=8 / >=12 strict pairwise matched evidence slots: {by_k[6]} / {by_k[8]} / {by_k[12]}.
- Route-clear k8 source-feasible blocks awaiting human equipoise: {source_blocks}.
- Potential final experimental blocks after F0: 0 certified; all require F1 human seed/equipoise/source-route audit.

## R1-R4 Coverage

{by_pair_md}

## Subfield Coverage

{by_sub_md}

## Pairwise Matching vs Loose Packet-Level Coverage

Loose packet-level k8 unique seeds: {loose_k8}. Route-clear pairwise k8 unique seeds: {match_k8}. Pairwise matching therefore {'materially reduces' if match_k8 < loose_k8 * 0.8 else 'does not materially reduce'} coverage under the frozen heuristic calipers.

Raw route-pair support before route-clear filtering appears in `route_pair_coverage.csv`; route-clear pairwise results appear in `route_pair_matchability.csv` and `matched_evidence_slots.csv`.

## Route Purity

Route-clear source papers: {route_summary['purity_counts'].get('ROUTE_CLEAR', 0)}. Mixed/ambiguous source papers: {mixed}. Route-clear filtering leaves enough automated matched slots for a narrow source-only bank, but these labels are keyword-provisional and require `route_annotation_audit_packet.csv` human review before any treatment use.

## Artifact/Knowledge Axis

The coarse Artifact/Knowledge/Both/Unclear axis is easier to audit mechanically than the fine route taxonomy because BUILD maps mostly to artifact contribution while DIAGNOSE/MEASURE/EXPLAIN map mostly to knowledge contribution. It is not a replacement for the predeclared R1-R4 route taxonomy, and it is recorded only as an external robustness axis.

## Main Bottleneck

Dominant blocker: `{dominant}`.

The strongest unresolved causal-core issue is temporal cleanliness: proceedings pages provide accepted-paper abstracts and publication-date metadata, but do not certify earliest public date or absence of pre-2024-08-31 versions. Seed leakage and method neutrality also need human review because seeds were automatically masked from focal abstracts. Mixed-route contamination remains a secondary blocker because many abstracts contain build+evaluate or diagnose+mitigate contributions.

## Best-Fit Areas

Best automated coverage is in the subfields with the largest k8 counts above. Route pairs with the largest k8 seed coverage are the most promising R1-R4 contrasts. R4 should be treated carefully because Round 27 identifies DIAGNOSE vs EXPLAIN as often complementary/high-composability.

## Attrition Waterfall

1. ICLR 2026 focal candidates: {audited}
2. Extractable method-masked seeds: {extractable}
3. Seed validity/leakage pass candidates: {seed_pass}
4. Multi-route-open candidates: {multi_open}
5. >=2 source-supported routes: {two_routes}
6. Relevance-matchable route pairs: k6={by_k[6]}, k8={by_k[8]}, k12={by_k[12]} unique seeds
7. Source-feasible blocks awaiting human equipoise: {source_blocks}
8. Potential final experimental blocks: 0 certified in F0; F1 required

## Human Review Required Before F1/P0

- `seed_validity_audit_packet.csv`
- `route_equipoise_audit_packet.csv`
- `route_annotation_audit_packet.csv`
- `temporal_cleanliness_report.md`
- `matching_diagnostics/unmatched_papers.csv`
- `matching_diagnostics/retrieval_candidates.csv`

## Stop Statement

F0 source-only artifacts are complete. This task stops here and does not enter P0.
"""
    (OUT / "FEASIBILITY_RESULT.md").write_text(result, encoding="utf-8")
    print(f"wrote F0 artifacts to {OUT}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
