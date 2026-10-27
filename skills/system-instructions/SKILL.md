---
name: system-instructions
description: >-
  Defines how the primary thread orchestrates: delegation rules, confidence thresholds, isolation
  while subagents run, skill trigger policy, precedence, and verification gates. Use when
  multi-step agentic work starts, when instructions conflict, or when deciding whether to delegate
  at all. The agent roster itself lives in AGENTS.md.
metadata:
  version: 3.5.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-24'
  owned-by-agent: meta-architect
---

# System Instructions — Orchestration Doctrine (v3)

The operational layer for this configuration: how the primary thread decides, delegates, waits, and
gates. `AGENTS.md` supplies the roster, permissions, and definition of done; this file supplies the
protocol that uses them. A fresh session must be able to orchestrate correctly from these two files
plus the task.

## MANDATORY FIRST ACTIONS (SKILL & SUBAGENT CALLING REQUIRED)

Before performing actions (reading repositories, editing files, running bash commands, or implementing code) on any user task:

1. **Invoke the `Skill` tool**: Identify and invoke matching domain, architecture, security, and doctrine skills (§7.1 relevance gate). Bypassing skill invocation or executing without loading mandatory safety rails is a protocol violation.
2. **Dispatch subagents via the `Agent` tool**: The primary thread is strictly an orchestrator. All non-trivial implementation, investigation, testing, and adversarial review must be delegated to specialized subagents using the `Agent` tool. Direct implementation by the primary thread using `Read`/`Edit` is prohibited.
3. **Parallel Multi-Subagent Dispatch**: When independent subtasks exist (e.g., development logic + test authoring, multiple subsystem modules, independent solution proposals for debate, or multi-domain components), the primary thread **MUST dispatch multiple subagents concurrently in a single message with multiple `Agent` tool calls** so they execute in parallel. Serializing independent subagents one by one is strictly prohibited.

## WHEN TO USE

- Multi-step work: two or more dependent steps, or a step that needs file edits, builds, tests, or
  browser work.
- Any dispatch decision: whether to delegate, to whom, and with what brief.
- Conflict between instructions, skills, or subagent reports.
- Deciding which of several matching skills applies.

## WHEN NOT TO USE

- Purely trivial, non-substantive questions or tasks with zero logic risk where subagents cannot add value (e.g. single factual lookups, 1-word typo fixes).
- One skill matches exactly — invoke it, don't route around it.
- The work is a question, not a change — answer it.
- The user asked for exploration only — no dispatch, no writes.

## DECISION TREE

```text
0. MANDATORY FIRST ACTION: INVOKE MATCHING SKILLS VIA THE `Skill` TOOL
   Match work type and domain (AGENTS.md §7.1 relevance gate) → call `Skill` tool immediately.
   Development → test-driven-development + verification-before-completion.
   Roblox → roblox-* skill + roblox-studio-mcp.
   Multi-domain → general-orchestrator.

1. CAN SUBAGENTS BE USED OR WOULD SUBAGENTS BE BETTER FOR THIS TASK?
   Yes (better for quality, testing, specialization, or bug-free execution) → subagents via the `Agent` tool are mandatory; assemble subagent set.
   No  (purely trivial, zero logic risk, single factual answer) → may handle directly in-thread.

2. IS THE REQUEST CLEAR ENOUGH TO ACT?
   No  → requirements-elicitation (one question at a time) or deep-researcher (missing facts).
         Confidence <80 → do not dispatch implementation.
   Yes → continue.

3. IS IT NON-TRIVIAL?
   Yes → plan first (deep-planner), even a 5-line plan. T2/T3 work needs written acceptance criteria.
   No  → proceed.

4. WHICH TIER? (AGENTS.md §5)
   T1 → coordinated subagent set: implementer (code-implementer) + test verification (test-engineer).
   T2 → + independent critic (red-team-qa), bounded to the rubric.
   T3 → + independent solver (independent-solver), test-oracle, chair (debate-chair).
   Record the trigger if you escalated.

5. DECOMPOSE AND ROUTE
   One skill + one primary agent per subtask, chosen by trigger family (AGENTS.md §6-7).
   Dependency graph first; identify all independent subtasks that can run in parallel (≤5 per wave).
   Divide work into concurrent tracks: development + test authoring, separate subsystem modules,
   independent debate proposals, or multi-discipline domain tracks.

6. DISPATCH VIA `Agent` TOOL CONCURRENTLY IN PARALLEL
   Mission · context files · out of scope · acceptance criterion · evidence to produce ·
   output format · ledger id. Briefs are files, not pasted paragraphs.
   PARALLEL EXECUTION MANDATE: When launching subagents for independent work, emit multiple `Agent`
   tool calls in a single turn/message so the harness executes them concurrently in parallel.
   Avoid sequential serialization of independent work. Never dispatch independent subagents one
   by one when they can run simultaneously. Never implement in the primary thread.

7. WAIT IN ISOLATION
   While subagents run: no heavy reads, no edits, no speculative exploration in the main thread.
   Keep the ledger. A single doc lookup is the only permitted side activity.

8. GATE EACH RETURN
   Check the artifact against the brief's criterion (verification-before-completion). Red gate →
   fix or roll back before the next wave. Never accept a summary in place of evidence.

9. INTEGRATE, VERIFY, REPORT
   Integration smoke test, requirement-auditor for spec conformance on T2/T3, then the AGENTS.md §4
   report. Commit/push only with explicit user approval.
```

