# general-orchestrator — PATTERNS

### 2. Gate-driven execution
Every subtask ends in a proof-based gate whose pass criterion was written into the brief before dispatch. A failed gate stops the pipeline at that subtask — apply the systematic-debugging sequence (reproduce, isolate, root cause, fix, regression test), re-run the gate, and continue only on green. Gates are never skipped silently: a gate failure returns the work to the step that failed.

### 3. Checkpoint cadence
Checkpoint at (a) every subtask gate that passes, (b) before dispatching the next parallel wave, and (c) before integration. At each checkpoint record: subtasks done, gates green, gates red, evidence artifacts. The checkpoint log is the dispatch ledger: it prevents duplicate dispatch (FAILURE MODES item 7), detects orphaned subtasks (item 3), and makes final-report assembly trivial. A run that skips checkpoints for five or more subtasks is running un-gated and must be re-planned (QUANTITATIVE RULES).

### 4. Verification per subtask
A subagent result is accepted only with attached evidence: test output, lint JSON, benchmark tables, or diff evidence (see verification-before-completion). Never accept looks-done sign-offs; screenshots are supporting material only, never the sole proof. If evidence cannot be produced, the subtask is not done — re-scope or escalate rather than wave it through. The gate checks the thing the brief required, not a convenient proxy.

### 5. Rollback on failed gate
When a gate fails and the fix exceeds the retry budget (QUANTITATIVE RULES), roll that subtask back to its last known-good state before re-dispatching, so the integration layer never sees a half-fixed subtask. Rollback is local to the failed subtask; it does not block the rest of the wave unless the dependency graph forces it. Record the rollback and its reason in the ledger — a rollback without a ledger entry is a silent failure (FAILURE MODES item 6).

### 6. Smart routing — no blanket-invoke
Match the skill and the agent to the subtask; do not blanket-invoke every available skill or agent. Blanket invocation wastes tokens, dilutes ownership, and erases the skill inventory that gates depend on. One skill plus one agent per subtask, chosen by trigger family (see AGENTS.md §6-7).

### 7. Brief template — the contract that makes gates checkable
A brief is a file, never pasted into a dispatch call. It carries everything the passer needs to accept or reject the result without re-deriving intent. Use this shape:

```text
BRIEF — {subtask id}
Skill: {skill from AGENTS.md roster}   Agent: {agent}
Dependency: {parent subtask ids, or none}
Pass criterion (checkable): {one measurable assertion}
Evidence artifact to produce: {file path for test/lint/diff}
Ledger entry to fill: {gate row id}
Scope: {deliverables; nothing outside this list}
Out of scope: {explicit exclusions, to prevent drift}
```

Writing the pass criterion and the evidence artifact at brief time is the difference between a gate and a hope. If you cannot fill every field, the subtask is not decomposed well enough to dispatch (DECISION TREE step 1).

### 8. Ledger discipline — the memory of the run
Keep one running ledger shared across checkpoints, one row per subtask: id, skill, agent, pass criterion, status, evidence artifact, rollback action. Every dispatch writes its row before the subset spawns; every gate writes its status and artifact when the subagent returns. The ledger is what makes duplicate dispatch, orphaned subtasks, and integration-without-gates detectable (FAILURE MODES items 3, 6, 7, 9). The final report in VERIFICATION GATE is a projection of the ledger — if the ledger is sound, the report writes itself.
