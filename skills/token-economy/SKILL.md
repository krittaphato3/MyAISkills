---
name: token-economy
description: >-
  Cuts the token cost of agent work without cutting quality: cache economics, stable prefixes,
  model tiering, tool-result filtering, map-first code reading, progressive disclosure, bounded
  fan-out, and session budgets. Use when a task or session burns tokens out of proportion to its
  output, when configuring models or skills for cost, or before claiming any token saving. What
  belongs in context at each step routes to context-engineering; harness design to
  agent-harness-design; the roster itself to agent-config-maintenance.
metadata:
  version: 1.0.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: meta-architect
---

# Token Economy

Quality is the constraint; tokens are the variable to minimize. Every technique here is judged
by "did quality hold?" — a cheaper run that silently drops verification is a regression, not a
saving. And no saving may be claimed without a measurement: estimates are labeled as estimates.

## WHEN TO USE

- A session or task family spends tokens far out of proportion to its artifact.
- Choosing where a model tier, a cache boundary, or a fan-out belongs.
- A prompt, skill, or config change is proposed "for cost" and needs scrutiny.
- Designing a workflow that will run many times (the cost multiplies).

## WHEN NOT TO USE

- The problem is *what* should be in context — `context-engineering`.
- The harness (tools, subagents, evals) is the thing being designed — `agent-harness-design`.
- The task itself is quality-critical and the tier question is already settled — proceed.

## COST MODEL (the parts that matter)

```text
Input tokens         base price
Cache reads          ~0.1× input   (the stable prefix; pays off after 1 read within the window)
Cache writes         ~1.25× input (5-min TTL) / ~2× (1-hour TTL; pays off after 2 reads)
Output tokens        priced above input on most providers — long outputs are the expensive kind
Subagent fan-out     multiplies everything; multi-agent runs have been measured at ~15× a chat
Tool results         enter context and stay; a 50k-token tool dump is paid on every later turn
```

Two consequences drive most savings: **stable prefixes are cheap when cached**, and **anything
that enters context is rent, not a one-time fee**.

## DECISION TREE

```text
1. MEASURE FIRST
   Which phase dominates: orientation reads, fan-out, retries, or long outputs? Read the
   session ledger/log. Optimizing the wrong phase is the classic waste.

2. KILL WASTE BEFORE SPLITTING WORK
   Repeated reads of the same file · whole-file reads to find one symbol · verbose tool output
   pasted into the thread · re-deriving known facts · retrying a failing approach unchanged.

3. RIGHT-SIZE THE READER (map → focus → range)
   python tools/repo_map.py .                 # structure in ~1-2k tokens
   python tools/repo_map.py . --focus stripe  # symbol hits with line numbers
   Then read the 20-60 lines around the hit. Bulk reads belong to subagents; the main thread
   keeps conclusions, not transcripts.

4. CHOOSE THE TIER, WITH EVIDENCE
   Cheap/fast: bounded mechanical work, file discovery, summaries, mechanical checks.
   Strong: ambiguity, architecture, security judgment, adversarial review, adjudication.
   Downgrade only after the eval passes; report pass rate and cost together.

5. FREEZE THE PREFIX
   System doctrine, skills, and tool schemas stay byte-stable across turns; the task-specific
   suffix varies. A prefix that changes every turn gets zero cache benefit.

6. BOUND THE FAN-OUT
   Parallel agents cost multiples and only pay when the units are independent and valuable.
   ≤5 concurrent; one brief per unit; no duplicate dispatch. Sequential work stays sequential.

7. FILTER BEFORE FOR CONTEXT
   Tool/MCP results: request the slice you need, transform large payloads outside the model
   (code execution, filters, pagination). Keep tool catalogs small and load the rest on demand:
   one measured example dropped a 150k-token tool flow to 2k by executing tools outside context.

8. COMPACT DELIBERATELY
   Summaries keep goal, constraints, decisions, changed files, gates, open questions. Drop
   re-fetchable output (old tool results, superseded plans). Files survive compaction; chat
   does not — write handoffs to disk.
```

## BUDGET LADDER

| Situation | Move |
|---|---|
| Need to know where a symbol lives | `repo_map.py --focus`, then a ranged read (~100 tokens instead of 5k) |
| Need to understand a subsystem deeply | One `codebase-cartographer` subagent, summarized return |
| Same question asked twice in a session | Write the answer to a file (plan.md, decisions.md) |
| Routine formatting/mechanical pass | Cheapest model tier that passes the eval |
| Two independent modules | Parallel subagents (2), separate files, one wave |
| Five similar files to sweep | One subagent per file is waste — one subagent with the pattern |
| Long tool output needed once | Transform/summarize before it enters the thread |
| Approaching the context limit | Compact with the handoff template; re-anchor; don't re-read |

## FAILURE MODES & MITIGATIONS

1. **Optimizing the wrong phase.** *DETECT:* savings plan targets reads; the burn is fan-out.
   *FIX:* measure the phase split first.
2. **False precision.** *DETECT:* "saves 80%" with no measurement. *FIX:* measure before/after;
   label estimates with assumptions.
3. **Quality quietly traded.** *DETECT:* a cheaper path skips a gate the quality path ran.
   *FIX:* the eval decides the tier, not the invoice.
4. **Cache misses from drift.** *DETECT:* the prefix changed mid-session (edited doctrine, added
   tools). *FIX:* freeze the prefix; batch prefix changes at the boundary.
5. **Retry storms.** *DETECT:* repeated identical failing calls. *FIX:* stop after 2, change the
   approach, or escalate.
6. **MCP/tool bloat.** *DETECT:* tools listed but never called; results that are 90% unused.
   *FIX:* remove unused servers; filter outputs; load on demand.

## QUANTITATIVE RULES

- No savings claim without before/after numbers; otherwise "estimate" with assumptions named.
- Metadata ≤~100 tokens per skill; the always-on doctrine file stays under ~300 lines.
- ≤5 concurrent subagents; fan-out only for independent units (fan-out cost multiplies tokens).
- Tool/MCP results over ~2k tokens get transformed before entering context.
- Model downgrades require an eval pass on ≥5 representative tasks.
- When a session exceeds ~70% context, compact before continuing — not after quality drops.

## VERIFICATION GATE

- [ ] The phase split was measured, not assumed.
- [ ] Savings are backed by before/after evidence, or labeled estimates with assumptions.
- [ ] Every quality gate still ran after the optimization (tests, review, verification).
- [ ] The stable prefix is byte-identical across the measured turns (for cache claims).
- [ ] No requirement was traded away for tokens; if it was, the trade is stated explicitly.

## REFERENCES

- `context-engineering` — retrieval, briefs, compaction (the "what")
- `agent-harness-design` — tools, subagents, evals (the "how")
- `tools/repo_map.py` — map-first code reading
- `AGENTS.md` §9 — cost discipline (fan-out caps, model tiering, stop rules)