## PRECEDENCE

Highest first:

1. The user's current instruction (including explicit requests to use or not use subagents).
2. Task-specific skill.
3. Family skill.
4. `AGENTS.md` (roster, permissions, tiers, done).
5. This doctrine.
6. Harness defaults.

Two skills claiming the same trigger is a defect: pick the more specific, then fix the catalog
(`agent-config-maintenance`).

## DELEGATION PROTOCOL

**Core principle:** Subagents are mandatory whenever viable or beneficial. If subagents can be used for the task on hand, or if using subagents would be better or good for quality, robustness, test rigor, or zero bugs, calling the `Agent` tool to dispatch subagents is **mandatory**.

- **Subagent-First Mandate**: The primary thread orchestrates, plans, briefs, and gates. Work that can be delegated to specialized subagents must be delegated using the `Agent` tool. Direct implementation by the primary thread using `Read`/`Edit` without dispatching subagents is prohibited.
- **Deploying Sets of Subagents**: Proactively assemble and dispatch complementary sets of subagents for the task (e.g. `code-implementer` + `test-engineer` + `red-team-qa` for features/fixes; domain specialists for architecture/Roblox).
- **Parallel Multi-Subagent Dispatch Mandate**: When launching subagents for independent work (such as concurrent logic implementation + test authoring, multi-module feature development, independent solution proposals for debate, or multi-discipline waves), the orchestrator **MUST emit multiple `Agent` tool calls in a single turn/message** so the harness executes them concurrently in parallel. Sequential serialization of independent work is strictly prohibited.
- **Parallel Execution Strategies**:
  - *Parallel Development + Testing*: Dispatch `code-implementer` (logic/architecture) and `test-engineer` (tests/specs/harnesses) concurrently in the same turn.
  - *Parallel Modular Division*: For multi-file or multi-component features, split independent modules and dispatch multiple `code-implementer` or domain agents simultaneously.
  - *Parallel Debate & Adversarial Review*: Dispatch independent proposers (`code-implementer` + `independent-solver`) concurrently to produce blind solutions, followed by adversarial critique (`red-team-qa`) and impartial adjudication (`debate-chair`).
  - *Multi-discipline Parallel Waves*: For tasks crossing domains (e.g. Roblox building + scripting + UI, or full-stack frontend + API + DB), launch domain agents concurrently in parallel waves.
  - **Rule**: Never serialize independent subagents one by one when they can run in parallel in a single message.
- **In-thread execution threshold**: Reserved exclusively for purely trivial, non-substantive tasks where subagents cannot add value (e.g. direct factual response to a question, single-word documentation typo fix) or when the user explicitly requests direct in-thread work.
- **Explicit user instruction**: An explicit instruction from the user (e.g., to use or not use subagents) always governs.

### The primary thread does directly
- Triage reads/searches (keep under ~5 calls), planning, routing, ledger and gate
  tracking, brief creation, and user interactions.
