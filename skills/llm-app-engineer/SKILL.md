---
name: llm-app-engineer
description: >-
  Builds LLM-backed product features: RAG and embeddings, prompt and context design,
  structured output, tool calling, streaming, guardrails, evals, and token or cost
  budgets. Use when an application calls a model and the result must be reliable. Model
  training routes to ml-python-scientist; orchestrating your own subagents to
  debate-protocol.
metadata:
  version: 3.0.0
  domain: delivery
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: llm-engineer
---

# LLM App Engineer

Building features on top of a model is not like calling an API — the callee is non-deterministic, metered, versioned in the open, and occasionally confidently wrong. This skill is the discipline that makes an AI feature shippable: retrieval that actually retrieves, output that is validated before it touches your data, and numbers that prove a prompt change helped.

## WHEN TO USE

- **New AI feature** — a chat surface, summarizer, classifier, extractor, or copilot in the product.
- **RAG / vector search** — chunking, embedding, indexing, retrieval quality, reranking.
- **Prompt work** — designing, versioning, or changing a system/task prompt.
- **Structured output / tool calling** — JSON contracts, function schemas, agentic loops.
- **Quality problems** — answers unsupported by context, format violations, regression after a prompt edit.
- **Cost or latency problems** — token bloat, retry storms, slow p95.

## WHEN NOT TO USE

- **Model training, fine-tuning, or dataset/model evaluation** — that is `ml-python-scientist`.
- **Choosing or wiring the provider service itself** (keys, quotas, SDK setup) — a service-selection and integration task first.
- **General backend API design around the feature** — `api-design-architect`.
- **Plain data engineering** — `data-pipeline-engineer`.

## DECISION TREE

1. **Does it need the model at all?** Rules, search, or a classifier may be cheaper, deterministic, and better. Reach for an LLM only where language understanding is genuinely required.
2. **Retrieval or not?** If the answer must be grounded in project data, it is RAG — build retrieval first, generation second.
3. **Which output contract?** Free text, constrained schema, or tool call. Prefer the strictest contract the UX can tolerate.
4. **How is it graded?** Define the eval set and pass criterion **before** writing the prompt (`test-driven-development` for prompts).
5. **What is the budget?** Tokens, currency, and p95 latency per request — write the ceiling before building.
6. **What fails?** Timeout, rate limit, invalid output, provider outage — each gets an explicit behavior.
7. **Verify per `verification-before-completion`** — eval delta and cost numbers attached, not impressions.

## PATTERNS

### 1. Retrieval
- Chunk on structure (headings, functions), ~200–800 tokens with overlap; store source metadata for citations.
- Measure retrieval separately: recall@k / nDCG before answer accuracy. Fix the retriever before the prompt.
- Hybrid search (keyword + vector) wins on names, IDs, code symbols, and rare terms.
- Rerank top candidates; keep the context window small and high-signal.

### 2. Prompting & versioning
- System prompt = role, constraints, output contract; task prompt = data. One job per prompt.
- Pin prompts as versioned artifacts with an id/hash; a prompt change is a code change that gets reviewed.
- Temperatures: near 0 for extraction/classification; higher only for creative surfaces.

### 3. Output validation
- Use the provider's schema/tool mechanism, then validate locally. On failure, repair-retry with the validation error (max 2), then fail loudly.
- Treat model output as untrusted input: no direct SQL, no direct shell, no direct filesystem path.

### 4. Evals
- Fixed, versioned dataset; graders: exact match, rubric, or LLM-judge with a rubric.
- Report pass rate before/after every prompt, model, or retrieval change. Never ship an unmeasured prompt.

### 5. Guardrails
- Delimit untrusted content and instruct the model to treat it as data, not instructions.
- Redact secrets/PII before prompting; never log raw prompts without a retention policy.
- Per-user rate and spend caps so a loop bug cannot drain the account.

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX.

1. **Hallucinated API** — DETECT: a model id or parameter not in current docs. FIX: verify against live docs (`source-driven-development`).
2. **Unguarded parse** — DETECT: model text parsed into business logic or DB. FIX: schema-validate + repair-retry.
3. **Prompt-tuned retrieval bug** — DETECT: repeated prompt edits with unchanged retrieval metrics. FIX: measure recall@k first.
4. **No eval** — DETECT: "feels better". FIX: run the set; attach the deltas.
5. **Context inflation** — DETECT: unbounded history/documents in the prompt. FIX: top-k + rerank + summarize; log token counts.
6. **Cost/latency blowout** — DETECT: unmeasured tokens or uncapped retries/tool loops. FIX: per-request budget + caps + usage logging.
7. **Prompt injection** — DETECT: retrieved content alters tool scope or instructions. FIX: delimit, treat as data, isolate tool permissions.
8. **Provider drift** — DETECT: quality shifts after an upstream update. FIX: pin versions where possible; re-run evals on change.

## QUANTITATIVE RULES

- Eval set ≥ 20 cases (golden + held-out) for a focused feature; pass rate recorded before/after.
- Retrieval recall@k reported independently of answer quality.
- Token and currency cost per request, plus p50/p95 latency, reported for every new path.
- Retry budget ≤ 2 on invalid output; tool-call loop cap set explicitly; per-user spend cap set explicitly.
- Prompt artifacts carry a version id; changed prompts without a recorded eval are not done.

## VERIFICATION GATE

- **Eval delta attached?** Pass rate before/after on a fixed set, with the artifact path.
- **Output validated?** Schema check present on every structured response.
- **Retrieval measured?** recall@k reported when RAG is involved.
- **Budget met?** Tokens, cost, and p95 stated and within the declared ceiling.
- **Failure paths handled?** timeout, rate limit, invalid output, provider down each have a defined behavior.
- **Injection considered?** Untrusted content delimited and treated as data.

```text
[LLM FEATURE]
Feature: {name} · Model: {id, pinned} · Prompt version: {id}
Evals: {n} cases · {before}% → {after}% · graders {..} · artifact {path}
Retrieval: recall@{k} {x}% (if RAG)
Budget: {tokens}/req · {cost}/req · p50 {x}ms · p95 {y}ms
Validation: {schema + repair policy}
Failure paths: timeout {..} · rate-limit {..} · invalid {..} · outage {..}
```

## REFERENCES

- `ml-python-scientist` — training/fine-tuning, carved out above.
- `api-design-architect` — the surrounding API contract.
- `background-jobs-engineer` — async ingestion/indexing work.
- `verification-before-completion`, `test-driven-development` — the eval-as-test discipline.
- `source-driven-development` — mandatory for provider SDK and model accuracy.

Ownership: maintained by llm-engineer; llm-app-engineer is the delivery-domain skill for model-backed features.
