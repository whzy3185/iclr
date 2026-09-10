# Prototype experiment results

运行环境：当前 ChatGPT sandbox CPU Python 环境。所有实验均为 synthetic / microbenchmark；没有真实 RAG benchmark 或 LLM generation。

## 1. Tests

```text
5 passed in 0.13s
```

覆盖：

- 3-hop chain propagation；
- context-conditioned seed correction；
- entity IDF behavior；
- bipartite PPR mass normalization；
- first-hop tier 2× inflation regression。

---

## 2. Tier consistency regression

构造：

- 一个第一跳 bridge entity，activation score = 0.70；
- 一个更深层 gold target，score = 0.80；
- passage prior 使用 `score * log(1+count) / tier` + dense term。

结果：

```text
old_first_hop_tier      = 1
correct_first_hop_tier  = 2
first_hop_bonus inflation = 2.0x

old distractor score   = 0.5052
fixed distractor score = 0.2626
gold score             = 0.3448

old ranking   : distractor > gold
fixed ranking : gold >= distractor
```

解释：hop/tier off-by-one 足以改变 passage 排名，因此必须作为 correctness bug 处理，而不是“超参差异”。

---

## 3. BFS / vectorized multi-path state mismatch demo

构造两个 active source entity，共享同一个 sentence 并共同到达一个 next entity：

```text
source scores        = [0.90, 0.80]
sentence similarity = 0.70
path scores          = [0.63, 0.56]
```

如果一个 BFS-like 路径对 graph-node weight 做累加、但 activated-entity dict 只保留最后一次写入，则：

```text
entity weight accumulator = 1.19
activated state (forward order) = 0.56
activated state (reverse order) = 0.63
```

而矩阵聚合天然得到：

```text
vectorized activated state = (0.90+0.80)*0.70 = 1.19
```

因此这个 toy case 同时揭示两件事：

- activated state 对遍历顺序敏感；
- vectorized passage scoring 读到的 entity score 可比 BFS forward-order state 大 2.125×。

这与上游代码静态审计的风险一致，说明应该先冻结多路径 reducer（max/sum）再比较 backend。

---

## 4. Context seed disambiguation demo

输入两个同名/近似候选：

```text
candidate 0: surface=0.96, context=0.18   (wrong sense)
candidate 1: surface=0.92, context=0.91   (right sense)
```

surface-only：

```text
choice = candidate 0
```

`0.55*surface + 0.45*context`：

```text
choice = candidate 1
score  = 0.9155
```

这里只说明机制可行；真实数据需要测 ambiguity subset、seed correctness 和 latency。

---

## 5. Hub-noise synthetic benchmark

100 trials，top-k passage=5。

### Paper-like raw propagation

```text
passage Recall@5       = 1.000 ± 0.000
passage Precision@5    = 0.600 ± 0.000
gold entity recall     = 1.000 ± 0.000
active entities        = 289.15 ± 9.18
hub score              = 118424.67 ± 3106.01
runtime                 ≈ 2.96 ms
```

### Entity-degree normalized

```text
passage Recall@5       = 1.000 ± 0.000
passage Precision@5    = 0.600 ± 0.000
gold entity recall     = 1.000 ± 0.000
active entities        = 4.00 ± 0.00
hub score              = 0.0
runtime                 ≈ 3.15 ms
```

加入 frontier budget=32 和 passage-IDF 在这个 toy case 上没有继续改变 top-5 指标，因为 degree normalization 已经完全抑制了构造的 hub。

### 结论边界

这是一个有意放大的 hub stress test。它支持：

> raw incidence-sum propagation 可以在高 degree 结构下产生巨大无关 activation；degree normalization 可以在这个构造中把 frontier 压回 gold chain，同时不损 gold passage recall。

它**不支持**：

> degree normalization 会提高真实 HotpotQA/2Wiki/MuSiQue accuracy。

真实验证需要检查不同 degree 分位的 entity 是否真的与错误 retrieval 相关。

---

## 6. Passage bonus sparse-matvec microbenchmark

合成规模：

```text
20,000 passages
10,000 entities
6 entities / passage
64 activated entities
```

Python baseline：对每个 passage 遍历 64 active entities 并做 set membership。注意：真实上游代码做的是字符串 `.count()`，通常更重。

结果（取多次运行最小值）：

```text
python nested   ≈ 0.1528 s
CSR sparse mv   ≈ 0.000080 s
speedup         ≈ 1902x
max abs diff    = 0.0
```

应如何解释：

- 这个热点可以 exact vectorize；
- speedup 量级只针对该 microkernel；
- end-to-end retrieval 还包含 query/sentence embedding similarity、entity activation、PPR，因此总体加速远小于 1900×；
- 但它是低风险、非常值得先落地的优化。

---

## 7. 下一次应该跑什么

代码层下一步：

1. 加一个 exact reference simulator，复现上游 BFS 的 sentence-dedup + per-entity top-k 语义；
2. 做 BFS vs vectorized differential tests，覆盖 shared sentence、多路径和 duplicate seed；
3. 从真实作者代码导出一个小 graph fixture，验证 passage prior sparse rewrite exact match；
4. 真实数据上先跑 retrieval-only degree normalization，不先跑 LLM generation。
