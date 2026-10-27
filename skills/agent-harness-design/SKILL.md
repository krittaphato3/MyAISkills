---
name: agent-harness-design
description: >-
  Designs the agent itself: prompt and skill contracts, tool schemas, subagent boundaries,
  context budgets, model tiering, and the eval harness that proves a change helps. Use when
  building or tuning an agentic workflow (prompts, tools, loops, subagents, memory), when an
  agent underuses a tool or drifts mid-task, or before shipping a prompt or model change on
  vibes. Product features that call a model route to llm-app-engineer; training and fine-tuning
  models to ml-engineer; this repo's roster and routing table to agent-config-maintenance.
metadata:
  version: 1.0.0
  domain: delivery
  grade: G3
  status: active
  last-reviewed: '2026-10-27'
  owned-by-agent: llm-engineer
---

# Agent Harness Design

An agent is a harness: the prompt, the tools, the context window, the subagents, and the loop
that decides what happens next. Harness failures look like intelligence failures — the model
"ignored" a tool it never learned to call, or "forgot" a fact that was compacted an hour ago.
This skill builds harnesses that work on the fifth task as well as the first.

## WHEN TO USE

- Designing or tuning an agentic workflow: prompts, skills, tool schemas, loops, subagents.
- An agent undertriggers a tool, loops, drifts, or produces uneven quality across similar tasks.
- Deciding whether to add a tool, a skill, a subagent, or another prompt paragraph.
- A prompt, model, or tool change needs evidence before it ships.

## WHEN NOT TO USE

- The product feature merely calls a model once — `llm-app-engineer`.
- Maintaining this configuration's roster, routing, and lint — `agent-config-maintenance`.
- Cutting token cost of a system that already works — `token-economy`.
- Training, fine-tuning, or evaluating a model's weights — `ml-engineer`.

## DECISION TREE

```text
1. WRITE THE OUTCOME CHECK FIRST
   What observable result proves the agent worked? Prefer an executable check (tests, build,
   file exists, API response). If the output is subjective, define a rubric with named criteria.
   No check → you cannot tell whether the prompt change helped.

2. BUDGET THE CONTEXT
   Always-on metadata: ~100 tokens per skill (name + description only).
   Activated instructions: keep under ~5k tokens; push detail to files loaded on demand.
   Bulk artifacts (logs, code, data): never inline; pass paths and read ranges.
   Design for the window you actually have, not the one in the demo.

3. DESIGN TOOLS LIKE AN API FOR A JUNIOR
   Narrow scope, typed arguments, deterministic errors, idempotent where possible.
   One obvious tool beats three overlapping wrappers (the model picks wrong among similar tools).
   Expensive output: transform before it reaches the model (filter, paginate, summarize).
   Tool descriptions are prompt real estate — every enabled tool costs context even unused.

4. SPLIT BY CONTEXT, NOT BY ORG CHART
   One subagent = one brief = one deliverable. Give it pointers, not transcripts.
   Independent units → parallel; shared files/state → serialize or partition first.
   Reviewers must not see the author's reasoning (they inherit its blind spots).

5. WRITE PROMPTS THAT EXPLAIN THE WHY
   State the goal and the reasoning; rigid MUST-stacking gets followed literally and breaks on
   the first unanticipated case. Describe trigger conditions for tools ("when the user asks about
   billing..."). Keep the stable prefix stable — it is the cacheable part.

6. PICK THE MODEL BY TASK, MEASURED
   Strong models for ambiguity, architecture, and adjudication; cheap models for bounded,
   mechanical, read-heavy work. Downgrade only after the eval passes on a representative set.
   Never set a model tier you cannot justify from a measurement.

7. BUILD THE EVAL SET AND KEEP IT RUNNING
   5+ representative tasks; grade with code where possible, rubric + human spot-check otherwise.
   Track pass rate, tokens, tool calls, latency per change. Keep failing cases as regressions.
   The suite must discriminate: if a change never moves the score, the suite is theater.
```

## PATTERNS

### 1. Skill/agent file contracts
```text
Frontmatter description = router (what it does, when to use it, nearest neighbor boundary).
Body = procedure: WHEN TO USE / WHEN NOT TO USE / decision tree / failure modes / gate.
Anything large = references/ loaded on demand. Scripts stay deterministic and rerunnable.
```

### 2. Subagent brief
```text
Mission (one outcome) · Context (paths + ranges) · Out of scope (explicit)
Acceptance (one measurable assertion) · Evidence to produce · Output format
```

### 3. Eval record per change
```text
Change: prompt/skill/tool/model delta (one variable at a time)
Tasks: 5+ representative, stable across runs
Result: pass rate ±, tokens ±, latency ±, regressions named
Verdict: ship / revise / revert — with the number that decided it
```

### 4. Failure injection before launch
Feed the agent: an ambiguous request, a tool error, a stale file, a huge input, a request with
a forbidden action. What it does under those four says more than ten happy paths.

## FAILURE MODES & MITIGATIONS

1. **Eval theater** — a green suite that passes before and after any change. *DETECT:* assertion
   pass rates identical across known-different versions. *FIX:* add discriminating cases; grade
   by outcome, not by trajectory.
2. **Context leak** — subagent sees the parent's whole conversation and wanders. *DETECT:* output
   touches files outside the brief. *FIX:* tighter brief; restate out-of-scope.
3. **Tool bloat** — 30 tools, most unused, all in context. *DETECT:* tool-call histograms skew to
   two tools. *FIX:* load tools on demand; delete wrappers; keep one obvious path per intent.
4. **Prompt stacking** — MUSTs accumulate after every incident until instructions conflict.
   *DETECT:* two rules that cannot both be followed. *FIX:* consolidate into principles with
   reasons; delete the redundant text; encode hard constraints as code/checks instead.
5. **Silent model downgrade** — cost falls, quality falls, nobody looked. *DETECT:* no before/after
   on a representative set. *FIX:* eval before and after; report both numbers.
6. **Fan-out for sequential work** — parallel agents edit shared state or duplicate effort.
   *DETECT:* merge conflicts between sibling agents; identical work twice. *FIX:* partition by
   ownership; serialize shared state.

## QUANTITATIVE RULES

- Per skill: metadata ≤~100 tokens; activated body <5k tokens; >500 lines → references/.
- Eval set: ≥5 representative tasks; one variable per change; keep regressions forever.
- Parallel fan-out: ≤5 concurrent, independent units only; shared state serializes.
- Prompt/model change ships only with before/after numbers (pass rate and cost).
- Tool result entering context: transform if >~2k tokens.

## VERIFICATION GATE

- [ ] The outcome check exists and was run against the changed harness.
- [ ] Before/after evidence attached for each prompt/tool/model change.
- [ ] The stable prompt prefix is unchanged (cache-friendly) unless the change is the prefix.
- [ ] Eval set discriminates: at least one task's result changed with the change.
- [ ] No secrets, PII, or credentials in prompts, logs, or tool results.
- [ ] Failure-injection cases exercised (ambiguous request, tool error, forbidden action).

## REFERENCES

- `llm-app-engineer` — model calls inside product features (retries, fallbacks, cost)
- `token-economy` — the cost side of these decisions
- `context-engineering` — what belongs in context at each step
- `agent-config-maintenance` — this repo's roster and routing
- `mcp-builder` — exposing external services as tools
