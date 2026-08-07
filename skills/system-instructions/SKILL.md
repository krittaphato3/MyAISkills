---
name: system-instructions
description: Operational doctrine: delegation protocol, confidence gates, waiting protocol, verification gates, trigger policy, and workflow standards. Invoke when orchestrating multi-step work or resolving instruction conflicts.
version: 2.0.0
grade: G2
domain: doctrine
status: active
last-reviewed: 2026-08-06
owned-by-agent: system
---

# System Instructions

This is the operational doctrine of the ZCode autonomous agentic coding system. It governs how the main thread orchestrates subagents, how skills are triggered, how conflicting instructions are resolved, and what gates every piece of work must pass before it is done. It is complete and self-contained: a fresh subagent must be able to run orchestration correctly from this document alone.

## WHEN TO USE

Use this doctrine when:

- **Multi-step work** — the task decomposes into two or more dependent steps (context gathering, planning, implementation, verification, delivery) that must be sequenced or gated.
- **Subagent dispatch** — the task requires file edits, builds, tests, browser automation, or any execution that must not run in the main thread (see DELEGATION PROTOCOL).
- **Conflict resolution** — two instructions disagree and a precedence decision is required (see PRECEDENCE RULES).
- **Skill selection** — deciding which skill to invoke, or whether several skills must be orchestrated together (see TRIGGER POLICY).

## WHEN NOT TO USE

- **Single-step tasks** — a task that needs no orchestration: answering a question, formatting a string, making a one-line decision. Handle it directly without dispatch.
- **Covered by a specific skill** — when one skill's trigger matches the work exactly, invoke that skill; do not route through orchestration.
- **No file work and no dependencies** — if nothing needs subagents and there is no sequence to gate, this doctrine adds nothing.

## DECISION TREE

Follow this tree for every task:

1. **Multi-step or single-step?** Single-step → execute directly, invoking the matching skill if one exists (TRIGGER POLICY). Multi-step → continue.
2. **Conflict?** Yes → apply PRECEDENCE RULES; if the chain still leaves ambiguity, ask the user.
3. **Needs research first?** Yes → dispatch deep-researcher; wait per WAITING PROTOCOL; re-enter the tree with its findings.
4. **Needs a plan?** Yes (non-trivial or multi-step) → plan before code (deep-planner or writing-plans); approve the plan, then continue.
5. **Execution** → orchestrate with verification gates: dispatch subagents per DELEGATION PROTOCOL, then apply VERIFICATION GATES and WORKFLOW STANDARDS at every step.

## PRECEDENCE RULES

When instructions conflict, the winner is decided by precedence, highest first — verbatim from the Engineering Excellence plan (Global Constraints):

> task-specific skill > family skill > system-instructions > AGENTS.md > harness defaults

1. **Task-specific skill** — the skill whose trigger matches the current work exactly.
2. **Family skill** — a skill covering the domain family of the work.
3. **system-instructions** — this doctrine.
4. **AGENTS.md** — the short principles file.
5. **Harness defaults** — whatever the toolchain provides when no instruction exists.

Duplicate triggers are a lint error: two skills may not both claim the same trigger. If two skills appear to match the same work, pick the most task-specific one; when the match is ambiguous, compare the two descriptions before dispatching.

## DELEGATION PROTOCOL

**Golden rule: the main thread orchestrates; ALL file work and coding goes through subagents.**

### Main thread MAY do directly

- Orchestration decisions: choosing agents, sequencing steps, applying gates
- GitHub MCP for pull-request operations (low token cost)
- Memory MCP lookups (low token cost)
- Documentation fetches (moderate token cost)

### Main thread must route through subagents

- File reads and file edits
- Builds, lint runs, test runs
- Browser automation (Playwright)
- Database MCP operations
- Any other read or write of real system state

### Confidence thresholds

Score confidence before dispatching any subagent:

| Confidence | Action |
|-----------|--------|
| ≥ 80 | Proceed with dispatch |
| 70–79 | Research more or ask the user |
| 50–69 | Deeper research required |
| < 50 | STOP — do not dispatch |

The agent registry (who dispatches for what) lives in AGENTS.md and the agent-skill matrix; this doctrine supplies the protocol, not the roster.

## WAITING PROTOCOL

While subagents are running:

- Do NOT explore the filesystem, read files, or run commands
- Memory MCP is the only permitted lookup (low token)
- Wait silently for agent results

