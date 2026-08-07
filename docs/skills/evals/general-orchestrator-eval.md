# general-orchestrator — Flagship Eval

## 1. Trigger test

Fire (5):
1. "Backend service needs a schema change, an OpenAPI route, and a deploy script in one delivery — decompose, dispatch, gate."
2. "Route these 4 independent subtasks to parallel subagents and recombine them after a smoke test."
3. "A subtask that writes a file that another subtask reads — build a dependency graph and sequence the waves."
4. "Dispatch a multi-skill task whose trigger spans several skills (db + API + devops)."
5. "Gate each subtask result with evidence artifacts and gate the whole run before merge."

Not fire (3):
6. "Fix this one CRUD endpoint bug in a single file (single-step)."
7. "Add query-index guidance to one sub-service (one skill only)."
8. "Plan a 6-service migration (that's deep-planner's job, not this executor)."

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — decompose, dependency graph, parallel-vs-seq, dispatch, verify per subtask, integrate, report; worked example.
(b) failure modes have detection+mitigation: 5/5 — agent-drift, context-overflow, orphan-gate, verification-theater, parallel-violation, duplicate-dispatch, integration-without-gates all DETECT/FIX.
(c) quantitative rules are numbers: 5/5 — fan-out ≤5 (cap 8), retry ≤2, green gate ≥1 artifact, confidence ≥80, granularity ≤10 subtasks.
(d) verification gate executable: 5/5 — checkpoint ledger rows, per-subtask gate, integration smoke, final report format.
(e) references authoritative: 4/5 — cites AGENTS.md/system-instructions/WORKFLOW/matrix (internal doctrine); those are authoritative for this repo.
(f) no contradictions: 5/5 — explicitly reconciles deep-planner handoff, WORKFLOW gates, system-instructions; no doctrine conflict; keep-checkpoint cadence consistent.

## 3. Reference task
The orchestrator must route a service delivery that decomposes into A (schema change), B (API route, depends on A), C (deploy script, depends on B) across 3 proven agents. It should emit the 3-subtask skill inventory table with per-agent, pass-criterion, evidence; order the waves A→B→C; gate each result at its pass criterion; run one integration smoke test; and emit the final [GENERAL ORCHESTRATOR] report.