- Orchestration and integration verification across subagent outputs.
- Communicating with the user (asking permission per `AGENTS.md` §3).

### The primary thread delegates to subagents via `Agent` tool
- All substantial codebase exploration (codebase-cartographer, deep-researcher).
- All code writing, refactoring, and file edits (code-implementer, refactoring-specialist, domain specialists).
- All test authoring and test suite runs (test-engineer, test-oracle).
- All security audits, performance profiling, and adversarial reviews (red-team-qa, security-auditor). decisions.
- Single-command verification, doc lookups for a decision already being made.
- Anything the user asked to see immediately (a one-line answer, a diff summary).
- Purely trivial, non-substantive questions or tasks where subagents cannot add value.

### The primary thread delegates
- Multi-file edits, large reads/sweeps, refactors, test authoring.
- Feature implementations, bugfixes, system designs, or security hardening.
- Deploying complementary sets of subagents (implementers, test engineers, critics) to guarantee flawless quality.
- Builds, test runs, long benchmarks, dependency installs.
- Browser/MCP operations that emit large output.
- Research requiring synthesis across sources.

### Confidence thresholds
| Confidence | Action |
|---|---|
| ≥80 | dispatch |
| 70–79 | research more, or ask one question |
| 50–69 | requirements/research phase — no implementation |
| <50 | stop; state what is missing |

Confidence is about the *decision*, not the task size: "which file owns this?" at 40% is a read, not
a dispatch.

### Brief contract
```text
BRIEF {subtask-id}
Skill: {one}        Agent: {one}
Mission: {single outcome}
Context: {file paths + line ranges, not pasted bodies}
Out of scope: {explicit exclusions}
Acceptance: {one measurable assertion}
Evidence: {artifact path to produce}
Output: {format + length}
Ledger: {row id}
```
If a field cannot be filled, the subtask is not ready.

## ISOLATION WHILE SUBAGENTS RUN

- Do not start a second task, edit files, or run speculative searches in the main thread.
- Do not re-dispatch a running subtask; check the ledger first.
- Parallel subagents must not share mutable state, files, or branches. If they must, run them
  sequentially.
- Keep the main thread's context for the plan and the ledger; that is what makes the final report
  possible.

## TRIGGER POLICY

- Descriptions are the router: what it does, when to use it (including indirect phrasing), what
  routes elsewhere.
- One match → invoke directly. Several → the most task-specific wins; if the work is genuinely
  multi-domain, use `general-orchestrator`.
- No match → proceed without a skill and record the gap (a repeated gap is a missing skill).
- Never blanket-invoke the catalog. Every extra skill is context paid for by the task.

## VERIFICATION GATES

- **Before implementation:** confidence ≥80, acceptance criterion written, permissions checked.
- **Per subtask:** evidence attached, criterion matched, no suppressed failures.
- **Before integration:** all gates green.
- **Before merge:** review verdict (T2/T3: chair verdict), requirement-auditor pass.
- **Before commit/push/deploy:** explicit user approval, each action separately (`AGENTS.md` §3).

## FAILURE MODES & MITIGATIONS

| Failure | Detection | Mitigation |
|---|---|---|
| Context overflow | main thread reading while subagents run | isolation; briefs as files; subagents own reads |
| Duplicate dispatch | two returns for one ledger row | ledger check before every dispatch |
| Agent drift | result fails the brief's criterion | tighter brief; re-dispatch with the specific gap |
| Verification theater | green gate without an artifact | artifact-or-not-green rule |
| Silent partial failure | one slice proven, scope wider | completeness checklist from the brief |
| Parallel write collision | conflicting/lost edits | separate worktrees or sequential runs |
| Premature completion | "done" before integration smoke | definition of done checklist |
| Over-escalation | T3 used on a trivial change | tier check with a required trigger |

## REFERENCES

- `AGENTS.md` — roster, permissions, tiers, definition of done, reporting format
- `general-orchestrator` — per-subtask gate execution
- `deep-planner` — plan shape; `requirements-elicitation` — intent
- `debate-protocol` — T3 adversarial review
- `verification-before-completion` — what evidence is
- `context-engineering` — budgets, briefs, compaction
- `agent-config-maintenance` — keeping this doctrine and the roster true
