---
name: general-orchestrator
description: >-
  Executes multi-skill work behind per-subtask gates: build a skill inventory, route each
  subtask to one skill and one agent, sequence by dependency graph, verify every subtask
  with evidence, then integrate behind a smoke test. Use when a task spans two or more
  domains or needs parallel waves. Single-skill work invokes that skill directly.
metadata:
  version: 3.5.0
  domain: doctrine
  grade: G3
  status: active
  last-reviewed: '2026-10-24'
  authored-by: code-implementer
---

# General Orchestrator

The gate-driven execution orchestrator for any multi-skill backend or distributed task. It turns the system-instructions protocol — decompose, dispatch, verify, integrate — into per-subtask proof-based gates: every subtask ends in a checkable gate, a failed gate stops the pipeline for a root-cause fix and re-verification, and nothing is done without attached evidence. When system-instructions trigger policy says several skills match the same work, this skill is the routing and gating layer over them: it reads the skill inventory per subtask, routes each one to the right agent, gates every result, and recombines behind an integration smoke test.

## MANDATORY FIRST ACTIONS

In accordance with `AGENTS.md` §0 and `system-instructions`:
- Calling the `Skill` tool is strictly mandatory before acting.
- Calling the `Agent` tool to dispatch subagents is strictly mandatory for all implementation, exploration, testing, and reviews. The primary orchestrator must never implement directly using `Read`/`Edit`.
- **Parallel Multi-Subagent Dispatch**: When independent subtasks exist in a wave, the primary orchestrator **MUST dispatch all independent subagents concurrently in a single turn with multiple `Agent` tool calls**. Serializing independent subagents one by one is strictly prohibited.

## WHEN TO USE

Use this skill when the task is multi-skill, parallelizable, or distributed:

- **Two or more skills or domains in one task** — for example, a backend service that needs database work (query-performance-engineer), API contract design (api-design-architect), and deployment (devops-pipeline-engineer) in a single delivery. When system-instructions trigger policy reports several matching skills, the trigger here is the combination, not any one skill.
- **Parallelizable backend work** — independent subtasks that can run concurrently on separate agents and must be recombined afterward, where a single agent would serialize or blow the context.
- **A dependency graph** — subtasks where some must finish before others start, requiring sequencing plus per-subtask gating. Gate-driven sequencing is the point, not raw speed.
- **Multi-agent work per AGENTS.md** — the task exceeds one agent brief: at least two distinct agents dispatch, verify, and integrate, and the golden rule (main thread orchestrates, all file work and coding through subagents) applies.
- **Gate value exists** — there is a checkable pass criterion per subtask and an integration point to smoke-test. If you cannot state a pass criterion, you are not ready to dispatch.

Relationship to the doctrine it implements: system-instructions supplies the operational skeleton — delegation protocol, precedence, waiting, confidence thresholds, verification gates — while this skill supplies the execution layer that turns those rules into a per-subtask gate sequence with a ledger and a report. A run that follows this skill is compliant with system-instructions by construction; a run using this skill but skipping gates is violating both.

## WHEN NOT TO USE

- **Single-skill tasks** — invoke the specific skill directly; routing through an orchestrator adds tokens and gates with no payoff. This is the hard line the decision tree enforces first. (A single-skill task still deploys subagents whenever viable or beneficial per AGENTS.md §5.1; it just does not need multi-wave orchestration.)
- **Single-step work** — one action, no decomposition, nothing to gate. system-instructions WHEN NOT TO USE lists it: handle directly without dispatch.
- **Already-covered work** — when one skill's trigger matches the task exactly, use that skill, not this one. Do not invent an orchestration layer over a one-skill task.
- **No subagents needed** — only when a task is purely trivial, non-substantive, or where subagents cannot add value.
- **Nothing to integrate** — a single deliverable with no recombination step has no reason for a wave structure.
- **Planning phase only** — a task that is still a goal, not a decomposition, goes to deep-planner first; this skill consumes a plan, it does not produce one.

## DECISION TREE

Branch top-down; the first match decides.

