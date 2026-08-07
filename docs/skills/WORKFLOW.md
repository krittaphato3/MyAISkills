# WORKFLOW.md — Delivery Discipline

The delivery-discipline reference for the ZCode autonomous agentic coding system. This file is the detailed, executable companion to the WORKFLOW STANDARDS section of system-instructions v2. Every content task and the general-orchestrator cite it for Definition-of-Done and verification rules. Every item below is a checkable rule, not prose.

Precedence: when this file conflicts with another instruction, apply the precedence chain in AGENTS.md (task-specific skill > family skill > system-instructions > AGENTS.md > harness defaults).

Full protocols live in the superpowers workflow skills, referenced by name: test-driven-development, verification-before-completion, systematic-debugging, requesting-code-review.

## 1. Definition of Done (DoD) checklist

A task is DONE only when all applicable items are checked and the evidence is attached:

- [ ] Tests pass — full suite green for code work; proof-based verification for non-code work (rendered output, diff evidence, checkable artifacts)
- [ ] Lint clean — no errors beyond the recorded baseline (tools/skill_lint.py)
- [ ] Review done — red-team-qa at every phase gate and requesting-code-review for non-trivial changes, both passed
- [ ] Changelog recorded — the change appears in docs/skills/CHANGELOG.md
- [ ] Evidence attached — test output, benchmark tables, or review verdict cited in the report

Any unchecked item means the task is NOT done. DoD is agreed before implementation starts (system-instructions v2: Definition of Done before starting).

## 2. TDD protocol

1. Failing test — write a test that reproduces the requirement; run it and confirm it fails for the expected reason
2. Minimal implementation — the smallest change that makes the failing test pass
3. Refactor — clean up while keeping the suite green
4. Green — full suite passes; record the output as evidence

Exceptions (e.g., non-code work, environment-only changes) require written justification in the report: what was substituted for the failing test and why.

## 3. Verification-before-completion rules

- Done means evidence: test output, benchmark tables, lint JSON, review verdicts
- Screenshots are supporting material only — never the sole proof
- No "looks right" sign-offs; a claim without an attached artifact is not verified
- If evidence cannot be produced, the work is not done — escalate or re-scope

## 4. Measurement discipline

Any performance claim requires:

- Before/after benchmark on an identical workload
- Pinned environment: versions, hardware, configuration recorded
- At least 5 runs per configuration
- Median and p90 reported — never best-case-only

A claim without these four is an unmeasured optimization (anti-pattern, section 7).

## 5. Systematic debugging protocol

1. Reproduce — obtain a reliable failing case
2. Isolate — reduce to the minimal trigger; bisect inputs or config
3. Root cause — explain the mechanism, not the symptom
4. Fix — address the root cause; no symptom patches
5. Regression test — add a test that failed before the fix and passes after; run the full suite

## 6. Review gates

- red-team-qa at every phase gate — contradiction and completeness review
- requesting-code-review for non-trivial changes before merge
- Review verdicts are recorded in the task report
- A gate failure returns the work to the step that failed; gates are never skipped silently

## 7. Anti-vibe-coding anti-patterns

Each of these is a hard violation in delivered work:

- Asserting without evidence — claiming done with no test output, benchmark, or artifact
- Merging untested code — committing without a green suite or proof-based verification
- Screenshots as sole verification — visual capture with no measurable assertion (section 3)
- No-stop execution without gates — running past defined gates with no review checkpoints
- Symptom patches — fixing the visible failure while the root cause remains (section 5)
- Unmeasured optimizations — performance claims with no before/after numbers (section 4)
- Skipping the plan for non-trivial work — implementing without an approved plan (section 8)

## 8. Plan-before-code rule

- Non-trivial tasks require an approved plan before implementation: deep-planner or the writing-plans superpowers skill
- Trivial tasks (single-step, no dependencies, no state change) may skip the plan but still pass DoD
- The plan states goal, steps, gates, and DoD; deviations are recorded in the report
