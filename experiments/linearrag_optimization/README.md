# LinearRAG optimization prototypes

这是一个**机制级、离线可运行**的实验目录，不依赖作者数据集、spaCy 模型、LLM API 或 GPU。

目标：把几条优化假设先做成最小可执行版本，快速检查它们是否在数学/实现层面说得通。

## 目录

```text
linearrag_opt/
  bridge.py       semantic bridging + degree normalization + context seed
  retrieval.py    sparse passage prior + bipartite PPR
  synthetic.py    controllable hub-noise Tri-Graph generator
benchmarks/
  synthetic_noise_benchmark.py
  tier_consistency_regression.py
  multipath_backend_mismatch_demo.py
  seed_disambiguation_demo.py
  passage_scoring_benchmark.py
tests/
  test_bridge.py
  test_retrieval.py
  test_tier_consistency.py
run_experiments.py
RESULTS.md
```

## 运行

```bash
cd experiments/linearrag_optimization
python run_experiments.py
```

单独运行：

```bash
python benchmarks/tier_consistency_regression.py
python benchmarks/multipath_backend_mismatch_demo.py
python benchmarks/seed_disambiguation_demo.py
python benchmarks/passage_scoring_benchmark.py
python benchmarks/synthetic_noise_benchmark.py --trials 100 --top-k 5
pytest -q tests
```

## 实验边界

### Synthetic hub benchmark

它故意创建：

- 一个 3-hop gold entity chain；
- 多条 moderately-relevant seed→hub 句子；
- 一个连接大量噪声实体/段落的高频 hub。

测试 raw matrix propagation 是否会因为“路径数多”而给 hub 过高质量，以及 entity-degree normalization 是否能抑制。

它不是 HotpotQA/2Wiki/MuSiQue 的替代，也不模拟真实 embedding distribution。

### Tier regression

只验证一个 correctness 点：如果 seed level 应是 1，那么 first-hop entity level 必须是 2。否则任何 `score / level` 形式的 passage bonus 都会把第一跳放大 2 倍。

### Seed disambiguation demo

是一个两候选 toy case，用于说明为什么 full-query context 有可能纠正 surface-only top1 matching。它不证明真实 NER/embedding 上一定更好。

### Passage scoring microbenchmark

Python baseline 用 integer set membership，实际上比上游每 query 做 `str.count` 更友好；CSR matvec 因此主要用于证明“这个位置存在巨大向量化空间”，不能把 microbenchmark speedup 直接当端到端速度提升。
