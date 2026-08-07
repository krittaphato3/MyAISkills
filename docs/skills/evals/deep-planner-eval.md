# deep-planner — Flagship Eval

## 1. Trigger test

Fire (5):
1. "Turn this spec into an executable plan for a 6-service migration with dependencies."
2. "Decompose this goal into a task graph with a critical path and estimate each task with a range."
3. "Produce a plan general-orchestrator can execute, with per-task acceptance criteria."
4. "Plan a dependency-heavy backend migration across multiple milestones/checkpoints."
5. "Given a confirmed intent, hand off a plan with a risk register and fan-out constraints."

Not fire (3):
6. "Fix this one-line typo in a config." — no graph needed.
7. "Write the code for task 3 right now (that's general-orchestrator execution)."
8. "Brainstorm/confirm intent for an unclear ask (that's requirements-elicitation)."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — step-0 clarity gate, decompose, dependency graph, estimate, risk register, review, handoff.
(b) failure modes have detection+mitigation: 5/5 — over-decomp, under-spec, hidden-deps, estimation-optimism-with-actuals, orphan, drift, cycle, unclosed-risk, detail-inversion, drift all DETECT/FIX.
(c) quantitative rules are numbers: 5/5 — S=0.5-1d/M=1-3d/L=3-5d/XL=5-10d, planning 10-15%, fan-out, re-plan <20% slip, High×High blocker.
(d) verification gate executable: 5/5 — task-testable, acyclic, critical-path computed, risk-mitigated, measurable; handoff shape has no blank cell.
(e) references authoritative: 4/5 — writing-plans, reference-class, cone-of-uncertainty, CPM/weighted; solid but some are secondary/training-recalled.
(f) no contradictions: 5/5 — explicit edges to requirements-elicitation, deep-research, general-orchestrator consistent with doctrine.

## 3. Reference task
Turn a 6-service migration into an executable plan: decompose into testable tasks, map deps (which must finish before which), compute a critical path, give ranges, register 3 risks with triggers, and emit a task-table + critical-path + risk-register with no blank cell.
