---
name: search-relevance
description: >-
  Builds and tunes non-LLM search quality: analyzers and tokenization, BM25 and hybrid retrieval,
  synonyms and typo tolerance, field boosts, faceting, reranking, and relevance evaluation with a
  labeled query set and nDCG or MRR. Use when search returns irrelevant results, an exact-match
  catalog is migrating to search, or relevance changes need proof they helped. RAG over your own
  documents routes to llm-app-engineer.
metadata:
  version: 1.0.0
  domain: architecture
  grade: G2
  status: active
  last-reviewed: '2026-11-08'
  authored-by: solution-architect
---

# Search Relevance

Relevance is a measurement problem before it is a tuning problem. Every change is a hypothesis
against a fixed query set; a change that "feels better" on three queries is not a result.

## WHEN TO USE

- Users search and get nothing, or get the wrong thing, and the query is not a phrasing problem.
- Building search over products, documents, tickets, or code with Elasticsearch, OpenSearch,
  Postgres full-text, Meilisearch, Typesense, or SQLite FTS.
- A catalog or listing page needs faceting, ranking, or typo tolerance.
- Adding hybrid retrieval (lexical + vector) and deciding how to fuse and rerank.
- Relevance changed and someone wants to know whether it improved.

## WHEN NOT TO USE

- Retrieval over documents to feed a model's context. That is RAG: `llm-app-engineer`.
- The index is stale or ingestion is broken. That is a `data-pipeline-engineer` problem.
- The query is slow, not wrong. `query-performance-engineer`.
- The user cannot express the query (autocomplete, intent classification). That is product design.

## DECISION TREE

```text
What is failing?
├─ exact queries return nothing ................... analyzer mismatch: casing, stemming, punctuation
│  └─ SKU/model codes ............................ exact-match subfield + keyword analyzer, boosted
├─ results exist but rank badly ................... field boosts, phrase proximity, recency, popularity
├─ typos kill recall .............................. fuzzy matching at edit distance 1 (2 for long terms)
├─ vocabulary mismatch (sofa / couch) ............. synonym graph at index time or query time
├─ one facet dominates results .................... post-filter vs filter context; count before filter
├─ long natural-language queries .................. tokenize + stopwords, then a reranker
├─ semantic intent (paraphrase) ................... hybrid: BM25 candidate set + vector, then fuse
└─ no way to tell if a change helped .............. build the labeled query set first
```

### Evaluation before tuning

| Artifact | Minimum | Purpose |
|---|---|---|
| Query set | 50-200 real queries, stratified by head/mid/tail | The only ground truth you have |
| Judgments | binary relevant/not, 2+ assessors on a sample | nDCG@10, MRR |
| Failure buckets | zero-result, off-topic, wrong-order, slow | Directs where to look |
| Baseline | metrics for the current system, frozen | Any change must beat it |

Head/mid/tail matters: head queries are 5% of volume and 60% of sessions, tail queries are where
recall dies. A set of only head queries will pass while tail users get nothing.

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| Vibes tuning | Three queries eyeballed, "looks better" | Labeled set, metric delta, and it must clear noise |
| Overfitting the set | Every query becomes a synonym entry | Hold out 20%; re-check against new queries |
| Analyzer drift | Index and query analyzers differ, so nothing matches | Same analyzer definition for both, asserted in a test |
| Fuzzy everywhere | Edit distance 2 on short terms returns noise | Apply by term length; never on IDs |
| Facet counts wrong | Counted after filtering | Count in filter context, display post-filter |
| Vector-only for SKUs | Embeddings lose exact model numbers | Hybrid, with exact-match boosted above all |
| Silent zero results | No logging, so the worst case is invisible | Log zero-result queries; review weekly |
| Recall never measured | Only top-10 precision | Track recall@100; retrieval failures hide there |

## QUANTITATIVE RULES

- **50 labeled queries minimum** before any tuning change, 200 before a ranking rewrite.
- **nDCG@10 for ranking, recall@100 for retrieval, MRR for single-answer lookups.** Pick one primary metric.
- **A change ships only if it beats baseline by more than the noise** measured by re-running the
  judgment set with a different assessor sample.
- **Fuzzy distance by length**: 1 for terms under 6 characters, 2 above; never on numeric IDs.
- **Zero-result rate under 5%** on the labeled set, or recall work comes first.
- **p95 query latency budget** stated up front; relevance that costs 800 ms is a product decision.

## VERIFICATION GATE

- [ ] Labeled query set exists, is stratified, and has a held-out portion.
- [ ] Baseline metrics recorded before any change.
- [ ] Analyzer equivalence between index and query asserted by a test.
- [ ] Metric delta attached for the change, with the query-level diff shown.
- [ ] Zero-result and off-topic queries logged and reviewed.
- [ ] Latency p95 measured under production-shaped index size.

## REFERENCES

- `query-performance-engineer` for latency and index structure.
- `llm-app-engineer` for embedding-based retrieval and RAG, and where it differs from this.
- `data-pipeline-engineer` for ingestion, reindexing, and schema evolution.
- `algorithms-and-data-structures` for candidate generation and ranking cost.
- `product-engineering` for the relevance/latency trade-off as a product decision.