Before step 1, confirm the run is pre-authorized to proceed: task understood, confidence >= 80, an approved plan exists for non-trivial work (AGENTS.md plan-before-code), the tier is chosen per AGENTS.md §5, and every destructive action — plus any commit, push, or deploy — is user-approved per AGENTS.md §3.

Before any of that, determine the execution shape (AGENTS.md §5.1): subagents are mandatory whenever viable or beneficial. Assemble and deploy an appropriate set of subagents suited for the task on hand whenever it is good or best to use them.

1. **Decompose** — split the task into subtasks and produce a skill inventory per subtask: which skill owns that subtask's trigger family and which agent should be dispatched for it. The inventory is a table, one row per subtask:

```text
Subtask | Skill (trigger family) | Agent (from AGENTS.md roster) | Pass criterion | Evidence artifact
```

   A subtask with no matching skill is a research or planning gap — resolve it with deep-researcher or deep-planner before dispatch. Every subtask in the inventory maps to exactly one skill and one agent (smart routing, PATTERNS section 6). If two skills claim the same subtask, apply the precedence chain from system-instructions and pick the most task-specific.

   Each row also carries its **mandatory co-skills per AGENTS.md §7.1 relevance gate**: development subtasks load `test-driven-development` + `verification-before-completion`, security subtasks load a security skill, Roblox subtasks load the matching `roblox-*` skill (plus `roblox-studio-mcp` for any Studio execution). The inventory column is `Skill / co-skills`. A row that omits a mandatory co-skill fails its gate before dispatch — the relevance gate is checked at the same time as the pass criterion.

2. **Build the dependency graph** — draw edges between subtasks (what must finish before what) and identify the critical path. A subtask with no incoming edges is wave-1 material; anything downstream of it is not. Edges exist when one subtask writes state or artifacts another reads. If the graph has cycles, the decomposition is wrong — re-decompose, never deadlock the pipeline.

3. **Parallel vs sequential** — subtasks with no edge between them form one parallel wave, respecting the fan-out cap in QUANTITATIVE RULES; subtasks on a chain run sequentially, each waiting on its predecessor's gate. **When executing a parallel wave, the orchestrator MUST emit all independent subagents of that wave concurrently in a single turn with multiple `Agent` tool calls.** Never serialize independent subagents one by one when they can run concurrently. Never parallelize an edge. When in doubt, prefer sequential: a correct sequential run beats a broken parallel one.

4. **Dispatch via `Agent` tool per AGENTS.md in parallel** — the main thread orchestrates only; all file work, builds, tests, and browser automation go through subagents dispatched via the `Agent` tool. Direct implementation by the primary thread is strictly prohibited. When launching a wave of independent subtasks, **emit all `Agent` tool calls concurrently in a single message/turn to execute them in parallel**. Serializing independent subtasks sequentially is strictly prohibited. Check confidence >= 80 before dispatch (system-instructions delegation protocol); below 80, research more or ask the user — never dispatch on a guess. Every brief is a file under the temp dir, never pasted text, and states: the subtask, its pass criterion, the evidence artifact to produce, and the ledger entry to fill. Spawn each subagent exactly once.

5. **Verify per subtask** — when a subagent returns, compare its result against the brief's pass criterion and the attached evidence before accepting it (verification-before-completion). A failed gate stops the pipeline: apply the systematic-debugging sequence (reproduce, isolate, root cause, fix, regression test), re-verify, and only then continue. Do not accept the rest of a wave while a gate is red. If the subtask is high-stakes or its gate remains contested after one repair, escalate it to T2/T3 per AGENTS.md §5 and run it through debate-protocol rather than arguing in the ledger.

6. **Integrate** — once every gate is green, recombine the subtasks behind an integration smoke test, then write the final report in the format given in VERIFICATION GATE. Integration is itself a gate: a smoke failure returns the run to the failing integration step.

7. **Report and hand off** — emit the final report from the ledger (VERIFICATION GATE format), state the run status, and record any new skill or routing pattern discovered in the run (for example, a subtask family that recurs). Do not claim done with red or ungated rows; hand off only a fully gated run.