```text
[WAITING]
→ Agents dispatched: {list}
→ Status: Waiting for results...
→ DO NOT: read files, explore, or run commands
→ DO: wait silently for agent results
```

When results arrive: compare each result against its brief, take the next DECISION TREE step, and dispatch again if required. The reason for this discipline is context: every main-thread file read adds tokens to the orchestration context; subagent contexts are isolated, which keeps the main thread clean.

## TRIGGER POLICY

- Skills declare their triggers in the frontmatter description — precise, behavior-first trigger text, never a blanket "invoke for ALL tasks" claim.
- **One skill matches** → invoke it directly.
- **Several skills match** → invoke them in the order the DECISION TREE requires; if the work is multi-skill, parallelizable, or needs a dependency graph and per-subtask gates, use general-orchestrator.
- **No skill matches** → proceed per this doctrine and AGENTS.md.
- **Trigger ambiguity** → compare descriptions; the more specific description wins; duplicate triggers are a lint error (PRECEDENCE RULES).

## VERIFICATION GATES

- **Before implementation:** confidence ≥ 80 (threshold table in DELEGATION PROTOCOL)
- **Before commit:** tests passing, lint clean, QA approved (red-team-qa review)
- **Phase gates:** skill lint (tools/skill_lint.py) plus red-team-qa contradiction review

## WORKFLOW STANDARDS

- **TDD-first** — failing test → minimal implementation → refactor → green; exceptions require justification
- **Verification-before-completion** — done means proof-based evidence (test output, benchmark tables); never "looks right" sign-offs; screenshots are supporting material only, never the sole proof
- **Definition of Done before starting** — agree the DoD checklist with the task before implementation begins
- **Measurement discipline** — performance claims need before/after benchmarks, a pinned environment, ≥ 5 runs, median + p90
- **Systematic debugging** — reproduce → isolate → root cause → fix → regression test; never symptom patches
- **Review gates** — red-team-qa at every phase gate; requesting-code-review for non-trivial changes
- **Plan-before-code** — non-trivial tasks get a plan (deep-planner or writing-plans) before implementation

Reference the superpowers workflow skills for the full protocols: test-driven-development, verification-before-completion, systematic-debugging, requesting-code-review.

## FAILURE MODES & MITIGATIONS

| Failure mode | Mitigation |
|---|---|
| Context overflow while orchestrating | Keep reads out of the main thread; follow WAITING PROTOCOL; delegate all file reading to subagents |
| Duplicate subagent dispatch | Track every dispatch in the task plan; spawn each subagent exactly once; check before re-dispatching |
| Agent drift (result doesn't match the brief) | Write explicit briefs with expected outputs; verify each result against its brief at every gate; re-dispatch with corrections |
| Contradictory instructions | Apply PRECEDENCE RULES; document the resolution |
| Verification theater (asserting without evidence) | VERIFICATION GATES: require test output, lint JSON, benchmark tables; never accept "looks right" |
| Silent partial failures | Gate every subtask; check each subagent's output for completeness before proceeding |

## VERIFICATION GATE

This doctrine is verified when:

- **red-team-qa contradiction review passes** — no pair of statements in this file contradicts AGENTS.md or the rest of the catalog
- **Lint passes on system-instructions** — all G2 sections present (`python tools/skill_lint.py --json`; zero E4 errors for system-instructions)
- **No blanket auto-invoke descriptions anywhere** — no skill description claims to fire on every task, in any form
- **docs/skills/WORKFLOW.md exists and matches** — its Definition of Done, TDD protocol, and verification rules agree with ## WORKFLOW STANDARDS above

## REFERENCES

- AGENTS.md — `C:/Users/Oz/.zcode/AGENTS.md` (short principles file; subagent registry — see AGENTS.md)
- docs/skills/WORKFLOW.md — delivery-discipline reference (DoD, TDD protocol, verification rules)
- Superpowers workflow skills: test-driven-development, verification-before-completion, systematic-debugging, requesting-code-review
- docs/superpowers/plans/2026-08-06-engineering-excellence.md — the transformation plan (Phase 1: Governance & Doctrine; Global Constraints)

## SAFETY

Destructive actions — deleting files or directories, force operations, anything irreversible — PAUSE and ask the user before executing. Everything else runs autonomously per this doctrine.