Worked example: a service deliverable decomposes into a schema change (A), an API route (B, depends on A), and a deployment script (C, depends on B). The skill inventory: A routes to db-architect / query-performance-engineer (pass criterion: migration applies cleanly and existing queries pass), B routes to api-architect / api-design-architect (pass criterion: OpenAPI contract renders and route tests pass), C routes to devops-engineer / devops-pipeline-engineer (pass criterion: pipeline dry-run succeeds). Waves: A alone, then B alone, then C alone — three sequential gates, no parallel violation, one integration smoke test at the end. Each gate carries its artifact into the ledger before the next wave dispatches.

## PATTERNS

### 1. Subagent routing via AGENTS.md roster
Route each subtask by its trigger family, not by habit. AGENTS.md §6 (roster) and §7 (routing map) map every skill to its owning agent; the owner is the default dispatch target for that subtask's trigger family.
Read the roster before wave 1 and let it drive the skill inventory from DECISION TREE step 1.

Full detail: `references/patterns.md`.

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX. All that apply must be checked at every checkpoint.

Full detail: `references/failure-modes-mitigations.md`.

## QUANTITATIVE RULES

Budgets for a single orchestration run. They exist to protect the orchestration context and keep gates reviewable.

Full detail: `references/quantitative-rules.md`.

## VERIFICATION GATE

This skill is verified by the gates it imposes on every orchestration run.

- **Pass criterion before dispatch**: every subtask brief states an explicit, checkable pass criterion before the subagent is dispatched. No criterion, no dispatch.
- **Checkpoint record**: at each gate and before each wave, write a checkpoint row to the ledger:

```text
CHECKPOINT {n}
Subtasks done: {x}   Gates green: {y}   Gates red: {z}
Evidence artifacts: {list}
Next action: {dispatch wave n+1 | fix subtask {id} | integrate}
```

  A checkpoint whose red count is nonzero and whose next action is not fix-or-rollback is a silent gate skip and must be corrected before continuing.

- **Per-subtask gate**: on return, the subagent's evidence is checked against the criterion (tests, logs, or other evidence — never looks-done per verification-before-completion). A red gate stops the pipeline: fix, re-verify, and record; a green gate records its artifact in the ledger.
- **Integration smoke test**: after all gates are green, recombine the subtasks and run one integration smoke test that exercises the assembled system end-to-end. A smoke failure returns the run to the failing integration step; gates are never skipped silently (verification-before-completion section 6).
- **Final report format:**

```text
[GENERAL ORCHESTRATOR — FINAL REPORT]
Task: {task description}
Subtasks:
  1. {subtask} — {status} — {gate evidence}
  2. {subtask} — {status} — {gate evidence}
  ...
Total: {X}/{Y} gates green
Failed gates: {list with rollback or retry actions}
Integration smoke test: {PASS|FAIL} — {artifact}
Status: {complete|blocked}
```

- **Definition of Done**: the run is done only when every applicable item in AGENTS.md §8 is ticked with attached evidence — tests pass, lint clean, review done, evidence attached. Any unchecked item means the run is not done.
- **Gate status vocabulary**: GREEN (criterion met, artifact attached), RED (criterion not met — fix or rollback before any further wave), FLAKY (passed on retry within budget, root cause still recorded), UNGATED (dispatched but never verified — treated as RED). Every ledger row ends in exactly one of these states at integration time; anything else is an incomplete run.
- **Anti-pattern coverage**: this skill explicitly forbids asserting without evidence (no green gate without an artifact), merging untested code (integration requires a fully green ledger), and skipping the plan (pre-run checklist requires one for non-trivial work). A gate row that displays any of these is itself a failed verification of this skill.

## REFERENCES

- AGENTS.md — short principles file and subagent roster; dispatch follows its roster, pipeline, and quality gates.
- system-instructions — operational doctrine this skill executes: delegation protocol, confidence thresholds, waiting protocol, trigger policy, precedence rules, verification gates.
- debate-protocol — escalation path when a subtask is T2/T3 or a gate stays contested after one repair (independent solver, test oracle, critic, chair).
- test-driven-development / verification-before-completion / systematic-debugging / requesting-code-review — gate protocols cited throughout.
- deep-planner + requirements-elicitation — plan/intent inputs this skill consumes.

Ownership: maintained by code-implementer; the skill is the delivery-domain flagship for gate-driven multi-skill execution.
